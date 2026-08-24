---
schema: foundry-doc-v1
title: "service-extraction — the DataGraph ingestion pipeline"
slug: service-extraction
category: services
type: topic
content_type: topic
quality: complete
index_group: ring-2-knowledge-and-processing
short_description: "service-extraction watches a directory for incoming JSON payloads carrying edge-classified entities, writes a per-payload ledger record for the target service, and can bridge the same text into the DataGraph ingestion pipeline."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-08-24
editor: pointsav-engineering
cites: []
paired_with: service-extraction.es.md
---

`service-extraction` watches a directory for incoming JSON payloads and turns each one into a durable ledger record. Unlike a Ring-2 component that classifies data itself, it consumes entities that have already been classified — its input payload carries an `edge_entities` field, populated by local WASM-based AI inference before the payload ever reaches this service.

## The watch-and-write cycle

Running as a filesystem watcher, the service picks up each new JSON file dropped into its watch directory, keyed by a `worm_id` derived from the filename. For each payload:

1. It reads the pre-classified `edge_entities` and builds a set of graph-ready entities from them.
2. It writes those entities to a `CRM_<worm_id>.json` ledger record, filed under the target service named in the payload itself — the target isn't fixed to one downstream service, it's whatever the payload specifies.
3. If a corpus-emission path is configured, it also writes a second, separate `CORPUS_<worm_id>.json` file carrying the payload's raw text — a bridge file that [[service-content]] watches independently, feeding that text into its own tiered entity-extraction pipeline for the knowledge graph.

The two outputs serve different purposes: the CRM ledger is the structured-entity record for the payload's own target service, and the CORPUS bridge is what lets the same text also feed the platform's general knowledge graph, without this service needing to know anything about how that extraction happens downstream.

## What it doesn't do

This service doesn't run its own AI classification — the `edge_entities` it consumes arrive already labelled. It doesn't parse binary document formats (PDF, DOCX, XLSX) — that's a separate, dedicated pipeline. And it doesn't hold a general-purpose routing matrix keyed by content type; each payload simply names its own target service.

## See also

- [[service-content]] — watches the CORPUS bridge files this service emits and runs its own tiered extraction on the text
- [[service-people]] — a common target service for CRM ledger records this service writes
- [[service-email]] — a typical upstream source of the JSON payloads this service watches for
