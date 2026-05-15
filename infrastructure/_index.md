---
schema: foundry-doc-v1
title: "Infrastructure"
slug: _index
category: infrastructure
type: topic
quality: complete
short_description: "Fleet deployment topology, cloud operational runtime, and physical infrastructure — from the WORM ledger storage substrate to edge deployment patterns, the sovereign mesh, and telemetry architecture."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-15
editor: pointsav-engineering
paired_with: _index.es.md
---

Infrastructure articles sit at the boundary between the abstract platform architecture and the concrete machines, services, and network paths that constitute a live deployment. This category covers storage substrate design, fleet topology, edge deployment patterns, key management operations, and the telemetry and mesh network that connect a fleet.

## Storage substrate

The foundational persistence layer — the WORM ledger and the audit surface it provides.

- [[worm-ledger-design]] — The four-layer Write-Once-Read-Many ledger: tile-based, hash-chained, cryptographically signed; satisfies SEC 17a-4(f), eIDAS, and SOC 2 by structure rather than policy.
- [[worm-ledger-architecture]] — Architectural layout of the WORM ledger across Ring 1 services.
- [[worm-ledger-storage-architecture]] — Physical storage organisation for WORM ledger deployments.
- [[storage]] — Storage topology and block-device configuration for PointSav deployments.
- [[data-vault-bookkeeping-substrate]] — An SMB bookkeeping architecture built on an immutable source vault and append-only journal, with structural separation between the bookkeeping record and any accounting tool.

## Fleet and edge deployment

How a deployment is provisioned, updated, and maintained across on-premises and cloud hardware.

- [[edge-deployment]] — Edge deployment patterns for PointSav instances operating at the network edge or in low-connectivity environments.
- [[tier-c-key-wiring]] — The operational procedure for managing external API keys in the Doorman service: where keys live, how they rotate, and how a breach is contained.

## Network and telemetry

How fleet nodes communicate and how observability signals are collected without centralising identifiable data.

- [[sovereign-mesh]] — The WireGuard-based peer-to-peer mesh network that connects PointSav fleet nodes without a central routing authority.
- [[sovereign-telemetry]] — Zero-state telemetry: the V4 Intent Beacon collects behavioural and hardware signals from edge clients without cookies, session identifiers, or third-party analytics.
- [[telemetry-architecture]] — Architecture of the telemetry pipeline across PointSav deployments.

## See also

- [Architecture](/architecture/) — cross-cutting platform architecture and the three-ring model
- [Systems](/systems/) — the operating systems that run on this infrastructure
- [Services](/services/) — the services that depend on the storage and network substrate
