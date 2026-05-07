---
schema: foundry-doc-v1
title: "service-places"
slug: service-places-filtering
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

`service-places` is the service responsible for validating and clustering civic and institutional infrastructure. Its primary role is to filter raw civic data to retain only regional-grade facilities — hospitals, universities, and major transport hubs — ensuring that GIS tier rankings reflect institutional-level concentration rather than local-service density.

## Filtering Thresholds

The service applies attribute-weight filters to the raw civic data provided by `service-fs`:

- **Regional hospitals:** minimum capacity threshold (50+ staffed beds).
- **Regional universities:** minimum enrollment threshold (1,000+ full-time equivalent students).
- **Airports:** validated as major regional transport hubs; general aviation facilities are excluded.

## Spatial Aggregation

Large institutional campuses frequently appear in raw open geospatial data as multiple separate points. `service-places` applies a 200 m spatial buffer to cluster these into a single regional anchor with a unified center of gravity, preventing over-counting of large campus footprints.

## Data Output

The resulting `cleansed-places.jsonl` provides the regional anchor dataset that `app-orchestration-gis` uses when awarding final co-location tier rankings.

## See Also

- [[service-fs-data-lake]]
- [[service-business-clustering]]
- [[app-orchestration-gis]]
