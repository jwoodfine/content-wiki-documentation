---
schema: foundry-doc-v1
title: "Infrastructure"
slug: infrastructure-index
category: infrastructure
type: topic
content_type: topic
quality: complete
short_description: "Fleet deployment topology, cloud operational runtime, and physical infrastructure — the WORM ledger storage substrate, edge deployment patterns, the private WireGuard mesh, sovereign telemetry, key-wiring operations, and the bookkeeping vault that anchors the SMB accounting surface."
index_type: thematic
index_scope: infrastructure
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-08-06
editor: pointsav-engineering
paired_with: _index.es.md
---

Infrastructure articles sit at the boundary between the abstract platform architecture and the concrete machines, services, and network paths that constitute a live deployment. This category covers storage substrate design, fleet topology, edge deployment patterns, key management operations, and the telemetry and mesh network that connect a fleet. Where the [[three-ring-architecture]] articles describe the logical model, the infrastructure articles describe the runtime — the physical substrate, the WireGuard tunnels, and the on-disk WORM ledger that any auditor can verify byte-for-byte.

<!-- START-HERE-HIGHLIGHT: engine reads this block to render the single "start here" card
     (reuses the existing cluster-card--start-here component). Do not add more than one. -->

**Start here:** [[worm-ledger-design|The WORM ledger design]] — the four-layer, tile-based, hash-chained ledger that every other article in this category ultimately writes to or builds on.

<!-- END-START-HERE-HIGHLIGHT -->

## Storage substrate

The foundational persistence layer — the Write-Once-Read-Many ledger and the bookkeeping vault built on top of it.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: storage-substrate -->
- [[totebox-archive]] — A self-contained, freely transferable micro-virtual machine that persists institutional data as immutable flat files; the deployment and storage unit for the [[totebox-os|os-totebox]] archive layer.
- [[worm-ledger-design]] — The four-layer Write-Once-Read-Many ledger: tile-based, hash-chained, cryptographically signed; satisfies SEC 17a-4(f), eIDAS, and SOC 2 by structure rather than policy.
- [[worm-ledger-architecture]] — Architectural layout of the WORM ledger across Ring 1 services.
- [[worm-ledger-storage-architecture]] — Physical storage organisation for WORM ledger deployments.
- [[storage]] — Hardware-level append-only writes, tamper-evident records, legal deletion through cryptographic key destruction, and backup protection via cryptographically paired secondary drives.
- [[data-vault-bookkeeping-substrate]] — An SMB bookkeeping architecture built on an immutable source vault and append-only journal, with structural separation between the bookkeeping record and any accounting tool.
- [[cryptographic-ledgers]] — Immutable-state storage by hash-chain; any alteration breaks a verifiable cryptographic proof rather than a policy check.
<!-- END AUTO-GENERATED -->

## Fleet and edge deployment

How a deployment is provisioned, updated, and maintained across on-premises and cloud hardware.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: fleet-and-edge-deployment -->
- [[edge-deployment]] — Edge deployment patterns: external network connections routed through Ring 1 boundary-ingest services, payload sanitisation before the core processing rings, clean events recorded to the audit ledger rather than raw network traffic.
- [[tier-c-key-wiring]] — The operational procedure for managing external API keys in the Doorman service: where keys live, how they rotate, and how a breach is contained.
- [[genesis-protocol]] — How an isolated fleet bootstraps itself from a cold state, deriving its identity and pairings without an external authority.
- [[five-stage-supply-chain]] — Code moves from contributor to production through five stages, with a double-blind air-gap that separates production credentials from contributor workspaces.
<!-- END AUTO-GENERATED -->

## Network and telemetry

How fleet nodes communicate and how observability signals are collected without centralising identifiable data.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: network-and-telemetry -->
- [[sovereign-mesh]] — The WireGuard-based peer-to-peer mesh that connects PointSav fleet nodes without a central routing authority.
- [[ppn-mesh-architecture]] — The private WireGuard mesh that connects Woodfine's fleet nodes, providing encrypted transport without granting application-layer access to the services on those nodes.
- [[ppn-command-protocol]] — The command protocol used over the private mesh: compact binary packets carried inside WireGuard tunnels.
- [[sovereign-telemetry]] — Zero-state telemetry: the V4 Intent Beacon collects behavioural and hardware signals from edge clients without cookies, session identifiers, or third-party analytics.
- [[telemetry-architecture]] — End-to-end telemetry pipeline: collection at production edge nodes, encrypted transport, locally controlled processing, no third-party cloud dependencies.
- [[data-sovereignty-telemetry]] — How telemetry preserves data-sovereignty guarantees while still producing operationally useful signal.
<!-- END AUTO-GENERATED -->

## Compute and VM fabric

How virtual machines are pooled, isolated, and secured across PPN nodes — from the per-node hypervisor resource pool to the seL4 architecture roadmap and the planned distributed fabric that lets VMs borrow compute across the mesh.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: compute-and-vm-fabric -->
- [[ppn-vm-resource-pool|PPN VM resource pool]] — The three-service stack — fleet controller, host agent, tenant proxy — that provisions, places, and accounts for VMs across a heterogeneous WireGuard mesh.
- [[ppn-hypervisor-resource-pool|PPN hypervisor resource pool]] — Per-node CPU and RAM pooling via virtio_balloon and cgroups v2 weights, structurally blind to the data-layer aggregator above it.
- [[ppn-tenant-vm-isolation|PPN tenant VM isolation]] — What namespace, process, and network isolation the PPN resource pool provides today, and the planned path to per-tenant WireGuard subnets.
- [[ppn-distributed-vm-fabric|PPN distributed VM fabric]] — The planned extension of the per-node hypervisor layer to a multi-node pool: cross-node memory lending, a distributed capability ledger, and a sovereign attestation chain.
- [[ppn-three-path-architecture|PPN three-path seL4 architecture]] — Three sequential seL4 options for PPN infrastructure nodes, from a hypervisor with a Linux guest to protection domains with no virtual machines at all.
<!-- END AUTO-GENERATED -->

## See also

- [Architecture](/architecture/) — cross-cutting platform architecture and the three-ring model
- [Systems](/systems/) — the operating systems that run on this infrastructure
- [Services](/services/) — the services that depend on the storage and network substrate
- [Substrate](/substrate/) — the foundational mechanism concepts the infrastructure realises
