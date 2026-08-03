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
last_edited: 2026-08-03
editor: pointsav-engineering
paired_with: os-orchestration.es.md
short_description: "os-orchestration is the commercial-tier OS letting a single operator see, query, and command many Totebox archives at once — the Fleet Aggregator for enterprise deployments."
cites: []
---

**Correction revised, 2026-08-02.** An earlier pass said "no crate named `os-orchestration` exists in the monorepo today" — checked against this archive's stale local branch. On canonical (`origin/main`), `os-orchestration/` is a real, registered crate (own `Cargo.toml`, `license = "FSL-1.1-ALv2"`), but its `src/lib.rs` is a 4-line placeholder ("SYSTEM EVENT: os-orchestration scaffold verified.") — no aggregation logic. The rename from `os-interface` is confirmed in-progress on canonical too (root `LICENSE`: "os-interface/ — interface module (renames to os-orchestration)"). The "PSP" (PointSav Protocol) claim was confirmed fabricated — re-checked directly against `origin/main`, zero code footprint anywhere — and has been removed below (2026-08-03); the aggregation-protocol description is now hedged as planned/intended with no invented protocol name. Net effect: the substantive finding is unchanged (this article's described functionality isn't built) but "the crate doesn't exist" was the wrong framing — it exists as an empty scaffold, same as many other placeholder crates found this session. The rest of the article has also been re-hedged to planned/intended language throughout (2026-08-03) — the "Proprietary" licence claim in the table below is kept as confirmed current fact, since the `LICENSE` file classification applies today even though the aggregation code does not yet exist.

`os-orchestration` is planned as the commercial-tier operating system intended to let a single operator see, query, and command many [[totebox-archive|Totebox archives]] at once. Where [[console-os|`os-console`]] connects to one [[totebox-os|`os-totebox`]], `os-orchestration` is intended as the hub between an operator's Console and a fleet of Toteboxes — what an executive would view to see the position of every property in a portfolio, every entity in a holding company, or every project in a development pipeline, in a single unified answer to "what is the state of the entire estate, right now?" This article covers the intended design: what `os-orchestration` is planned to do, what it is designed to deliberately not do, how aggregation is intended to work, the commercial features planned for it, and when it would be deployed. **None of this is built yet** — see the correction above.

## What it is designed not to do

`os-orchestration` is designed not to store raw records — to be stateless. The intent is that it would pull metadata from Toteboxes, synthesise a unified view, and present it through `os-console`, with raw data never leaving its Totebox. Under this design the aggregator would see only what the Totebox is permitted to expose.

This boundary is intended to be structurally important: even if `os-orchestration` were compromised, the underlying Toteboxes would remain sealed, since the aggregator is not meant to hold keys to the archives.

## Where it is planned to sit in the product line

| Component | Role | Licence model (planned) |
|---|---|---|
| `os-console` | Operator-facing terminal | AGPL-3.0-or-later source; free BETA today |
| `os-totebox` | Data archive per entity | FSL-1.1-ALv2 source-available now; converts to Apache-2.0 after 2 years; free BETA today |
| `os-orchestration` | Fleet aggregator (planned) | Proprietary — confirmed via the monorepo `LICENSE` file today, ahead of the aggregation logic itself |

The commercial line is intended to be drawn at the aggregator. The Console and the Totebox are intended to be free and freely transferable. The Orchestration aggregator is planned as the paid product — an individual operator managing one entity would never need it.

## How aggregation is intended to work

The design intent is for `os-orchestration` to connect to Toteboxes through a [[capability-based-security|capability-based]] protocol tunnelled through standard TLS at the edge — no specific protocol name is committed to code today. Inside the tunnel, the intended flow is:

1. The aggregator would send a signed capability object granting permission to read a specific row of a specific Totebox for a fixed time window.
2. The Totebox would verify the capability, run the query internally, and emit only the result — never the raw record.
3. The aggregator would combine results from many Toteboxes into a single unified view.

If built as designed, promise pipelining and zero-copy memory mapping are intended to make the experience feel local even when Toteboxes are distributed across multiple regions.

## The commercial features (planned)

Three capabilities are planned to be reserved exclusively to `os-orchestration`:

| Feature | What it is intended to enable |
|---|---|
| Aggregation | Reading metadata from multiple Toteboxes simultaneously |
| Multi-tenancy | Serving multiple operators against the same underlying fleet |
| Complex viewports | Cross-archive dashboards — portfolio rollups, cross-entity reconciliation, executive summaries |

These features are intended to be intentionally absent from the open `os-console` codebase — planned to live in the `os-orchestration` codebase and nowhere else, once built.

## The Diode discipline (planned)

The design calls for `os-orchestration` to be able to issue commands downstream to the Toteboxes it manages, with Toteboxes unable to issue commands back up. The aggregator is intended to itself be a [[diode-standard|Diode]] subject: receiving commands only from `os-console`, never from a Totebox. This is designed to make lateral movement structurally impossible — a compromised Totebox would not be able to use the aggregator as a bridge to the operator's Console. The [[totebox-orchestration|Totebox Orchestration]] article covers the coordination layer's provisioning and lifecycle management.

## When it would be deployed

`os-orchestration` is planned as a commercial product for multi-entity operators. Single-entity operators managing one Totebox would not need it. Multi-entity operators — real-estate portfolios, public companies with subsidiaries, family offices with multiple holdings — would be the intended customer once the cognitive load of running separate Consoles against individual Toteboxes justifies the aggregator.

## See also

- [[console-os]] — the Direct vs. Aggregate mode distinction; os-console pairs with os-orchestration in Aggregate mode
- [[totebox-os]] — the archives being aggregated
- [[diode-standard]] — the unidirectional command discipline that governs the aggregator
- [[machine-based-auth]] — how pairings secure aggregator-to-Totebox connections
- [[deployment-patterns]] — how os-orchestration appears in commercial deployment configurations
- [[os-family-overview]] — the eight-OS family and how os-orchestration fits
