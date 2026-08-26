---
schema: foundry-doc-v1
title: "Regional name resolution architecture"
slug: regional-name-resolution-architecture
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
short_description: "The layered offline reverse-geocoding engine that turns a cluster's coordinates into a human-readable regional name — its boundary datasets, its country-specific routing order, and the post-processing that makes source-language names readable — with no external API calls."
cites: [overture-maps]
paired_with: regional-name-resolution-architecture.es.md
---

Every co-location cluster is labelled with a human-readable regional name — a North American metropolitan area, a European NUTS-3 region, a Mexican municipio, a Canadian census subdivision. That name is not a field on the source data. It is the output of a layered offline reverse-geocoding engine.

**Why it matters:** the whole resolution runs from local boundary files with no external geocoding API in the loop, so the [[location-intelligence-substrate|substrate]] keeps its offline-capable, no-per-request-cost posture even for the one step that most obviously invites a hosted service.

## The boundary layers

Each cluster anchor's coordinates are tested against a layered set of boundary datasets in a country-specific order. The core routing layers:

| Layer | Source | Coverage | Granularity |
|---|---|---|---|
| `us_cbsa.geojson` | US Census Bureau TIGER GENZ2023 | United States | Core-Based Statistical Areas (metro + micropolitan) |
| `ca_cma.geojson` | Statistics Canada 2021 Census | Canada | Census Metropolitan Areas |
| `ca_csd.geojson` | GADM 4.1 admin-3 | Canada | Census subdivision proxies (municipalities) |
| `mx_municipio.geojson` | GADM 4.1 admin-2 | Mexico | Municipios |
| `mx_metro.geojson` | INEGI 2018 Zonas Metropolitanas | Mexico | Metropolitan zones (intermediate fallback) |
| `eu_nuts3.geojson` | Eurostat GISCO 2021 | EU + UK + EFTA + Western Balkans | NUTS-3 regions |
| `fallback_ne_admin1.geojson` | Natural Earth 10m | Global | Admin-1 (states / provinces) |

Beyond this core set, the engine loads a further layer of settlement-level boundary files — finer-grained city, town, and municipality boundaries for the United States, the European Union, and Canada — which resolve a more specific place name where that data exists. All files load once at engine initialisation, and spatial indexes bring point-in-polygon lookups to logarithmic cost per query.

**Why it matters:** loading everything once at startup is what makes per-cluster resolution cheap enough to run across the whole manifold on every rebuild.

## Country-specific routing

The engine routes each cluster's anchor coordinates by ISO country code:

- **United States** — CBSA lookup. On a match, the name is formatted: state suffix stripped, "Metro Area" appended if absent.
- **Canada** — census subdivision first (admin-3). Where both a subdivision and the surrounding census metropolitan area match and differ, the result is composed: "Strathcona County, Edmonton". Where only one matches, that name is returned alone.
- **Mexico** — municipio lookup (admin-2), with Spanish-text post-processing on a match. On a miss, the engine falls through to the metropolitan-zone layer, and if that also misses, to the Natural Earth state-level fallback.
- **European Union, United Kingdom, EFTA, Western Balkans** — NUTS-3 lookup.
- **Fallback** — Natural Earth admin-1 for any country not covered by the layered files, returning state or province names.

Each layer carries a tolerance in its spatial query: when a point falls just outside every polygon — a coastal store on a fjord edge, for instance — the engine accepts the nearest polygon within roughly 15 km.

**Why it matters:** without the tolerance, legitimate coastal and island stores fall through every specific layer to a state-level fallback, and the map labels a Norwegian town with the name of its county.

## Post-processing the raw names

Boundary files carry source-language names with concatenated affixes that are not human-readable. Three transformations clean them.

**CamelCase splitter.** GADM admin-2 and admin-3 names are stored without word separators: "StrathconaCounty" becomes "Strathcona County".

**Spanish preposition splitter.** Mexican municipio names occasionally carry preposition concatenation — "Bocadel Río", "Apetatitlánde Antonio Carvajal". A regular expression detects the prepositions *de*, *del*, *la*, *las*, *el*, and *los* glued to a preceding lowercase character and inserts a space before them.

**Period normaliser.** "Gustavo A.Madero" is normalised to "Gustavo A. Madero".

A separate explicit-override dictionary handles cases outside the regular-expression scope: Greek names transliterated to English, Finnish suffix simplifications, Polish prefix stripping, Belgian bilingual name normalisation. That dictionary held roughly 200 entries as of mid-2026.

**Why it matters:** the name is the only part of this pipeline a human reads directly, so a mechanical artefact in it undermines confidence in every number shown beside it.

## Display overrides

Some municipio names are technically correct but not the form a Spanish-speaking reader expects on a map. A small display-override dictionary maps INEGI metropolitan-zone names to their common short forms — "Zona Metropolitana del Valle de México" becomes "Ciudad de México"; "Zona Metropolitana de Guadalajara" becomes "Guadalajara".

## Scale

After layered routing and post-processing, the engine produces roughly 1,200 unique region names across the operational footprint as of May 2026: 671 distinct US metropolitan areas, 245 Canadian regions (census subdivisions and metropolitan areas combined), 104 Mexican municipios, and several hundred European NUTS-3 regions. Each appears in cluster pop-ups and the inspector panel.

## See also

- [[location-intelligence-substrate]] — the flat-file GIS architecture this engine runs inside
- [[poi-data-schema]] — the record structures whose coordinates feed the engine
- [[service-business-clustering]] — the clustering service that consumes the resolved names
- [[gis-as-bim-substrate]] — how a resolved region name is used downstream by a BIM pipeline
