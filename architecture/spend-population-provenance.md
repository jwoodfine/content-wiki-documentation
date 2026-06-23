---
schema: foundry-doc-v1
title: "Spend and population estimation: provenance and assumptions"
slug: spend-population-provenance
category: architecture
type: concept
content_type: topic
quality: complete
status: stable
bcsc_class: public-disclosure-safe
language: en
last_edited: 2026-06-23
editor: pointsav-engineering
paired_with: spend-population-provenance.es.md
cites: []
---

The Woodfine location intelligence map presents two synthesised demographic surfaces for every co-location cluster: a catchment population and an estimated annual retail spend. Both are decision-grade inputs — a site-selection analyst or a capital allocator will read them as measurements. They are not measurements. They are layered model estimates built on open data. This article documents exactly how those two surfaces are produced, what they assume, where they are weakest, and how their uncertainty is — and is not yet — communicated.

## The estimation chain

The spend figure shown on a cluster is the output of three sequential modelling steps. None of the error introduced at each step is currently propagated forward into the displayed value.

### Step 1 — Population: WorldPop dasymetric raster

Population originates from the **WorldPop 2026 100-metre gridded population product** (CC BY 4.0). WorldPop is itself a model: census counts collected at coarse administrative units are redistributed to a 100 m grid using dasymetric techniques — satellite-derived settlement extent, land cover, and ancillary covariates reallocate people from the administrative unit to the cells where they are most likely to live. The 100 m cell is a modelled allocation, not a counted population. Its error is heteroscedastic: tighter where recent, high-quality census microdata exists (most of North America and Western Europe), looser where the underlying census is older or coarser.

### Step 2 — Aggregation to H3 resolution 7

The 100 m cells are filtered to those within 150 km of a co-location cluster centroid, then summed into their containing **H3 resolution-7 hexagon** (average area approximately 5.16 km²). Catchment population is the sum of cell populations over the H3 cells whose centroids fall inside a cluster's distance rings.

### Step 3 — Spend: per-capita multiplier

Estimated annual spend is **population × a per-capita expenditure multiplier**, applied per country and per retail category (grocery, hardware, wholesale). The multipliers are proxies derived from national household-expenditure surveys — BLS Consumer Expenditure Survey for the US, Statistics Canada Household Expenditures for Canada, Eurostat Household Budget Survey for the EU member countries, and INEGI for Mexico.

### The uniform-per-capita assumption

The single most consequential simplification is: **every resident of a country is assigned the same per-capita spend, regardless of where they live.** A household in central London and a household in a Welsh market town receive the identical grocery multiplier. The model has no income, age, household-size, or cost-of-living variation below the national level.

This assumption is defensible as a baseline — it is transparent, requires only one authoritative survey per country, and does not pretend to a granularity the inputs cannot support. But it breaks in predictable ways:

- High-income metropolitan areas are systematically understated. A cluster in an affluent catchment carries the national-average multiplier and therefore reports less spend than the area actually commands.
- Lower-income regions are systematically overstated by the same mechanism.
- The error is spatially correlated, not random. Because it tracks the local income gradient, it does not cancel out across a catchment; it biases the entire trade-area total in one direction.

A future pipeline version is intended to vary the multiplier sub-nationally using local income data — US ACS median household income by tract, Statistics Canada census income, Eurostat regional income at NUTS-2/NUTS-3 — replacing the flat national constant. Until that ships, the uniform assumption holds and is stated in the Method modal.

### False-precision risk

Each step above has its own error, and they compound. The current pipeline carries no error term through any step. A spend figure is emitted and rendered as a single scalar.

The discipline that follows is therefore a presentation rule: **the map must not display false-precision figures.** A modelled spend estimate of $147,382,901 implies measurement accuracy the model does not have. Spend is shown rounded to a band the model can defend — for example "~$150M annual grocery spend" or a range — and labelled as an estimate. Catchment population follows the same rule: "~140,000 people" rather than "139,847."

### The modifiable-areal-unit problem

Both surfaces are aggregated to the H3 resolution-7 grid before catchment sums are taken. The modifiable-areal-unit problem (MAUP) is the well-established result that statistics computed over areal units change when the unit's size or boundary changes. Two consequences for this map:

- **Scale effect.** Aggregating WorldPop's 100 m cells to approximately 5.16 km² hexagons smooths the population surface. A different resolution would produce different catchment totals for the same rings, because the H3 cells intersect the distance rings differently.
- **Edge effect.** A distance ring slices through hexagons at its boundary. A cell is counted as fully in or fully out based on its centroid, so the catchment total is sensitive to exactly how the hexagon lattice falls relative to the ring.

MAUP is not a defect to be fixed; it is an inherent property of any areal aggregation. The obligation is to acknowledge it in the Method modal and to avoid over-interpreting small differences between clusters. The magnitude of the MAUP effect at resolution 7 for the distance rings in use has not yet been quantified; a sensitivity sweep across resolutions 6, 7, and 8 is a documented gap.

## Confidence and how it is shown

### What confidence already exists

The pipeline already computes a per-market **confidence flag** in `regional-markets.json`. This flag is a function of input-data quality and coverage: clusters in OSM-sparse or census-stale regions, or clusters whose anchor geometry was resolved by name-query fallback rather than an exact Wikidata brand match, are lower confidence.

At the 2026-05-22 build, 2,942 of 2,986 Regional Market objects carried the high-confidence flag. Despite this, the flag is not yet rendered anywhere — the map draws every cluster at full opacity with an identical marker, so a lower-confidence estimate is visually indistinguishable from a higher-confidence one.

### How confidence is intended to be encoded

The cartographic intention is to make confidence a visual channel on the tier dot, not buried in the modal:

- **Opacity** — lower-confidence clusters rendered at reduced fill opacity so the reader's eye is drawn to the estimates most strongly evidenced.
- **Hollow versus filled markers** — a hollow (stroke-only) dot for lower-confidence clusters and a filled dot for higher-confidence ones is an unambiguous, colour-independent encoding that survives colour-vision deficiency and does not collide with the ordinal tier ramp.

Whichever channel is adopted, it must be explained in the legend so the reader knows a faint or hollow dot means "lower confidence," not "lower tier."

## Source register

The on-map provenance line and the Data / Method modal both derive from this register.

### On-map provenance line

A persistent line on the map face, in the form:

> Data: WorldPop 2026, OSM, Kontur CC-BY — updated [build month] · Method ⓘ

OpenStreetMap attribution is a licence obligation under ODbL and remains present separately from the provenance line.

### Data sources

| Source | Role | Vintage | Licence |
|---|---|---|---|
| WorldPop | 100 m gridded population — Step 1 of the spend chain | 2026 raster | CC BY 4.0 — WorldPop (www.worldpop.org) |
| OpenStreetMap | Retail and civic POI locations defining the clusters | Continuously updated; snapshot per build | ODbL 1.0 — © OpenStreetMap contributors |
| Overture Maps — Places | Global POI theme for anchor resolution | 2026 release | CDLA-Permissive-2.0 — © Overture Maps Foundation |
| Overture Maps — Addresses | Street-address backfill for null-address POI records | Release 2026-04-15.0 | ODbL 1.0 — © Overture Maps Foundation contributors |
| Kontur Population | Auxiliary population reference (H3-native) | 2026 (HDX) | CC BY 4.0 |
| BLS Consumer Expenditure Survey | US per-capita spend multiplier proxy | Latest published | US federal public data |
| Statistics Canada — Household Expenditures | Canada per-capita spend multiplier proxy | Latest survey | StatCan Open Licence — adapted from Statistics Canada data; not an endorsement |
| Eurostat — Household Budget Survey | EU per-capita spend multiplier proxy | Latest HBS | CC BY 4.0 — © European Union, 1995–2026 |
| INEGI | Mexico spend proxy and business registry | Latest | INEGI Terms of Free Use |

### Countries covered

United States, Canada, Mexico, Great Britain, Germany, France, Netherlands, Austria, Portugal, Greece, Denmark, Iceland, and Poland — 13 countries at the current pipeline version.

### Per-capita annual spend multipliers

Multipliers are annual per-capita expenditure proxies expressed in local currency. They are Step-3 inputs and are not currency-normalised.

| Country | Grocery | Hardware | Wholesale | Currency |
|---|---|---|---|---|
| USA | $3,500 | $1,200 | $1,500 | USD |
| Canada | C$3,200 | C$1,100 | C$1,300 | CAD |
| Mexico | MX$18,000 | MX$3,500 | MX$2,500 | MXN |
| Great Britain | £2,800 | £850 | £900 | GBP |
| Germany | €2,900 | €950 | €1,000 | EUR |
| France | €3,100 | €900 | €1,000 | EUR |
| Netherlands | €2,700 | €1,000 | €1,100 | EUR |
| Austria | €3,000 | €950 | €1,000 | EUR |
| Portugal | €2,400 | €600 | €700 | EUR |
| Greece | €2,200 | €500 | €600 | EUR |
| Denmark | €3,500 | €1,200 | €1,100 | EUR |
| Iceland | €4,000 | €1,500 | €1,500 | EUR |
| Poland | PLN 8,000 | PLN 2,000 | PLN 2,500 | PLN |

**Currency note.** Because multipliers are in local currency and are not FX-normalised, cross-country spend comparisons are not directly meaningful. Rankings are most defensible within a single country or within the eurozone.

## How to read a spend or population figure

1. **Population and spend are modelled estimates, not counts.** They are built from open data and carry the errors described above.
2. **Spend assumes everyone in a country spends the same per head.** Affluent catchments are understated; lower-income catchments are overstated. Local income variation is planned but not yet applied.
3. **Figures are rounded on purpose.** A round number signals an estimate; a precise-looking number would imply false accuracy.
4. **A faint or hollow dot means lower confidence,** not a lower tier.
5. **Small differences between clusters may be grid artefacts** (MAUP), not real differences. Compare orders of magnitude, not final digits.
6. **Spend is comparable within a country, not across currencies** until FX normalisation ships.

## Status summary

| Item | State |
|---|---|
| WorldPop → H3 resolution-7 population surface | Shipped |
| Per-capita spend multipliers (13 countries) | Shipped |
| Confidence flag in `regional-markets.json` | Computed; not yet rendered |
| On-map provenance and vintage line | Planned |
| Data / Method modal with full source register and caveats | Planned |
| Confidence encoded on tier dots (opacity or hollow marker) | Planned |
| Per-estimate error propagation and ± bands | Planned |
| Sub-national income-varying spend multipliers | Planned |
| MAUP sensitivity sweep (resolutions 6, 7, 8) | Planned — gap, not yet quantified |
| FX normalisation for cross-country spend | Open question |

All forward-looking items above are stated as planned or intended; they describe the intended direction of the pipeline, not capabilities currently live on gis.woodfinegroup.com.

## See also

- [[trade-area-methodology]] — how the polygon over which population and spend are summed is defined
- [[co-location-tiering-scoring]] — how the spend figure feeds the planned strength score
- [[regional-market-definition]] — the settlement-level rollup that aggregates cluster-level figures
- [[app-orchestration-gis]] — the orchestration layer that runs the spend and population pipeline
