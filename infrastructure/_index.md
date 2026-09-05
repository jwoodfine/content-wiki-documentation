---
schema: foundry-doc-v1
title: "Where It Runs"
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
last_edited: 2026-09-04
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
- [[totebox-archive]] — A Totebox Archive is a sovereign data vault for a single entity — a freely transferable bootable disk image storing WORM flat files, accessed only via the Diode Standard.
- [[worm-ledger-design]] — Write-Once-Read-Many ledger substrate for PointSav Ring 1 services, designed toward a hash-chained, signed format that satisfies recordkeeping rules by structure.
- [[worm-ledger-architecture]] — The per-tenant WORM immutable ledger every Ring 1 service writes through, built on C2SP tlog-tiles with hash-chaining and monthly Sigstore Rekor anchoring.
- [[worm-ledger-storage-architecture]] — C2SP tlog-tiles is the target storage primitive; the current service-fs build persists a per-tenant JSON append log pending the tile backend, immutable by design.
- [[storage]] — The platform's tamper-evident record rests on filesystem read-only permissions and a cryptographic hash chain, not a hardware write-block — a privileged administrator can still bypass it, and any bypass is detectable, not prevented.
- [[data-vault-bookkeeping-substrate]] — An SMB bookkeeping and accounting architecture built on an immutable source vault and append-only journal, structurally separate from any accounting tool.
<!-- END AUTO-GENERATED -->

## Fleet and edge deployment

How a deployment is provisioned, updated, and maintained across on-premises and cloud hardware.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: fleet-and-edge-deployment -->
- [[edge-deployment]] — The platform routes external network connections through Ring 1 boundary-ingest services at the edge, sanitizing payloads before core processing and recording clean events.
- [[tier-c-key-wiring]] — The operational procedure for managing external API keys in the Doorman service — where keys live, how they are provisioned, how they rotate, and how a breach is contained.
- [[os-orchestration-stateless-hub]] — os-orchestration coordinates work across Totebox Archives without storing customer data, keys, or audit records — a stateless routing surface above the capability layer.
<!-- END AUTO-GENERATED -->

## Network and telemetry

How fleet nodes communicate and how observability signals are collected without centralising identifiable data.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: network-and-telemetry -->
- [[sovereign-mesh]] — The sovereign mesh is the application-level WireGuard overlay connecting every PPN fleet node, carrying signed binary commands without a centralised message broker.
- [[ppn-mesh-architecture]] — Hub-and-spoke WireGuard mesh connecting fleet nodes, with physical key custody on the operator's premises and Mesh Fusion node joining.
- [[ppn-command-protocol]] — The PPN Command Protocol is the 16-byte binary wire format app-network-admin uses to issue commands to os-infrastructure nodes over WireGuard, with no central broker.
- [[sovereign-telemetry]] — Zero-state telemetry: a single unload beacon carrying URI and timestamp, paired server-side with the requester's IP and user agent, written unmasked to an append-only CSV ledger.
- [[telemetry-architecture]] — The platform collects web traffic analytics from production edge nodes, routing them to a locally controlled environment via an encrypted path, no third-party cloud.
<!-- END AUTO-GENERATED -->

## Compute and VM fabric

How virtual machines are pooled, isolated, and secured across PPN nodes — from the per-node hypervisor resource pool to the seL4 architecture roadmap and the planned distributed fabric that lets VMs borrow compute across the mesh.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: compute-and-vm-fabric -->
- [[ppn-vm-resource-pool|PPN VM resource pool]] — The PPN VM resource pool is a three-service stack that provisions, places, and accounts for VMs across a heterogeneous WireGuard mesh spanning cloud and physical nodes.
- [[ppn-hypervisor-resource-pool|PPN hypervisor resource pool]] — The PPN hypervisor layer is designed to manage a per-node pool of CPU and RAM via virtio_balloon and cgroups v2 — neither mechanism is built in os-infrastructure yet.
- [[ppn-tenant-vm-isolation|PPN tenant VM isolation]] — The PPN resource pool separates tenant workloads through namespace isolation, per-VM process isolation, and user-mode networking; subnet isolation is a planned milestone.
- [[ppn-distributed-vm-fabric|PPN distributed VM fabric]] — The planned extension of the per-node PPN hypervisor layer to a multi-node resource pool, letting VMs borrow compute and migrate across the fleet automatically.
- [[ppn-three-path-architecture|PPN three-path seL4 architecture]] — Three sequential seL4 options for PPN infrastructure nodes: Option B ships first (hypervisor + Linux guest), Option C adds WireGuard as a protection domain.
- [[ppn-architecture-overview]] — Physical infrastructure plane of the PointSav stack, enrolling nodes into a cryptographically authenticated mesh and hosting the fleet's virtual machines.
- [[spot-vm-lifecycle-kill-switch]] — Single-controller lifecycle for the Yo-Yo spot VM — why one timer owns both start and stop, plus the sentinel-file kill switch for immediate operator override.
<!-- END AUTO-GENERATED -->

## See also

- [How It's Built](/architecture/) — cross-cutting platform architecture and the three-ring model
- [Operating Systems](/systems/) — the operating systems that run on this infrastructure
- [Platform Services](/services/) — the services that depend on the storage and network substrate
- [Building Blocks](/substrate/) — the foundational mechanism concepts the infrastructure realises
