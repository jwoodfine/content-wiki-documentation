---
schema: foundry-doc-v1
title: "Business clustering"
slug: service-business-clustering
category: services
type: topic
content_type: topic
quality: complete
index_group: specialist-and-domain-services
status: active
audience: public
short_description: "A parent-child spatial pattern that turns raw retail points into one commercial entity per physical site, so the GIS pipeline reasons about a location once instead of once per co-located tenant."
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-08-22
editor: pointsav-engineering
paired_with: service-business-clustering.es.md
cites: []
---

Retail data is inherently messy — a single commercial site often contains multiple distinct points, such as a big-box anchor, a nested pharmacy, and a fuel outlet sharing the same parking area. The platform's business-clustering step turns those raw points into commercial clusters using a parent-child pattern, so downstream GIS analysis reasons about one unified commercial entity per physical site rather than several overlapping records.

## The parent-child pattern

Points that plausibly belong to the same physical site are merged in a small number of proximity-based passes, using different distance thresholds depending on whether the points share an identifying signal (the same retail chain, for example) or only a brand-level match. The highest-weight named point at a merged site becomes the parent record; the rest become children. Without this step, several co-located tenants at one site would each count as an independent signal in downstream scoring, overstating that location's commercial weight.

## Where this fits in the pipeline

Clustering runs as part of the same Python-based GIS pipeline documented in [[app-orchestration-gis]] — the code that turns raw geographic and business data into the regional co-location index — rather than as a separately deployed service. This article does not restate the pipeline's specific distance thresholds or internal script names; the general pattern (merge co-located points, promote the strongest anchor to parent) is the stable, public-facing part of the design.

## See also

- [[app-orchestration-gis]] — the pipeline this clustering step is part of
- [[service-fs-data-lake]] — the raw data this step consumes
