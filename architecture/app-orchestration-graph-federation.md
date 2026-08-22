---
schema: foundry-doc-v1
type: topic
content_type: topic
slug: app-orchestration-graph-federation
title: "DataGraph Federation: From app-orchestration-slm to app-orchestration-graph"
short_description: "How PointSav federates sovereign per-archive DataGraphs through a single auditable gateway, and the conditions under which that gateway becomes a dedicated service."
audience: vendor-public
bcsc_class: current-fact
language: en
paired_with: app-orchestration-graph-federation.es.md
category: architecture
index_group: platform-structure
status: active
quality: complete
last_edited: 2026-06-23
---

Every [[totebox-archive|Totebox Archive]] in the PointSav platform maintains a sovereign DataGraph — a
graph of entities, relationships, and corpus metadata specific to its operational
domain. The GIS archive holds geographic entities and spatial relationships. The
editorial archive holds content entities and authorship graphs. These DataGraphs do
not merge. They do not replicate. Each is authoritative for its own domain and
inaccessible to any other archive by default.

This sovereignty is a design invariant, not a limitation. The [[capability-geometry|capability geometry]] of
the platform makes cross-archive DataGraph access impossible except through a single,
auditable path: the DataGraph federation gateway.

## How Federation Works Today

In the current platform (as of [[os-orchestration]] Phase 2), DataGraph federation is
handled by `app-orchestration-slm` via `POST /v1/graph/federated`. When a downstream
process requires a cross-archive entity query, the request arrives at the chassis. The
chassis calls `FleetRegistry.list_full()` — which returns all registered Totebox fleet
members with their full `doorman_endpoint` — and fans out the query to each member
concurrently. Each Totebox [[doorman-protocol|Doorman]] queries its own `service-content` DataGraph and
returns the result. The chassis aggregates the `FederatedGraphEntry` responses and
returns a `FederatedGraphResponse`.

This design has three properties:

**Pull-on-demand.** The chassis holds no DataGraph state. It queries Toteboxes when
asked, aggregates in memory, and discards. Nothing is cached between requests. This
preserves sovereignty: if an archive's DataGraph is updated, the next federated query
returns fresh data without any synchronisation step.

**Operator-invoked only.** The federation endpoint is not called automatically. It
requires an explicit POST from an authorised caller. No background process on
os-orchestration sweeps Totebox DataGraphs. This is intentional — unsolicited reads
from a sovereign archive would require a standing cross-archive capability grant,
which the architecture does not permit.

**Fire-and-forget fan-out.** The chassis's own outbound call to each Doorman carries
no signed capability header today — that's a property `app-orchestration-graph`
(below) adds when it activates, not something the current `app-orchestration-slm`
mechanism does yet. An unreachable archive is silently omitted from the response
rather than raising an error; the caller sees `archives_queried` against
`archives_reachable` and can tell the two numbers apart.

## Why app-orchestration-slm Holds Federation Now

`app-orchestration-slm` is the inference broker — its primary function is routing
inference requests from Tier 0 Doormen to the appropriate compute tier. Federation
is collocated with inference for a straightforward reason: in a small fleet, the
operator action that triggers a federated inference task (inject cross-archive context
into a prompt) also needs the federated DataGraph result to construct that context.
Keeping both in one process avoids an extra network hop.

This colocation is correct at fleet sizes of 2–10 Toteboxes. At this scale, DataGraph
fanout queries are infrequent relative to inference requests, the connection overhead
is trivial, and the aggregation logic is simple enough to maintain inline.

## When the Separation Becomes Necessary

Three conditions signal that DataGraph federation should be extracted into a dedicated
`app-orchestration-graph` service:

**Workload independence.** When DataGraph queries arrive at rates, volumes, or latency
budgets substantially different from inference requests, the two workloads compete for
resources inside the same process. A slow federation fanout (waiting on 15 Toteboxes)
stalls inference routing; a burst of inference requests queues behind federation
aggregation. Extraction eliminates this coupling.

**Multiple consumers.** As long as only the inference path needs cross-Totebox
DataGraph access, colocation is defensible. If a second consumer emerges — a reporting
pipeline, a cross-archive search surface, or a training schedule coordinator that needs
entity counts across all archives — the fanout logic should not be duplicated. A
dedicated service with a stable API serves all consumers.

**Connection pool requirements.** `app-orchestration-graph` would maintain persistent
HTTP connections to every registered Totebox's `service-content` endpoint. For a fleet
of 20 or more Toteboxes, this connection pool is a non-trivial resource. Managing it
inside `app-orchestration-slm` — which is designed to be a stateless routing process —
introduces operational complexity that a dedicated service handles naturally.

`app-orchestration-graph` activates when the fleet reaches two Totebox Archives with
DataGraph endpoints, or when a second consumer of federated queries emerges —
whichever comes first.

## What app-orchestration-graph owns

`app-orchestration-graph` already exists as a working scaffold, not yet activated in
production. It serves `GET /v1/graph/context?q=&module_id=`, fanning out to every
target listed in the `ORCHESTRATION_GRAPH_TARGETS` environment variable — a
comma-separated list of `archive_name|endpoint|module_id` triples, so each target
carries its own tenant scope explicitly rather than being inferred from a bare URL.
Each fan-out call carries a signed `X-Foundry-Capability` header, established at
startup via an Ed25519 pairing handshake with each target; a target's own
capability gate rejects a query whose signed scope doesn't match the `module_id` it
was queried under. Entities returned from different archives are deduplicated by
normalised name. The response reports `warnings`, `archives_queried`, and
`archives_responding` rather than a single `partial` flag — a caller can see exactly
which archives answered and which didn't, not just whether the query was complete.

Planned port: `:9181` (`:9180` is `app-orchestration-slm`).

## What app-orchestration-graph does not own

`app-orchestration-graph` holds no entity data, replicates no DataGraph, and pushes
nothing to Toteboxes. It is a read-only gateway. The source of truth for every entity
remains the `service-content` instance in the Totebox that generated it.

The name `app-orchestration-content` was considered and explicitly rejected. It would
introduce confusion with `service-content` — the per-Totebox DataGraph store. The
graph naming (`app-orchestration-graph`) signals the function (graph federation
gateway) without implying data ownership.

## Relationship to the Tier Split Architecture

`app-orchestration-graph` is a Phase 3+ consideration in the SLM tier split
architecture. The Phase 1 and Phase 2 deployments — using `app-orchestration-slm`'s
built-in `POST /v1/graph/federated` — remain in place throughout. The Reserved-folder
stub exists to capture the architectural intent and prevent the design from being lost
as the fleet grows incrementally.

When the extraction is eventually performed, the transition is intended to be additive:
stand up `app-orchestration-graph` alongside `app-orchestration-slm`, migrate the
federated graph endpoint, verify parity, then remove the endpoint from
`app-orchestration-slm`. No Totebox Archive changes are required — the fanout target
changes at the chassis layer, invisible to individual archives.
