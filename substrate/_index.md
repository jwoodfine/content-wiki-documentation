---
schema: foundry-doc-v1
title: "Building Blocks"
slug: substrate-index
category: substrate
type: topic
content_type: topic
quality: complete
short_description: "The substrate category collects the platform's foundational mechanism concepts — the Compounding Substrate, Apprenticeship Substrate, Citation Substrate, Disclosure Substrate, Trajectory Substrate, Language Protocol Substrate, and the disciplines and primitives that compose them — each describing a structural property the platform relies on rather than a specific service or system."
index_type: thematic
index_scope: substrate
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-09-04
editor: pointsav-engineering
paired_with: _index.es.md
---

The **substrate** category collects the platform's foundational mechanism concepts. Each substrate names a structural property the platform relies on — not a specific service or system, but a pattern that composes services, systems, and content into a coherent whole.

The category answers questions like: *what makes the platform improve continuously without surrendering data ownership? what makes citations machine-auditable? what makes disclosures structurally compliant? what makes contributor work feed back into model training?* The articles here describe the mechanisms; the architecture, services, and systems categories describe how they're realised in concrete components.

<!-- START-HERE-HIGHLIGHT: engine reads this block to render the single "start here" card
     (reuses the existing cluster-card--start-here component). Do not add more than one. -->

**Start here:** read [[compounding-substrate]] first — it is the canonical pattern PointSav stewards and the frame that makes the other substrates legible. Then read [[apprenticeship-substrate]] (how editorial verdicts feed continued pretraining), [[citation-substrate]] (how every claim resolves to an authoritative source), and [[disclosure-substrate]] (how forward-looking statements remain BCSC-compliant by structure).

<!-- END-START-HERE-HIGHLIGHT -->

## Core named substrates

The nine named substrates: each names a structural property the platform depends on.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: core-named-substrates -->
- [[compounding-substrate]] — Architectural pattern pairing open platform code and a deterministic AI-free data layer with an optional intelligence layer whose interactions compound as training signal.
- [[apprenticeship-substrate]] — Platform mechanism routing work through a local Small Language Model first, capturing signed senior verdicts as preference pairs for continued pretraining.
- [[citation-substrate]] — Platform-wide YAML citation registry with drift detection that makes provenance machine-auditable from regulatory instrument to published claim.
- [[disclosure-substrate]] — Mechanism making a version-controlled Markdown wiki the primary continuous-disclosure record, with signed authorship chains and cryptographic content hashes.
- [[trajectory-substrate]] — The platform mechanism converting operational work — commits, sessions, feedback — into structured JSONL training tuples feeding a continued-pretraining corpus.
- [[language-protocol-substrate]] — The routing mechanism that carries a draft's declared register, document type, and destination between archives — a frontmatter field, a routing table, and a mailbox convention, not an AI adapter system.
- [[design-system-substrate]] — The design-system substrate is a self-hosted, customer-owned engine storing tokens and components in the customer's own Git repo, served via a machine-readable MCP endpoint.
- [[location-intelligence-substrate]] — A flat-file, open-GIS architecture letting customers own geographic datasets end-to-end using open data and a Rust-aligned rendering stack, retail co-location as first surface.
- [[retail-co-location-tier-methodology]] — Gate-based tier classification for retail co-location clusters — Regional, District, Local, or Fringe — assigned by passing fixed composition, catchment, civic-support, and overlap tests rather than by a composite score.
- [[brief-queue-substrate]] — A durable file-backed queue that makes idle-shutdown Yo-Yo compute viable without losing apprenticeship corpus capture data — the durability layer of the three-tier SLM substrate.
- [[gis-as-bim-substrate]] — What the co-location dataset offers a BIM composition pipeline: the cluster manifold and its joinable fields, region-resolution depth, civic context layers, and the stability guarantees a downstream consumer can rely on.
- [[bim-object-specification]] — The platform's reusable building-element specification unit: a fixed set of primitive categories anchored to open standards (IFC, Uniclass, bSDD), each carrying three layers of information at once — what it is, what its jurisdiction requires, and what its climate requires.
- [[editorial-draft-routing-protocol]] — Metadata classification layer that routes editorial drafts by their language_protocol declaration — which gateway processes an artifact and which vocabulary rules apply.
<!-- END AUTO-GENERATED -->

## The compounding Doorman and AI boundary

The single AI gateway that enforces the Ring 3 boundary, routes inference, and accumulates training signal.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: compounding-doorman-and-ai-boundary -->
- [[compounding-doorman]] — The operational pattern at the heart of sovereign AI substrates: a single service mediating every external compute call, logging events, accumulating training signal.
- [[mcp-substrate-protocol]] — Every Ring 1 and Ring 2 service exposes a Model Context Protocol server interface as its primary external contract, with the Doorman as the MCP gateway.
- [[adapter-composition]] — The operating-system metaphor for AI in PointSav — the Doorman as kernel, adapters as processes — and the algebra assembling intelligence from LoRA layers.
- [[knowledge-graph-grounded-apprenticeship]] — The Doorman looks up matching entities in the per-tenant knowledge graph before dispatching a request, grounding the model's response in facts the graph already holds.
- [[single-boundary-compute-discipline]] — Every AI inference request in a platform deployment routes exclusively through the Doorman, with bypass structurally prevented at the kernel level.
<!-- END AUTO-GENERATED -->

## Small Language Model stack

How the SLM tier is structured, selected, and trained.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: small-language-model-stack -->
- [[llm-substrate-decision]] — The rationale for selecting OLMo 3 as the local and GPU-burst substrate: the only fully open model family permitting continued pretraining and public-company procurement.
- [[four-tier-slm-substrate]] — A graduated sovereignty path for AI deployment: four customer tiers from a lightweight API gateway up to a domain-specialist service, each adding capability without regressions.
- [[yoyo-compute-substrate]] — The three-ring compute substrate letting service-slm spin GPU inference capacity up and down while retaining state and producing an audit ledger of every compute event.
- [[yo-yo-lora-training-pipeline]] — The nightly two-phase pipeline on Yo-Yo #1: Phase 1 runs entity extraction for the DataGraph; Phase 2 trains a LoRA adapter via QLoRA on a single L4 GPU.
- [[tui-corpus-producer]] — Every terminal interaction with service-slm through the operator TUI is a curated training corpus contribution for the per-tenant adapter.
- [[nightly-datagraph-rebuild]] — The scheduled process that reconstructs the platform's knowledge graph from canonical flat-file sources each night. A human-approval checkpoint exists for AI-extracted entities, but it is opt-in — an operator must enable it; automated writes land without per-item review by default.
- [[ontological-datagraph]] — Organizational knowledge graph of people, companies, projects, and relationships — persistent semantic memory for answering business-state queries without re-reading sources.
- [[soft-slm-tiered-gateway]] — A tiered inference gateway routing AI requests through a local model first, escalating to remote GPU nodes and external APIs only when needed, minimizing cost and exposure.
<!-- END AUTO-GENERATED -->

## Cryptographic and microkernel primitives

The formal verification and cryptographic foundations beneath every PointSav operating system.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: cryptographic-and-microkernel-primitives -->
- [[sel4-microkernel-substrate]] — Formally verified seL4 microkernel, PointSav's planned shared L1 kernel substrate — not yet the running kernel for every OS family member as shipped today.
- [[merkle-proofs-as-substrate-primitive]] — Merkle proofs are the cryptographic mechanism letting the platform prove to any third party that a record is part of an append-only log that has not been rewritten.
- [[capability-ledger-substrate]] — The Capability Ledger Substrate is the mechanism by which every access-control decision becomes a cryptographically auditable event anchored to a customer-controlled log.
- [[system-substrate-doctrine]] — The kernel-level architecture beneath every PointSav service — a customer-rooted capability ledger, a two-bottoms sovereign OS strategy, and boot-anywhere recovery.
- [[capability-geometry]] — Capability Geometry is PointSav's term for seL4-based authorization that replaces mutable access-control policy with a formally proven, kernel-enforced capability DAG.
- [[moonshot-toolkit-build-orchestrator]] — Rust-only build orchestrator for seL4 unikernel images — TOML spec to content-addressed manifest to bootable AArch64 elfloader, replacing Python and CMake.
- [[sel4-aarch64-qemu-substrate-target]] — Hardware foundation for the unikernel platform — formally verified seL4 on AArch64 with QEMU's virt machine as the development, testing, and CI environment.
- [[sel4-unikernel-substrate]] — os-console is intended to run as a seL4 Microkit unikernel image in production, compiling application code with a formally verified kernel to eliminate OS attack surface.
<!-- END AUTO-GENERATED -->

## Sovereignty and customer ownership

What the platform makes freely transferable, customer-owned, and vendor-independent.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: sovereignty-and-customer-ownership -->
- [[sovereign-ai-commons]] — PointSav's market positioning as steward of shared, open AI infrastructure for regulated SMBs: structural properties large cloud providers cannot offer without changing billing.
- [[knowledge-commons]] — The economic model separating what PointSav publishes freely from what it sells — public knowledge under open licenses, paid service at multi-Totebox aggregation.
- [[customer-owned-graph-ip]] — The per-tenant knowledge graph and trained adapter weights are the customer's intellectual property, portable and exportable without vendor approval.
- [[tier-zero-customer-side-sovereign-specialist]] — The Tier 0 Totebox is a sovereign specialist deployment running on the customer's own hardware with no required cloud dependency and no required internet connectivity.
- [[substrate-without-inference-base-case]] — The Totebox Archive remains fully operational and freely transferable even when no AI inference tier is available; the deterministic substrate is the load-bearing foundation.
- [[substrate-native-compatibility]] — Structural compatibility with MediaWiki reader and integrator conventions while declining API mimicry, keeping substrate-native interfaces to reduce maintenance burden.
<!-- END AUTO-GENERATED -->

## Platform mechanics

Cross-cutting principles that apply across all substrate implementations.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: platform-mechanics -->
- [[code-for-machines-first]] — Every inter-service contract, audit record, configuration, and ontology is machine-readable as a primary surface; human-facing interfaces are skins on machine-first APIs.
- [[seed-taxonomy-as-smb-bootstrap]] — Every tenant deployment provisions a four-part seed taxonomy — Archetypes, Chart of Accounts, Domains, Themes — as the knowledge graph bootstrap.
- [[reverse-flow-substrate]] — The Doorman gateway and audit ledger enforcing inbound data discipline are planned to also enforce outbound commercial flows — marketplace and ad exchange, opt-in per tenant.
<!-- END AUTO-GENERATED -->

## See also

- [How It's Built](/architecture/) — cross-cutting platform architecture
- [Design Patterns](/patterns/) — named design patterns realised on top of substrates
