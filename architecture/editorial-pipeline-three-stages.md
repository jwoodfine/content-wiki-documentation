---
title: "The Three-Stage Editorial Pipeline"
slug: editorial-pipeline-three-stages
category: architecture
last_edited: 2026-06-29
editor: pointsav-engineering
status: stable
---

The **three-stage editorial pipeline** is the processing sequence that `service-proofreader`
applies to every `/v1/proofread` request. Each stage is independent, has a defined input
shape, and produces a structured finding set. The stages run in order: cheap deterministic
rules first, mechanical grammar analysis second, and generative rewriting third. The
cost-discipline rationale is direct — Stage 1 terminates the request early on clear
violations; Stage 2 mechanical findings are embedded in the Stage 3 prompt, preventing the
model from re-discovering errors the rule pass already catalogued.

## Why three stages, in this order

The ordering reflects three distinct cost and reliability profiles. Stage 1 is deterministic
and has no external dependency; it completes in sub-millisecond time and cannot fail due to
infrastructure. Stage 2 calls a locally deployed LanguageTool instance and can degrade
gracefully if that service is unreachable. Stage 3 routes through the Doorman to one of three
compute tiers and is the only stage subject to latency and cost variance.

Each stage produces an independently verifiable finding set. An operator reviewing a
`/v1/proofread` response can attribute each flag to the stage that produced it — a
banned-vocabulary hit from Stage 1 carries different authority than a style suggestion from
Stage 3.

## Stage 1 — Banned-vocabulary scan (deterministic, rule-driven)

Stage 1 is a pure text scan against the workspace's banned-vocabulary lists. Four genre
families are defined — PROSE, COMMS, LEGAL, and TRANSLATE — each with its own list of
disallowed terms, AI-product marketing vocabulary, and vague hedge phrases. A match produces a
`Severity::Banned` flag with the matched span, the family that triggered the match, and a
replacement hint where one exists. Stage 1 flags only; it never rewrites. The disposition
remains with the operator.

## Stage 2 — LanguageTool 6.6 mechanical pass (Docker companion)

Stage 2 calls the LanguageTool 6.6 HTTP API running as a Docker companion service co-located
with the proofreader binary. LanguageTool handles spelling, grammar, punctuation, and style
rules too numerous to enumerate as a static list. The response is normalised: each LanguageTool
rule match is mapped to the proofreader's internal `Finding` type, assigned
`Severity::Mechanical`, and annotated with the matched span, the rule identifier, and the
suggested replacement. The full Stage-2 finding set is then serialised to JSON for Stage-3
consumption.

## Stage 3 — Doorman generative pass (service-SLM via Tier A/B/C)

Stage 3 routes through the Doorman (service-slm) to one of three compute tiers: Tier A (OLMo
3 7B Q4 running locally), Tier B (OLMo 3.1 32B on cloud GPU burst), or Tier C (external API
endpoint). The Doorman selects the tier based on request shape, queue depth, and configured
budget cap. The Stage-3 prompt is constructed with the full input text and the serialised
Stage-2 finding set embedded as an annotation block — the model reads prior mechanical
findings as editorial context rather than starting from scratch. The output is a whole-text
rewrite. Per-span model suggestions are reserved for a future `Severity::Generative` variant.

## How Stage 2 findings flow into Stage 3 as inline JSON

The Stage-2 finding set is embedded directly in the Stage-3 Doorman prompt as a structured
JSON annotation block. Each entry in the block includes the matched span offsets, the
LanguageTool rule ID, the suggested replacement, and the `Severity::Mechanical` discriminant.
The model is instructed to address — or consciously disregard with a stated reason — each
flagged span in its rewrite. Inline embedding is preferred over a separate context-injection
endpoint because it keeps the Stage-3 input self-contained and auditable: the finding set is
part of the signed request record, not a side-channel dependency.

## Per-flag severity on the wire

The `/v1/proofread` response carries a `findings` array. Each entry has a `severity`
discriminant: `Banned` (Stage 1), `Mechanical` (Stage 2), or `Generative` (Stage 3,
reserved). Callers use severity to drive UI decisions: `Banned` findings auto-highlight and
block submission; `Mechanical` findings display inline but are collapsible; `Generative`
findings, when implemented, will appear as per-span alternatives in a review pane.

## Operator verdict closes the apprenticeship loop

After reviewing the Stage-3 rewrite, the operator records one of three dispositions via
`/v1/verdict`: `accepted` (the operator takes the rewrite as-is), `rejected` (the operator
discards the rewrite), or `edited` (the operator submits a hand-modified version as the final
text). The verdict and the associated texts form an event-pair tuple —
`draft-created` → `draft-refined` → `creative-edited` — that feeds the apprenticeship corpus
for continued model refinement. Stage-1 DPO pairs derive from the
`(input, chosen-rewrite, operator-disposition)` triple. Tenant separation is structural: each
tenant's verdict records are written to the path for that tenant's deployment instance and
cannot be co-mingled.

## When stages degrade gracefully

Each stage has a defined degradation path. If Stage 2's LanguageTool Docker companion is
unreachable, the pipeline continues to Stage 3 with an empty mechanical findings set; the
response metadata carries `mechanical_pass: false` so the caller can surface a warning to the
operator. If Stage 3's Doorman cannot reach any compute tier within the configured timeout,
the pipeline returns Stage-1 and Stage-2 findings only, with `generative_pass: false` in the
response. In both degraded cases, the response remains valid — findings from available stages
are returned — and the operator can act on what is present.

## See also

- [[language-protocol-substrate]] — the four genre families and vocabulary lists Stage 1
  draws from; companion article
- [[customer-tier-catalog-pattern]] — how the proofreader deployment instance is provisioned
  to run this pipeline; companion article
