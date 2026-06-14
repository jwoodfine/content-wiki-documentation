---
schema: foundry-doc-v1
title: "Business clustering service"
slug: service-business-clustering
category: services
type: topic
content_type: topic
quality: complete
status: active
audience: public
short_description: "service-business turns raw retail data points into actionable commercial clusters by applying a parent-child spatial schema — so when multiple distinct operators share a single physical site, the GIS engine receives one commercial entity per site rather than several overlapping points."
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-25
editor: pointsav-engineering
paired_with: service-business-clustering.es.md
cites: []
---

Retail data is inherently messy — a single commercial site often contains multiple distinct points, such as a big-box anchor, a nested pharmacy, and a fuel outlet sharing the same parking area. **`service-business`** turns those raw points into actionable commercial clusters using a parent-child spatial schema, so the GIS engine receives one unified commercial entity per physical site rather than several overlapping records. The service iterates the `service-fs` raw data lake, groups entities that share a footprint within a 100 m proximity threshold, and assigns the highest-weight named anchor as the parent.

## The Clustering Logic

`service-business` processes raw commercial nodes so that the GIS engine produces a single, unified commercial entity per physical site.

### Grid-Based Spatial Indexing

To perform this at scale, the service uses a grid-based spatial index (approximately 1 km cells). It iterates through the `service-fs` raw data lake and groups entities that share a physical footprint within a 100 m proximity threshold.

### Parent-Child Schema

- **Parent node:** The primary commercial driver — typically the highest-weight named anchor at the site.
- **Children (sub-entities):** Secondary operators located within the same spatial node.

## Cleansed Data Output

The output is a refined `cleansed-clusters.jsonl` file. This processed dataset is consumed by the downstream `app-orchestration-gis` to build the regional co-location index.

## See also

- [[app-orchestration-gis]]
- [[service-fs-data-lake]]
- [[service-places-filtering]]
