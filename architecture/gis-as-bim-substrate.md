---
schema: foundry-doc-v1
title: "GIS as a BIM substrate"
slug: gis-as-bim-substrate
short_description: "What the PointSav GIS co-location dataset offers a BIM composition pipeline: cluster manifold fields, civic context layers, and stability guarantees."
category: architecture
type: topic
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-25
editor: pointsav-engineering
paired_with: gis-as-bim-substrate.es.md
---

# GIS as a BIM substrate

Building Information Modelling (BIM) occupies the building scale: structural geometry, material assemblies, mechanical systems, occupancy. A model is meaningful in isolation, but its commercial value emerges when it is sited — positioned in a real geography with real neighbours, real catchments, and real regulatory context. The [[pointsav-overview|PointSav]] GIS [[co-location-methodology|co-location]] dataset is designed to provide that siting context to BIM composition pipelines.

This article documents what the GIS dataset offers a BIM consumer, which fields are stable, and what extensions are anticipated.

---

## The cluster manifold

The primary GIS output is a manifold of approximately 6,400 deduplicated commercial co-location clusters across the United States, Canada, Mexico, the United Kingdom, and continental Europe. Each cluster carries:

- a stable identifier and fixed geographic position (latitude/longitude)
- the regional name resolved through the layered boundary engine
- the tier classification (Regional, District, Local, Fringe)
- the categorical composition (which anchor types are present)
- the count of stores within nested catchment radii (1 km, 2 km, 3 km)

For a BIM consumer, this manifold answers questions a model alone cannot: How densely commercial is the area within 3 km of this proposed building? Which anchor formats already serve the catchment? Where is the nearest equivalent existing site against which a model could be benchmarked?

---

## Cluster properties available for BIM ingest

Each cluster's properties record carries fields suitable for direct ingest by a city-code composition pipeline:

| Field | Type | BIM use |
|---|---|---|
| `cluster_id` | string | Stable join key |
| `latitude`, `longitude`, `centroid_lat`, `centroid_lon` | float | Anchor and centroid positions for siting |
| `region_name` | string | Resolved metro or municipal name; useful as a model parameter |
| `tier_descriptor` | string | Regional / District / Local / Fringe — density signal |
| `count_1km`, `count_3km` | integer | Catchment density |
| `unique_brands` | integer | Distinct retail brands within catchment |
| `merged_zones` | array | Same-zone clusters consolidated; shown for transparency |
| `iso`, `state` | string | Jurisdiction codes |

The cluster manifold is published as PMTiles with a layer schema supporting individual store positions (Layer 1) and cluster envelopes with proximity rings (Layer 2). A BIM consumer can fetch the GeoJSON manifest at `/data/clusters-meta.json` for direct lat/lon access, or read the PMTiles directly via byte-range requests for spatially indexed queries.

---

## Region resolution depth

The boundary engine resolves coordinates to one of five granularities, from most specific to most general:

1. GADM admin-3 (Canadian Census Subdivision proxies, Mexican Municipios)
2. GADM admin-2 (where admin-3 is unavailable)
3. Eurostat NUTS-3 (European regions)
4. Statistics Canada CMA / US Census Core-Based Statistical Area
5. Natural Earth admin-1 (state/province global fallback)

A BIM composition that needs to anchor against a municipal jurisdiction — for instance, a building proposed inside Strathcona County in Alberta — receives that level of resolution. A composition that needs only a metropolitan reference frame receives the surrounding CMA.

---

## Civic context layers

Beyond the cluster manifold, the GIS dataset includes two civic layers relevant to building programmes that depend on civic adjacency:

- **Hospital catalogue.** Approximately 28,000 hospital locations across the operational footprint, sourced from OpenStreetMap.
- **University catalogue.** Approximately 19,000 higher-education locations, similarly sourced.

Distance to the nearest hospital and nearest university are computed per cluster within a 5 km practical limit. For a BIM consumer modelling a healthcare-adjacent or campus-adjacent programme, these distances are direct inputs.

---

## Stability guarantees

**Stable across releases:** cluster identifiers, the manifold structure, the tier classification scheme, the regional name resolution algorithm, and the catchment radii.

**Likely to change:** the size of the brand-family taxonomy (food and pharmacy families are expanding), the absolute store counts (OpenStreetMap coverage is improving year over year), and the inclusion of additional countries (Belgium, Luxembourg, Ireland, and Switzerland are absent from the May 2026 footprint).

A BIM composition that joins on `cluster_id` sees growth but no deletion of existing identifiers. A composition that joins on `region_name` should be aware that text values may shift slightly with each region-engine refinement.

---

## See Also

- [[co-location-methodology]]
- [[regional-name-resolution-architecture]]
- [[city-code-as-composable-geometry]]
