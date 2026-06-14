---
schema: foundry-doc-v1
title: "GIS orchestration application"
slug: app-orchestration-gis
category: applications
type: topic
content_type: topic
quality: complete
status: active
audience: public
short_description: "app-orchestration-gis is the stateless spatial analytics engine that performs linear-geometry calculations and coordinate mapping to produce the Woodfine co-location rankings and the interactive map at gis.woodfinegroup.com — a pure function that holds no canonical data and can be re-provisioned by pointing a fresh instance at the immutable data layer."
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-08
editor: pointsav-engineering
paired_with: app-orchestration-gis.es.md
cites:
 - pmtiles-spec
 - maplibre-gl-js
---

`app-orchestration-gis` is the stateless spatial analytics engine that performs linear-geometry calculations and coordinate mapping to produce the Woodfine co-location rankings and the interactive map at [gis.woodfinegroup.com](https://gis.woodfinegroup.com). The application holds no canonical data — it operates as a pure function from cleansed cluster files to ranked geo-tiles, so a lost instance can be re-provisioned by pointing a fresh process at the immutable [[totebox-archive|Totebox data layer]] with no state migration. It runs on [[os-orchestration|`os-orchestration`]] and composes with [[service-business-clustering]] and [[service-places-filtering]] to produce its input datasets.

## Scoring Algorithm

The engine implements a linear geometric decay model using the Haversine formula. For every Alpha Anchor in the cleansed data layers, it calculates two proximity scores:

- **Secondary proximity (3.0 km radius):** score = max(0, 100 × (3.0 − distance_km) / 3.0)
- **Tertiary proximity (5.0 km radius):** score = max(0, 100 × (5.0 − distance_km) / 5.0)

The two scores combine to produce a continuous co-location score ranging from 0 to 400. Higher scores reflect greater convergence of capital-intensive operators within the defined catchment radii.

## Tile Generation

The engine compiles scored output into vector tile assets for delivery to the interactive map:

- **Vector tiles:** PMTiles format for client-side rendering without a dedicated tile server [pmtiles-spec]
- **Rendering:** MapLibre GL JS processes the tiles client-side at high performance [maplibre-gl-js]
- **Visual tiers:** Spatial convergence across anchor categories (primary, hardware, warehouse, civic) maps to a four-tier visual classification on the map surface, expressed through the [[co-location-methodology|co-location scoring methodology]]

## Stateless Architecture

The application holds no canonical data. It operates as a pure function: cleansed cluster files enter, ranked geo-tiles exit. If the application instance is lost, the entire analytics environment can be re-provisioned by pointing a fresh instance at the immutable data layer — no state migration required.

## See also

- [[pointsav-gis-engine]] — the rendering layer that serves tiles produced by this engine
- [[service-business-clustering]] — the clustering service that groups POI data into co-location clusters
- [[service-places-filtering]] — the places filtering service that prepares cleansed input data
- [[co-location-methodology]] — the scoring and ranking methodology implemented by the engine
- [[location-intelligence-platform]] — the platform article covering the full GIS deployment

## References

- [Haversine formula](https://en.wikipedia.org/wiki/Haversine_formula) — Wikipedia, accessed 2026-06-14
