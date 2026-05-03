---
schema: foundry-doc-v1
title: "Services — Category Landing"
slug: _index
category: services
status: pre-build
last_edited: 2026-04-29
editor: pointsav-engineering
---

## Services

This category covers the autonomous services that implement Ring 1 and Ring 2 of the three-ring architecture. Ring 1 services handle per-tenant boundary ingest — each one implements a Model Context Protocol server interface, the standard by which external systems connect to the platform. Ring 2 services provide deterministic knowledge and processing: extraction, content management, search, and egress. The platform functions fully across both rings without AI compute.

Each article describes one service: its purpose, its position in the ring structure, the API contract it presents, and the data it owns. Articles are written for engineers integrating with or extending a service, and for architects evaluating how the platform composes.

`service-slm` is the single boundary between Ring 2 and Ring 3 — the Doorman that routes AI requests among three compute tiers and holds all API keys. Its article describes the routing logic and the audit surface it produces.

## Articles in this category

- [[service-email]] — The Ring 1 ingest service for email: MCP interface, per-tenant isolation, and the WORM-ledger write path.
- [[service-extraction]] — The Ring 2 extraction service: deterministic parsing, structured-record production, and the service-content write path.
- [[service-people]] — The Ring 1 identity and contacts ingest service: person records, role assignments, and tenant scoping.
- [[service-search]] — The Ring 2 full-text search service: Tantivy index, per-tenant sharding, and query API.
- [[service-slm]] — The Ring 3 Doorman: AI routing across local, burst, and external compute tiers; audit ledger; key management.

<!-- ENGINE: this list is editorial in iteration-1; iteration-2+
generates it from category-directory file listing once PL.7
chunked-migration moves articles into category subdirectories. -->

## See also

- [Wiki home](/)
- [Architecture](/architecture/)
- [Systems](/systems/)

<!-- EDITORIAL NOTE: PL.7 chunked normalization sweep will migrate
     root-prefixed TOPICs into this category subdirectory. Until
     migration lands, the existing root TOPICs render at their current
     URLs (topic-<slug>.md); this landing references them by current slug. -->
