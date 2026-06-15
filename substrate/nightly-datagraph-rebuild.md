---
schema: foundry-doc-v1
title: "Nightly Datagraph rebuild"
slug: nightly-datagraph-rebuild
category: substrate
type: concept
content_type: topic
status: stub
short_description: "The scheduled process that reconstructs the platform's knowledge graph from canonical flat-file sources each night, producing a fresh queryable substrate from deterministic inputs without AI involvement."
bcsc_class: public-disclosure-safe
last_edited: 2026-05-18
editor: pointsav-engineering
paired_with: nightly-datagraph-rebuild.es.md
---

The nightly datagraph rebuild is the scheduled pipeline that reconstructs the platform's full knowledge graph from its canonical flat-file sources. Every graph-queryable relationship — entity links, [[service-extraction|extraction outputs]], [[worm-ledger-architecture|ledger entries]], and [[location-intelligence-substrate|location intelligence indexes]] — is derived from the same deterministic inputs each cycle. The result is a fresh, stable snapshot available to all query consumers at the start of each operating day.

## Key Takeaways

- The graph is rebuilt from flat-file sources nightly, not maintained by continuous mutation. Consumers read a stable snapshot, not a live partially-constructed graph.
- Every rebuild cycle can be replicated from archived flat files. The same inputs produce the same graph — no AI inference, no probabilistic classification.
- The rebuild pattern enforces [SYS-ADR-07](governance/architecture-decisions) compliance: structured entity data is produced by deterministic rules, not AI model outputs.
- Each cycle compounds the prior cycle. Newly committed records extend the graph; no record is removed. The [[compounding-substrate]] mechanism means the graph grows monotonically accurate over time.

## Purpose

The rebuild pattern ensures that the queryable substrate reflects the committed state of the canonical record, not accumulated in-memory drift. Any single run can be replicated from the archived flat files.

The pipeline runs without AI inference. Relationships are computed by deterministic extraction rules and schema-driven joins, not by probabilistic classification. This is the SYS-ADR-07 enforcement boundary: structured graph data is a computed product of deterministic rules applied to verified records, not a model-generated artefact.

## Pipeline stages

The rebuild pipeline follows a fixed sequence:

1. **Ledger snapshot** — reads the current committed state of all [[worm-ledger-design|WORM ledger]] segments. The ledger is append-only; the snapshot is the complete history as of the scheduled start time.
2. **Extraction pass** — [[service-extraction|service-extraction]] runs its deterministic entity-recognition rules against the snapshot, producing entity records for persons, organisations, assets, and events.
3. **Schema-driven joins** — entity records are joined against the canonical taxonomy and location intelligence indexes using explicit foreign-key relationships. No fuzzy matching at this stage.
4. **Graph construction** — joined records are assembled into the queryable graph substrate consumed by [[service-content|service-content]] and the [[doorman-protocol|Doorman inference layer]].
5. **Swap** — the completed graph replaces the prior snapshot atomically. Query consumers switch to the new version at the next request after the swap.

## Position in the substrate stack

The nightly rebuild sits between the [[worm-ledger-design|WORM ledger]] (which accumulates append-only writes during the day) and the query-serving tier (which reads the most recently completed graph). Consumers of the [[knowledge-graph-grounded-apprenticeship|knowledge graph]] always read a stable snapshot, not a partially-constructed graph.

The [[compounding-substrate]] mechanism means each rebuild cycle inherits the full prior graph, then adds newly committed records on top. Accuracy compounds over time: an entity that appeared in three ledger records two years ago and twelve ledger records last month has a richer graph node than a newly registered entity — without any manual curation step.

## See also

- [[compounding-substrate]] — the mechanism by which each rebuild cycle compounds prior knowledge
- [[worm-ledger-design]] — the append-only ledger that feeds the rebuild pipeline
- [[service-extraction]] — the extraction service that produces entity records consumed by the rebuild
- [[service-content]] — the query-serving service that reads the completed graph
- [[doorman-protocol]] — the inference-layer client that queries the graph for entity context
