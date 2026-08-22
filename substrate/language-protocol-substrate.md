---
schema: foundry-doc-v1
title: "Language-protocol substrate"
slug: language-protocol-substrate
category: substrate
type: topic
content_type: topic
quality: complete
index_group: core-named-substrates
short_description: "The routing mechanism that carries a draft's declared register, document type, and destination between archives — a frontmatter field, a routing table, and a mailbox convention, not an AI adapter system."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-08-22
editor: pointsav-engineering
cites:
 - ni-51-102
 - osc-sn-51-721
paired_with: language-protocol-substrate.es.md
---

Every draft artifact moving through the PointSav platform — a wiki article, a README, a legal correction, a translation — declares its register, document type, and destination up front rather than having those inferred later. That declaration is the language-protocol substrate: a frontmatter field, a routing table, and a mailbox convention, not an AI system.

The substrate has two real, separate layers. The **routing layer** — described in full below — is genuinely operational: every staged draft carries a `language_protocol` value, a workspace-level table maps that value to the archive that owns it, and a mailbox message picks up the hand-off automatically. The **register-and-schema layer** — what a PROSE or LEGAL document must contain, and which words it may not use — lives as data, not code: YAML token files in `pointsav-design-system` (one register file per wiki, e.g. `register-documentation.yaml`; one banned-vocabulary list per wiki; one schema per content type — TOPIC, GUIDE, JOURNAL) that an editorial-lint script reads and checks drafts against before they publish. There is no unified "four-family adapter taxonomy," no LoRA adapter composed per request, and no single Rust crate that owns schema, templates, and validation together — those are three real, separate mechanisms this article previously described as one integrated system.

## The four protocol values — real, and how they actually route

`PROSE-*`, `COMMS-*`, `LEGAL-*`, and `TRANSLATE-*` are real `language_protocol` values a staged draft's frontmatter carries. Two gateway archives own the routing: `project-editorial` receives PROSE/COMMS/LEGAL/TRANSLATE, `project-design` receives DESIGN-*. A draft is staged with `foundry-draft-v1` frontmatter (language protocol, destination, routing field), and a mailbox message-prefix convention carries the routing intent to the owning archive automatically — no manual hand-off. This is the mechanism this article's own architecture section (below) already described accurately.

What is not real: an AI system that composes a base model with a per-tenant "brand voice" adapter and a per-protocol adapter at inference time, or that produces "eighteen genre templates" and "eight cross-genre prohibited terms" from a shared Rust crate. The register and schema content that actually governs each protocol's output is per-wiki YAML — currently 3 content-type schemas (TOPIC, GUIDE, JOURNAL) and one banned-vocabulary list per wiki, not a single cross-genre taxonomy of eighteen templates.

## Where the register and schema content actually lives

`pointsav-design-system/tokens/linguistic/` holds one register file per wiki (defining section structure, tone, and accessibility rules) and one banned-vocabulary file per wiki (retired internal terms, each with an approved plain-language replacement). `pointsav-design-system/tokens/content-schema/` holds the frontmatter and structural schema for each content type. `project-editorial` is the content-steward of this token subtree — it drafts and applies these files, though committing changes to them routes through `project-design`, which holds the mechanical commit gate.

`editorial-lint.py` (owned by `project-editorial`) reads these token files directly and checks a draft's structure and vocabulary against them before it can be committed. This is a lint script run at commit time, not an inference-time adapter or a service any other component calls at request time.

## `service-proofreader` — a real, separately-deployed service

`service-proofreader` is a real, running interactive write-assist service (`local-proofreader.service`, port 9092) — but it is not a crate inside `pointsav-monorepo`, and it is not one leg of a four-service split alongside `service-content`/`service-slm`. It is its own deployment, reachable from the [[radical-proofreader-ui|proofreader console]] terminal cartridge, and it dispatches its generative pass through the Doorman like any other inference caller. Whether every editorial action anywhere on the platform produces a verdict-signed training tuple through it, as previously claimed, is not confirmed — that claim described a broader integration than what is verified here.

## Multi-tenant via moduleId namespacing

One `service-content` instance per platform deployment, with `moduleId` partitioning tenants inside. Per-tenant isolated deployment is the escalation path — when a customer needs key-management-per-tenant or stronger isolation, they spin up their own platform instance in their own infrastructure and get their own `service-content` there.

This is the meaning of "tenant escalation happens at the deployment boundary, not the service-naming boundary." The service stays multi-tenant; the deployment topology grows isolation when warranted.

## Architectural grounding

The substrate sits on three interconnected mechanisms.

The `foundry-draft-v1` schema is the frontmatter envelope every draft artifact carries. It
requires a language-protocol field, a destination field, and a routing field — the
machine-readable instructions the schema enforces at staging time. A workspace-level routing
table maps each protocol value to a gateway project and destination; the table is the single
source of truth for that mapping, so no archive hard-codes routing logic for another archive's
artifacts. A mailbox message-prefix convention then carries the routing intent between
archives: a staged draft generates an outbound message that a relay picks up automatically,
with no manual hand-off step required.

The substrate differs from a content management system in two ways. It does not store content
— content lives in git, in the receiving archive's tracked directories. It does not own
routing logic — each gateway project implements its own pipeline against the incoming draft
shape. The substrate makes content machine-routable across archives without requiring
archives to know each other's internals. It also differs from a language-server protocol:
a language-server protocol defines a real-time bidirectional session, while the substrate has
no session state — the protocol declaration on a draft is a per-artifact stamp, made once at
staging time, that travels with the artifact through every hand-off.

## Why explicit protocol selection

The substrate's foundational design choice is to require the caller to declare a language
protocol on every editorial request rather than auto-detecting one from the input. A 2023
Cornell University study on writing-style auto-detection found that automatically inferring
style from input text narrows the range of voices a model produces — the detection step
homogenizes output toward the model's expectation of the genre rather than the author's own
register. Explicit selection sidesteps this: the operator declares the intended register at
the request boundary, and the pipeline applies genre-specific rules from that declared
position. The operator already knows what register they are writing in; the substrate
reflects that knowledge structurally rather than inferring it.

## Auditing editorial work done outside the Doorman

A cluster that does editorial work locally — without routing the request through the Doorman — can still push a record of it into the central audit ledger with a single call. The event carries a type tag: `prose-edit` for editorial work, plus `design-edit`, `graph-mutation`, `anchor-event`, and `verdict-issued` for other work classes the same endpoint covers. This keeps the ledger complete even when work happens off the Doorman's own request path — it does not, by itself, generate a training tuple; only work that actually routes through the Doorman's apprenticeship pipeline does that.

Per `[ni-51-102]` continuous-disclosure language and in accordance with the forward-looking information principles of `[osc-sn-51-721]`: whether every editorial action across the platform eventually produces a verdict-signed training tuple for a customer's own adapter is a planned target, not a confirmed current behavior.

## See also

- [[customer-hostability]]
- [[anti-homogenization-discipline]]
- [[apprenticeship-substrate]]
- [[citation-substrate]]
