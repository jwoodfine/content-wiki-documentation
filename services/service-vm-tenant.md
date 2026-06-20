---
schema: foundry-doc-v1
title: "service-vm-tenant"
slug: service-vm-tenant
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
paired_with: service-vm-tenant.es.md
short_description: "The tenant proxy enforces authentication, namespace isolation, quota limits, and an immutable audit trail at the customer boundary of the PPN VM resource pool."
cites: []
---

The tenant proxy is the customer-facing layer of the PPN VM resource pool. It accepts spawn, destroy, and status requests from authenticated callers and enforces the tenant contract before forwarding to the [[service-vm-fleet|fleet controller]].

## Authentication and namespace isolation

Authentication uses bearer tokens issued at tenant provisioning time. Each token carries a tenant identifier that the proxy uses to namespace all VM records. A tenant may not query, modify, or destroy VMs belonging to another tenant; the proxy enforces this at every endpoint before any fleet interaction.

## Quota enforcement

Each tenant is assigned a capacity ceiling at provisioning time. The proxy checks current allocated capacity against the ceiling before forwarding a spawn request; requests that would exceed the quota are rejected. Concurrent creates from the same tenant are serialised through a per-tenant gate to prevent two simultaneous requests from both passing the quota check against the same pre-spawn total.

## Audit trail

All write operations are appended to an immutable audit log. Each entry records the tenant identifier, VM identifier, operation type, timestamp, and request source. The log is append-only; no path touches existing entries.

## See also

- [[ppn-vm-resource-pool|PPN VM Resource Pool Architecture]] — full architecture overview including fleet controller, host agent, and tenant proxy
- [[ppn-tenant-vm-isolation|PPN Tenant VM Isolation]] — the isolation model enforced by the tenant proxy
- [[service-vm-fleet|service-vm-fleet]] — the fleet controller that receives forwarded spawn requests

*Woodfine Capital Projects™, MCorp™, PointSav Digital Systems™, Totebox Orchestration™, Totebox Archive™, and Capability Geometry™ are trademarks of Woodfine Capital Projects Inc., used in Canada, the United States, Latin America, and Europe. All other trademarks are the property of their respective owners.*
