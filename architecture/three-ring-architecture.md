---
schema: foundry-doc-v1
title: "Three-Ring Architecture"
slug: three-ring-architecture
category: architecture
type: topic
quality: complete
short_description: "The durable composition pattern for the PointSav platform: three concentric rings with strict one-way dependencies, where the AI ring is structurally optional and the deterministic data pipeline operates fully without it."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-04-30
editor: pointsav-engineering
cites: []
paired_with: three-ring-architecture.es.md
---

The **Three-Ring Architecture** is the platform's core composition pattern. It organises every service into one of three rings, each with a clean one-way dependency on the rings below it. The outermost ring adds AI inference. The inner two rings — boundary ingest and deterministic knowledge — function fully without it.

This separation is a structural choice, not a design preference. A regulated buyer who requires an air-gapped deployment with no AI can run the full data pipeline at Ring 1 and Ring 2. A deployment that adds Ring 3 gains intelligence without any change to the data model, the audit surface, or the identity boundaries that the inner rings maintain.

## Ring layout

```
                 Ring 3 — Optional Intelligence
                 service-slm + Yo-Yo (multi-cloud burst)
                 + Tier C external API integration
                          ↓ queries (read-only)
                 Ring 2 — Knowledge and Processing
                 service-content + service-extraction
                 + service-search + service-egress
                          ↑ feeds              ↓ writes
                 Ring 1 — Boundary Ingest (per-tenant)
                 service-fs + service-people
                 + service-email + service-input
                 (data flows in; per-tenant; MCP servers)
```

**Directional invariants:**
- Ring 1 produces raw data and depends on nothing else.
- Ring 2 reads from Ring 1 and writes structured records; it depends only on Ring 1.
- Ring 3 reads from Ring 2 and never writes to it. Ring 1 and Ring 2 function without Ring 3.

## Service taxonomy

| Ring | Service | Purpose | Required at all tiers? |
|---|---|---|---|
| 1 | service-fs | Immutable Ledger (WORM append-only) | Required |
| 1 | service-people | Identity Ledger | Optional |
| 1 | service-email | Communications Ledger | Optional |
| 1 | service-input | Generic document ingestion | Optional |
| 2 | service-extraction | Deterministic parser (no AI, per SYS-ADR-07) | Required |
| 2 | service-content | Taxonomy Ledger and knowledge graph | Required |
| 2 | service-search | Search index (Tantivy, DARP-compliant) | Required |
| 2 | service-egress | Physical release valve | Required for output |
| 3 | service-slm | AI Gateway — the Doorman | Optional |
| 3 | (slm-yoyo) | Multi-cloud GPU burst orchestrator | Optional |

## Ring 1 — Boundary Ingest

Ring 1 is the per-tenant data boundary. Each service in this ring accepts raw data from one external source — the filesystem, an email inbox, a document upload, an identity provider — and writes it to a durable ledger. No data in Ring 1 is transformed or classified; it is only stored.

Every Ring 1 service implements a Model Context Protocol (MCP) server interface. Ring 2 talks to Ring 1 services as MCP clients. A customer who needs a new data source adds an additional MCP server without modifying any existing service. The MCP boundary is what makes Ring 1 extensible without coupling.

Because Ring 1 is per-tenant, each tenant's data lives in a separate service instance with its own storage root. There is no shared state between tenants at this ring.

## Ring 2 — Knowledge and Processing

Ring 2 reads from Ring 1 and produces structured knowledge: parsed records, knowledge graphs, classified entities, search indexes. All Ring 2 processing is deterministic. SYS-ADR-07 prohibits AI from writing to the knowledge graph or the structured record stores; those paths are exclusively Ring 2's.

The practical effect: Ring 2 output is reproducible given the same Ring 1 input. An audit that questions a classification can replay the deterministic parse against the unchanged Ring 1 ledger and get the same result. No AI variance enters the authoritative record.

Ring 2 services are multi-tenant via `moduleId`. One process handles requests for all tenants, but the knowledge graph and search index for each tenant are logically isolated behind their `moduleId` namespace.

## Ring 3 — Optional Intelligence

Ring 3 is a single read-only consumer of Ring 2. It never writes to the knowledge graph, the ledger, or the structured record stores. The only outputs Ring 3 produces are proposals: text the operator reviews, drafts the operator approves, suggestions the operator accepts or discards. Every accepted output that enters the authoritative record passes through a Ring 2 write path with a human at the checkpoint.

`service-slm` is the single Ring 3 service. It implements the Doorman pattern: every request enters through one boundary, which sanitises outbound data, routes among the three compute tiers (local, GPU burst, external API), and logs every call to the per-tenant audit ledger. No API key lives outside the Doorman boundary.

The three compute tiers available to Ring 3 are:

- **Tier A — local**: OLMo 3 7B running on the customer's own hardware. Zero marginal cost, full data locality. Default for most requests.
- **Tier B — GPU burst**: OLMo 3.1 32B Think on a short-lived GPU instance. Used when Tier A cannot handle the request shape efficiently. The customer controls when it starts and stops.
- **Tier C — external API**: external vendor APIs used only with an explicit per-request allowlist. Every call is logged at the customer's audit ledger.

## Multi-tenant isolation model

Tenant isolation varies by ring in a deliberate pattern:

- **Ring 1**: hard isolation by service instance. Each tenant's boundary ingest runs as a separate process with separate storage. There is no code path from one tenant's Ring 1 data to another's.
- **Ring 2**: logical isolation by `moduleId`. One process, one set of indexes, with strict namespace separation at every read and write path. Queries for tenant A cannot return records for tenant B.
- **Ring 3**: single `service-slm` instance with per-`moduleId` LoRA loading. The Doorman enforces audit-ledger writes that include the `moduleId` on every call.

## Why AI is structurally optional

The three-ring pattern makes AI optional by construction rather than by configuration. Rings 1 and 2 have no import, no dependency, no runtime call that reaches Ring 3. A deployment that excludes Ring 3 entirely ships fewer processes, exposes less attack surface, and satisfies network-isolation requirements that prohibit external API calls.

For deployments that include Ring 3, the read-only constraint means the deterministic core remains the authoritative record. Operators who want to audit AI involvement in any output can inspect the audit ledger entry for the relevant Doorman call, compare the proposal against the Ring 2 record it was drawn from, and confirm that no AI path modified the underlying structured data.

## See Also

- [[compounding-substrate]] — the five structural properties that the Three-Ring Architecture implements
- [[service-slm]] — the Ring 3 Doorman service that routes among compute tiers and logs every call
- [[compounding-doorman]] — the operational pattern the Doorman implements and why it compounds over time
- [[worm-ledger-architecture]] — the Ring 1 append-only ledger that underpins the audit guarantee
- [[apprenticeship-substrate]] — how Ring 3 interactions generate training signal that improves the local model over time

## References

1. PointSav Doctrine §XIV, The Compounding Substrate — claims #14–#18; Three-Ring composition as the structural basis for Optional Intelligence Layer (claim #16).
2. `conventions/three-ring-architecture.md` — workspace canonical specification.
3. `conventions/compounding-substrate.md` — meta-pattern the rings implement.
4. SYS-ADR-07 — structured data never routes through AI; enforces the Ring 2 / Ring 3 boundary.

---

## Provenance

Source material: workspace-root draft `topic-three-ring-architecture.md`, workspace conventions `three-ring-architecture.md` and `compounding-substrate.md`, service catalog in MEMO §6.3. Refinement disciplines applied: no body H1 (renderer supplies from frontmatter title); structural-positioning discipline (no competitive-by-name framing); BCSC posture applied (no forward-looking claims requiring labelling in this article — the ring structure is an operational present-state description); banned-vocabulary pass (no substitutions required).

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*

*Woodfine Capital Projects™, Woodfine Management Corp™, PointSav Digital Systems™, Totebox Orchestration™, and Totebox Archive™ are trademarks of Woodfine Capital Projects Inc., used in Canada, the United States, Latin America, and Europe. All other trademarks are the property of their respective owners.*
