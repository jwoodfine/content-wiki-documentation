---
schema: foundry-doc-v1
title: "Parking Structures (PKS)"
slug: parking-structures
category: archetypes
type: concept
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-06-02
editor: pointsav-engineering
paired_with: parking-structures.es.md
short_description: "A Parking Structure is a 3–9 story multi-level car park at a regional airport or intercity train station — one of three Location Intelligence archetypes. Its defining relationship: a Regional Market feeds a Metro Market by plane or train, and the parking structure is the infrastructure that makes this journey possible at scale."
cites: []
---

A **Parking Structure** is a 3–9 story multi-level car park located at a regional airport or intercity train station. Its function is to serve residents of a Regional Market who drive to the transit node, park their car, and travel onward by plane or train to a Metro Market.

The defining relationship: a **Regional Market feeds a Metro Market** either by plane or by train. The parking structure is the physical infrastructure that makes this journey possible at scale.

Three-letter code: **PKS**. One of three Location Intelligence archetypes alongside [[professional-centres|Professional Centres (PRO)]] and [[vertical-warehouse|Vertical Warehouse (VWH)]].

## The regional-to-metro relationship

A PKS site sits at the hinge between two market types:

- **Regional Market** — the city or suburb where the parking structure's users live and shop (captured by the existing T1/T2/T3 PRO cluster system)
- **Metro Market** — the major city that those users travel to by plane or train

The PKS parking structure exists because the journey between them is long enough that driving to the transit node and parking beats driving all the way to the metro. This threshold is approximately 15–150 km:

| Distance to major metro | PKS viability |
|---|---|
| ≤15 km | Too close — suburb; driving to the metro is faster than parking and transiting |
| 15–100 km | Prime PKS zone — 1–2 hours driving; transit saves meaningful time |
| 100–150 km | Viable if transit is fast (high-speed rail, direct flight) |
| >150 km | Standalone market; may have its own metro relationship or be too remote |

## Transit anchor types

### Regional airports

A regional airport is distinguished from a major hub by:
- Serving primarily domestic routes or short-haul international destinations
- Passenger volume typically 500,000–5,000,000 annually
- Located 15–150 km from a major metro centre
- No T1 Professional Centres cluster immediately adjacent

OSM identification: `aeroway=aerodrome` with `aerodrome:type IN (public, regional, domestic)` or `iata=*` tag present. Exclude: `aerodrome:type IN (private, military, glider)`, `aeroway=heliport`, `aeroway=airstrip`.

**Country exceptions:**
- Mexico: No national intercity passenger rail — PKS is airport-only
- Iceland: No passenger rail — airport-only

### Intercity train stations

An intercity train station serves trains that travel 30–150 km to a major metro centre. This is distinct from metro/subway stations, commuter rail platforms, and tram and light rail stops.

OSM identification: `railway=station` with `station NOT IN (subway, light_rail, tram, monorail)`, further filtered by membership in route relations with `service IN (long_distance, high_speed, regional)`.

**National intercity operators by country:**

| Country | Operator |
|---|---|
| US | Amtrak |
| CA | VIA Rail Canada |
| FR | SNCF (TGV, Intercités, TER) |
| DE | Deutsche Bahn (ICE, IC, EC, RE, RB) |
| ES | Renfe (AVE, Alvia, Regional) |
| IT | Trenitalia, Italo |
| AT | ÖBB (Railjet, Intercity) |
| NL | NS |
| SE | SJ |
| DK | DSB |
| NO | Vy (formerly NSB) |
| FI | VR Group |
| PT | CP (Comboios de Portugal) |
| PL | PKP Intercity, RegioJet |

## Co-location signals for site selection

**Essential:**

| Signal | Threshold | Rationale |
|---|---|---|
| Regional transit anchor | ≤3 km | Airport or intercity station with direct metro service |
| Metro isolation | 15–150 km | Defines the regional relationship |
| T1 or T2 PRO cluster | ≤10 km | The Regional Market whose population generates parking demand |
| Multi-lane road access | ≤1 km | Parking structure inflow/outflow requires arterial capacity |
| Regional population | ≥150,000 | Minimum demand for structure viability |

**Significant:**

| Signal | Threshold | Rationale |
|---|---|---|
| Car rental within 1 km | — | Arriving travellers need transport; highest-confidence PKS commercial signal |
| Hotel cluster | ≤500 m | Business travel; multi-day parking demand |
| Second transit mode | ≤5 km | Airport + train station = multi-modal integration; highest-value sites |
| No major hub | ≥30 km | Competing major airport kills park-and-fly demand to regional |

**Disqualifying:**
- Major international airport within 15 km
- Population under 100,000
- No direct service to a major metro

## Commercial co-location pattern

From Overpass API queries against four confirmed PKS test sites (Toluca MX, Delicias MX, Largo FL, Haines City FL):

| Commercial use | Signal strength | Notes |
|---|---|---|
| Car rental | Defining | Found at every well-mapped airport zone |
| Auto parts | Strong | Present at manufacturing-belt sites (VWH/PKS spatial overlap) |
| Fuel / petrol | Strong | Pre-departure fill-up |
| Convenience retail | Strong | Perimeter concessions |
| Quick-service food | Moderate | 8–24 outlets per site |

## Current test results — as of 2026-06-01

The production PKS detection pipeline uses Overture airport data (unfiltered) as a proxy. After 5 km deduplication and 15–150 km metro distance filter, with T1-within-5 km hub exclusion:

**6,640 PKS candidates** across 17 display countries. "Integrated" = PKS candidate with a T1/T2 PRO cluster within 10 km — the highest-value development sites:

| Country | Total | Integrated | Integration % |
|---|---|---|---|
| US | 3,678 | 1,071 | 29% |
| DE | 547 | 216 | 39% |
| CA | 421 | 133 | 32% |
| FR | 405 | 97 | 24% |
| GB | 338 | 129 | 38% |
| IT | 245 | 41 | 17% |
| MX | 214 | 28 | 13% |
| ES | 189 | 27 | 14% |
| PL | 143 | 24 | 17% |

These counts are intended and expected to reduce substantially once `ingest-osm-airports.py` applies the IATA/aerodrome:type filter, removing private airstrips and general aviation fields. Railway station data will then add a complementary set of intercity station PKS candidates.

## Data collection plan

Two ingest scripts are planned for the transit infrastructure layer:

- `ingest-osm-airports.py` → `service-places/cleansed-civic-airports.jsonl` (IATA tag or `aerodrome:type=public/regional/domestic/international`)
- `ingest-osm-railway.py` → `service-places/cleansed-civic-railway.jsonl` (`railway=station`, exclude subway/light_rail/tram, intercity operators only)

Car rental chains are the primary commercial signal. Priority additions: Enterprise Rent-A-Car (~8,500 NA), Hertz (~3,500 NA), Avis (~2,500 NA), Sixt (~700 EU), Europcar (~2,000 EU).

## References

- [Park and ride](https://en.wikipedia.org/wiki/Park_and_ride) — Wikipedia, accessed 2026-06-14
