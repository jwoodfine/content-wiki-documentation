---
schema: foundry-doc-v1
title: "Location intelligence platform"
slug: location-intelligence-platform
category: applications
type: topic
content_type: topic
quality: complete
index_group: location-intelligence-applications
short_description: "Customer-owned flat-file GIS application for retail cluster analysis and strategic site selection, pairing an analytics engine with a rendering layer."
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-08-01
editor: pointsav-engineering
paired_with: location-intelligence-platform.es.md
cites:
 - osm-odbl
 - overture-maps-cdla-2-0
 - ni-51-102
 - osc-sn-51-721
---

The PointSav Location Intelligence platform is a customer-owned flat-file GIS application designed for retail cluster analysis and strategic site selection — composed of [[app-orchestration-gis]] (the analytics engine) and [[location-intelligence-substrate]] (the rendering layer), with every dataset, algorithm, and rendering decision under the customer's direct control. The platform answers a fundamental commercial question — *which geographic nodes possess the capital-validated density required to support adjacent development?* — by transforming raw store locations into actionable commercial nodes through the [[retail-co-location-tier-methodology]]. All canonical datasets reside in a [[totebox-archive|Totebox Archive]] as flat JSONL and GeoParquet files, applying the [[worm-ledger-design|WORM ledger discipline]] to geospatial records.

## Operational Capabilities

The platform transforms raw store locations into actionable commercial nodes by executing the [[retail-co-location-tier-methodology|Retail Co-location Tier Methodology]]. It answers a fundamental commercial question: *which geographic nodes possess the capital-validated density required to support adjacent development?*

### 1. Five-Degree Cluster Identification
The platform computes co-location clusters around Primary Target anchors (e.g., Walmart Supercentres) using a deterministic spatial algorithm. Each cluster is scored based on the convergence of independent, capital-intensive operators (Costco, Home Depot, etc.) and supporting civic infrastructure (hospitals, universities).

### 2. Multi-Layer Interactive Interface
The interactive map at [gis.woodfinegroup.com](https://gis.woodfinegroup.com) uses a three-layer architecture:
- **Layer 1 — Global POIs:** Toggled view of 31,000+ individual retail locations, color-coded by brand family.
- **Layer 2 — Co-location Clusters:** The primary analytical view, encoding cluster strength through visual saturation and size.
- **Layer 3 — Catchment Radii:** Visualized proximity boundaries (default 3.0 km — Correction, 2026-08-02: the real value used by `build-radius.py` is `DEFAULT_CATCHMENT_KM = 150.0` (27.0 for dense urban corridors), roughly 50× the figure stated here; the 3.0 km figure appears to conflate an unrelated DBSCAN cluster-tightness parameter with the trade-area catchment radius. Flagged, not resolved.) that define the scope for trade-area analysis and mobility data procurement.

## Sovereign Architecture

The platform adheres to [[location-intelligence-substrate|the substrate's]] principles of [[customer-hostability|customer-rooted data sovereignty]]:
- **Flat-File Operation:** All data persists as versioned JSONL and GeoParquet files within a [[totebox-archive|Totebox Archive]], rather than a running database daemon.
- **Open Standards Rendering:** Uses PMTiles and MapLibre GL JS to serve vector maps directly from standard web servers, eliminating proprietary tile-API dependencies.
- **Reproducible Build:** If a gateway node is destroyed, the application surface can be re-provisioned instantly by pointing a fresh instance at the immutable data layer.

## Data Foundations and Licensing

The platform integrates high-fidelity open data sources to ensure transparency and auditability:
- **Retail Data:** Sourced from OpenStreetMap contributors and the Overture Maps Foundation.
- **Civic Infrastructure:** Healthcare and institutional records from the Overture Maps Foundation Places dataset.
- **Sovereign Basemap:** OpenFreeMap liberty tiles served via the PointSav infrastructure.

*Material assumptions for current platform performance include the continued availability of high-fidelity open geographic datasets. [osm-odbl] [overture-maps-cdla-2-0]*

## Future Roadmap

Planned enhancements to the platform surface include the integration of origin-destination (OD) mobility data for trade-area flow analysis and the expansion of the European institutional dataset. [ni-51-102] [osc-sn-51-721]

## See also

- [[app-orchestration-gis]] — the stateless analytics engine that produces co-location rankings
- [[location-intelligence-substrate]] — the rendering layer that serves vector tiles to the map interface
- [[retail-co-location-tier-methodology]] — the tier methodology underlying cluster analysis
- [[location-intelligence-ux]] — the UX design philosophy for the interactive map surface
- [[totebox-archive]] — the flat-file archive that holds all canonical geospatial data
