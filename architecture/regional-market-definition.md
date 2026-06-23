---
schema: foundry-doc-v1
title: "Regional market definition"
slug: regional-market-definition
category: architecture
type: concept
content_type: topic
quality: complete
status: stable
bcsc_class: public-disclosure-safe
language: en
last_edited: 2026-06-23
editor: pointsav-engineering
paired_with: regional-market-definition.es.md
cites: []
---

The Woodfine location intelligence map organises co-location clusters into two spatial containers: the **settlement with co-location presence** (a coverage statistic) and the **Regional Market** (a tighter object reserved for settlements with meaningful concentrations of co-located retail). A third, coarser container — the **Metro Market** — provides context at the major-metropolitan level. This article defines each object, states the rule that produces it, and distinguishes between what each count measures and what it does not.

## The two objects currently called Regional Markets

The pipeline resolves each co-location cluster to an incorporated municipal or CSD polygon using `RegionEngine.resolve_market()` — a point-in-polygon assignment against TIGER 2023 places for the US, GISCO LAU 2021 plus GADM GBR for the EU and UK, with rural co-locations resolving to their containing municipality. A settlement becomes a Regional Market object the moment **one** co-location falls inside its polygon.

Under this permissive rule, the count of Regional Market objects approximates the count of distinct settlements that contain any co-location at all. At the 2026-05-22 build, the pipeline produces approximately **3,011 settlements** (North America and EU/UK) with co-location presence, of which **2,986** are published in the gateway's `regional-markets.json` and **2,942** carry the high-confidence geocoding flag.

That is a coverage statistic. It records how widely the tracked anchor chains are observed. It does not identify where retail demand actually concentrates, because a floor of one co-location admits every town with a single qualifying co-location on exactly the same terms as a metropolitan area with dozens.

## The distinction: coverage versus market

Two failure modes follow from conflating coverage with market:

**Single-anchor settlements dominate the population.** A town with one qualifying co-location is, under the current rule, the same object class as a metro holding many. The label "Regional Market" implies concentrated retail demand; the rule admits the single-anchor case. The headline count is therefore inflated by exactly the cases that carry the least decision value for site selection or investment.

**The count reads as an artefact of the floor, not the geography.** A reviewer can move the count up or down simply by arguing the floor, which is the classic sign that the threshold — not the data — is doing the work. This is the same failure class as the DBSCAN parameter sensitivity documented in [[co-location-tiering-scoring]], where parameter sweeps move the North American cluster count across a wide range without any change to the underlying retailer data.

`mkt_conf` does not resolve this. It is geocoding precision — specifically the quality of the boundary assignment — not market quality, and must not be presented as a ranking or a quality signal.

## Recommendation: split the objects

The recommended response is to maintain both objects but distinguish them clearly by name:

### Settlement with co-location presence

- **Definition.** Any incorporated municipal or CSD polygon that contains at least one co-location.
- **Count.** The full approximately 3,011 (NA plus EU/UK). Stated as a coverage statistic with the honest gloss: *"3,011 settlements across 13 countries contain at least one observed retail co-location."*
- **Role.** Coverage map, footprint claim, and the base set from which the tighter object is drawn. Not the headline market count.

### Regional Market

A settlement is promoted to Regional Market only when it clears a stated floor. Two candidate floors are on the table:

**Floor option 1 — composition.** A Regional Market contains a minimum number of co-locations within its polygon. A floor of two immediately excludes every single-anchor settlement; a floor of three aligns the term with the intuition that a market is a place where multiple retail nodes cluster. This floor is the cheapest to compute — the co-location counts already exist per polygon — and the easiest to defend.

**Floor option 2 — demand threshold.** A Regional Market clears a stated catchment population or estimated annual spend threshold. This is more defensible analytically — it ties the term to demand rather than supply density — but it depends on the catchment and spend surfaces being trustworthy first. Adoption of this floor is appropriate once those surfaces carry their uncertainty framing (see [[spend-population-provenance]] and [[trade-area-methodology]]).

The recommended sequencing is to adopt a composition floor now, because it is computable from current outputs and immediately defensible, and to state the intention to migrate to a demand threshold once the catchment and spend surfaces clear their own revisions. Whichever floor is chosen, **the resulting Regional Market count must be re-derived and published alongside the floor** — for example, "under a floor of two co-locations, NA and EU/UK contain X Regional Markets out of 3,011 settlements with co-location presence." The count is not meaningful without the floor printed next to it.

If the floor is not raised, the minimum acceptable change is renaming: dropping "Regional Market" for the permissive object and calling it "settlements with co-location presence" on the map face, in the Method modal, and in this TOPIC. The term "market" carries an implied claim of concentrated demand that the one-co-location rule does not support.

## The Top-400 co-locations

The Top-400 is a list of co-locations (not Regional Markets) produced per region — North America as one region, Europe (UK, Nordics, Continental) as another — cut at 400. Each row carries a Regional Market column for context. It is the spine of the BentoBox detail view, where the rank shown is a continental-cutoff position.

The list is published and ranked, but the **ranking variable is not currently stated** anywhere on the map face or in the documentation. A reader cannot tell whether position 1 means most co-located chains, largest catchment population, highest estimated spend, or tightest cluster. A ranked list with an unstated sort key is not defensible for a site-selection or investment audience.

The recommendation is to publish one ranking variable and one tie-break, in plain language, in the Method modal and in this article. Candidate options in increasing order of defensibility:

- **Co-location depth (anchor count).** Honest, computationally inexpensive, already available, but weak as a "best markets" claim — it ranks supply density, not demand. If used, the list is labelled accordingly: *"ranked by number of co-located anchor chains,"* never "top markets."
- **Modelled catchment population** (WorldPop 2026, H3 resolution 7). A demand quantity, but inherits the catchment-model caveats until those are resolved.
- **Estimated annual catchment spend** (population × per-capita multiplier). The strongest "market" framing, but chains three layers of estimation and must ship with the per-capita assumption and error framing stated.
- **A composite explainable score** (population, spend, and accessibility, with the top drivers shown per site). This is the direction the scorecard work is heading and is the most defensible long-term, but it must be published as an explainable score — drivers visible — not a black box.

The recommended sequencing is to state the current ranking variable honestly today and declare the intended migration to a demand-based or composite score as the catchment, spend, and scoring revisions land. A cutoff of exactly 400 is a presentation choice and is labelled as one rather than implied to be a natural break in the data.

## Metro Market

The Metro Market is a coarser, contextual container: a major metropolitan area on a published reference list (US MSA/CBSA, Canadian CMA). A Regional Market nests inside at most one Metro Market and is never dissolved into it. Metro Market is context only — it is never the co-location or ring zoom level and never a breadcrumb level. Raising the Regional Market floor does not affect the Metro Market layer.

## What does not change

The boundary resolution rule — Sherwood Park resolves to its containing polygon (Strathcona County) under the uniform "one rule, no exceptions" boundary policy confirmed 2026-05-22 — is not altered by any floor change. The deleted Nominatim override for that settlement is not reinstated.

One wiki TOPIC per Regional Market (on projects.woodfinegroup.com) remains the article unit, with a section per co-location inside it. Raising the Regional Market floor reduces the number of stub TOPICs — single-anchor settlements no longer generate a thin market article — which is a content-quality improvement.

## Counts stated honestly

Every count below is reported with the rule that produced it. Figures are as of the most recent build referenced in the artifact registry and must be re-derived whenever the floor or the boundary set changes.

| Object | Rule | Count | What it measures |
|---|---|---|---|
| Settlements with co-location presence | ≥1 co-location in polygon | ~3,011 (NA + EU/UK) | Coverage and footprint |
| Regional Markets (proposed, floor of 2) | ≥2 co-locations in polygon | To be re-derived on adoption | Concentrated co-location |
| Published RM objects (gateway) | Current permissive rule | 2,986 (2,942 high-confidence) | Coverage; geocoding quality |
| Top-400 co-locations (per region) | Top 400 by a stated variable | 400 NA + 400 EU | Ranked candidate sites |
| NA co-locations (DBSCAN) | eps/minPts/IoU — sensitive | 226–476 across parameter sweep | Cluster count (descriptive) |

Two honesty notes belong in the Method modal alongside this table:

- The Regional Market count under any raised floor will be lower than 3,011, and that is the point — the lower, tighter number is the more defensible market count, not a regression.
- `mkt_conf` is geocoding precision, not market quality, and is not a ranking variable.

## See also

- [[co-location-tiering-scoring]] — how tiers and the planned strength score are computed for each co-location inside a Regional Market
- [[trade-area-methodology]] — how the trade area for each co-location is defined
- [[spend-population-provenance]] — the estimation chain for population and spend figures attributed to each co-location
- [[app-orchestration-gis]] — the orchestration layer that resolves co-locations to Regional Markets
