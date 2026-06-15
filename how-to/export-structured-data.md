---
schema: foundry-doc-v1
title: "How to export structured data from the platform"
slug: export-structured-data
category: how-to
content_type: how-to
type: how-to
status: active
last_edited: 2026-06-14
editor: pointsav-engineering
paired_with: export-structured-data.es.md
---

The platform stores data at multiple layers — raw ledger tiles, entity records in the DataGraph, wiki content, and location intelligence datasets. Exporting that data means choosing the right layer for your use case and the appropriate export format. This guide covers the four main export paths and when to use each.

For the layered data model, see [[service-content]]. For the underlying ledger storage, see [[service-fs-architecture]].

## Prerequisites

- A paired device with appropriate tier access (INPUT for ledger; USER for read-only exports)
- An active Totebox session (see [[open-first-totebox-session]])
- Knowledge of which data layer you are targeting

## Export path 1: Entity data from the DataGraph

Use this when you need structured records about people, organisations, projects, or services.

Call `query_datagraph` to identify the entity, then call `get_entity_context` to retrieve the full entity profile. The returned JSON object is the authoritative entity record. Copy or pipe it to your destination system.

For bulk exports, the `service-fs` API provides a `read_since` operation that returns entity-linked records from the ledger in chronological order.

## Export path 2: Wiki articles as Markdown

Use this when you need article content for downstream publication, processing, or indexing.

Wiki articles are plain Markdown files with YAML frontmatter, stored in the `media-knowledge-*` git repositories. Export them by reading the files directly, or by using the knowledge instance's export endpoint if it is configured:

```
GET /export/<category>/<slug>
Accept: text/markdown
```

The response is the raw Markdown file including frontmatter. No authentication is required for content marked `audience: vendor-public`.

## Export path 3: Location intelligence datasets as GeoJSON

Use this when you need cluster or archetype spatial data for GIS applications.

The GIS gateway serves pre-built GeoJSON files at:

```
GET /data/archetype-<name>.geojson
```

Where `<name>` is one of: `vwh` (Vertical Warehouse), `pks` (Parking Structures), or the main cluster file. These files include tier classifications, co-location signal fields, and enrichment attributes.

For the data schema and field definitions, see [[pointsav-gis-engine]].

## Export path 4: Ledger tiles for audit

Use this when you need tamper-evident records for compliance, legal discovery, or third-party audit.

Use the `service-fs verify` CLI or the `read_since` API to export C2SP tlog-tiles:

```
service-fs export --from <checkpoint-id> --format tlog-tiles --out <output-file>
```

The resulting file is plain text, verifiable with a SHA-256 utility, and readable without any PointSav tooling. See [[verify-worm-ledger]] for the verification procedure.

## Choosing the right path

| What you need | Use export path |
|---|---|
| Information about a named entity (person, project, service) | 1 — DataGraph |
| Article content for publishing or indexing | 2 — Wiki Markdown |
| Spatial cluster data for a map application | 3 — GeoJSON |
| Tamper-evident records for compliance or audit | 4 — Ledger tiles |

## Key takeaways

- The DataGraph is the right path for named entity data — it holds verified, current records
- Wiki Markdown exports include frontmatter; strip it or process it before sending to downstream consumers that expect plain prose
- GeoJSON files are pre-built and served statically; they update when the nightly rebuild runs
- Ledger tile exports are self-verifying with a SHA-256 utility; no live service is needed after export

## See also

- [[service-content]] — the Gravity Engine and the five-layer data model
- [[service-fs-architecture]] — the WORM ledger that stores the raw record layer
- [[verify-worm-ledger]] — how to verify the integrity of an exported ledger tile
- [[pointsav-gis-engine]] — the GIS engine and its data schema
- [[query-the-datagraph]] — how to look up entity data before exporting
