---
schema: foundry-doc-v1
title: "The Four-Tier SLM Substrate Ladder"
slug: four-tier-slm-substrate
category: architecture
type: topic
quality: published
short_description: "A graduated sovereignty path for AI deployment: four customer tiers from a lightweight API gateway with no local model up through a domain-specialist AI service trained on the vendor's aggregated corpus, each tier adding capability without breaking the lower-tier guarantee."
status: pre-build
last_edited: 2026-05-01
editor: pointsav-engineering
cites: []
paired_with: four-tier-slm-substrate.es.md
---

The PointSav platform structures AI deployment as a four-tier ladder. Customers start at the tier that matches their current hardware, budget, and sovereignty requirements. Each higher tier adds capability. Dropping back to a lower tier at any point does not break the substrate the customer already operates — it simply removes the premium capability.

The ladder is the operational form of the platform's designed-for-breakout principle: every customer owns their substrate end-to-end at every tier, and the commercial value the platform adds is in the capabilities above the floor, not in lock-in to vendor infrastructure.

## Tier 0 — Community member, no local model

At Tier 0 the Doorman operates as a pure API gateway. No language model runs locally. The Doorman holds the customer's keys for whichever Tier C external service they have configured, routes requests through a per-purpose allowlist, and logs every call to the local audit ledger.

Tier 0 is available on any hardware that can run ToteboxOS. It is appropriate for solo operators, community contributors, and customers evaluating the platform before committing to local hardware. The Ring 1 and Ring 2 services — all deterministic knowledge and processing — function fully without a language model at Ring 3. Intelligence is optional.

## Tier 1 — Local OLMo 7B plus external API access

At Tier 1 the customer runs OLMo 3 7B Think locally. A consumer GPU with 8 GB of VRAM is sufficient; the quantised model works on CPU with 8 GB of RAM at reduced throughput. The Doorman routes most requests to the local model at Tier A; it routes heavier requests to Tier C external services when configured; and it routes requests to the vendor-hosted 32B model if the customer has subscribed to Tier 2.

Tier 1 is the baseline for SMB Customer deployments. It provides offline-capable narrow AI participation and selective access to larger inference capacity, without giving up data locality for routine operations.

At Tier 1, the customer's per-tenant LoRA adapter training is available. A first adapter can be trained on a corpus of roughly 1,000 to 5,000 high-quality preference pairs from the customer's own operational history. That adapter lives on the customer's ToteboxOS instance and does not leave it unless the customer explicitly opts into the federated marketplace.

## Tier 2 — Vendor-hosted 32B model (Yo-Yo)

At Tier 2 the vendor operates a 32B model on a GPU burst instance with idle-shutdown discipline. From the customer's perspective, this is a Tier C service accessed by their local Doorman — a hosted endpoint that handles requests the local 7B model is not well-suited to. From the vendor's perspective, it is the same infrastructure the vendor uses for its own heavyweight inference tasks, made available to customers as a subscription service.

The Tier 2 model is OLMo 3.1 32B Think. At runtime, a composition of adapters is applied per request: a constitutional adapter reflecting current platform doctrine, an engineering adapter trained on accumulated platform corpus, and tenant-specific adapters where applicable. No external API keys are held by the inference engine itself; key custody remains exclusively at the Doorman boundary.

The pricing structure is intended to sit structurally below that of fully-managed AI platforms requiring annual contracts in the six-figure range. This is a planned commercial position, not yet published rate-card pricing.

## Tier 3 — PointSav-LLM specialist service (planned)

Tier 3 is a planned standalone AI service trained via continued pretraining on the vendor's aggregated multi-tenant corpus. It is not a LoRA adapter applied to a base model — it is a new base model, produced by following the published AI2 continued-pretraining recipe: 100 billion tokens of midtraining, long-context extension, and post-training alignment.

The intended result, at the planned scale of 32B parameters, is a model with deep operational familiarity with the PointSav platform: archive deployment and configuration, standard editorial patterns, code generation aligned to platform conventions, and the mechanics of federated contribution. It would operate as a multi-tenant API service, accessible from customer Doorman instances via a per-customer authentication token with the same shape as any Tier C external key.

Tier 3 incorporates a structured escalation path: queries the model cannot handle with adequate confidence are flagged for human review. Human responses to flagged queries are captured as training signal that feeds the next continued-pretraining cycle, closing the loop between customer support and model improvement.

The first PointSav-OLMo-N continued-pretraining run is planned to begin in 2027, subject to corpus accumulation targets and operational readiness. The timeline carries material uncertainty.

## API key boundary discipline

A single rule applies across all tiers: API keys are held only at the Doorman boundary. No downstream service, no inference engine, and no Ring 2 process holds a vendor key. The Doorman is the single point of key custody, the single point of call auditing, and the single point of per-purpose allowlist enforcement. This matches the consensus pattern for production AI gateway deployments in 2026.

## The upgrade and downgrade path

Tier graduation is additive. Moving from Tier 0 to Tier 1 adds local hardware and the first LoRA training cycle. Moving from Tier 1 to Tier 2 adds the burst subscription. Moving from Tier 2 to Tier 3 adds the specialist service subscription. At each graduation, the capabilities of the lower tier remain fully functional.

Downgrading is equally clean. A customer who drops the Tier 3 subscription retains their local Tier 1 substrate. Their LoRA adapters, their audit ledger, and their knowledge graph remain on their own hardware. This is the structural guarantee that the commercial relationship is about capability, not captivity.

## Two structural market gaps

The federated LoRA marketplace — where customers contribute privacy-preserved adapter signal to a commons that improves the base for all participants — has no shipping commercial analogue in 2026. All technical components (privacy-preserving federated learning frameworks, differential privacy primitives, adapter-only exchange protocols) are mature. The marketplace with payment rails is an unclaimed position.

The open-substrate customer-service specialist — a domain-expert AI accessible at per-token pricing within reach of SMB contract values, built on a fully open model base — is also unclaimed in 2026. Managed AI services for the customer-service vertical operate at price floors that structurally exclude PointSav's target market. Tier 3 as described is intended to occupy this gap, pending the continued-pretraining timeline above.

## See Also

- [[compounding-doorman]] — the Doorman boundary that enforces the key custody rule across all tiers
- [[llm-substrate-decision]] — why OLMo 3 is the base model across all tiers
- [[apprenticeship-substrate]] — the training loop that makes higher tiers compound over time
- [[economic-model]] — how the four tiers map to Community and SMB Customer commercial tiers

## References

1. AllenAI OLMo 3 blog — continued pretraining recipe and model architecture.
2. `conventions/four-tier-slm-substrate.md` — source convention for this article.
3. Federated LoRA framework paper, arXiv 2502.05087 — privacy-preserving federated learning foundations.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
