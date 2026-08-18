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

**What changed in this rewrite.** A 2026-08-02 correction note on this article confirmed most of the specific stack described in earlier versions did not match the real `service-slm` codebase, and asked for a rewrite of the "canonical stack" and "flat binary architecture" sections against the real dependency graph rather than a wording fix. This is that rewrite — re-verified against source again, not just carrying the 2026-08-02 note forward, and it found further problems the note hadn't caught: an "L1/L2/L3" framework unrelated to the platform's real one, a third external service with no support in the codebase, and a self-contradiction about which inference engine is actually deployed.

[[service-slm|`service-slm`]] ships as a Rust cargo workspace of five real crates (`slm-core`, `slm-doorman`, `slm-doorman-server`, `adapter-hub`, `slm-mcp-server`) with two real `[[bin]]` targets (`slm-doorman-server`, `slm-mcp-server`) — not the single statically-linked binary earlier text claimed; no static-link (musl or similar) target configuration exists in the toolchain config. The workspace's own `ARCHITECTURE.md` calls this a "flat architecture" per binary, not one binary for the entire system.

The choice of Rust is not a language preference. It is an engineering constraint imposed by the intended deployment target — [[totebox-os|ToteboxOS]] appliance hardware, where a CPython interpreter plus a large ML framework does not fit in the available memory envelope, and where cold-start predictability and the absence of a garbage collector are operational requirements rather than optional improvements.

## The real "We Own It" framework — not the Rust-dependency taxonomy earlier text invented

Earlier versions of this article described a three-level "L1/L2/L3 Rust-ness" table grading how much of the dependency tree is Rust versus FFI, and called that the "We Own It" test. **That table does not correspond to any real framework in this codebase.** The actual "We Own It" concept, documented in `substrate/llm-substrate-decision.md` and `service-slm/docs/yoyo-training-substrate-and-service-content-integration.md`, grades **LLM openness**, not dependency-graph composition: L1 is open weights, L2 adds a permissive license, L3 requires the entire lineage — weights, training data, and code — to be openly licensed. OLMo 3 is cited in the real documentation as satisfying L3 under *this* framework, which is a claim about the model, not about how much of `service-slm`'s own Cargo dependency tree is written in Rust. The license-hygiene property earlier text was reaching for (no copyleft anywhere in the dependency graph, so PointSav holds an unrestricted right to fork, modify, and redistribute) is real and enforced by `cargo-deny` — it just isn't what "We Own It" means in this codebase's own vocabulary, and conflating the two invents a framework that doesn't exist.

## The canonical stack

### Inference layer

The inference runtime is **not** a Rust binary. Tier A runs **llama-server (llama.cpp)** and Tier B runs **vLLM** — both external, non-Rust processes called over HTTP (`service-slm/ARCHITECTURE.md`). `mistral.rs` and `candle` are not deployed anywhere in the current stack; `candle` appears only as a hypothetical future path in documentation, not as production infrastructure. Earlier text's claim that vLLM was "the Phase 1 trial inference engine, replaced by mistral.rs in Phase 2" is self-contradictory with the rest of this article's own correction history — vLLM is the actual, current Tier B runtime, with no replacement planned or underway.

The OLMo 3 model family is the production base model selection. OLMo 3 carries an Apache 2.0 code license and an Open Data Commons license for training data, making it the only major open-weight family whose entire lineage — weights, training data, and code — is permissively licensed end-to-end. This is the requirement for the [[apprenticeship-substrate]] training path, where PointSav exercises the right to run continued pretraining on customer-accumulated signal.

### HTTP and async runtime

The [[doorman-protocol|Doorman]]'s inbound HTTP surface is served by **axum** (MIT), with **tower** middleware for retries, timeouts, and backpressure, running on the **tokio** async runtime (MIT). Outbound HTTP calls use **reqwest**. These dependencies are confirmed in the real `Cargo.toml`.

### Storage and state

The audit ledger uses **rusqlite** with an SQLite backend, not `sqlx` as earlier text claimed — `Cargo.lock` has zero `sqlx` matches across all 286 packages in the workspace. The long-term knowledge graph (held by [[service-content]]) is LadybugDB. No `object_store` dependency was found for model-weight/adapter cloud storage; earlier text's claim there is unconfirmed.

### Document processing, orchestration, and observability — not real dependencies

Earlier text named a substantial document-processing and orchestration stack — `oxidize-pdf`, `docx-rust`, `calamine`, `pulldown-cmark` for document ingest; `apalis` for job orchestration; `opentelemetry-rust` for tracing export; `sigstore-rs` for artifact signing; `mupdf-rs` as an explicitly-excluded AGPL dependency. **None of these appear anywhere in the workspace's `Cargo.lock`.** This entire section of earlier text was invented, not merely imprecise — there is no real evidence any of this document-processing/orchestration/observability stack exists in `service-slm` today.

### License hygiene — confirmed real, with minor corrections

`cargo-deny` genuinely runs in CI with a real `deny.toml` policy file, confirmed by direct read. The allowed-license list is largely as earlier text described (`MIT`, `Apache-2.0`, `BSD-2-Clause`, `BSD-3-Clause`, `ISC`, `MPL-2.0` file-level, `Zlib`), with two corrections: the real file also allows `Apache-2.0 WITH LLVM-exception` and `CC0-1.0`, both omitted from earlier text; and the Unicode license entries are `Unicode-DFS-2016`/`Unicode-3.0` in the real file, not the bare `Unicode-DFS` earlier text used.

## ToteboxOS integration

The binary architecture is motivated in part by ToteboxOS deployment constraints. A CPython stack plus a GPU inference framework does not fit in the memory envelope available on constrained appliance hardware. A Rust binary with a quantised inference runtime operating in CPU mode does.

**The binding constraint on Laptop-A hosts is the 4 GB RAM envelope** — not the "~550 MB available headroom" figure earlier text cited, which has no source anywhere in the codebase; the real `ARCHITECTURE.md` states the 4 GB figure directly.

- Static binary per `[[bin]]` target, no interpreter warmup — seconds, not minutes to first inference
- No garbage collector, no interpreter heap
- True parallelism across cores without a global interpreter lock
- Cross-compilation via `cargo build --target aarch64-unknown-linux-gnu` for ARM ToteboxOS targets

## Two external non-Rust services — not three

Earlier versions of this article listed three external non-Rust services in the Yo-Yo compute substrate, including "SkyPilot" for multi-cloud GPU orchestration. **SkyPilot has zero references anywhere in the monorepo** and is dropped here rather than carried forward unverified. The two real ones:

**LMCache + Mooncake Store** (Python control plane + C++ Mooncake Transfer Engine): the KV cache tier that persists prefill state across GPU node teardowns. service-slm holds a Rust client that speaks to Mooncake over HTTP and TCP. No FFI coupling. Both are Apache-2.0 licensed.

**vLLM** (Python): the real, current Tier B inference engine (see Inference layer, above) — not a superseded trial, as earlier text claimed. Apache-2.0.

Both are behind stable network protocols; service-slm depends on the wire protocol, not the implementation. Swapping either requires changing one client module.

## See also

- [[compounding-doorman]] — the operational pattern service-slm implements
- [[yoyo-compute-substrate]] — the multi-ring compute substrate service-slm drives
- [[apprenticeship-substrate]] — how the audit ledger feeds LoRA adapter training
- [[three-ring-architecture]] — Ring 3 placement of service-slm in the platform
