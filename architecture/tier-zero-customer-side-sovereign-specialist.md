---
schema: foundry-doc-v1
title: "Tier 0 Customer-Side Sovereign Specialist"
slug: tier-zero-customer-side-sovereign-specialist
category: architecture
type: topic
quality: published
short_description: "The Tier 0 Totebox is a sovereign specialist deployment running on the customer's own hardware with no required cloud dependency and a 1 GB total footprint."
status: pre-build
last_edited: 2026-05-01
editor: pointsav-engineering
cites: []
paired_with: tier-zero-customer-side-sovereign-specialist.es.md
---

The **Tier 0 Customer-Side Sovereign Specialist** is the reference deployment model for Foundry: the complete platform stack running on the customer's own hardware, with no required cloud dependency, no required internet connectivity, and a total disk footprint of approximately one gigabyte. This pattern encodes Doctrine claim #49.

## The reference unit

The reference Tier 0 deployment is a Totebox — a small-form-factor x86 or ARM appliance. The full stack occupies approximately one gigabyte of disk and a two-to-four gigabyte working memory set on two to four CPU cores. No GPU is required.

The stack includes the WORM file ledger (`service-fs`), the knowledge runtime (`service-content`), the Doorman boundary (`service-slm`), the local specialist model (OLMo 2 1B at roughly 600 MB on disk), the operator TUI (`slm-cli`), and the input, extraction, and egress services. All components are self-contained binaries with no runtime dependencies beyond the operating system.

Hardware at this scale costs in the range of three hundred to fifteen hundred dollars depending on the customer's size and requirements. The intended monthly operating cost is zero — there is no subscription, no recurring cloud fee, and no per-seat charge.

## Why a specialist rather than a generalist

The local model on the Totebox is a purpose-routed sysadmin specialist. It handles system administration and IT-support questions, mechanical edits such as commit messages and schema validation, routine queries against the customer's audit ledger and knowledge graph, and short-output tasks.

It is not intended for editorial work, bilingual generation, or long-form reasoning. Those tasks route to the optional GPU burst tier when available, or return a graceful "tier unavailable" response when not. The specialist's value is that it handles a large fraction of daily operational queries quickly and with zero marginal cost — questions that would otherwise consume expensive API calls or require a heavier model.

## Empirical basis for CPU-only inference

The Tier A claim rests on measured performance rather than theoretical capability: on a four-vCPU CPU-only deployment, the 1B parameter model at four-bit quantization produces approximately seven tokens per second, yielding end-to-end responses in the range of six seconds for typical 40-token answers. This is fast enough for human-conversational use. The operator types a question; the specialist responds in seconds.

No GPU acquisition, no driver maintenance, and no thermal management are required. The hardware profile is the same class as any other internal appliance the customer already operates.

## Sovereignty properties

The Totebox operates without Foundry's servers, without any continuing relationship with the model's original authors (existing files work indefinitely), without external API keys (Tier C is opt-in and off by default), without internet connectivity, and without any cloud subscription. The substrate works fully offline.

The [[substrate-without-inference-base-case]] convention extends this: even the AI tier itself is optional. The deterministic Ring 1 and Ring 2 services — the ledger, the knowledge graph, and the processing services — operate independently of the AI tier. The Totebox is the customer's property in the strongest sense.

## Hardware scale

For a five-person business, a mini-PC class appliance is sufficient. For a thirty-person firm, a slightly larger appliance handles concurrent Ring 1, Ring 2, and AI tier operations. For a three-hundred-person firm or a regional hospital, a multi-unit cluster with an optional GPU box is intended. The Foundry commercial focus is the first two scales; larger deployments are possible but not the primary market.

## Optional tiers

Tier B (GPU burst capacity) is opt-in per tenant. The customer chooses between arranged GPU cloud capacity or a customer-owned GPU box. Tier B routes through the customer's local Doorman, preserving audit and boundary discipline. It is used for tasks the local specialist cannot handle efficiently — editorial, bilingual, and long-form reasoning work.

Tier C (external API) is opt-in per tenant and off by default. When configured, external API calls are limited to an explicit allowlist of purposes, are audit-logged at the customer's ledger rather than the vendor's, and are disclosed to the operator. Most customers are intended to operate without Tier C entirely.

## See Also

- [[substrate-without-inference-base-case]] — deterministic-only operation when all AI tiers are unavailable
- [[single-boundary-compute-discipline]] — all inference, including the local specialist, routes through the Doorman
- [[seed-taxonomy-as-smb-bootstrap]] — the per-tenant taxonomy that the Tier 0 deployment boots with

## References

1. Doctrine claim #49 — Tier 0 Customer-Side Sovereign Specialist (ratified v0.1.0).
2. Empirical validation: workspace VM Tier A swap, 2026-04-30 — OLMo 2 1B Q4 at 7 tokens/second on CPU.

---

## Provenance

Source: `convention-tier-zero-customer-side-sovereign-specialist.md` (refined 2026-04-30). Workspace-internal file paths and open questions removed. Hardware cost estimates and market analysis presented as structural observations; BCSC forward-looking framing applied to commercial focus claims.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
