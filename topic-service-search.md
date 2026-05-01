---
schema: foundry-doc-v1
title: "service-search: Inverted Index"
slug: topic-service-search
category: services
type: topic
quality: complete
short_description: "service-search is the Ring 2 full-text search service built on the Tantivy Rust library, providing microsecond retrieval across millions of files through a static binary inverted index that requires no active database process."
status: pre-build
last_edited: 2026-04-30
editor: pointsav-engineering
cites: []
paired_with: topic-service-search.es.md
---

# service-search: Inverted Index

> service-search is the Ring 2 full-text search service built on the Tantivy Rust library, providing microsecond retrieval across millions of files through a static binary inverted index that requires no active database process.

**service-search** is a Ring 2 knowledge-and-processing service in the PointSav three-ring architecture. It provides full-text search across the platform's document archive through a static binary inverted index built in Rust using the Tantivy library. Because the index is a static binary structure rather than a live database, the entire search index can be copied to portable media and queried on any machine without additional software dependencies. The service guarantees compliance with the DARP (Data Archive and Retrieval Protocol) standard.

## Overview

An inverted index works by building a compressed map from every word in the corpus to the list of documents that contain it — analogous to the index at the back of a reference book. At query time, the service looks up the query terms in this map and returns matching documents in microseconds, regardless of corpus size. Tantivy, the underlying Rust library, is designed for high-throughput indexing and low-latency retrieval on commodity hardware.

## Ring and Role

service-search occupies **Ring 2 — Knowledge and Processing** in the three-ring architecture. Ring 2 is multi-tenant via `moduleId` namespacing and operates deterministically without AI inference. service-search's role within Ring 2 is retrieval: it answers queries against the indexed corpus and returns ranked document references that Ring 2 or Ring 3 services use for downstream processing. The service does not generate content or classify documents — it locates them.

## Architecture

The index is built as a static binary file. Key architectural properties:

- **No active process required for queries.** The index is memory-mapped at query time; there is no database daemon to manage or restart.
- **Portable.** The index file can be copied to USB storage or a different machine and queried immediately.
- **Compressed.** Tantivy's index format uses block-maximal encoding for term frequency data, keeping the index compact relative to corpus size.
- **Updatable.** New documents are added to the index via a background indexing process that merges new segments. Queries can run against existing segments while new segments are being built.

The service is integrated with `app-workplace-presentation` for interactive search in the workplace application and with the system contracts layer for programmatic retrieval.

## Configuration

| Parameter | Purpose |
|---|---|
| Index path | Filesystem path for the Tantivy index directory |
| Schema | Field definitions for indexed documents (title, body, date, category, moduleId) |
| Merge policy | Segment merge configuration controlling index compaction frequency |
| Writer threads | Number of indexing threads for parallel document ingestion |

## See Also

- [[topic-service-extraction]]
- [[topic-service-slm]]
- [[topic-service-people]]
- [[topic-trajectory-substrate]]

## References

- DOCTRINE.md §XI — Ring 2 knowledge-and-processing architecture
- `pointsav-monorepo/service-search/` — implementation crate
- Tantivy documentation — <https://docs.rs/tantivy/>
- DARP (Data Archive and Retrieval Protocol) — compliance requirement governing the index portability guarantee

---
Copyright © 2026 Woodfine Capital Projects Inc.
Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).
PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.