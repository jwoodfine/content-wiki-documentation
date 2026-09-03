---
schema: foundry-doc-v1
title: "How AI Is Used and Contained"
slug: ai-index
category: ai
type: topic
content_type: topic
quality: complete
short_description: "Where AI sits and where it is not allowed: the boundary that keeps AI away from the authoritative record, the routing between models, and the small, customer-side models designed to learn a customer's own environment. The core runs fully without it."
index_type: thematic
index_scope: ai
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-08-24
editor: pointsav-engineering
paired_with: _index.es.md
---

The **ai** category collects where AI sits in the platform and where it is not allowed. It covers the boundary that keeps AI away from the authoritative record, the routing between models, and the small, customer-side models designed to learn a customer's own environment. The deterministic core runs fully without AI.

This is the front door for the platform's most distinctive architectural claim — AI is used, and it is contained — and for engineers looking up a specific piece of the AI stack: the inference boundary, sovereign routing, the vendor-tier model programme, and the training pipelines that produce it.

<!-- START-HERE-HIGHLIGHT: engine reads this block to render the single "start here" card
     (reuses the existing cluster-card--start-here component). Do not add more than one. -->

**"The core runs fully without it"** is this category's own headline claim, and the article that argues it — [[substrate-without-inference-base-case]] — lives in [Building Blocks](/category/substrate), not here. Read it first if you're evaluating the containment claim itself; everything below assumes it.

<!-- END-START-HERE-HIGHLIGHT -->

## The Doorman boundary

The single gateway every inference call routes through — no service holds its own AI credentials or makes a direct outbound call.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: the-doorman-boundary -->
- [[doorman-protocol|Doorman protocol]] — the sole AI request boundary: three-tier routing, the audit ledger, the `moduleId` discipline
- [[sovereign-ai-routing|AI routing and the linguistic air-lock]] — the sanitize-outbound / rehydrate-inbound discipline enforced at that boundary before any data reaches an external model
- [[decode-time-constraints|Decode-time constraints]] — grammar rules applied at each token step, making banned vocabulary or invalid output mathematically impossible to produce
- [[slm-stack-architecture|SLM Rust stack architecture]] — the Rust dependency graph and binary architecture behind `service-slm`, the crate that implements the Doorman
<!-- END AUTO-GENERATED -->

## Compute tiers

Where inference actually runs, and the vendor-tier model this routes toward at the top.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: compute-tiers -->
- [[zero-container-inference|Zero-container inference]] — the planned Tier B GPU deployment pattern: native binaries under systemd, idle-shutdown timers instead of a container runtime
- [[pointsav-llm|PointSav-LLM]] — the planned Tier 3 vendor specialist model, not yet operational; forward-looking throughout
<!-- END AUTO-GENERATED -->

## Entity extraction and the training loop

How the platform turns use into training signal — the mechanism behind "the platform learns from how it gets used."

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: entity-extraction-and-training-loop -->
- [[tiered-entity-extraction-architecture|Tiered entity extraction architecture]] — the three-tier extraction pipeline per document: GLiNER extractive detection, OLMo generative fallback, GPU enrichment
- [[elastic-compute-lora-training-pipeline|Elastic Compute #1 nightly LoRA training pipeline]] — the nightly two-phase job that rebuilds the DataGraph and trains adapter weights
- [[learning-datagraph-architecture|Learning DataGraph]] — the four legs of training-signal capture: trajectory capture, apprenticeship queue, editorial DPO pairs, correction distillation
- [[flow-quality-architecture|Knowledge flow: training loop and ontological DataGraph]] — the quality framework asking whether the training loop and the DataGraph are actually working, not just running
<!-- END AUTO-GENERATED -->

## See also

- [How It's Built](/architecture/) — the three-ring build that makes this boundary structural
- [Building Blocks](/substrate/) — AI-adjacent mechanism concepts, including the AI-optionality article above
- [Platform Services](/services/) — the per-service pages, including the AI service itself
