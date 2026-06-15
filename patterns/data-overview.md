---
schema: foundry-doc-v1
title: "Data Overview — Location Intelligence and GIS Data Layers"
slug: data-overview
category: patterns
type: concept
content_type: topic
quality: stub
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-06-15
editor: pointsav-engineering
paired_with: data-overview.es.md
short_description: "An orientation to the platform's data layers: location intelligence clusters, co-location tiers, and the GIS tile pipeline."
cites: []
---

The PointSav platform produces and serves geospatial data in two primary forms: a location intelligence cluster dataset covering commercial co-location patterns across multiple countries, and a point-of-interest taxonomy that underlies the cluster algorithm. This article orients readers to those layers and links to the substantive methodology and archetype articles.

## Location intelligence clusters

The cluster dataset groups commercial points of interest into three-tier co-location nodes — T1 (anchor), T2 (developed), T3 (emerging) — using a two-pass DBSCAN algorithm. Three archetypes describe distinct commercial patterns: PRO (professional retail co-location), VWH (vertical warehouse / urban industrial), and PKS (parking structures / transit-adjacent commercial).

See [[topic-location-intelligence-archetypes|Location Intelligence Co-location Archetypes]] for a full introduction.

## GIS tile pipeline

Cluster data is compiled into PMTiles and served at `gis.woodfinegroup.com`. The pipeline runs nightly, producing updated archetype GeoJSON files and spatial tile layers. See the [[guide-catalog|Developer Guide Catalog]] for the nightly rebuild and AEC hazard pipeline guides.

## Methodology articles

- [[od-catchment-methodology|O-D Catchment Methodology]] — crow-flies origin-destination model and catchment ring rationale
- [[catchment-ranking-methodology|Catchment Ranking Methodology]] — combined primary and secondary rank dimensions
- [[colocation-tier-nomenclature|Co-location Tier Nomenclature]] — T1/T2/T3 vocabulary

*This article is a stub. Full content is planned for a future session.*
