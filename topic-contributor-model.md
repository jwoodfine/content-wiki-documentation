---
title: "The Three-Tier Contributor Model"
slug: topic-contributor-model
category: governance
status: pre-build
last_edited: 2026-04-27
editor: pointsav-engineering
cites:
  - ni-51-102
---

# The Three-Tier Contributor Model

Foundry's substrate is too broad for any single team to maintain
and too valuable to lock to a single team's release cadence. The
contributor model that follows from this constraint operationally
produces three distinct tiers — Core, Paid, and Open — with
explicit mobility paths between them. This article describes the
tiers, the mathematics of why the model works, and the
architectural primitives that make it tractable.

## The three tiers

| Tier | Headcount target | Funding | Role |
|---|---|---|---|
| **Core** | 4-7 | PointSav-employed; salaried; equity in PointSav Digital Systems | Day-to-day stewardship of the substrate |
| **Paid** | 50-100 | PointSav-funded contracts; outcome-based deliverables | Project-tier engineering work via GitHub PRs |
| **Open** | 10,000+ | None — Apache 2.0 / MIT / CC BY 4.0 contributions | Public substrate contributions; no CLA required |

### Core (4-7 people)

The Core tier owns workspace documents, doctrine amendments,
conventions, and the citations registry. Architectural decisions
flow through this tier. Apprentice-mode oversight (the senior
review function in the apprenticeship substrate) for new model
versions and new contributors lives here.

This tier is small by design. Three architectural primitives keep
it tractable: the substrate is operationally self-sufficient
enough that customer breakouts do not require Core handholding;
the Trajectory Substrate makes the substrate self-documenting;
and the Adapter Composition Algebra makes operational personality
composable rather than person-dependent.

### Paid (50-100 people)

Project-tier engineering work, paid by PointSav, executed via
GitHub pull requests against the public substrate repositories.
Engineering work in `pointsav-monorepo/` and the per-project
cluster paths. Multi-tenant aggregation services. Per-
jurisdiction export adapters. LoRA adapter authoring. Customer-
specific deployment provisioning and integration.

The 50-100 band is the size where individual contributor
reputation can be tracked through the Trajectory Substrate's
attribution, per-deliverable contracting is operationally
tractable without enterprise procurement bureaucracy, and
revenue from multi-tenant aggregation services can sustain the
headcount without venture-scale capital.

### Open (10,000+ people)

Contributors to the public substrate via pull requests against
the open repositories: `pointsav/factory-release-engineering`,
`pointsav-design-system`, the wiki engine
`app-mediakit-knowledge`, MCP server adapters, LoRA adapter
recipes, and TOPIC content in the `content-wiki-*` repositories.

Apache 2.0 / MIT / CC BY 4.0 licensed contributions per the
artefact tier. **No CLA required** for contributions to the open
core, per 2026 open-core-handbook best practice; CLAs are only
needed for dual-licensed commercial-tier components.

The 10,000+ scale is plausible because comparable substrate
communities have demonstrated it: the Linux kernel sustains
roughly 14,000 contributors per year, the Apache Foundation
crosses tens of thousands across projects, Kubernetes carries
4,000-plus on a single project, and PostgreSQL operates with
roughly 700 core contributors plus many more occasional. The
licensing posture (Apache 2.0 weights + CC BY 4.0 docs + MIT
design-system) matches the licensing patterns that have
demonstrably scaled to these levels.

The Open tier is what makes the substrate self-sustaining at
scale that 4-7 Core could not possibly maintain alone. Most
substrate features ship via Open contribution; Core reviews and
accepts; Paid implements the commercial-tier extensions that
Open contributors do not typically tackle.

## Cross-tier mobility

The model is not caste-bound. Three mobility paths operate:

- **Open → Paid.** A contributor whose recurring work shows
  operational quality is offered Paid contracts. Reputation
  derives from the Trajectory Substrate's attribution — Master
  Claude's view of how much each contributor's work shapes
  downstream recommendations.
- **Paid → Core.** Rare; requires alignment with PointSav's
  long-term substrate stewardship and senior operational trust.
- **Anyone can fork, leave, and operate their own substrate.**
  The Designed-for-Breakout property applies at the contributor
  level: a contributor can take their work, their adapters, and
  their tenant data and operate independently. The substrate
  does not lock contributors any more than it locks customers.

## Why the math works

Naïve calculation: 4-7 employees plus 50-100 contractors plus
10,000-plus open contributors yields a substrate with the reach
of a hyperscaler-scale platform team (roughly 1,000-plus) at
roughly five percent of the headcount cost.

This is the structural advantage. Three architectural primitives
make it real:

1. The Trajectory Substrate makes contributor reputation
   cryptographically attributable, so Open-tier reputation can
   compound into Paid-tier eligibility without procurement
   bureaucracy.
2. The Adapter Composition Algebra lets individual contributors
   ship adapters without owning the whole substrate.
3. The Designed-for-Breakout property keeps the contributor
   relationship voluntary — no contributor is locked in, which
   means contributors choose to participate because the
   substrate serves their interests, not because they cannot
   leave.

## Forward-looking — scaling the Open tier

Per `[ni-51-102]` continuous-disclosure language, the
trajectory toward 10,000-plus Open contributors is `planned`
and `intended`, not declarative-future. The shape is in place;
the operational throughput matures as the substrate's user
base grows.

The path: each Foundry-shaped customer who runs the substrate
becomes a candidate Open contributor; a fraction of those
contribute back; a fraction of those graduate to Paid; a small
number of those graduate to Core over decades. The model is
slow at the top tier and fast at the bottom — by design.

## What this model is not

It is not a hierarchy in the dignity sense. The Open tier is
not "lower" than Core; it is differently scoped. A contributor
who ships a substrate-shaping LoRA adapter as Open is doing
work the Core tier could not have done alone. The tiers
describe role and funding, not status.

It is not a replacement for governance. Core makes
architectural decisions; Paid implements; Open contributes.
But the Constitutional Convention process per Doctrine §III is
the venue for substrate-level disagreements, and any
contributor can bring an amendment.

It is not a venture-scale labour model. The 50-100 Paid tier
sustains on multi-tenant aggregation revenue without venture-
scale capital — the unit economics work because the headcount
is small, the deliverables are bounded, and the customer base
pays for outcomes rather than tickets.

## See also

- [The Compounding Substrate](topic-compounding-substrate.md)
- [The Apprenticeship Substrate](topic-apprenticeship-substrate.md)
- [Customer Hostability](topic-customer-hostability.md)
- [Canadian-Simple Copyright Posture](topic-canadian-simple-copyright.md)
- The convention this article reflects:
  `~/Foundry/conventions/knowledge-commons.md` §7
