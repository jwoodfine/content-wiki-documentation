---
schema: foundry-doc-v1
title: "Query the DataGraph"
slug: query-the-datagraph
short_description: "Queries the DataGraph for current entity state with the real query_datagraph and get_entity_context MCP tools, and handles DataGraph unavailability as its own signal, separate from Doorman's inference tiers."
category: how-to
index_group: records-storage
content_type: how-to
type: how-to
quality: complete
status: active
audience: "Engineers (hands on keyboard); customer operators"
last_edited: 2026-08-06
editor: pointsav-engineering
paired_with: query-the-datagraph.es.md
research_trail:
  sources: [live MCP tool schemas for query_datagraph and get_entity_context, confirmed 2026-08-06; app-console-slm F9 dashboard's DataGraph section (confirmed in a prior investigation this session — entity_count is its own field, not a Doorman tier)]
  verification_method: "the two tool signatures were read directly from the live, currently-registered MCP schema rather than inferred from documentation; corrected the guide's own prior Correction note's finding (DataGraph availability is not a Doorman tier) into plain prose"
---

## Prerequisites

- Access to the DataGraph MCP tools (`query_datagraph`, `get_entity_context`)
- DataGraph availability (check the F9 dashboard's DataGraph section — see [[use-f-key-model]])

## Purpose

Look up current, verified entity state instead of relying on session memory, which is a snapshot that drifts. A lookup takes seconds once you know which tool to reach for.

## Procedure

1. For a broad or exploratory lookup, call `query_datagraph` with a free-text or keyword query:

   ```
   query_datagraph(q: "project-editorial archive status")
   ```

   It accepts an optional `limit` (default 10 results) and an optional `format_for_prompt` flag that returns a pre-formatted block ready to paste into another prompt.

2. For a full profile of a specific, already-identified entity, call `get_entity_context` with its name or identifier:

   ```
   get_entity_context(entity: "service-content")
   ```

3. To follow a relationship from one entity to another, take the identifier of the entity you're interested in from your first result and call `get_entity_context` on it directly. Navigate from the entity you already know toward the one you're looking for.

4. Narrow a broad query by adding an entity-type keyword — person, organization, project, service, deployment — to the query text; the DataGraph's own taxonomy usually surfaces the right entity in the first result.

## Expected outcome

A ranked list of matching entities from `query_datagraph`, or a full entity profile from `get_entity_context` — current, verified state rather than a snapshot from whenever your own context was last updated.

## Verification

Compare the result's freshness against your own assumption — if you expected a fact that isn't in the returned profile, or the profile is older than you expected, treat the DataGraph's answer as authoritative and update your own understanding, not the reverse.

> **Note:** DataGraph availability is not one of Doorman's inference tiers. Tiers A/B/C govern where an inference request routes; DataGraph is a separate live entity store with its own status, shown in its own section of the F9 dashboard. The two can be up or down independently of each other.

## Rollback

Queries are read-only. Nothing to undo.

## Next steps

- [[export-structured-data]] — export entity records once you've found what you need
- [[use-f-key-model]] — where DataGraph's own status is actually shown

## See also

- [[service-content]] — the service that maintains the DataGraph
- [[service-extraction]] — how entities enter the graph from raw corpus documents
- [[doorman-protocol]] — the separate inference-routing gateway and its tier model
