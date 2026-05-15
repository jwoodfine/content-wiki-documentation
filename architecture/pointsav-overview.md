---
schema: foundry-doc-v1
title: "PointSav — Company Overview and Three-Organisation Structure"
slug: pointsav-overview
category: architecture
type: concept
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-15
editor: pointsav-engineering
paired_with: pointsav-overview.es.md
short_description: "PointSav Digital Systems is a technology vendor that builds sovereign, on-premise-capable operating systems for record-keeping and business administration. It sits within a three-organisation structure established by Woodfine Capital Projects Inc."
cites: []
---

PointSav Digital Systems is a technology vendor that builds and licenses sovereign, on-premise-capable operating systems and services for record-keeping, business administration, and cyberphysical-system integration. The company exists to engineer the substrate that runs its parent group's real-estate operations, then licenses that substrate to similarly-structured institutional customers. PointSav sits inside a three-organisation governance topology established by Woodfine Capital Projects Inc., a real-estate firm focused on procurement, development, and management of real property. This article covers the three-organisation structure, the structural advantages it produces, and the licensing and contributor model.

## The three-organisation structure

| Organisation | Role | Relationship |
|---|---|---|
| **Woodfine Capital Projects Inc.** | 100% parent | Real-estate firm; owns both subsidiaries outright |
| **PointSav Digital Systems** | Vendor | IP holder; designs and builds the technology platform |
| **Woodfine Management Corp.** | Customer | First and reference customer; operates real-property assets |

The relationship flow is strictly one-directional: the vendor builds, the customer adopts, deployments run. There are no reverse writes — the customer never edits vendor source, and the vendor never manages customer records.

## Why this structure matters

Three structural advantages emerge from the separation:

**Clean IP custody.** PointSav holds the intellectual property. Woodfine Management Corp. licenses the product like any other customer. There is no commingling of corporate records and source code.

**Reference deployment.** Because Woodfine Management Corp. is a real operator — not a test environment — every product feature must survive contact with actual business operations before it can be sold elsewhere. The reference customer is the quality gate.

**Investor clarity.** The vendor (PointSav) is the asset that scales. The customer (Woodfine Management Corp.) is the asset that operates. Each can be measured, audited, and valued on its own terms.

## Licensing model

The product strategy follows an open-core pattern. The core operating systems (`os-totebox`, `os-console`, `os-workplace`) are intended for release under Apache 2.0 with a planned Sovereign Addendum ensuring that running instances remain freely transferable by the operator regardless of where they are hosted. The fleet-aggregator product (`os-orchestration`) is intended to remain proprietary as the commercial revenue driver.

PointSav intends to partner with the Sovereign Data Foundation to oversee the integrity of the open-source components. Terms and structure of any such arrangement are planned and subject to finalisation.

## Contributor model

Engineering work flows through staging-tier contributor identities: `jwoodfine` and `pwoodfine` are the two established staging contributors, both Woodfine Management Corp. employees who push to their own GitHub forks. The vendor administration function accepts contributions via squash-merge — the moment the intellectual property formally transfers from contributor to vendor. The customer organisation pulls release tags from the vendor. A double-blind air-gap applies: contributors never push directly to customer repositories; the customer organisation never has visibility into contributor forks.

## See also

- [[legal-and-ip-structure]] — corporate entities, IP transfer mechanics, patent and licence strategy
- [[deployment-patterns]] — the six canonical configurations for PointSav deployments
- [[os-family-overview]] — the eight operating systems PointSav builds
- [[machine-based-auth]] — the security model that underlies the platform
- [[compliance-and-continuous-disclosure]] — BCSC posture and continuous-disclosure obligations
