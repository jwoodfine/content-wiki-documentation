---
schema: foundry-doc-v1
title: "Location intelligence platform"
slug: location-intelligence-platform
category: applications
type: topic
content_type: topic
quality: complete
index_group: location-intelligence-applications
short_description: "Customer-owned flat-file GIS application for retail cluster analysis and strategic site selection, pairing a nightly scoring pipeline with an interactive rendering layer."
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-08-22
editor: pointsav-engineering
paired_with: location-intelligence-platform.es.md
cites:
 - osm-odbl
 - overture-maps-cdla-2-0
---

The PointSav Location Intelligence platform is a customer-owned flat-file GIS application for retail cluster analysis and strategic site selection — a nightly [[app-orchestration-gis|pipeline]] that scores and tiers commercial nodes, paired with [[location-intelligence-substrate|a rendering layer]] that serves the result as an interactive map, with every dataset, algorithm, and rendering decision under the customer's direct control. The platform answers a fundamental commercial question — *which geographic nodes possess the capital-validated density required to support adjacent development?* — by transforming raw store locations into actionable commercial nodes through the [[retail-co-location-tier-methodology]]. All canonical datasets reside in a [[totebox-archive|Totebox Archive]] as flat JSONL and GeoParquet files.

## Operational capabilities

The platform transforms raw store locations into actionable commercial nodes by executing the [[retail-co-location-tier-methodology|Retail Co-location Tier Methodology]]. It answers a fundamental commercial question: *which geographic nodes possess the capital-validated density required to support adjacent development?*

### Cluster identification

The pipeline groups nearby capital-intensive operators (Walmart, Costco, Home Depot, and
similar anchors) and supporting civic infrastructure (hospitals, universities) into clusters
using a spatial clustering algorithm, then scores each cluster and assigns it one of four
tiers per the tier methodology.

### Interactive map interface

The interactive map at [gis.woodfinegroup.com](https://gis.woodfinegroup.com) renders tier
conclusions rather than individual data points, per the platform's
[[location-intelligence-ux|Conclusion-First design philosophy]]. Analytical layers —
Clusters, Catchment, and OD Study — are presented as primary navigation toggles inside a
drawer component, with the four-tier Regional/District/Local/Fringe color scheme surfacing
the strongest nodes at a national zoom level before a user drills into individual sites.
Trade-area catchment radii default to approximately 150 km for standard regional analysis,
narrowing to roughly 27 km in dense urban corridors.

## Data sovereignty

The platform's data model is deliberately flat-file rather than a running database daemon:
- **Flat-file operation:** All data persists as versioned JSONL and GeoParquet files within a [[totebox-archive|Totebox Archive]].
- **Open standards rendering:** Uses PMTiles and MapLibre GL JS to serve vector maps directly from standard web servers, eliminating proprietary tile-API dependencies.
- **Reproducible build:** The application surface can be re-provisioned by pointing a fresh instance at the immutable data layer and re-running the nightly pipeline.

## Data foundations and licensing

The platform integrates open data sources for transparency and auditability:
- **Retail data:** Sourced from OpenStreetMap contributors and the Overture Maps Foundation.
- **Civic infrastructure:** Healthcare and institutional records from the Overture Maps Foundation Places dataset.
- **Basemap:** Vector tiles served via the platform's own infrastructure, not a third-party tile API.

Coverage already spans both North American and European markets — origin-destination mobility
data for trade-area flow analysis is live today, not a future addition (the "OD Study" layer
described above). *Material assumptions for current platform performance include the continued
availability of high-fidelity open geographic datasets. [osm-odbl] [overture-maps-cdla-2-0]*

## See also

- [[app-orchestration-gis]] — the pipeline that produces co-location rankings
- [[location-intelligence-substrate]] — the rendering layer that serves vector tiles to the map interface
- [[retail-co-location-tier-methodology]] — the tier methodology underlying cluster analysis
- [[location-intelligence-ux]] — the UX design philosophy for the interactive map surface
- [[totebox-archive]] — the flat-file archive that holds all canonical geospatial data
