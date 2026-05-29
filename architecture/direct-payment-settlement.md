---
schema: foundry-doc-v1
title: "Direct-payment settlement"
slug: direct-payment-settlement
category: architecture
type: topic
quality: complete
short_description: "Payment for marketplace transactions is planned to flow directly from buyer to the customer-tenant; PointSav's share is a transaction fee at settlement, not a recurring subscription."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-01
editor: pointsav-engineering
cites: []
paired_with: direct-payment-settlement.es.md
---

**Direct-Payment Settlement** is the planned payment architecture for the platform's data marketplace and ad exchange flows. Under this model, payment is intended to travel directly from the buyer to the customer-tenant, with [[pointsav-overview|PointSav]] deducting a transparent transaction fee at the moment of settlement. No funds are planned to flow through the platform's accounts; no payout cycles are planned; and the customer's access to the platform is not contingent on any subscription or minimum payment. See also [[economic-model|the economic model]] and [[service-wallet-settlement|service-wallet-settlement]].

## Why direct payment matters for small businesses

Marketplace platforms that intermediate payment create operational complications for small businesses that enterprise operators absorb routinely. A 30-to-60-day payout cycle is a treasury management problem for a five-person firm that has no treasury function. An intermediary holding customer funds introduces counterparty exposure that a small business cannot practically manage. And platform-intermediated payment requires the seller to reconcile platform statements against their own records — a compliance overhead that compounds for businesses in regulated industries.

Direct payment removes these complications. The buyer pays the seller; [[pointsav-overview|PointSav]] takes its fee at the moment of transaction; no float period exists; and the audit chain is simpler.

## Two planned settlement rails

[[service-wallet-settlement|`service-settlement`]] (planned [[three-ring-architecture|Ring 2]] service) is intended to support two rails simultaneously:

**Traditional banking rail.** The intended pattern connects the tenant's business bank account at provisioning. When a buyer initiates a transaction, the payment routes through a standard marketplace settlement mechanism — the buyer is charged, [[pointsav-overview|PointSav]]'s fee is deducted, and the remainder transfers to the tenant's account. This rail handles tax reporting obligations for applicable jurisdictions and operates at industry-standard transaction fee rates.

**Direct cryptocurrency rail.** The intended alternative connects a customer-owned crypto wallet. When a buyer chooses this rail, a transaction is constructed directing funds from buyer to tenant with a fee output to PointSav's operating wallet. The buyer broadcasts the transaction; the tenant holds funds as soon as the chain confirms. Settlement is intended to be faster than the banking rail and to operate across borders without currency conversion complexity. This rail is planned as opt-in; tenants who do not want it do not see it.

## Intended fee model

The intended fee is a percentage of transaction value deducted at settlement. The fee is intended to be transparent (visible to both buyer and tenant before the transaction is confirmed), consistent (a per-transaction percentage rather than per-tenant negotiation), and non-recurring (no subscription, no minimum, no annual fee).

Tenant onboarding is not planned to require any upfront payment. [[pointsav-overview|PointSav]] is intended to earn only when the tenant earns. This aligns with the [[customer-owned-graph-ip]] principle: the customer's data and adapters are their property; the platform is planned to take a service fee on monetization activity, not a license fee on access to the customer's own records.

## Settlement audit shape

Every planned settlement event is intended to record a structured entry in the audit ledger: the settlement identifier, the transaction it corresponds to, the tenant module identifier, the rail used, the gross amount, the fee breakdown, the net amount to the tenant, the settlement timestamp, and a confirmation identifier. The audit ledger is intended to be anchored periodically to a cryptographic transparency log, making past settlements verifiable against an immutable record.

## Composition

Direct-Payment Settlement composes with the [[reverse-flow-substrate]] — every marketplace and ad exchange transaction is intended to trigger a settlement event. It composes with [[customer-owned-graph-ip]] — revenue from monetizing customer-owned intellectual property flows to the IP holder. And it composes with [[single-boundary-compute-discipline]] — settlement traffic is intended to route through the [[doorman-protocol|Doorman]] so that the same audit boundary captures monetization as well as inference.

## See also

- [[reverse-flow-substrate]] — the planned marketplace and ad exchange flows that generate settlement events
- [[customer-owned-graph-ip]] — the ownership principle that makes customer-direct payment the correct model
- [[single-boundary-compute-discipline]] — the Doorman as the intended settlement audit boundary
