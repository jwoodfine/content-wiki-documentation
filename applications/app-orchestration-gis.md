---
schema: foundry-doc-v1
title: "GIS orchestration application"
slug: app-orchestration-gis
category: applications
type: topic
content_type: topic
quality: complete
index_group: location-intelligence-applications
status: active
audience: public
short_description: "Stateless spatial analytics engine producing the Woodfine co-location rankings and interactive map — a pure function holding no canonical data."
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-08-01
editor: pointsav-engineering
paired_with: app-orchestration-gis.es.md
cites:
 - pmtiles-spec
 - maplibre-gl-js
---

**Correction (2026-08-02):** `app-orchestration-gis` (this archive's directory of that name) is a placeholder — its own README states plainly "Reserved-folder — directory created to close registry drift... implementation details in project-gis cluster." The real implementation is a Python data pipeline (ingest/cluster/tile-build scripts) in the separate `project-gis` archive, not a Rust engine here. `os-orchestration` is a real crate on canonical but currently an empty placeholder scaffold (retracted from an earlier, wrong "doesn't exist as a built crate" claim — see [[app-orchestration-command-branch-model]]), and `[[service-business-clustering]]`/`[[service-places-filtering]]` have no corresponding directories anywhere in the workspace — already flagged to Command (`command-20260801-gis-cluster-wiki-fix-found-service-busin`, sent during the Round 4 GIS cluster merge), not re-escalated here. The PMTiles/MapLibre/tier-methodology mechanics described elsewhere in this article are independently verified accurate against the real pipeline — only the product/architecture framing around them (Rust engine, this directory, os-orchestration hosting) is wrong. **Flagged, not resolved.**

`app-orchestration-gis` is the stateless spatial analytics engine that performs linear-geometry calculations and coordinate mapping to produce the Woodfine co-location rankings and the interactive map at [gis.woodfinegroup.com](https://gis.woodfinegroup.com). The application holds no canonical data — it operates as a pure function from cleansed cluster files to ranked geo-tiles, so a lost instance can be re-provisioned by pointing a fresh process at the immutable [[totebox-archive|Totebox data layer]] with no state migration. It runs on [[os-orchestration|`os-orchestration`]] and composes with [[service-business-clustering]] and [[service-places-filtering]] to produce its input datasets.

## Tier Assignment

The engine assigns every cluster one of four tiers by testing it against the
[[retail-co-location-tier-methodology|retail co-location tier methodology]] — composition,
catchment-population rank, civic support, and non-overlap with stronger neighboring
clusters. Tier assignment is a pass/fail classification against fixed gates, not a
composite numeric score.

## Tile Generation

The engine compiles scored output into vector tile assets for delivery to the interactive map:

- **Vector tiles:** PMTiles format for client-side rendering without a dedicated tile server [pmtiles-spec]
- **Rendering:** MapLibre GL JS processes the tiles client-side at high performance [maplibre-gl-js]
- **Visual tiers:** Spatial convergence across anchor categories (primary, hardware, warehouse, civic) maps to the four-tier visual classification on the map surface, per the [[retail-co-location-tier-methodology|tier methodology]] above

## Stateless Architecture

The application holds no canonical data. It operates as a pure function: cleansed cluster files enter, ranked geo-tiles exit. If the application instance is lost, the entire analytics environment can be re-provisioned by pointing a fresh instance at the immutable data layer — no state migration required.

## See also

- [[location-intelligence-substrate]] — the rendering layer that serves tiles produced by this engine
- [[service-business-clustering]] — the clustering service that groups POI data into co-location clusters
- [[service-places-filtering]] — the places filtering service that prepares cleansed input data
- [[retail-co-location-tier-methodology]] — the tier methodology implemented by the engine
- [[location-intelligence-platform]] — the platform article covering the full GIS deployment
