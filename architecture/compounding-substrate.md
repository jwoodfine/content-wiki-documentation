---
schema: foundry-doc-v1
title: "The Compounding Substrate"
slug: compounding-substrate
category: architecture
type: topic
quality: complete
short_description: "The five structural properties that define PointSav's open-substrate architecture, where every operational interaction generates training signal that compounds across deployments while customers retain full ownership of data, compute, and governance."
status: pre-build
last_edited: 2026-04-30
editor: pointsav-engineering
cites:
  - ni-51-102
  - osc-sn-51-721
paired_with: compounding-substrate.es.md
---

The **Compounding Substrate** is the architectural pattern PointSav builds and stewards. It answers a single structural question: how does a software platform let every customer own their data, run on their own infrastructure, and compose AI in or out at will — while still benefiting from collective improvement without surrendering that ownership?

Five structural properties define the answer. Each is non-replicable by any vendor whose revenue depends on multi-tenant data centralisation. Together they produce a substrate that compounds: every operational interaction generates training signal; the signal flows to a curator; the curator rolls accumulated learning into improved base models; the improved models return to every deployment; and customer ownership of data, compute, and governance is preserved at every step.

This article introduces the pattern. The ratified specification lives at `conventions/compounding-substrate.md`. Doctrine context is at DOCTRINE.md §XIV (claims #14–#18).

## Substrate sovereignty

Every customer owns their full stack: data, compute, adapters, and deployment composition. The substrate code is open, forkable, and openly licensed. The base model carries open weights trained on openly declared data. The customer's data, adapters, and audit ledger never leave customer-controlled hardware.

A multi-tenant service-as-a-product cannot offer this by design. Its tenancy boundary is what prevents data co-mingling, enables centralised billing, and gates feature access. A substrate has no tenancy boundary in the data plane — only in the business plane (commercial-support contracts, certification programmes, training services). A tenant can be evicted; a substrate user cannot.

## Optional Intelligence Layer

AI is composed in, never built in. The deterministic data layer — filesystems, ledgers, knowledge graphs, search indexes — functions fully without any AI compute. AI is added when and where the customer chooses, at the tier they choose: local CPU model, GPU burst, or external API. The customer holds the routing configuration.

This is structurally distinct from products where AI is the primary interface. In a Compounding Substrate, AI is a peripheral — useful, optional, swappable, observable, and auditable. A regulated buyer who requires an air-gapped deployment with no AI at all can run the substrate at full capability. The substrate stays useful; the customer stays compliant.

## Three-tier compute routing

When AI operates, it routes among three tiers under explicit per-request policy:

- **Tier A (local)** — CPU-class small language model on the customer's own hardware. Default for most operations. Zero marginal cost; full data locality.
- **Tier B (GPU burst)** — short-lived GPU instance in the customer's cloud account, billed by inference-second. Used for workloads the local tier cannot handle efficiently. The owner controls start and stop; idle-shutdown is the default.
- **Tier C (external API)** — external vendor APIs used only with an explicit per-request allowlist. Audit-logged at the customer's substrate, not at the vendor. Used for narrow precision tasks the local and burst tiers cannot match.

The customer's configuration — request shape and budget caps — determines tier selection; no per-request manual choice is required. The substrate enforces an audit-ledger rule across all three tiers: every external call is recorded in the customer's per-tenant audit log with sanitised-outbound and rehydrate-inbound semantics.

## Federated compounding

The substrate's most distinctive property is its compounding mechanism. Every operational interaction — a refinement, a verdict, a classification, a clarification — generates a structured training signal. The signal accumulates locally in each customer's apprenticeship corpus. Periodically, customers who opt into federation contribute distilled signal to the curator (PointSav, in this substrate's instance). The curator rolls accumulated signal across many federations into an improved base model. The improved model flows back to every deployment. No customer's raw data leaves customer-controlled storage; only structurally distilled signal travels.

*The federation cadence is currently planned for quarterly cycles, with timing subject to the first full federation cycle. Actual cadence may differ materially based on operating conditions. Material assumptions include continued pretraining capability on the selected open base model family and customer opt-in to federation. [ni-51-102] [osc-sn-51-721]*

The curator role is itself a substrate property, not a vendor position. The curator is bound by the substrate's open-licence and audit obligations. A different curator can fork the role and the process if PointSav's stewardship breaks down. The substrate outlives its current curator.

## Continued pretraining as compounding

The structural advantage of this pattern is most visible in what the curator does: roll federation signal into continued pretraining of an open base model (currently OLMo 3 by Allen AI, Apache 2.0 licence), then redistribute the improved weights as the new substrate baseline. The customer's adapters — LoRA layers carrying per-tenant style, classification, and voice — are recompiled against the new baseline. The customer's deployment improves without the customer re-paying for the work; prior adapters still compose; the customer's data never moved.

This is what "the customer benefits from collective learning" means in an ownership-preserving architecture. Centralised pretraining requires centralised data access. The Compounding Substrate achieves the equivalent outcome through curator-mediated distilled signal. The customer can verify their data never left their hardware because the substrate's audit ledger and the curator's distilled-signal contract are both open and forkable.

## What this enables

Building on the substrate, customers can assemble capabilities that depend on the five structural properties above:

- **Vendor-obsolescence-survivable archives** — when the curator's organisation disappears, the data, deployments, adapters, and substrate remain readable, deployable, and improvable. A twenty-year-old archive opens on any forked substrate.
- **Air-gapped deployments with optional AI** — the substrate runs in environments where Tier C is impossible by policy. Tier A plus a local adapter plus customer-side audit produces the same classification, summarisation, and structured-output capabilities available to cloud customers.
- **Per-jurisdiction data residency** — customers in different jurisdictions run the same substrate with different audit ledgers and tenant configurations. The substrate is jurisdiction-neutral; the customer's compliance posture rides in the per-tenant configuration.
- **Cross-substrate composition** — a single deployment can run the bookkeeping substrate, the design-system substrate, the documentation substrate, and the proofreader substrate, all on shared identity, shared audit ledger, and shared three-ring architecture.

The Compounding Substrate is the platform's structural commitment to a market that requires giving up the centralisation that other platforms sell.

## See Also

- [[three-ring-architecture]] — the Ring 1 / Ring 2 / Ring 3 service composition that implements the Compounding Substrate
- [[service-slm]] — the Doorman service that routes across the three compute tiers and logs every call to the per-tenant audit ledger
- [[apprenticeship-substrate]] — how training signal accumulates in the per-customer corpus between federation cycles
- [[trajectory-substrate]] — session-level signal capture that feeds the apprenticeship corpus
- [[worm-ledger-architecture]] — the append-only immutable ledger that underpins the audit-log guarantee
- [[disclosure-substrate]] — how the substrate's open-licence and audit obligations apply to regulatory disclosure

## References

1. PointSav Doctrine §XIV, The Compounding Substrate — claims #14–#18 ratified workspace v0.0.4, 2026-04-25.
2. `conventions/compounding-substrate.md` — workspace canonical specification, ratified 2026-04-25.
3. `conventions/sovereign-ai-commons.md` — curator-of-the-commons framing and the commons/sovereign layer table.
4. `conventions/llm-substrate-decision.md` — OLMo 3 base model selection and continued-pretraining specifics.
5. NI 51-102, Continuous Disclosure Obligations (BCSC). [ni-51-102]
6. OSC Staff Notice 51-721, Forward-Looking Information Disclosure. [osc-sn-51-721]

---

## Provenance

Source material: workspace canonical specification `conventions/compounding-substrate.md` (ratified 2026-04-25); DOCTRINE.md §XIV (claims #14–#18); `conventions/three-ring-architecture.md`; `conventions/sovereign-ai-commons.md` curator framing.

Refinement disciplines applied: structural-positioning discipline (competitive-by-name references removed; structural contrasts retained); BCSC forward-looking adapter (quarterly federation cadence labelled per ni-51-102 / osc-sn-51-721); banned-vocabulary adapter (no substitutions required in source draft); body H1 removed per content-contract.md §5.2 (renderer supplies from title: frontmatter); slug set to `compounding-substrate` to match featured-topic.yaml pin; citations registered in citations.yaml.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
