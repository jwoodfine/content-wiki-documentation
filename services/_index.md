---
schema: foundry-doc-v1
title: "Platform Services"
slug: services-index
category: services
type: topic
content_type: topic
quality: complete
short_description: "The autonomous services that implement Ring 1 boundary ingest and Ring 2 deterministic knowledge processing in the PointSav three-ring architecture — grouped by ring layer and function."
index_type: thematic
index_scope: services
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-08-22
editor: pointsav-engineering
paired_with: _index.es.md
---

PointSav's three-ring architecture assigns every service to a layer with defined authority and dependencies. Ring 1 services handle per-tenant boundary ingest — each accepts raw data from one external source and writes it to a durable ledger. Ring 2 services provide deterministic knowledge and processing: they read from Ring 1 and produce structured records, knowledge graphs, and search indexes. Ring 3 is a single service, service-slm, which reads from Ring 2 and never writes to it.

The platform functions fully across Rings 1 and 2 without AI compute — a deployment can exclude Ring 3 entirely, shrinking the attack surface and satisfying network-isolation requirements. Where Ring 3 is included, the compliance question of whether AI has touched the authoritative record is answered architecturally, not procedurally: Ring 2 services may call Ring 3 for extraction or classification proposals (`service-extraction`'s corpus hand-off to `service-content`, which calls the Doorman for grammar-constrained entity extraction into the DataGraph, is one such path), but Ring 3 never writes to the knowledge graph, the ledger, or any structured record store. Every accepted proposal enters the record only through a Ring 2 write path with a human approval checkpoint.

<!-- START-HERE-HIGHLIGHT: engine reads this block to render the single "start here" card
     (reuses the existing cluster-card--start-here component). Do not add more than one. -->

**Start here:** [[service-fs]] — the filesystem service every other Ring 1 service writes to, and the foundation of the WORM audit posture the rest of this category assumes.

<!-- END-START-HERE-HIGHLIGHT -->

## Ring 1 — Boundary ingest

Per-tenant boundary services. Each runs as a separate process per tenant and exposes a Model Context Protocol server interface.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: ring-1-boundary-ingest -->
- [[service-fs]] — The filesystem service: append-only WORM ledger, per-tenant storage root, the foundation every other Ring 1 service writes to — architecture, durability, and the SEC 17a-4(f)/eIDAS/SOC 2 compliance posture it enables by construction.
- [[service-email]] — Email ingest: SMTP and IMAP, sanitised payloads, append-only Maildir on local block storage.
- [[service-people]] — Identity ledger: an F2 os-console surface exposing append, lookup, and regex-based email-scan tools over MCP, backed by a store that rejects conflicting identities.
- [[service-input]] — Document intake at the Ring 1 boundary: parses PDF, Markdown, DOCX, and XLSX by format detection, normalizes to a `ParsedDocument`, and hands off to service-fs for WORM ledger commit.
<!-- END AUTO-GENERATED -->

## Ring 2 — Knowledge and processing

Deterministic processing services. Each reads from Ring 1 and produces structured records — no AI variance enters the authoritative record.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: ring-2-knowledge-and-processing -->
- [[service-extraction]] — The central Ring 2 traffic controller: strips proprietary formatting, constructs Entity Bundles, assigns transaction IDs, routes to deterministic services or to service-slm.
- [[service-content]] — The Gravity Engine: reads raw payloads from a Totebox, runs them against an institutional taxonomy, generates the structured documents an organisation publishes.
- [[service-search]] — Full-text search on Tantivy: a designed but not yet built inverted-index service — only a description exists today, no source code.
- [[service-egress]] — Physical release valve: structured records leave the platform only through this service.
- [[archetypes-and-chart-of-accounts]] — The institutional taxonomy: eleven archetypes and a Chart of Accounts that classify personnel and documents by structural position and functional role.
<!-- END AUTO-GENERATED -->

## Ring 3 — AI gateway

One service spans Ring 3. It reads from Ring 2 and produces proposals a human reviews; it never writes to the knowledge graph or the ledger.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: ring-3-ai-gateway -->
- [[service-slm]] — The Doorman: AI routing across local, burst, and external compute tiers; audit ledger on every call; every API key held at this boundary.
- [[service-slm-yoyo-operational]] — Operational state of service-slm and the Yo-Yo GPU burst VM: Tier A/B configuration, apprenticeship brief queue, idle-shutdown cost ceiling.
- [[service-slm-totebox-sysadmin]] — A planned direction for service-slm as a Totebox sysadmin assistant, built on the real, already-operational apprenticeship training pipeline — the specific task taxonomy is proposed, not yet registered.
- [[service-slm-graph-store-migration]] — The DataGraph's live property graph: nightly LadybugDB rebuild via grammar-constrained entity extraction through the Doorman, writing directly with no review step of its own.
- [[yoyo-daily-enrichment-cycle]] — The Yo-Yo GPU burst VM's daily batch window: two phases, DataGraph rebuild and (once fully enabled) adapter training — training currently runs in marker-only mode.
<!-- END AUTO-GENERATED -->

## Specialist and domain services

Services built for specific platform capabilities.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: specialist-and-domain-services -->
- [[service-business-clustering]] — Turns raw retail data into commercial clusters: parent-child spatial schema, one commercial entity per site.
- [[service-places-filtering]] — Filters civic and institutional infrastructure to retain only regional-grade facilities for GIS tier rankings.
- [[service-wallet-settlement]] — Wallet and direct payment settlement: a planned per-tenant accounting ledger design, not yet built.
- [[message-courier]] — Headless web-automation engine bridging internal identity ledgers with external web portals.
- [[fs-anchor-emitter]] — Signed WORM ledger checkpoints at hourly cadence, anchored to Sigstore Rekor on a monthly schedule for external auditability.
- [[service-fs-data-lake]] — Flat-file data lake for the GIS pipeline: raw geospatial points from open sources, no ETL step.
- [[template-ledger]] — Distributes approved email templates to the operator's mail environment; eliminates version drift between template design and execution.
- [[editorial-pipeline-three-stages]] — Three-stage proofreading pipeline ordered by cost: deterministic banned-vocabulary scan, LanguageTool mechanical pass, then a generative rewrite routed through the inference layer.
- [[private-git-paid-customer-endpoint]] — The binary release server behind software.pointsav.com: verifies Ed25519 license tokens and streams compiled binaries, holding no payment records or signing keys.
- [[service-pointsav-link]] — A named but unbuilt design concept for a fleet-connecting adapter; no corresponding package exists in the monorepo today.
- [[service-vm-fleet]] — The placement and registry service for the PPN VM resource pool: two-pass placement algorithm and heartbeat-driven node state.
- [[poi-data-schema]] — The record structures for location data ingested from OpenStreetMap and Overture Maps Foundation, normalised into a unified JSONL schema before cluster analysis.
- [[regional-name-resolution-architecture]] — The layered offline reverse-geocoding engine that turns a cluster's coordinates into a human-readable regional name, with no external API calls.
- [[service-vm-tenant]] — The customer-facing tenant proxy for the PPN VM resource pool: authentication, namespace isolation, quota enforcement, and an immutable audit trail.
<!-- END AUTO-GENERATED -->

## See also

- [Operating Systems](/systems/) — the operating systems that services run within
- [How It's Built](/architecture/) — the three-ring model and the invariants that govern ring interaction
- [Where It Runs](/infrastructure/) — fleet deployment and the physical layer services run on
