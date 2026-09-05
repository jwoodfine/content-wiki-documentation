---
schema: foundry-doc-v1
title: "Wallet settlement — the design"
slug: service-wallet-settlement
short_description: "service-wallet is a planned per-tenant accounting ledger for reverse-flow marketplace revenue — no code exists yet; the design calls for a non-custodial, signed-entry ledger rather than a payment rail."
category: services
type: topic
content_type: topic
quality: complete
index_group: specialist-and-domain-services
status: active
audience: vendor-public
bcsc_class: forward-looking
language_protocol: PROSE-TOPIC
last_edited: 2026-09-05
editor: pointsav-engineering
paired_with: service-wallet-settlement.es.md
references:
  - id: 1
    text: "PointSav platform specification: per-tenant accounting ledger design for reverse-flow settlement — structural properties of the service-wallet component."
  - id: 2
    text: "PointSav platform specification: reverse-flow substrate — the revenue-routing mechanism through which data marketplace proceeds reach operator wallets."
  - id: 3
    text: "PointSav platform specification: customer-owned graph intellectual property — the portability and ownership guarantees for operator-generated graph data."
  - id: 4
    text: "PointSav platform specification: Write-Once-Read-Many (WORM) ledger design — the append-only storage substrate underpinning all platform accounting records."
---

`service-wallet` is a planned per-tenant accounting ledger for revenue from the platform's
data marketplace and ad exchange — recording and settling what a tenant is owed as
cryptographically signed entries, never holding funds itself. No implementation exists yet;
this article describes the design, not a shipped service. A distinct, real, already-shipped
utility named `tool-wallet` exists in the same monorepo — a single-tenant, vendor-side
Polygon USDC payment watcher for license purchases — but it is a different component with a
different purpose, not this planned ledger under another name.

## The design's central distinction

The design calls for `service-wallet` to be an accounting ledger, never a payment rail and
never a custodial wallet — a distinction that matters both structurally and legally.

- **Accounting ledger**: records credits, debits, and fees as signed entries denominated in
  the operator's chosen unit of account; no funds pass through the platform.
- **Not a payment rail**: money would move directly between the buyer and the destination
  address or smart contract; the platform's fee is intended as an accounting deduction at the
  moment a credit is recorded, not a separate money movement.
- **Not a custodial wallet**: the platform would never hold a tenant's private keys — a
  tenant's balance would be an accounting figure representing an amount owed, not a pool of
  funds under platform control.

## What the design proposes

A signed record per credit, debit, or fee entry, tracking amount, currency, chain (if
applicable), fee deduction, and a running tenant balance. A settlement flow where a revenue
event records a credit with the platform fee deducted at that step, the tenant's balance
accumulates, and the tenant — not the platform — initiates any withdrawal, whether to a
crypto address, a bank account, or reinvested as compute credit. Every withdrawal receipt
would anchor to the same external transparency log [[fs-anchor-emitter]] already uses for
other platform records, and the full ledger history would be exportable by the tenant at any
time in the same format it was written in — unconditional portability, matching the
platform's customer-owned-data commitments elsewhere.[^3]

## What this is not

No implementation exists yet — everything above is design, not a shipped service. If built
as designed, this would keep the platform structurally outside regulated money-transmitter
and custodial-wallet territory; that is a description of intended design, not legal advice,
and a tenant's own payment activities remain their own counsel's to assess. Specific fee
percentages, chain choices, and gas-abstraction mechanics named in earlier drafts of this
design are implementation detail that has not been decided, let alone built — not repeated
here as though they were settled.

## See also

- [[reverse-flow-substrate]] — the revenue sources this ledger would record
- [[customer-owned-graph-ip]] — the portability commitment this design's export format follows
- [[worm-ledger-architecture]] — the append-only storage pattern this design would use
