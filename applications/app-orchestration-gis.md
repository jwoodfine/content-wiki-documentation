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
short_description: "The Python data pipeline that produces the Woodfine co-location rankings and interactive map — cluster geometry rebuilt on a nightly schedule from source datasets, published as static map tiles."
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-08-22
editor: pointsav-engineering
paired_with: app-orchestration-gis.es.md
cites:
 - pmtiles-spec
 - maplibre-gl-js
---

The pipeline that produces the Woodfine co-location rankings and the interactive map at [gis.woodfinegroup.com](https://gis.woodfinegroup.com) is a Python data pipeline, not a standing service — it holds no canonical data of its own and produces no output until it runs. Each nightly rebuild reads current business and places datasets, re-clusters them, re-tiers each cluster, and writes fresh map tiles; the tiles it produces are what the site actually serves between rebuilds.

## Tier assignment

The pipeline assigns every cluster one of four tiers by testing it against the
[[retail-co-location-tier-methodology|retail co-location tier methodology]] — composition,
catchment-population rank, civic support, and non-overlap with stronger neighboring
clusters. Tier assignment is a pass/fail classification against fixed gates, not a
composite numeric score.

## Tile generation

The pipeline compiles scored output into vector tile assets for delivery to the interactive map:

- **Vector tiles:** PMTiles format for client-side rendering without a dedicated tile server [pmtiles-spec]
- **Rendering:** MapLibre GL JS processes the tiles client-side at high performance [maplibre-gl-js]
- **Visual tiers:** Spatial convergence across anchor categories (primary, hardware, warehouse, civic) maps to the four-tier visual classification on the map surface, per the [[retail-co-location-tier-methodology|tier methodology]] above

## Rebuild cadence, not a request-driven service

The pipeline runs on a nightly schedule, not on demand. A rebuild re-clusters current source data, regenerates the tile layers, and publishes the result; the site between rebuilds serves whatever the last successful run produced. This makes recovery simple in one specific sense: a lost or corrupted tile set is replaced by the next scheduled rebuild, or an on-demand re-run, with no state migration required. It also means the published map reflects data as of the last rebuild, not the current instant.

## See also

- [[location-intelligence-substrate]] — the rendering layer that serves tiles produced by this pipeline
- [[retail-co-location-tier-methodology]] — the tier methodology implemented by the pipeline
- [[location-intelligence-platform]] — the platform article covering the full GIS deployment
