---
schema: foundry-doc-v1
title: "Economic model — community and SMB customer tiers"
slug: economic-model
category: architecture
type: topic
quality: complete
short_description: "PointSav's two-tier commercial structure: a free Community tier that serves as an adoption funnel, and a paid SMB Customer tier targeting regulated small-to-medium businesses that hyperscale billing models cannot serve economically."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-22
editor: pointsav-engineering
cites: []
paired_with: economic-model.es.md
---

A regulated small business sits in a gap. It is too small for an enterprise AI contract — those begin in the hundreds of thousands of dollars a year — and too regulated to run its data through a consumer AI product. Neither sales motion reaches it.

[[pointsav-overview|PointSav]]'s commercial structure is built entirely around that gap. <!--claim id=two-tiers-no-enterprise confidence=structural cites=[]-->There are two tiers and no Enterprise tier: a free Community tier that is the adoption funnel, and a paid SMB Customer tier for regulated small-to-medium businesses.<!--/claim-->

<!--claim id=structural-not-positional confidence=structural cites=[]-->The decision is structural, not positional. The target segment runs AI-tooling contracts of roughly 5,000 to 50,000 dollars a year — too small for an enterprise sales motion, too regulated for a consumer product — and the platform's cost structure is designed to serve it profitably.<!--/claim-->

For a buyer in that segment, the platform's economics are aligned with theirs. This article covers the two tiers, why there is no Enterprise tier, the addressable segment, federation, and the cost asymmetry that protects the position.

## The two tiers

<!--claim id=community-tier confidence=structural cites=[]--><strong>Community</strong> is the free tier, under an AGPL-3.0-or-later licence. A Community deployment is one [[totebox-os|ToteboxOS]] archive and one [[console-os|ConsoleOS]] terminal, with local model inference as an optional component. Community is the adoption funnel — it generates contributors and surfaces edge cases — and [[pointsav-overview|PointSav]] earns no revenue from it.<!--/claim-->

<!--claim id=smb-tier confidence=structural cites=[]--><strong>SMB Customer</strong> is the revenue tier, under a Functional Source License with an Apache-2.0 fallback after the delay period, plus a commercial licence where required. An SMB Customer deployment adds multi-archive aggregation, GPU burst capability, federated adapter-marketplace participation, and priority access to updated base models. The relationship is an Order Form per customer.<!--/claim-->

## Why no Enterprise tier

The addressable customer for an Enterprise-tier AI platform typically runs annual contract values above 500,000 dollars. Hyperscale providers are structured for that segment — their sales organisations, compliance certifications, and infrastructure commitments reflect it. [[pointsav-overview|PointSav]] is not equipped to compete there and does not try.

<!--claim id=the-gap confidence=structural cites=[]-->The segment [[pointsav-overview|PointSav]] targets runs annual AI-tooling contract values of 5,000 to 50,000 dollars. That gap — too small for an enterprise motion, too regulated for a consumer product — is structurally inaccessible to a platform built around a hyperscale billing model.<!--/claim-->

The 2026 market evidence is consistent: GPU pricing at specialist providers runs structurally below hyperscale pricing, a substantial fraction of hyperscale customers report billing unpredictability, and capital-expenditure commitments for AI infrastructure continue to rise. None of these trends help a small business; each raises the pricing floor it faces.

## The addressable SMB segment

Regulated small-to-medium businesses share three properties that define the market.

1. They are too small for an enterprise sales motion at hyperscale minimums.
2. They are too regulated for consumer or unmanaged AI — HIPAA, PIPEDA, GDPR, FINRA, and equivalent Canadian provincial frameworks apply.
3. They require their data and their AI to remain on infrastructure they control.

Examples include small clinics under health-privacy legislation, regional law firms with privilege and confidentiality obligations, mid-cap financial advisors with regulatory reporting requirements, and real-estate operators maintaining corporate document archives. These are not edge cases. They are the mainstream of the regulated economy below the enterprise threshold.

## Federation

<!--claim id=federation-included confidence=structural cites=[]-->Federation capabilities — the federated adapter marketplace, the shared key-value cache pool, and base-model updates — are included in the SMB Customer licence. There is no separate federation tier; every paying customer may participate.<!--/claim-->

## Continued pretraining as a curatorial investment

<!--claim id=linux-distro-model confidence=structural cites=[]-->[[pointsav-overview|PointSav]]'s investment in continued pretraining of the base model is funded by SMB Customer licence revenue, and the improved base benefits every customer when it ships in the next platform release. The economic structure resembles a Linux distribution: curation is funded by the subscription business, customers run their own installations, and the improved base returns to the full subscriber base.<!--/claim-->

## The cost asymmetry

The economics that protect this position are straightforward. Adapter fine-tuning of a seven-billion-parameter model costs roughly 30 to 100 dollars per adapter. Continued pretraining of that same model costs 30,000 to 100,000 dollars. Pretraining from scratch at that scale costs 500,000 to 2,000,000 dollars.

<!--claim id=cost-asymmetry confidence=structural cites=[]-->A small business can fine-tune adapters on its own data; it cannot fund continued pretraining. [[pointsav-overview|PointSav]] funds the continued pretraining, and federation pools the per-customer adapter learning into a commons that improves the base for everyone. The asymmetry does not depend on any particular competitive outcome — it depends on the economics of compute at scale.<!--/claim-->

## Service availability by tier

[[three-ring-architecture|Ring 1]] services (boundary ingest) and Ring 2 services (knowledge and processing) are available in both tiers. Ring 3 differs: Community includes optional local model inference; SMB Customer adds GPU burst, external API integration, multi-archive aggregation, federation, and access to updated base models. Support is community-forum only for Community and contracted for SMB Customer.

## See also

- [[compounding-substrate]] — the five structural properties this economic model funds
- [[sovereign-ai-commons]] — the market positioning of the substrate as a commons
- [[llm-substrate-decision]] — how the model choice maps to Community and SMB Customer capability tiers
- [[four-tier-slm-substrate]] — the four deployment tiers within the SMB Customer model
