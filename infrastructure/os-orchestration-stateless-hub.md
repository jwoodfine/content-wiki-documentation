---
schema: foundry-doc-v1
type: topic
content_type: topic
slug: os-orchestration-stateless-hub
title: "os-orchestration: The Stateless Aggregation Layer"
short_description: "os-orchestration coordinates work across Totebox Archives without storing customer data, keys, or audit records, acting as a stateless routing and brokering surface above the per-archive capability layer."
audience: vendor-public
bcsc_class: current-fact
language: en
paired_with: os-orchestration-stateless-hub.es.md
category: infrastructure
status: active
quality: complete
last_edited: 2026-06-23
---

# os-orchestration: The Stateless Aggregation Layer

The PointSav platform is built around a deliberate architectural boundary: the aggregation layer that coordinates work across Totebox Archives holds no customer data, stores no keys, and writes nothing to any WORM ledger. This layer is `os-orchestration`.

Understanding what `os-orchestration` is requires first understanding what it is not. It is not a database, not a credential store, and not a custodian. Every archive in the PointSav network maintains its own isolated state — its own WORM audit trail, its own key material, its own DataGraph segment. `os-orchestration` sits above that layer as a coordinator: it routes requests, enforces capability boundaries, and brokers cross-archive work without ever touching the underlying data.

## The Federation Model

Access between Totebox Archives is governed by Protection Domains (PDs). Each archive runs its own capability-broker PD, which holds the only authority to grant or deny cross-Totebox access for that archive. The rule is strict: no application-layer PD contacts a Totebox directly. Every cross-archive request passes through the capability-broker PD of the target archive, which applies the per-org capability boundary defined for that organization.

`os-orchestration` operates on the federation tier, above the per-archive PDs. It can observe that a request exists and route it to the appropriate capability broker, but it cannot authorize the request itself. Authorization lives where the data lives — in the archive.

This design reflects Capability Geometry at the federation layer. Each organization's data is enclosed within a capability boundary that `os-orchestration` cannot cross on behalf of another organization. A request from one organization cannot be routed to another organization's archive by exploiting the aggregation layer. The geometry of the system makes this impossible by construction, not by policy.

## What Stateless Means for Trust

Statelessness is a trust property, not merely an implementation detail. Because `os-orchestration` writes nothing and stores nothing, it cannot be compelled to produce customer data that it does not hold. A subpoena directed at the aggregation layer returns nothing of substance. A breach of the aggregation layer exposes routing topology, not content.

This stands in contrast to hub-and-spoke architectures where the hub accumulates session state, cached credentials, or derived data. In those designs, the hub becomes a target. In the PointSav model, the aggregation layer is structurally inert with respect to customer data. The archives are the custodians; `os-orchestration` is the switchboard.

Practically, this means `os-orchestration` carries no obligation under data residency or data custody regulations. Regulatory obligations attach to the archives, which can be provisioned in specific jurisdictions. The aggregation layer can run anywhere.

## The Commercial Model

The commercial structure of the PointSav platform follows the Rings model. The first two Rings of capability — the foundational services that every Totebox requires to operate — are provided free of charge with each Totebox provisioning. This covers the local inference tier (Tier A), basic DataGraph access, and the standard service stack.

The paid tier activates when workloads exceed local capacity or when operators elect to access the broader data marketplace. Tier B inference routes through `os-orchestration` to the inference hub, where capacity is pooled across the network. The data marketplace allows archives to publish structured datasets and consume datasets published by other archives within the capability boundary.

Revenue accrues at the aggregation layer for Tier B and marketplace transactions. The aggregation layer is the commercial gateway even though it is not a data custodian. This is the intended design: monetization flows through routing and access control, not through data accumulation.

## The Yo-Yo GPU Broker

`app-orchestration-slm` is the commercial Yo-Yo GPU broker, implementing the on-demand GPU allocation mechanism. When a Totebox Archive submits an inference request that exceeds local Tier A capacity — either because the model is too large for the local hardware or because concurrent load has exhausted available compute — the request is routed to `app-orchestration-slm`.

The broker holds a pool of GPU capacity drawn from the PointSav Private Network and from contracted external providers. It allocates capacity on demand, routes the inference request, and returns the result to the originating archive. The archive never requires its own GPU hardware for Tier B workloads; the broker provides elasticity.

The name reflects the design metaphor: compute capacity extends outward from the archive on demand and retracts when the request completes. No persistent GPU allocation is held by the archive between requests.

## What This Means at Deployment

When an operator provisions an `os-orchestration` instance, they are deploying a routing and brokering surface, not a storage system. The provisioning checklist is accordingly shorter than for a Totebox Archive: no WORM storage configuration, no key provisioning beyond the TLS certificates required for mutual authentication with the archives it will serve, no data migration.

An `os-orchestration` instance can be replaced, scaled, or relocated without data loss, because it holds no data. This property makes the aggregation layer straightforward to operate: its failure modes are limited to availability (it is unreachable) rather than integrity (its state has drifted or been corrupted).

For the same reason, `os-orchestration` is never the system of record for any business process. Operators who need to audit what happened — which archive processed which request, when, under whose authorization — read the WORM ledger of the relevant Totebox Archive. The aggregation layer is absent from that audit trail except as a routing node.

## Doctrine Anchors

The design of `os-orchestration` is grounded in four doctrine positions. The commercial structure, including the Rings model and the Yo-Yo broker, establishes the on-demand GPU allocation mechanism. The data marketplace provisions govern the per-org capability boundaries that prevent cross-organizational data leakage. The WORM audit obligation applies to archives and deliberately excludes the aggregation layer. The browser-facing orchestration surfaces (`app-orchestration-exchange`, `app-orchestration-market`) operate as the customer-visible face of the aggregation tier.

Together these positions define a platform where coordination is separated from custody. The aggregation layer is effective precisely because it does not hold what it routes.
