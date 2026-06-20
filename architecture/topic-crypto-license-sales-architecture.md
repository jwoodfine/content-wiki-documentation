---
schema: foundry-doc-v1
content_type: topic
title: "Crypto License Sales Architecture"
slug: topic-crypto-license-sales-architecture
aliases:
  - topic-crypto-license-sales-architecture
short_description: "How PointSav moves a customer from payment intent through on-chain settlement to a cryptographic license token that grants binary access, without a traditional payment processor."
category: architecture
type: reference
quality: complete
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-06-20
editor: pointsav-engineering
paired_with: topic-crypto-license-sales-architecture.es.md
cites: []
---

# Crypto License Sales Architecture

The crypto license sales architecture describes how a customer moves from expressing
intent to purchase through on-chain payment to receiving a license token that grants
binary access — all without a traditional payment processor or identity provider in
the critical path.

## Design Principles

Three principles shape the architecture:

1. **Payment and identity are separated.** The on-chain payment address is derived
   deterministically from a customer index; no identity information is required before
   payment arrives.
2. **The license token is the sole trust carrier.** Once issued, a license token can be
   verified by the binary server without contacting any other service.
3. **Key custody stays with the customer.** The marketplace never holds a private key
   on the customer's behalf. The Ed25519 keypair derived at issuance is the customer's
   credential.

## End-to-End Flow

### Step 1 — Address Derivation

When a customer creates an order on `app-privategit-marketplace`, the marketplace
requests a payment address from `tool-wallet`. The wallet derives an HD address using
the BIP-32 path `m/44'/60'/0'/0/<customer_index>` from a BIP-39 mnemonic held in the
wallet's key store. The derived Polygon address is unique to that customer slot and is
returned to the marketplace for display.

### Step 2 — On-Chain Payment

The customer sends USDC on the Polygon network to the displayed address. `tool-wallet`
polls the Polygon RPC endpoint at a configurable interval. When a transfer to the
customer's address is confirmed at the required block depth, the wallet writes a payment
receipt to its append-only store and notifies the marketplace.

The wallet does not submit transactions; it reads only.

### Step 3 — License Issuance

On receiving payment confirmation, `app-privategit-marketplace` calls the wallet to
generate an Ed25519 keypair for this license. The public key is stored in the
marketplace's license registry. The signed license token is constructed with:

| Field | Value at issuance |
|---|---|
| `product_id` | Ordered product identifier |
| `version_constraint` | Purchased version range |
| `customer_id` | Opaque marketplace customer ID |
| `issued_at` | Current Unix timestamp |
| `expires_at` | 0 (perpetual) or configured expiry |

The token is signed with the Ed25519 private key generated in this step. The private key
is delivered to the customer and is not retained by the marketplace. The marketplace
retains only the public key for future verification queries.

### Step 4 — Token Delivery

The signed license token is delivered to the customer over HTTPS. The customer stores
the token and presents it in the `Authorization: Bearer <token>` header on all subsequent
download requests to `app-privategit-source`.

### Step 5 — Binary Access

`app-privategit-source` receives the download request with the embedded token. It decodes
the token, recovers the public key from its local license registry, and verifies the
Ed25519 signature locally. If the product and version fields match the requested binary,
the binary is served. The binary server contacts no external service during this step.

Registry synchronization between the marketplace and the binary server is intended for a
future phase; in the current phase the registry is populated by direct write at issuance
time.

## Failure Modes

| Failure | Behaviour |
|---|---|
| Polygon RPC unavailable | Wallet queues payment checks; no impact on existing tokens |
| Marketplace unavailable | New orders blocked; existing license tokens continue to work |
| Binary server unavailable | Downloads blocked; license tokens remain valid |
| Token expired | Binary server returns 403; customer must renew via marketplace |

## Key Custody

The architecture guarantees that no single service holds both the ability to confirm
payment and the ability to issue a valid license. `tool-wallet` holds the BIP-39
mnemonic (address derivation and Ed25519 keygen) but has no access to the product
catalog or customer records. `app-privategit-marketplace` holds the product catalog and
customer records but calls the wallet only for key generation and payment confirmation —
it does not hold the BIP-39 mnemonic directly.

## See Also

- [[topic-software-distribution-substrate|Software Distribution Substrate]] —
  component inventory and deployment overview
- [[topic-private-git-paid-customer-endpoint|Private Git Paid Customer Endpoint]] —
  the binary server from the customer's perspective
- [[topic-ppn-small-business-compute|PPN Small-Business Compute]] — compute capacity
  sold through this same architecture

---

*Woodfine Capital Projects™, MCorp™, PointSav Digital Systems™, Totebox Orchestration™, Totebox Archive™, and Capability Geometry™ are trademarks of Woodfine Capital Projects Inc., used in Canada, the United States, Latin America, and Europe. All other trademarks are the property of their respective owners.*
