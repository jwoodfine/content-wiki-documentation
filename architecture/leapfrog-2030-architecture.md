---
schema: foundry-doc-v1
title: "The leapfrog 2030 architecture"
slug: leapfrog-2030-architecture
category: architecture
type: concept
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-15
editor: pointsav-engineering
paired_with: leapfrog-2030-architecture.es.md
cites:
 - ni-51-102
 - osc-sn-51-721
references:
 - id: 1
 text: "IDC. 'The SMB 2026 Digital Landscape: How AI is Redefining Growth.' IDC Research, 2026."
 url: "https://www.idc.com/resource-center/blog/the-smb-2026-digital-landscape-how-ai-is-redefining-growth/"
 - id: 2
 text: "Anthropic, Google, and contributors. 'Model Context Protocol Specification.' modelcontextprotocol.io, 2024."
 url: "https://modelcontextprotocol.io/"
---

Three market forces converging in 2026 — viable small language models on commodity hardware, the Model Context Protocol as the standard for AI-native service composition, and on-premises as the fastest-growing SMB deployment type — open a structural gap that hyperscaler vendors cannot close without dismantling their own business model. The Leapfrog 2030 architecture is PointSav's commitment to that gap: sovereign platform code, composable services, and transactional revenue rather than recurring license fees. The customer owns their hardware, their data, and their adapter weights; PointSav takes a transaction percentage when value flows. This article covers the five structural shifts the thesis describes, the substrate that realizes them, and the compounding loop that makes the commitment durable over time.

## The five structural shifts

| From (incumbent pattern) | To (PointSav pattern) |
|---|---|
| Rented SaaS interface | Owned operating system |
| Centralised vendor cloud database | Per-entity [[totebox-os|Totebox]] archive |
| Username + password (RBAC) | Hardware-bound pairing ([[machine-based-auth|MBA]]) |
| Single source of truth | Self-healing claims ledger |
| 50-page annual audit reports | Machine-readable continuous proof |

Each shift is a single architectural decision with downstream consequences. Each is enforced at the kernel or protocol layer, not by policy.

## What the thesis is not

The thesis is not anti-cloud. PointSav uses commercial cloud providers extensively. It is not anti-AI. PointSav embeds language models throughout the architecture. It is not a rejection of open source. PointSav's core operating systems are intended for release under Apache 2.0.

The thesis is structural: the asset the customer owns is the running instance, not a subscription seat.

## Why now

Three institutional currents converge in 2026. First, small open-weight language models have crossed the usability threshold for narrow-domain work: OLMo 2 1B Instruct produces production-viable sysadmin output at five to fifteen tokens per second on commodity 4-vCPU hardware. Second, the Model Context Protocol has become the standard for AI-native service composition [^2]. Third, on-premises is the fastest-growing deployment type within the SMB software market [^1].

These three forces open a structural gap.

Hyperscaler vendors are committed to concentrated compute plus integrated stack plus recurring revenue. Their SMB tier is a discounted enterprise tier. Their AI features require ongoing data flow into their cloud. Their pricing assumes the customer is renting capability, not owning it.

The opening is for a different commitment: sovereign substrate plus composable services plus transactional revenue. The customer owns their hardware, their data, their adapter weights, and their relationships. PointSav Digital Systems is the substrate provider; the customer is the substrate operator; revenue flows when value flows.

## What "leapfrog 2030" means

Three structural distinctions from the hyperscaler stack:

**Sovereignty over service.** The customer's [[totebox-os|Totebox]] — the customer data vault, a compact on-premises appliance — is designed to boot, run, query, audit, and export without any PointSav-side dependency. If PointSav Digital Systems ceases operations, the customer's substrate is intended to continue functioning. This is not a backup feature; it is the designed default operational mode.

**Specialisation over generalisation.** The Tier A inference tier — always-on, customer-side — is a 1-billion-parameter sysadmin specialist, not a 32-billion-parameter generalist. It runs on commodity CPU. It trains on the customer's own engineering and IT-support corpus. Over time it becomes specifically useful for that customer's environment. The generalist tier (Tier B, 32B class on GPU) is opt-in and on-demand; the precision tier (Tier C, external API) is rare and sovereignty-disclosed.

**Compounding over capture.** PointSav Digital Systems's intended revenue compounds with the customer's revenue, not against it. The Direct-Payment Settlement substrate is designed to route data marketplace and ad-exchange transactions directly from buyer to customer; PointSav takes a transaction percentage at settlement, not a subscription fee on access. The customer is intended to be a revenue partner, not a license-payer.

## The substrate at a glance

A deployment composes three rings:

**Ring 1 — Boundary Ingest.** Per-tenant MCP servers handling inbound data: service-fs (WORM ledger), service-input (file, email, and voice), [[service-extraction]] (entity extraction), [[service-people]] (CRM), [[service-email]]. Each is bounded, auditable, and deterministic at its baseline.

**Ring 2 — Knowledge and Processing.** Multi-tenant via module identifier: [[service-content]] (the per-tenant graph and vector store), [[service-egress]] (outbound formatting), service-marketplace (data marketplace gateway), service-ad-exchange (IAB OpenRTB 2.6+ gateway), service-settlement (Stripe Connect and crypto rail).

**Ring 3 — Optional Intelligence.** [[service-slm]] Doorman as MCP gateway; Tier A 1B sysadmin specialist (always-on); Tier B 32B generalist (on-demand GPU pool or customer GPU, on-demand); Tier C external API (rare; allowlist-gated).

The Single-Boundary Compute Discipline makes the Doorman the only path to inference compute. Bearer tokens, API keys, and endpoint URLs live exclusively in the Doorman's configuration. Bypass is structurally prevented — by firewall, UID-owner iptables, and bearer-only-in-Doorman — not by policy alone.

## How it works for the small business

A 5-employee business installs a [[totebox-os|Totebox]]: a $300–$500 mini-PC on site. The Totebox runs the substrate stack — ledger, knowledge graph, ingest, and the 1B sysadmin specialist. The operator selects a Vertical Seed Pack: a set of archetypes, Chart of Accounts profiles, domains, and starter themes. They customise in approximately 30 minutes — the pack is their starting point, not a vendor-imposed ontology.

From day one, the operator can ask the Tier A specialist operational questions. Responses arrive in seconds. Every interaction is a potential training example for the customer's own adapter; over weeks, the specialist is intended to become tuned to their environment.

When the operator needs editorial or bilingual work they may enable Tier B on-demand. The GPU instance wakes, processes the request, and idles back down. Cost is metered by the minute, not by seat.

When the operator wants to monetise their first-party data they may enable the marketplace. A buyer queries the listing, transacts through the gateway, and pays directly to the operator's bank account or crypto wallet. PointSav takes its transaction fee at settlement.

When the operator sells the business, the new owner imports the Totebox bundle and operates from day one without re-training, without data migration, and without vendor cooperation.

## How it works for the larger institution

A 300-lawyer firm deploys a Totebox cluster: multiple units plus a Tier B GPU box. Per-matter graph isolation — per-tenant module identifier at the matter granularity — provides ethical walls native to the architecture. Senior partners' reasoning captured as interface verdicts is intended to train the firm's adapter; the next associate-level question benefits from a more partner-shaped response.

A regional hospital deploys a Totebox per service line. Patient graphs are isolated; data sovereignty is the default. Data does not egress without explicit consent; Tier C is structurally disabled at this tenant. The clinical knowledge graph builds from encounter notes; the graph grounds the next clinical-decision question.

A real-property firm builds a seed taxonomy hand-tuned to their operations — Investor Relations, Capital Projects, Compliance, Construction. Themes age in and out as initiatives close and new ones launch. The graph is their property, growing with the business.

In each case the form is the same: substrate, graph, specialist, optional generalist, audit, marketplace. The substance differs per industry.

## What centralised platforms cannot match

Centralised platform vendors are committed to integrated recurring revenue. Their model assumes compute concentrates in their cloud, data flows to their cloud, subscription fees are charged regardless of customer usage, and lock-in increases as data accumulates.

PointSav's intended model assumes compute distributes to customer hardware, data stays at the customer, transaction fees are charged when value flows, and transfer is a single-command operation.

These are not minor configuration differences. They are structural inversions. A centralised platform vendor cannot adopt PointSav's commercial model without dismantling its existing revenue base. This is the structural window in which PointSav may be the only realistic answer for the institution that wants AI-native operations without lock-in.

## The compounding loop

The architecture has a positive-feedback loop:

1. The customer's Totebox runs deterministic operations on their data — the substrate-without-inference base case
2. The Tier A specialist trains on their engineering corpus and interface verdicts
3. The specialist becomes more useful → the operator uses it more → more verdicts → improved specialist
4. The graph grows from accepted inferences → more grounding for the next inference → fewer hallucinations → more accepted inferences
5. The customer's data accumulates value as the graph grows; marketplace flows may begin generating revenue
6. Direct-payment settlement routes revenue directly to the customer; PointSav takes a transaction fee
7. Pack contributions back to the marketplace may make the next sector-customer onboarding faster

Every loop iteration is a marginal improvement. The compounding runs in customer time, not vendor time. PointSav Digital Systems's commercial incentive is to keep the loops running well.

## The first reference deployment

The PointSav development environment is the first reference deployment of the substrate. PointSav Digital Systems operates this instance as their own production environment; Woodfine Management Corp. is the first customer. The platform composes the same shape for both.

This is the structural realization of the customer-first-ordering principle: PointSav builds what Woodfine will install, on the same substrate Woodfine will use, in the same order Woodfine will install it.

## What ships when (planned)

All phases are planned targets, not commitments. Forward-looking statements apply throughout per Canadian securities continuous-disclosure requirements [ni-51-102] [osc-sn-51-721].

The intended implementation rolls out over 2026:

- **Phase 1 (May 2026):** Architecture ratified; Tier A 1B model swap empirically validated
- **Phase 2 (May 2026):** Rebuild blueprints staged at engineering monorepo; cluster tasks begin
- **Phase 3 (May–June 2026):** service-content, service-extraction, service-input rebuilt as MCP servers
- **Phase 4 (June 2026):** Doorman MCP gateway; slm-cli TUI Phase 1
- **Phase 5 (July–August 2026):** service-marketplace, service-ad-exchange, service-settlement; first marketplace transactions
- **Phase 6 (Q3 2026):** First customer Totebox provisioned; first IT-support adapter trained
- **Phase 7 (Q4 2026):** Community Vertical Seed Pack contributions begin
- **Phase 8+ (2027):** Continued model improvement; second customer Totebox; federated marketplace launch

Material assumptions: engineering cluster tasks executing on the rebuild scope; operator ratification of the architecture specification; Woodfine's readiness to participate as the Phase 6 reference customer.

## What this is, and what it is not

This is **a structural commitment** to sovereignty, composability, and SMB-first design.

This is **not** a centralised-platform-replacement product. PointSav is not designed to serve enterprises that want vendor-managed compute with recurring license fees. That is a well-served market. The platform is designed for the market that is not well served.

This is **not** a niche or experimental architecture. The 2026 industry research consistently points toward the structural shape PointSav is building. The platform is deliberately positioned at the intersection where centralised platform vendors are structurally unable to follow.

The platform is in place. The architecture is ratified. The first deployment is operational. The next chapter is scale.

## See also

- [[compounding-substrate]] — the compounding ownership model underlying the thesis
- [[service-slm-yoyo-operational]] — the Yo-Yo relay and Doorman operational state
- [[source-of-truth-inversion]] — the canonical/view/ephemeral pattern underpinning the substrate
- [[four-tier-slm-substrate]] — the four-tier inference model (Tier 0/A/B/C)
- [[machine-based-auth]] — the hardware-bound pairing model underlying the MBA shift
- [[compliance-and-continuous-disclosure]] — the continuous-proof posture that replaces annual audit cycles
