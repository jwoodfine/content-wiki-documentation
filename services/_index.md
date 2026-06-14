---
schema: foundry-doc-v1
title: "Services"
slug: _index
category: services
type: topic
content_type: topic
quality: complete
short_description: "The autonomous services that implement Ring 1 boundary ingest and Ring 2 deterministic knowledge processing in the PointSav three-ring architecture — grouped by ring layer and function."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-15
editor: pointsav-engineering
paired_with: _index.es.md
---

PointSav's three-ring architecture assigns every service to a layer with defined authority and dependencies. Ring 1 services handle per-tenant boundary ingest — each accepts raw data from one external source and writes it to a durable ledger. Ring 2 services provide deterministic knowledge and processing: they read from Ring 1 and produce structured records, knowledge graphs, and search indexes. Ring 3 is a single service, service-slm, which reads from Ring 2 and never writes to it.

The platform functions fully across Rings 1 and 2 without AI compute. Removing Ring 3 shrinks the attack surface, satisfies network-isolation requirements, and answers the compliance question of whether AI has touched the authoritative record. The answer is architectural: Rings 1 and 2 have no import, no dependency, and no runtime call that reaches Ring 3.

## Ring 1 — Boundary ingest

Per-tenant boundary services. Each runs as a separate process per tenant and exposes a Model Context Protocol server interface.

- [[service-fs-architecture]] — The filesystem service: append-only WORM ledger, per-tenant storage root, the foundation every other Ring 1 service writes to.
- [[service-email]] — Email ingest: SMTP and IMAP, sanitised payloads, append-only Maildir on local block storage.
- [[service-people]] — Identity ledger: person records, role assignments, and the Anchor-Claim-Socket data model that never overwrites state.

## Ring 2 — Knowledge and processing

Deterministic processing services. Each reads from Ring 1 and produces structured records — no AI variance enters the authoritative record.

- [[service-extraction]] — The central Ring 2 traffic controller: strips proprietary formatting, constructs Entity Bundles, assigns transaction IDs, routes to deterministic services or to service-slm.
- [[service-content]] — The Gravity Engine: reads raw payloads from a Totebox, runs them against an institutional taxonomy, generates the structured documents an organisation publishes.
- [[service-search]] — Full-text search on Tantivy: per-tenant sharding, microsecond retrieval, no active database process required.
- [[service-egress]] — Physical release valve: structured records leave the platform only through this service.
- [[archetypes-and-chart-of-accounts]] — The institutional taxonomy: eleven archetypes and a Chart of Accounts that classify personnel and documents by structural position and functional role.

## Ring 3 — AI gateway

One service spans Ring 3. It reads from Ring 2 and produces proposals a human reviews; it never writes to the knowledge graph or the ledger.

- [[service-slm]] — The Doorman: AI routing across local, burst, and external compute tiers; audit ledger on every call; every API key held at this boundary.
- [[service-slm-yoyo-operational]] — Operational state of service-slm and the Yo-Yo GPU burst VM: Tier A/B configuration, apprenticeship brief queue, idle-shutdown cost ceiling.
- [[service-slm-totebox-sysadmin]] — How service-slm becomes the operational assistant for Totebox deployments: ten operational task families, four-stage pipeline from corpus capture to per-tenant LoRA adapters.

## Specialist and domain services

Services built for specific platform capabilities.

- [[service-business-clustering]] — Turns raw retail data into commercial clusters: parent-child spatial schema, one commercial entity per site.
- [[service-places-filtering]] — Filters civic and institutional infrastructure to retain only regional-grade facilities for GIS tier rankings.
- [[pointsav-gis-engine]] — High-performance location intelligence in Rust: offline-first, flat-file, no centralised database instances.
- [[service-wallet-settlement]] — Wallet and direct payment settlement infrastructure.
- [[message-courier]] — Headless web-automation engine bridging internal identity ledgers with external web portals.
- [[fs-anchor-emitter]] — Signed WORM ledger checkpoints at hourly cadence, anchored to Sigstore Rekor on a monthly schedule for external auditability.
- [[service-fs-security-compliance]] — service-fs compliance posture for SEC 17a-4(f), eIDAS, and SOC 2 by structural guarantee.
- [[service-fs-data-lake]] — Flat-file data lake for the GIS pipeline: raw geospatial points from open sources, no ETL step.
- [[template-ledger]] — Distributes approved email templates to the operator's mail environment; eliminates version drift between template design and execution.

## See also

- [Systems](/systems/) — the operating systems that services run within
- [Architecture](/architecture/) — the three-ring model and the invariants that govern ring interaction
- [Infrastructure](/infrastructure/) — fleet deployment and the physical layer services run on
