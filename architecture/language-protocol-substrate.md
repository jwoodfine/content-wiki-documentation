---
title: "The Language-Protocol Substrate"
slug: language-protocol-substrate
category: architecture
last_edited: 2026-06-29
editor: pointsav-engineering
status: stable
references:
  - id: 1
    text: "Padmakumar, V. et al. Does Writing with Language Models Reduce Content Diversity? arXiv:2310.06992, 2023."
    url: "https://arxiv.org/abs/2310.06992"
---

The **language-protocol substrate** is a metadata classification layer governing how editorial
content is categorised, routed, and processed across the Foundry workspace. Every draft
artifact carries a `language_protocol:` declaration in its frontmatter. That declaration is
the machine-readable instruction that determines which gateway processes the artifact, which
vocabulary rules apply, and which destination receives the finished article. The substrate does
not store content and does not own processing logic — those responsibilities belong to git and
to the gateway projects, respectively.

## Architectural grounding

The substrate sits on three interconnected mechanisms:

**`foundry-draft-v1` schema** — the frontmatter envelope that every draft artifact carries.
The schema requires a `language_protocol:` field, a `destination:` field, and a `route_to:`
field. These three fields are the machine-readable routing instructions; the schema enforces
their presence at staging time.

**Routing table** — the workspace-level classification file that maps `language_protocol:`
values to gateway projects and destinations. A draft declaring `language_protocol: TOPIC-*`
resolves to the `project-editorial` gateway and the documentation wiki destination. This file
is the single source of truth for routing; no archive hard-codes routing logic for another
archive's artifacts.

**Archive notification convention** — the protocol by which outbox messages carry draft
routing intent. A draft staged to `.agent/drafts-outbound/` generates an outbox message
addressed to the appropriate gateway session. The relay picks it up within 15 minutes; no
manual relay step is required.

The substrate differs from a content management system in two ways. It does not store content
— content lives in git, in the receiving archive's tracked directories. It does not own
routing logic — each gateway project implements its own pipeline against the incoming draft
shape. The substrate makes content machine-routable across archives without requiring archives
to know each other's internals. It also differs from a language server protocol: a language
server protocol defines a real-time bidirectional session. The language-protocol substrate has
no session state. The `language_protocol:` declaration on a draft artifact is a per-artifact
stamp, made once at staging time, that travels with the artifact through every hand-off.

## Why explicit protocol selection

The substrate's foundational design choice is to require the caller to declare a language
protocol on every editorial request rather than auto-detecting one from the input. A 2023
Cornell study found that auto-detection of writing style narrows the space of voices a model
produces — the detection step homogenises outputs toward the model's expectation of the genre
rather than the author's own register.[^1] Explicit selection sidesteps this: the operator
declares the intended register at the request boundary, and the pipeline applies genre-specific
rules from that declared position. The operator knows what register they are writing in; the
substrate reflects that knowledge structurally.

## The four genre families

Four genre families are defined, each with its own banned-vocabulary list, register-tightening
targets, and Stage-1 scan rules:

- **PROSE** — general editorial: articles, technical documentation, architecture TOPICs.
  Targets Bloomberg-article register; bans AI-product marketing vocabulary and vague hedge
  phrases.
- **COMMS** — external communications: investor letters, press releases, public statements.
  Additional formality constraints; continuous disclosure posture applies where applicable.
- **LEGAL** — contracts and legal instruments. Precision-first; minimal paraphrase; specific
  disallowed-synonym list to prevent unintended meaning drift.
- **TRANSLATE** — bilingual production: the `.es.md` pass for TOPIC and GUIDE articles.
  Flag-don't-rewrite applies strictly; the human translator is the authority.

## Three-stage pipeline composition

`service-proofreader` composes three stages on every `/v1/proofread` call:

1. **Banned-vocabulary scan** — rule-driven; deterministic; sub-millisecond; flags only,
   never rewrites
2. **LanguageTool 6.6 mechanical pass** — spelling, grammar, and style; runs as a Docker
   companion; findings serialised to JSON for Stage 3
3. **Doorman generative pass** — register-tightening whole-text rewrite via the Doorman
   (service-slm); reads Stage-2 findings as inline JSON context; produces a complete rewrite

See [[editorial-pipeline-three-stages]] for the full pipeline specification, including
inline JSON flow, severity discriminants, and degradation paths.

## Flag-don't-rewrite default

The `/v1/proofread` response carries a structured `findings` array; the caller decides what to
apply. The substrate never silently rewrites the operator's text. An Apply-all action is
opt-in per request, not a default. This is a deliberate sovereignty boundary: the substrate
refines, flags, and suggests — the operator retains the final text.

## Operator verdict closes the apprenticeship loop

After reviewing the Stage-3 rewrite, the operator records one of three dispositions:
`accepted`, `rejected`, or `edited` (with the final text of their choice). The verdict feeds
the apprenticeship corpus event-pair — `draft-created` → `draft-refined` → `creative-edited`
— per the reverse-funnel editorial pattern. Stage-1 DPO pairs derive directly from the
`(input, chosen-rewrite, operator-disposition)` tuple. The substrate is both the editorial
tool and the data-collection layer for continued model training; these two functions are
inseparable by design.

## Tenant separation in the corpus

Corpus output is routed per tenant by path: records for the vendor account write to the
workspace-tier corpus root; records for customer accounts write to the customer tenant's
deployment instance directory. Tenant mixing is structurally impossible because the path
component is the boundary. No runtime flag or configuration controls this separation; it is a
property of the directory layout.

## What the substrate does not do

- Does not auto-detect protocol — the operator declares at the request boundary
- Does not silently rewrite — the operator chooses which findings to apply
- Does not embed Tier-C API keys in the proofreader binary — keys live with the Doorman
- Does not train on tenant text by default — the no-train contract is enforced at the corpus
  write layer, not at the request layer

## See also

- [[editorial-pipeline-three-stages]] — the three-stage pipeline in full detail
- [[customer-tier-catalog-pattern]] — how deployment instances are provisioned to run
  the pipeline
