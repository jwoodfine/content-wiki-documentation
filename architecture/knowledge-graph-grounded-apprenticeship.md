---
schema: foundry-doc-v1
title: "Knowledge-Graph-Grounded Apprenticeship"
slug: knowledge-graph-grounded-apprenticeship
category: architecture
type: topic
quality: published
short_description: "The Doorman consults the per-tenant knowledge graph before every inference request, producing training tuples where the graph and the model adapter co-evolve."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-01
editor: pointsav-engineering
cites: []
paired_with: knowledge-graph-grounded-apprenticeship.es.md
---

**Knowledge-Graph-Grounded Apprenticeship** is the pattern by which the Doorman (`service-slm`) consults the per-tenant knowledge graph in `service-content` before routing every substantive inference request. The grounding context — a subgraph of entities and relationships relevant to the query — is supplied to the model alongside the request. The resulting training tuple carries both the graph context and the model's response, which means the knowledge graph and the per-tenant adapter improve together over time.

This pattern encodes Doctrine claim #44 and extends the apprenticeship substrate with a graph-grounding layer.

## Pre-inference grounding

Before the Doorman dispatches a request to any compute tier, it calls `service-content`'s graph query tool to assemble a two-hop subgraph around the query terms. The subgraph is rendered as a structured prefix to the model's system prompt, presenting the relevant entities, their relationships, and their domain and theme classifications.

The model therefore receives not only the user's query but also the factual context that the knowledge graph already holds about the parties and topics involved. The grounded entity identifiers are recorded in the audit ledger for subsequent citation verification.

When a query has no relevant graph context — for example, a generic system administration question — the graph query returns an empty subgraph and the request proceeds without grounding. These ungrounded tuples are valid training data; the model learns that some questions do not require graph context.

## Post-inference graph mutation

When the model's response includes structured outputs and the senior verdict accepts the response, the Doorman may propose graph mutations derived from the response — new entities, new relationships, or updated properties. It calls `service-content`'s graph mutation tool; `service-content` applies the changes atomically, per tenant, and the audit ledger records the mutation event.

The loop closes: entities discovered during one inference interaction become grounding context for the next. The knowledge graph grows through use.

## Training tuple shape

The apprenticeship corpus tuple gains a graph context field alongside the brief, the model's attempt, and the verdict. Direct preference optimisation training treats verdict-signed tuples with populated graph context as higher-weight examples than ungrounded tuples. Supervised fine-tuning over unsigned tuples uses graph context as additional input signal.

Because graph context is per-tenant — isolated by module identifier — the Woodfine adapter trains on Woodfine graph context and the PointSav adapter trains on PointSav graph context. There is no cross-tenant leakage at training time.

## Graph-coherence quality metrics

A model response can be evaluated against the knowledge graph on three dimensions:

**Citation rate** — the fraction of named entities in the response that exist in the graph. A high citation rate indicates the model is staying within known facts.

**Relationship accuracy** — the fraction of stated relationships that match edges in the graph. Inaccurate relationships signal model drift from the grounded record.

**Hallucination rate** — the fraction of named entities in the response that are not present in the graph. Hallucination rate is the primary failure mode; responses above a threshold are candidates for refinement or rejection.

These metrics feed the verdict process. A response with high hallucination rate is rejected; one with low citation rate is a candidate for refinement before acceptance.

## Dependency on single-boundary discipline

Knowledge-graph-grounded apprenticeship depends on the [[single-boundary-compute-discipline]]. If inference can bypass the Doorman, it bypasses graph grounding. An ungrounded inference call produces no graph context field in the training tuple, no citation rate measurement, and no proposed graph mutation. The two claims compose as a structural dependency: without single-boundary enforcement, graph-grounded apprenticeship cannot be guaranteed.

## See Also

- [[single-boundary-compute-discipline]] — structural prerequisite; grounding happens at the Doorman boundary
- [[seed-taxonomy-as-smb-bootstrap]] — the per-tenant taxonomy that seeds the knowledge graph used for grounding
- [[mcp-substrate-protocol]] — the MCP tools (`graph_query`, `graph_mutate`) through which the Doorman interacts with `service-content`

## References

1. Doctrine claim #44 — Knowledge-Graph-Grounded Apprenticeship (ratified v0.1.0).
2. `conventions/apprenticeship-substrate.md` — upstream training tuple substrate.
3. Microsoft GraphRAG (2024) — published evidence for hallucination reduction via graph-grounded inference.

---

## Provenance

Source: `convention-knowledge-graph-grounded-apprenticeship.md` (refined 2026-04-30). Workspace-internal file paths and open questions removed. BCSC forward-looking framing applied to the co-evolution claim (graph and adapter improvement described as a structural pattern, not a guaranteed schedule).

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*

*Woodfine Capital Projects™, Woodfine Management Corp™, PointSav Digital Systems™, Totebox Orchestration™, and Totebox Archive™ are trademarks of Woodfine Capital Projects Inc., used in Canada, the United States, Latin America, and Europe. All other trademarks are the property of their respective owners.*
