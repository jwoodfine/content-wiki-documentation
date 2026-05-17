---
schema: foundry-doc-v1
title: "PointSav GIS engine"
slug: pointsav-gis-engine
category: services
type: topic
quality: complete
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-08
editor: pointsav-engineering
short_description: "The PointSav GIS Engine is a high-performance, customer-owned location intelligence platform built in Rust for offline-first, flat-file operation — a structural departure from traditional geographic information systems that rely on centralised database instances and continuous network connectivity."
paired_with: pointsav-gis-engine.es.md
cites:
 - maplibre-gl-js
 - pmtiles-spec
 - tippecanoe-tool
---

The PointSav GIS Engine is a high-performance, customer-owned location intelligence platform built in Rust for offline-first, flat-file operation — a structural departure from traditional geographic information systems that rely on centralised database instances and continuous network connectivity. The engine reads from a static PMTiles archive on the customer's own filesystem, renders interactively through MapLibre GL JS in the browser, and serves every query without an external dependency. The map data lives in the customer's archive; nothing leaves the deployment unless the operator explicitly chooses to publish.

## Architectural Principles

The engine is engineered to operate as a stateless application surface, adhering to the PointSav principle of complete data sovereignty.

### Flat-File Substrate
Unlike traditional GIS stacks (e.g., PostGIS, Esri) which require persistent database management, the PointSav engine utilizes a flat-file substrate. It consumes geographic data directly from `JSONL`, `GeoParquet`, and `YAML` formats versioned within a Totebox Archive. This architecture ensures the data layer remains entirely decoupled from the application logic, eliminating database maintenance overhead and preventing vendor lock-in.

### Sovereign Rendering Stack
The platform avoids commercial SaaS mapping dependencies by utilizing a high-performance, open-source rendering stack:

- **PMTiles:** A single-file archive format for tiled data that enables maps to be served directly from standard web servers (Nginx) or blob storage without a dedicated tile server. [pmtiles-spec]
- **MapLibre GL JS:** A WebGL-based library for rendering interactive vector maps with high client-side performance. [maplibre-gl-js]
- **Tippecanoe:** A tool used to compile massive flat-file datasets into optimized vector tiles, ensuring rapid delivery of complex co-location clusters. [tippecanoe-tool]

## Spatial Processing and Orchestration

The engine's core logic resides in the `app-orchestration-gis` service. This component executes the Woodfine co-location methodology deterministically:

1. **Ingestion:** Reads retail and civic infrastructure records from the Totebox Archive.
2. **Analysis:** Executes spatial joins and proximity queries to identify co-location clusters across 1.0 km, 3.0 km, and 5.0 km radii.
3. **Ranking:** Applies the 12-rank named-anchor matrix to generate site quality tiers.
4. **Serialization:** Outputs the processed results as tiled data for the visual interface at [gis.woodfinegroup.com](https://gis.woodfinegroup.com).

This stateless approach ensures that the entire GIS environment can be re-provisioned instantly from the immutable data layer, providing maximum service resilience and auditability.

## See also
* Guide: Totebox Orchestration for GIS (operational runbook; available in fleet deployment documentation)
* [[co-location-methodology]]
