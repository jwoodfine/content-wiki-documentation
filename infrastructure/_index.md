---
schema: foundry-doc-v1
title: "Infrastructure"
slug: _index
category: infrastructure
type: topic
quality: complete
short_description: "Fleet deployment topology, cloud operational runtime, and physical infrastructure — the WORM ledger storage substrate, edge deployment patterns, the private WireGuard mesh, sovereign telemetry, key-wiring operations, and the bookkeeping vault that anchors the SMB accounting surface."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-29
editor: pointsav-engineering
paired_with: _index.es.md
---

Infrastructure articles sit at the boundary between the abstract platform architecture and the concrete machines, services, and network paths that constitute a live deployment. This category covers storage substrate design, fleet topology, edge deployment patterns, key management operations, and the telemetry and mesh network that connect a fleet. Where the [[three-ring-architecture]] articles describe the logical model, the infrastructure articles describe the runtime — the physical substrate, the WireGuard tunnels, and the on-disk WORM ledger that any auditor can verify byte-for-byte.

## Storage substrate

The foundational persistence layer — the Write-Once-Read-Many ledger and the bookkeeping vault built on top of it.

- [[worm-ledger-design]] — The four-layer Write-Once-Read-Many ledger: tile-based, hash-chained, cryptographically signed; satisfies SEC 17a-4(f), eIDAS, and SOC 2 by structure rather than policy.
- [[worm-ledger-architecture]] — Architectural layout of the WORM ledger across Ring 1 services.
- [[worm-ledger-storage-architecture]] — Physical storage organisation for WORM ledger deployments.
- [[storage]] — Hardware-level append-only writes, tamper-evident records, legal deletion through cryptographic key destruction, and backup protection via cryptographically paired secondary drives.
- [[data-vault-bookkeeping-substrate]] — An SMB bookkeeping architecture built on an immutable source vault and append-only journal, with structural separation between the bookkeeping record and any accounting tool.
- [[cryptographic-ledgers]] — Immutable-state storage by hash-chain; any alteration breaks a verifiable cryptographic proof rather than a policy check.

## Fleet and edge deployment

How a deployment is provisioned, updated, and maintained across on-premises and cloud hardware.

- [[edge-deployment]] — Edge deployment patterns: external network connections routed through Ring 1 boundary-ingest services, payload sanitisation before the core processing rings, clean events recorded to the audit ledger rather than raw network traffic.
- [[tier-c-key-wiring]] — The operational procedure for managing external API keys in the Doorman service: where keys live, how they rotate, and how a breach is contained.
- [[genesis-protocol]] — How an isolated fleet bootstraps itself from a cold state, deriving its identity and pairings without an external authority.
- [[five-stage-supply-chain]] — Code moves from contributor to production through five stages, with a double-blind air-gap that separates production credentials from contributor workspaces.

## Network and telemetry

How fleet nodes communicate and how observability signals are collected without centralising identifiable data.

- [[sovereign-mesh]] — The WireGuard-based peer-to-peer mesh that connects PointSav fleet nodes without a central routing authority.
- [[pointsav-private-network]] — The private WireGuard mesh that connects Woodfine's fleet nodes, providing encrypted transport without granting application-layer access to the services on those nodes.
- [[ppn-command-protocol]] — The command protocol used over the private mesh: compact binary packets carried inside WireGuard tunnels.
- [[sovereign-telemetry]] — Zero-state telemetry: the V4 Intent Beacon collects behavioural and hardware signals from edge clients without cookies, session identifiers, or third-party analytics.
- [[telemetry-architecture]] — End-to-end telemetry pipeline: collection at production edge nodes, encrypted transport, locally controlled processing, no third-party cloud dependencies.
- [[data-sovereignty-telemetry]] — How telemetry preserves data-sovereignty guarantees while still producing operationally useful signal.

## See also

- [Architecture](/architecture/) — cross-cutting platform architecture and the three-ring model
- [Systems](/systems/) — the operating systems that run on this infrastructure
- [Services](/services/) — the services that depend on the storage and network substrate
- [Substrate](/substrate/) — the foundational mechanism concepts the infrastructure realises
