---
schema: foundry-doc-v1
type: topic
content_type: topic
slug: os-totebox-service-pd-model
title: "How service-* Become seL4 Protection Domains on os-totebox"
short_description: "Explains how os-totebox maps Rust service binaries to seL4 Protection Domains, covering the seven-PD stack, capability confinement model, startup ordering, and the two-bottom development path."
audience: vendor-public
bcsc_class: current-fact
language: en
paired_with: os-totebox-service-pd-model.es.md
category: architecture
status: active
quality: complete
last_edited: 2026-06-23
---

# How service-* Become seL4 Protection Domains on os-totebox

os-totebox is the Sovereign WORM Data Vault tier of the three-binary architecture. It runs as a Type I bare-metal OS on top of the seL4 microkernel — no shell, no root process, no init system, no package manager. Every service that handles durable data is a seL4 Protection Domain (PD): a hardware-enforced isolation unit whose capability set is fixed at build time and cannot be extended at runtime. This article explains what that means, why the design takes the shape it does, and how two planned tools — moonshot-sel4-vmm and moonshot-toolkit — turn ordinary Rust service binaries into a formally verified PD graph.

## The toolchain that makes it work

Two components are intended to assemble the os-totebox system image (Phase H1, planned):

**moonshot-sel4-vmm** is a ~300-line Rust crate that acts as the PD runtime. It provides the `sel4_main!` entry point macro that each service binary uses in place of `fn main()`, initialises the IPC channels between PDs at boot, and registers each PD's heartbeat with the watchdog. The crate targets the seL4 Microkit ABI — it does not use the external rust-sel4 crate. That external dependency was evaluated and rejected; the sovereign runtime is the only seL4 Rust binding in use.

**moonshot-toolkit** is the system image builder (v0.3.1, 35 tests, Phase 1C complete). It reads a TOML system specification — `examples/os-totebox.toml` — and emits a `.system` file describing the full PD graph: which PDs exist, what capabilities each one holds, how IPC endpoints are wired, and what memory regions are assigned. The toolkit's image verifier asserts, at build time, that the block device capability appears exactly once in the grant table — held by service-fs PD and by no other PD. If that assertion fails, the build fails.

The TOML spec is the single authoritative declaration of the PD graph. A developer who wants to understand which service can reach which resource reads `os-totebox.toml`, not a runtime configuration file or a policy document.

## Seven protection domains — why this many, and not more

The planned production stack (Phase H1+) runs seven PDs. Each PD corresponds directly to a service binary already in the monorepo. The priority values follow the seL4 Microkit convention: a higher number means the scheduler will preempt a lower-priority PD to run this one.

| PD | Crate | Priority | Block device cap |
|----|-------|----------|-----------------|
| watchdog-pd | system-security | 250 | No |
| service-fs PD | service-fs | 200 | Yes (only grant) |
| network-pd | smoltcp VirtIO-net | 180 | No |
| service-content PD | service-content | 150 | No |
| service-people PD | service-people | 130 | No |
| service-slm PD | slm-doorman-server | 120 | No |
| service-extraction PD | service-extraction | 110 | No |

Seven is the minimal viable secure stack. Fewer PDs would collapse the isolation boundaries the design depends on: if service-slm and service-fs ran in the same PD, the formal confinement proof would not hold, because the combined PD would hold both the inference surface and the block device capability. More PDs would introduce IPC overhead without adding isolation beyond what the seven-way split already provides.

The architecture does not use a general-purpose microservice mesh. Each PD has a specific role, a specific capability set, and a specific reason to exist at its assigned priority level.

## Startup sequence — why this order

The startup sequence enforces a strict dependency chain. watchdog-pd starts first because it must be able to preempt any other PD at any time; if it started after the services it monitors, there would be a window during which a failing service could go undetected. service-fs PD starts second because it holds the block device capability — no Ring 2 service may begin until the WORM ledger enforcer is healthy. Any attempt by a Ring 2 service to write to durable storage before service-fs PD is ready would be refused at the IPC boundary, not merely rejected by a configuration check.

After service-fs PD reaches a healthy state, network-pd starts. It holds the VirtIO-net device cap and routes all HTTP traffic for Ring 2 services. Ring 2 services cannot expose an HTTP surface until network-pd is up, so the ordering is again structural, not advisory.

The four Ring 2 services — service-content, service-people, service-slm, and service-extraction — start in descending priority order. service-content (DataGraph, :9081) starts before service-people because service-people relies on the DataGraph for entity resolution. service-slm (Doorman, :9080) starts after service-content because Doorman uses the DataGraph to route inference requests. service-extraction (the CORPUS pipeline) starts last because it is a background process that feeds the DataGraph over time; it has no latency-critical upstream dependency waiting on it.

The `os-totebox/scripts/start-stack.sh` shell script implements this ordering for the development path (std/Linux, Phase H0 compat bottom). On the seL4 native path, the PD scheduler enforces the same ordering at the capability level — a PD cannot receive a start notification from moonshot-sel4-vmm until its declared dependencies have sent a ready signal.

## Capability confinement — what the seL4 proof covers

The critical security property of the design is geometric: a compromised service-slm PD cannot reach service-fs PD, regardless of what code runs inside service-slm. This is not a runtime policy assertion. The seL4 kernel enforces capability type-safety on every invocation, and the Isabelle/HOL proofs in vendor-sel4-kernel (BSD-2-Clause, seL4 Foundation, covering AArch64 and RISC-V 64 as of Microkit 2.2.0, March 2026) formally verify that no invocation path bypasses this enforcement.

The derivation path matters. service-slm PD holds no capability whose derivation chain leads to the block device endpoint. network-pd routes HTTP for service-slm but holds no block device cap itself. service-extraction holds a write capability scoped to service-fs PD's drop directory channel — it cannot address the block device directly. The only entity in the system that holds a block device cap is service-fs PD, and that cap is granted in `os-totebox.toml` and verified by moonshot-toolkit before the image is assembled.

One limitation applies: the seL4 proof covers invocation-path confinement but does not cover side-channel attacks through shared physical DRAM or shared cache lines. A deployment on hardware with separate physical DMA zones per PD would eliminate that residual risk. That hardware configuration is a planned Phase H2 target; it is not part of the Phase H1 QEMU development boot milestone.

## The two-bottom development path

Because seL4 Microkit 2.2.0 targets AArch64 and RISC-V 64 only, the x86_64 development environment uses a parallel arrangement. Phase H0 (complete) provides a pre-built NetBSD QCOW2 reference image running the same services under a conventional OS. Phase H1 (planned) delivers the seL4 PD runtime on QEMU AArch64 (cortex-a53, VirtIO block and net). The two paths are not merged: the NetBSD compat bottom is a transitional artefact, and the seL4 native bottom is the production target.

The AArch64 hardware decision for Phase H2 bare-metal deployment — GCP AArch64 instance or Firecracker x86_64 with KVM on local hardware — remains an open decision requiring direction from the system administrator. That decision gates the Phase H2 milestone but not the Phase H1 QEMU dev boot.

## Relationship to the three-binary architecture

os-totebox is one surface in a three-binary deployment:

- **os-console** is the operator terminal surface (TUI, app-console-* cartridges). It relays inference requests to Doorman but cannot bypass os-totebox's capability boundaries.
- **os-totebox** is the data persistence tier. It is the only surface that holds WORM block device capabilities and signs ledger checkpoints.
- **os-orchestration** is the stateless aggregation layer. It coordinates Tier B GPU inference across the Yo-Yo broker (:9180) but never touches the WORM ledger directly.

Inference on os-totebox is Tier A only — local OLMo 7B via Doorman (:9080). Tier B (GPU broker) and Tier C (external API) are routed through os-orchestration's app-orchestration-slm crate. This boundary is enforced by the PD capability graph: service-slm PD on os-totebox holds an IPC cap to the local OLMo engine only. It holds no capability that reaches an external network endpoint.

The WORM ledger is the authoritative audit record for the system. Every write that passes through service-fs PD is append-only and checksummed. No PD can modify an existing ledger entry; the seL4 capability model makes that structurally impossible.

---

*All Phase H1 and later language in this article describes planned or intended functionality. The Phase H0 NetBSD reference image is the only deployed artefact at the time of writing (2026-06-19).*
