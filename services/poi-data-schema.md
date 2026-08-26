---
schema: foundry-doc-v1
title: "POI data schema"
slug: poi-data-schema
language: en
category: services
index_group: specialist-and-domain-services
type: topic
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-08-26
editor: pointsav-engineering
short_description: "The record structures for location data ingested from OpenStreetMap and Overture Maps Foundation, normalised into a unified JSONL schema before cluster analysis. Wikidata QIDs are the primary chain identifier, and a parent-child sub-location model handles co-branded ancillary services."
cites: [overture-maps]
paired_with: poi-data-schema.es.md
---

The POI data schema defines the record structure for the two location-data classes the [[location-intelligence-substrate|location intelligence substrate]] consumes: retail chain locations ingested from OpenStreetMap, and institutional anchor locations ingested from the Overture Maps Foundation. Both are normalised into a unified flat-file JSONL schema before [[service-business-clustering|cluster analysis]] runs.

**Why it matters:** no proprietary data purchase is required. Every record derives from a publicly licensed source and is version-controllable in the same ledger as the rest of the platform, so a customer's location dataset is auditable end to end.

## Record types

**Service-business records** represent individual retail chain locations — hardware stores, warehouse clubs, hypermarkets, food anchors. Each is identified by a `chain_id` key linking it to a chain configuration file, and by a `brand_wikidata` field holding the Wikidata QID for the brand.

**Service-places records** represent institutional anchors — hospitals, universities, airports — ingested from Overture Maps via the `taxonomy.primary` category field. These use a `category_id` key (`hospital`, `university`, `airport`) in place of `chain_id`.

## Core fields

Both record classes share the following:

| Field | Type | Notes |
|---|---|---|
| `location_name` | string | Display name; COALESCE of brand name and category fallback |
| `brand_wikidata` | string or null | Wikidata QID (e.g. `Q13556979`); null for civic places with no brand identity |
| `street_address` | string or null | Freeform address from OSM `addr:housenumber` + `addr:street`, or Overture addresses |
| `city` | string or null | Locality from `addr:city`, `addr:town`, or `addr:municipality` |
| `region` | string or null | Province, state, or NUTS-3 region |
| `iso_country_code` | string | ISO 3166-1 alpha-2 |
| `latitude` | float | WGS 84, 7 decimal places |
| `longitude` | float | WGS 84, 7 decimal places |
| `naics_code` | string | NAICS industry classification |
| `top_category` | string | NAICS top-level category description |
| `sub_category` | string | NAICS sub-category description |
| `source` | string | `osm` or `overture` |
| `confidence` | float | Confidence score (OSM: fixed 0.85; Overture: from dataset) |

**Why it matters:** one shared field set across both classes means downstream analysis code does not branch on record type for anything except the chain-versus-category key.

## Chain identification and the Wikidata QID

The `brand_wikidata` field holds the Wikidata QID for the retail brand. QIDs are persistent, language-independent, and community-maintained, which makes them the preferred chain identifier across both commercial and open POI datasets — they are brand-level rather than name-level, so two stores spelled differently but sharing a QID belong to the same chain.

The OpenStreetMap community tags retail locations with `brand:wikidata=<QID>`, and the ingest uses this tag as its primary query filter; a location tagged with the correct QID is captured regardless of local name spelling. Overture Maps exposes the same identity via `brand.wikidata` in its Places schema, extracted at ingest for service-places records.

**Why it matters:** chain identity survives translation, rebranding of a local storefront name, and inconsistent data entry — which is what makes cross-border comparison possible at all.

## Overture taxonomy schema

Overture Maps deprecated the `categories` struct in November 2025 and removed it in the June 2026 release. The replacement `taxonomy` struct exposes `taxonomy.primary` (equivalent to the old `categories.primary`) and `taxonomy.alternate`, an array of secondary category associations with optional attribute structs.

Category identifiers are unchanged across the migration: a query that previously read `categories.primary = 'hospital'` becomes `taxonomy.primary = 'hospital'` with no change to the filter values.

## Spatial deduplication

OSM data for large-format retailers sometimes includes both a node and a way for the same physical location — the building footprint as a way, the entrance as a node. The ingest deduplicates by rounding each location's coordinates to four decimal places (roughly 11 metres) and treating records that round to the same pair as the same building, retaining the record with the most complete address fields.

Records sharing coordinates at this resolution but carrying different `chain_id` values under the same `brand_wikidata` QID are treated as sub-format or co-branded stores — a fuel station sharing the parent retailer's QID, for instance — and are candidates for the parent-child model below.

**Why it matters:** without this pass, a single store can appear two or three times and inflate every count computed downstream of it.

## Parent-child sub-location model

Large-format retailers frequently operate ancillary services at the same address: pharmacies, fuel stations, optical centres, garden centres. In raw OSM data these appear as separate POI elements, each with a distinct name and sometimes a distinct `chain_id`.

A configuration-driven parent mapping resolves this: each sub-entity `chain_id` known to be an ancillary service maps to its canonical parent chain. Sub-entities are excluded from cluster scoring and surfaced only on the parent's info card; the map shows one marker per parent location. This follows the industry-standard parent-child POI pattern, in which the parent record holds the canonical address and coordinates and sub-entities share that anchor while carrying their own service classification.

The Placekey standard — a globally unique location identifier with a `What@Where` structure — expresses the same relationship via a shared `Where` component: two POIs at one address share the geocell suffix while their brand-hash prefix differs. A Placekey-based spatial-matching approach is a planned future mechanism rather than the current one; the schema retains a `placekey` field for it, not yet populated during ingest.

**Why it matters:** counting a hypermarket's fuel station as an independent anchor would inflate a cluster's apparent brand diversity, which is the signal the tier system is built on.

## Address completeness

Address coverage varies by country. OSM coverage of `addr:housenumber` and `addr:street` is strong in Western Europe and Canada, moderate in the United States, and sparse in some Nordic and Southern European markets. A planned enhancement will spatial-join POI records against the Overture Addresses theme within a 15-metre radius to back-fill missing street-level addresses; that theme provides structured records for over two billion global addresses derived from authoritative national registries.

## Data update cadence

Service-business records are re-ingested per chain on demand — typically when a new chain is added to the configuration, or when quarterly coverage audits flag anomalies. Service-places records are re-ingested against new Overture quarterly releases; the ingest script's Overture object-store path must be updated to reference each new release.

## See also

- [[location-intelligence-substrate]] — the flat-file GIS architecture and storage layer
- [[service-business-clustering]] — the clustering service that consumes these records
- [[service-places-filtering]] — civic-anchor filtering downstream of ingest
- [[regional-name-resolution-architecture]] — how cluster coordinates become regional names
- [[location-intelligence-platform]] — the application surface these records are served through

---

*OpenStreetMap data © OpenStreetMap contributors, licensed under ODbL. Overture Maps Foundation data under CDLA Permissive 2.0.*
