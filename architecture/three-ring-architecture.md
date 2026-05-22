---
schema: foundry-doc-v1
title: "Three-ring architecture"
slug: three-ring-architecture
category: architecture
type: topic
quality: complete
short_description: "The durable composition pattern for the PointSav platform: three concentric rings with strict one-way dependencies, where the AI ring is structurally optional and the deterministic data pipeline operates fully without it."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-22
editor: pointsav-engineering
cites: []
paired_with: three-ring-architecture.es.md
---

Before a regulated organization buys an AI platform, it has to answer one question: can AI silently touch the authoritative record? On most platforms the answer is procedural — a policy, a configuration flag. A flag can be flipped, and a policy is only as strong as its enforcement.

PointSav answers the question architecturally. <!--claim id=three-rings confidence=structural cites=[]-->The Three-Ring Architecture organises every service into one of three concentric rings with strict one-way dependencies; the two inner rings — boundary ingest and deterministic processing — function fully without the outer AI ring.<!--/claim-->

<!--claim id=ai-optional-by-construction confidence=structural cites=[]-->Rings 1 and 2 contain no import, no dependency, and no runtime call that reaches Ring 3. A deployment can exclude Ring 3 entirely; where Ring 3 is included, it is a read-only consumer that produces proposals, never record writes.<!--/claim-->

For a regulated buyer the verification is structural rather than procedural. A deployment without Ring 3 has no AI to audit; a deployment with it keeps the deterministic core as the sole authoritative record. This article covers the ring layout, the service taxonomy, the multi-tenant isolation model, and why AI is optional by construction.

## Ring layout

```
 Ring 3 — Optional Intelligence
 service-slm + GPU burst orchestrator
 + Tier C external API integration
 ↓ queries (read-only)
 Ring 2 — Knowledge and Processing
 service-content + service-extraction
 + service-search + service-egress
 ↑ feeds ↓ writes
 Ring 1 — Boundary Ingest (per-tenant)
 service-fs + service-people
 + service-email + service-input
 (data flows in; per-tenant; MCP servers)
```

<!--claim id=directional-invariants confidence=structural cites=[]-->Ring 1 produces raw data and depends on nothing else. Ring 2 reads from Ring 1, writes structured records, and depends only on Ring 1. Ring 3 reads from Ring 2 and never writes to it.<!--/claim-->

## Service taxonomy

| Ring | Service | Purpose | Required at all tiers? |
|---|---|---|---|
| 1 | service-fs | Immutable Ledger (WORM append-only) | Required |
| 1 | [[service-people]] | Identity Ledger | Optional |
| 1 | [[service-email]] | Communications Ledger | Optional |
| 1 | service-input | Generic document ingestion | Optional |
| 2 | [[service-extraction]] | Deterministic parser; structured data never routes through Ring 3 | Required |
| 2 | [[service-content]] | Taxonomy Ledger and knowledge graph | Required |
| 2 | [[service-search]] | Search index | Required |
| 2 | [[service-egress]] | Physical release valve | Required for output |
| 3 | [[service-slm]] | AI Gateway — the Doorman | Optional |
| 3 | GPU burst orchestrator | Ephemeral multi-cloud burst | Optional |

## Ring 1 — Boundary Ingest

Ring 1 is the per-tenant data boundary. Each service accepts raw data from one external source — the filesystem, an email inbox, a document upload, an identity provider — and writes it to a durable ledger. No Ring 1 data is transformed or classified; it is only stored.

<!--claim id=ring1-mcp confidence=structural cites=[]-->Every Ring 1 service implements a Model Context Protocol server interface, and Ring 2 talks to Ring 1 as an MCP client. A customer who needs a new data source adds another MCP server without modifying any existing service.<!--/claim-->

Because Ring 1 is per-tenant, each tenant's data lives in a separate service instance with its own storage root. There is no shared state between tenants at this ring.

## Ring 2 — Knowledge and Processing

Ring 2 reads from Ring 1 and produces structured knowledge: parsed records, knowledge graphs, classified entities, search indexes. <!--claim id=ring2-deterministic confidence=structural cites=[]-->All Ring 2 processing is deterministic, and a binding architecture decision prohibits AI from writing to the knowledge graph or the structured record stores. Ring 2 output is reproducible: the same Ring 1 input replays to the same result.<!--/claim-->

An audit that questions a classification can replay the deterministic parse against the unchanged Ring 1 ledger and get the same answer. No AI variance enters the authoritative record. Ring 2 services are multi-tenant by `moduleId`: one process serves all tenants, and each tenant's knowledge graph and search index are isolated behind a `moduleId` namespace.

## Ring 3 — Optional Intelligence

<!--claim id=ring3-read-only confidence=structural cites=[]-->Ring 3 is a single read-only consumer of Ring 2. It never writes to the knowledge graph, the ledger, or the structured record stores; its only outputs are proposals — text the operator reviews, drafts the operator approves. Every accepted output enters the record through a Ring 2 write path with a human at the checkpoint.<!--/claim-->

`service-slm` is the single Ring 3 service. It implements the Doorman pattern: every request enters through one boundary, which sanitises outbound data, routes among the three compute tiers, and logs every call to the per-tenant audit ledger. No API key lives outside the Doorman boundary.

The three compute tiers available to Ring 3:

- **Tier A — local.** A 7B-class model on the customer's own hardware. Zero marginal cost, full data locality. The default for most requests.
- **Tier B — GPU burst.** A larger model on a short-lived GPU instance, used when Tier A cannot handle the request shape efficiently. The customer controls when it starts and stops.
- **Tier C — external API.** External vendor APIs, used only with an explicit per-request allowlist. Every call is logged at the customer's audit ledger.

## Multi-tenant isolation model

Tenant isolation varies by ring, by deliberate design.

- **Ring 1** — hard isolation by service instance. Each tenant's boundary ingest runs as a separate process with separate storage. No code path reaches from one tenant's Ring 1 data to another's.
- **Ring 2** — logical isolation by `moduleId`. One process, one set of indexes, strict namespace separation at every read and write. A query for tenant A cannot return tenant B's records.
- **Ring 3** — a single `service-slm` instance with per-`moduleId` adapter loading. The Doorman writes the `moduleId` into every audit-ledger entry.

## Why AI is structurally optional

The three-ring pattern makes AI optional by construction, not by configuration. A deployment that excludes Ring 3 ships fewer processes, exposes less attack surface, and satisfies network-isolation requirements that prohibit external API calls.

For a deployment that includes Ring 3, the read-only constraint keeps the deterministic core as the authoritative record. An operator auditing AI involvement in any output inspects the audit-ledger entry for the Doorman call, compares the proposal against the Ring 2 record it drew from, and confirms that no AI path modified the underlying structured data.

## See also

- [[compounding-substrate]] — the five structural properties the Three-Ring Architecture implements
- [[service-slm]] — the Ring 3 Doorman service that routes among compute tiers and logs every call
- [[compounding-doorman]] — the operational pattern the Doorman implements and why it compounds over time
- [[worm-ledger-architecture]] — the Ring 1 append-only ledger that underpins the audit guarantee
- [[apprenticeship-substrate]] — how Ring 3 interactions generate training signal that improves the local model over time
- [[architecture-decisions]] — the binding decisions that govern how rings interact and where AI is permitted
