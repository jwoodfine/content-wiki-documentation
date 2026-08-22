---
schema: foundry-doc-v1
title: "service-content"
slug: service-content
category: services
type: concept
content_type: topic
quality: complete
index_group: ring-2-knowledge-and-processing
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-08-22
editor: pointsav-engineering
paired_with: service-content.es.md
short_description: "service-content extracts named entities from raw payloads through a tiered model pipeline, writes them into the knowledge graph under a human-review checkpoint, and hosts the platform's reference taxonomies."
cites: []
references:
  - id: 1
    text: "ILO. 'ISCO-08: International Standard Classification of Occupations.' International Labour Organization, 2012."
    url: "https://www.ilo.org/public/english/bureau/stat/isco/isco08/"
---

An organization's files hold its knowledge but do not surface it. An email archive, a folder of contracts, a store of PDFs — each is searchable, and none of it knows who relates to whom or what the organization's own terms mean. `service-content` is the platform's entity-extraction and knowledge-graph write service: it turns raw document payloads into named entities and relationships, and it owns the reference taxonomies those entities are classified against.

## Extraction runs through three tiers, cheapest first

When a payload arrives, `service-content` tries the fastest extraction method first and only escalates when it has to:

1. **Tier 0 — GLiNER.** A direct HTTP call to a local GLiNER model (port 9085), with no call to the AI request router (the Doorman) involved. Most documents are handled here.
2. **Tier A fallback — OLMo, via the Doorman.** Runs when GLiNER is unreachable, when GLiNER finds nothing (to catch its blind spots), or when the payload is structured CSV data GLiNER's natural-language model can't parse. Every Tier 0 pass also queues an asynchronous Tier A run in the background. The two results become a training pair — GLiNER's extractive output as the preferred answer, OLMo's as the comparison — used to keep improving Tier A's own extraction quality over time. This is the platform's real self-improvement loop for this pipeline: a concrete training-data mechanism, not an organically growing glossary.
3. **Tier B — OLMo 32B, via the Doorman's `/v1/extract` endpoint.** The heaviest tier, used when the faster tiers are unavailable or insufficient.

A backpressure check against the Doorman's queue depth can defer a document rather than pile onto an already-loaded pipeline.

## Every automated graph write is held for a human verdict

`service-content` never writes extracted entities straight into the knowledge graph. Every write — from either tier — passes through the same checkpoint. It captures the write first, then promotes it only after a human signs off:

1. **Capture.** The write is recorded to a durable, on-disk JSONL file instead of touching the graph. It survives a process restart, and a human can review the full pending queue at any time.
2. **Verify.** A reviewer submits an SSH-signed verdict. The signature is checked against the workspace's `allowed_signers` file under a dedicated namespace, so a verdict signature from this system can never be replayed against an unrelated one.
3. **Promote on accept.** Only after a verdict is signed does the write actually reach the graph.
4. **Discard on reject.** The pending record is kept — never deleted — with the rejection verdict attached, for audit.

This satisfies the platform's SYS-ADR-07 (no structured data through AI) and SYS-ADR-19 (no automated AI publishing to verified ledgers) commitments directly: the extraction pipeline can run unattended, but nothing it produces becomes part of the graph of record without an explicit, signed human decision.

## The reference taxonomies it hosts

Separately from extraction, `service-content` owns a set of CSV taxonomy files — the [[archetypes-and-chart-of-accounts|Chart of Accounts and eleven archetypes]] among them, plus domain vocabularies, glossaries, and topic/guide indexes for each wiki. These load into the graph as static reference entities through a small admin API, distinct from the entities the extraction pipeline produces from real documents.

## See also

- [[archetypes-and-chart-of-accounts]] — the two reference taxonomies `service-content` loads into the knowledge graph
- [[verification-surveyor]] — where a human applies the archetype label that `service-content`'s taxonomy makes available
- [[service-extraction]] — the deterministic identity layer entities receive once extracted
- [[app-console-input]] — the F12 gate where an operator reviews a pending automated write
- [[query-the-datagraph]] — step-by-step guide: search named entities, navigate relationships, and handle Tier A outages
- [[export-structured-data]] — step-by-step guide: four export paths including DataGraph queries and wiki Markdown
