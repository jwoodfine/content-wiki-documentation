---
schema: foundry-doc-v1
title: "Places filtering"
slug: service-places-filtering
category: services
type: topic
content_type: topic
quality: complete
index_group: specialist-and-domain-services
status: active
audience: public
short_description: "A filtering step that keeps only regional-grade institutions from raw civic data, so GIS tier rankings reflect institutional concentration rather than every clinic and community facility."
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-09-05
editor: pointsav-engineering
paired_with: service-places-filtering.es.md
cites: []
references:
  - id: 1
    text: "Point of interest. Wikipedia, accessed 2026-06-14."
    url: "https://en.wikipedia.org/wiki/Point_of_interest"
---

[[retail-co-location-tier-methodology|GIS tier rankings]] depend on knowing where regional
institutions sit, not where every local clinic or community facility sits. The platform's
places-filtering step keeps only civic and institutional facilities that meet a regional
scale — hospitals, universities, and validated major transport hubs above fixed size
thresholds — and consolidates multi-point campus records into a single regional anchor.
Local-service density is removed at this stage, so downstream rankings reflect institutional
concentration rather than raw facility count.[^1]

## What the filter keeps

The filter applies fixed, structural thresholds rather than configurable parameters: a
hospital must reach a minimum staffed-bed count, a university a minimum full-time-equivalent
enrollment, and an airport must be a validated major regional hub rather than a general
aviation facility. Institutions below these thresholds are dropped before any downstream
scoring runs.

## Consolidating campus records

A large institutional campus often appears in raw open geospatial data as many separate
points. The filter merges points that plausibly belong to the same physical campus into a
single regional anchor with one unified centroid, preventing a single large institution from
being counted many times over.

## Where this fits in the pipeline

Filtering runs as part of the same Python-based GIS pipeline documented in
[[app-orchestration-gis]] — the code that turns raw geographic and business data into the
regional co-location index — rather than as a separately deployed service. Its output feeds
[[app-orchestration-gis]] alongside the retail clustering step from
[[service-business-clustering]] when the pipeline assigns final co-location tiers. This
article does not restate the pipeline's specific thresholds, buffer distances, or internal
file names; the general pattern (drop sub-regional facilities, consolidate multi-point
campuses to a single anchor) is the stable, public-facing part of the design.

## See also

- [[app-orchestration-gis]] — the pipeline this filtering step is part of
- [[service-business-clustering]] — the retail clustering step that runs alongside it
- [[service-fs-data-lake]] — the raw civic and retail data this step consumes
- [[retail-co-location-tier-methodology]] — the tier methodology the filtered data feeds
