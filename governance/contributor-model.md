---
schema: foundry-doc-v1
title: "Three-tier contributor model"
slug: contributor-model
category: governance
type: topic
content_type: topic
quality: complete
index_group: licensing-and-contribution
short_description: "The Three-Tier Contributor Model organises substrate contributors into Core (4-7 engineers), Paid (50-100 contractors), and Open (10,000+ public), with mobility paths."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-04-30
editor: pointsav-engineering
cites:
 - ni-51-102
paired_with: contributor-model.es.md
---


The PointSav platform is too broad for any single team to maintain and too valuable to lock to a single team's release cadence. The **Three-Tier Contributor Model** that follows from this constraint produces three distinct tiers — Core, Paid, and Open — with explicit mobility paths between them. This article describes the tiers, the mathematics of why the model works, and the architectural primitives that make it tractable.

## The three tiers

| Tier | Headcount target | Funding | Role |
|---|---|---|---|
| **Core** | 4–7 | PointSav-employed; salaried; equity in PointSav Digital Systems | Day-to-day stewardship of the substrate |
| **Paid** | 50–100 | PointSav-funded contracts; outcome-based deliverables | Project-tier engineering work via GitHub pull requests |
| **Open** | 10,000+ | None — AGPL-3.0-or-later for most platform code, FSL-1.1-ALv2 for a smaller set of modules, CC BY 4.0 for documentation | Public substrate contributions; no CLA required |

### Core

The Core tier owns workspace documents, doctrine amendments, conventions, and the citations registry. Architectural decisions flow through this tier. Apprentice-mode oversight — the senior review function in the apprenticeship substrate — for new model versions and new contributors lives here.

This tier is small by design. Three architectural primitives keep it tractable: the substrate is operationally self-sufficient enough that customer breakouts do not require Core handholding; the [[trajectory-substrate|Trajectory Substrate]] makes the substrate self-documenting; and the [[adapter-composition|Adapter Composition Algebra]] makes operational personality composable rather than person-dependent.

### Paid

Project-tier engineering work, paid by PointSav, executed via GitHub pull requests against the public substrate repositories. Engineering work in `pointsav-monorepo/` and the per-project cluster paths. Multi-tenant aggregation services. Per-jurisdiction export adapters. LoRA adapter authoring. Customer-specific deployment provisioning and integration.

The 50–100 band is the size where individual contributor reputation can be tracked through the [[trajectory-substrate|Trajectory Substrate's attribution]], per-deliverable contracting is tractable without enterprise procurement bureaucracy, and revenue from multi-tenant aggregation services can sustain the headcount without venture-scale capital.

### Open

Contributors to the public substrate via pull requests against the open repositories: `pointsav/factory-release-engineering`, `pointsav-design-system`, the wiki engine `app-mediakit-knowledge`, MCP server adapters, LoRA adapter recipes, and TOPIC content in the `content-wiki-*` repositories.

Licensing is assigned per directory: most platform code (`service-*`, `system-*`, `os-console`, `os-workplace`, most `tool-*`, most `moonshot-*`) is AGPL-3.0-or-later; a smaller set of modules (`os-infrastructure`, `os-privategit`, `os-totebox`, `os-mediakit`, `os-network-admin`, and their `app-*` extensions) is the more permissive FSL-1.1-ALv2; documentation is CC BY 4.0. AGPL's network-use copyleft is a deliberate choice for the platform-code tier — it requires anyone who runs a modified version as a network service to publish their modifications, closing the loop that a plain permissive license leaves open. No CLA is required for open-core contributions; CLAs apply only to the proprietary, dual-licensed commercial-tier components not covered here.

The 10,000-plus scale is plausible under a strong copyleft license because the closest real-world comparable operates under one: the Linux kernel, GPL-2.0-licensed, sustains roughly 14,000 contributors per year. A strong copyleft license has not historically been a ceiling on contributor scale for platform-shaped projects.

The Open tier is what makes the substrate self-sustaining at a scale that 4–7 Core could not possibly maintain alone. Most substrate features ship via Open contribution; Core reviews and accepts; Paid implements the commercial-tier extensions that Open contributors do not typically tackle.

## Cross-tier mobility

The model is not caste-bound. Three mobility paths operate:

- **Open to Paid.** A contributor whose recurring work shows operational quality is offered Paid contracts. Reputation derives from the [[apprenticeship-substrate|Trajectory Substrate's attribution]] — how much each contributor's work shapes downstream recommendations.
- **Paid to Core.** Rare; requires alignment with PointSav's long-term substrate stewardship and senior operational trust.
- **Anyone can fork, leave, and operate their own substrate.** The Designed-for-Breakout property applies at the contributor level: a contributor can take their work, their adapters, and their tenant data and operate independently. The substrate does not lock contributors any more than it locks customers.

## Why the math works

Naïve calculation: 4–7 employees plus 50–100 contractors plus 10,000-plus open contributors yields a substrate with the reach of a large platform team at roughly five percent of the headcount cost.

Three architectural primitives make it real:

1. The [[trajectory-substrate|Trajectory Substrate]] makes contributor reputation cryptographically attributable, so Open-tier reputation can compound into Paid-tier eligibility without procurement bureaucracy.
2. The [[adapter-composition|Adapter Composition Algebra]] lets individual contributors ship adapters without owning the whole substrate.
3. The [[customer-hostability|Designed-for-Breakout]] property keeps the contributor relationship voluntary — no contributor is locked in, which means contributors participate because the substrate serves their interests, not because they cannot leave.

## Forward-looking — scaling the Open tier

Per `[ni-51-102]` continuous-disclosure language, the trajectory toward 10,000-plus Open contributors is planned and intended, not declared as a current state. The shape is in place; the operational throughput matures as the substrate's user base grows.

The path: each customer who runs the platform substrate becomes a candidate Open contributor; a fraction of those contribute back; a fraction of those graduate to Paid; a small number graduate to Core over decades. The model is slow at the top tier and fast at the bottom — by design.

## What this model is not

It is not a hierarchy in the dignity sense. The Open tier is not lower than Core; it is differently scoped. A contributor who ships a substrate-shaping LoRA adapter as Open is doing work the Core tier could not have done alone.

It is not a replacement for governance. Core makes architectural decisions; Paid implements; Open contributes. But the platform's constitutional convention process is the venue for architectural disagreements, and any contributor can bring an amendment.

It is not a venture-scale labour model. The 50–100 Paid tier sustains on multi-tenant aggregation revenue without venture-scale capital — the unit economics work because the headcount is small, the deliverables are bounded, and the customer base pays for outcomes rather than tickets.

## See also

- [[compounding-substrate]] — the substrate architecture that open contributors extend and improve
- [[apprenticeship-substrate]] — corpus capture and attribution pipeline that tracks contributor reputation
- [[trajectory-substrate]] — cryptographic attribution substrate that makes Open-to-Paid mobility tractable
- [[customer-hostability]] — the breakout property that keeps contributor participation voluntary
- [[canadian-simple-copyright]] — IP ownership posture governing work produced under the Paid and Core tiers
