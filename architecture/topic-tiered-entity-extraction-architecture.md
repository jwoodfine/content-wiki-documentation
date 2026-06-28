---
schema: foundry-doc-v1
title: "Tiered Entity Extraction Architecture"
slug: topic-tiered-entity-extraction-architecture
category: architecture
type: concept
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: current-fact
language_protocol: PROSE-TOPIC
last_edited: 2026-06-28
editor: editorial
short_description: "The PointSav entity extraction pipeline runs three tiers in sequence on each document: Tier 0 provides fast extractive detection via GLiNER; Tier A provides a generative fallback via OLMo on CPU; Tier B provides GPU enrichment and records improvements as training signal."
paired_with: topic-tiered-entity-extraction-architecture.es.md
aliases:
  - topic-dual-tier-extraction-architecture
cites: []
---

The PointSav entity extraction pipeline runs three tiers in sequence on each document. Tier 0 provides fast extractive detection on CPU. Tier A provides a generative fallback when Tier 0 is unavailable. Tier B provides a higher-capacity GPU enrichment pass and records improvements as training signal.

## Tier 0 — Extractive Detection (GLiNER)

Tier 0 routes document payloads to `service-gliner`, a GLiNER named entity recognition microservice running locally on the workspace VM. GLiNER is a BERT-encoder model that reads a text span and returns entity spans with classifications. It is purely extractive: it can only return spans that appear verbatim in the input text and cannot generate or infer names that are not present.

Typical latency on CPU is 130–208 milliseconds per document. This is two to three orders of magnitude faster than generative inference.

Documents sent to Tier 0 are truncated at a sentence boundary near 2,000 characters before dispatch. The BERT encoder operates on a fixed context of 512 tokens; prose at the 2,000-character limit occupies approximately 480 tokens, leaving room for the label description strings without truncation. Content beyond the 2,000-character limit is not sent to Tier 0. Article chunking (planned) will address entity recall in the second half of long documents.

Labels are expressed as plain-English descriptions rather than bare category names. The domain identifier in the document payload selects a label set:

- `projects` — covers real estate investment and commercial property content. Recognises Person, Company, Project (named developments, buildings, funds), Location, and Account.
- `corporate` — covers general organisational content. Recognises Person, Company, Project, Location, and Account.
- `documentation` — covers engineering and technical content. Recognises Person, Company, Project (software projects), Location, and Account.

When Tier 0 returns an empty entity list for a document, the pipeline falls through to Tier A. An empty response from a well-functioning Tier 0 service is expected and normal for structured data files, source code, and other non-prose inputs.

## Tier A — Generative Fallback (OLMo)

Tier A routes document payloads to OLMo 7B running on the workspace VM's CPU via the Doorman's `/v1/chat/completions` endpoint. Tier A activates when Tier 0 is unreachable (network error, service down) or returns an empty entity list for a document that the pipeline determines should produce entities.

Extraction uses a structured prompt that constrains the model to the same five entity classifications used by Tier 0. When grammar constraints are enabled, the model is forced to emit valid JSON conforming to the extraction schema, eliminating schema-violation rejections. The inference call uses `temperature: 0.0` to produce deterministic output and `cache_prompt: true` to allow KV-cache reuse across consecutive extraction calls on the same system prompt.

Tier A latency on CPU ranges from 30 to 137 seconds per document depending on document length and concurrent load. When the Doorman's apprenticeship drain queue is active, Tier A slots may be occupied and interactive extraction calls will queue.

## Tier B — GPU Enrichment

Tier B routes through the Doorman's `/v1/extract` endpoint to a GPU inference node. When the Tier B circuit is closed and a node is reporting healthy, the Doorman forwards the document for a second, higher-capacity enrichment pass.

Tier B results pass through the same entity classification filter as Tier 0 and Tier A output. When Tier B succeeds structurally but all returned entities fail the filter — a condition that arises when grammar constraints are not enforced on the Tier B path — the pipeline applies a rescue behaviour: it uses the Tier 0 entity set at reduced confidence rather than writing zero entities to the graph store. The document is marked for Tier B retry so that a subsequent run can produce enriched output when grammar enforcement is available on the Tier B path.

Tier B results and their Tier A baseline are recorded as a DPO (Direct Preference Optimisation) feedback pair. This corpus accumulates across live extraction runs and is used for future model fine-tuning under the Yo-Yo training cycle.

## Graph Store Write Path

Entities from whichever tier produces the accepted result are written to LadybugDB. Entities are keyed by module identifier and entity name; within-module duplicates are upserted. A checkpoint is issued after each write batch to ensure that entities written by the drain worker thread are immediately visible to HTTP read queries, which execute on a separate runtime context.

The extraction service tracks processed documents in a JSONL processing ledger to prevent re-extraction on service restart.

## Backpressure

When the Doorman reports a queue depth exceeding the configured threshold and Tier 0 is unavailable, documents that would fall through to Tier A alone are deferred rather than processed. Deferral prevents the engineering document backlog from being permanently marked as processed at low quality during a Tier 0 outage.

Documents for which Tier 0 returns a non-empty entity list always proceed to Tier B enrichment regardless of queue depth.

## Tier Summary

| Tier | Service | Method | Typical latency | Activates when |
|---|---|---|---|---|
| 0 | service-gliner (GLiNER) | Extractive span detection | 130–208 ms | Default — first path |
| A | service-slm (OLMo 7B CPU) | Generative completion | 30–137 s | Tier 0 down or returns empty |
| B | service-slm (GPU node) | Generative enrichment | 10–30 s | Circuit closed + node healthy |
