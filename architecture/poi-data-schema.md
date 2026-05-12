---
schema: foundry-doc-v1
title: "POI Data Schema"
slug: poi-data-schema
category: architecture
type: topic
quality: core
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-07
editor: pointsav-engineering
cites:
  - ni-51-102
paired_with: poi-data-schema.es.md
---

The POI data schema defines the record structure for the two location data classes used by the co-location intelligence platform: retail chain locations ingested from OpenStreetMap, and institutional anchor locations ingested from the Overture Maps Foundation. Both classes are normalised into a unified flat-file JSONL schema before cluster analysis. No proprietary data purchase is required; all records are derived from publicly licensed sources and are version-controllable in the same ledger as the rest of the platform. The schema has been in production since the initial platform build in 2026.

## Record types

The platform operates two record classes within its location data layer.

**Service-business records** represent individual retail chain locations: hardware stores, warehouse clubs, hypermarkets, and food anchors. Each record is identified by a `chain_id` key that links it to a chain configuration file, and by a `brand_wikidata` field holding the Wikidata QID for the retail brand. The Wikidata QID is the most reliable cross-source chain identifier because it is brand-level rather than name-level — two stores spelled differently but sharing the same QID belong to the same chain.

**Service-places records** represent institutional anchors: hospitals, universities, and airports. These are ingested from Overture Maps using the `taxonomy.primary` category field, which replaced the deprecated `categories.primary` field in the Overture 2025-11 release. Service-places records use a `category_id` key (`hospital`, `university`, `airport`) in place of `chain_id`.

## Core fields

Both record classes share the following fields:

| Field | Type | Notes |
|---|---|---|
| `location_name` | string | Display name; COALESCE of brand name and category fallback |
| `brand_wikidata` | string or null | Wikidata QID (e.g. `Q13556979`); null for civic places with no brand identity |
| `street_address` | string or null | Freeform address from OSM `addr:housenumber` + `addr:street` or Overture addresses |
| `city` | string or null | Locality from `addr:city`, `addr:town`, or `addr:municipality` |
| `region` | string or null | Province, state, or NUTS-3 region |
| `iso_country_code` | string | ISO 3166-1 alpha-2 country code |
| `latitude` | float | WGS 84, 7 decimal places |
| `longitude` | float | WGS 84, 7 decimal places |
| `naics_code` | string | NAICS industry classification |
| `top_category` | string | NAICS top-level category description |
| `sub_category` | string | NAICS sub-category description |
| `source` | string | `osm` or `overture` |
| `confidence` | float | Confidence score (OSM: fixed 0.85; Overture: from dataset) |

## Chain identification and the Wikidata QID

The `brand_wikidata` field holds the Wikidata QID for the retail brand. Wikidata QIDs are persistent, language-independent, and maintained by a global community — making them the preferred chain identifier across commercial and open POI datasets.

The OpenStreetMap community tags retail locations with `brand:wikidata=<QID>`, and the ingest pipeline uses this tag as its primary query filter. A location tagged with the correct QID will be captured regardless of local name spelling variations.

The Overture Maps Foundation exposes brand identity via the `brand.wikidata` field in its Places schema. The platform extracts this field at ingest for service-places records.

## Overture taxonomy schema

Overture Maps deprecated the `categories` struct in November 2025 and removed it in the June 2026 release. The replacement is the `taxonomy` struct, which exposes:

- `taxonomy.primary` — the primary category identifier (equivalent to the old `categories.primary`)
- `taxonomy.alternate` — an array of secondary category associations with optional attribute structs

Category identifiers are unchanged across this migration. Queries that previously read `categories.primary = 'hospital'` become `taxonomy.primary = 'hospital'` without any change to the filter values.

## Spatial deduplication

OSM data for large-format retailers sometimes includes both node and way elements for the same physical location — the building footprint as a way, and the entrance as a node. The pipeline deduplicates records within a 100-metre spatial cluster per chain, retaining the record with the most complete address fields.

A second deduplication pass runs at 25 metres across different `chain_id` values sharing the same `brand_wikidata` QID. This identifies sub-format or co-branded stores — a fuel station sharing the parent retailer's QID, for example — which are candidates for the parent-child sub-location model described below.

## Parent-child sub-location model

Large-format retailers frequently operate ancillary services at the same address: pharmacies, fuel stations, optical centres, and garden centres. In raw OSM data these appear as separate POI elements, each with a distinct name and sometimes a distinct `chain_id`.

The intended model (pending operator approval) treats the primary store as the parent location and collapses ancillary services into a `sub_entities` list within the parent record. On the map, one bubble represents the parent; the detail panel lists sub-services. This follows an industry-standard parent-child POI pattern in which the parent record holds the canonical address and coordinates, and sub-entities share that anchor while carrying their own service classification.

The Placekey standard — a globally unique location identifier with a `What@Where` structure — expresses this relationship via a shared `Where` component: two POIs at the same address share their `Where` suffix (the geocell), while their `What` prefix (the brand hash) differs. Placekey integration is intended as the primary mechanism for identifying co-located sub-businesses in a future pipeline update [ni-51-102].

## Address completeness

Address coverage in the current dataset varies by country. OSM coverage of `addr:housenumber` and `addr:street` is strong in Western Europe and Canada, moderate in the United States, and sparse in some Nordic and Southern European markets.

A planned enhancement will spatial-join POI records against the Overture Addresses theme (≤15 metre radius) to back-fill missing street-level addresses. The Overture Addresses theme provides structured address records for over two billion global addresses derived from authoritative national registries [ni-51-102].

## Data update cadence

Service-business records are re-ingested per chain on demand — typically when a new chain is added to the configuration or when quarterly coverage audits flag anomalies. Service-places records are re-ingested against new Overture quarterly releases; the Overture S3 path in the ingest script must be updated to reference each new release.

## See also

- [[location-intelligence-platform]] — platform overview, Named-Anchor Model, and V2 scoring tiers
- [[location-intelligence-substrate]] — flat-file GIS architecture and storage layer
- [[app-orchestration-gis]] — GIS service application that operates the ingest pipeline
