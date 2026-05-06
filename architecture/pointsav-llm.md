---
schema: foundry-doc-v1
title: "PointSav-LLM"
slug: pointsav-llm
category: architecture
type: topic
quality: core
short_description: "The planned vendor-tier specialist AI model for substrate-sovereign SMBs — Tier 3 of the Four-Tier SLM Substrate Ladder, built by continued pretraining of OLMo 3 32B on Foundry's federated apprenticeship corpus."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-04-30
editor: pointsav-engineering
cites:
  - ni-51-102
  - osc-sn-51-721
paired_with: pointsav-llm.es.md
---

**PointSav-LLM** is the planned Tier 3 specialist AI model in PointSav's Four-Tier SLM Substrate Ladder — the vendor-trained layer that is intended to emerge from continued pretraining of OLMo 3 32B Think (Apache 2.0) on Foundry's federated, multi-tenant apprenticeship corpus. It is not an active product. It is a planned trajectory: a first continued-pretraining (CPT) cycle is currently targeted for v0.5.0, Q1 2027, with a productized deployment currently targeted for v1.0.0, Q4 2027. When operational, PointSav-LLM is intended to serve small and medium-sized businesses that require a specialist model trained on PointSav conventions, Totebox Archive operations, and multi-tenant editorial patterns — without requiring the infrastructure investment or minimum-spend commitments that closed-source enterprise AI products impose.

*All capability descriptions, timelines, pricing structures, and performance targets in this article are forward-looking. They are planned or intended, not current operational facts. Actual outcomes depend on corpus growth rate, model performance, engineering capacity, and market conditions. [ni-51-102] [osc-sn-51-721]*

---

## What PointSav-LLM is intended to be

PointSav-LLM is planned as a narrow specialist, not a general-purpose model. Its intended training corpus comes from Foundry's aggregated, multi-tenant apprenticeship substrate: the trajectory logs, editorial decision pairs, escalation records, and code-aligned commit histories produced by contributing Task Claude sessions across the platform.

When the first CPT cycle completes, the model is intended to demonstrate depth in:

- **Totebox Archive operation** — query patterns, ingestion formats, tenant namespace isolation, and ledger-consistency checks specific to PointSav's storage substrate.
- **PointSav conventions** — Foundry commit patterns, mailbox protocol structure, repo-layout discipline, and the Tetrad milestone format.
- **Multi-tenant editorial patterns** — the PROSE / COMMS / LEGAL / TRANSLATE adapter families, bilingual pairing conventions, BCSC-posture editing, and banned-vocabulary substitution.
- **Code generation aligned to Foundry** — Rust workspace conventions, Ring 1/2/3 service boundaries, and the three-tier compute routing interface.
- **Federated training contribution** — the mechanics by which a customer's contributing-tier subscription routes anonymized trajectory data back into the corpus, compounding the model's value over each CPT cycle.

What PointSav-LLM is not intended to be is equally important. It is not planned to compete with broad-capability frontier models on general knowledge, creative breadth, or multi-domain reasoning. Customers whose queries require that breadth will continue routing those requests through Tier C external API calls (Anthropic Claude, Google Gemini) via the Doorman's classification logic. PointSav-LLM is intended to serve the narrow slice of queries where specialist depth and per-token economics matter more than frontier-model breadth.

The OLMo 3 base (Apache 2.0; Open Data Commons for training data) means the base weights are open. Customer-portable adapters are planned to preserve tenancy sovereignty per Doctrine claim #28 (Designed-for-Breakout Tenancy): a customer who leaves the platform is intended to retain the right to carry their contributed data and any tenant-specific fine-tune they funded. This is a structural property of the planned architecture, not a contractual carve-out.

---

## How customers are intended to access it

The planned access path routes entirely through each customer's local Doorman. No customer sends queries directly to a PointSav-LLM API endpoint. The sequence, as currently designed:

1. Customer application sends a query to the local Doorman (127.0.0.1:9080 by default).
2. Doorman classifies query complexity using the current Tier A local model (OLMo 3 7B Q4).
3. For queries classified as simple or routine, the Doorman routes to Tier A and returns a local response — no external call.
4. For queries classified as requiring specialist depth (domain-specific Foundry conventions, Totebox Archive operations, multi-tenant editorial structure), the Doorman is intended to route to the PointSav-LLM Tier C endpoint, authenticating via the customer's provisioned API key.
5. The response returns through the Doorman. An audit row is written simultaneously at the customer's local Doorman and at the PointSav-LLM gateway — two-ledger, per-call audit trail.
6. Per-token billing is computed at the gateway and reported to the customer's subscription account.

The customer's application code does not change between Tier A local routing and Tier C PointSav-LLM routing. The Doorman is the single routing surface. This is a structural property inherited from the three-tier compute routing architecture already operational in the Yo-Yo substrate (Tier B).

---

## Human-in-the-loop design

PointSav-LLM is intended to carry explicit confidence signalling. When the model's output confidence falls below a threshold (the specific threshold to be calibrated during the first CPT cycle), the response envelope is planned to include:

```json
{
  "confidence": "low",
  "escalate_to_human": true,
  "escalation_reason": "<structured tag>"
}
```

The customer's Doorman, on receiving this envelope, is intended to surface an escalation prompt to the end user — for example, "Ask a PointSav engineer." The customer does not see the raw confidence score; they see a product-level prompt tuned to their configured language and escalation SLA.

Escalation events are planned to become training data. A resolved escalation — where a human engineer provides the correct answer — is intended to generate a Direct Preference Optimization (DPO) pair that feeds back into the next CPT cycle via the apprenticeship-substrate pipeline (Doctrine claim #32). The intended tiering:

| Tier | Planned handling | Target query share (planned) |
|------|-----------------|------------------------------|
| L1 | Autonomous PointSav-LLM response | ~80–90% of queries (planned) |
| L2 | Human-in-the-loop escalation | Remaining automated queries |
| L3 | Engineering-tier escalation surfaced from unresolved L2 | Edge cases |

All percentages are planned targets, not current operational data.

---

## Market positioning

The customer-service and enterprise-knowledge AI market in 2026 is served primarily by fully-managed, closed-source products structured for large enterprise buyers. Minimum contract commitments, per-seat pricing floors, and data-residency terms designed for multi-thousand-person organizations make these products structurally inaccessible to most small and medium-sized businesses.

SMBs with 10–200 employees that require AI assistance across their archive operations, editorial workflows, or customer-service function face two options under the current market structure: absorb pricing aimed at organizations an order of magnitude larger, or operate without AI assistance. A third option — self-hosting open-source general-purpose models — requires ML infrastructure expertise that most SMBs do not have.

PointSav-LLM is intended to serve this gap. The planned architecture routes specialist queries through a vendor-maintained model without requiring customers to provision GPU infrastructure, manage model updates, or negotiate enterprise-tier contracts. The per-token pricing model, when published, is intended to be accessible at SMB contract sizes. The open OLMo 3 base and the Designed-for-Breakout Tenancy principle (Doctrine claim #28) mean customers are not structurally locked in.

The commercial logic mirrors the open-source software service model: the base training weights are open (Apache 2.0); the commercial line is the value PointSav adds — specialist CPT on the aggregated Foundry corpus, the human-in-the-loop escalation infrastructure, the per-tenant audit and compliance substrate, and the SLA. Customers who contribute trajectory data to the corpus under the contributing tier are intended to receive preferential per-token rates, as their data compounds the model's specialist depth for every subsequent subscriber.

---

## Pricing structure (planned trajectory)

Three planned subscription tiers, details and specific token rates not yet published:

**Open tier (free, community contributor)**
- Intended access: knowledge-commons read access, community forum, public documentation.
- Model access: Tier A local model only (customer-hosted).
- Corpus contribution: not included.
- Target entry point: individuals and organizations contributing to the knowledge commons, currently targeted at 10,000 or more registered users at the platform level per Doctrine claim #23 (§7.3).

**Paid Tier C (per-token, subscription)**
- Intended access: PointSav-LLM API via Doorman routing.
- Per-token pricing: intended to be accessible at SMB contract sizes; specific rates not yet published.
- Corpus contribution: read-only; contributes anonymized query telemetry.
- SLA: standard response-time commitments.

**Paid Tier C+ (premium)**
- Intended access: PointSav-LLM API with escalation SLA bucket.
- Pricing: per-token plus reserved escalation hours.
- Corpus contribution: full contributing-tier trajectory data, intended to generate preferential per-token rates in subsequent billing cycles as compounding credit.
- SLA: enhanced response-time commitments plus L2/L3 escalation response window.

Specific token rates and escalation SLA windows will be published when the first CPT cycle assessment data is available. All pricing is planned and subject to revision based on infrastructure costs, model performance, and market conditions. [ni-51-102] [osc-sn-51-721]

---

## Relationship to the Four-Tier SLM Substrate Ladder

PointSav-LLM occupies Tier 3 of the planned Four-Tier SLM Substrate Ladder (Doctrine claim #40). The four tiers, as currently designed:

| Tier | Name | Base | Status |
|------|------|------|--------|
| 0 | Deterministic core | Rules, regex, structured lookup | Operational |
| A | Local small model | OLMo 3 7B Q4 (CPU) | Operational (Yo-Yo substrate) |
| B | Burst compute | OLMo 3.1 32B Think (GPU via Yo-Yo) | Operational |
| C | Vendor specialist | PointSav-LLM (planned CPT of OLMo 3 32B) | Planned — Q1 2027 |

Tiers 0, A, and B are operational today. Tier C (PointSav-LLM) is planned, with no operational state at the time of this article. The Doorman's routing logic for Tier C is planned infrastructure; its current state is Tier A/B routing only.

---

## See Also

- [[compounding-substrate]] — the five structural properties that enable the federated CPT path
- [[service-slm-yoyo-operational]] — the current Tier A/B operational state this article describes Tier 3 of
- [[apprenticeship-substrate]] — the DPO loop that feeds the CPT corpus
- [[brief-queue-substrate]] — durable queue for brief accumulation
- [[contributor-model]] — the Three-Tier Contributor Model aligned with pricing tiers

---

## References

1. PointSav Doctrine claim #15 — Continued-pretraining path: the planned mechanism by which Foundry's aggregated corpus feeds vendor-tier specialist model development.
2. PointSav Doctrine claim #23 — Knowledge Commons / Service Commerce: the open-knowledge access tier and the commercial service layer built on top of it.
3. PointSav Doctrine claim #28 — Designed-for-Breakout Tenancy: customer-portable adapters and data-sovereignty protections that prevent structural lock-in.
4. PointSav Doctrine claim #32 — Apprenticeship Substrate: the DPO-loop mechanism that converts human-in-the-loop escalation resolutions into next-cycle training data.
5. PointSav Doctrine claim #40 — Four-Tier SLM Substrate Ladder: the full ladder from deterministic core (Tier 0) through vendor specialist (Tier C).
6. AllenAI. *OLMo 3 model family*. Apache 2.0 license; training data under Open Data Commons license. https://allenai.org/olmo
7. *National Instrument 51-102 Continuous Disclosure Obligations.* British Columbia Securities Commission. [ni-51-102]
8. *OSC Staff Notice 51-721: Forward-Looking Information Disclosure.* Ontario Securities Commission. [osc-sn-51-721]

---

## Provenance

Source material: PointSav Doctrine claims #15, #40; `conventions/four-tier-slm-substrate.md`; `conventions/llm-substrate-decision.md`; `conventions/apprenticeship-substrate.md`; `conventions/knowledge-commons.md`. Research on customer-service AI market structure and pricing consulted. All capability and timeline statements in this article are planned trajectory per BCSC disclosure posture. [ni-51-102] [osc-sn-51-721]

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*

*Woodfine Capital Projects™, Woodfine Management Corp™, PointSav Digital Systems™, Totebox Orchestration™, and Totebox Archive™ are trademarks of Woodfine Capital Projects Inc., used in Canada, the United States, Latin America, and Europe. All other trademarks are the property of their respective owners.*
