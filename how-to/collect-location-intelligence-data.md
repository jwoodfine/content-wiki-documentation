---
schema: foundry-doc-v1
title: "Location intelligence: data collection"
slug: collect-location-intelligence-data
short_description: "How new retail and infrastructure chains get added to the location-intelligence pipeline's taxonomy, and how the pipeline ingests their location data from OpenStreetMap."
category: how-to
content_type: how-to
type: how-to
quality: complete
status: active
audience: vendor-internal
bcsc_class: no-disclosure-implication
language_protocol: RUNBOOK
last_edited: 2026-07-11
editor: pointsav-engineering
paired_with: collect-location-intelligence-data.es.md
research_trail:
  sources: [pointsav-monorepo app-orchestration-gis taxonomy.py, config.py, ingest-osm.py]
  verification_method: "re-verified 2026-09-05 against app-orchestration-gis: build-vwh-clusters.py does not exist under that name; test-cluster-archetypes.py, build-clusters.py, and export-clusters-ols.py do"
---

The location-intelligence pipeline classifies retail and infrastructure locations into two archetypes — Vertical Warehouse (VWH) and Parking Structures (PKS) — by matching OpenStreetMap records against a maintained chain taxonomy. This runbook covers extending that taxonomy to a new chain, country, or infrastructure category, and re-running the ingest and clustering steps that follow.

Working directory for all commands: `app-orchestration-gis/` (inside the GIS monorepo clone).

## Prerequisites

- Overpass API access (queries run through the pipeline's OSM ingest script; no API key required)
- Python 3.11+ with pipeline dependencies installed
- The active deployment's data directory path configured

## Purpose

Add a new chain, country, or infrastructure category to the location-intelligence taxonomy, ingest its OpenStreetMap records, and re-run the clustering build so the new data is reflected in the VWH/PKS archetype outputs.

## Procedure

1. **Verify the pipeline is clean** by importing the taxonomy and config modules and confirming both load without error.

2. **Add a new chain to the taxonomy.** Each chain is declared in its own YAML record: a chain identifier, country and region, a category (mapped to a NAICS code), the retailer's canonical legal name and parent company, a public identifier used to match OpenStreetMap records (typically a Wikidata QID via the `brand:wikidata` OSM tag), and an approximate store count used only as a sanity check on ingest results — never as a tier-qualification input. A chain that spans multiple countries is flagged as such rather than duplicated per country.

3. **Register the chain's category in the taxonomy module**, if it introduces a category not already present. Each category carries a label, a NAICS code, and a note on which archetype signal it contributes (VWH or PKS) — none of these categories gate archetype-tier logic on their own; tier assignment is a separate downstream step.

4. **Run the OSM ingest for the new chain(s).** The ingest script queries Overpass for the chain's tagged locations and writes the results to the pipeline's business-data directory. If a chain returns zero records, check whether Wikidata tag coverage is sparse in OSM for that chain and add a name-based fallback query to its YAML record.

5. **For a new infrastructure category** (for example, commercial airports or intercity rail stations, as opposed to a retail chain), write a dedicated ingest script following the existing infrastructure-ingest pattern: an Overpass query scoped to the relevant `aeroway`/`railway` tags, filtered to exclude out-of-scope subtypes (private airstrips and military fields for airports; subway, light rail, and tram for railway stations), with per-country operator or IATA-code enrichment applied where the source tagging supports it.

6. **Re-run the clustering build** once all new chain and infrastructure ingests are in place, using the pipeline's DBSCAN cluster-build scripts for each archetype. Copy the outputs to the active deployment's data directory and confirm the new cluster counts are at or above the prior production baseline — a drop below the baseline indicates an ingest or taxonomy regression, not an expected result of adding data.

## Expected outcome

The new chain, country, or infrastructure category appears in the archetype's OSM ingest output with a plausible record count for its real-world scale, and the subsequent clustering build produces cluster counts at or above the pipeline's prior production baseline.

## Verification

Count the records in each newly ingested chain's output file and compare against the chain's real-world scale as a sanity check, not an exact target. Confirm the clustering build's output feature counts for VWH and PKS are at or above their last known production baseline before treating the run as complete.

## Rollback

A new chain YAML or taxonomy-category entry can be removed and the ingest re-run without side effects — the ingest step is idempotent per chain. The clustering build can be re-run at any time from its existing inputs; it does not need to be reverted, only re-run once the taxonomy correction is in place.

## Next steps

- [[connect-osm-data-pipeline]] — the generic single-chain ingest path this runbook extends

## See also

- Urban Fringe — the VWH archetype model and chain taxonomy
- Commuter — the PKS archetype model and chain taxonomy
- Location intelligence archetypes (projects.woodfinegroup.com/site-selection) — PRO/VWH/PKS overview and map integration
- [[connect-osm-data-pipeline]] — generic single-chain ingest for new retail categories
