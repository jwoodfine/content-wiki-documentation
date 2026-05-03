---
schema: foundry-doc-v1
title: "Knowledge Commons and Service Commerce"
slug: knowledge-commons
category: architecture
type: topic
quality: published
short_description: The economic model that separates what PointSav publishes freely from what it sells — public knowledge artifacts under open licenses, paid service at the point of multi-Totebox aggregation.
status: pre-build
last_edited: 2026-05-01
editor: pointsav-engineering
cites: []
paired_with: knowledge-commons.es.md
---

The **Knowledge Commons / Service Commerce** model is PointSav's economic architecture. Knowledge artifacts — doctrine, conventions, training recipes, adapter weights, and sanitised trajectory corpus — are published under open licenses and freely reusable. The commercial threshold is crossed precisely when two or more Totebox Archives must be operated as a single coordinated system. Solo Totebox operation is sovereign infrastructure; multi-Totebox aggregation is paid service.

The line between them is bright and structural. It is not a pricing decision — it follows directly from the architecture.

## The public side

The following artifacts are published at every Doctrine MINOR version bump under open licenses:

| Artifact | License |
|---|---|
| DOCTRINE.md and amendments | CC BY 4.0 |
| Conventions | CC BY 4.0 |
| Citation registry (`citations.yaml`) | CC0 |
| Sanitised trajectory corpus shard | CC BY 4.0 with redaction |
| Adapter recipes (training scripts, hyperparameters) | Apache 2.0 |
| Constitutional adapter weights | Apache 2.0 |
| Engineering adapter weights | Apache 2.0 |
| Design-system tokens, components, guidelines | MIT + CC BY 4.0 |

Each Doctrine MINOR bump produces a signed, versioned bundle pushed to `pointsav/factory-release-engineering` with a stable ID (`pointsav-foundry-doctrine-vM.m.p`). The bundle is itself a citable artifact. Downstream deployments and Customers can pin against a specific bundle version and know what they are running.

## The commercial threshold

A single Totebox running its own Foundry deployment is sovereign infrastructure. The Customer owns the substrate, the data, the adapter, and the runtime. Nothing about a single Totebox crosses the commercial threshold.

The threshold is crossed when two or more Totebox Archives — or a Totebox Archive plus an external system in coordination — must be operated as one. Examples include:

- Querying across two regional Toteboxes for a consolidated report
- Federating a Customer's Totebox with a partner's Totebox for joint research
- Routing Tier B requests to PointSav's hosted LLM capacity
- Participating in the adapter marketplace for adapter sharing

The line is structural because aggregation requires crossing trust boundaries, identity boundaries, and operational boundaries that a single sovereign Totebox does not have. Customers pay for the substrate that crosses those boundaries, not for access to knowledge that has no boundary.

## Why the recipe is public

Publishing the recipe does not threaten the business. The reasoning:

**Extraction economics for SMBs are poor.** A small customer who reads the doctrine and attempts self-implementation was never the addressable customer. Service customers pay because operational implementation, integration, compliance, and aggregation represent real work, not because the knowledge is gated.

**Public knowledge increases substrate value.** When the doctrine is public and citable, downstream Customers have a stable reference for their adapters, their compliance posture, and their contributor onboarding. The substrate's reliability is what they pay for.

**The commons is a recruiting funnel.** Contributors find PointSav through public artifacts. They join because the substrate is one they can build on. The `factory-release-engineering` bundle is the entry point.

**Public doctrine resists capture.** A publicly versioned, signed, citable doctrine cannot be acquired and quietly altered. The versioning and signing are the durability mechanism.

## Three-tier contributor model

The Knowledge Commons model operationally produces three contributor tiers:

**Core (4–7 people, PointSav employees)** — day-to-day stewardship of the substrate. Architectural decisions, apprentice-mode oversight for new model versions, customer-service operations. Small by design; the substrate's structural properties are intended to allow this tier to remain small as scale grows.

**Paid contributors (50–100 people, PointSav-funded)** — project-tier engineering work paid by PointSav and executed via GitHub pull requests against the public substrate repositories. Per-jurisdiction export adapters, LoRA adapter authoring, customer-specific deployment provisioning, multi-Totebox aggregation services. Outcome-based contracts tied to Customer service revenue.

**Open contributors (10,000+, CC/Apache-licensed)** — contributions to the public substrate via pull requests to `pointsav/factory-release-engineering`, the design system, the wiki engine, MCP server adapters, and TOPIC content in the content wikis. No CLA required for open-core contributions. Reputation accrues via the Trajectory Substrate's per-contributor attribution. A path to the paid tier exists for contributors whose work demonstrates recurring quality and operational fluency.

The leverage of this structure is that the Open tier sustains features and coverage that a Core of 4–7 people could not maintain alone. Most substrate features are intended to ship via Open contribution; Core reviews and accepts; Paid implements commercial-tier extensions.

## Cross-tier mobility

The model is not fixed. An Open contributor whose recurring work demonstrates operational quality may be offered Paid contracts. A Paid contributor may in time move toward Core. Any contributor can fork, take their adapters and tenant data, and operate independently — the substrate is designed to make graceful exit the default, not litigation.

## See Also

- [[compounding-substrate]] — the five structural properties that make the substrate compound over time
- [[disclosure-substrate]] — the substrate-substitution pattern applied to continuous-disclosure platforms
- [[apprenticeship-substrate]] — the training mechanism that makes per-tenant corpus contribution valuable
- [[adapter-composition]] — how per-tenant adapters are composed and versioned

## References

1. Open Core Handbook, 2026 — open-core licensing best practice.
2. Open Source Guides — leadership in open source communities.
3. Knowledge Commons Wiki — commons-based peer production.
4. Open Knowledge Foundation — open data and open content standards.
5. Creative Commons — CC BY 4.0 and CC0 license texts.

---

## Provenance

Source material: `conventions/knowledge-commons.md` (ratified 2026-04-26, doctrine v0.0.2, extended v0.1.10 with three-tier contributor model). Disciplines applied: no body H1; structural positioning; BCSC forward-looking framing on federated marketplace and PointSav-LLM (planned/may); banned-vocabulary pass; workspace-internal operational paths stripped.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
