---
schema: foundry-doc-v1
title: "Places filtering service"
slug: service-places-filtering
category: services
type: topic
content_type: topic
quality: complete
status: active
audience: public
short_description: "service-places filters raw civic and institutional infrastructure data to retain only regional-grade facilities — hospitals, universities, and major transport hubs — so GIS tier rankings reflect institutional-level concentration rather than local-service density."
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-08
editor: pointsav-engineering
paired_with: service-places-filtering.es.md
cites: []
---

[[co-location-methodology|GIS tier rankings]] depend on knowing where regional institutions sit, not where every clinic and community college sits. **`service-places`** filters raw civic data to retain only regional-grade facilities — hospitals with at least 50 staffed beds, universities with at least 1,000 full-time-equivalent students, validated major regional transport hubs — and applies a 200 m spatial buffer to consolidate large institutional campuses into single regional anchors. Local-service density is filtered out at this stage; downstream rankings reflect institutional concentration rather than facility count.

## Key Takeaways

- Regional-grade thresholds are hard-coded into the service: hospitals require ≥50 staffed beds, universities require ≥1,000 full-time-equivalent students, and general aviation facilities are excluded from airport scoring. These filters are structural, not configurable parameters.
- A 200 m spatial buffer consolidates multi-point campus records — a large hospital campus often appears as dozens of OSM nodes — into a single regional anchor with a unified centroid. This prevents tier over-counting on large institutional footprints.
- Output is `cleansed-places.jsonl`, consumed by `[[app-orchestration-gis]]` alongside the retail cluster dataset from `[[service-business-clustering]]` when assigning final co-location tiers.
- The filtering stage is deliberately upstream of tier scoring. Once local-service density is removed here, all downstream scoring operates on a clean regional-institution signal.

## Filtering Thresholds

The service applies attribute-weight filters to the raw civic data provided by [[service-fs-data-lake|`service-fs`]]:

- **Regional hospitals:** minimum capacity threshold (50+ staffed beds).
- **Regional universities:** minimum enrollment threshold (1,000+ full-time equivalent students).
- **Airports:** validated as major regional transport hubs; general aviation facilities are excluded.

## Spatial Aggregation

Large institutional campuses frequently appear in raw open geospatial data as multiple separate points. `service-places` applies a 200 m spatial buffer to cluster these into a single regional anchor with a unified center of gravity, preventing over-counting of large campus footprints.

## Data Output

The resulting `cleansed-places.jsonl` provides the regional anchor dataset that [[app-orchestration-gis]] uses when awarding final [[co-location-methodology|co-location tier rankings]].

## See also

- [[service-fs-data-lake]] — GIS data lake supplying the raw civic and retail data
- [[service-business-clustering]] — retail clustering service that consumes the filtered place data
- [[app-orchestration-gis]] — orchestration layer that assembles tier rankings from both services
- [[co-location-methodology]] — the ranking methodology driving tier assignments

## References

- [Point of interest](https://en.wikipedia.org/wiki/Point_of_interest) — Wikipedia, accessed 2026-06-14
