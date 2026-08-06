---
schema: foundry-doc-v1
title: "Connect to the OSM data pipeline"
slug: connect-osm-data-pipeline
short_description: "Ingests a new retail or service chain from OpenStreetMap using the real ingest-osm.py script and taxonomy.py's CATEGORIES/BRAND_FILL dicts, then rebuilds the servable cluster tiles."
category: how-to
index_group: integration-data
content_type: how-to
type: how-to
quality: complete
status: active
audience: "Engineers (hands on keyboard); customer operators"
last_edited: 2026-08-06
editor: pointsav-engineering
paired_with: connect-osm-data-pipeline.es.md
research_trail:
  sources: [pointsav-monorepo app-orchestration-gis/ingest-osm.py, taxonomy.py, nightly-rebuild.sh (real rebuild script chain), how-to/collect-location-intelligence-data.md (the vendor-internal runbook that already exercised this exact pipeline against real chains)]
  verification_method: "grounded directly in collect-location-intelligence-data.md's own real, executed command history rather than re-deriving the pipeline from scratch, cross-checked against app-orchestration-gis's real directory listing and nightly-rebuild.sh's actual script chain on 2026-08-06; resolves a contradiction between this guide's own prior correction note and its sibling's by confirming build-clusters.py (not build-geometric-ranking.py, which only adds ranking to an existing file, and not the VWH/PKS-specific scripts) is the real generic rebuild step"
---

## Prerequisites

- Access to the `app-orchestration-gis` working directory (the pipeline scripts)
- Python 3.11+ with the pipeline's dependencies installed
- Network access to the Overpass API
- A Wikidata Q-ID for the chain you're ingesting (look it up at wikidata.org)

## Purpose

Add a new retail or service chain to the location-intelligence pipeline — from raw OpenStreetMap data to a servable cluster tile — a chain that's genuinely been run before, not a hypothetical procedure.

## Procedure

1. Look up the chain's Wikidata Q-ID. This is the stable, language-neutral identifier the taxonomy anchors to (Walmart: Q483551, IKEA: Q54078). If the chain has no clean Wikidata entry, you'll fall back to a name-based query later.

2. Run the ingest script directly against the chain's identifier — there's no separate YAML descriptor file to author for a straightforward run:

   ```bash
   python3 ingest-osm.py --chain <chain-id>
   ```

   This queries the Overpass API and writes JSONL records to the platform's data directory. If the chain returns zero records, Wikidata tag coverage may be sparse in OpenStreetMap for that chain — check whether a name-based fallback query is warranted before assuming the chain has no data.

3. Register the chain's category in `taxonomy.py`, in the `CATEGORIES` dict:

   ```python
   "your_category_slug": {
       "label": "Human-Readable Category Name",
       "naics": "<naics-code>",
       "description": "One line describing what this category signals.",
   },
   ```

4. Add the chain to `BRAND_FILL`, under its category, keyed by country code:

   ```python
   "your_category_slug": {
       "US": ["your-chain-id"],
       "CA": [],
       # ... every display country needs an entry, even if empty
   },
   ```

5. Rebuild the cluster layer and its servable tiles:

   ```bash
   python3 build-clusters.py       # rebuilds work/clusters.geojson from all registered chains
   python3 build-tiles.py --layer 2  # regenerates the PMTiles archive served to the map
   ```

## Expected outcome

The new chain's locations are present in the rebuilt cluster GeoJSON and reflected in the regenerated PMTiles archive that the map actually serves.

## Verification

Check the new chain's record count landed as expected:

```bash
grep -c '"chain":"your-chain-id"' path/to/your-chain-id.jsonl
```

Then confirm it appears in the rebuilt cluster output before treating the ingest as complete. A chain registered in the taxonomy but never actually ingested, or an ingest that ran but was never included in a rebuild, both leave the map showing stale data with no error to warn you.

## Rollback

Remove the chain's entries from `CATEGORIES`/`BRAND_FILL` and delete its JSONL file, then re-run the rebuild steps to regenerate cluster output without it. There's no in-place "undo" for a rebuild already served — the previous state is only recoverable by rebuilding again from a taxonomy that excludes the chain.

## Next steps

- [[build-a-colocation-map]] — render the rebuilt cluster tiles in a MapLibre application

## See also

- [[location-intelligence-substrate]] — the flat-file/PMTiles architecture this pipeline feeds
