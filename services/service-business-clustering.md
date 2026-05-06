---
schema: foundry-doc-v1
title: "service-business"
slug: service-business-clustering
category: services
type: topic
quality: complete
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-06
editor: pointsav-engineering
cites: []
---

`service-business` is the intelligence layer responsible for transforming raw retail data points into actionable commercial clusters. It implements a parent-child clustering pattern to handle complex physical retail environments where multiple distinct operators share a single commercial node.

## The Clustering Logic

Retail data is inherently messy. A single commercial node often contains multiple distinct points — for example, a big-box anchor store, a nested pharmacy, and a fuel outlet in the same parking area. `service-business` processes these points so that the GIS engine produces a single, unified commercial entity per physical site.

### Grid-Based Spatial Indexing

To perform this at scale, the service uses a grid-based spatial index (approximately 1 km cells). It iterates through the `service-fs` raw data lake and groups entities that share a physical footprint within a 100 m proximity threshold.

### Parent-Child Schema

- **Parent node:** The primary commercial driver — typically the highest-weight named anchor at the site.
- **Children (sub-entities):** Secondary operators located within the same spatial node.

## Cleansed Data Output

The output is a refined `cleansed-clusters.jsonl` file. This processed dataset is consumed by the downstream `app-orchestration-gis` to build the regional co-location index.

## See Also

- [[app-orchestration-gis]]
- [[service-fs-data-lake]]
- [[service-places-filtering]]

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*

*Woodfine Capital Projects™, Woodfine Management Corp™, PointSav Digital Systems™, Totebox Orchestration™, and Totebox Archive™ are trademarks of Woodfine Capital Projects Inc., used in Canada, the United States, Latin America, and Europe. All other trademarks are the property of their respective owners.*
