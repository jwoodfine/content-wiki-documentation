---
schema: foundry-doc-v1
title: "How to build a co-location map"
slug: build-a-colocation-map
category: how-to
content_type: how-to
type: how-to
status: stub
last_edited: 2026-06-14
editor: pointsav-engineering
paired_with: build-a-colocation-map.es.md
---

The PointSav GIS engine exposes a tile API and a clusters endpoint that you can integrate into any MapLibre GL application. This guide covers authenticating against the GIS API, fetching the cluster GeoJSON layer, and rendering tier-coloured cluster markers on a MapLibre map canvas.

For the GIS engine architecture, see [[pointsav-gis-engine]]. For the co-location scoring system that produces the cluster data, see [[topic-co-location-ranking-system|co-location ranking system]].

## See also

- [[pointsav-gis-engine]] — GIS engine architecture and available API surfaces
- [[topic-co-location-methodology|co-location methodology]] — how cluster tiers are scored
- [[topic-od-catchment-methodology|O-D catchment methodology]] — how trade areas are defined
- [[federate-archives-via-content-mounts]] — mount location-intelligence data into a second instance
