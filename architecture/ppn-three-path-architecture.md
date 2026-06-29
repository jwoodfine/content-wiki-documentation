---
schema: foundry-doc-v1
title: "PPN Three-Path seL4 Architecture"
slug: ppn-three-path-architecture
category: architecture
type: topic
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-06-29
editor: pointsav-engineering
paired_with: ppn-three-path-architecture.es.md
short_description: "Three sequential seL4 architecture options for PPN infrastructure nodes: Option B ships first (seL4 hypervisor + Linux guest), Option C adds WireGuard as a seL4 protection domain, and Option A targets a pure seL4 environment with no virtual machines."
cites: []
---

The PointSav Private Network node stack is designed around the seL4 microkernel. Three architecture options define the roadmap. They are sequential: Option B is the current development path; Option C gates on Option B shipping and remaining stable; Option A gates on Option C. All three are documented together so that decisions made in Option B do not foreclose the later options.

---

## Option B — seL4 hypervisor with Linux guest

**Current path.**

seL4 runs as a Type 1 hypervisor at EL2 (AArch64) or with VT-x (x86-64). The CAmkES VMM runs as a seL4 protection domain and hosts one Linux (Debian 12) guest VM. All PPN services — WireGuard, fleet management, inference routing — run inside the Linux guest.

```
Hardware
└── seL4 microkernel (EL2 / VT-x)
    └── CAmkES VMM [seL4 PD]
        └── Linux (Debian 12) guest
            ├── WireGuard mesh interface
            ├── service-vm-fleet
            ├── service-vm-host
            └── os-network-admin
```

**What seL4 provides:** The kernel is formally verified. No guest VM can access the hypervisor layer, another guest's memory, or any seL4 kernel object without an explicit seL4 capability grant. On AArch64 EL2, the integrity proof (April 2025) extends this to a machine-checked guarantee.

**What seL4 does not provide in Option B:** The CAmkES VMM and Linux guest are not formally verified. A compromised Linux guest remains confined by seL4's capability topology, but services inside the guest are trusted relative to each other by Linux's normal process model.

**Formal security coverage:**

| Architecture | Formal claim | Notes |
|---|---|---|
| AArch64 EL2 | seL4 integrity proof (April 2025) | Valid formal security claim at the hypervisor boundary |
| x86-64 | Functional correctness only | No formal integrity proof; development target only |

---

## Option C — seL4 protection domains own WireGuard

**Status: planned/intended.** Gate: Option B ships and is stable for six months or more.

Hybrid architecture. seL4 protection domains own WireGuard and the PPN network control plane. A Linux guest VM hosts non-critical workloads. The security boundary is the WireGuard protection domain — the Linux VM cannot modify peer tables without going through seL4 IPC.

```
seL4 microkernel (EL2 / VT-x)
├── PD: wireguard-control  [WireGuard peer table, CPace gating]
├── PD: ppn-gate           [seL4 IPC channel enforcement]
└── CAmkES VMM
    └── Linux guest (Doorman, fleet, telemetry, media)
```

By moving the WireGuard mesh interface to a seL4 protection domain, a fully compromised Linux VM cannot gain access to peer tables or the ability to add or remove nodes. Peer addition flows through seL4 IPC to the wireguard-control domain, which validates each request independently.

What changes from Option B: `os-network-admin`'s WireGuard management moves from Linux to a seL4 PD; the Linux guest has no `wg0` interface; peer addition requests flow Linux VM → seL4 IPC → wireguard-control PD → kernel state.

---

## Option A — Pure seL4 protection domains, no virtual machines

**Status: planned/intended.** Gate: Option C ships and is stable.

No virtual machines. No VMM. Every PPN service is a seL4 protection domain. WireGuard is ported to a seL4 PD with no Linux socket layer. Fleet management and service routing are protection domains. This produces the smallest possible trusted computing base.

```
seL4 microkernel (EL2 — AArch64 only for formal claims)
├── PD: wireguard     [WireGuard crypto + peer table, seL4 IPC only]
├── PD: fleet-tracker [service-vm-fleet, no tokio, no std net]
├── PD: doorman       [inference routing, seL4 IPC-based]
└── PD: ppn-control   [os-network-admin, CPace ceremony]
```

Eliminating the Linux guest removes the largest unverified component from the stack. On AArch64 EL2 with the confidentiality proof in progress as of mid-2026, Option A targets all three CIA properties at the kernel layer — the deepest security posture of the three options.

---

## Microkit 2.2.0 architecture targets

Microkit 2.2.0 — the seL4 Foundation's recommended framework for new seL4 projects — supports these hardware targets:

| Target | Architecture | Hardware virtualisation | Verification |
|---|---|---|---|
| `aarch64` | AArch64 | No (EL2 only) | Integrity proof (April 2025) |
| `x86_64_generic` | x86-64 | No (TCG software) | Functional correctness |
| `x86_64_generic_vtx` | x86-64 | Yes (VT-x/AMD-V) | Functional correctness |

x86-64 support was added in Microkit 2.1.0. This architecture is a valid development and runtime target but does not carry the integrity or confidentiality proofs available on AArch64.

---

## Summary

| Option | seL4 as | Linux | Trusted computing base | Verification | Status |
|---|---|---|---|---|---|
| B (current) | Hypervisor | Guest VM | seL4 + VMM + Linux | AArch64 integrity | Active |
| C (planned) | Hypervisor + WireGuard PD | Guest VM (limited) | seL4 + VMM + WireGuard PD + Linux | AArch64 integrity | Planned/intended |
| A (planned) | OS (all components) | None | seL4 only | AArch64 all CIA (in progress) | Planned/intended |

## See also

- [[sel4-capability-topology]] — formal basis: how the seL4 capability topology determines security boundaries
- [[ppn-architecture-overview]] — how the seL4 hypervisor layer fits into the four-layer PPN stack
- [[sovereign-mesh]] — the WireGuard overlay that runs within the Linux guest (Option B) or as a seL4 PD (Option C/A)
- [[os-products-distribution-model]] — artifact formats in which os-infrastructure ships for deployment
