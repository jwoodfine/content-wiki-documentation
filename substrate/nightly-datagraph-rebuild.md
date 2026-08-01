---
schema: foundry-doc-v1
title: "Nightly Datagraph rebuild"
slug: nightly-datagraph-rebuild
category: substrate
type: concept
content_type: topic
status: stub
short_description: "The scheduled process that reconstructs the platform's knowledge graph from canonical flat-file sources each night — AI-assisted entity extraction produces proposals only; every write to the graph passes through a Ring 2 write path with a human approval checkpoint."
bcsc_class: public-disclosure-safe
last_edited: 2026-08-01
editor: pointsav-engineering
paired_with: nightly-datagraph-rebuild.es.md
---

The nightly datagraph rebuild is the scheduled pipeline that reconstructs the platform's full knowledge graph from its canonical flat-file sources. Every graph-queryable relationship — entity links, [[service-extraction|extraction outputs]], [[worm-ledger-architecture|ledger entries]], and [[location-intelligence-substrate|location intelligence indexes]] — is derived from the same deterministic inputs each cycle. The result is a fresh, stable snapshot available to all query consumers at the start of each operating day.

## Key Takeaways

- The graph is rebuilt from flat-file sources nightly, not maintained by continuous mutation. Consumers read a stable snapshot, not a live partially-constructed graph.
- Every rebuild cycle can be replicated from archived flat files, since the WORM ledger snapshot each cycle reads from is itself immutable.
- Entity extraction uses grammar-constrained inference through the [[doorman-protocol|Doorman]] — this is Ring 2 calling Ring 3 for a proposal, not a Ring 2-internal deterministic step. The [SYS-ADR-07](governance/architecture-decisions) boundary is enforced downstream of extraction, not by excluding AI from the pipeline: extraction output is a proposal only, and every write to the graph passes through a Ring 2 write path with a human approval checkpoint before it lands. See [[architecture/three-ring-architecture|the Three-Ring Architecture]] for the general rule this pipeline follows.
- Each cycle compounds the prior cycle. Newly committed records extend the graph; no record is removed. The [[compounding-substrate]] mechanism means the graph grows monotonically accurate over time.

## Purpose

The rebuild pattern ensures that the queryable substrate reflects the committed state of the canonical record, not accumulated in-memory drift. Any single run can be replicated from the archived flat files.

Schema-driven joins against the canonical taxonomy and location intelligence indexes are deterministic — no fuzzy matching. Entity extraction itself is not: it is grammar-constrained inference through the Doorman, producing a structured proposal that a human reviews before it becomes a graph write. This matches the platform-wide SYS-ADR-07 boundary — AI never writes to a structured record store directly, regardless of which ring called it — rather than excluding AI from the extraction step entirely.

## Pipeline stages

The rebuild pipeline follows a fixed sequence:

1. **Ledger snapshot** — reads the current committed state of all [[worm-ledger-design|WORM ledger]] segments. The ledger is append-only; the snapshot is the complete history as of the scheduled start time.
2. **Extraction pass** — [[service-extraction|service-extraction]] hands corpus text to [[service-content|service-content]], which calls the Doorman for grammar-constrained entity extraction, producing proposed entity records for persons, organisations, assets, and events. This is a Ring 2 → Ring 3 call for a proposal, not a deterministic step — see the compliance note above.
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
