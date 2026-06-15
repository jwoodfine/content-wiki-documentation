---
schema: foundry-doc-v1
title: "How to connect to the OSM data pipeline"
slug: connect-osm-data-pipeline
category: how-to
content_type: how-to
type: how-to
status: active
last_edited: 2026-06-14
editor: pointsav-engineering
paired_with: connect-osm-data-pipeline.es.md
---

The platform's location intelligence system ingests point-of-interest (POI) data from OpenStreetMap via JSONL ingest files. Connecting to the OSM data pipeline means writing or adapting an ingest script that queries the Overpass API, producing a JSONL file in the platform's schema, and registering the ingest with the taxonomy configuration. This guide covers a single-chain ingest for a new retail or service category.

For the GIS engine architecture, see [[pointsav-gis-engine]]. For building a map from ingested cluster data, see [[build-a-colocation-map]].

## Prerequisites

- Access to the `app-orchestration-gis` working directory (the pipeline scripts)
- Python 3.9+ with `requests` available
- Network access to the Overpass API (`overpass-api.de` or a local mirror)
- A Wikidata Q-ID for the chain or category being ingested (look up at `wikidata.org`)

## Step 1: Identify the Wikidata Q-ID

Every chain in the taxonomy is anchored to a Wikidata Q-ID. This provides a stable, language-neutral identifier for the entity. Look up the chain on Wikidata and record the Q-ID (e.g., Walmart: Q483551, IKEA: Q54078).

If the category has no single Wikidata entry, use a name-based query (`name_query` mode) rather than a Q-ID lookup.

## Step 2: Write the ingest YAML

Create an ingest YAML file under `service-business/` named `<chain-name>-<country-code>.yaml`:

```yaml
chain: walmart-us
wikidata_id: Q483551
query_mode: wikidata    # or: name_query
name_query: null         # used only when query_mode: name_query
country_code: US
bbox: [-125.0, 24.4, -66.9, 49.4]   # bounding box for the country
output: service-business/walmart-us.jsonl
taxonomy_family: ALPHA_HYPERMARKET
taxonomy_tier: 1
```

For `name_query` mode (when Wikidata coverage is sparse), set `query_mode: name_query` and provide `name_query: "Walmart"`. The ingest script performs a free-text name search in the Overpass API.

## Step 3: Run the ingest script

Run the existing ingest script with the new YAML:

```
python3 app-orchestration-gis/ingest-chain.py service-business/walmart-us.yaml
```

The script queries the Overpass API, filters results by the bounding box and country code, and writes JSONL records to `service-business/walmart-us.jsonl`. Each record contains: `name`, `lat`, `lon`, `wikidata_id`, `chain`, `country`, `taxonomy_family`, `taxonomy_tier`.

Typical record counts: dense urban chains produce 500–2,000 records; national hypermarket chains produce 100–500; specialty retailers produce 50–200.

## Step 4: Register the chain in the taxonomy

Add the new chain to the taxonomy configuration in `app-orchestration-gis/taxonomy.py` under the appropriate family group:

```python
"walmart-us": TaxonomyEntry(
    family="ALPHA_HYPERMARKET",
    tier=1,
    jsonl_path="service-business/walmart-us.jsonl",
    wikidata_id="Q483551",
),
```

## Step 5: Rebuild the cluster layer

After registration, rebuild the cluster layer to incorporate the new POI data:

```
python3 app-orchestration-gis/build-geometric-ranking.py
```

The rebuild reads all registered JSONL files, runs the DBSCAN clustering pass, and regenerates `clusters-meta.json`. Verify the new chain appears in the cluster output:

```
python3 -c "import json; d=json.load(open('gateway/www/data/clusters-meta.json')); print(sum(1 for c in d['clusters'] if 'walmart' in str(c)))"
```

## Key takeaways

- Every chain requires a YAML ingest descriptor and a JSONL output file in `service-business/`
- Wikidata Q-IDs are preferred over name queries; fall back to name queries only when Wikidata coverage is absent
- The taxonomy registration step links the JSONL file to the clustering pipeline
- A full cluster rebuild is required after adding a new chain — incremental updates are not supported in the current pipeline

## See also

- [[pointsav-gis-engine]] — the GIS engine architecture and the DBSCAN clustering pipeline
- [[build-a-colocation-map]] — how to surface cluster data in a MapLibre web application
- [[location-intelligence-archetypes]] — the PRO/VWH/PKS archetype model that the taxonomy feeds
- [[export-structured-data]] — exporting the resulting GeoJSON for external use
