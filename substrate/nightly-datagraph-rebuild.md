---
schema: foundry-doc-v1
title: "Nightly Datagraph rebuild"
slug: nightly-datagraph-rebuild
category: substrate
type: concept
status: stub
short_description: "The scheduled process that reconstructs the platform's knowledge graph from canonical flat-file sources each night, producing a fresh queryable substrate from deterministic inputs without AI involvement."
bcsc_class: public-disclosure-safe
last_edited: 2026-05-18
editor: pointsav-engineering
paired_with: nightly-datagraph-rebuild.es.md
---

The nightly datagraph rebuild is the scheduled pipeline that reconstructs the platform's full knowledge graph from its canonical flat-file sources. Every graph-queryable relationship — entity links, [[service-extraction|extraction outputs]], [[worm-ledger-architecture|ledger entries]], and [[location-intelligence-substrate|location intelligence indexes]] — is derived from the same deterministic inputs each cycle.

## Purpose

The rebuild pattern ensures that the queryable substrate reflects the committed state of the canonical record, not accumulated in-memory drift. Any single run can be replicated from the archived flat files.

The pipeline runs without AI inference. Relationships are computed by deterministic extraction rules and schema-driven joins, not by probabilistic classification.

## Position in the substrate stack

The nightly rebuild sits between the [[worm-ledger-design|WORM ledger]] (which accumulates append-only writes during the day) and the query-serving tier (which reads the most recently completed graph). Consumers of the [[knowledge-graph-grounded-apprenticeship|knowledge graph]] always read a stable snapshot, not a partially-constructed graph.

## See also

- [[compounding-substrate]] — the mechanism by which each rebuild cycle compounds prior knowledge
- [[worm-ledger-design]] — the append-only ledger that feeds the rebuild pipeline
- [[service-extraction]] — the extraction service that produces entity records consumed by the rebuild
