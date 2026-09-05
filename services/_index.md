---
schema: foundry-doc-v1
title: "Platform Services"
slug: services-index
category: services
type: topic
content_type: topic
quality: complete
short_description: "The autonomous services that implement Ring 1 boundary ingest and Ring 2 deterministic knowledge processing in the PointSav three-ring architecture — grouped by ring layer and function."
index_type: thematic
index_scope: services
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-09-04
editor: pointsav-engineering
paired_with: _index.es.md
---

PointSav's three-ring architecture assigns every service to a layer with defined authority and dependencies. Ring 1 services handle per-tenant boundary ingest — each accepts raw data from one external source and writes it to a durable ledger. Ring 2 services provide deterministic knowledge and processing: they read from Ring 1 and produce structured records, knowledge graphs, and search indexes. Ring 3 is a single service, service-slm, which reads from Ring 2 and never writes to it.

The platform functions fully across Rings 1 and 2 without AI compute — a deployment can exclude Ring 3 entirely, shrinking the attack surface and satisfying network-isolation requirements. Where Ring 3 is included, the compliance question of whether AI has touched the authoritative record is answered architecturally, not procedurally: Ring 2 services may call Ring 3 for extraction or classification proposals (`service-extraction`'s corpus hand-off to `service-content`, which calls the Doorman for grammar-constrained entity extraction into the DataGraph, is one such path), but Ring 3 never writes to the knowledge graph, the ledger, or any structured record store. Every accepted proposal enters the record only through a Ring 2 write path with a human approval checkpoint.

<!-- START-HERE-HIGHLIGHT: engine reads this block to render the single "start here" card
     (reuses the existing cluster-card--start-here component). Do not add more than one. -->

**Start here:** [[service-fs]] — the filesystem service every other Ring 1 service writes to, and the foundation of the WORM audit posture the rest of this category assumes.

<!-- END-START-HERE-HIGHLIGHT -->

## Ring 1 — Boundary ingest

Per-tenant boundary services. Each runs as a separate process per tenant and exposes a Model Context Protocol server interface.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: ring-1-boundary-ingest -->
- [[service-fs]] — The per-tenant Write-Once-Read-Many immutable ledger that backs every record written to the platform — a real, implemented HTTP and MCP interface over a hash-chained append log, with monthly external anchoring to a public transparency log.
- [[service-email]] — service-email pulls mail out of a Microsoft Exchange mailbox over EWS, writes the raw message to local storage, and deletes it from the source mailbox immediately after extraction — the cloud mailbox is a transit point, not a copy of record.
- [[service-people]] — service-people is the F2 surface in os-console — an MCP server over an append-only, WORM-backed identity ledger with three tools: append, lookup, and regex-based email scanning.
- [[service-input]] — service-input batch-migrates markdown reference material from a source archive into the platform's ingest pipeline, deduplicating by content hash and validating against each file's own ledger record — with a companion tool that scores how well downstream extraction matches that ledger.
<!-- END AUTO-GENERATED -->

## Ring 2 — Knowledge and processing

Deterministic processing services. Each reads from Ring 1 and produces structured records — no AI variance enters the authoritative record.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: ring-2-knowledge-and-processing -->
- [[service-extraction]] — service-extraction watches a directory for incoming JSON payloads carrying edge-classified entities, writes a per-payload ledger record for the target service, and can bridge the same text into the DataGraph ingestion pipeline.
- [[service-content]] — service-content extracts named entities from raw payloads through a tiered model pipeline, writes them into the knowledge graph under a human-review checkpoint, and hosts the platform's reference taxonomies.
- [[service-search]] — service-search is a designed but unbuilt Ring 2 full-text search service — a README describes a Tantivy-based inverted index, but no source code exists yet.
- [[service-egress]] — service-egress compresses and chunks local mail data for outbound transfer, and only deletes the local source once an external counterpart confirms receipt with a cryptographic proof — an outbound release valve, not a cloud-to-local import.
- [[archetypes-and-chart-of-accounts]] — The Chart of Accounts and eleven archetypes are two reference taxonomies service-content loads into the knowledge graph, giving every classified entity a structural category and a functional signature.
<!-- END AUTO-GENERATED -->

## Ring 3 — AI gateway

One service spans Ring 3. It reads from Ring 2 and produces proposals a human reviews; it never writes to the knowledge graph or the ledger.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: ring-3-ai-gateway -->
- [[service-slm]] — service-slm is the platform's AI inference gateway — every request, local or remote, transits the Doorman's audit boundary and one of three compute tiers before a response returns.
- [[service-slm-yoyo-operational]] — How service-slm's three-tier inference router and the Yo-Yo GPU burst VM operate: the Doorman boundary, the local and burst tiers, the apprenticeship queue, and the idle-shutdown cost ceiling.
- [[service-slm-totebox-sysadmin]] — A planned direction for service-slm: using its real, already-operational capture-then-verdict training pipeline to build a Totebox sysadmin assistant — the specific task taxonomy and tooling described here are not yet built.
- [[service-slm-graph-store-migration]] — service-slm's graph store runs a nightly rebuild — entity extraction via the Doorman writes directly to the graph on completion, with no human review step in the rebuild script itself.
- [[yoyo-daily-enrichment-cycle]] — The nightly two-phase GPU batch window that rebuilds the DataGraph and, once fully enabled, trains adapter weights for the local language model — currently running in DataGraph-only mode.
<!-- END AUTO-GENERATED -->

## Specialist and domain services

Services built for specific platform capabilities.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: specialist-and-domain-services -->
- [[service-business-clustering]] — A parent-child spatial pattern that turns raw retail points into one commercial entity per physical site, so the GIS pipeline reasons about a location once instead of once per co-located tenant.
- [[service-places-filtering]] — A filtering step that keeps only regional-grade institutions from raw civic data, so GIS tier rankings reflect institutional concentration rather than every clinic and community facility.
- [[service-wallet-settlement]] — service-wallet is a planned per-tenant accounting ledger for reverse-flow marketplace revenue — no code exists yet; the design calls for a non-custodial, signed-entry ledger rather than a payment rail.
- [[message-courier]] — A deliberately thin engine that dynamically loads a customer's private adapter script and hands it execution control — keeping every operational detail of a client's web-automation logic out of the open-source codebase entirely.
- [[fs-anchor-emitter]] — A one-shot binary that fetches a signed WORM-ledger checkpoint from service-fs, anchors it to the public Sigstore Rekor transparency log, and writes the resulting log entry back — making ledger state auditable from outside the platform.
- [[service-fs-data-lake]] — The GIS pipeline's data lake is its foundational storage layer — a flat-file store holding raw geospatial points, available to every downstream step in the same pipeline. Distinct from service-fs, the platform's separate WORM ledger.
- [[template-ledger]] — Distribution mechanism in service-email-template that syncs one authoritative copy of every approved template to the operator's mail environment, eliminating version drift.
- [[editorial-pipeline-three-stages]] — The real client-confirmed contract for the platform's proofreading pipeline: a fixed set of language protocols, a response that reports which compute tier ran and what degraded, and a binary human verdict that feeds the training corpus.
- [[private-git-paid-customer-endpoint]] — The binary release server behind software.pointsav.com verifies Ed25519 license tokens and streams compiled binaries — stateless, holding no payment records or keys, with some products served openly and no license check at all.
- [[service-pointsav-link]] — service-pointsav-link is a named but unbuilt adapter concept for connecting an os-* node to a PointSav fleet — no corresponding package exists in the monorepo today.
- [[service-vm-fleet]] — The fleet controller maintains a global view of node capacity across the PPN WireGuard mesh and handles placement decisions for virtual machine spawns.
- [[poi-data-schema]] — The record structures for location data ingested from OpenStreetMap and Overture Maps Foundation, normalised into a unified JSONL schema before cluster analysis. Wikidata QIDs are the primary chain identifier, and a parent-child sub-location model handles co-branded ancillary services.
- [[regional-name-resolution-architecture]] — The layered offline reverse-geocoding engine that turns a cluster's coordinates into a human-readable regional name — its boundary datasets, its country-specific routing order, and the post-processing that makes source-language names readable — with no external API calls.
- [[service-vm-tenant]] — The tenant proxy enforces authentication, namespace isolation, quota limits, and an immutable audit trail at the customer boundary of the PPN VM resource pool.
<!-- END AUTO-GENERATED -->

## See also

- [Operating Systems](/systems/) — the operating systems that services run within
- [How It's Built](/architecture/) — the three-ring model and the invariants that govern ring interaction
- [Where It Runs](/infrastructure/) — fleet deployment and the physical layer services run on
