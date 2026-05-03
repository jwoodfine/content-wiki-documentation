---
schema: foundry-doc-v1
title: "Reverse-Flow Substrate"
slug: reverse-flow-substrate
category: architecture
type: topic
quality: published
short_description: "The Doorman gateway and audit ledger that enforce inbound data discipline are planned to also enforce outbound commercial flows — data marketplace and ad exchange — both opt-in per tenant."
status: pre-build
last_edited: 2026-05-01
editor: pointsav-engineering
cites: []
paired_with: reverse-flow-substrate.es.md
---

The **Reverse-Flow Substrate** is the planned extension of the Doorman gateway, audit ledger, and per-tenant module identifier to govern outbound commercial flows. The same boundary that mediates inbound inference requests is intended to also mediate two outbound flows: a data marketplace and an ad exchange. Both are planned as opt-in per tenant, structurally disabled by default, and require per-record cryptographic provenance. This pattern encodes Doctrine claim #52.

## The two planned reverse flows

**Data Marketplace.** The customer's accumulated knowledge graph, audit ledger, and trained adapter weights are intended to be saleable assets. The planned marketplace gateway (`service-marketplace`) is intended to expose per-tenant inventory to external buyers. Planned inventory categories include anonymized aggregate queries against the per-tenant graph, trained adapter weights (saleable to other tenants in the same vertical with explicit permission), curated content-wiki material with consent and license terms, and verdict-signed corpus tuples with cryptographic provenance for AI training data buyers.

**Ad Exchange.** The customer is planned to operate as both seller and buyer in a standards-compliant real-time bidding exchange. As seller, the customer's first-party audience — with per-record consent and AI intent classification — is intended to be real-time-bid inventory. As buyer, the customer's adapter may classify their own audience intent to support targeted outbound campaigns. The customer's budget controls the bid.

## Per-tenant opt-in discipline

Reverse flows are structurally disabled by default. Enabling them requires the operator to authenticate as the tenant's primary identity, run the appropriate enable command in the TUI, and complete a guided consent flow that includes inventory category selection, consent-record review, pricing configuration, and settlement rail selection. The configuration is signed by the operator's identity key and recorded in the audit ledger.

There is no API path that enables marketplace or ad exchange flows without operator-signed consent. The TUI flow is the structural enforcement of the opt-in requirement.

## Audit ledger as proof-of-rights

Every planned transaction in either reverse flow is intended to record the consent terms in force at transaction time, the audit chain from source data to the inventory item (provenance), the buyer identity, and the settlement event. The audit ledger is the intended legally admissible record that data was sold with consent, that the consent matched the transaction's terms, and that no cross-tenant data leakage occurred.

## Per-tenant isolation in reverse flows

The module identifier discipline that prevents cross-tenant graph traversal also prevents cross-tenant inventory leakage. Marketplace listings are scoped by tenant; a buyer cannot query across tenants without explicit per-tenant grants. Ad exchange impression inventory uses opaque tenant-scoped tokens; the buyer never sees the underlying tenant audience.

The customer's decision to combine their own audience data with other data sources is the customer's decision to make, through the consent flow. The platform does not combine tenant data for advertiser targeting without explicit tenant authorization.

## Composition with other principles

The planned reverse flows depend on [[single-boundary-compute-discipline]] — all marketplace and ad exchange traffic is intended to route through the Doorman, so the same audit boundary that captures inference also captures monetization events. They depend on [[customer-owned-graph-ip]] — the inventory is the customer's intellectual property, and reverse flows are the mechanism through which the customer may realize commercial value from that property. And they depend on [[direct-payment-settlement]] — payment flows directly from buyer to the customer-tenant, with Foundry taking a transaction fee at settlement.

## See Also

- [[customer-owned-graph-ip]] — the ownership principle that makes reverse flows a customer-controlled decision
- [[direct-payment-settlement]] — the planned payment mechanism for marketplace and ad exchange transactions
- [[vertical-seed-packs-marketplace]] — planned packs as first-class marketplace inventory
- [[single-boundary-compute-discipline]] — the Doorman boundary that governs outbound as well as inbound flows

## References

1. Doctrine claim #52 — Reverse-Flow Substrate (ratified v0.1.0).
2. IAB OpenRTB 2.6 specification — planned ad exchange alignment.
3. `conventions/customer-owned-graph-ip.md` — claim #48 composition.

---

## Provenance

Source: `convention-reverse-flow-substrate.md` (refined 2026-04-30). Workspace-internal file paths and open questions removed. All marketplace, ad exchange, and settlement claims carry "planned," "intended," and "is intended to" framing throughout — Phase 5 implementation has not begun. BCSC continuous-disclosure posture applied.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
