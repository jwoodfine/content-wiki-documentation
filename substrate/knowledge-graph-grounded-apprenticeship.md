---
schema: foundry-doc-v1
title: "Knowledge-graph-grounded apprenticeship"
slug: knowledge-graph-grounded-apprenticeship
category: substrate
type: topic
content_type: topic
quality: complete
index_group: the-compounding-doorman-and-ai-boundary
short_description: "The Doorman looks up matching entities in the per-tenant knowledge graph before dispatching a request, grounding the model's response in facts the graph already holds."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-08-22
editor: pointsav-engineering
cites: []
references:
  - id: 1
    text: "Edge, D. et al. 'From Local to Global: A Graph RAG Approach to Query-Focused Summarization.' arXiv:2404.16130, 2024."
    url: "https://arxiv.org/abs/2404.16130"
paired_with: knowledge-graph-grounded-apprenticeship.es.md
---

**Knowledge-graph grounding** is the pattern by which the [[compounding-doorman|Doorman]] ([[service-slm]]) consults the per-tenant knowledge graph in [[service-content]] before dispatching a request to a compute tier. Matching entities are prepended to the model's system prompt as factual context, isolated per tenant by module identifier — the Woodfine adapter never sees PointSav graph context or vice versa.

This pattern extends the [[apprenticeship-substrate]] with a graph-grounding layer.

## Pre-inference grounding

Before dispatching a request, the Doorman extracts words of four or more characters from the user's most recent message and queries [[service-content]] for entities whose names substring-match those words, preferring longer and more specific candidates first. A matching entity carries its classification (Person, Company, Project, Account, or Location) and, where known, role, location, and contact detail — the query defaults to one hop out from the matched entities, not a wider traversal. Results are prepended as a system message the model sees alongside the user's query.

The lookup is non-fatal: if `service-content` is unavailable or no entity matches, the request proceeds unmodified. A generic system-administration question with no relevant entities in its text simply gets no grounding — that is the expected, common case, not a failure.

## No automatic graph-writeback from inference

Nothing in the Doorman's routing or verdict-handling path writes back to the graph. The mutation endpoint [[service-content]] exposes (`POST /v1/graph/mutate`) exists, but its only real caller is a human-operated tool — project-editorial's `graph-committer.py`, which requires an operator to review a staged proposal and pass `--confirm` before anything is written. A separate, unrelated path writes graph entities without a per-item human review: a nightly extraction job that (when enabled) captures automatically-extracted entities for later batch approval rather than writing them immediately — see [[nightly-datagraph-rebuild]] for that mechanism's own real behavior and its currently-open governance gap. Neither path is triggered by an inference request's verdict.

## Graph-coherence quality metrics

A model response can still be evaluated against the knowledge graph on three dimensions, independent of whether the graph itself changes:

**Citation rate** — the fraction of named entities in the response that exist in the graph. A high citation rate indicates the model is staying within known facts.

**Relationship accuracy** — the fraction of stated relationships that match the graph's own recorded edges. Inaccurate relationships signal model drift from the grounded record.

**Hallucination rate** — the fraction of named entities in the response that are not present in the graph. Hallucination rate is the primary failure mode; responses above a threshold are candidates for refinement or rejection. [^1]

These metrics feed the verdict process. A response with high hallucination rate is rejected; one with low citation rate is a candidate for refinement before acceptance.

## Dependency on single-boundary discipline

Grounding depends on the [[single-boundary-compute-discipline]]. If inference can bypass the Doorman, it bypasses graph grounding entirely — a request routed around the Doorman gets no entity context and no citation-rate measurement. Without single-boundary enforcement, grounded apprenticeship cannot be guaranteed for every request.

## See also

- [[single-boundary-compute-discipline]] — structural prerequisite; grounding happens at the Doorman boundary
- [[seed-taxonomy-as-smb-bootstrap]] — the per-tenant taxonomy that seeds the knowledge graph used for grounding
- [[mcp-substrate-protocol]] — the MCP tools through which the Doorman interacts with `service-content`
- [[nightly-datagraph-rebuild]] — the separate, unrelated path that writes new entities into the graph

