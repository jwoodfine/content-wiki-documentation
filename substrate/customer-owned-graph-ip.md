---
schema: foundry-doc-v1
title: "Customer-Owned Graph IP"
slug: customer-owned-graph-ip
category: substrate
type: topic
quality: complete
short_description: "The per-tenant knowledge graph and trained adapter weights are the customer's intellectual property, portable and exportable without vendor approval."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-01
editor: pointsav-engineering
cites: []
paired_with: customer-owned-graph-ip.es.md
---

**Customer-Owned Graph IP** is the principle that the per-tenant knowledge graph held in `service-content` is the customer's intellectual property, not a by-product of using the platform. The trained model adapters produced from that customer's corpus are also the customer's property.

## What ownership means

Every node, edge, mutation, and audit-ledger entry scoped to a tenant's module identifier is owned by that tenant. The platform has no claim to aggregate, resell, or use tenant graph data outside the specific per-tenant opt-ins defined in the platform's architecture.

Ownership carries four operational properties:

**Export at any time.** The operator may run a single export command to produce a complete bundle: the graph, the audit ledger, the per-tenant adapters, and the seed taxonomy. This is a routine operation, not a legal or contractual event requiring vendor involvement.

**No format lock-in.** The export bundle uses open formats: a Cypher dump for the graph, JSONL for the audit ledger, and standard tensor formats for the adapter weights. The bundle is importable into any compatible system.

**No aggregate license.** The platform does not retain rights to use the customer's data to train cross-tenant models without explicit per-tenant consent.

**Transfer of ownership.** The customer may sell, gift, or transfer their Totebox and export bundle without vendor involvement. This is addressed in more detail in [[substrate-without-inference-base-case]].

## Why this matters

Most enterprise software platforms shape customer data to the vendor's ontology. When a customer attempts to leave, the data must be re-shaped to fit whatever system they are moving to — a migration project that typically requires vendor cooperation and specialist staff.

The platform's approach inverts this. The customer's data is shaped by their own seed taxonomy (see [[seed-taxonomy-as-smb-bootstrap]]). Export is a single-command operation producing an open-format bundle. The customer's access to their data does not depend on the platform's servers remaining operational.

The economic complement is the transaction-fee pricing model (see [[direct-payment-settlement]]): the customer pays a platform fee only when they earn from their data, not a recurring subscription for access to their own records.

## Relationship to reverse flows

The [[reverse-flow-substrate]] describes the mechanisms by which a customer's accumulated graph may become a saleable asset — patterns such as a data marketplace or an ad exchange. These reverse flows are opt-in per tenant and require explicit operator consent at each transaction. The customer's ownership is the foundation that makes monetization a customer decision: the customer is selling or licensing their own intellectual property, with the platform facilitating the transaction for a fee.

## Per-tenant isolation

The module identifier that scopes each graph also isolates it. The knowledge graph and training corpus of one tenant cannot be accessed by another tenant or used to train another tenant's adapter. The boundaries are structural, not policy.

## See also

- [[seed-taxonomy-as-smb-bootstrap]] — the customer's customized seed taxonomy is part of their intellectual property
- [[reverse-flow-substrate]] — planned mechanisms for monetizing customer-owned graph assets
- [[direct-payment-settlement]] — the payment model that makes customer ownership commercially meaningful
- [[substrate-without-inference-base-case]] — the transfer-of-ownership flow that makes the ownership right exercisable
