---
schema: foundry-doc-v1
title: "Fleet aggregator"
slug: os-orchestration
category: systems
type: concept
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-15
editor: pointsav-engineering
paired_with: os-orchestration.es.md
short_description: "os-orchestration is the commercial-tier operating system that lets a single operator see, query, and command many Totebox archives at once — the Fleet Aggregator for multi-entity portfolios and enterprise deployments."
cites: []
---

`os-orchestration` is the commercial-tier operating system that lets a single operator see, query, and command many [[totebox-archive|Totebox archives]] at once. Where [[console-os|`os-console`]] connects to one [[totebox-os|`os-totebox`]], `os-orchestration` is the hub between an operator's Console and a fleet of Toteboxes. It is what an executive views when they want the position of every property in a portfolio, every entity in a holding company, or every project in a development pipeline — a single unified answer to "what is the state of the entire estate, right now?" This article covers what `os-orchestration` does, what it deliberately does not do, how aggregation works, the commercial features it adds, and when to deploy it.

## What it does not do

`os-orchestration` does not store raw records. It is stateless. It pulls metadata from Toteboxes, synthesises a unified view, and presents it through `os-console`. Raw data never leaves its sovereign Totebox. The aggregator sees only what the Totebox is permitted to expose.

This boundary is structurally important: even if `os-orchestration` is compromised, the underlying Toteboxes remain sealed. The aggregator holds no keys to the archives.

## Where it sits in the product line

| Component | Role | Licence model (planned) |
|---|---|---|
| `os-console` | Operator-facing terminal | Apache 2.0 (intended to be free) |
| `os-totebox` | Data archive per entity | Apache 2.0 (intended to be free) |
| `os-orchestration` | Fleet aggregator | Proprietary (intended as a commercial product) |

The commercial line is drawn at the aggregator. The Console and the Totebox are intended to be free and freely transferable. The Orchestration aggregator is the paid product — an individual operator managing one entity never needs it.

## How aggregation works

`os-orchestration` connects to Toteboxes through the PointSav Protocol (PSP) — a [[capability-based-security|capability-based]] binary protocol that tunnels through standard TLS at the edge. Inside the tunnel:

1. The aggregator sends a signed capability object granting permission to read a specific row of a specific Totebox for a fixed time window.
2. The Totebox verifies the capability, runs the query internally, and emits only the result — never the raw record.
3. The aggregator combines results from many Toteboxes into a single unified view.

Promise pipelining and zero-copy memory mapping make the experience feel local even when Toteboxes are distributed across multiple regions.

## The commercial features

Three capabilities are reserved exclusively to `os-orchestration`:

| Feature | What it enables |
|---|---|
| Aggregation | Reading metadata from multiple Toteboxes simultaneously |
| Multi-tenancy | Serving multiple operators against the same underlying fleet |
| Complex viewports | Cross-archive dashboards — portfolio rollups, cross-entity reconciliation, executive summaries |

These features are intentionally absent from the open `os-console` codebase. They live in the `os-orchestration` codebase and nowhere else.

## The Diode discipline

`os-orchestration` can issue commands downstream to the Toteboxes it manages. The Toteboxes cannot issue commands back up. The aggregator is itself a [[diode-standard|Diode]] subject: it receives commands only from `os-console`, never from a Totebox. This makes lateral movement structurally impossible — a compromised Totebox cannot use the aggregator as a bridge to the operator's Console. The [[totebox-orchestration|Totebox Orchestration]] article covers the coordination layer's provisioning and lifecycle management.

## When to deploy

`os-orchestration` is a commercial product for multi-entity operators. Single-entity operators managing one Totebox do not need it. Multi-entity operators — real-estate portfolios, public companies with subsidiaries, family offices with multiple holdings — deploy it when the cognitive load of running separate Consoles against individual Toteboxes justifies the aggregator.

## See also

- [[console-os]] — the Direct vs. Aggregate mode distinction; os-console pairs with os-orchestration in Aggregate mode
- [[totebox-os]] — the archives being aggregated
- [[diode-standard]] — the unidirectional command discipline that governs the aggregator
- [[machine-based-auth]] — how pairings secure aggregator-to-Totebox connections
- [[deployment-patterns]] — how os-orchestration appears in commercial deployment configurations
- [[os-family-overview]] — the eight-OS family and how os-orchestration fits
