---
title: "Location Intelligence Substrate"
slug: location-intelligence-substrate
category: architecture
status: stable
last_edited: 2026-04-30
editor: pointsav-engineering
quality: complete
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
    text: "OSC Staff Notice 51-721 Forward-Looking Information Disclosure"
---

Foundry's Location Intelligence Substrate is a flat-file, open-GIS architecture that lets customers own their geographic datasets end-to-end — no tile API billing, no warehouse licensing, no cloud-vendor lock-in. The substrate is built on Apache-licensed open-data foundations (Overture Maps Foundation, Foursquare Open Source Places) and rendered via a Rust-aligned open-source stack (MapLibre GL JS, Martin tile server, PMTiles).[^1][^2]

The first deployed surface is `gis.woodfinegroup.com` — a co-location map showing retail anchor co-presence across the United States, Canada, Mexico, and Spain.

## Architecture — flat-file vs database

Three options exist for canonical storage of geographic records:

**Flat-file canonical** — JSONL for human-diffable change tracking; GeoParquet for performant analytic reads; FlatGeobuf for browser-side spatial-bbox streaming. GeoParquet is an OGC incubating standard that adds Point/Line/Polygon types to columnar Parquet.[^3] FlatGeobuf carries a packed Hilbert R-tree at the file header that enables a browser to stream only the features inside the current viewport over HTTP range requests.[^4] Advantages: sovereign by construction, version-controllable, customer-portable, zero infrastructure to operate. Limitation: writes are single-author-at-a-time; concurrent online edits would race.

**Database canonical** — PostgreSQL plus a spatial extension, the genre's industry default. Advantages: rich spatial SQL, multi-writer concurrency, production-tested operations. Limitation: the customer's data lives in a running daemon they must operate; portability requires a dump-and-restore that is not a directory move.

**Hybrid** — flat-file canonical, ephemeral database materialised from the flat-file as a query cache. Matches the vault-as-canonical, derived-tables-as-cache approach Foundry uses for bookkeeping.

For workloads of tens of thousands of POI records across a small number of countries, with infrequent batch writes and read-mostly queries, flat-file is sufficient and is the architecture both Foursquare and Overture Maps Foundation chose for their substrate releases.[^1][^2] The recommendation: GeoParquet as the canonical at-rest format (one file per country per service, rolled monthly), JSONL siblings for git-tracked human-diffable history, FlatGeobuf as the browser-streamable derivative.

## Map tile and layer delivery

The rendering stack uses MapLibre GL JS in the browser — a community-driven open-source vector-tile renderer that supports WebGL, dynamic styling, smooth animation, and 3D without per-traffic licence cost.[^5]

Tile generation uses Tippecanoe (Felt's actively-maintained fork) for converting GeoJSON to MBTiles or PMTiles, reducing file size by 85–95% over raw GeoJSON at POI dataset scale. Tile serving uses Martin, the MapLibre Foundation's Rust tile server, supporting PostGIS, MBTiles, and PMTiles.[^6]

The tile archive format is PMTiles — a single-file archive with HTTP range-request support, enabling tile serving directly from nginx without running Martin when the tiles are pre-baked.[^7] Martin is used when dynamic tile generation is needed (viewport-filtered density layers that respond to real-time filter state).

For data-visualisation overlays (scatter, heatmap, arc, polygon-extrusion layers), deck.gl composes naturally with MapLibre.

## Service schema — service-business, service-places, service-parking

A single record shape covers all three Ring 1 location services with discriminator fields:

```jsonc
{
  "id": "01HZ...",                     // ULID
  "service": "business" | "places" | "parking",
  "operator": "walmart",               // brand slug
  "operator_brand_family": "walmart",  // unifies regional equivalents
  "name": "Walmart Supercenter Burnaby",
  "country_code": "US" | "CA" | "MX" | "ES",
  "address": "...",
  "lat": 49.2827,
  "lng": -123.1207,
  "geometry": { "type": "Point", ... },
  "store_type": "supercenter" | "warehouse" | "diy" | "warehouse-club",
  "data_source": "official-store-locator" | "openstreetmap" | "overture" | "foursquare-os" | "manual",
  "captured_at": "2026-04-30T00:00:00Z"
}
```

Brand-family normalisation lets co-location queries treat regional equivalents as one logical operator across countries. `service-places` carries a `place_type` field (hospital, higher-education, airport). `service-parking` carries a Polygon `geometry` (the lot geofence) rather than a Point, plus an `associated_business_id` linking the lot to its anchor business when known.

## Co-location analysis algorithm

The co-location query identifies locations from brand family A within 1 km, 2 km, and 3 km of locations from brand family B (and optionally a third family). Algorithm:

1. Iterate every record in brand family A.
2. For each, find the nearest record in each other brand family using a haversine distance against an in-memory R-tree index. At tens of thousands of records, each lookup runs in microseconds.
3. Bucket each multi-brand tuple by the maximum pairwise distance: `<1 km`, `1–2 km`, `2–3 km`, `>3 km`.
4. Emit a GeoJSON FeatureCollection: tuple centroid, triangle polyline connecting the locations, radius circles, and a `cluster_grade` property.

Browser visualisation layers: POIs as circles coloured by brand family (Layer 1); co-location tuples with their radius haloes, toggled by grade (Layer 2); country boundaries and filter chips (Layer 3). Hover popovers show brand, format, year opened, distance to nearest co-located neighbours, and cluster grade.

At 15,000 POI records (combined coverage across four countries and three brand families), client-side rendering in MapLibre is well within comfortable operating range. Supercluster client-side clustering becomes relevant at approximately 50,000 records; server-side vector tile generation at 500,000+.

## Retail co-location research basis

Retail co-location clustering is a documented phenomenon with academic precedent: major retail anchor categories exhibit strong tendencies toward mutual proximity. Costco entry effects on neighbouring retailers have been studied formally. The co-location analysis the substrate produces maps directly to established methodology (average distance to nearest neighbour, tested against a permutation null distribution).

## Composition with the rest of Foundry

The co-location triples produced by the location intelligence substrate compose with the rest of the Foundry substrate: a retail catchment polygon from the GIS layer and a building envelope from the BIM layer can share the same coordinate frame, the same per-element YAML sidecars, and the same WORM ledger anchoring. Two clusters; one substrate.

`service-slm` is available for routine annotation work (suggesting categories for newly-ingested POIs, summarising dataset deltas, labelling anomalies) but the platform is fully functional with the Doorman shut down — the Optional Intelligence principle applied to geographic data. This is by design: GIS analysis does not require AI; AI is additive.

## Data sourcing

Apache 2.0-licensed open datasets are the primary substrate:

- **Foursquare Open Source Places** — 100M+ POIs, monthly Parquet drops.[^2]
- **Overture Maps Foundation** — places, buildings, transportation, and addresses as GeoParquet.[^1]
- **OpenStreetMap** (via Nominatim or Photon geocoder) — secondary source for coverage gaps.

Direct scraping of retailer websites is not used where terms of service prohibit data mining. The open-data foundations have already accumulated the POI records that would otherwise require scraping.

## Forward-looking information

Statements regarding deployment schedule, customer outcomes, and feature roadmap for the Location Intelligence Substrate are intended targets subject to change. Actual timelines depend on operator review at each stage, open-data coverage accuracy, and development velocity. These statements carry "planned"/"intended"/"may" framing per the workspace's continuous-disclosure posture.[^8][^9]

## See Also

- [[three-ring-architecture]] — `service-business`, `service-places`, and `service-parking` are Ring 1 services
- [[substrate-without-inference-base-case]] — GIS substrate functions fully without the AI ring
- [[customer-owned-graph-ip]] — geographic datasets owned by the customer, not the vendor

## References

[^1]: Overture Maps Foundation — GeoParquet places schema. overturemaps.org
[^2]: Foursquare Open Source Places — 100M+ POIs, Apache 2.0. huggingface.co/datasets/foursquare
[^3]: GeoParquet specification — OGC incubating standard. geoparquet.org
[^4]: FlatGeobuf — Hilbert R-tree packed flat-file format. flatgeobuf.org
[^5]: MapLibre GL JS — Community-driven vector-tile renderer. maplibre.org
[^6]: Martin tile server — Rust tile server (MapLibre Foundation). maplibre.org/martin
[^7]: PMTiles — Single-file tile archive with HTTP range requests. protomaps.com/pmtiles
[^8]: NI 51-102 Continuous Disclosure Obligations — BCSC
[^9]: OSC Staff Notice 51-721 Forward-Looking Information Disclosure

---
Copyright © 2026 Woodfine Capital Projects Inc.
Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).
PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.
