---
schema: foundry-doc-v1
title: "Wallet settlement"
slug: service-wallet-settlement
short_description: "A per-tenant internal accounting ledger that records and settles reverse-flow revenue from the data marketplace as signed JSONL entries, with non-custodial withdrawal options to blockchain or fiat and platform-fee deductions applied at credit time."
category: services
type: topic
quality: complete
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-25
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

`service-wallet` is the per-tenant internal accounting ledger that records and settles all reverse-flow revenue from the platform's data marketplace and ad exchange. The service operates at Ring 2 — the knowledge-and-processing layer of the platform — and holds no funds: it tracks credits, debits, and fees as cryptographically signed entries, with withdrawal to the operator's own wallet or bank account handled outside the platform.

The structural design properties are specified in the platform accounting ledger design.[^1]

## Structural Accounting Isolation

`service-wallet` is an **accounting ledger**, not a payment rail and not a custodial wallet. The distinction matters legally and structurally:

- **Accounting ledger**: records credits, debits, and fees as signed JSONL entries; denominated in the operator's chosen unit of account; no funds in transit; PointSav holds no float
- **Not a payment rail**: The platform does not route money between parties; the buyer's transaction goes directly to the destination address or through the smart contract; the platform fee is an accounting deduction at the time the incoming credit is recorded
- **Not a custodial wallet**: The platform never holds the tenant's private keys; the tenant's balance in `service-wallet` is an accounting balance representing amounts owed, not a pool of funds under platform control

This architecture keeps the platform structurally outside regulated money-transmitter and custodial-wallet territory. Tenants should obtain local legal counsel on their own payment activities; this is directional, not legal advice.

## Cryptographic Ledger Records

Every credit, debit, and fee entry is a signed JSONL record:

```json
{
 "schema": "foundry-wallet-entry-v1",
 "entry_id": "<ulid>",
 "tenant_id": "<module_id>",
 "type": "credit | debit | fee_deduction | withdrawal",
 "amount": "<decimal string>",
 "currency": "USDC | USD | CAD | <operator-configured>",
 "chain": "polygon-pos | solana | fiat | null",
 "tx_hash": "<on-chain tx hash if applicable>",
 "source_service": "service-market | service-exchange",
 "platform_fee_pct": "<decimal string>",
 "platform_fee_amount": "<decimal string>",
 "net_tenant_amount": "<decimal string>",
 "signed_at": "<ISO 8601>",
 "ledger_seq": "<monotonic integer>"
}
```

The `platform_fee_amount` is deducted at credit time. The tenant's balance is `net_tenant_amount` accumulated across credits minus debits.

## Settlement Flow Execution

```
1. Revenue event occurs (data purchase or ad impression/win)
2. Incoming credit recorded in service-wallet ledger
 Platform fee deducted at this step (accounting deduction)
3. Tenant's net balance increases
4. Tenant initiates withdrawal (tenant-controlled; not automatic)
 Options:
 (a) Crypto withdrawal → tenant's pre-registered address (EVM or Solana)
 (b) Fiat withdrawal → tenant's bank account (via Stripe Connect or equivalent)
 (c) Tier B credit → balance reinvested as Yo-Yo compute budget
5. Withdrawal event recorded in ledger
 Receipt anchored to Sigstore Rekor
 WORM ledger entry in service-fs closes the accounting cycle
```

## Settlement Payment Rails

| Chain | Typical fee | Role |
|---|---|---|
| Polygon PoS | approximately $0.002/tx | Primary — lowest fees, proven micropayment volume |
| Solana | approximately $0.0005/tx | Secondary — fastest settlement, sub-cent fees |

Non-custodial: platform stores destination addresses (public keys only). The withdrawal transaction is signed by the tenant's wallet, not by the platform. Platform cannot move funds without the tenant's signature.

Circle Paymaster handles gas abstraction — tenants pay gas in USDC; no native Polygon/Solana token required for SMB operators.

## Fee Deduction Mechanism

The platform fee percentage is an operator configuration at deployment time, applied uniformly across all reverse-flow transactions for that tenant. It is an accounting deduction, not a separate transaction. The specific percentage is an open operator decision.

Industry reference: direct-payment-to-rights-holder models at scale validate that customers keeping a majority of revenue is a workable commercial structure. The platform's revenue split is an operator configuration; the intended default is "customer keeps majority."

## Audit and Public Anchoring

Every withdrawal receipt is anchored to Sigstore Rekor. The anchor record includes: tenant ID, ledger sequence at withdrawal, amount, chain, and transaction hash. This provides a tamper-evident external timestamp suitable for accounting and legal purposes.

The full ledger history is queryable by the tenant at any time. The export format is JSONL — the same format as the ingestion record. Portability is unconditional; the ledger travels with the tenant on exit per the customer-owned data portability guarantee.[^3]

## See also

- [[reverse-flow-substrate]] — revenue sources; payment rail detail
- [[customer-owned-graph-ip]] — ledger export is unconditional tenant property
- [[worm-ledger-architecture]] — service-wallet appends to service-fs WORM ledger
