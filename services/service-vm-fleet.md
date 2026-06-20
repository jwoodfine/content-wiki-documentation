---
schema: foundry-doc-v1
title: "service-vm-fleet"
slug: service-vm-fleet
category: services
type: service
content_type: topic
quality: stub
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-06-20
editor: pointsav-engineering
paired_with: service-vm-fleet.es.md
short_description: "The fleet controller maintains a global view of node capacity across the PPN WireGuard mesh and handles placement decisions for virtual machine spawns."
cites: []
---

The fleet controller is the placement and registry service for the PPN VM resource pool. It maintains an in-memory registry of node state — available capacity, hardware virtualisation availability, current VM count, and reservation status — and resolves placement requests from the [[service-vm-tenant|tenant proxy]].

## Placement algorithm

Placement uses a two-pass selection algorithm. The first pass considers only non-reserved nodes, satisfying the requested capacity ceiling. If the first pass yields no candidate, the second pass widens the search to include reserved nodes. This separation allows operators to designate nodes for latency-sensitive workloads while still permitting overflow placement under load.

## Heartbeat ingestion

Host agents report node state to the fleet controller via periodic heartbeats. Ingestion is trust-bounded by the WireGuard underlay and node identity, not by separate credentials. Heartbeat data — available memory, CPU load, KVM availability, current VM count — updates the in-memory registry directly.

## Fleet status endpoints

The fleet controller exposes endpoints for global node state and per-tenant VM listings. These endpoints serve the tenant proxy and operator tooling.

## See also

- [[ppn-vm-resource-pool|PPN VM Resource Pool Architecture]] — full architecture overview including fleet controller, host agent, and tenant proxy
- [[service-vm-tenant|service-vm-tenant]] — the customer-facing tenant proxy that submits placement requests
- [[ppn-small-business-compute|PPN Small-Business Compute]] — the commercial product built on the PPN substrate

*Woodfine Capital Projects™, MCorp™, PointSav Digital Systems™, Totebox Orchestration™, Totebox Archive™, and Capability Geometry™ are trademarks of Woodfine Capital Projects Inc., used in Canada, the United States, Latin America, and Europe. All other trademarks are the property of their respective owners.*
