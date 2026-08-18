---
schema: foundry-doc-v1
title: "SLM Rust stack architecture"
slug: slm-stack-architecture
category: ai
type: topic
content_type: topic
quality: complete
index_group: the-doorman-boundary
short_description: "The full Rust dependency graph and binary architecture for service-slm, the Doorman service that mediates every inference call in the PointSav platform."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-08-17
editor: pointsav-engineering
cites: []
paired_with: slm-stack-architecture.es.md

---

[[service-slm|`service-slm`]] ships as a Rust cargo workspace of five crates (`slm-core`, `slm-doorman`, `slm-doorman-server`, `adapter-hub`, `slm-mcp-server`) with two `[[bin]]` targets (`slm-doorman-server`, `slm-mcp-server`) — a flat architecture per binary, not a single statically-linked binary for the entire system.

The choice of Rust is not a language preference. It is an engineering constraint imposed by the intended deployment target — [[totebox-os|ToteboxOS]] appliance hardware, where a CPython interpreter plus a large ML framework does not fit in the available memory envelope, and where cold-start predictability and the absence of a garbage collector are operational requirements rather than optional improvements.

## The "We Own It" framework

"We Own It" grades LLM openness, not dependency-graph composition: L1 is open weights, L2 adds a permissive license, L3 requires the entire lineage — weights, training data, and code — to be openly licensed. OLMo 3 satisfies L3 under this framework.

Separately, the dependency graph itself carries no copyleft license anywhere, so PointSav holds an unrestricted right to fork, modify, and redistribute — a property enforced by `cargo-deny`, distinct from the We Own It grading above.

## The canonical stack

### Inference layer

The inference runtime is **not** a Rust binary. Tier A runs **llama-server (llama.cpp)** and Tier B runs **vLLM** — both external, non-Rust processes called over HTTP. `mistral.rs` and `candle` are not deployed anywhere in the current stack; `candle` appears only as a hypothetical future path, not production infrastructure. vLLM is the current, production Tier B runtime, with no replacement planned.

The OLMo 3 model family is the production base model selection. OLMo 3 carries an Apache 2.0 code license and an Open Data Commons license for training data, making it the only major open-weight family whose entire lineage — weights, training data, and code — is permissively licensed end-to-end. This is the requirement for the [[apprenticeship-substrate]] training path, where PointSav exercises the right to run continued pretraining on customer-accumulated signal.

### HTTP and async runtime

The [[doorman-protocol|Doorman]]'s inbound HTTP surface is served by **axum** (MIT), with **tower** middleware for retries, timeouts, and backpressure, running on the **tokio** async runtime (MIT). Outbound HTTP calls use **reqwest**.

### Storage and state

The audit ledger uses **rusqlite** with an SQLite backend. The long-term knowledge graph (held by [[service-content]]) is LadybugDB. No dependency for model-weight/adapter cloud storage is present in the stack today.

### Document processing, orchestration, and observability

None of these are part of the stack today: no PDF/DOCX ingestion libraries, no job-orchestration framework, no tracing exporter, and no artifact-signing dependency exist in this workspace.

### License hygiene

`cargo-deny` runs in CI. The allowed-license list is `MIT`, `Apache-2.0`, `Apache-2.0 WITH LLVM-exception`, `BSD-2-Clause`, `BSD-3-Clause`, `CC0-1.0`, `ISC`, `MPL-2.0` (file-level), `Unicode-DFS-2016`, `Unicode-3.0`, and `Zlib`.

## ToteboxOS integration

The binary architecture is motivated in part by ToteboxOS deployment constraints. A CPython stack plus a GPU inference framework does not fit in the memory envelope available on constrained appliance hardware. A Rust binary with a quantised inference runtime operating in CPU mode does.

**The binding constraint on Laptop-A hosts is a 4 GB RAM envelope.**

- Static binary per `[[bin]]` target, no interpreter warmup — seconds, not minutes to first inference
- No garbage collector, no interpreter heap
- True parallelism across cores without a global interpreter lock
- Cross-compilation via `cargo build --target aarch64-unknown-linux-gnu` for ARM ToteboxOS targets

## Two external non-Rust services

The Yo-Yo compute substrate depends on two external, non-Rust services:

**LMCache + Mooncake Store** (Python control plane + C++ Mooncake Transfer Engine): the KV cache tier that persists prefill state across GPU node teardowns. service-slm holds a Rust client that speaks to Mooncake over HTTP and TCP. No FFI coupling. Both are Apache-2.0 licensed.

**vLLM** (Python): the current Tier B inference engine (see Inference layer, above). Apache-2.0.

Both are behind stable network protocols; service-slm depends on the wire protocol, not the implementation. Swapping either requires changing one client module.

## See also

- [[compounding-doorman]] — the operational pattern service-slm implements
- [[yoyo-compute-substrate]] — the multi-ring compute substrate service-slm drives
- [[apprenticeship-substrate]] — how the audit ledger feeds LoRA adapter training
- [[three-ring-architecture]] — Ring 3 placement of service-slm in the platform
