---
schema: foundry-doc-v1
title: "Full-text search"
slug: service-search
category: services
type: topic
content_type: topic
quality: complete
index_group: ring-2-knowledge-and-processing
short_description: "service-search is a designed but unbuilt Ring 2 full-text search service — a README describes a Tantivy-based inverted index, but no source code exists yet."
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-09-05
editor: pointsav-engineering
cites: []
references:
  - id: 1
    text: "Tantivy. 'Tantivy — A Full-Text Search Engine Library in Rust.' docs.rs, 2024."
    url: "https://docs.rs/tantivy/"
paired_with: service-search.es.md
---

`service-search` is a design, not yet an implementation. Its directory in the monorepo holds
only a README describing the intended service — a static, memory-mapped full-text index
built with the [[three-ring-architecture|Ring 2]] Rust library Tantivy — and no source code.
The design goal, as recorded, is retrieval that answers full-text queries across the
platform's documents without a live database process: the index is a file, so it can be
copied and queried on any machine with no server to run.

## The intended design

An inverted index maps every word in a corpus to the documents that contain it, the same
principle as the index at the back of a reference book. Tantivy is built for high-throughput
indexing and low-latency lookup on commodity hardware. [^1] The recorded design calls for the
index to sit in Ring 2 of the platform's tiered architecture — multi-tenant, deterministic,
no AI inference in the retrieval path — answering queries with ranked document references
that other services consume for downstream processing. It would not generate or classify
content, only locate it.

## What exists today

Nothing beyond the description. There is no build configuration, no source directory, and no
running service. Nothing in the platform currently depends on `service-search` for
retrieval; other services perform any full-text lookups they need directly.

## See also

- [[service-extraction]] — a Ring 2 service that would feed parsed output into this index if built
- [[service-slm]] — the Ring 3 intelligence layer that would consume ranked retrieval results
- [[service-people]] — an identity ledger whose records would form part of a future searchable corpus
