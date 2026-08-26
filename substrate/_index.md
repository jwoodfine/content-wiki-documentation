---
schema: foundry-doc-v1
title: "Substrate"
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
last_edited: 2026-08-06
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
- [[compounding-substrate]] — Five structural properties that make every operational interaction a compounding training event across all tenant deployments.
- [[apprenticeship-substrate]] — Routes work through a local SLM, captures signed senior verdicts, and uses the resulting preference pairs as continued-pretraining signal.
- [[citation-substrate]] — Platform-wide YAML citation registry with drift detection; makes provenance machine-auditable from regulatory instrument to published claim.
- [[disclosure-substrate]] — Version-controlled Markdown with signed authorship chains and cryptographic content hashes produces structurally BCSC-compliant continuous-disclosure records.
- [[trajectory-substrate]] — Converts operational work — commits, sessions, operator feedback — into structured JSONL training tuples for continued pretraining.
- [[language-protocol-substrate]] — Four adapter families and eighteen genre templates encoding register, brand voice, and target audience as reusable prompt scaffolding.
- [[design-system-substrate]] — Self-hosted design-system engine storing tokens and components in the customer's own git repository; W3C DTCG token format; machine-readable MCP endpoint.
- [[location-intelligence-substrate]] — Flat-file open-GIS architecture: Apache-licensed open data, Rust-aligned rendering stack, retail co-location analysis as the first deployed surface.
- [[retail-co-location-tier-methodology]] — The four-tier (Regional/District/Local/Fringe) gate system that scores retail co-location clusters — composition, catchment rank, civic support, non-overlap.
- [[brief-queue-substrate]] — Durable file-backed queue that makes idle-shutdown Yo-Yo compute viable without losing apprenticeship corpus capture data.
- [[gis-as-bim-substrate]] — What the co-location dataset offers a BIM composition pipeline: the cluster manifold and its joinable fields, region-resolution depth, civic context layers, and the stability guarantees a downstream consumer can rely on.
<!-- END AUTO-GENERATED -->

## The compounding Doorman and AI boundary

The single AI gateway that enforces the Ring 3 boundary, routes inference, and accumulates training signal.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: compounding-doorman-and-ai-boundary -->
- [[compounding-doorman]] — The single service mediating every external compute call: logs every event, accumulates training signal.
- [[mcp-substrate-protocol]] — Every Ring 1 and Ring 2 service exposes a Model Context Protocol server interface as its primary external contract; the Doorman is the MCP gateway.
- [[adapter-composition]] — The OS metaphor for AI in PointSav: Doorman as kernel, adapters as processes, service-content as filesystem; composition algebra for per-request intelligence from versioned LoRA layers.
- [[knowledge-graph-grounded-apprenticeship]] — The Doorman consults the per-tenant knowledge graph before every inference request; graph and adapter co-evolve as training tuples accumulate.
- [[single-boundary-compute-discipline]] — Every AI inference request routes exclusively through the Doorman; bypass is structurally prevented at the kernel level.
<!-- END AUTO-GENERATED -->

## Small Language Model stack

How the SLM tier is structured, selected, and trained.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: small-language-model-stack -->
- [[llm-substrate-decision]] — The rationale for OLMo 3: the only fully open model family — training data, training code, and checkpoints included — satisfying a Canadian public-company procurement posture.
- [[four-tier-slm-substrate]] — A graduated sovereignty path from a lightweight API gateway with no local model up through a domain-specialist service trained on the vendor's aggregated corpus.
- [[yoyo-compute-substrate]] — The three-ring compute substrate that lets service-slm spin GPU inference capacity up and down while retaining state and producing an audit ledger of every compute event.
- [[yo-yo-lora-training-pipeline]] — The nightly two-phase pipeline: entity extraction for the business DataGraph (Phase 1) and LoRA adapter training against engineering and apprenticeship corpora using QLoRA on a single L4 GPU (Phase 2).
- [[tui-corpus-producer]] — Every terminal interaction with service-slm through the operator TUI is a curated training corpus contribution for the per-tenant adapter.
- [[nightly-datagraph-rebuild]] — The scheduled process that reconstructs the platform's knowledge graph from canonical flat-file sources each night; entity extraction runs through the Doorman, with a human-approval checkpoint that exists but is off by default.
- [[ontological-datagraph]] — The organizational knowledge graph of people, companies, projects, and relationships — persistent semantic memory injected as context before every AI inference request.
- [[soft-slm-tiered-gateway]] — The tiered inference gateway that routes AI requests through a local model first, escalating to burst GPU nodes and external APIs only when needed.
<!-- END AUTO-GENERATED -->

## Cryptographic and microkernel primitives

The formal verification and cryptographic foundations beneath every PointSav operating system.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: cryptographic-and-microkernel-primitives -->
- [[sel4-microkernel-substrate]] — The mathematically formally verified seL4 microkernel as L1 kernel for all PointSav operating systems: structurally guaranteed memory isolation, zero buffer overflows, capability-based permissions.
- [[merkle-proofs-as-substrate-primitive]] — RFC 9162 Merkle proof primitives as the cryptographic floor of the platform's capability ledger; ledger validity verifiable without trust in any central authority.
- [[capability-ledger-substrate]] — The mechanism by which every access-control decision in a Foundry deployment becomes a cryptographically auditable event anchored to a customer-controlled log; extends seL4's formally verified capability model with a Merkle transparency layer.
- [[system-substrate-doctrine]] — The kernel-level architecture: a customer-rooted capability ledger that is the audit log, a two-bottoms sovereign OS strategy, and three mechanisms for time-bound capabilities and boot-anywhere recovery.
- [[capability-geometry]] — PointSav's term for seL4-based authorization that replaces mutable access-control policy with a formally proven, kernel-enforced capability DAG.
- [[moonshot-toolkit-build-orchestrator]] — Rust-only build orchestrator for seL4 unikernel images — TOML spec to content-addressed manifest to bootable AArch64 elfloader binary, replacing Python and CMake.
- [[sel4-aarch64-qemu-substrate-target]] — Hardware foundation for the unikernel platform — formally verified seL4 on AArch64 with QEMU's virt machine as the development, testing, and CI target.
- [[sel4-unikernel-substrate]] — os-console's intended production form: a seL4 Microkit unikernel image compiling application code directly with a formally verified kernel, eliminating general-purpose OS attack surface.
<!-- END AUTO-GENERATED -->

## Sovereignty and customer ownership

What the platform makes freely transferable, customer-owned, and vendor-independent.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: sovereignty-and-customer-ownership -->
- [[sovereign-ai-commons]] — PointSav's market positioning as a steward of shared open AI infrastructure for regulated SMBs: five structural properties that large-scale cloud providers cannot offer without dismantling their own billing models.
- [[knowledge-commons]] — The economic model that separates what PointSav publishes freely from what it sells: public knowledge artifacts under open licences, paid service at the point of multi-Totebox aggregation.
- [[customer-owned-graph-ip]] — The per-tenant knowledge graph and trained adapter weights are the customer's intellectual property, portable and exportable without vendor approval.
- [[tier-zero-customer-side-sovereign-specialist]] — A sovereign specialist Totebox deployment running on the customer's own hardware with no required cloud dependency and no required internet connectivity.
- [[substrate-without-inference-base-case]] — The Totebox Archive remains fully operational and freely transferable even when no AI inference tier is available; the deterministic substrate is the load-bearing foundation.
- [[substrate-native-compatibility]] — Structural compatibility with MediaWiki reader conventions while deliberately declining API mimicry, maintaining substrate-native interfaces.
<!-- END AUTO-GENERATED -->

## Platform mechanics

Cross-cutting principles that apply across all substrate implementations.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: platform-mechanics -->
- [[code-for-machines-first]] — Every inter-service contract, audit record, configuration, and ontology is machine-readable as a primary surface; human-facing interfaces are skins on machine-first APIs.
- [[seed-taxonomy-as-smb-bootstrap]] — Every tenant deployment provisions a four-part seed taxonomy — Archetypes, Chart of Accounts, Domains, Themes — as the knowledge graph bootstrap.
- [[reverse-flow-substrate]] — The Doorman gateway and audit ledger that enforce inbound data discipline are planned to also enforce outbound commercial flows — data marketplace and ad exchange — both opt-in per tenant.
<!-- END AUTO-GENERATED -->

## See also

- [Architecture](/architecture/) — cross-cutting platform architecture
- [Patterns](/patterns/) — named design patterns realised on top of substrates
