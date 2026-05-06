---
schema: foundry-doc-v1
title: "Location Intelligence Platform — Strategy and Architecture"
slug: location-intelligence-strategy
category: architecture
type: topic
quality: core
short_description: "The strategic and architectural frame for the platform's Location Intelligence substrate: a flat-file open-GIS approach that lets customers own their location data end-to-end, running offline, without ongoing per-seat or per-request vendor costs."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-04-30
editor: pointsav-engineering
cites:
  - geoparquet-spec
  - flatgeobuf
  - overture-maps
  - foursquare-os-places
  - maplibre-gl-js
  - martin-tile-server
  - pmtiles-spec
  - tippecanoe
  - meteoblue-maps-api
  - mdpi-vector-rendering-2025
  - carto-tile-architecture
  - esri-arcgis-online-pricing
  - mapbox-pricing
  - placer-ai
  - planetizen-retail-clusters
  - nber-w17220-costco
  - walmart-store-count-2025
  - homedepot-store-count-2025
  - costco-store-count-2025
  - ikea-spain-stores
  - bricomart-spain
  - leroy-merlin-spain
  - nominatim-osm
  - photon-geocoder
  - deck-gl
  - eupl-1-2
  - ni-51-102
  - osc-sn-51-721
paired_with: location-intelligence-strategy.es.md
---

The Location Intelligence substrate gives customers a dataset of place records — businesses, points of interest, parking geometries — stored as flat files the customer owns, versioned in the same ledger as every other Totebox record, and rendered through an open-source mapping stack with no per-request or per-seat costs. The first application is a co-location map: every Walmart-family, Home-Depot-family, and Costco location across the United States, Canada, Mexico, and Spain, with retail clusters that fall within defined proximity ranges surfaced as the visible analytic.

This article describes the market context, the architectural decisions, the technical stack, and the planned implementation path.

## The Location Intelligence market — structural patterns

The Location Intelligence segment in 2026 organises into four architectural families, each with a structural revenue mechanism that constrains what it can offer.

**Cloud-native query-on-warehouse platforms.** These platforms execute spatial queries directly inside a customer's data warehouse, then render tiles from query results [carto-tile-architecture]. The architecture requires no data copy. It also requires the customer to maintain a data warehouse; customers who want to operate without one are not addressed.

**Legacy enterprise GIS.** Products in this category sell progressive user-type licences and use credits as the in-platform currency for storage, analysis tools, and premium data [esri-arcgis-online-pricing]. The licensing model makes them a poor fit for SMB customers operating a small, owned dataset without seat-by-seat budget allocation.

**Developer-tier mapping platforms.** These price on monthly active users, map loads, tile-API requests, and tileset-processing volume [mapbox-pricing]. The open-source fork of the leading platform (MapLibre GL JS) is now the standard for vector-tile rendering. The proprietary side ties cost to traffic; a public-facing site with substantial traffic generates a proportionally large bill.

**Foot-traffic and movement analytics.** These operate a panel of mobile devices and extrapolate store visitation through statistical methods [placer-ai]. The data is additive for retail-strategy work. The architecture is necessarily centralised and privacy-aggregated — a customer cannot operate an equivalent instance on their own data while remaining a customer.

**Open-data foundations.** Two public initiatives reset the substrate floor: Foursquare released its 100M+ POI dataset as Apache-2.0-licensed monthly Parquet drops in late 2024 [foursquare-os-places], and the Overture Maps Foundation publishes places, buildings, transportation, and addresses as GeoParquet on public cloud storage [overture-maps]. A Location Intelligence platform built in 2026 that does not draw from these substrates duplicates work the open-data community has already completed.

Each platform family ties revenue to something the customer's data passes through — warehouse compute, seat licences, request volume, or panel access. None can offer the inverse: a substrate the customer owns end-to-end, runs offline, and replicates without paying recurring costs. The platform's Location Intelligence substrate occupies that position.

## Architectural commitments — flat-file, open standards, optional intelligence

Three commitments carried forward from the rest of the platform define what the Location Intelligence substrate can show that no service in the market above can:

**The customer's location dataset is a customer-owned directory.** `service-business`, `service-places`, and `service-parking` are not databases living in a vendor cloud — they are GeoParquet files (with JSONL siblings for git-diff readability) inside a Totebox Archive the customer signs and stores. A customer who adds 200 retail locations of their own owns those records the same way they own their documents.

**Intelligence is optional.** The map renders, the co-location query runs, and the layers compose without any AI compute. `service-slm` becomes available for annotation work — suggesting categories for newly-ingested POIs, summarising dataset deltas, flagging anomalies — but the platform operates fully with the Doorman shut down.

**The substrate composes with the rest of Foundry.** Co-location triples produced in `service-business` today can compose with building envelopes from `service-bim` tomorrow. Two clusters, one coordinate system, one WORM ledger, one identity model.

## Data architecture — flat-file canonical for service-business

The operator-facing question is whether `service-business` keeps records flat or in a database. Three options are viable:

**Flat-file canonical.** JSONL for human-readable change tracking; GeoParquet for performant analytic reads; FlatGeobuf for browser-side spatial bounding-box streaming. GeoParquet is an OGC incubating standard that adds Point, Line, and Polygon types to columnar Parquet [geoparquet-spec]. FlatGeobuf carries a Hilbert R-tree at the file header that lets a browser stream only the features inside the current viewport over HTTP range requests [flatgeobuf]. Advantages: sovereign by construction, version-controllable, customer-portable, zero infrastructure to operate. Constraint: writes are single-author-at-a-time (the file is rewritten on update).

**Database canonical.** PostgreSQL with PostGIS. Advantages: rich spatial SQL, multi-writer concurrency. Constraint: the customer's data lives in a running daemon; portability requires a dump-and-restore, not a directory move.

**Hybrid.** Flat-file canonical; ephemeral database materialised from the flat file as a query cache. This matches the vault-as-canonical, derived-tables-as-cache pattern the platform already uses for bookkeeping.

For the current workload — tens of thousands of POI records across four countries, three brand families, infrequent batch writes, read-mostly query — flat-file is sufficient. Foursquare and Overture Maps Foundation chose the same format for their substrate releases [foursquare-os-places][overture-maps]. The recommendation: **GeoParquet as the canonical at-rest format** (one file per country per service, rolled monthly), **JSONL siblings for git-tracked history**, **FlatGeobuf as the browser-streamable derivative**. If a future workload introduces real-time concurrent writes across multiple browsers simultaneously, the hybrid pattern is the migration path.

## Per-record schema

A single record shape covers all three Ring 1 services with discriminator fields. Stored as JSONL for git readability; batch-rolled monthly into per-country GeoParquet and FlatGeobuf.

```jsonc
{
  "id": "01HZ...",                          // ULID
  "service": "business" | "places" | "parking",
  "operator": "walmart",                    // brand slug
  "operator_brand_family": "walmart",       // unifies regional equivalents
  "name": "Walmart Supercenter Burnaby",    // localised
  "country_code": "US" | "CA" | "MX" | "ES",
  "address": "...",
  "lat": 49.2827,
  "lng": -123.1207,
  "geometry": { "type": "Point", ... },     // GeoJSON; Polygon for parking
  "store_type": "supercenter" | "warehouse" | "diy" | "warehouse-club",
  "place_type": null,                       // service-places only: hospital | university | airport
  "open_year": 2018,
  "data_source": "official-store-locator" | "openstreetmap" | "overture" | "foursquare-os" | "manual",
  "data_provenance_url": "https://...",
  "captured_at": "2026-04-30T00:00:00Z"
}
```

Brand-family normalisation lets the co-location query treat regional equivalents as one logical operator across countries:

```yaml
walmart_family:    [walmart, ikea-spain]        # large-format consumer general merchandise
homedepot_family:  [homedepot, bricomart-spain] # warehouse-format DIY and trade
costco_family:     [costco]                     # warehouse-club; present in Spain since 2014
```

## Spain Home Depot equivalent — research finding

Identifying the Home Depot structural analog in Spain requires distinguishing between consumer-DIY format and trade-warehouse format.

**Bricomart (rebranded Obramat in 2024)** — owned by the Adeo group (the same parent as Leroy Merlin), warehouse format oriented towards professional trade and self-builder customers, approximately 22 locations in Spain [bricomart-spain]. The format match — warehouse-scale, professional-trade-focused, large-volume positioning — is the closest structural analog to Home Depot.

**Leroy Merlin** — also Adeo group, the dominant consumer-DIY brand in Spain at 120+ locations [leroy-merlin-spain]. The closest analog by store count and consumer visibility, but the format is consumer-DIY rather than trade-warehouse; the Lowe's comparison fits it better than the Home Depot one.

**Recommendation: Bricomart (Obramat) maps to Home Depot** in the brand-family schema. Leroy Merlin maps to the Lowe's position. Costco has direct Spain presence at five warehouses [costco-store-count-2025], so the co-location query in Spain is genuinely cross-brand, not a synthesis across regional substitutes.

## Map tile and layer delivery

The visual quality target is WebGL-rendered vector tiles styled in the browser. The recommended open-source stack:

- **Renderer**: MapLibre GL JS [maplibre-gl-js] — the community-maintained fork that supports vector tiles and WebGL, dynamic styling, and 3D without per-traffic licence cost. Benchmarks confirm WebGL renderers outperform raster-based alternatives at high feature counts [mdpi-vector-rendering-2025].
- **Data-visualisation overlays**: deck.gl [deck-gl] when scatter, heatmap, arc, or polygon-extrusion layers are needed.
- **Tile generation**: Tippecanoe for converting GeoJSON to MBTiles or PMTiles, with 85–95 percent file-size reductions over raw GeoJSON [tippecanoe].
- **Tile serving**: Martin, the MapLibre Foundation's Rust tile server [martin-tile-server]. Supports PostGIS, MBTiles, and PMTiles. Rust-aligned with the rest of the platform stack.
- **Tile archive format**: PMTiles [pmtiles-spec] — a single-file archive that supports HTTP range requests, allowing the deployment to serve tiles directly from nginx without running Martin when tiles are pre-baked.

Implementation rule: bake static tiles for brand-family POIs and co-location radius circles via Tippecanoe and PMTiles; serve directly from nginx. Move to Martin only when dynamic tile generation is needed.

## Co-location analysis algorithm

The surface use case: show where Walmart-family, Home-Depot-family, and Costco co-locate within 1 km, 2 km, and 3 km of each other. Retail co-location clustering is a recognised analytical method; the tendency of complementary large-format retailers to cluster near each other is documented in the literature [planetizen-retail-clusters][nber-w17220-costco].

Algorithm (single batch pass):

1. Iterate every record where `operator_brand_family = walmart_family`.
2. For each, find the nearest record where `operator_brand_family = homedepot_family` and the nearest where `operator_brand_family = costco_family`. A haversine distance against an in-memory R-tree on tens of thousands of records is microseconds per query.
3. Bucket each triple by the maximum pairwise distance among the three legs: under 1 km, 1–2 km, 2–3 km, above 3 km.
4. Emit a GeoJSON FeatureCollection: triple centroid, triangle polyline connecting the three vertices, three radius circles, and a `cluster_grade` property.

Browser visualisation (MapLibre GL):

- Layer 1: POIs as circles, coloured by `operator_brand_family`, sized by `store_type`.
- Layer 2: co-location triples with `cluster_grade ≤ 1 km` shown as filled triangles and 1-km radius haloes; 2-km and 3-km grade layers toggleable.
- Layer 3: country boundary; brand-family filter chips.
- Hover popovers: brand, format, year opened, distances to co-located neighbours, cluster grade.

The current dataset is approximately 15,000 records (combined US/CA/MX/ES across three brand families) — client-side rendering is sufficient at this scale. US breakdown: Walmart 4,605 [walmart-store-count-2025]; Home Depot 2,359 [homedepot-store-count-2025]; Costco (US + Puerto Rico) 623 [costco-store-count-2025]. Spain: IKEA approximately 28 [ikea-spain-stores]; Bricomart approximately 22 [bricomart-spain]; Costco 5 [costco-store-count-2025].

## Planned implementation path

All milestones below are intended targets, subject to acceptance criteria and operator review at each stage. [ni-51-102] [osc-sn-51-721]

**Week 1 — Deployment frame.** The deployment instance is provisioned at `deployments/gateway-orchestration-gis-1/` with MANIFEST, README, and README.es.md per the deployment template. An nginx virtual host for `gis.woodfinegroup.com` serves HTTP first; HTTPS via Let's Encrypt once DNS resolves. Sub-clones are provisioned for `pointsav-monorepo`, `pointsav-design-system`, and `woodfine-fleet-deployment` under `clones/project-gis/`. The catalog folder in `customer/woodfine-fleet-deployment/gateway-orchestration-gis/` is created with initial GUIDE drafts.

**Week 2 — Application scaffold.** `app-orchestration-gis` Rust binary (Axum server, MapLibre GL JS front end) binds to the next available local port. Initial HTML shell with map container, brand-family filter chips, and country selector. Static dummy POI data verifies the rendering pipeline end-to-end.

**Week 3 — US data ingestion.** The Walmart, Home Depot, and Costco subset is drawn from Foursquare's Open Source Places monthly Parquet drop or the Overture Maps Foundation places dataset [foursquare-os-places][overture-maps], filtered by operator name and country, normalised into the `service-business` schema, and written as JSONL, GeoParquet, and FlatGeobuf. Approximately 7,600 records. Co-location algorithm runs in seconds at this scale.

**Week 4 — Co-location surface ready for demonstration.** MapLibre GL layers for POIs, co-location triples, and 1/2/3 km radius circles. Click-through detail: brand, format, distance, cluster grade.

**Weeks 5–6 — Canada and Mexico.** Canada: Walmart 404, Home Depot 182, Costco 109. Mexico: Walmart 3,191, Home Depot 142, Costco 41. Total dataset approximately 12,000 records before Spain.

**Week 7 — Spain.** IKEA Spain under `walmart_family`, Bricomart under `homedepot_family`, Costco Spain. Approximately 55 records — illustrative of the cross-regional brand-family abstraction.

**Weeks 8+ — service-places, service-parking, Workplace OS scaffold, editorial fan-out.** `app-workplace-gis` Tauri desktop shell; `service-places` ingestion (hospitals, universities, airports); TOPIC drafts for the documentation wiki; COMPONENT drafts for the design system.

## Deployment naming — Nomenclature recommendation

The correct Nomenclature prefix for a Workplace OS deployment instance is `node-`. The Nomenclature Matrix §4 defines `node-` as "an individual user terminal endpoint / state manager." A `node-workplace-gis` instance is precisely "an individual user terminal endpoint" that projects the GIS workplace surface. This reuses the existing prefix and preserves symmetry with `node-console-gis`.

If the operator later finds `node-workplace-*` insufficient — for example, because dedicated hardware warrants a visually distinct prefix — the alternative is a `desktop-` prefix amendment to the Nomenclature Matrix, which is a Master-scope edit gated on operator ratification.

## See Also

- [[three-ring-architecture]] — the Ring 1 / Ring 2 / Ring 3 composition that service-business, service-places, and service-parking implement
- [[compounding-substrate]] — the sovereignty and optional-intelligence properties this substrate implements
- [[worm-ledger-architecture]] — the append-only ledger that anchors co-location records in the customer's Totebox Archive
- [[service-slm]] — the optional Ring 3 service available for annotation and anomaly detection on ingested POI records

## References

1. Foursquare Open Source Places — 100M+ POIs, Apache 2.0, monthly Parquet. [foursquare-os-places]
2. Overture Maps Foundation — GeoParquet places schema, v1.13.0, October 2025. [overture-maps]
3. GeoParquet specification (OGC incubating). [geoparquet-spec]
4. FlatGeobuf — packed Hilbert R-tree, HTTP range request streaming. [flatgeobuf]
5. MapLibre GL JS — community-maintained WebGL vector-tile renderer. [maplibre-gl-js]
6. MDPI vector-rendering benchmark 2025 — WebGL vs raster at scale. [mdpi-vector-rendering-2025]
7. Martin tile server (MapLibre Foundation, Rust). [martin-tile-server]
8. Tippecanoe (Felt fork) — GeoJSON to MBTiles/PMTiles conversion. [tippecanoe]
9. PMTiles specification — single-file HTTP range-request archive. [pmtiles-spec]
10. CARTO tile architecture — query-on-warehouse pattern. [carto-tile-architecture]
11. ArcGIS Online pricing — user-type licence model. [esri-arcgis-online-pricing]
12. Mapbox pricing — per-traffic cost model. [mapbox-pricing]
13. Placer.ai — mobile-device-panel foot-traffic analytics. [placer-ai]
14. Planetizen — retail co-location clustering patterns. [planetizen-retail-clusters]
15. NBER W17220 — Costco entry effects on incumbents. [nber-w17220-costco]
16. Walmart US store count 2025. [walmart-store-count-2025]
17. Home Depot US store count 2025. [homedepot-store-count-2025]
18. Costco store count 2025 (US, CA, MX, ES). [costco-store-count-2025]
19. IKEA Spain store count. [ikea-spain-stores]
20. Bricomart Spain — Obramat rebrand 2024. [bricomart-spain]
21. Leroy Merlin Spain store count. [leroy-merlin-spain]
22. Nominatim / OSM geocoder. [nominatim-osm]
23. Photon geocoder. [photon-geocoder]
24. deck.gl — WebGL data-visualisation framework. [deck-gl]
25. EUPL-1.2 — European Union Public Licence. [eupl-1-2]
26. NI 51-102, Continuous Disclosure Obligations (BCSC). [ni-51-102]
27. OSC Staff Notice 51-721, Forward-Looking Information Disclosure. [osc-sn-51-721]

---

## Provenance

Source material: workspace-root draft `topic-location-intelligence-strategy.md` (authored 2026-04-30 at workspace v0.1.88). Background references: `clones/project-gis/.claude/manifest.md`, `clones/project-bim/.claude/manifest.md` (parallel cluster pattern), DOCTRINE.md claims #14/#16/#18/#28/#38, `conventions/four-tier-slm-substrate.md`, `IT_SUPPORT_Nomenclature_Matrix_V8.md` §4. Web research: 17 primary sources consulted — market survey (CARTO, ArcGIS, Mapbox, Placer.ai architectures), open-data foundations (Foursquare OS, Overture Maps), tile stack (MapLibre, Martin, PMTiles, Tippecanoe, deck.gl), Spain DIY-retail landscape (Bricomart/Obramat, Leroy Merlin, Bauhaus, Brico Depôt), store-count data across US/CA/MX/ES, retail-clustering literature.

Refinement disciplines applied: no body H1; structural-positioning discipline (market-survey section describes structural revenue mechanisms, not competitive-by-name contrast; no service named by competitive framing); BCSC forward-looking adapter (implementation milestone schedule, co-location demo deliverables, service-places expansion, and Workplace OS scaffold all labelled as intended targets per ni-51-102/osc-sn-51-721); banned-vocabulary pass (`blazingly-fast` removed from Martin description; no other substitutions required); Open Questions §10 from source omitted from published TOPIC (internal operator decisions, not public doctrine); Provenance footer BCSC-scrubbed.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*

*Woodfine Capital Projects™, Woodfine Management Corp™, PointSav Digital Systems™, Totebox Orchestration™, and Totebox Archive™ are trademarks of Woodfine Capital Projects Inc., used in Canada, the United States, Latin America, and Europe. All other trademarks are the property of their respective owners.*
