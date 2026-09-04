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
last_edited: 2026-09-04
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
- [[doorman-protocol|Doorman protocol]] — The Doorman is the sole AI request boundary through which every inference call routes, holding every external-model credential and logging every call to an immutable audit ledger.
- [[sovereign-ai-routing|AI routing and the linguistic air-lock]] — AI routing holds every external-model credential and audit-logs every request at a single boundary. It does not scrub PII from prompts, and Tier C external routing is not live yet.
- [[decode-time-constraints|Decode-time constraints]] — The constrained-decoding technique, and a clear line between it and what PointSav has built today: an advisory post-generation linter, with the grammar-based mechanism itself planned, not shipped.
- [[slm-stack-architecture|SLM Rust stack architecture]] — The full Rust dependency graph and binary architecture for service-slm, the Doorman service that mediates every inference call in the PointSav platform.
<!-- END AUTO-GENERATED -->

## Compute tiers

Where inference actually runs, and the vendor-tier model this routes toward at the top.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: compute-tiers -->
- [[zero-container-inference|Zero-container inference]] — Tier B GPU deployment pattern using native Linux binaries under systemd on an L4 GPU, with idle detection run from the Doorman server process rather than a timer on the GPU VM itself.
- [[pointsav-llm|PointSav-LLM]] — The planned vendor-tier specialist AI model for substrate-sovereign SMBs — Tier 3 of the Four-Tier SLM Substrate Ladder, built by continued pretraining of the OLMo 3 32B base model.
<!-- END AUTO-GENERATED -->

## Entity extraction and the training loop

How the platform turns use into training signal — the mechanism behind "the platform learns from how it gets used."

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: entity-extraction-and-training-loop -->
- [[tiered-entity-extraction-architecture|Tiered entity extraction architecture]] — The entity extraction pipeline runs three tiers per document: Tier 0 fast extractive detection via GLiNER, Tier A generative fallback via OLMo, Tier B GPU enrichment.
- [[elastic-compute-lora-training-pipeline|Elastic Compute #1 nightly LoRA training pipeline]] — Nightly two-phase pipeline on Elastic Compute #1 that rebuilds the deployment DataGraph and trains LoRA adapter weights for the workspace language model.
- [[learning-datagraph-architecture|Learning DataGraph]] — Training loop turning operator interactions into training signal — trajectory capture, an apprenticeship queue, and a GLiNER→OLMo distillation pipeline that generates entity-extraction DPO pairs.
- [[flow-quality-architecture|Knowledge flow: training loop and ontological DataGraph]] — Quality framework for the Totebox knowledge flow, asking whether LoRA adapters measurably improve the model and whether the DataGraph is an accurate ontology.
<!-- END AUTO-GENERATED -->

## See also

- [How It's Built](/architecture/) — the three-ring build that makes this boundary structural
- [Building Blocks](/substrate/) — AI-adjacent mechanism concepts, including the AI-optionality article above
- [Platform Services](/services/) — the per-service pages, including the AI service itself
