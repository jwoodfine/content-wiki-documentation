---
schema: foundry-doc-v1
title: "PointSav-LLM"
slug: pointsav-llm
category: ai
type: topic
content_type: topic
quality: complete
index_group: compute-tiers
short_description: "The planned vendor-tier specialist AI model for substrate-sovereign SMBs — Tier 3 of the Four-Tier SLM Substrate Ladder, built by continued pretraining of the OLMo 3 32B base model (not the Think variant earlier text named — AllenAI has not published a 32B-Think variant)."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-08-17
editor: pointsav-engineering
cites:
 - ni-51-102
 - osc-sn-51-721
paired_with: pointsav-llm.es.md

---

**PointSav-LLM** is the planned Tier 3 specialist AI model in [[pointsav-overview|PointSav]]'s [[four-tier-slm-substrate|Four-Tier SLM Substrate Ladder]] — the vendor-trained layer that is intended to emerge from continued pretraining of the OLMo 3 32B base model (Apache 2.0) on the platform's federated, multi-tenant [[apprenticeship-substrate|apprenticeship corpus]]. Internal engineering documentation describes this specifically as CPT of the 32B **base** model, not a "32B Think" variant — AllenAI has not published a Think variant at the 32B size, so that framing in earlier text was not just imprecise but referred to a model that does not exist. It is not an active product. It is a planned trajectory: a first continued-pretraining (CPT) cycle is currently targeted for v0.5.0, Q1 2027, with a productized deployment currently targeted for v1.0.0, Q4 2027. When operational, PointSav-LLM is intended to serve small and medium-sized businesses that require a specialist model trained on PointSav conventions, [[totebox-archive|Totebox Archive]] operations, and multi-tenant editorial patterns — without requiring the infrastructure investment or minimum-spend commitments that closed-source enterprise AI products impose.

*All capability descriptions, timelines, pricing structures, and performance targets in this article are forward-looking. They are planned or intended, not current operational facts. Actual outcomes depend on corpus growth rate, model performance, engineering capacity, and market conditions. [ni-51-102] [osc-sn-51-721]*

---

## What PointSav-LLM is intended to be

PointSav-LLM is planned as a narrow specialist, not a general-purpose model. Its intended training corpus comes from the platform's aggregated, multi-tenant apprenticeship substrate: the trajectory logs, editorial decision pairs, escalation records, and code-aligned commit histories produced by contributing AI agent sessions across the platform.

When the first CPT cycle completes, the model is intended to demonstrate depth in:

- **Totebox Archive operation** — query patterns, ingestion formats, tenant namespace isolation, and ledger-consistency checks specific to PointSav's storage substrate.
- **PointSav conventions** — platform commit patterns, mailbox protocol structure, repo-layout discipline, and the Tetrad milestone format.
- **Multi-tenant editorial patterns** — the PROSE / COMMS / LEGAL / TRANSLATE adapter families, bilingual pairing conventions, BCSC-posture editing, and banned-vocabulary substitution.
- **Code generation aligned to the platform** — Rust workspace conventions, Ring 1/2/3 service boundaries, and the three-tier compute routing interface.
- **Federated training contribution** — the mechanics by which a customer's contributing-tier subscription routes anonymized trajectory data back into the corpus, compounding the model's value over each CPT cycle.

### What it is not intended to be

What PointSav-LLM is not intended to be is equally important. It is not planned to compete with broad-capability frontier models on general knowledge, creative breadth, or multi-domain reasoning. Customers whose queries require that breadth will continue routing those requests through Tier C external API calls (Anthropic Claude, Google Gemini) via the [[doorman-protocol|Doorman]]'s classification logic. PointSav-LLM is intended to serve the narrow slice of queries where specialist depth and per-token economics matter more than frontier-model breadth.

The OLMo 3 base (Apache 2.0; Open Data Commons for training data) means the base weights are open. Customer-portable adapters are planned to preserve tenancy sovereignty — a customer who leaves the platform is intended to retain the right to carry their contributed data and any tenant-specific fine-tune they funded. This is a structural property of the planned architecture, not a contractual carve-out.

---

## How customers are intended to access it

The planned access path routes entirely through each customer's local [[doorman-protocol|Doorman]]. No customer sends queries directly to a PointSav-LLM API endpoint. The sequence, as currently designed:

1. Customer application sends a query to the local [[doorman-protocol|Doorman]] (127.0.0.1:9080 by default).
2. Doorman classifies query complexity using the current Tier A local model (OLMo 3 7B Q4).

**Correction (2026-08-17, citation fixed — the underlying finding was real, the prior
citation to `service-slm/NEXT.md` was not; no file by that name exists anywhere in the
monorepo).** The Tier A model name genuinely is inconsistent across the real engineering
source, confirmed by direct search, not by wiki cross-referencing alone: the canonical
registry (`service-slm/data/base-registry.yaml`) sets `allenai/OLMo-3-7B-Instruct` as
Tier A — matching this article and the Four-Tier table below — but several other real
docs disagree with the canonical registry and with each other: `docs/topic-claude-code-
sovereign-routing.md`, `docs/guide-activate-anthropic-shim.md`, and `docs/topic-tos-
training-constraints.md` all say "OLMo 2 1B," while `docs/guide-post-commit-training-
hook.md` and `crates/adapter-hub/src/lib.rs` say "OLMo-2-7B." [[learning-datagraph-
architecture]]'s own prior "OLMo-2 7B Q4" claim has since been corrected there to match
the canonical registry (OLMo 3, not OLMo 2) — this article's "OLMo 3 7B Q4" was already
right. The underlying inconsistency in the engineering docs themselves is real and still
unresolved — **flagged, not resolved** — needs project-totebox confirmation of which
non-canonical doc references should be updated to match `base-registry.yaml`.
3. For queries classified as simple or routine, the Doorman routes to Tier A and returns a local response — no external call.
4. For queries classified as requiring specialist depth (domain-specific platform conventions, [[totebox-archive|Totebox Archive]] operations, multi-tenant editorial structure), the Doorman is intended to route to the PointSav-LLM Tier C endpoint, authenticating via the customer's provisioned API key.
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

This exact JSON shape does not exist in code today, which is expected for a Tier 3 product that has no operational state — but a differently-shaped, currently-real mechanism for a related, distinct purpose is worth noting as design precedent: `slm-core/src/apprenticeship.rs` already gates internal agent apprenticeship trajectories on `self_confidence: f32` and an `escalate: bool` flag, threshold `APPRENTICE_ESCALATE_THRESHOLD = 0.5`. That mechanism governs whether an AI session's own attempt gets escalated to a senior reviewer inside this workspace — it is not a customer-facing PointSav-LLM response envelope, and should not be cited as evidence this feature is built. It is evidence the general pattern (confidence score → threshold → escalation) already has one working implementation to design the customer-facing version against.

### Escalation events as training data

Escalation events are planned to become training data. A resolved escalation — where a human engineer provides the correct answer — is intended to generate a Direct Preference Optimization (DPO) pair that feeds back into the next CPT cycle via the apprenticeship-substrate pipeline. The intended tiering:

| Tier | Planned handling | Target query share (planned) |
|------|-----------------|------------------------------|
| L1 | Autonomous PointSav-LLM response | ~80–90% of queries (planned) |
| L2 | Human-in-the-loop escalation | Remaining automated queries |
| L3 | Engineering-tier escalation surfaced from unresolved L2 | Edge cases |

All percentages are planned targets, not current operational data — and unlike most other figures in this article, no design document or prototype was found backing the specific ~80–90% split; treat it as illustrative rather than a sourced estimate until one exists.

**Related, currently-real infrastructure, for a different tier of the commercial ladder.** `crates/adapter-hub/src/lib.rs` implements substantial, working LoRA/adapter infrastructure today — but it serves customer-tenant and commit-graph adapters (the commercial ladder's Tier 1/2), not the Tier 3 CPT model this article describes. It's the closest thing to "something has already been built" in this space, and worth knowing about, but it answers a different question than PointSav-LLM's own readiness.

---

## Market positioning

The customer-service and enterprise-knowledge AI market in 2026 is served primarily by fully-managed, closed-source products structured for large enterprise buyers. Minimum contract commitments, per-seat pricing floors, and data-residency terms designed for multi-thousand-person organizations make these products structurally inaccessible to most small and medium-sized businesses.

SMBs with 10–200 employees that require AI assistance across their archive operations, editorial workflows, or customer-service function face two options under the current market structure: absorb pricing aimed at organizations an order of magnitude larger, or operate without AI assistance. A third option — self-hosting open-source general-purpose models — requires ML infrastructure expertise that most SMBs do not have.

### Serving the SMB gap

PointSav-LLM is intended to serve this gap. The planned architecture routes specialist queries through a vendor-maintained model without requiring customers to provision GPU infrastructure, manage model updates, or negotiate enterprise-tier contracts. The per-token pricing model, when published, is intended to be accessible at SMB contract sizes. The open OLMo 3 base and the Designed-for-Breakout Tenancy principle mean customers are not structurally locked in.

The commercial logic mirrors the open-source software service model: the base training weights are open (Apache 2.0); the commercial line is the value PointSav adds — specialist CPT on the aggregated platform corpus, the human-in-the-loop escalation infrastructure, the per-tenant audit and compliance substrate, and the SLA. Customers who contribute trajectory data to the corpus under the contributing tier are intended to receive preferential per-token rates, as their data compounds the model's specialist depth for every subsequent subscriber.

---

## Pricing structure (planned trajectory)

Three planned subscription tiers, details and specific token rates not yet published:

**Open tier (free, community contributor)**
- Intended access: knowledge-commons read access, community forum, public documentation.
- Model access: Tier A local model only (customer-hosted).
- Corpus contribution: not included.
- Target entry point: individuals and organizations contributing to the knowledge commons, with a target of 10,000 or more registered users at the platform level.

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

PointSav-LLM occupies Tier 3 of the planned Four-Tier SLM Substrate Ladder. The four tiers, as currently designed:

| Tier | Name | Base | Status |
|------|------|------|--------|
| 0 | Deterministic core | Rules, regex, structured lookup | Operational |
| A | Local small model | OLMo 3 7B Q4 (CPU) | Operational (local llama-server) |
| B | Burst compute | `Olmo-3-1125-32B-Think` (GPU via Yo-Yo) | Operational |
| C | Vendor specialist | PointSav-LLM (planned CPT of OLMo 3 32B base) | Planned — Q1 2027 |

Tiers 0, A, and B are operational today. Tier C (PointSav-LLM) is planned, with no operational state at the time of this article. The Doorman's routing logic for Tier C is planned infrastructure; its current state is Tier A/B routing only.

**A real distinction this table's own "0/A/B/C" numbering blurs.** The engineering source (`slm-core/src/tier.rs`) uses `InferenceRoute` (`Local`/`Yoyo`/`External`) for the technical compute tiers this table calls A/B/C — and its own code comment explicitly warns this naming is chosen "to avoid colliding with the unrelated customer-facing commercial tier ladder (Tier 0/1/2/3)." That commercial ladder (the Open/Paid-C/Paid-C+ pricing tiers described later in this article) is a genuinely separate numbering scheme from the technical A/B/C compute-routing tiers, even though this table's single "0/A/B/C" column visually merges them into one ladder. Worth keeping distinct in any future revision of this table, not collapsing further.

---

## See also

- [[compounding-substrate]] — the five structural properties that enable the federated CPT path
- [[service-slm-yoyo-operational]] — the current Tier A/B operational state this article describes Tier 3 of
- [[apprenticeship-substrate]] — the DPO loop that feeds the CPT corpus
- [[brief-queue-substrate]] — durable queue for brief accumulation
- [[contributor-model]] — the Three-Tier Contributor Model aligned with pricing tiers
- [[service-slm|SLM Service]] — the local model service that PointSav-LLM is intended to extend at Tier C
- [[slm-stack-architecture|SLM Stack Architecture]] — the Four-Tier SLM Substrate Ladder this article describes Tier 3 of

---

## References

1. AllenAI. *OLMo 3 model family*. Apache 2.0 license; training data under Open Data Commons license. https://allenai.org/olmo
2. *National Instrument 51-102 Continuous Disclosure Obligations.* British Columbia Securities Commission. [ni-51-102]
3. *OSC Staff Notice 51-721: Forward-Looking Information Disclosure.* Ontario Securities Commission. [osc-sn-51-721]
