---
schema: foundry-doc-v1
title: "Inverted index"
slug: service-search
category: services
type: topic
quality: complete
short_description: "service-search is the Ring 2 full-text search service built on the Tantivy Rust library, providing microsecond retrieval across millions of files through a static binary inverted index that requires no active database process."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-15
editor: pointsav-engineering
cites: []
references:
 - id: 1
 text: "Tantivy. 'Tantivy — A Full-Text Search Engine Library in Rust.' docs.rs, 2024."
 url: "https://docs.rs/tantivy/"
paired_with: service-search.es.md
---

**service-search** answers full-text queries across millions of platform documents in microseconds, using a static binary inverted index built in Rust on the Tantivy library — and because the index is a file rather than a live database process, it can be copied to portable media and queried on any machine without additional dependencies. The service is a Ring 2 knowledge-and-processing component and conforms to the Data Archive and Retrieval Protocol (DARP) standard. It locates documents; it does not generate or classify them.

## Architectural Baseline

An inverted index works by building a compressed map from every word in the corpus to the list of documents that contain it — analogous to the index at the back of a reference book. At query time, the service looks up the query terms in this map and returns matching documents in microseconds, regardless of corpus size. Tantivy, the underlying Rust library, is designed for high-throughput indexing and low-latency retrieval on commodity hardware. [^1]

## Ring and Role

service-search occupies **Ring 2 — Knowledge and Processing** in the three-ring architecture. Ring 2 is multi-tenant via `moduleId` namespacing and operates deterministically without AI inference. service-search's role within Ring 2 is retrieval: it answers queries against the indexed corpus and returns ranked document references that Ring 2 or Ring 3 services use for downstream processing. The service does not generate content or classify documents — it locates them.

## Structural Organization of Components

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

## See also

- [[service-extraction]]
- [[service-slm]]
- [[service-people]]
- [[trajectory-substrate]]

