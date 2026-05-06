---
schema: foundry-doc-v1
title: "seL4 Foundation"
slug: sel4-foundation
category: architecture
type: topic
quality: stub
short_description: "The seL4 foundation is the formally verified microkernel that acts as the root of trust in PointSav's operating-system layer, providing mathematically proven isolation between all hardware resources and software components."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-04-30
editor: pointsav-engineering
cites: []
paired_with: sel4-foundation.es.md
---

# seL4 Foundation

> The seL4 foundation is the formally verified microkernel that acts as the root of trust in PointSav's operating-system layer, providing mathematically proven isolation between all hardware resources and software components.

**The seL4 foundation** refers to the formally verified C-based microkernel that underpins the PointSav operating-system layer. seL4 is formally verified in Isabelle/HOL, meaning its isolation properties are mathematically proven for the verified hardware configuration rather than asserted by policy. It acts as the absolute root of trust: every hardware resource — CPU time, physical memory, network interfaces, storage — is allocated and isolated through the seL4 kernel. The Rust capability manager that enforces the PointSav capability-based security model executes on top of the seL4 foundation. No software component can bypass kernel-enforced isolation to reach a hardware resource it has not been explicitly granted access to.

<!-- EXPAND: lead needs 200+ words -->

## Overview

The microkernel design is deliberately minimal. seL4 handles only the most primitive operations: routing physical memory to isolated address spaces and scheduling CPU time. All drivers, network interfaces, and application services run outside the kernel in protected user-space processes. This means the formally verified kernel code base is small enough to verify exhaustively — the entire isolation guarantee is proven, not approximated.

When the PointSav platform operates on hardware where seL4 can boot natively, the isolation boundary is kernel-enforced and formally verified. When hardware does not support native seL4 boot, a Linux or BSD guest VM hosted inside a seL4-based hypervisor provides equivalent structural isolation around the guest — the seL4 hypervisor layer provides verified containment even when the guest OS is conventional.

## Architecture

seL4 sits below the Rust capability manager and below all PointSav operating-system variants (ToteboxOS, MediaKit OS). The capability manager reads a system policy at deployment time and requests the kernel to grant or deny capability tokens to each process. The kernel enforces those grants at runtime; the capability manager cannot override a kernel-level isolation boundary.

The `service-fs` WORM ledger and all Ring 1 boundary-ingest services operate within process isolation provided by the seL4 foundation. Cross-tenant access is structurally impossible because no process holds capability grants into another tenant's address space.

## See Also

- [[capability-based-security]]
- [[worm-ledger-architecture]]
- [[3-layer-stack]]
- [[compounding-substrate]]
- [[machine-based-auth]]

## References

- `conventions/system-substrate-doctrine.md` — The Two-Bottoms substrate and seL4 as the security foundation
- `DOCTRINE.md §XIV` — Compounding Substrate context; seL4 as the Boot-Anywhere Capability Recovery mechanism
- `conventions/three-ring-architecture.md` — Ring 1 isolation model that seL4 underpins


---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*

*Woodfine Capital Projects™, Woodfine Management Corp™, PointSav Digital Systems™, Totebox Orchestration™, and Totebox Archive™ are trademarks of Woodfine Capital Projects Inc., used in Canada, the United States, Latin America, and Europe. All other trademarks are the property of their respective owners.*
