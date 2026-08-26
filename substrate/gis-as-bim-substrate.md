---
schema: foundry-doc-v1
title: "GIS as a BIM substrate"
slug: gis-as-bim-substrate
language: en
category: substrate
index_group: core-named-substrates
type: topic
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-08-26
editor: pointsav-engineering
short_description: "What the co-location dataset offers a BIM composition pipeline: the cluster manifold and its joinable fields, region-resolution depth, civic context layers, and the stability guarantees a downstream consumer can rely on."
cites: []
paired_with: gis-as-bim-substrate.es.md
---

Building Information Modelling occupies the building scale — structural geometry, material assemblies, mechanical systems, occupancy. A model is meaningful in isolation, but its commercial value emerges when it is *sited*: positioned in a real geography with real neighbours, real catchments, and real regulatory context. The [[location-intelligence-substrate|location intelligence substrate]]'s co-location dataset is designed to supply that siting context to a BIM composition pipeline.

**Why it matters:** two substrates that share a coordinate system and a ledger can be joined by a key rather than reconciled by hand, which is what makes "where is this building" a queryable property of the model rather than a separate document.

This article documents what the dataset offers a BIM consumer, which fields are stable, and what extensions are anticipated.

## The cluster manifold

The primary output is a manifold of roughly 6,400 deduplicated commercial co-location clusters across the United States, Canada, Mexico, the United Kingdom, and continental Europe. Each cluster carries a stable identifier and fixed geographic position, the regional name resolved through the [[regional-name-resolution-architecture|layered boundary engine]], a tier classification, its categorical composition, and store counts within nested catchment radii of one, two, and three kilometres.

For a BIM consumer, the manifold answers questions a model alone cannot: how densely commercial is the area within three kilometres of this proposed building, which anchor formats already serve the catchment, and where is the nearest equivalent existing site against which the model could be benchmarked.

**Why it matters:** these are the questions that decide whether a building is worth designing, and they have historically lived in a consultant's report rather than in a queryable dataset.

## Cluster properties available for BIM ingest

Each cluster's properties record carries fields suitable for direct ingest by a composition pipeline:

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

The manifold is published as PMTiles with a layer schema supporting individual store positions (layer 1) and cluster envelopes with proximity rings (layer 2). A consumer can fetch the GeoJSON manifest for direct coordinate access, or read the PMTiles via byte-range requests for spatially indexed queries.

**Why it matters:** a consumer needs no database and no API key — the dataset is a file it can read directly, in line with the substrate's flat-file posture.

## Region resolution depth

The boundary engine resolves coordinates to one of five granularities, most specific first: GADM admin-3 (Canadian Census Subdivision proxies, Mexican municipios); GADM admin-2 where admin-3 is unavailable; Eurostat NUTS-3 for European regions; Statistics Canada CMA or US Census Core-Based Statistical Area; and Natural Earth admin-1 as a global state or province fallback.

A composition that needs to anchor against a municipal jurisdiction receives that level of resolution. One that needs only a metropolitan reference frame receives the surrounding CMA.

**Why it matters:** jurisdictional resolution is what lets a [[city-code-as-composable-geometry|regulatory overlay]] be selected automatically rather than chosen by hand for each project.

## Civic context layers

Beyond the cluster manifold, two civic layers are relevant to building programmes that depend on civic adjacency: a catalogue of roughly 28,000 hospital locations across the operational footprint, and roughly 19,000 higher-education locations, both sourced from OpenStreetMap. Distance to the nearest hospital and nearest university is computed per cluster within a five-kilometre practical limit.

**Why it matters:** for a healthcare-adjacent or campus-adjacent programme, these distances are direct model inputs rather than context a designer has to research separately.

## Stability guarantees

**Stable across releases:** cluster identifiers, the manifold structure, the tier classification scheme, the regional name-resolution algorithm, and the catchment radii.

**Likely to change:** the size of the brand-family taxonomy (food and pharmacy families are expanding), absolute store counts (OpenStreetMap coverage improves year over year), and the set of countries included.

A composition that joins on `cluster_id` sees growth but no deletion of existing identifiers. A composition that joins on `region_name` should expect text values to shift slightly as the region engine is refined.

**Why it matters:** a downstream consumer can decide which fields are safe to build on before writing the join, rather than discovering a breaking change after a rebuild.

## See also

- [[location-intelligence-substrate]] — the flat-file GIS architecture this dataset is produced by
- [[regional-name-resolution-architecture]] — how `region_name` is resolved
- [[city-code-as-composable-geometry]] — the jurisdictional overlay the resolved region selects
- [[service-business-clustering]] — the clustering service that produces the manifold
