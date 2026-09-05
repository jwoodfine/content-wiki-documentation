---
schema: foundry-doc-v1
title: "GIS data lake"
slug: service-fs-data-lake
category: services
type: topic
content_type: topic
quality: complete
index_group: specialist-and-domain-services
status: active
audience: public
short_description: "The GIS pipeline's data lake is its foundational storage layer — a flat-file store holding raw geospatial points, available to every downstream step in the same pipeline. Distinct from service-fs, the platform's separate WORM ledger."
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-09-05
editor: pointsav-engineering
paired_with: service-fs-data-lake.es.md
cites: []
---

**The GIS data lake** is the foundational storage layer for the platform's [[location-intelligence-substrate|GIS pipeline]] — a flat-file store that holds raw geospatial points ingested from open sources (OpenStreetMap, Overture Maps Foundation) in separate retail and civic landing zones, available immediately to every downstream step in the same pipeline without an ETL step. Retail records — commercial operators, anchor stores, fuel outlets — and civic records — hospitals, universities, transport hubs — are kept in distinct subtrees so the [[service-places-filtering|filtering]] and [[service-business-clustering|clustering]] steps can work on each domain independently. This data lake is a distinct component from [[service-fs]], the platform's separate per-tenant WORM ledger — the two share no code and no storage format.

## Key Takeaways

- Two separate landing zones — retail and civic — hold raw points from OpenStreetMap and Overture Maps Foundation. Downstream steps read directly from the landing zones; no ETL transformation step sits between ingestion and consumption.
- Data persistence is decoupled from analytical logic. If [[app-orchestration-gis]] is reprovisioned, the raw data assets in the data lake remain intact and are immediately available to any replacement analytical layer.
- Today the landing zones are plain directories on the host filesystem, populated and read directly by the GIS pipeline's own ingestion and analysis scripts. There is no dedicated storage service, no restricted API, and no unikernel envelope in front of them. The [[service-business-clustering|business-clustering]] and [[service-places-filtering|places-filtering]] steps that read this data run as steps inside the same Python-based pipeline documented in [[app-orchestration-gis]], not as separate crates or services reading through a boundary.
- The flat-file, open-format design avoids proprietary format lock-in. Raw geospatial records are stored as plain files readable by any toolchain in any decade.

## Data Ingestion and Storage

The pipeline maintains a unified filesystem structure with separate landing zones for retail and civic infrastructure data.

- **Retail landing:** raw commercial operator records ingested from open geospatial registries (OpenStreetMap, Overture Maps Foundation).
- **Civic landing:** raw civic and institutional facility records from the same open sources.

### Architectural role

As the stateful layer of the GIS pipeline, the data lake is responsible for data persistence, kept independent of the analytical code that reads it — if [[app-orchestration-gis|the GIS orchestration layer]] is re-provisioned, the core data assets remain intact within this layer. The clean separation between data persistence and analytical logic is a core design invariant of this pipeline. It is a separate design from the platform's WORM ledger ([[service-fs]]), which anchors institutional records for compliance rather than storing raw geospatial points — the two are not layers of one shared four-layer system.

## What this is not

There is no dedicated storage service or restricted API in front of these landing zones today — they are plain host-filesystem directories, read and written directly by the GIS ingestion and analysis scripts with ordinary file I/O. No `service-business` or `service-places` crate exists in the codebase; the business-clustering and places-filtering steps are Python steps inside [[app-orchestration-gis]]'s own pipeline, not separately deployed services with their own storage boundary. The [[retail-co-location-tier-methodology|retail co-location tier methodology]] describes how the clustering output is used to generate tier rankings.

## See also

- [[service-business-clustering]]
- [[service-places-filtering]]
- [[app-orchestration-gis]]
- [[service-fs]] — the platform's separate WORM ledger; a distinct component from this data lake
