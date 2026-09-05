---
schema: foundry-doc-v1
title: "How It's Built"
slug: architecture-index
category: architecture
type: topic
content_type: topic
quality: complete
short_description: "Cross-cutting platform architecture: the three-ring composition model, AI routing and inference boundary, security and identity substrate, customer ownership principles, and the location intelligence domain."
index_type: thematic
index_scope: architecture
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-09-04
editor: pointsav-engineering
paired_with: _index.es.md
---

PointSav is composed from three concentric rings with strict one-way dependencies, a deterministic data pipeline that runs fully without AI, and a sovereignty discipline that allows customers to fork the entire stack on day one. Architecture articles describe the structural decisions behind those properties — why they are designed the way they are, how they compose, and what invariants must hold across every deployment.

The three-ring model is the load-bearing frame: Ring 1 handles per-tenant boundary ingest, Ring 2 provides deterministic knowledge and processing, and Ring 3 adds optional AI inference that never writes to the authoritative record. Articles in this category explain the rings, the security model that enforces their boundaries, the AI routing logic, and the customer-ownership principles that govern the platform's commercial architecture.

<!-- START-HERE-HIGHLIGHT: engine reads this block to render the single "start here" card
     (reuses the existing cluster-card--start-here component). Do not add more than one. -->

**Start here:** [[three-ring-architecture]] — the load-bearing frame every other article in this category assumes: three concentric rings with strict one-way dependencies, AI structurally optional throughout.

<!-- END-START-HERE-HIGHLIGHT -->

## Platform structure

The foundational structural articles — the patterns that compose every PointSav deployment.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: platform-structure -->
- [[three-ring-architecture]] — The durable composition pattern for the platform: three concentric rings with one-way dependencies, where the AI ring is structurally optional and data flows without it.
- [[3-layer-stack]] — The Three-Layer Stack is the infrastructure decomposition pattern across PointSav deployments, separating raw compute, isolated platform execution, and secure operator access.
- [[three-layer-architecture]] — Strict one-way flow of PointSav deliverables through three layers — vendor monorepo, customer showcase catalogue, and private running instances.
- [[six-tier-sovereignty-matrix]] — Six fixed directory prefixes organising the PointSav monorepo by purpose, making the repository self-documenting and enforcing dependency hygiene by convention.
- [[foundry-doctrine-overview]] — The planned scope for PointSav's future constitutional charter — not yet ratified or written; described here in planned/intended terms only.
- [[leapfrog-2030-architecture]] — Structural positioning thesis pairing customer-owned hardware, data, and adapter weights with transactional rather than subscription revenue.
- [[pointsav-overview]] — PointSav Digital Systems is a technology vendor building sovereign, on-premise-capable operating systems for record-keeping, within a three-organisation structure.
- [[architecture]] — The platform's cryptographic consistency rests on a real Merkle-chained ledger; sovereign bootability — collapsing a deployment into one portable image — is a design goal, not yet a shipped feature.
- [[architecture-overview]] — A map of the PointSav platform's major architectural surfaces: compute substrate, software distribution, GIS intelligence, and the editorial pipeline.
- [[foundry-doctrine-architecture]] — The planned scope for a future constitutional charter intended to encode foundational commitments and structural claims governing PointSav engineering decisions — not yet written or ratified.
- [[three-binary-architecture]] — Totebox Orchestration is delivered through three binary operating environments — os-console, os-totebox, os-orchestration — each with a distinct role and target.
- [[app-orchestration-graph-federation]] — How PointSav federates sovereign per-archive DataGraphs through a single auditable gateway, and the conditions under which that gateway becomes a dedicated service.
- [[software-distribution-substrate]] — A three-component system — release server, storefront, payment watcher — delivering compiled binaries against on-chain USDC payments, no accounts or subscriptions.
<!-- END AUTO-GENERATED -->

## Customer ownership and deployment

The principles and mechanisms by which customers own their deployment outright.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: customer-ownership-and-deployment -->
- [[customer-hostability]] — Customer hostability is the architectural commitment that every artefact runs on the customer's own hardware and keys, making self-hosted deployment the canonical pattern.
- [[economic-model]] — PointSav's two-tier commercial structure: a free Community tier as an adoption funnel, and a paid SMB tier targeting regulated businesses hyperscale billing can't serve.
- [[direct-payment-settlement]] — Payment for marketplace transactions is planned to flow directly from buyer to customer-tenant; PointSav's share is a settlement fee, not a recurring subscription.
- [[totebox-orchestration-development]] — PointSav's development environment is itself a Totebox Orchestration instance — the workspace that builds the platform runs on the same architecture it delivers.
- [[totebox-session]] — A Totebox Session is an AI-assisted contributor session within a single Totebox Archive — scoped to declared repositories, the standard entry point for development.
- [[vertical-seed-packs-marketplace]] — PointSav intends to distribute curated industry-specific seed packs as starter taxonomies, enabling tenants to contribute refinements back through a planned marketplace.
- [[foundry-services-slice-model]] — A systemd cgroup memory reservation that protects production services from being evicted by heavy build or research processes on the same host — single-node isolation without Kubernetes.
- [[cargo-target-per-user-discipline]] — Per-user partitioning of the shared Cargo build cache — why a per-developer CARGO_TARGET_DIR eliminates cross-user lock races and permission errors.
- [[mailbox-atomicity]] — flock-guarded prepend and msg-id idempotency for flat-file mailboxes — how concurrent sessions serialize writes instead of silently losing messages.
- [[multi-engine-session-coordination]] — Session-lock protocol for concurrent AI engines on one host — boot_id staleness detection and role locks that keep two sessions off the same .git/index.
- [[os-products-distribution-model]] — os-network-admin distributes today at software.pointsav.com at $0 USDC (beta); os-infrastructure's bare-metal/cloud-VM distribution model is planned but not yet catalogued. Both ship as signed artifacts, licensed and delivered on-chain.
<!-- END AUTO-GENERATED -->

## Location intelligence and domain

Architectural decisions for the location intelligence and real-property domain.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: location-intelligence-and-domain -->
- [[hardware-co-location-methodology]] — A structured approach for ranking hardware co-location candidates across jurisdictional, network, infrastructure, and cost dimensions, regulatory requirements first.
- [[flat-file-bim-leapfrog]] — The Building Design System is built on five architectural constraints — flat-file storage, open standards, Rust and Tauri, offline-first operation, and Apache 2.0 licensing. Asset-anchored ownership, offline field use, IoT ingestion, and convergence of the model with lease and financial records follow from the architecture rather than being added on top.
- [[building-design-system]] — A planned coordination layer for the built environment: a canonical, machine-readable library of building-element specifications that independent BIM authoring surfaces consume by reference, the way a software design system keeps independent product teams consistent.
- [[asset-anchored-bim-vault]] — A building's authoritative digital record structured as plain-text and standardized-binary files in a git-versioned directory, qualifying as an ISO 19650-conforming Common Data Environment that travels with the property deed.
<!-- END AUTO-GENERATED -->

An additional planned article for the location-intelligence and BIM/real-property domain — covering regional development taxonomy — is not yet written.

## See also

- [Building Blocks](/substrate/) — foundational mechanism concepts: the compounding, apprenticeship, citation, and disclosure substrates
- [Design Patterns](/patterns/) — named design patterns realised across the platform
- [Governance and Standards](/governance/) — the formal decision records, licensing posture, and compliance requirements
- [Where It Runs](/infrastructure/) — fleet deployment topology, cloud runtime, and physical infrastructure
