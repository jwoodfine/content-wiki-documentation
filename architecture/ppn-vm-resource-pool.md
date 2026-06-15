---
schema: foundry-doc-v1
title: "PPN VM Resource Pool Architecture"
slug: ppn-vm-resource-pool
category: architecture
type: concept
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-06-15
editor: pointsav-engineering
paired_with: ppn-vm-resource-pool.es.md
short_description: "The PPN VM resource pool is a three-service stack that provisions, places, and accounts for virtual machines across a heterogeneous WireGuard mesh spanning cloud and physical nodes."
forbidden_terms_cleared: true
cites: []
---

The PointSav Private Network (PPN) VM resource pool is a three-service stack that provisions, places, and accounts for virtual machines across a heterogeneous WireGuard mesh. The pool combines cloud nodes with physical hardware, forming a distributed compute substrate that spans different capability profiles.

Three services partition the responsibility surface. The fleet controller maintains a global view of node capacity and handles placement decisions. The host agent runs per-node as the spawn authority, communicating with the hypervisor and holding the local state for each VM. The tenant proxy sits at the customer boundary, enforcing authentication, tenant namespace isolation, quota limits, and an immutable audit trail. Above this stack, a commercial inference broker manages metered workloads for the local SLM tier.

All service processes communicate across the PPN WireGuard underlay. No service exposes a public interface; all customer-facing traffic enters through the tenant proxy.

## Fleet controller

The fleet controller maintains an in-memory registry of node state: available capacity, hardware virtualisation availability, current VM count, and reservation status.

Placement uses a two-pass selection algorithm. The first pass considers only non-reserved nodes, satisfying the requested capacity ceiling. If the first pass yields no candidate, the second pass widens the search to include reserved nodes. This separation allows operators to designate nodes for latency-sensitive workloads while still permitting overflow placement under load.

Fleet status endpoints provide a global view of node state and per-tenant VM listings. Heartbeat ingestion from host agents is trust-bounded by the WireGuard underlay and node identity, not by separate credentials.

## Host agent

The host agent is the per-node spawn authority. Each node in the pool runs one instance, which accepts spawn and destroy requests forwarded by the fleet controller after placement.

On receiving a spawn request, the agent assembles the required initialisation configuration, invokes the hypervisor with the appropriate parameters, and writes state metadata alongside the disk image. This sidecar stores the VM identifier and enables heartbeat recovery after a process restart or node reboot without querying the fleet controller.

Nodes signal their reservation status and stable identity to the fleet controller at startup. Nodes where hardware virtualisation (KVM) is unavailable — such as cloud instances without nested virtualisation — report this capability flag in their heartbeat; the hypervisor falls back to software emulation on those nodes.

## Tenant proxy

The tenant proxy is the customer-facing layer. It accepts spawn, destroy, and status requests from authenticated callers and enforces the tenant contract before forwarding to the fleet controller.

Authentication uses bearer tokens issued at tenant provisioning time. Each token carries a tenant identifier that the proxy uses to namespace all VM records. A tenant may not query, modify, or destroy VMs belonging to another tenant; the proxy enforces this at every endpoint before any fleet interaction.

Quota enforcement operates at the capacity level. Each tenant is assigned a ceiling at provisioning time. The proxy checks current allocated capacity against the ceiling before forwarding a spawn request; requests that would exceed the quota are rejected. Concurrent creates from the same tenant are serialised through a per-tenant gate to prevent two simultaneous requests from both passing the quota check against the same pre-spawn total.

All write operations are appended to an immutable audit log. Each entry records the tenant identifier, VM identifier, operation type, timestamp, and request source. The log is append-only; no path touches existing entries.

## Inference broker

The inference broker manages metered traffic to the local SLM tier, positioned above the VM stack as the commercial brokering surface. It does not spawn or manage VMs directly; it brokers inference requests and accounts for per-tenant consumption.

The broker implements a circuit breaker with configurable thresholds. When the circuit is open or the admission gate is closed, incoming inference requests receive a service-unavailable response rather than queuing indefinitely. This protects the local SLM from load spikes that would otherwise degrade response latency for all tenants.

Per-tenant metering records token counts for each completed inference. A billing reconciliation endpoint aggregates metering records by tenant. License status is checked at startup and periodically thereafter; a license fault closes the admission gate without dropping in-flight requests.

## WireGuard mesh

The PPN underlay uses a WireGuard mesh. All service processes bind to their WireGuard interface addresses, not to public interfaces. Peer configuration is static; each node holds the public keys of its peers and the routing ranges for each tunnel.

A cloud relay node forwards traffic between physical nodes that are on separate networks without a direct route, though WireGuard uses direct peer paths when available. The relay role does not require the cloud node to participate in VM placement — it operates at the network layer only.

Node heterogeneity is a deliberate property of the pool. Each node type contributes a different capability profile: cloud nodes provide reliable uptime and elastic storage; physical nodes provide hardware-accelerated virtualisation. Placement decisions reflect these differences through the capability flag and the two-pass reserved/non-reserved selection algorithm.

## Planned extensions

Three extensions to the compute substrate are intended for future deployment; none is operational today.

**Microkernel isolation (planned/intended):** The VM spawn path on AArch64 hardware is intended to use a formally-verified microkernel component model. The intended design would replace the host kernel as the trust boundary for VM isolation, providing formal verification of the scheduler and inter-process communication paths between VMs.

**Lightweight microVM (planned/intended):** An alternative hypervisor backend is under evaluation for workloads where sub-second boot time and reduced memory overhead are priorities. The intended integration point is the host agent, which would select the hypervisor backend based on the workload type specified in the spawn request.

**Bare-metal provisioning ISO (planned/intended):** A signed, reproducible boot image is intended as the provisioning substrate for new PPN nodes. The planned design is intended to install the full node stack from a single boot, without requiring an existing operating system install or manual configuration.

## See also

- [[ppn-small-business-compute|PPN Small-Business Compute]] — the small-business product built on the PPN resource pool
- [[ppn-tenant-vm-isolation|PPN Tenant VM Isolation]] — detailed isolation model and planned network-level isolation
- [[software-distribution-substrate|Software Distribution Substrate]] — binary distribution and license verification
