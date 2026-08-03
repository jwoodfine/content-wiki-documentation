---
schema: foundry-doc-v1
type: topic
content_type: topic
slug: os-orchestration-stateless-hub
title: "os-orchestration: The Stateless Aggregation Layer"
short_description: "os-orchestration coordinates work across Totebox Archives without storing customer data, keys, or audit records — a stateless routing surface above the capability layer."
audience: vendor-public
bcsc_class: forward-looking
language: en
paired_with: os-orchestration-stateless-hub.es.md
category: infrastructure
status: active
quality: complete
last_edited: 2026-08-03
---

**Correction (2026-08-02, verified against canonical `origin/main`):** the elaborate capability-broker/federation/statelessness-enforcement architecture described below doesn't exist. The real `os-orchestration/src/lib.rs` is a 2-line placeholder scaffold (`"SYSTEM EVENT: os-orchestration scaffold verified."`) — no capability brokers, no federation model, no commercial-tier Ring logic. Its own README even names a different aggregation crate, `app-interface-command`, not the `app-orchestration-exchange`/`app-orchestration-market` names this article uses elsewhere. The "Yo-Yo GPU Broker" section is closer to accurate — `app-orchestration-slm` is real (`crates/orchestration-slm/src/{allocation,fleet,yoyo_proxy}.rs`, port 9180) — though it's framed differently in real code (a chassis connecting `service-slm` Doorman instances, not "a pool of GPU capacity from PPN + external providers"). **Resolved 2026-08-03**: the whole article is re-hedged to planned/intended language below; the Commercial Model section's Tier B revenue/metering claim — which this correction had not yet flagged as a separate defect — turned out to be misattributed to `os-orchestration` entirely and is corrected to name `app-orchestration-slm` (the real crate that actually implements per-tenant usage metering, `crates/orchestration-slm/src/metering.rs`, confirmed on `origin/main`) as the system that owns that model.

The PointSav platform is designed around a deliberate architectural boundary: an aggregation layer intended to coordinate work across [[totebox-archive|Totebox Archives]] while holding no customer data, storing no keys, and writing nothing to any [[worm-ledger-architecture|WORM ledger]]. This layer is planned as `os-orchestration` — today a registered but unimplemented scaffold crate, not a running system (see the correction above).

Understanding what `os-orchestration` is intended to be requires first understanding what it is designed not to be. It is not planned as a database, not a credential store, and not a custodian. Every archive in the PointSav network is designed to maintain its own isolated state — its own WORM audit trail, its own key material, its own DataGraph segment. `os-orchestration` is planned to sit above that layer as a coordinator: routing requests, enforcing capability boundaries, and brokering cross-archive work without ever touching the underlying data.

## The Federation Model (planned)

Access between Totebox Archives is designed to be governed by Protection Domains (PDs). Each archive would run its own capability-broker PD, holding the only authority to grant or deny cross-Totebox access for that archive. The intended rule is strict: no application-layer PD would contact a Totebox directly. Every cross-archive request would pass through the capability-broker PD of the target archive, which would apply the per-org capability boundary defined for that organization.

`os-orchestration` is planned to operate on the federation tier, above the per-archive PDs — able to observe that a request exists and route it to the appropriate capability broker, but not to authorize the request itself. Authorization is designed to live where the data lives — in the archive.

This design is intended to reflect [[capability-geometry|Capability Geometry]] at the federation layer. Each organization's data would be enclosed within a capability boundary that `os-orchestration` could not cross on behalf of another organization. A request from one organization would not be routable to another organization's archive by exploiting the aggregation layer — by design, not merely by policy, once built.

## What Statelessness Is Intended to Mean for Trust

Statelessness is designed as a trust property, not merely an implementation detail. Because `os-orchestration` is intended to write nothing and store nothing, it would not be compellable to produce customer data it does not hold. Under this design, a subpoena directed at the aggregation layer would return nothing of substance, and a breach of the aggregation layer would expose routing topology, not content.

This is intended to stand in contrast to hub-and-spoke architectures where the hub accumulates session state, cached credentials, or derived data — designs where the hub becomes a target. In the planned PointSav model, the aggregation layer would be structurally inert with respect to customer data: the archives are the custodians; `os-orchestration` is intended as the switchboard.

Practically, this design intends for `os-orchestration` to carry no obligation under data residency or data custody regulations, with regulatory obligations attaching instead to the archives, which can be provisioned in specific jurisdictions. The aggregation layer, once built, is intended to be able to run anywhere.

## The Commercial Model

The commercial structure of the PointSav platform is intended to follow a Rings model. The first two planned Rings of capability — the foundational services every Totebox would require to operate — are intended to be provided free of charge with each Totebox provisioning. This is meant to cover the local inference tier (Tier A), basic DataGraph access, and the standard service stack.

**This section previously misattributed a working revenue and metering system to `os-orchestration`. It does not have one — `os-orchestration` is an unimplemented scaffold (see the correction above). The real Tier B usage-based revenue and metering model belongs to a different, real crate: `app-orchestration-slm`.** `app-orchestration-slm` is a working "Yo-Yo broker chassis" (confirmed on canonical `origin/main`, port `:9180`) connecting Totebox Archives' `service-slm` Doorman instances to a shared Yo-Yo GPU fleet. It implements real per-tenant cost metering (`crates/orchestration-slm/src/metering.rs`): each inference request's cost is computed from measured inference time and a configured hourly USD rate, and recorded to a per-tenant ledger that a Tier B customer is billed against. Tier A — the free, local inference tier — is unaffected by this and requires no metering. If `os-orchestration` is ever built as an aggregation/federation layer, it may in principle route requests toward `app-orchestration-slm`'s Tier B service, but the metering, billing, and revenue-accrual logic itself lives in `app-orchestration-slm`, not in `os-orchestration`.

## The Yo-Yo GPU Broker

`app-orchestration-slm` is the real, working [[yoyo-compute-substrate|Yo-Yo GPU broker]] chassis (see the Commercial Model correction above), implementing on-demand GPU allocation and per-tenant metering today. When a Totebox Archive's `service-slm` Doorman submits an inference request that exceeds local Tier A capacity — either because the model is too large for the local hardware or because concurrent load has exhausted available compute — the request is routed to `app-orchestration-slm`'s chassis.

The chassis connects to a Yo-Yo GPU fleet and routes the inference request, returning the result to the originating archive. The archive does not need its own GPU hardware for Tier B workloads; the chassis provides elasticity, and records the cost of each request against the requesting tenant.

The name reflects the design metaphor: compute capacity extends outward from the archive on demand and retracts when the request completes. No persistent GPU allocation is held by the archive between requests.

## What This Is Intended to Mean at Deployment

When an operator eventually provisions an `os-orchestration` instance, the intent is that they would be deploying a routing and brokering surface, not a storage system. The provisioning checklist is designed to be shorter than for a Totebox Archive: no WORM storage configuration, no key provisioning beyond the TLS certificates that would be required for mutual authentication with the archives it serves, no data migration.

An `os-orchestration` instance is intended to be replaceable, scalable, or relocatable without data loss, because it is designed to hold no data. This property is meant to make the aggregation layer straightforward to operate: its failure modes would be limited to availability (it is unreachable) rather than integrity (its state has drifted or been corrupted).

For the same reason, `os-orchestration` is designed never to be the system of record for any business process. Operators who need to audit what happened — which archive processed which request, when, under whose authorization — would read the WORM ledger of the relevant Totebox Archive. The aggregation layer is intended to be absent from that audit trail except as a routing node.

## Design Anchors

The intended design of `os-orchestration` draws on several architectural positions. The planned commercial structure, including the Rings model, sets the frame within which `app-orchestration-slm`'s real on-demand GPU allocation and metering mechanism operates today — see the Commercial Model correction above for how that split actually works. The data marketplace provisions, if built, are intended to govern the per-org capability boundaries that would prevent cross-organizational data leakage. A WORM audit obligation is intended to apply to archives and to deliberately exclude the aggregation layer. The browser-facing orchestration surfaces (`app-orchestration-exchange`, `app-orchestration-market`) are intended to operate as the customer-visible face of the aggregation tier, once built.

Together these positions describe a platform where coordination is intended to be separated from custody. The design goal is for the aggregation layer to be effective precisely because it does not hold what it routes — though today, only `app-orchestration-slm`'s piece of this picture is real.
