---
schema: foundry-doc-v1
title: "The Sovereign AI Commons"
slug: sovereign-ai-commons
category: architecture
type: topic
quality: published
short_description: "PointSav's market positioning as a steward of shared, open AI infrastructure for regulated small-to-medium businesses: five structural properties that large-scale cloud providers cannot offer without dismantling their own billing models."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-01
editor: pointsav-engineering
cites: []
paired_with: sovereign-ai-commons.es.md
---

PointSav builds and stewards a sovereign AI commons — a substrate, a protocol stack, and a federation designed for small-to-medium businesses that need sovereign AI without surrendering data ownership or paying for infrastructure they cannot control.

The architecture specification is in the [[compounding-substrate]] article. The economic structure is in [[economic-model]]. This article is the market-positioning frame: who the commons serves, what makes it structurally distinct, and what PointSav's role within it is.

## The market the commons serves

Regulated small-to-medium businesses. Not large enterprise accounts — those are served by platforms with sales organisations, procurement relationships, and compliance certifications structured for six-figure annual contracts. Not consumer applications — those are unregulated and served by mass-market products. The segment in between is where the commons operates.

The defining characteristics of the target customer:

- Annual contract value for AI tooling in the range of $5,000 to $50,000 — below the minimum economically viable for an enterprise sales motion
- Regulatory exposure under frameworks including HIPAA, PIPEDA, GDPR, FINRA, and equivalent provincial regulations
- A requirement that data and AI infrastructure remain on infrastructure the customer controls, not a vendor's cloud

Small clinics, regional law firms, mid-cap financial advisors, real-estate operators with corporate document archives, small public-sector contractors, and family offices describe this segment concretely. These customers are collectively large — the regulated SMB economy is a substantial fraction of commercial activity in developed markets — but individually too small and too regulated for the platforms built around hyperscale economics.

## What is commons, what is sovereign

The distinction matters. The substrate code, the base model, the protocol specifications, and the published research into federated learning techniques are commons: open, shared, improved by collective contribution. The customer's data graph, the customer's per-tenant LoRA adapters, the customer's tenant configuration, and the customer's audit ledger are sovereign: they stay on the customer's infrastructure and do not leave without the customer's explicit action.

Commons increases the value of sovereign deployments: every customer's substrate is improved by improvements that any participant contributes to the shared base. Sovereign deployments protect what makes each customer distinctive. The two are co-designed rather than in tension.

## Five structural properties unavailable elsewhere

The platform's design incorporates five properties that are, taken together, structurally inaccessible to large-scale cloud providers:

**Substrate sovereignty.** The substrate code is open and forkable. A customer who wants to operate independently of the vendor has a complete path to do so. For a managed cloud service, forking the substrate would undermine the revenue model; the architecture cannot be structured that way.

**Optional intelligence.** Rings 1 and 2 — all deterministic data handling and knowledge processing — function fully without the AI layer at Ring 3. Customers can run the platform without AI, add AI when they have a specific use for it, and withdraw it without losing the rest of the system. For a platform where AI compute is the primary revenue source, making AI genuinely optional removes the commercial incentive.

**Multi-tier compute routing.** The Doorman selects among a local model, a GPU burst instance, and external API services per request. The selection spans infrastructure that includes competitors' frontier models at Tier C. No single organisation controls all three tiers, and the customer's routing configuration governs which tier handles which request.

**Federated compounding.** The intended path to improving the platform's AI capability involves pooling privacy-preserved training signal from many customers' LoRA adapters into improvements to a shared base model. Per-tenant billing and compliance structures make this arrangement unavailable to platforms where each customer's data is held by the vendor under a managed-service agreement.

**Continued-pretraining path.** The base model is OLMo 3, published under Apache 2.0 with full training data and training code available. This is the only 2026 non-Chinese open model that permits a deploying organisation to continue training the base, starting from a known checkpoint, on corpus material that the deploying organisation itself accumulates. The intended outcome — a customer-owned specialised base model — requires this property. It is unavailable from any model where the training data is closed.

## PointSav's role

PointSav operates as a steward, not a gatekeeper. The distinction is operational:

What PointSav does: operates the protocol stack under a governance structure designed to be transferred to a constitutional convention; curates the base model through planned continued pretraining; operates the federation infrastructure for the LoRA marketplace and KV pool; sells ToteboxOS appliances, integration, and support; and maintains the reference deployment.

What PointSav does not do: lock customers into PointSav infrastructure; hold customer data under a managed-service arrangement; charge for AI compute as the primary revenue source; compete with large-scale cloud providers on volume cloud AI.

## The 2030 intended trajectory

The commons' intended trajectory over the following years, as currently planned:

By 2030, the intended outcome includes a PointSav-OLMo-N model variant that is competitive with frontier proprietary models on regulated SMB tasks; a base of federation-active SMB customer deployments; a versioned protocol stack that has been ratified through constitutional convention; and recognition as a reference implementation of open AI infrastructure for the regulated SMB market.

These are forward-looking statements based on the platform's current design and trajectory. They carry material assumptions: that the OLMo 3 license terms remain in effect, that GPU compute costs continue to decline, that the federated learning techniques underlying the marketplace remain viable at scale, and that the platform reaches the customer base necessary to fund continued pretraining. Each assumption could be disrupted. The structural foundation for the trajectory is in place; the execution remains to be demonstrated.

## See Also

- [[compounding-substrate]] — the five structural properties in architectural detail
- [[economic-model]] — the two-tier commercial structure that funds the commons
- [[llm-substrate-decision]] — why OLMo 3 enables the continued-pretraining path
- [[four-tier-slm-substrate]] — the four deployment tiers customers move through

## References

1. `conventions/sovereign-ai-commons.md` — source convention for this article.
2. `conventions/compounding-substrate.md` — five structural properties in architectural detail.
3. `conventions/economic-model.md` — two-tier commercial structure.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*

*Woodfine Capital Projects™, Woodfine Management Corp™, PointSav Digital Systems™, Totebox Orchestration™, and Totebox Archive™ are trademarks of Woodfine Capital Projects Inc., used in Canada, the United States, Latin America, and Europe. All other trademarks are the property of their respective owners.*
