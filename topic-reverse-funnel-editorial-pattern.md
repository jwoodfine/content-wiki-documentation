---
schema: foundry-doc-v1
title: "The Reverse-Funnel Editorial Pattern"
slug: topic-reverse-funnel-editorial-pattern
category: architecture
status: pre-build
last_edited: 2026-04-28
editor: pointsav-engineering
cites:
  - ni-51-102
  - osc-sn-51-721
  - constitutional-ai-2212-08073
  - olmo3-allenai
  - llguidance
  - knowledge-commons-wiki
---

The substrate inverts the conventional editorial cycle. Most
publishing pipelines put the human Creative at the start of the
loop — drafts the manuscript, hands to copy-editor, ships to
readers. Foundry's substrate puts the Creative at the END of the
loop. Cluster Tasks ship rough drafts forward to a single editorial
gateway; the gateway refines to register; the refined version goes
live; Creative Contributors edit the published file; their edits
feed the next training cycle as preference data. This is the
inversion that lets a small Creative team scale to a substrate the
size of Wikipedia.

## Definition

The Reverse-Funnel Editorial Pattern is a publishing discipline
where:

1. Multiple originating clusters produce **bulk drafts** —
   technically accurate, freely-cited, rough register.
2. A single editorial gateway (`service-language`, the
   project-language cluster) refines every draft to production
   register: banned-vocabulary enforcement, BCSC continuous-
   disclosure posture, bilingual pair generation, citation registry
   resolution.
3. Refined version publishes immediately to the destination repo.
4. Creative Contributors enter at the **end** — they edit the
   published file. Their edits become the second leg of a
   preference pair.
5. Quarterly continued pretraining on the corpus of (raw → refined
   → creative-edited) tuples produces a substrate baseline that
   drifts closer to (refined ⊕ Creative) over time.

The pattern is the inverse of standard editorial workflow.
Standard: human writes, machine assists. Reverse-funnel: machine
drafts, human refines, both signals train the substrate.

## How the substrate operates

The substrate runs three input ports:

- Cluster Task drafts at `~/Foundry/clones/<cluster>/.claude/drafts-outbound/`
- Root drafts at `<repo>/.claude/drafts-outbound/`
- Master drafts at `~/Foundry/.claude/drafts-outbound/`

`bin/draft-sweep.sh` walks all three at session start;
project-language picks up `state: draft-pending-language-pass`
items in priority order. Each draft carries `foundry-draft-v1`
frontmatter declaring originating cluster, target repo, audience,
BCSC class, language protocol, and `notes_for_editor`. The draft
body is bulk — references inline as URLs, repetition allowed,
register discipline NOT enforced. project-language enforces.

Refinement applies four disciplines deterministically:

1. **Banned-vocabulary grammar** — Lark EBNF declares forbidden
   editorial terms; `validate.py` (Phase 1B) and decode-time
   enforcement via `[llguidance]` (AS-2 pending) make violations
   grammatically impossible.
2. **BCSC continuous-disclosure posture** — forward-looking claims
   carry planned / intended / may language, cautionary framing, and
   reasonable-basis blocks per `[ni-51-102]`.
3. **Citation registry resolution** — inline URLs in the bulk
   become `[citation-id]` references resolved against
   `~/Foundry/citations.yaml`.
4. **Bilingual pair generation** — Spanish strategic adaptation
   per DOCTRINE.md §XII (overview, not 1:1 translation).

Refined output hands off to the destination repo via the standard
`handoffs-outbound.md` mechanism. Three JSONL events emit to the
apprenticeship corpus: `draft-created` (originator),
`draft-refined` (project-language), `creative-edited` (originator
after publish + Creative edit).

## Why hyperscaler-managed AI cannot replicate

Three structural reasons.

**1. Per-tenant SLM continued-pretraining is structurally absent.**
Multi-tenant SaaS LLMs run a single editorial regime across all
customers. A Creative's edits in one tenant cannot feed an SLM
that personalises responses for that tenant only — the model is
shared. The Reverse-Funnel pattern's compounding loop closes only
when the SLM has tenant-private adapters and tenant-private
training corpus.

**2. Per-tenant editorial-floor adapters are structurally absent.**
Banned-vocabulary grammars, BCSC discipline templates,
language-protocol adapters are tenant-specific. Hyperscaler
products expose neither grammar composition nor adapter
composition primitives. Tenants get structured-output modes, not
"here is your tenant's grammar that loads at inference time."

**3. The closed loop demands tenant-sovereign training data.**
Even if a hyperscaler captured Creative edits, the resulting
training data feeds a tenant-neutral or vendor-specific model.
Tenants cannot own a model that becomes literate in their own
voice. The compounding loop demands the
`[constitutional-ai-2212-08073]`-style training-data sovereignty
that the multi-tenant LLM business model structurally cannot grant.

## What this enables in Foundry

The Compounding Substrate's editorial path closes a continued-
pretraining loop on craft, not just structure:

- The apprenticeship-substrate (Doctrine claim #32) closes the
  loop on **structural correctness** — apprentice diff → senior
  verdict → Stage-1 DPO pair.
- The Reverse-Funnel pattern closes the loop on **editorial craft**
  — refined draft → creative-edited → Stage-2 DPO pair.
- Both stages feed the same OLMo `[olmo3-allenai]` continued-
  pretraining corpus.

After enough cycles, the substrate produces draft baselines at
80% → 90% → 95% of Creative's craft level. Creative load drops
monotonically; their scope expands. They move upstream to brand
strategy, architectural framing, novel-form authorship — work the
substrate cannot reach yet.

## Three-Tier Contributor Model — explicit mapping

The Three-Tier Contributor Model `[knowledge-commons-wiki]`
(Core / Paid / Open) maps onto the cycle position:

- **Core** (4-7 operators): operate the substrate; cluster Tasks;
  doctrine; throughout the cycle
- **Paid** (50-100 Creative Contributors): edit the published
  refined version at the END of the cycle; craft + brand + voice
- **Open** (10K+ wiki consumers): consume + cite + fork outside
  the cycle

Paid contributors in this pattern are not tech writers. They are
craft specialists — designers, narrative editors, brand-voice
contributors. The recruitment profile optimises for taste, not
technical synthesis. The substrate-generated draft supplies the
technical floor; the Creative's job is to raise the ceiling.

Each tier works at a distinct timescale: Core in real-time
(sessions per day); Paid per-publication-event (edits per
refined-publication batch); Open per-consumption-event (citations
and forks over months and years).

## Operational implications

Recruitment shifts. Because the substrate-generated draft already
carries accurate technical content, Paid-tier contributors do not
require deep engineering background. The hiring profile shifts
toward craft discipline: narrative specialists, brand-voice
editors, illustration contributors.

Quality control simplifies. The substrate floor is verifiable
mechanically — banned-vocabulary violations are caught before
publication; BCSC posture is enforced by grammar, not by auditor.
Human QC focuses on brand alignment, narrative coherence, and
graphics rendering rather than factual accuracy. Most accuracy
verification is automated.

Per-tenant voice distils into per-tenant adapters. As
creative-edited preference pairs accumulate on a given tenant's
namespace, the tenant adapter learns the tenant's voice.
Subsequent drafts on that namespace arrive closer to the tenant's
established baseline without additional human instruction. This is
Adapter Composition Algebra (Doctrine claim #22) applied to the
editorial layer.

## Forward-looking — pending substrate work

Per `[ni-51-102]` and `[osc-sn-51-721]` continuous-disclosure
language, the trajectory below is `planned` and `intended`.
Material assumptions include continued availability of OLMo
open-weight models under Apache 2.0 licensing, sufficient
Creative-edited corpus volume to support meaningful DPO fine-
tuning, and uninterrupted operation of the project-language
editorial gateway. Actual outcomes may differ.

- AS-2 (project-slm Task) intends to integrate `[llguidance]`
  into the Doorman so vLLM Tier B accepts
  `extra_body.structured_outputs.grammar`. service-language is
  the planned primary consumer.
- Per-tenant Creative-voice adapters are intended to distil from
  accumulated Stage-2 DPO pairs over the first year of operation.
- The Stage-1 + Stage-2 OLMo continued-pretraining run targets a
  quarterly cadence.
- Creative-tier recruitment is planned to begin after the first
  batch of refined TOPICs publishes; the first cycles are
  operator-edited as bootstrapping data.

## See also

- [The Compounding Substrate](topic-compounding-substrate.md)
- [The Apprenticeship Substrate](topic-apprenticeship-substrate.md)
- [Decode-Time Constraints](topic-decode-time-constraints.md)
- [The Three-Tier Contributor Model](topic-contributor-model.md)
- The conventions:
  `~/Foundry/conventions/reverse-funnel-editorial-pattern.md`
  `~/Foundry/conventions/cluster-wiki-draft-pipeline.md`
- The sweep helper:
  `~/Foundry/bin/draft-sweep.sh`
