---
schema: foundry-doc-v1
title: "app-orchestration-gis"
slug: app-orchestration-gis
category: applications
type: topic
quality: complete
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-06
editor: pointsav-engineering
paired_with: app-orchestration-gis.es.md
cites:
  - pmtiles-spec
  - maplibre-gl-js
---

# app-orchestration-gis

`app-orchestration-gis` is the stateless spatial analytics engine of the PointSav GIS platform. It performs linear-geometry calculations and coordinate mapping to produce the Woodfine co-location rankings and the interactive map surface at [gis.woodfinegroup.com](https://gis.woodfinegroup.com).

## Scoring Algorithm

The engine implements a linear geometric decay model using the Haversine formula. For every Alpha Anchor in the cleansed data layers, it calculates two proximity scores:

- **Secondary proximity (3.0 km radius):** score = max(0, 100 × (3.0 − distance_km) / 3.0)
- **Tertiary proximity (5.0 km radius):** score = max(0, 100 × (5.0 − distance_km) / 5.0)

The two scores combine to produce a continuous co-location score ranging from 0 to 400. Higher scores reflect greater convergence of capital-intensive operators within the defined catchment radii.

## Tile Generation

The engine compiles scored output into vector tile assets for delivery to the interactive map:

- **Vector tiles:** PMTiles format for client-side rendering without a dedicated tile server [pmtiles-spec]
- **Rendering:** MapLibre GL JS processes the tiles client-side at high performance [maplibre-gl-js]
- **Visual tiers:** Spatial convergence across anchor categories (primary, hardware, warehouse, civic) maps to a four-tier visual classification on the map surface

## Stateless Architecture

The application holds no canonical data. It operates as a pure function: cleansed cluster files enter, ranked geo-tiles exit. If the application instance is lost, the entire analytics environment can be re-provisioned by pointing a fresh instance at the immutable data layer — no state migration required.

## See Also

- [[pointsav-gis-engine]]
- [[service-business-clustering]]
- [[service-places-filtering]]

---
## Provenance
- **Source:** `app-orchestration-gis` service documentation (project-gis cluster)
- **Refinement:** 2026-05-06 by project-editorial Task
- **Verification:** Scoring algorithm, tile format, and stateless design confirmed against build configuration.
- **BCSC Posture:** Current-fact description of operational service.
