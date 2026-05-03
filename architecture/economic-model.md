---
schema: foundry-doc-v1
title: "Economic Model — Community and SMB Customer Tiers"
slug: economic-model
category: architecture
type: topic
quality: published
short_description: "PointSav's two-tier commercial structure: a free Community tier that serves as an adoption funnel, and a paid SMB Customer tier targeting regulated small-to-medium businesses that hyperscalers cannot serve economically."
status: pre-build
last_edited: 2026-05-01
editor: pointsav-engineering
cites: []
paired_with: economic-model.es.md
---

PointSav's commercial structure has two tiers. There is no Enterprise tier. The decision is not a positioning choice — it is a structural one. Regulated small-to-medium businesses occupy a market segment hyperscalers cannot reach economically, and the platform is designed entirely around serving that segment.

## The two tiers

**Community** is the free tier. It operates under an AGPL-3.0-or-later license. A Community deployment consists of one ToteboxOS archive and one ConsoleOS terminal, with local model inference available as an optional component. Community is the adoption funnel: it generates contributors, surfaces edge cases, and makes the substrate legible to future customers. PointSav earns no revenue from Community deployments.

**SMB Customer** is the revenue tier. It operates under a Functional Source License with an Apache-2.0 fallback after the Delay Open-Source Publication period, plus a commercial license where required. SMB Customer deployments include multi-archive aggregation via os-orchestration, GPU burst capability, federated LoRA marketplace participation, and priority access to updated base models as they are produced. The commercial relationship is an Order Form per customer.

## Why no Enterprise tier

The addressable customer for an Enterprise-tier AI platform typically runs annual contract values above $500,000. Hyperscalers are structured for that segment — their sales organisations, compliance certifications, and infrastructure commitments reflect it. PointSav is not equipped to compete there, and should not try.

The segment PointSav targets runs annual contract values of $5,000 to $50,000 for AI tooling. That gap — too small for an enterprise motion, too regulated for a consumer product — is structurally inaccessible to platforms built around hyperscale billing models.

The 2026 evidence is consistent: GPU pricing at neoclouds is structurally lower than at hyperscalers, a substantial fraction of hyperscaler customers report billing unpredictability, and hyperscaler capital expenditure commitments for AI infrastructure continue to rise. These trends do not help SMBs; they increase the pricing floor those customers face.

## The addressable SMB segment

Regulated SMBs share three properties that define the market:

1. They are too small for an enterprise sales motion at hyperscaler minimums.
2. They are too regulated for consumer or unmanaged AI — HIPAA, PIPEDA, GDPR, FINRA, and equivalent Canadian provincial frameworks apply.
3. They require their data and their AI to remain on infrastructure they control.

Examples include small clinics subject to health privacy legislation, regional law firms with privilege and confidentiality obligations, mid-cap financial advisors with regulatory reporting requirements, and real-estate operators maintaining corporate document archives. These customers are not edge cases. They are the mainstream of the regulated economy below the enterprise threshold.

## Federation

Federation capabilities — the federated LoRA marketplace, the Mooncake KV pool, and base model updates as they are produced — are included in the SMB Customer license. There is no separate federation tier. Every paying customer may participate; privacy-preserving federated learning techniques are mature enough in 2026 to make this structurally sound.

## Continued pretraining as a curatorial investment

PointSav's investment in continued pretraining of the base model — the production of PointSav-OLMo-N variants — is funded by SMB Customer license revenue and benefits every customer when an updated base is distributed in the next platform release. The economic structure resembles that of a Linux distribution: curation is funded by the subscription business; customers run their own installations; the improved base returns to the full subscriber base.

## The cost asymmetry

The economics that protect this position are straightforward. LoRA fine-tuning of a seven-billion-parameter model costs in the range of $30 to $100 per adapter. Continued pretraining of that same model costs $30,000 to $100,000. Pretraining from scratch at that scale costs $500,000 to $2,000,000.

SMBs can do LoRA fine-tuning on their own data. They cannot do continued pretraining. PointSav does continued pretraining. Federation pools the learning from per-customer LoRA adapters into a commons that improves the base for everyone. This asymmetry is structural: it does not depend on any particular competitive outcome. It depends on the economics of compute at scale, which are unlikely to invert.

## Service availability by tier

Ring 1 services (boundary ingest: filesystem, people, email, and input) and Ring 2 services (knowledge and processing: content, extraction, search, and egress) are available in both tiers. Ring 3 services differ: Community includes optional local model inference; SMB Customer adds GPU burst, external API integration, multi-archive aggregation, federation, and access to updated base models. Support and integration services are community-forum only for Community and contracted for SMB Customer.

## See Also

- [[compounding-substrate]] — the five structural properties this economic model funds
- [[sovereign-ai-commons]] — the market positioning of the substrate as a commons
- [[llm-substrate-decision]] — how the model choice maps to Community and SMB Customer capability tiers
- [[four-tier-slm-substrate]] — the four deployment tiers within the SMB Customer model

## References

1. PointSav factory-release-engineering `LICENSE-MATRIX.md` — authoritative license assignment per tier.
2. `conventions/sovereign-ai-commons.md` — structural market positioning.
3. `conventions/economic-model.md` — source convention for this article.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
