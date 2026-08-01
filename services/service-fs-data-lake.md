---
schema: foundry-doc-v1
title: "FS data lake"
slug: service-fs-data-lake
category: services
type: topic
content_type: topic
quality: complete
status: active
audience: public
short_description: "service-fs is the foundational storage layer for the GIS pipeline — a flat-file data lake storing raw geospatial points, available to every downstream service."
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-07-31
editor: pointsav-engineering
paired_with: service-fs-data-lake.es.md
cites: []
---

**`service-fs`** is the foundational storage layer for the platform's [[pointsav-gis-engine|GIS pipeline]] — a flat-file data lake that stores raw geospatial points ingested from open sources (OpenStreetMap, Overture Maps Foundation) in separate retail and civic landing zones, available immediately to every downstream service without an ETL step. Retail records — commercial operators, anchor stores, fuel outlets — and civic records — hospitals, universities, transport hubs — are kept in distinct subtrees so the [[service-places-filtering|filtering]] and [[service-business-clustering|clustering]] services can work on each domain independently.

## Key Takeaways

- Two separate landing zones — retail and civic — hold raw points from OpenStreetMap and Overture Maps Foundation. Downstream services read directly from the landing zones; no ETL transformation step sits between ingestion and consumption.
- Data persistence is decoupled from analytical logic. If `[[app-orchestration-gis]]` is reprovisioned, the raw data assets in `service-fs` remain intact and are immediately available to any replacement analytical layer.
- The target production deployment is a low-overhead unikernel exposing a restricted API, with only the intelligence layers ([[service-business-clustering|`service-business`]] and [[service-places-filtering|`service-places`]]) able to read raw data and write back processed results. **Not yet built**: today the landing zones are plain directories on the host filesystem, populated and read by ingestion/analysis scripts directly — no unikernel, no restricted API, no dedicated `service-business`/`service-places` crates confirmed in the codebase yet.
- The flat-file, open-format design avoids proprietary format lock-in. Raw geospatial records are stored as plain files readable by any toolchain in any decade.

## Data Ingestion and Storage

The service maintains a unified filesystem structure with separate landing zones for retail and civic infrastructure data.

- **Retail landing:** raw commercial operator records ingested from open geospatial registries (OpenStreetMap, Overture Maps Foundation).
- **Civic landing:** raw civic and institutional facility records from the same open sources.

### Architectural Role

As the stateful layer of the platform, `service-fs` is responsible for data persistence. It is designed to be independent of the analytical software — if the [[app-orchestration-gis|GIS orchestration layer]] is re-provisioned, the core data assets remain intact within this layer. The clean separation between data persistence and analytical logic is a core design invariant. This same separation principle extends to the WORM ledger used for institutional records; see [[service-fs-architecture|FS architecture]] for the full four-layer design.

## Unikernel Implementation (Planned)

The target production deployment is a low-overhead unikernel providing a restricted API for the [[service-business-clustering|`service-business`]] and [[service-places-filtering|`service-places`]] intelligence layers to read raw data and write back processed results, enforcing clean separation between storage and analysis concerns. **Current state**: the unikernel envelope does not exist yet — the landing zones described above are plain host-filesystem directories, read and written directly by the GIS ingestion and analysis scripts (verified against `app-orchestration-gis`'s own ingestion scripts, which read/write these paths with ordinary file I/O). The [[retail-co-location-tier-methodology|retail co-location tier methodology]] describes how the clustering output is used to generate tier rankings, once that analysis layer is built.

## See also

- [[service-business-clustering]]
- [[service-places-filtering]]
- [[app-orchestration-gis]]
- [[service-pointsav-link|PointSav Link Service]] — fleet adapter that makes os-* storage accessible across node boundaries
