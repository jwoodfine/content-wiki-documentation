---
schema: foundry-doc-v1
title: "service-slm Rust Stack Architecture"
slug: topic-slm-stack-architecture
category: architecture
type: topic
quality: published
short_description: "The full Rust dependency graph and binary architecture for service-slm, the Doorman service that mediates every inference call in the PointSav platform."
status: pre-build
last_edited: 2026-05-01
editor: pointsav-engineering
cites: []
paired_with: topic-slm-stack-architecture.es.md
---

`service-slm` is built as a single, statically-linked Rust binary. Every direct dependency in the stack is either pure Rust or Rust bindings to a permissively licensed native library. No copyleft licenses appear anywhere in the dependency graph, which means PointSav holds an unrestricted right to fork, modify, and redistribute the entire codebase. This property is called the "We Own It" criterion.

The choice of Rust is not a language preference. It is an engineering constraint imposed by the intended deployment target — ToteboxOS appliance hardware, where a CPython interpreter plus a large ML framework does not fit in the available memory envelope, and where cold-start predictability and the absence of a garbage collector are operational requirements rather than optional improvements.

## Why L2 Rust, not L3 Rust

Three distinct levels of "Rust-ness" are commonly conflated:

| Level | Meaning | Achievable for service-slm? |
|---|---|---|
| L1 — Source Rust | All code written by PointSav is Rust | Yes |
| L2 — Direct-deps Rust | Every crate directly depended on is a Rust crate (may internally FFI to C/C++) | Yes |
| L3 — Transitive Rust | Every line in the entire dependency tree, including GPU kernels, is Rust | No — and not the right goal |

L3 is unachievable for GPU inference and graph databases in 2026 because CUDA kernels and columnar storage engines have a twenty-year C++ inheritance. L2 is achievable and sufficient. The "We Own It" test is a license question, not a language question: `MIT + Apache-2.0 = we own it`.

## The canonical stack

### Inference layer

The inference runtime for service-slm is **mistral.rs**, a statically-linked Rust binary that ships with FlashAttention V2/V3, PagedAttention, prefix caching, and LoRA hot-swap per token. It exposes an OpenAI-compatible HTTP endpoint, which is the wire protocol the Doorman uses for Tier A (local) and Tier B (GPU burst) calls.

The foundation ML framework underneath mistral.rs is **candle** (Apache-2.0/MIT dual license, Hugging Face). If mistral.rs ever diverges from platform requirements, candle provides a clean rebuild path without re-architecting the stack.

The OLMo 3 model family is the production base model selection. OLMo 3 carries an Apache 2.0 code license and an Open Data Commons license for training data, making it the only major open-weight family whose entire lineage — weights, training data, and code — is permissively licensed end-to-end. This is the requirement for the [[apprenticeship-substrate]] training path, where PointSav exercises the right to run continued pretraining on customer-accumulated signal.

### HTTP and async runtime

The Doorman's inbound HTTP surface is served by **axum** (MIT), with **tower** middleware for retries, timeouts, and backpressure, running on the **tokio** async runtime (MIT). Outbound HTTP calls — to Cloud Run GPU instances, to the Tier C external API allowlist — use **hyper** and **reqwest**.

### Storage and state

The audit ledger uses **sqlx** with an SQLite backend for local, append-only structured storage. The long-term knowledge graph is held by LadybugDB, addressed through Rust bindings (MIT). Cloud object storage for model weights and LoRA adapter artefacts is abstracted through **object_store** (Apache-2.0).

### Document processing

The document ingest path uses **oxidize-pdf** for PDF parsing (pure Rust, zero C dependencies, 99.3% success rate across real-world PDFs at 3,000–4,000 pages per second), **docx-rust** for `.docx` files, **calamine** for `.xlsx` spreadsheets, and **pulldown-cmark** for Markdown.

**mupdf-rs is explicitly excluded** from the dependency graph. It carries an AGPL-3.0 license, which would taint the binary if linked. The `cargo-deny` CI policy enforces this exclusion automatically on every commit.

### Orchestration

Internal job orchestration uses **apalis** (MIT) — a job-processing library with step-based workflow composition and tower middleware compatibility. apalis fits the service-slm work shape: sanitise, send, await, receive, rehydrate. It introduces no Python runtime dependency, which is the meaningful distinction from Python-native workflow engines used in the `service-content` derivative pipeline.

### Observability and supply-chain security

Structured logging and distributed tracing are provided by the **tracing** crate family (MIT), with **opentelemetry-rust** for OpenTelemetry export to the SOC 3 audit pipeline. Container image signing and OCI artefact attestation use **sigstore-rs** (Apache-2.0).

**cargo-deny** runs in CI on every commit and enforces license policy across the full transitive dependency tree, blocking any new dependency that introduces AGPL, GPL, LGPL, BSL, or custom community licenses. This turns manual license discipline into an automated build constraint.

## Flat binary architecture

The cargo workspace produces one binary: `slm-cli`. Logical modules communicate via Rust function calls, not RPC. External calls — to Cloud Run, to the Mooncake KV cache sidecar, to Tier C API endpoints, to LadybugDB — are the only network boundaries.

```
service-slm/
├── crates/
│   ├── slm-core/            shared types, moduleId discipline
│   ├── slm-doorman/         sanitise / send / receive / rehydrate
│   ├── slm-ledger/          append-only audit trail (SQLite + CSV)
│   ├── slm-compute/         Cloud Run driver, container management
│   ├── slm-memory-kv/       LMCache + Mooncake wire protocol client
│   ├── slm-memory-adapters/ LoRA adapter registry and loader
│   ├── slm-inference-local/ mistral.rs-backed local inference
│   ├── slm-inference-remote/ GPU burst driver
│   ├── slm-api/             axum inbound endpoints
│   └── slm-cli/             binary entry point
└── xtask/                   build helpers, release automation
```

This is the shape a ToteboxOS appliance component requires: one process, one log stream, one set of metrics, one binary to sign with Sigstore, one configuration file.

## ToteboxOS integration

The binary architecture is motivated in part by ToteboxOS deployment constraints. A CPython stack plus a GPU inference framework does not fit in the memory envelope available on constrained appliance hardware. A Rust binary with a quantised inference runtime operating in CPU mode does.

The relevant constraints per ToteboxOS Laptop-A hardware profile (~550 MB available headroom after core services):

- Static binary, no interpreter warmup — seconds, not minutes to first inference
- No garbage collector, no interpreter heap
- True parallelism across cores without a global interpreter lock
- Cross-compilation via `cargo build --target aarch64-unknown-linux-gnu` for ARM ToteboxOS targets

## Three external non-Rust services

Three services in the Yo-Yo compute substrate sit outside the Rust binary, all behind stable network protocols:

**LMCache + Mooncake Store** (Python control plane + C++ Mooncake Transfer Engine): the KV cache tier that persists prefill state across GPU node teardowns. service-slm holds a Rust client that speaks to Mooncake over HTTP and TCP. No FFI coupling. Both are Apache-2.0 licensed.

**vLLM** (Python): the Phase 1 trial inference engine. Replaced by mistral.rs in Phase 2. Apache-2.0.

**SkyPilot** (Python): multi-cloud GPU orchestration. Used when Cloud Run GPU alone is insufficient. Apache-2.0.

All three are behind stable network protocols. service-slm depends on the wire protocol, not the implementation. Swapping any of them requires changing one client module.

## License hygiene

The mandatory rule for the entire dependency graph: every entry is one of `MIT`, `Apache-2.0`, `BSD-2-Clause`, `BSD-3-Clause`, `ISC`, `Unicode-DFS`, `MPL-2.0` (file-level), or `Zlib`. Anything else fails the CI build.

`cargo-deny` with a `deny.toml` policy file enforces this. The `deny.toml` is committed to the repository and reviewed at every dependency addition.

## See Also

- [[compounding-doorman]] — the operational pattern service-slm implements
- [[topic-yoyo-compute-substrate]] — the multi-ring compute substrate service-slm drives
- [[apprenticeship-substrate]] — how the audit ledger feeds LoRA adapter training
- [[three-ring-architecture]] — Ring 3 placement of service-slm in the platform

## References

1. `SLM-STACK.md` — workspace-root technical specification for the service-slm Rust stack; source document for this topic.
2. `YOYO-COMPUTE.md` — workspace-root specification for the Yo-Yo compute substrate; companion to this topic.
3. SYS-ADR-07 — structured data never routes through AI; the sanitise-outbound discipline at the Doorman boundary.
4. `conventions/compounding-substrate.md` — the meta-pattern service-slm implements.

---

## Provenance

Source material: workspace-root `SLM-STACK.md` (v1, 2026-04-20). Naming corrections applied: `vendor-phi3-mini` / `phi3-mini` → `OLMo 3` / `vendor-olmo-3`; `frontend` → `ConsoleOS`; `ArchiveOS` → `ToteboxOS`. Structural-positioning discipline applied: no competitive platform named by contrast. BCSC forward-looking framing applied to open-source release path (Apache-2.0 option labelled "intended"). Bloomberg register throughout.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
