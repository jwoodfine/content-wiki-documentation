---
schema: foundry-doc-v1
title: "Procurement overview"
slug: procurement-overview
category: governance
type: topic
content_type: topic
quality: complete
short_description: "What a regulated buyer acquires when deploying PointSav: hardware the customer owns outright, data the vendor never holds, no minimum-spend commitment, and compliance properties enforced by architecture rather than contractual promise."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-15
editor: pointsav-engineering
cites:
 - ni-51-102
 - osc-sn-51-721
paired_with: procurement-overview.es.md
---

PointSav delivers a data platform on hardware the customer owns outright. There is no shared cloud, no vendor-held encryption keys, and no minimum-spend commitment required to reach compliance-grade infrastructure. Every record the customer writes lives in the customer's own storage from the moment it is written, and can be presented to a regulator without coordinating with the vendor.

Every artefact ships with a bootstrap script that brings the full stack up on a machine the customer provides — no SaaS dependency, no provider login, no metered cloud API. A customer who terminates the relationship retains every record they ever wrote, every trained adapter they funded, and the complete audit ledger of every action taken on their data. The vendor does not hold what the customer built.

The platform's [[three-ring-architecture|three-ring architecture]] separates boundary ingest (Ring 1), deterministic processing (Ring 2), and optional AI inference (Ring 3). AI inference never writes to the authoritative record; that path belongs exclusively to deterministic Ring 2 services. A deployment that excludes Ring 3 entirely still delivers the full compliance-grade record-keeping stack — and exposes less attack surface in the process.

For a regulated buyer under continuous-disclosure obligations, this architecture has a concrete audit consequence: the authoritative record sits on hardware the buyer controls, the ledger is cryptographically append-only, and the buyer can satisfy a regulator's request for records without depending on the vendor's continued operation or cooperation. `[ni-51-102]`

## What the customer owns

Three properties are structurally guaranteed — not contractually promised:

**The data.** Every record written by a Ring 1 service is written to the customer's local storage in an append-only WORM format. The vendor's network never carries the customer's unencrypted record content. A customer who moves their hardware moves their data.

**The adapters.** When the customer's optional AI adapter trains on the customer's corpus, the resulting model weights live inside the customer's substrate — not on the vendor's servers. The customer's training corpus lives inside the customer's substrate. Tenant-private corpus records never traverse the vendor's network.

**The audit ledger.** The per-tenant audit ledger — the record of every editorial action, every AI inference call, every data ingestion — lives at the customer's deployment. A vendor outage does not impair the customer's ability to produce this ledger for a regulator.

## What the vendor does not hold

No PointSav service stores a decryption key for customer data on the vendor's infrastructure. No PointSav service routes customer record content through a vendor-operated intermediate. The vendor provides the software; the customer provides the hardware, the keys, and the storage. This is the [[customer-hostability]] commitment expressed as procurement terms: the substrate does not have a data-export feature because the data was already on the customer's hardware from the moment it was written.

## Commercial structure (planned)

Per `[osc-sn-51-721]`, the following describes the planned commercial trajectory. Specific rates and SLA terms will be published when the first continued-pretraining assessment data is available.

**Open tier (no cost).** Knowledge-commons read access, community forum, and public documentation. The intended entry point for individual contributors and organisations evaluating the platform.

**Paid Tier C (per-token, subscription).** Access to the planned [[pointsav-llm|PointSav-LLM]] specialist model through the customer's local Doorman. Per-token pricing intended to be accessible at SMB contract sizes — no enterprise-tier minimum spend. The model routes through the customer's Doorman; the customer's audit ledger logs every call.

**Paid Tier C+ (premium).** Per-token access plus reserved escalation hours for L2/L3 human-in-the-loop support. Customers who contribute trajectory data to the training corpus under this tier are intended to receive preferential per-token rates in subsequent billing cycles, as their data compounds the model's specialist depth.

The base model weights (OLMo 3, Apache 2.0) are open source. The commercial line is the value the vendor adds: specialist continued pretraining on the aggregated corpus, the human-in-the-loop escalation infrastructure, the per-tenant audit substrate, and the SLA.

## Compliance properties

The platform's compliance posture is structural rather than procedural. Compliance is not achieved by policy controls that a misconfigured administrator can override — it is achieved by the architecture of the storage engine and the service boundaries.

- **Record immutability.** The WORM ledger satisfies SEC Rule 17a-4(f) for US broker-dealer record-keeping, eIDAS qualified electronic records preservation, and SOC 2. Modification is not denied at the policy layer; it is denied by the storage engine, which has no delete or overwrite operation.
- **AI audit trail.** Every AI inference call — local, GPU burst, or external API — passes through the [[doorman-protocol|Doorman]] and generates an audit row in the customer's local ledger. The vendor's gateway generates a second audit row simultaneously. Two-ledger, per-call coverage.
- **BCSC continuous disclosure.** The platform produces continuous-disclosure-grade records as a structural output of Ring 2 processing. A reporting issuer under NI 51-102 who deploys the platform inside their own substrate can satisfy continuous-disclosure obligations against records they own and control.
- **Data residency.** Customer data never leaves the customer's designated hardware except through an explicit egress call audited in the ledger. Data residency is a property of the deployment topology, not a contractual commitment subject to interpretation.

## Regulatory context

Customers operating under the following frameworks have directly applicable compliance properties in the platform's architecture:

| Framework | Applicable property |
|---|---|
| Canadian NI 51-102 continuous disclosure | WORM ledger + egress audit trail satisfy documentary requirements |
| US SEC Rule 17a-4(f) | WORM ledger satisfies non-erasable, non-rewritable electronic storage requirements |
| EU eIDAS qualified preservation | Hash-chained, signed ledger satisfies qualified electronic records requirements |
| SOC 2 | WORM ledger + access-control audit trail satisfy SOC 2 availability and integrity criteria |

Customers in other regulated environments should evaluate the platform's structural properties against their own framework. The technical documentation is [[worm-ledger-design]] and [[compliance-and-continuous-disclosure]].

## Vendor structure

PointSav Digital Systems is the software vendor and is wholly owned by Woodfine Capital Projects Inc. The customer-facing deployment catalog is maintained by Woodfine Management Corp., also wholly owned by Woodfine Capital Projects Inc.

The vendor runs `documentation.pointsav.com` because PointSav is the canonical-tier customer of every package it ships. Customer-hosted deployment is the canonical pattern; vendor hosting is a convenience option.

## See also

- [[customer-hostability]] — the architectural commitment that makes the procurement properties structural
- [[architecture-decisions]] — the twelve binding engineering decisions, including the data-separation and AI-authority rules that underpin the compliance properties
- [[compliance-and-continuous-disclosure]] — how the platform produces continuous-disclosure-grade records
- [[worm-ledger-design]] — the WORM ledger that satisfies SEC 17a-4(f), eIDAS, and SOC 2 by structure
- [[economic-model]] — the two-tier commercial structure and its rationale
- [[bcsc-disclosure-posture]] — the BCSC continuous-disclosure posture and how the platform satisfies it by structure
- [[security-overview]] — the platform's security architecture for technical due diligence
