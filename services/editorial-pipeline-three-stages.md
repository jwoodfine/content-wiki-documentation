---
schema: foundry-doc-v1
title: "The Three-Stage Editorial Pipeline"
slug: editorial-pipeline-three-stages
category: services
type: topic
content_type: topic
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-06-10
editor: pointsav-engineering
paired_with: editorial-pipeline-three-stages.es.md
---

Every document processed by `service-proofreader` passes through three discrete stages executed in sequence. Each stage is independently verifiable. Each has a defined degradation path when its dependency is unavailable. The stages are ordered from cheapest to most expensive, so that inexpensive deterministic checks prevent costlier downstream operations from handling input that a rule-pass could resolve.

## Why Three Stages, in This Order

Three principles drive the ordering.

*Cost discipline.* Stage 1 is deterministic and completes in sub-millisecond time for any input length. Stage 2 calls a locally-hosted language service. Stage 3 routes through the inference layer to a compute tier that may involve GPU capacity or an external API. Processing stops and returns early if Stage 1 flags a banned-vocabulary violation severe enough to require human intervention before any language pass is appropriate. Expensive inference never receives input that the upstream stages have already handled.

*Correctness.* Stage 2 applies hundreds of grammar and style rules with consistent output. When Stage 3 receives the document, the Stage-2 finding set is embedded in the prompt as editorial context. The inference model therefore encounters the document with known mechanical errors already annotated rather than discovering them inconsistently on each pass.

*Auditability.* Each stage emits a structured finding set that is independently verifiable. The full pipeline response includes findings from all three stages, each attributed to its source. An operator can inspect what each stage flagged and verify that the final rewrite addressed or consciously disregarded each item.

## Stage 1 — Banned-Vocabulary Scan

Stage 1 scans the input text against the workspace vocabulary lists compiled per language protocol family: PROSE, COMMS, LEGAL, and TRANSLATE families each carry different term sets appropriate to their registered genres.

A match produces a finding with severity `Banned`, a character span identifying the flagged term, and a replacement hint drawn from the vocabulary list entry. Stage 1 flags findings only — it does not silently rewrite the document. The principle is that a banned-vocabulary match requires a human to understand and apply the correct substitution; automated rewriting would bypass that understanding.

Stage 1 has no external dependency. It runs against an in-memory term set and completes regardless of the availability of the Stage-2 or Stage-3 services.

## Stage 2 — LanguageTool Mechanical Pass

Stage 2 calls LanguageTool 6.6, running as a companion HTTP service co-located with the pipeline. LanguageTool applies spelling, grammar, and style rules — categories too numerous to enumerate as a static vocabulary list.

The pipeline normalises the LanguageTool response into the internal `Finding` type used across all three stages. Each LanguageTool rule match is mapped to a finding with severity `Mechanical` and a character span. The normalisation step isolates the pipeline from changes in the LanguageTool response schema.

Stage-2 findings are serialised as a structured JSON annotation block embedded in the prompt for Stage 3. Each entry in the block carries the span, the rule category, and the LanguageTool rule identifier. The annotation block is part of the signed request record — the findings that Stage 3 was given are recoverable after the fact.

## Stage 3 — Generative Pass

Stage 3 routes the document and the embedded Stage-2 finding set to the inference layer. The routing service selects a compute tier based on the request shape and applicable budget constraints: Tier A is a locally-hosted 7B quantised model, Tier B is a 32B model available via multi-cloud GPU capacity, and Tier C routes to an external inference API. The system prompt includes the Stage-2 annotation block so the model reads the mechanical findings as editorial context rather than discovering the same issues independently.

The Stage-3 output is a whole-text rewrite of the input. The rewrite is expected to address or consciously disregard each item in the Stage-2 finding set. The operator review step that follows can compare the annotation block against the rewrite to verify which findings were acted on.

Stage-3 findings carry severity `Generative` and represent per-span editorial suggestions arising from the inference pass, beyond the scope of the Stage-2 mechanical rules.

## Severity Levels on the Wire

The `/v1/proofread` response carries a `findings` array where each entry has a `severity` field:

| Severity | Source | Meaning |
|---|---|---|
| `Banned` | Stage 1 | Term appears in the applicable vocabulary list; requires human substitution |
| `Mechanical` | Stage 2 | Grammar, spelling, or style rule match from the mechanical pass |
| `Generative` | Stage 3 | Per-span suggestion from the editorial inference pass |

Callers use severity to drive interface decisions. `Banned` findings may warrant prominent display before any editorial work proceeds; `Mechanical` findings may be collapsed by default in a review pane; `Generative` findings are advisory.

## Operator Verdict and the Learning Loop

After reviewing the Stage-3 rewrite, the operator records a verdict via `/v1/verdict`: `accepted` (the rewrite is adopted as-is), `rejected` (the operator reverts to the original), or `edited` (the operator has made further changes and submits the final text).

The verdict closes the loop by contributing to the corpus that informs future model behaviour. The tuple of original input, pipeline rewrite, and operator disposition forms a training-quality pair. When the operator edits rather than accepting or rejecting outright, the edited text is the positive example and the unedited rewrite is the negative. The corpus accumulates across verdicts, building an editorial preference record grounded in actual operator decisions rather than external datasets.

## Graceful Degradation

Each stage has a defined behaviour when its dependency is unavailable.

If the Stage-2 LanguageTool service is unreachable, the pipeline continues to Stage 3 with an empty mechanical findings set. The Stage-3 prompt includes a metadata flag indicating that the mechanical pass did not run. The response includes this flag so the caller can surface a partial-results notice.

If Stage 3 cannot reach any compute tier within its configured timeout, the pipeline returns the Stage-1 and Stage-2 findings only, with `generative_pass: false` in the response. The caller receives a complete mechanical-pass result rather than an error.

Neither degradation path silently omits findings available from the stages that did run. The response accurately represents the scope of what was evaluated.

## See Also

- [[language-protocol-substrate]] — the genre family definitions and per-family vocabulary lists that Stage 1 draws from
- [[customer-tier-catalog-pattern]] — the deployment model for the proofreader service instance
- [[soft-slm-tiered-gateway]] — the inference routing layer that Stage 3 dispatches through
