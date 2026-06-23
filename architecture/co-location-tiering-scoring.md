---
schema: foundry-doc-v1
title: "Co-location tiering and scoring"
slug: co-location-tiering-scoring
category: architecture
type: concept
content_type: topic
quality: complete
status: stable
bcsc_class: public-disclosure-safe
language: en
last_edited: 2026-06-23
editor: pointsav-engineering
paired_with: co-location-tiering-scoring.es.md
cites: []
---

The Woodfine location intelligence map assigns each co-location cluster one of three tiers — T1, T2, or T3 — on the basis of retailer-category composition. The tiers are rendered as coloured dots graduated from T1 (deepest co-location) to T3 (shallowest qualifying co-location). Understanding precisely what the tiers measure — and what they do not — is necessary for reading any cluster result correctly.

## What the tiers measure

The variable that drives the tier is **retailer-category composition**: the count and mix of distinct anchor categories co-present within a single spatial cluster. A cluster that contains a hypermarket, a home-improvement big-box, and a warehouse-club anchor has deeper composition than a cluster with a single hypermarket and one grocer. The tier is therefore an ordinal compositional classification.

The tiers measure composition. They do not measure trade-area strength, sales potential, population reached, or spend captured. Two consequences follow directly:

**Composition does not imply demand.** A T1 cluster has more anchor diversity than a T3 cluster. It does not follow that a T1 cluster has more people, more spend, or better accessibility in its trade area. A dense small-city cluster of three anchors can rank T1 on composition while serving a smaller catchment than a single-anchor T3 site in a major metropolitan area. The tier ranks the bundle of retailers present, not the market the bundle sits in.

**Quality claims require an outcome variable.** A label asserting quality implies evaluation against an outcome — footfall, revenue, return on a hypothetical investment. The compositional tier carries no such outcome. The on-map labelling therefore reads "co-location depth (anchor count)" rather than "quality tiers," and the plain-language definition of each tier is tied to composition:

- **T1** — strongest co-location depth (most anchor categories co-present)
- **T2** — intermediate co-location depth
- **T3** — shallowest qualifying co-location

## How clusters are formed: DBSCAN parameters

The clusters that receive tiers are produced by spatial clustering of anchor retailer locations using **DBSCAN** (density-based spatial clustering), followed by a de-duplication pass. DBSCAN is governed by three parameters that are published in the Method modal and stated here:

- **eps** — the neighbourhood radius that defines whether two anchor points are density-reachable; sets the spatial scale at which separate stores read as one cluster.
- **minPts** — the minimum number of points required to seed a cluster; sets the floor on what counts as a co-location rather than an isolated store.
- **IoU threshold** — the intersection-over-union cut-off used to de-duplicate overlapping candidate clusters, so the same physical agglomeration is not counted twice.

A hard **3.0 km cap** on cluster span (maximum pairwise diameter) applies uniformly. Widening to 4 km is not used because it merges distinct agglomerations. A span at or under 1.0 km carries a `tight_intact` quality flag.

The values for eps, minPts, and the IoU threshold are read from the current `build-geometric-ranking.py` pipeline at each build and stated in the Method modal alongside the build version from which they are taken.

### Sensitivity: the cluster count is a model output, not a measurement

DBSCAN is a **descriptive** procedure. It partitions the observed retailer points under a chosen density model; it does not estimate a true, parameter-independent number of clusters that exists in the world. The number of clusters the algorithm returns is a function of eps, minPts, and the IoU threshold, and it moves materially when those are varied within reasonable bounds.

Parameter sweeps conducted during development demonstrate this directly: across the reasonable range tested, the **North American cluster count moves from roughly 226 to 476** depending on settings — more than a factor of two — without any change to the underlying retailer data. A headline cluster count is therefore a model output under one chosen parameterisation, not a precise count of an objective phenomenon. Any public presentation of cluster counts must be accompanied by the parameters under which the count was produced.

## The planned strength score

The composition tier answers "what retailer mix is here." A separate per-cluster **strength score** — planned, not yet built — is intended to answer "how much market does this location command." The two dimensions are reported side by side once the scorecard is wired; they are never collapsed into a single colour or a single number.

### Design principles

The intended strength score is explainable, not opaque. It is a transparent combination of named drivers, each of which can be shown in the cluster scorecard with its own value and its contribution to the total. No machine-learned weights and no hidden interaction terms. A reviewer must be able to reconstruct the score from the displayed drivers.

### Proposed driver set

Three demand-side quantities the data layers already support:

1. **Population reached** — catchment population and households, from the WorldPop 2026 dasymetric raster aggregated to H3 resolution 7. This is the size of the addressable market.
2. **Spend captured** — estimated annual retail spend in the catchment, derived from population and per-capita spend proxies (BLS, StatCan, Eurostat). This carries the estimation caveats documented in the [[spend-population-provenance]] article and must be displayed with that framing.
3. **Accessibility** — how reachable the catchment is, expressed through observed origin-destination demand where available (LODES for the US, MITMA for Spain) and a distance-band fallback elsewhere. This inherits the `demand_basis` flag (observed versus interim) so that observed-mobility and ambient-fallback clusters are not ranked in the same pool without disclosure.

### Weights: an open question

How these three drivers combine into a single number is an open question that this article deliberately does not resolve. Three candidate forms are on the table: an equal-weight normalised sum, a lexicographic ranking, and operator-tunable weights. Until the weighting is ratified, the scorecard displays driver values individually so any composite shown is always decomposable. A composite score with undisclosed weights would reintroduce exactly the credibility problem that the tier-label revision exists to remove.

### What the scorecard is intended to show

For each clicked cluster the planned detail panel presents, at minimum:

- Composition tier and its plain-language definition.
- Catchment population and households, with vintage and the dasymetric basis noted.
- Estimated annual spend, explicitly framed as a modelled estimate.
- The list of co-located chains driving the composition.
- The strength score (when built) with its top drivers and each driver's contribution, and the `demand_basis` flag.

## What changes from the earlier presentation

| Dimension | Earlier | Current |
|---|---|---|
| Tier label | "QUALITY TIERS" | "Co-location depth (anchor count)" — composition only |
| What a tier measures | Ambiguous | Explicitly composition (anchor-category count and mix), ordinal |
| Decision support | Tier badge and rings only | Planned scorecard: population, spend, co-located chains, explainable strength score with named drivers |
| Strength score | Conflated into the tier | Planned as separate, demand-side, decomposable dimension |
| DBSCAN parameters | Not published | eps, minPts, IoU, and 3.0 km span cap published in Method modal and here |
| Cluster count | Stated as a precise figure | Model output under one parameterisation; NA sweep range disclosed |

## See also

- [[trade-area-methodology]] — catchment derivation, geodesic computation, and the migration from distance bands toward observed trade areas
- [[spend-population-provenance]] — the estimation chain for the spend driver in the strength score
- [[regional-market-definition]] — the settlement-level rollup and the Top-400 selection criterion
- [[app-orchestration-gis]] — the orchestration layer that produces the tiered clusters
- [[service-business-clustering]] — upstream retail clustering feeding the co-location index
