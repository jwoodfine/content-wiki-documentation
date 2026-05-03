---
schema: foundry-doc-v1
title: "Architecture — Category Landing"
slug: _index
category: architecture
status: pre-build
last_edited: 2026-04-29
editor: pointsav-engineering
---

## Architecture

This category covers the design principles, substrate patterns, and cross-cutting invariants that govern how the PointSav platform is built. Architecture articles describe the logical structure of the system — how rings compose, how properties compound across deployments, how editorial and AI-routing layers are coordinated, and why the design choices are durable at the scale of a decade.

The platform is organised around a three-ring stack: Ring 1 handles per-tenant boundary ingest, Ring 2 provides deterministic knowledge and processing, and Ring 3 adds optional AI inference. Architecture articles explain what each ring does, how they interoperate, and the invariants that must hold across all three. Articles in this category are written for engineers and technical readers who need to understand the platform at depth before building on it or extending it.

## Articles in this category

- [[compounding-substrate]] — The five structural properties of the Compounding Substrate and the value-chain inversion they produce.
- [[3-layer-stack]] — The three-ring architecture: boundary ingest, knowledge and processing, and optional intelligence.
- [[apprenticeship-substrate]] — How every operational interaction generates training signal that compounds across deployments.
- [[citation-substrate]] — The machine-readable citation graph that links every published claim to its evidential source.
- [[customer-hostability]] — The design properties that allow a customer to host the full stack on their own hardware.
- [[decode-time-constraints]] — Inference-time constraints applied at the boundary to enforce compliance and safety without post-processing.
- [[design-system-substrate]] — The visual and component substrate that keeps UI consistent across the platform's applications.
- [[disclosure-substrate]] — The continuous-disclosure architecture that produces BCSC-compliant output as a structural property.
- [[language-protocol-substrate]] — The four-family adapter taxonomy that routes editorial work through a shared linguistic air-lock.
- [[reverse-funnel-editorial-pattern]] — The pipeline by which cluster drafts are refined and published to the documentation wiki.
- [[substrate-native-compatibility]] — How the substrate maintains compatibility across tenant deployments without a compatibility layer.
- [[trajectory-substrate]] — The session-trajectory capture mechanism that feeds the continued-pretraining path.
- [[worm-ledger-architecture]] — The four-layer WORM ledger that satisfies SEC 17a-4(f) and eIDAS requirements by structure.
- [[anti-homogenization-discipline]] — The editorial discipline that prevents AI-generated content from converging to a single voice.
- [[capability-based-security]] — Capability-based security as the foundation of the ToteboxOS isolation model.

<!-- ENGINE: this list is editorial in iteration-1; iteration-2+
generates it from category-directory file listing once PL.7
chunked-migration moves articles into category subdirectories. -->

## See also

- [Wiki home](/)
- [Systems](/systems/)
- [Services](/services/)
- [Governance](/governance/)

<!-- EDITORIAL NOTE: PL.7 chunked normalization sweep will migrate
     root-prefixed TOPICs into this category subdirectory. Until
     migration lands, the existing root TOPICs render at their current
     URLs (topic-<slug>.md); this landing references them by current slug. -->
