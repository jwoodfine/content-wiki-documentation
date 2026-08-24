---
schema: foundry-doc-v1
title: "Retail co-location tier methodology"
slug: retail-co-location-tier-methodology
category: substrate
type: concept
content_type: topic
quality: complete
index_group: core-named-substrates
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-08-24
editor: pointsav-engineering
paired_with: retail-co-location-tier-methodology.es.md
cites:
 - ni-51-102
 - np-51-201
---

A retail co-location cluster earns a tier by passing a fixed set of gates, not by
accumulating points toward a score. The [[location-intelligence-platform|Location
Intelligence]] platform assigns every cluster one of four tiers — Regional, District,
Local, or Fringe — by testing composition, catchment population rank, civic support, and
overlap with stronger neighbors against country-specific thresholds. A cluster either
clears every gate for a tier or it does not; there is no partial credit and no composite
number a customer would need to interpret.

## Why gates instead of a score

An earlier version of this methodology combined proximity distances into a single
continuous score. That approach was retired: a composite number invites the reading that
the platform is forecasting financial outcomes, when what it actually measures is spatial
proximity and brand diversity. The gate-based system makes that boundary explicit in the
mechanism itself — the tier is a classification, not a projection of revenue, foot
traffic, market share, or a recommendation to acquire, develop, or lease any site.

## Tier definitions

| Tier | Name | What it represents |
|---|---|---|
| 1 | Regional | A major trade-area anchor — top decile nationally by primary catchment population |
| 2 | District | A significant multi-format node — top quartile nationally by primary catchment |
| 3 | Local | A hardware or wholesale hub with civic support |
| 4 | Fringe | Any cluster that does not clear a Tier 1–3 gate |

Tier names follow the shopping-center industry's own Regional → District → Local
hierarchy, so the labels mean the same thing here that they mean in a leasing broker's
vocabulary.

## What a cluster must clear

Every tier requires all of its gates to pass — composition, catchment rank, spend rank
where it applies, civic support, and non-overlap:

- **Composition** — which categories of capital-intensive anchor must co-occur. Regional
  requires a warehouse-club or lifestyle anchor alongside a hypermarket; District requires
  a hypermarket alongside hardware or warehouse; Local requires a hardware or warehouse
  anchor on its own.
- **Catchment population rank** — each cluster's catchment population is ranked
  against every other cluster *within its own country*, not globally, so a Tier 1 cluster
  in a smaller market is compared to its own market's distribution rather than penalized
  for that market's overall size. Regional requires the top 10% nationally on primary
  catchment (plus a secondary-catchment population check); District the top 25% on primary
  catchment; Local the top 50%.
- **Spend rank** — District additionally requires the cluster to rank in the top quartile
  nationally on at least one of several consumer-spend measures, not population alone.
- **Civic support** — a minimum count of regionally or locally classified hospitals within
  the cluster's outer catchment ring. Regional requires a regional-grade hospital; District
  accepts a regional or district hospital; Local accepts any classified hospital.
- **Non-overlap** — a cluster that sits mostly inside a stronger neighboring cluster's own
  catchment does not additionally qualify at a lower tier for the same geography. This is
  measured as the overlap between the two clusters' catchment areas; Regional clusters must
  be almost entirely non-overlapping with any stronger peer, District clusters allow more
  overlap.

Threshold precision is intentionally coarse — the goal is separating nationally
significant clusters from local ones, not producing a precise numeric ranking. Threshold
refinement is an active area of ongoing work.

## What is deliberately excluded

Neighborhood grocery formats (operating in the thousands of small-footprint locations per
country) are not ingested as anchors. Their density would produce a large number of
low-value clusters below any threshold useful for site selection — a deliberate scope
decision, not a data-coverage gap.

## Relationship to the platform

The tier assignment is what the [[location-intelligence-platform|map interface]] renders
directly — the [[location-intelligence-ux|Conclusion-First design]] shows a cluster's tier,
not the gate values behind it, so a user comparing markets sees the conclusion first and
drills into the underlying anchors only when a cluster has earned that attention.
[[app-orchestration-gis]] computes tier assignment from the cleansed cluster data; the
result renders through [[location-intelligence-substrate|the platform's rendering
stack]] as the tiered map layer.

## Forward-looking information

Statements regarding threshold refinement and future methodology changes are intended
targets subject to change. Actual timelines depend on operator review, data coverage, and
development velocity. [ni-51-102] [np-51-201]

## See also

- [[location-intelligence-platform]] — the platform this methodology scores clusters for
- [[app-orchestration-gis]] — the engine that computes tier assignment
- [[location-intelligence-substrate]] — the technical architecture that stores and renders tiered clusters
- [[location-intelligence-ux]] — the interface design that displays tier conclusions
