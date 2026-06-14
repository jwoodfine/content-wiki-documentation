---
schema: foundry-doc-v1
title: "Architecture"
slug: _index
category: architecture
type: topic
content_type: topic
quality: complete
short_description: "Cross-cutting platform architecture: the three-ring composition model, AI routing and inference boundary, security and identity substrate, customer ownership principles, and the location intelligence domain."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-15
editor: pointsav-engineering
paired_with: _index.es.md
---

PointSav is composed from three concentric rings with strict one-way dependencies, a deterministic data pipeline that runs fully without AI, and a sovereignty discipline that allows customers to fork the entire stack on day one. Architecture articles describe the structural decisions behind those properties — why they are designed the way they are, how they compose, and what invariants must hold across every deployment.

The three-ring model is the load-bearing frame: Ring 1 handles per-tenant boundary ingest, Ring 2 provides deterministic knowledge and processing, and Ring 3 adds optional AI inference that never writes to the authoritative record. Articles in this category explain the rings, the security model that enforces their boundaries, the AI routing logic, and the customer-ownership principles that govern the platform's commercial architecture.

## Platform structure

The foundational structural articles — the patterns that compose every PointSav deployment.

- [[three-ring-architecture]] — Three concentric rings with strict one-way dependencies; AI is structurally optional; the deterministic pipeline runs fully without Ring 3.
- [[3-layer-stack]] — The three-layer infrastructure decomposition: raw compute capability, isolated platform execution, and secure operator access.
- [[three-layer-architecture]] — How PointSav deliverables move through SOFTWARE, SHOWCASE, and INSTANCE layers with a strict one-way vendor-to-customer flow.
- [[six-tier-sovereignty-matrix]] — The six-prefix monorepo taxonomy (app-, asset-, os-, service-, system-, moonshot-) that makes dependency hygiene structural.
- [[foundry-doctrine-overview]] — A public summary of the platform's constitutional charter: six pillars, fifty-two structural claims, and the economic model that sustains them.
- [[leapfrog-2030-architecture]] — The Leapfrog 2030 architectural vision: the infrastructure physics of the 2030 hyperscaler era, and how the platform is positioned to benefit from it.
- [[pointsav-overview]] — PointSav Digital Systems: what the company builds, how it is organised, and the three-entity corporate structure.

## Security and identity

How the platform enforces isolation, verifies identity, and makes unauthorised access structurally impossible.

- [[diode-standard]] — The foundational unidirectional command-flow discipline; eliminates lateral movement by removing the routing logic that would allow it.
- [[capability-based-security]] — Every software component holds a cryptographic capability token to communicate with any other; no ambient authority.
- [[machine-based-auth]] — Machine-based authorization: cryptographic hardware pairing replaces username and password; the pair is the permission.
- [[crypto-attestation]] — Edge-node content attestation: client-side SHA-256 hashing lets any auditor verify a disclosure has not been altered in transit.
- [[cryptographic-ledgers]] — Immutable-state storage by hash-chain; any alteration breaks a verifiable cryptographic proof rather than a policy check.
- [[personnel-permissions]] — Contributor identity in Totebox Orchestration: cryptographic hardware pairings, not role-based access control stored in a database.
- [[five-stage-supply-chain]] — Code moves from contributor to production through five stages, with a double-blind air-gap that separates production credentials from contributor workspaces.
- [[verification-surveyor]] — The human-in-the-loop component that presents extracted identity fragments to an operator before permanent commitment to the verified ledger.

## AI routing and inference boundary

How AI requests are classified, routed, and contained so they never touch the authoritative record.

- [[doorman-protocol]] — The Doorman: the single AI boundary that sanitises data, routes among compute tiers, and holds every API key; no key lives outside this boundary.
- [[pointsav-llm]] — The planned vendor-tier specialist model (Tier 3 of the Four-Tier SLM Substrate Ladder); continued pretraining of OLMo 3 32B on the federated apprenticeship corpus.
- [[slm-stack-architecture]] — The full Rust dependency graph and binary architecture for service-slm.
- [[sovereign-ai-routing]] — AI requests pass through a local sanitisation step before reaching any external model; internal structured data never travels to third-party servers in identifiable form.
- [[zero-container-inference]] — Why the platform runs inference directly in the service binary rather than in a container runtime, and what that means for isolation and cost.
- [[decode-time-constraints]] — Structural constraints applied at each token-emission step; banned vocabulary and structurally invalid responses are mathematically impossible to produce.

## Customer ownership and deployment

The principles and mechanisms by which customers own their deployment outright.

- [[customer-hostability]] — The architectural commitment that every artefact runs on the customer's own hardware, against the customer's own keys, with the customer's own audit ledger.
- [[economic-model]] — The two-tier commercial structure: a free Community tier and a paid SMB Customer tier sized for regulated businesses that hyperscalers cannot serve economically.
- [[direct-payment-settlement]] — Marketplace transaction payments flow directly from buyer to customer-tenant; PointSav's share is a transaction fee at settlement.
- [[totebox-orchestration-development]] — The development environment itself is a Totebox Orchestration instance; the workspace that builds the platform runs on the architecture it delivers.
- [[totebox-session]] — A Totebox Session: an AI-assisted contributor session scoped to one archive, unable to write outside it, the standard entry point for all development work in Totebox Orchestration.
- [[vertical-seed-packs-marketplace]] — Curated industry-specific starter taxonomies distributed as seed packs; tenants contribute refinements back through a planned marketplace.

## Location intelligence and domain

Architectural decisions for the location intelligence and real-property domain.

- [[co-location-methodology]] — The spatial analysis methodology for co-location ranking: how retail and institutional concentrations are measured and scored.
- [[location-intelligence-strategy]] — The strategic and architectural frame for the location intelligence substrate: flat-file open-GIS, offline-first, no per-seat vendor costs.
- [[flat-file-bim-leapfrog]] — How Building Information Modelling is handled as flat-file ISO 19650 records rather than hosted database instances.
- [[building-design-system-bim]] — Design system tooling adapted for BIM and real-property workflows.
- [[development-regions]] — Regional taxonomy for development and planning analysis across PointSav deployments.

## See also

- [Substrate](/substrate/) — foundational mechanism concepts: the compounding, apprenticeship, citation, and disclosure substrates
- [Patterns](/patterns/) — named design patterns realised across the platform
- [Governance](/governance/) — the formal decision records, licensing posture, and compliance requirements
- [Infrastructure](/infrastructure/) — fleet deployment topology, cloud runtime, and physical infrastructure
