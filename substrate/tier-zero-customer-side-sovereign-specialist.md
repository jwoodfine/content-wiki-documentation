---
schema: foundry-doc-v1
title: "Tier 0 customer-side sovereign specialist"
slug: tier-zero-customer-side-sovereign-specialist
category: substrate
type: topic
content_type: topic
quality: complete
index_group: sovereignty-and-customer-ownership
short_description: "The Tier 0 Totebox is a sovereign specialist deployment running on the customer's own hardware with no required cloud dependency and no required internet connectivity."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-01
editor: pointsav-engineering
cites: []
paired_with: tier-zero-customer-side-sovereign-specialist.es.md
---

The **Tier 0 Customer-Side Sovereign Specialist** is the reference deployment model for the platform: the complete platform stack running on the customer's own hardware, with no required cloud dependency and no required internet connectivity. It is the operational form of [[customer-hostability]].

## The reference unit

The reference Tier 0 deployment is a Totebox — a small-form-factor x86 or ARM appliance. The platform's own deterministic services (the ledger, the knowledge runtime, the input/extraction/egress services) are a few hundred megabytes of self-contained binaries; the local specialist model, a quantized 7B-parameter OLMo 3 build, is by far the largest single component on disk, several gigabytes at 4-bit quantization. No GPU is required.

The stack includes the [[worm-ledger-architecture|WORM file ledger]] (`service-fs`), the knowledge runtime ([[service-content|`service-content`]]), the [[compounding-doorman|Doorman boundary]] (`service-slm`), the local specialist model (OLMo 3 7B Instruct, quantized), the operator interface ([[app-console-slm|app-console-slm]]), and the input, extraction, and egress services. All components are self-contained binaries with no runtime dependencies beyond the operating system.

Hardware at this scale costs in the range of three hundred to fifteen hundred dollars depending on the customer's size and requirements. The intended monthly operating cost is zero — there is no subscription, no recurring cloud fee, and no per-seat charge.

## Why a specialist rather than a generalist

The local model on the Totebox is a purpose-routed sysadmin specialist. It handles system administration and IT-support questions, mechanical edits such as commit messages and schema validation, routine queries against the customer's audit ledger and knowledge graph, and short-output tasks.

It is not intended for editorial work, bilingual generation, or long-form reasoning. Those tasks route to the optional GPU burst tier when available, or return a graceful "tier unavailable" response when not. The specialist's value is that it handles a large fraction of daily operational queries quickly and with zero marginal cost — questions that would otherwise consume expensive API calls or require a heavier model.

## CPU-only inference

The Tier A specialist is a quantized 7B-parameter model, larger than the class of model that would be expected to run comfortably on shared CPU cores — but the specialist's routed workload (short-output classification, mechanical edits, ledger and knowledge-graph lookups) tolerates a slower per-token rate than interactive long-form generation would. The operator types a question; the specialist responds within a few seconds for a typical short answer, without a GPU.

No GPU acquisition, no driver maintenance, and no thermal management are required. The hardware profile is the same class as any other internal appliance the customer already operates.

## Sovereignty properties

The Totebox operates without the platform's servers, without any continuing relationship with the model's original authors (existing files work indefinitely), without external API keys (Tier C is opt-in and off by default), without internet connectivity, and without any cloud subscription. The substrate works fully offline.

The [[substrate-without-inference-base-case]] convention extends this: even the AI tier itself is optional. The deterministic Ring 1 and Ring 2 services — the ledger, the knowledge graph, and the processing services — operate independently of the AI tier. The Totebox is the customer's property in the strongest sense.

## Hardware scale

For a five-person business, a mini-PC class appliance is sufficient. For a thirty-person firm, a slightly larger appliance handles concurrent Ring 1, Ring 2, and AI tier operations. For a three-hundred-person firm or a regional hospital, a multi-unit cluster with an optional GPU box is intended. The platform's commercial focus is the first two scales; larger deployments are possible but not the primary market.

## Optional tiers

Tier B ([[yoyo-compute-substrate|GPU burst capacity]]) is opt-in per tenant. The customer chooses between arranged GPU cloud capacity or a customer-owned GPU box. Tier B routes through the customer's local [[compounding-doorman|Doorman]], preserving audit and boundary discipline. It is used for tasks the local specialist cannot handle efficiently — editorial, bilingual, and long-form reasoning work.

Tier C (external API) is opt-in per tenant and off by default. When configured, external API calls are limited to an explicit allowlist of purposes, are audit-logged at the customer's ledger rather than the vendor's, and are disclosed to the operator. Most customers are intended to operate without Tier C entirely.

## See also

- [[substrate-without-inference-base-case]] — deterministic-only operation when all AI tiers are unavailable
- [[single-boundary-compute-discipline]] — all inference, including the local specialist, routes through the Doorman
- [[seed-taxonomy-as-smb-bootstrap]] — the per-tenant taxonomy that the Tier 0 deployment boots with
