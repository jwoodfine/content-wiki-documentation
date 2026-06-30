---
schema: foundry-doc-v1
title: "The seL4 microkernel substrate"
slug: sel4-microkernel-substrate
short_description: "The platform adopts the mathematically formally verified seL4 microkernel as the L1 kernel for all PointSav operating systems, providing structurally guaranteed memory isolation, zero buffer overflows, capability-based permissions, and deterministic execution without building a custom kernel."
category: substrate
type: concept
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-15
editor: pointsav-engineering
paired_with: sel4-microkernel-substrate.es.md
references:
  - id: 1
    text: "Klein, G., et al. 'seL4: Formal Verification of an OS Kernel.' ACM SOSP, 2009."
    url: "https://dl.acm.org/doi/10.1145/1629575.1629596"
  - id: 2
    text: "seL4 Foundation. 'seL4 Reference Manual.' seL4 Foundation, 2023."
    url: "https://sel4.systems/Info/Docs/seL4-manual-latest.pdf"
---

The seL4 microkernel is the mathematically formally-verified L1 kernel on which all PointSav operating systems run — its security properties are proved by formal mathematical proof, not asserted by testing. [^1] PointSav adopts seL4 as raw material rather than building a custom kernel, and constructs its proprietary Rust layer above it. Memory isolation, zero buffer overflows, [[capability-ledger-substrate|capability-based permissions]], and deterministic execution are guaranteed structurally — the foundation for security claims that can be reasoned about formally and presented to regulators rather than merely asserted through penetration testing. This article covers the architectural rationale, the layered stack, the toolchain constraints, and the [[system-substrate-doctrine|language discipline]] enforced above the kernel.

## Why adopt rather than build

A reasonable alternative would be to write a custom kernel. PointSav explicitly rejects that path:

| Option | Cost | Outcome |
|---|---|---|
| Build a custom kernel | Tens of millions of dollars; five or more years of formal-verification work | Catching up to a 2009 standard in the 2030s |
| Adopt seL4 | Zero | Already proved; ready to build on |

The principle is to use seL4 as a raw material — like structural steel — and build the proprietary value above it. PointSav's competitive technical work happens in the [[system-substrate-doctrine|Rust layer above seL4]], not in the kernel itself.

## The layered stack

| Layer | Component | Owner |
|---|---|---|
| L0 — Hardware | x86_64 Haswell+ CPU (see [[hardware-reference|hardware reference]]) | Hardware vendor |
| L1 — Microkernel | seL4 [^2] | seL4 project (adopted upstream; minor patches) |
| L2 — Driver framework | sDDF (seL4 Device Driver Framework) with VirtIO | seL4 ecosystem |
| L3 — System packages | `system-*` Rust crates — drivers, networking, filesystem | PointSav |
| L4 — Services | `service-*` Rust crates — application logic | PointSav |
| L5 — Operating systems | `os-*` compositions | PointSav |
| L6 — Applications | `app-*` user surfaces | PointSav |

The boundary between L2 (kernel-adjacent) and L3 (PointSav-owned) is the line PointSav draws around its proprietary value. Everything below is adopted commodity; everything above is owned.

When the target hardware does not support native seL4 boot, a Linux or BSD guest VM inside a seL4-based hypervisor provides equivalent structural isolation around the guest OS. The hypervisor layer supplies formally-verified containment even when the guest itself is a conventional operating system.

## What seL4 provides

| Property | What it means in practice |
|---|---|
| Mathematical isolation | If `service-email` crashes, `service-people` cannot feel it; the kernel guarantees the boundary |
| Deterministic execution | Real-time guarantees on instruction timing — important for synchronisation protocols |
| Capability-based security | Permissions are passed as cryptographic capability tokens, not entries in a central permission table |
| Zero buffer overflows in the kernel | The class of vulnerability that produces most OS CVEs is mathematically excluded from the kernel |

The result is a substrate where security properties can be reasoned about formally rather than asserted by penetration testing. This changes what kinds of security claims can be defensibly presented to a regulator — and forms the [[compliance-and-continuous-disclosure|continuous-proof compliance]] foundation.

## The Microkit and toolchain constraints

seL4 is intentionally minimal: it provides capabilities and inter-process communication and very little else. To make it practically usable, PointSav relies on the seL4 Microkit, a framework that translates higher-level system descriptions (XML manifests, ELF binaries) into the low-level capability operations the kernel expects.

The Microkit has constraints. One is documented in detail in the engineering archive: the Microkit's x86_64 builder eagerly maps 1 GB Huge Pages for kernel code, and then fails to shatter those pages back into 4 KB sub-pages when subsequent small mappings collide. The pragmatic resolution — placing the IPC buffer at the very bottom of memory and the kernel just above it — is the kind of fine-grained discipline that working at this layer demands.

This is a Microkit tooling quality-of-life issue, not a kernel bug. seL4 is working as designed for a high-assurance system that prioritises deterministic memory layout over developer convenience.

## Language discipline

The substrate enforces one language above the kernel: Rust.

| Language | Status | Reasoning |
|---|---|---|
| Rust | Mandatory for all `system-*`, `service-*`, and `os-*` code | Memory safety without garbage collection; aligns with seL4's formal verification |
| C / C++ | Banned at L3 and above | A single buffer overflow in C undoes the value of seL4's proofs |
| Python / JavaScript | Banned at L3 and above | Requires heavyweight runtimes; cannot run as a seL4 Protection Domain without violating isolation guarantees |
| WebAssembly | Permitted for guest user extensions only | A future user-plugin format; runs inside a Rust-hosted Wasm runtime, never as a core service |

Allowing one non-Rust service into a Protection Domain would reintroduce runtime bloat and unpredictable execution that the microkernel substrate is designed to eliminate.

## The end-state architecture

The long-term shape of the substrate is a Multi-Server Microkernel OS: every service — networking, filesystem, application logic — runs as an isolated unikernel passing messages through seL4 IPC. The kernel's only job is hardware routing and capability enforcement.

This is one of the most difficult patterns in computer science to engineer correctly. The substrate is now mature enough — through frameworks like Genode and Rust-based unikernel compilers — for an institutional vendor to build [[os-family-overview|operating system surfaces]] on it.

## See also

- [[machine-based-auth]] — capability-based authorization built above the seL4 capability model
- [[diode-standard]] — the unidirectional command flow protocol enforced above the kernel
- [[os-family-overview]] — the five OS surfaces that compose above this substrate
- [[hardware-reference]] — the CPU architectural requirements (Haswell+, fsgsbase, 1 GB Huge Pages)
- [[compliance-and-continuous-disclosure]] — how formal kernel verification supports continuous-proof compliance
