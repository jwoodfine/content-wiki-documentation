---
schema: foundry-doc-v1
title: "PPN Tenant VM Isolation"
slug: ppn-tenant-vm-isolation
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
paired_with: ppn-tenant-vm-isolation.es.md
short_description: "The PPN resource pool separates tenant workloads through namespace isolation, per-VM process isolation, and user-mode networking. Network-level subnet isolation is a planned milestone."
forbidden_terms_cleared: true
cites: []
---

The PointSav Private Network (PPN) resource pool allows multiple tenants to run virtual machines on a shared set of physical and cloud nodes. This article describes the isolation model: what separation is provided, what is not, and the planned path to stronger network-level isolation.

## The stack

Every virtual machine request passes through three layers before a QEMU process starts on a physical node:

- **Tenant proxy** — authenticates the caller, enforces namespace and quota, and is the sole external entry point
- **Fleet controller** — manages placement and delegates to the host agent; accepts connections only from the tenant proxy and internal mesh participants
- **Host agent** — spawns the QEMU process on the selected node; not reachable by external callers

A caller who has the fleet controller's address but not a valid tenant credential cannot reach the fleet controller directly — the authentication layer cannot be bypassed.

## What tenant isolation provides

### Namespace isolation

An authenticated tenant can create, list, and destroy only their own virtual machines. The tenant identity is injected by the tenant proxy into every request forwarded to the fleet controller; a tenant cannot supply a different identity in a request body. Listing VMs returns only records owned by the authenticated tenant. Destroy requests are validated against ownership before being forwarded.

This isolation survives fleet controller restarts: the tenant identity is stored in the VM record, echoed back in every node heartbeat, and restored to the in-memory registry on startup. Ownership is not held only in memory on the tenant proxy.

### Process isolation

Each virtual machine is a separate QEMU process on the physical node. Guest operating systems run in hardware-isolated address spaces (on nodes with KVM acceleration) or software-isolated address spaces (on TCG-only nodes). One tenant's virtual machine cannot read the memory or disk of another tenant's virtual machine through normal software paths.

### Per-VM network containment

Virtual machines use SLIRP user-mode networking: each guest receives a private NAT address stack with no inbound path from the host network or from other VMs. A guest process that opens a server socket is not reachable unless a host-forwarding rule was configured at spawn time. The VM creation response includes the list of forwarded host ports so callers know how to reach their VM.

### Bearer token security

Tenant credentials are opaque bearer tokens that map to a tenant identity in the tenant proxy's configuration. Knowing a tenant's identity string is not sufficient to authenticate; the caller must present the associated token. Tokens are not logged in any audit record.

### Audit trail

Every tenant lifecycle operation — create VM, destroy VM — is recorded in two places: a local append-only file on the tenant proxy, and the WORM ledger. The WORM record includes the tenant identity, operation type, VM identifier, timestamp, and outcome. WORM entries cannot be overwritten or deleted.

## What tenant isolation does not provide

### No per-tenant network subnet

All virtual machines on a given physical node egress through the same host network interface. A network observer watching the node's outbound traffic cannot distinguish traffic from one tenant's VM from traffic from another tenant's VM at the transport layer. Tenants are isolated at the application layer through separate network stacks but not at the network layer.

### No isolation from the node operator

Anyone with administrative access to the physical machine that hosts a VM can read the guest's disk image and memory. This is a property of the current QEMU-based virtualization model, not a limitation of the PPN control plane.

The intended response to both limitations is the seL4 isolation layer, described below.

## Quota enforcement

Each tenant has a maximum VM count configured in the tenant proxy. The tenant proxy enforces quotas using a serialized gate on concurrent create requests: two simultaneous requests from the same tenant both pass the quota check only if sufficient quota exists for both.

## Path to network-level isolation

Network-level isolation — per-tenant WireGuard subnets so tenant VMs are cryptographically unreachable from other tenants, not merely API-separated — requires two future milestones:

**Phase S3 of the PPN network control plane (planned):** The control plane gains the ability to manage WireGuard peer tables programmatically. When a new node joins the mesh, the control plane is intended to update all nodes' routing configurations automatically. This is the intended foundation for assigning each tenant a distinct subnet with its own WireGuard keys.

**seL4 Mode B (planned/intended):** The network control plane itself is intended to run as a first-class VM inside the PPN, isolated by a formally-verified microkernel. In Mode B, even a node operator with administrative access to the physical machine is intended to be unable to inspect the network control plane's configuration or extract tenant keys.

Until these milestones are delivered, the isolation boundary is accurately described as API-level isolation: tenants cannot reach each other's resources through the control plane, but they share physical network paths at the transport layer, and node operators retain administrative access to the physical machines they administer.

## See also

- [[ppn-small-business-compute|PPN Small-Business Compute]] — system overview, three-node stack, WireGuard mesh
- [[software-distribution-substrate|Software Distribution Substrate]] — binary distribution and license verification
