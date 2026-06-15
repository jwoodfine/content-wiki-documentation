---
schema: foundry-doc-v1
title: "Vertical Warehouse (VWH)"
slug: vertical-warehouse
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
paired_with: vertical-warehouse.es.md
short_description: "A Vertical Warehouse is a 3–6 story multi-storey building used for light manufacturing, just-in-time logistics, and last-mile delivery in urban or near-urban locations — one of three Location Intelligence archetypes."
cites: []
---

A **Vertical Warehouse** is a 3–6 story multi-storey building used for light manufacturing, just-in-time logistics, and last-mile delivery in urban or near-urban locations. The building type stacks functions that would traditionally spread horizontally across a ground-level industrial precinct: fabrication, component storage, assembly, and outbound dispatch.

Three-letter code: **VWH**. One of three Location Intelligence archetypes alongside [[professional-centres|Professional Centres (PRO)]] and [[parking-structures|Parking Structures (PKS)]].

## What a Vertical Warehouse does

Typical tenant mix:

- **Light manufacturing** — electronics assembly, robotics integration, paint and coatings formulation, precision fabrication
- **Just-in-time delivery** — regional distribution hub for e-commerce and manufacturing supply chains; goods arrive by truck, are processed, and depart same-day or next-day
- **Last-mile logistics** — final sort and dispatch for urban delivery zones; proximity to dense population required

The vertical form factor is driven by urban land cost. Where a horizontal warehouse would require 4–8 acres at the urban fringe, a Vertical Warehouse achieves equivalent floor area on 1–2 acres by going up. Ground-floor truck access and dock levellers are retained; upper floors are served by freight elevators rated for forklift loads.

## Where Vertical Warehouses locate

**Spatial signature:** 5–25 km from the nearest major metro centre, in the industrial-to-suburban transition zone. Located along multi-lane arterial roads or highway interchanges with direct truck access. Zoned industrial or light industrial.

**What is nearby:**
- Hardware anchors (Home Depot, Leroy Merlin, OBI, Bauhaus class) — building trades supply
- Auto-parts retailers (AutoZone, O'Reilly, Halfords) — vehicle maintenance for the fleet
- Tool rental branches (United Rentals, Sunbelt, Loxam, Kiloutou) — equipment for fit-outs
- Industrial MRO distributors (Würth, Fastenal, Grainger, Hilti) — fasteners, tools, consumables
- Flooring and tile supply (Floor & Decor, Topps Tiles) — finishing materials, contractor supply
- Lumber and building materials (84 Lumber, Builders FirstSource) — structural supply

**What is NOT nearby:** grocery hypermarkets, lifestyle anchors (IKEA), price clubs (Costco/Sam's Club in their consumer role). A VWH zone is defined partly by the *absence* of grocery-anchored retail.

## Site selection signals

**Essential — required for a viable VWH site:**

| Signal | Threshold | Rationale |
|---|---|---|
| Highway interchange | ≤2 km | Trucks cannot use local residential roads for daily bulk delivery |
| Industrial landuse neighbours | Adjacent or within 500 m | Zoning compatibility; existing logistics ecosystem |
| Labour catchment | 300,000+ population / 30-min drive | Manufacturing and logistics roles require accessible workforce |
| Freight rail access | ≤2 km (where available) | Just-in-time component delivery; bulk raw material |

**Significant — value-add:**

| Signal | Threshold | Rationale |
|---|---|---|
| Air cargo airport | ≤20 km | Electronics components, rapid replenishment |
| Logistics hub (FedEx/UPS/DHL/Amazon) | ≤5 km | Shared last-mile infrastructure |
| Transit corridor | ≤500 m | Workers without vehicles need bus/rail access |
| Power substation | ≤2 km | Robotics and electronics manufacturing: heavy electrical load |

**Disqualifying:**
- Dense residential immediately adjacent (truck traffic conflict, planning restrictions)
- Flood plain (capital investment at risk; insurance prohibitive)
- Heritage or environmentally protected area (height and access restrictions)
- Inside an existing [[professional-centres|Professional Centres (PRO)]] cluster (wrong land use; grocery retail adjacent)

## Production dataset

The VWH production pipeline uses DBSCAN-based clustering of hardware, trade-supply, and light-industrial retail chains. Calibration uses existing hardware store locations as proxy anchors: a calibrated build must place hardware anchors within 3 km of at least 73% of T1 and T2 clusters. The June 2026 build met this threshold.

**6,368 clusters** across 17 display countries as of the June 2026 calibration:

| Tier | Count | Share |
|---|---|---|
| T1 Full Trade Hub | 852 | 13.4% |
| T2 Established Trade | 1,327 | 20.8% |
| T3 Emerging | 4,189 | 65.8% |

Country distribution (top eight by cluster count): US · DE · GB · CA · FR · NL · IT · PL.

T3 represents the majority because single-category hardware clusters qualify as thin VWH sites. Full trade hubs combining hardware, MRO industrial, tool rental, and auto parts are genuinely rare — this T3-heavy distribution reflects real-world site rarity at the T1 level.

## Tier classification

VWH tiers use a **group-collapse model**: tier assignment is based on the number of distinct trade-supply category groups present in a cluster, not the total member count. A cluster with many hardware stores but no other trade categories does not qualify for T1; diversity across distinct trade categories is what matters.

**T1 Full Trade Hub:** At least two distinct trade-supply groups present — for example, hardware plus MRO industrial supply, or hardware plus tool rental. This indicates a genuine contractor and logistics ecosystem, not a single-category commercial strip.

**T2 Established Trade:** Hardware anchor with at least one secondary trade-supply category (auto parts, building materials, or flooring).

**T3 Emerging:** Hardware anchor present without additional trade-supply co-location. Single-category thin VWH sites.

## The retail contamination flag

Nearly half of VWH clusters have a grocery hypermarket within 1 km. Hypermarkets do appear near industrial and warehouse districts at the urban fringe, particularly in Europe where industrial parks and retail parks often share access roads. Rather than excluding these mixed-use sites, the production dataset flags them with a `retail_contamination` indicator, noting that the site has grocery-anchor proximity.

A flagged site is not disqualified as a VWH location, but site selection analysis should account for the retail traffic and zoning dynamics that come with grocery-anchor proximity — these are mixed-use zones, not pure industrial precincts.

## Data collection plan

### Priority additions — Tier A chains (definitive VWH signal)

| Chain | Market | Notes |
|---|---|---|
| Floor & Decor | US | Warehouse-format contractor flooring |
| Topps Tiles | UK | Contractor tile retail in industrial estates |
| United Rentals | NA | Deliberately co-locates next to hardware anchors |
| Sunbelt Rentals | NA | Same strategy; never in grocery parks |
| Loxam | EU | Tool rental; industrial estates |
| Kiloutou | FR | Tool rental |
| Würth | EU | MRO distributor; present in every EU industrial park |
| Fastenal | NA | Industrial MRO; always industrial-zoned |
| Grainger | NA | Industrial MRO |
| Hilti | EU | Precision tools; Hilti Centers in industrial parks |
| 84 Lumber | US | Lumber yards are definitionally industrial fringe |
| Builders FirstSource | US | Lumber/building materials B2B |

### Taxonomy categories needed

`flooring`, `tool_rental`, `mro_industrial`, `lumber`, `plumbing`, `electrical` — these enrich VWH cluster member arrays but do not gate T1/T2/T3 tier logic.

## References

- [Warehouse](https://en.wikipedia.org/wiki/Warehouse) — Wikipedia, accessed 2026-06-14
- [Retail park](https://en.wikipedia.org/wiki/Retail_park) — Wikipedia, accessed 2026-06-14

*Chain location data used to derive VWH cluster centroids is sourced from OpenStreetMap contributors and licensed under the Open Database Licence (ODbL). OpenStreetMap data © OpenStreetMap contributors.*
