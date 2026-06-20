---
schema: foundry-doc-v1
content_type: topic
title: "PPN Small-Business Compute"
slug: topic-ppn-small-business-compute
aliases:
  - topic-ppn-small-business-compute
short_description: "The PointSav Private Network compute layer provides pooled virtual machine capacity to small-business customers through three cooperating services: fleet controller, per-node agent, and customer-facing tenant proxy."
category: architecture
type: reference
quality: complete
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-06-20
editor: pointsav-engineering
paired_with: topic-ppn-small-business-compute.es.md
cites: []
---

# PPN Small-Business Compute

The PointSav Private Network (PPN) compute layer provides pooled virtual machine
capacity to small-business customers. Capacity runs on cloud e2 instances under the
QEMU TCG hypervisor and is managed through three cooperating services: a fleet
controller, a per-node heartbeat agent, and a customer-facing tenant proxy.

## Architecture

### VM Image

Each VM instance boots from a NetBSD 10.1 QCOW2 disk image built by
`os-totebox/scripts/build-image.sh`. The image carries a curated set of services
in its overlay:

- `system-ledger-server` — append-only capability ledger (Unix socket at
  `/run/system-ledger/ledger.sock`)
- `slm-doorman-server` — small-language-model inference gateway
- `sshd` — operator access; `UseDNS no` to avoid banner timeout under TCG

Veriexec runs in strict mode (`kern.veriexec.strict=1`). A manifest generated at
image-build time covers every executable in the overlay; unsigned binaries are denied
execution at runtime.

### Fleet Controller (`service-vm-fleet`)

`service-vm-fleet` is the central coordinator for the PPN compute layer. It exposes
three endpoints:

| Endpoint | Method | Purpose |
|---|---|---|
| `/v1/vms` | POST | Register a new VM and receive advisory placement |
| `/v1/vms` | GET | List VMs; optional `?tenant_id=` filter |
| `/healthz` | GET | Health probe |

The controller ingests periodic heartbeats from `service-vm-host` agents running on
each node. Placement advice is based on reported available memory; the controller
holds no scheduling authority over the hypervisor.

### Per-Node Agent (`service-vm-host`)

`service-vm-host` runs on every physical host. It reads `/proc/meminfo` at each
heartbeat interval and reports current memory availability to the fleet controller.
A QEMU monitor stub is present for future live-migration support.

### Tenant Proxy (`service-vm-tenant`)

`service-vm-tenant` is the only endpoint exposed to customers. Requests carry a
`Bearer` token in the `Authorization` header. The proxy:

1. Validates the token against the in-memory `TenantStore`.
2. Checks quota (maximum VMs per tenant) before forwarding create requests to the
   fleet controller.
3. Writes an audit entry to `system-ledger-server` for each create attempt, approval,
   denial, and destroy.

If the ledger socket is unavailable, the proxy logs a warning and proceeds — the
ledger is advisory in the current phase.

### Wire Types (`system-vm-fleet-types`)

`system-vm-fleet-types` is a `no_std`-compatible library crate that defines the shared
wire types used by all three services:

- `VmRecord` — represents a registered VM instance; carries `tenant_id: Option<String>`
- `CreateVmRequest` — customer create payload
- `HeartbeatPayload` — per-node availability report

## Quota and Isolation

Each tenant is isolated by a numeric VM cap stored in `TenantRecord`. The proxy enforces
the cap before forwarding to the fleet controller; the fleet controller does not validate
tenant identity. A TOCTOU-safe create path holds a per-tenant `Mutex` for the duration
of the create–response cycle, preventing quota overshoot under concurrent requests from
the same tenant.

## Deployment

The PPN compute layer is intended to deploy with one fleet controller node and one or
more QEMU hosts, with the fleet controller and tenant proxy as workspace members in
`pointsav-monorepo`. The NetBSD image is built from source on each release via
`build-image.sh`.

## See Also

- [[topic-os-console-architecture|OS Console Architecture]] — the operator TUI for
  managing fleet state
- [[topic-software-distribution-substrate|Software Distribution Substrate]] — the
  licensing layer that gates customer access to PPN capacity
- [[topic-private-git-paid-customer-endpoint|Private Git Paid Customer Endpoint]] —
  binary delivery for licensed customers

---

*Woodfine Capital Projects™, MCorp™, PointSav Digital Systems™, Totebox Orchestration™, Totebox Archive™, and Capability Geometry™ are trademarks of Woodfine Capital Projects Inc., used in Canada, the United States, Latin America, and Europe. All other trademarks are the property of their respective owners.*
