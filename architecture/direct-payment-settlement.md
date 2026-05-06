---
schema: foundry-doc-v1
title: "Direct-Payment Settlement"
slug: direct-payment-settlement
category: architecture
type: topic
quality: published
short_description: "Payment for marketplace transactions is planned to flow directly from buyer to the customer-tenant; Foundry's share is a transaction fee at settlement, not a recurring subscription."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-01
editor: pointsav-engineering
cites: []
paired_with: direct-payment-settlement.es.md
---

**Direct-Payment Settlement** is the planned payment architecture for Foundry's data marketplace and ad exchange flows. Under this model, payment is intended to travel directly from the buyer to the customer-tenant, with Foundry deducting a transparent transaction fee at the moment of settlement. No funds are planned to flow through Foundry's accounts; no payout cycles are planned; and the customer's access to the platform is not contingent on any subscription or minimum payment. This pattern encodes Doctrine claim #53.

## Why direct payment matters for small businesses

Marketplace platforms that intermediate payment create operational complications for small businesses that enterprise operators absorb routinely. A 30-to-60-day payout cycle is a treasury management problem for a five-person firm that has no treasury function. An intermediary holding customer funds introduces counterparty exposure that a small business cannot practically manage. And platform-intermediated payment requires the seller to reconcile platform statements against their own records — a compliance overhead that compounds for businesses in regulated industries.

Direct payment removes these complications. The buyer pays the seller; Foundry takes its fee at the moment of transaction; no float period exists; and the audit chain is simpler.

## Two planned settlement rails

`service-settlement` (planned Ring 2 service) is intended to support two rails simultaneously:

**Traditional banking rail.** The intended pattern connects the tenant's business bank account at provisioning. When a buyer initiates a transaction, the payment routes through a standard marketplace settlement mechanism — the buyer is charged, Foundry's fee is deducted, and the remainder transfers to the tenant's account. This rail handles tax reporting obligations for applicable jurisdictions and operates at industry-standard transaction fee rates.

**Direct cryptocurrency rail.** The intended alternative connects a customer-owned crypto wallet. When a buyer chooses this rail, a transaction is constructed directing funds from buyer to tenant with a fee output to Foundry's operating wallet. The buyer broadcasts the transaction; the tenant holds funds as soon as the chain confirms. Settlement is intended to be faster than the banking rail and to operate across borders without currency conversion complexity. This rail is planned as opt-in; tenants who do not want it do not see it.

## Foundry's intended fee model

Foundry's intended fee is a percentage of transaction value deducted at settlement. The fee is intended to be transparent (visible to both buyer and tenant before the transaction is confirmed), consistent (a per-transaction percentage rather than per-tenant negotiation), and non-recurring (no subscription, no minimum, no annual fee).

Tenant onboarding is not planned to require any upfront payment to Foundry. Foundry is intended to earn only when the tenant earns. This aligns with the [[customer-owned-graph-ip]] principle: the customer's data and adapters are their property; Foundry is planned to take a service fee on monetization activity, not a license fee on access to the customer's own records.

## Settlement audit shape

Every planned settlement event is intended to record a structured entry in the audit ledger: the settlement identifier, the transaction it corresponds to, the tenant module identifier, the rail used, the gross amount, the fee breakdown, the net amount to the tenant, the settlement timestamp, and a confirmation identifier. The audit ledger is intended to be anchored periodically to a cryptographic transparency log, making past settlements verifiable against an immutable record.

## Composition

Direct-Payment Settlement composes with the [[reverse-flow-substrate]] — every marketplace and ad exchange transaction is intended to trigger a settlement event. It composes with [[customer-owned-graph-ip]] — revenue from monetizing customer-owned intellectual property flows to the IP holder. And it composes with [[single-boundary-compute-discipline]] — settlement traffic is intended to route through the Doorman so that the same audit boundary captures monetization as well as inference.

## See Also

- [[reverse-flow-substrate]] — the planned marketplace and ad exchange flows that generate settlement events
- [[customer-owned-graph-ip]] — the ownership principle that makes customer-direct payment the correct model
- [[single-boundary-compute-discipline]] — the Doorman as the intended settlement audit boundary

## References

1. Doctrine claim #53 — Direct-Payment Settlement (ratified v0.1.0).
2. `conventions/reverse-flow-substrate.md` — claim #52 composition.
3. Sigstore Rekor transparency log — intended cryptographic anchoring for settlement audit chain.

---

## Provenance

Source: `convention-direct-payment-settlement.md` (refined 2026-04-30). Workspace-internal file paths and open questions removed. All settlement, fee, and rollout claims carry "planned," "intended," and "is intended to" framing — Phase 5 implementation has not begun. BCSC continuous-disclosure posture applied throughout.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*

*Woodfine Capital Projects™, Woodfine Management Corp™, PointSav Digital Systems™, Totebox Orchestration™, and Totebox Archive™ are trademarks of Woodfine Capital Projects Inc., used in Canada, the United States, Latin America, and Europe. All other trademarks are the property of their respective owners.*
