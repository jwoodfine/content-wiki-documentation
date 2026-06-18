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
last_edited: 2026-06-18
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

The VWH detection pipeline is production-grade as of 2026-06-11. Hardware stores (10,338 locations across 45 chains) were profiled as proxy anchors; DBSCAN was run on trade-supply POIs without the hardware anchor (held-out validation); tier rules were calibrated using group-collapse logic and validated against hardware co-location (73.4% of T1+T2 clusters have a hardware store within 3 km — above the 55% acceptance threshold).

**6,368 clusters** identified globally across 17 display countries:

| Country | Clusters | Notes |
|---|---|---|
| US | 3,167 | Home Depot / Lowe's / Menards + MRO + auto parts |
| DE | 648 | OBI / Hornbach / Hagebaumarkt + Würth + Bauking |
| GB | 543 | B&Q / Wickes + Screwfix / Toolstation + Travis Perkins |
| CA | 506 | Home Depot / Home Hardware + Fastenal + Princess Auto |
| FR | 420 | Castorama / Leroy Merlin + Loxam / Kiloutou + Point-P |
| NL | 240 | Praxis / Gamma + Boels Rental |
| IT | 226 | Leroy Merlin + Rexel |
| PL | 171 | Leroy Merlin / Castorama + Fastenal |

Tier distribution: T1 (Full Trade Hub) = 852 (13.4%), T2 (Established) = 1,327 (20.8%), T3 (Emerging / Thin) = 4,189 (65.8%). T3-heavy is expected: most hardware store locations are thin VWH sites; full trade hubs (MRO + tool rental + builders merchant + auto parts) are legitimately rare.

## Tier classification

VWH tiers use a **group-collapse model**: tier assignment is based on the number of distinct trade-supply category groups present in a cluster, not the total member count. A cluster with many hardware stores but no other trade categories does not qualify for T1; diversity across distinct trade categories is what matters.

**T1 Full Trade Hub:** At least two distinct trade-supply groups present — for example, hardware plus MRO industrial supply, or hardware plus tool rental. This indicates a genuine contractor and logistics ecosystem, not a single-category commercial strip.

**T2 Established Trade:** Hardware anchor with at least one secondary trade-supply category (auto parts, building materials, or flooring).

**T3 Emerging:** Hardware anchor present without additional trade-supply co-location. Single-category thin VWH sites.

The T1/T2/T3 tier labels used here are shared with the other Location Intelligence archetypes. For the general tier vocabulary, see [[colocation-tier-nomenclature]].

## The retail contamination flag

Nearly half of VWH clusters have a grocery hypermarket within 1 km. Hypermarkets do appear near industrial and warehouse districts at the urban fringe, particularly in Europe where industrial parks and retail parks often share access roads. Rather than excluding these mixed-use sites, the production dataset flags them with a `retail_contamination` indicator, noting that the site has grocery-anchor proximity.

A flagged site is not disqualified as a VWH location, but site selection analysis should account for the retail traffic and zoning dynamics that come with grocery-anchor proximity — these are mixed-use zones, not pure industrial precincts.

## Chain taxonomy

All chains below are ingested and active in the production pipeline as of 2026-06-11.

### TRADE chains (gate T1/T2 tier logic via group-collapse rules)

| chain_id | Chain | Category | Market |
|---|---|---|---|
| `wurth-de` | Würth | `mro_industrial` | EU-wide |
| `fastenal-us`, `fastenal-ca` | Fastenal | `mro_industrial` | NA |
| `grainger-us` | Grainger | `mro_industrial` | NA |
| `hilti-ch` | Hilti | `mro_industrial` | EU |
| `princess-auto-ca` | Princess Auto | `mro_industrial` | CA |
| `floor-decor-us` | Floor & Decor | `flooring` | US |
| `topps-tiles-uk` | Topps Tiles | `flooring` | UK |
| `united-rentals-us` | United Rentals | `tool_rental` | NA |
| `sunbelt-rentals-us` | Sunbelt Rentals | `tool_rental` | NA |
| `loxam-fr` | Loxam | `tool_rental` | EU |
| `kiloutou-fr` | Kiloutou | `tool_rental` | FR |
| `boels-rental-nl` | Boels Rental | `tool_rental` | NL/EU |
| `hss-hire-uk`, `speedy-hire-uk` | HSS Hire / Speedy | `tool_rental` | UK |
| `travis-perkins-uk`, `jewson-uk`, `selco-uk` | Travis Perkins / Jewson / Selco | `builders_merchant` | UK |
| `point-p-fr`, `bigmat-fr` | Point-P / BigMat | `builders_merchant` | FR |
| `bauking-de`, `raab-karcher-de` | Bauking / Raab Karcher | `builders_merchant` | DE |
| `screwfix-uk`, `toolstation-uk` | Screwfix / Toolstation | `trade_counter` | UK |
| `cef-uk` | City Electrical Factors | `electrical` | UK |
| `rexel-fr` | Rexel | `electrical` | EU |
| `ahlsell-se` | Ahlsell | `electrical` | SE |
| `ferguson-us` | Ferguson | `plumbing` | NA |
| `wolseley-uk` | Wolseley | `plumbing` | UK |

### AUTO chains (combine with TRADE for T2; alone = T3)

| chain_id | Chain | Category | Market |
|---|---|---|---|
| `autozone-us`, `oreilley-auto-us`, `napa-us` | AutoZone / O'Reilly / NAPA | `auto_parts` | NA |
| `atu-de` | ATU | `auto_parts` | DE |
| `norauto-fr` | Norauto | `auto_parts` | FR |
| `halfords-uk` | Halfords | `auto_parts` | UK |

### SUPPORT chains (informational — never gate tier)

| chain_id | Chain | Category | Market |
|---|---|---|---|
| `sherwin-williams-us` | Sherwin-Williams | `paint` | NA |
| `comex-mx` | Comex | `paint` | MX |
| Various self-storage | U-Haul, Public Storage, Shurgard, Big Yellow, etc. | `self_storage` | NA/EU |

### Not ingested (low OSM coverage; excluded from calibration)

| Chain | Category | Reason |
|---|---|---|
| 84 Lumber, Builders FirstSource, Kent Building Supplies | `lumber` | 0.9% co-occurrence with hardware anchors — below structural signal threshold |
| BOC UK | `welding` | 0.3% co-occurrence — 12 POIs only; insufficient signal |

## Related Research

A companion academic study, *Industrial Co-location in the Metropolitan Ring: Spatial Signatures of the Urban Fringe Archetype Across Eighteen Countries*, is in preparation for intended submission to Regional Science and Urban Economics (Elsevier). The study applies the Vertical Warehouse archetype proxy criterion across eighteen countries using OpenStreetMap point-of-interest data and formalises the grocery-absence and hardware-presence co-location signal at continental scale.

## References

- [Warehouse](https://en.wikipedia.org/wiki/Warehouse) — Wikipedia, accessed 2026-06-14
- [Retail park](https://en.wikipedia.org/wiki/Retail_park) — Wikipedia, accessed 2026-06-14

## Data Sources

Map and location data © [OpenStreetMap contributors](https://www.openstreetmap.org/copyright) / [ODbL](https://opendatacommons.org/licenses/odbl/).
