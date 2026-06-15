---
schema: foundry-doc-v1
title: "How to query the DataGraph"
slug: query-the-datagraph
category: how-to
content_type: how-to
type: how-to
status: active
last_edited: 2026-06-14
editor: pointsav-engineering
paired_with: query-the-datagraph.es.md
---

The DataGraph is the live entity store at the centre of `service-content`. It holds every person, organisation, project, and service that the Gravity Engine has identified and verified from the corpus — the ground truth for entity state at any point in time. Querying the DataGraph lets you look up current entity state, navigate relationships between entities, and verify facts before committing content.

For the DataGraph's place in the Gravity Engine, see [[service-content]]. For how entities are extracted into the graph, see [[service-extraction]].

## Prerequisites

- Access to the Doorman gateway (see [[doorman-protocol]])
- Doorman Tier A circuit in a live state (check the SLM Cartridge status bar)
- A `query_datagraph` call routed through the MCP interface

## Make a basic entity lookup

Call `query_datagraph` with a plain-text question about the entity you are looking for:

```
query_datagraph("project-editorial archive status")
```

The DataGraph performs a semantic search over the entity store and returns a ranked list of matching entities. Each result includes the entity's identifier, type, and the most recent verified fields.

For a full entity profile with all recorded fields, use `get_entity_context`:

```
get_entity_context("service-content")
```

## Navigate related entities

Entity results include a `related_to` field listing linked entities by type. To follow a relationship:

1. Read the entity result and note the identifier of the related entity.
2. Call `get_entity_context("<identifier>")` to retrieve the related entity's profile.

Relationships are directional — a project entity links to the services it depends on, but a service entity does not automatically list all projects that use it. Navigate from the entity you know toward the entity you are looking for.

## Filter results by type

Add an entity type keyword to the query to narrow results:

```
query_datagraph("service extraction pipeline")
query_datagraph("project editorial status")
```

The DataGraph understands the platform's entity taxonomy: persons, organisations, projects, services, deployments. Qualifying the query with the type usually surfaces the right entity in the first result.

## Handle a closed Tier A circuit

If Doorman's Tier A circuit is `OPEN`, the DataGraph is unavailable. The inference stack falls back to Tier B (SLM only) or Tier C (local fallback), but `query_datagraph` calls will fail.

Proceed with the following caveat in any content you are drafting: *"DataGraph unavailable — verified from session memory; check current state before committing."* Do not commit entity-dependent content during a Tier A outage without the caveat.

## Key takeaways

- The DataGraph is the live authority for entity state; session memory is a snapshot and drifts
- Use `get_entity_context` when you need the full profile, `query_datagraph` for search
- A Tier A circuit OPEN means the DataGraph is unreachable — note the caveat and check before committing
- Related entities are traversed by calling `get_entity_context` on the identifier from the first result

## See also

- [[service-content]] — the Gravity Engine that maintains the DataGraph
- [[service-extraction]] — how entities enter the graph from raw corpus documents
- [[doorman-protocol]] — the gateway routing DataGraph calls and its circuit-breaker model
- [[app-console-slm]] — the Doorman health dashboard showing Tier A/B/C states
- [[run-first-slm-query]] — submitting inference queries once Tier A/B is live
