---
schema: foundry-doc-v1
title: "Trade-area methodology"
slug: trade-area-methodology
category: architecture
type: concept
content_type: topic
quality: complete
status: stable
bcsc_class: public-disclosure-safe
language: en
last_edited: 2026-06-23
editor: pointsav-engineering
paired_with: trade-area-methodology.es.md
cites: []
---

The trade-area methodology governs how the Woodfine location intelligence map (gis.woodfinegroup.com) defines, renders, and labels the area around each co-location cluster from which customers are estimated to travel. A trade area is not simply the geographic extent of the stores in a cluster; it is a representation of where demand originates. The methodology specifies, plainly and with its limitations stated, how that representation is constructed at each stage of the product's development.

## What the map shows today

The live map renders a distance band around each cluster centroid. **Until the observed-trade-area pipeline is integrated, that band is a straight-line radius, not a measured catchment.** The labelling rule is unambiguous: any geometry derived from a straight-line formula reads as "distance band (straight-line)" on the map face and in the detail panel — never "catchment" and never "trade area."

The Method modal carries a plain statement: *"Distance bands are straight-line radii around the cluster centroid; they approximate, but do not measure, where customers come from."*

This is a deliberate honesty edit. A clearly-labelled approximation is defensible in front of a reviewer; a circle mislabelled as a measured catchment is not.

Distances are computed geodesically rather than on screen. A band labelled 35 km represents 35 km of actual ground distance regardless of latitude, because haversine distances and metric geodesic buffers are used throughout. The rendered ring is a Web Mercator oval on screen; the underlying number is projection-independent.

## The intended model: observed origins and drive-time

A trade area is the set of places customers actually travel from. Two methods — drive-time isochrones and empirical origin-destination polygons — are planned as successive improvements to the current distance bands.

### Drive-time isochrones

An isochrone replaces the straight-line radius with the area reachable within a stated drive time (for example 10, 20, or 30 minutes) along the road network. Isochrones respect barriers that circles ignore — rivers, motorway access, mountain passes, one-way coastal routes — so two clusters with identical straight-line radii can have substantially different reachable areas. Drive-time isochrones are the retail-geography standard that site-selection reviewers expect.

The intended implementation uses a self-hosted routing engine over the OSM extracts already ingested in the archive. A dependency on a metered third-party isochrone API is not the intended path for a product built on sovereign, self-contained data infrastructure. The specific routing engine is an open question in the engineering backlog.

### Observed origin-destination polygons

Rather than modelling where customers could come from, an O-D polygon draws where they do come from, using mobility data already on disk:

- **United States — US LEHD LODES.** Worker origin-destination flows aggregated to H3 cells, 49 states, approximately 684,000 H3 cells. Supports a workplace-origin trade area for US clusters.
- **Spain — MITMA.** The Spanish Ministry of Transport mobility matrices are ingested for 58 ES clusters, providing an observed origin distribution rather than a modelled ring.
- **`layer6-mobility-work.pmtiles`.** The combined US LODES and MITMA work-origin surface is built and served as a map tile layer. The data needed to render observed origin polygons for US and Spain clusters is present; the integration that turns a cluster click into an observed-origin polygon, rather than a ring, is planned but not yet wired.

The intended O-D trade area for a cluster is the set of origin cells contributing the top share — for example 70–80% — of observed trips or workers to that cluster's destination cells. Coverage is uneven (US and Spain today; UK, France, and Germany researched as viable next sources), so the planned rollout is country-by-country. Clusters without O-D coverage keep the clearly-labelled distance band as an explicit interim.

### Why both methods are complementary

Drive-time isochrones answer the question "who can reach this site." Observed O-D polygons answer "who actually shops or works here." The intended map exposes the best available representation per cluster, with the Method modal stating which model produced the polygon on screen and over what vintage. A measured polygon and a drawn circle are never combined under a single label.

## The previous radius formula

The distance band used in the initial product version was computed as:

```
radius_km = max(1.0, span_km / 2 × 1.15)
```

where `span_km` is the extent of the member stores within the cluster.

This is a geometric artifact, not a demand quantity. It describes how spread out the stores are, then inflates that half-span by 15%. It carries no information about how far customers travel. Two failure modes follow directly: a dense urban cluster gets a small ring because its stores sit close together, even though its trade area may be large; a sprawling exurban cluster gets a large ring because its stores sit far apart, not because it draws from far away.

Neither the `1.15` inflation factor nor the `1.0 km` floor has a published derivation. They are tuning constants that make the picture look reasonable. Until observed O-D or drive-time boundaries are adopted, any interim distance band discloses the formula and both constants in the Method modal rather than applying them silently.

The intended end state removes the `span_km / 2 × 1.15` expression from the live pipeline entirely, replacing it with a boundary whose parameter is a quantity a domain expert can evaluate on its merits — a stated drive-time, a stated percentile of modelled demand, or a stated population threshold.

## Geodesic computation and the Web Mercator caveat

The map renders in Web Mercator (EPSG:3857). Web Mercator preserves shape locally but distorts area and on-screen distance with latitude: scale inflates as 1 / cos(latitude). A circle of constant pixel radius is not a circle of constant ground distance.

The methodology therefore computes distances and areas geodesically:

- Distance tests use the haversine (great-circle) distance between geographic coordinates, consistent across all 13 countries and both the North American and European frames.
- Polygon construction uses metric geodesic buffers — turf's metric buffer builds geometry in true ground distance and projects to Web Mercator only for display, so the rendered polygon is the correct ground shape even though it appears as a latitude-stretched oval on screen.
- Area figures — catchment area, density per square kilometre — are computed on the geodesic polygon, not from screen pixels.

The Method modal carries the caveat: *"Distances and areas are computed on the ellipsoid; the map is drawn in Web Mercator, which stretches with latitude — a band at 60°N covers less ground than the same band drawn at 25°N."*

## Spatial framework

Population and spend are aggregated on the H3 global hexagonal grid at resolution 7 (approximately 5.16 km² per cell, approximately 2.11 km centre-to-centre). The grid is worldwide and consistent, which supports cross-cluster comparison across all 13 countries. This revision does not change the aggregation grid; it changes how the trade-area polygon over that grid is defined — by observed origin or drive-time where data allows, and by a clearly-labelled, geodesically-computed distance band where it does not yet.

A single H3 cell may fall inside the trade areas of several clusters. This is intentional: trade areas overlap because the retail landscape is competitive, and a household near two competing clusters contributes to both. This holds whether the boundary is a distance band, an isochrone, or an O-D polygon, and it underpins the cross-cluster comparison.

## Migration plan (planned)

The intended migration from crow-flies rings is phased:

1. **Honesty edit.** Relabel every straight-line ring "distance band (straight-line)"; surface the radius formula, the 1.15 factor, the 1.0 km floor, and the Web Mercator caveat in the Method modal.
2. **Observed O-D where data exists.** Wire the ingested LODES and MITMA mobility data into the cluster-click so US and Spain clusters show an observed work-origin polygon; clusters without coverage retain the labelled distance band.
3. **Drive-time isochrones.** Stand up a self-hosted routing engine and offer a fixed-drive-time band as the default reachable-area view, removing the `span_km / 2 × 1.15` expression from the live pipeline.
4. **Distance-decay calibration.** Fit decay curves to the O-D flows to set published percentile-of-demand boundaries, extending defensible polygons to countries with viable O-D sources.

Each phase narrows the gap between what the polygon claims and what the data supports.

## Application

Trade-area membership is the basis for population aggregation (WorldPop 2026), spend aggregation (modelled per-capita multipliers), and cross-cluster competitive ranking. The numbers attributed to a cluster are only as defensible as the polygon they are summed over — which is why the polygon's definition, parameters, and projection treatment are stated here rather than implied by a circle on a map.

## See also

- [[co-location-tiering-scoring]] — how clusters are assigned composition tiers and the planned strength score
- [[spend-population-provenance]] — the estimation chain for population and spend within the trade area
- [[regional-market-definition]] — the settlement-level rollup built over co-location clusters
- [[app-orchestration-gis]] — the orchestration layer that runs the spatial analysis pipeline
- [[service-business-clustering]] — upstream retail clustering feeding the co-location index
