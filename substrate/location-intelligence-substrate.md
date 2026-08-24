---
schema: foundry-doc-v1
title: "Location intelligence substrate"
slug: location-intelligence-substrate
short_description: "A flat-file, open-GIS architecture letting customers own geographic datasets end-to-end using open data and a Rust-aligned rendering stack, retail co-location as first surface."
category: substrate
type: topic
content_type: topic
quality: complete
index_group: core-named-substrates
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-08-24
editor: pointsav-engineering
paired_with: location-intelligence-substrate.es.md
aliases:
  - pointsav-gis-engine
references:
  - id: 1
    text: "Overture Maps Foundation — GeoParquet places schema. overturemaps.org"
  - id: 2
    text: "Foursquare Open Source Places — 100M+ POIs, Apache 2.0. huggingface.co/datasets/foursquare"
  - id: 3
    text: "GeoParquet specification — OGC incubating standard. geoparquet.org"
  - id: 4
    text: "FlatGeobuf — Hilbert R-tree packed flat-file format. flatgeobuf.org"
  - id: 5
    text: "MapLibre GL JS — Community-driven vector-tile renderer. maplibre.org"
  - id: 6
    text: "Martin tile server — Rust tile server (MapLibre Foundation). maplibre.org/martin"
  - id: 7
    text: "PMTiles — Single-file tile archive with HTTP range requests. protomaps.com/pmtiles"
  - id: 8
    text: "NI 51-102 Continuous Disclosure Obligations — BCSC"
  - id: 9
    text: "CSA National Policy 51-201 Forward-Looking Information Disclosure"
---

A platform that depends on a running database and a live network connection is a platform a customer rents, not owns — outages, per-seat cost, and air-gap ineligibility follow. The Location Intelligence Substrate avoids that dependency by construction: it is a flat-file, open-GIS architecture that lets [[customer-hostability|customers own their geographic datasets end-to-end]] — no tile API billing, no warehouse licensing, no cloud-vendor lock-in. The substrate is built on Apache-licensed open-data foundations (Overture Maps Foundation, Foursquare Open Source Places) and rendered via a Rust-aligned open-source stack (MapLibre GL JS, Martin tile server, PMTiles).[^1][^2]

The first deployed surface is `gis.woodfinegroup.com` — a co-location map showing retail anchor co-presence across the United States, Canada, Mexico, and Spain.

## Architecture — flat-file vs database

Three options exist for canonical storage of geographic records:

**Flat-file canonical** — JSONL for human-diffable change tracking; GeoParquet for performant analytic reads; FlatGeobuf for browser-side spatial-bbox streaming. GeoParquet is an OGC incubating standard that adds Point/Line/Polygon types to columnar Parquet.[^3] FlatGeobuf carries a packed Hilbert R-tree at the file header that enables a browser to stream only the features inside the current viewport over HTTP range requests.[^4] Advantages: sovereign by construction, version-controllable, customer-portable, zero infrastructure to operate. Limitation: writes are single-author-at-a-time; concurrent online edits would race.

**Database canonical** — PostgreSQL plus a spatial extension, the genre's industry default. Advantages: rich spatial SQL, multi-writer concurrency, production-tested operations. Limitation: the customer's data lives in a running daemon they must operate; portability requires a dump-and-restore that is not a directory move.

**Hybrid** — flat-file canonical, ephemeral database materialised from the flat-file as a query cache. Matches the vault-as-canonical, derived-tables-as-cache approach the platform uses for bookkeeping.

For workloads of tens of thousands of POI records across a small number of countries, with infrequent batch writes and read-mostly queries, flat-file is sufficient and is the architecture both Foursquare and Overture Maps Foundation chose for their substrate releases.[^1][^2] The recommendation: GeoParquet as the canonical at-rest format (one file per country per service, rolled monthly), JSONL siblings for git-tracked human-diffable history, FlatGeobuf as the browser-streamable derivative.

## Map tile and layer delivery

The rendering stack uses MapLibre GL JS in the browser — a community-driven open-source vector-tile renderer that supports WebGL, dynamic styling, smooth animation, and 3D without per-traffic licence cost.[^5]

Tile generation uses Tippecanoe (Felt's actively-maintained fork) for converting GeoJSON to MBTiles or PMTiles, reducing file size by 85–95% over raw GeoJSON at POI dataset scale. Tile serving uses Martin, the MapLibre Foundation's Rust tile server, supporting PostGIS, MBTiles, and PMTiles.[^6]

The tile archive format is PMTiles — a single-file archive with HTTP range-request support, enabling tile serving directly from nginx without running Martin when the tiles are pre-baked.[^7] Martin is used when dynamic tile generation is needed (viewport-filtered density layers that respond to real-time filter state).

For data-visualisation overlays (scatter, heatmap, arc, polygon-extrusion layers), deck.gl composes naturally with MapLibre.

## Data shape — business and places records

The ingest pipeline organizes records into two data categories, business and places, each with a discriminator field, a brand slug and brand-family normalisation (so regional equivalents of the same chain count as one logical operator across countries), a point geometry, and a source-provenance field recording which open dataset each record came from. Places records carry an additional type field for non-retail anchors such as hospitals, higher-education campuses, and airports.

These categories are pipeline-level data conventions, not standalone platform services in the sense [[service-content]] or [[service-people]] are — the record shape is a schema this article's own ingest and tiering process uses internally, not a public request/response contract. A third category this article previously described, covering parking-lot geofences, does not exist in the current pipeline.

## Tier rendering

Cluster records carry a `tier` property once [[app-orchestration-gis]] applies the
[[retail-co-location-tier-methodology|tier methodology]] to the ingested data. The
substrate's job past that point is presentation: emit a GeoJSON `FeatureCollection` per
cluster (anchor points, a catchment-radius polygon, and the `tier` property), and let the
browser layers render it — POIs as circles colored by brand family (Layer 1), tiered
clusters with catchment haloes (Layer 2), and country boundaries with filter chips (Layer
3). Hover popovers surface brand, format, year opened, and tier without a page navigation.

At 15,000 POI records (combined coverage across four countries and three brand
families), client-side rendering in MapLibre is well within comfortable operating range.
Supercluster client-side clustering becomes relevant at approximately 50,000 records;
server-side vector tile generation at 500,000+.

## Retail co-location research basis

Retail co-location clustering is a documented phenomenon with academic precedent: major retail anchor categories exhibit strong tendencies toward mutual proximity. Costco entry effects on neighbouring retailers have been studied formally. The co-location analysis the substrate produces maps directly to established methodology (average distance to nearest neighbour, tested against a permutation null distribution).

## Composition with the rest of the platform

The co-location triples produced by the location intelligence substrate compose with the rest of the platform substrate: a retail catchment polygon from the GIS layer and a building envelope from the BIM layer can share the same coordinate frame, the same per-element YAML sidecars, and the same [[worm-ledger-architecture|WORM ledger]] anchoring. Two clusters; one substrate.

[[service-slm]] is available for routine annotation work (suggesting categories for newly-ingested POIs, summarising dataset deltas, labelling anomalies) but the platform is fully functional with the [[compounding-doorman|Doorman]] shut down — the [[substrate-without-inference-base-case|Optional Intelligence]] principle applied to geographic data. This is by design: GIS analysis does not require AI; AI is additive.

## Data sourcing

Apache 2.0-licensed open datasets are the primary substrate:

- **Foursquare Open Source Places** — 100M+ POIs, monthly Parquet drops.[^2]
- **Overture Maps Foundation** — places, buildings, transportation, and addresses as GeoParquet.[^1]
- **OpenStreetMap** (via Nominatim or Photon geocoder) — secondary source for coverage gaps.

Direct scraping of retailer websites is not used where terms of service prohibit data mining. The open-data foundations have already accumulated the POI records that would otherwise require scraping.

## Forward-looking information

Statements regarding deployment schedule, customer outcomes, and feature roadmap for the Location Intelligence Substrate are intended targets subject to change. Actual timelines depend on operator review at each stage, open-data coverage accuracy, and development velocity. These statements carry "planned"/"intended"/"may" framing per the workspace's continuous-disclosure posture.[^8][^9]

## See also

- [[three-ring-architecture]] — the boundary-ingest pattern this substrate's data pipeline follows
- [[substrate-without-inference-base-case]] — GIS substrate functions fully without the AI ring
- [[customer-owned-graph-ip]] — geographic datasets owned by the customer, not the vendor
- [[retail-co-location-tier-methodology]] — the tier gates applied to the `tier` property rendered here
- [[app-orchestration-gis]] — the engine that computes tier assignment from ingested cluster data
