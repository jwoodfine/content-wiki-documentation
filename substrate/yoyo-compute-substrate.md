---
schema: foundry-doc-v1
title: "Yo-yo compute substrate"
slug: yoyo-compute-substrate
category: substrate
type: topic
content_type: topic
quality: complete
index_group: small-language-model-stack
short_description: "The three-ring compute substrate letting service-slm spin GPU inference capacity up and down while retaining state and producing an audit ledger of every compute event."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-15
editor: pointsav-engineering
cites: []
references:
  - id: 1
    text: "Open Source Security Foundation. 'SLSA: Supply chain Levels for Software Artifacts v1.0.' SLSA.dev, 2023."
    url: "https://slsa.dev/spec/v1.0/"
paired_with: yoyo-compute-substrate.es.md
---

The Yo-Yo Compute Substrate is the specification for how [[service-slm]] manages GPU inference across teardowns. A GPU inference node is expensive at idle. But a node that discards all state on shutdown forces a full re-computation on the next spin-up — slow, wasteful, and commercially corrosive at scale. The Yo-Yo substrate resolves this by decomposing compute state into three rings, each with a different persistence strategy, so that spin-up is fast, state is retained where it is worth retaining, and every event is recorded in a SOC 3-grade [[worm-ledger-architecture|audit ledger]].

The name is literal: the compute tier comes down and goes back up, repeatedly, without losing what matters.

## The three-ring memory model

| Ring | Name | Storage | Survives teardown? |
|---|---|---|---|
| 1 | Bootstrap | Container image + GCS-cached model weights | Yes (as artefacts in cold storage) |
| 2 | Working memory (KV cache) | LMCache + Mooncake Store | Yes (pooled, `moduleId`-isolated) |
| 3a | Long-term graph memory | LadybugDB in [[service-content]] | Yes (authoritative) |
| 3b | Long-term skill (adapters) | [[adapter-composition|LoRA adapter]] stack as OCI Artefacts | Yes (portable, signed) |

Everything outside these rings is ephemeral and intentionally discarded.

## Ring 1 — Bootstrap: a scheduled VM, not a serverless endpoint

The real Yo-Yo #1 node is a `google_compute_instance` — a conventional GCE VM with an L4 GPU, brought up on a `google_compute_resource_policy` schedule for the nightly training window, not a Cloud Run service scaling to zero between requests. There is no drivers-pre-installed serverless cold start to describe here; the real boot sequence starts the VM and then waits — up to ninety minutes — for the inference server to signal readiness before the nightly pipeline's first phase can begin. The workload pattern this ring actually serves is scheduled batch work, not opportunistic sub-second query-time bursts.

**Pre-downloaded model weights**, staged on a persistent disk (`google_compute_disk`) rather than pulled fresh on every boot, remain accurate — this avoids re-downloading tens of gigabytes from the upstream model repository on every nightly cycle.

CUDA checkpoint/restore, single-routed-adapter migration, and the other forward-looking primitives described later in this article remain genuinely planned research directions independent of this correction — this section's fix is about which GCP product Ring 1 actually runs on and how long its real boot takes, not about whether those primitives are worth pursuing.

## Ring 2 — Working memory: KV cache that survives teardown

When a GPU node tears down, the in-GPU KV cache is lost. On the next spin-up, the inference engine re-prefills every prompt from scratch — even when ninety percent of the input (the graph subgraph, the system prompt, the task classification context) is identical to what was just processed. This is the dominant cause of "the second run feels slow."

**LMCache** integrates with the inference engine via the KV connector interface. It hashes token blocks and fetches matching KV cache blocks from a tiered store: GPU memory → CPU DRAM → remote object storage. **Mooncake Store** is the remote storage tier — a distributed KV pool that persists in CPU DRAM on persistent hosts or in SSD-backed object storage. It survives inference engine instance teardown because it runs as a separate process.

The `moduleId` field from the RF2 envelope namespaces every cache block. Customer A's blocks never collide with Customer B's, even when both draw from the same physical pool. The Mooncake master instance is a small, always-on host — provisioned once, not per-project.

For workloads with repeated-prefix structure — every document processed against the same knowledge graph shares a multi-thousand-token system prompt and context spine — cache hit rates above sixty percent are achievable on the second full corpus run. At scale this translates directly into GPU cost reduction.

## Ring 3a — Long-term graph memory

The LadybugDB knowledge graph in `service-content` is the long-term semantic memory for every project. `service-slm` reads from it at context-assembly time. It never writes back directly — writes flow through the human-gated proposal pipeline documented elsewhere in this wiki, not an automated cycle inside `service-slm` itself.

Ring 3a is project-scoped by design. One tenant's graph partition is inaccessible to another without an explicit export through the authorised data channel. This is the correct behaviour for data. It is the wrong behaviour for skill — which is why Ring 3b exists as a separate layer.

## Ring 3b — Long-term skill: the LoRA adapter library

This is the compounding layer. Each new project leaves behind a fine-tuned LoRA adapter — a small, versioned, frozen-weight module that encodes task-specific behaviour. A adapter trained on classification patterns, entity resolution, or domain terminology runs on top of the base model weights at near-base inference speed. The dual-adapter pattern feeds the [[apprenticeship-substrate]] training loop over time.

Adapters are stored as OCI Artefacts, Sigstore-signed and SLSA-attested. [^1] They are loaded at inference engine boot:

- **Shared adapters** (prefixed `dka-*`) accumulate cross-project general-domain skill. Every project benefits when these improve.
- **Per-project adapters** (prefixed `{client}-*`) carry project-specific entity and terminology knowledge. They stay with their project.

The dual-adapter pattern (shared + per-project, with orthogonality constraints to prevent catastrophic forgetting) is the recommended starting configuration. Migration to a single routed adapter becomes worthwhile when the adapter library grows beyond approximately ten projects and management overhead increases.

Every adapter version is registered in `service-slm/memory/adapters/registry.yaml` before activation, with a training-data hash and evaluator sign-off. Adapter selection at query time is automatic: the `moduleId` plus the task classification determine which adapter stack activates.

**This is the compounding asset.** The base model is a commodity that every deployment in the industry can access. The adapter library is specific to the operator's accumulated operational history. It grows with every project. It cannot be purchased from a third party.

## The audit ledger

Every Yo-Yo event is logged to an append-only CSV ledger. The schema records event type, `moduleId`, node identifier, job identifier, input hash, adapter versions active, KV cache hit ratio, tokens processed, GPU seconds consumed, estimated cost, completion status, and operator identity.

Event types include `BOOT_REQUEST`, `BOOT_COMPLETE`, `JOB_START`, `JOB_COMPLETE`, `CHECKPOINT`, `TEARDOWN_REQUEST`, `TEARDOWN_COMPLETE`, `PREEMPTION`, `ADAPTER_LOAD`, and `KV_POOL_SYNC`.

This ledger is a processing-integrity artefact. An operator who needs to answer "which adapter weighed in on this output, and what did it cost?" can inspect the ledger directly, without querying a third-party system. The ledger links every output — every wiki page, every exported data record, every generated analysis — back to the exact compute event, the exact adapter versions, and the exact source material that produced it.

Managed inference endpoints structurally cannot produce this record. They operate at a layer above the events the Yo-Yo ledger captures, and they have no incentive to expose per-call cost decomposition or adapter provenance.

## The `moduleId` discipline

The RF2 envelope already carries a `moduleId` field on every message. The Yo-Yo substrate extends its reach into compute:

- **Ring 1**: selects the container variant to boot (rarely varies per project)
- **Ring 2**: namespaces Mooncake block hashes (Project A and Project B share a pool; they never share cache blocks)
- **Ring 3a**: scopes the LadybugDB graph traversal to the correct partition
- **Ring 3b**: selects the LoRA adapter stack to activate — the [[four-tier-slm-substrate|tier selection]] propagates `moduleId` into every adapter load
- **Ledger**: tags every entry for per-project cost accounting

One field, five jobs. The multi-tenant isolation property was not an afterthought; it is a structural consequence of `moduleId` propagating through every ring.

## 2030 headroom

The substrate is designed so research primitives that are planned or at RFC stage in 2026 can be integrated without architectural change:

| Primitive | Status (2026) | Integration point |
|---|---|---|
| CUDA checkpoint/restore | RFC stage; ten-times cold-start gain demonstrated in controlled settings | Ring 1: optional checkpoint bundle input |
| Single routed adapter (C-LoRA) | Published 2025 | Ring 3b: registry schema migration |
| Multi-cloud KV pool | Long-horizon research direction; no orchestration layer for it exists in the current deployment | Ring 2: Mooncake master on multi-cloud pool |
| FP8 KV cache quantisation | Available as inference engine config flag | Ring 2: config flag, approximately two-times memory reduction |
| Sleep-time adapter retraining | Research stage | Ring 3b: nightly batch retraining on reduced-cost compute |

Each of these may integrate as a configuration addition or new subdirectory. None requires rewriting `service-slm`.

## Phase roadmap

**Phase 1 (current — trial)**: Ring 1 built as a scheduled GCE VM (see above, not the Cloud Run/SkyPilot shape this roadmap once described). Ledger fully built with all event types defined. `moduleId` propagated through every call even with only one project active. Rings 2 and 3b are not yet needed and are intentionally deferred. The Yo-Yo tier is currently down at the time of this wiki's own [[service-slm-yoyo-operational|operational status article]] — worth checking before assuming Phase 1 is presently serving live traffic.

**Phase 2 (planned — after trial)**: Ring 2 added. LMCache and Mooncake Store integrated. Target: sixty percent or greater cache hit rate on the second full corpus run.

**Phase 3 (planned — first commercial deployment beyond initial customer)**: Ring 3b added. First LoRA adapters trained (task classification, archetype detection, entity resolution). Dual-adapter pattern, adapter registry, training pipeline.

**Phase 4 (intended — when research matures)**: CUDA checkpoint/restore integration. Single-adapter C-LoRA migration. Multi-cloud KV pool.

## See also

- [[compounding-doorman]] — the Doorman pattern that service-slm implements; the Yo-Yo substrate is its Tier B compute path
- [[slm-stack-architecture]] — the Rust dependency graph and binary layout for service-slm
- [[apprenticeship-substrate]] — how the Yo-Yo audit ledger generates LoRA adapter training signal
- [[three-ring-architecture]] — the platform ring structure the Yo-Yo substrate extends

