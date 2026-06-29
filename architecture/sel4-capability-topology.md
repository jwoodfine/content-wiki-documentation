---
schema: foundry-doc-v1
title: "seL4 Capability Topology"
slug: sel4-capability-topology
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
paired_with: sel4-capability-topology.es.md
short_description: "In an seL4 system, security is determined by the shape of the capability graph — the topology. If component A has no capability path to component B, A cannot reach B by any means, a property proved by machine-checked formal verification."
cites: []
references:
  - id: 1
    text: "Shapiro, J. S. and Miller, M. S. 'EROS: A Capability System.' USENIX Annual Technical Conference, 1999."
  - id: 2
    text: "Murray, T. et al. 'seL4: From General Purpose to a Proof of Information Flow Enforcement.' IEEE Symposium on Security and Privacy, 2013."
  - id: 3
    text: "Drossopoulou, S. et al. 'Holistic Specifications for Robust Programs.' ECOOP, 2016."
---

In the seL4 microkernel, every object access is mediated by a **capability** — an unforgeable token that grants a specific right to a specific object. A process that does not hold a capability to an object cannot observe it, modify it, or call it. There is no ambient authority. There is no root privilege at the kernel level.

Capabilities are stored in **CSpaces** — per-process capability space tables managed by the seL4 kernel. The CSpace is a bounded directed graph: capability pointers are edges; kernel objects (threads, memory regions, IPC endpoints, notification objects) are nodes.

## The topology invariant

The collection of all CSpaces in a running seL4 system forms a directed graph called the **capability topology**. The seL4 kernel enforces one invariant above all others:

> *Only connectivity begets connectivity.*
> — Shapiro and Miller, 1999 [^1]

In formal terms: if component A has no capability to reach component B — directly or transitively through any chain of intermediate capabilities — then A cannot obtain information from B, cannot modify B's state, and cannot cause B to take any action.

This invariant is machine-checked. The seL4 Foundation has published formal proofs in the Isabelle/HOL proof assistant covering:

1. **Functional correctness** (C-level, all architectures): the kernel implementation matches its abstract specification.
2. **Integrity** (AArch64 EL2, April 2025): no process can modify kernel objects or another process's capabilities without holding a grant right to the relevant capability.
3. **Confidentiality** (RISC-V64, published; AArch64 in progress): no process can read another process's data without holding a read right. [^2]

## What "topology determines security" means

Security in an seL4 system is not determined by policies, ACLs, or software checks. It is determined by the shape of the capability graph — the topology.

An architect who draws the capability topology of a system has drawn its security boundary. Two components that share no path in the capability graph have no information channel, regardless of what software runs inside them. A compromised component cannot escape its partition because escape would require obtaining a capability it does not hold — and the kernel proves that capability creation is monotone: a process cannot create a capability it does not already possess.

## Architecture coverage by seL4 target

| Architecture | Formal security claim | Notes |
|---|---|---|
| AArch64 EL2 | Functional correctness + integrity | Integrity proof published April 2025 |
| RISC-V64 | Functional correctness + integrity + confidentiality | Deepest proofs; HiFive Unleashed hardware |
| x86-64 | Functional correctness only | No integrity or confidentiality proof |

The formal claim that "topology determines security" applies to AArch64 EL2 and RISC-V64 deployments. x86-64 deployments carry only functional correctness proofs; the topology security claim does not extend to that architecture.

## Prior art — Fuchsia component topology

Google's Fuchsia OS uses the same capability model and the same vocabulary. Fuchsia's documentation refers to the "component topology" to describe the tree of component capability relationships that determines what system calls and interfaces are reachable. The same terminology appears in formal treatments of capability safety using directed-graph structures [^3], tracing to early capability OS literature [^1].

## PPN application

The PointSav Private Network is planned/intended to use seL4 as the hypervisor layer on AArch64 nodes. In that configuration, the seL4 capability topology governs what components can communicate across the mesh. The WireGuard mesh interface, the pairing ceremony server, and the fleet management service each occupy distinct seL4 protection domains with explicitly granted capability channels. A component without a capability to the WireGuard protection domain cannot modify peer tables — regardless of whether it is compromised.

This is the formal basis for the PPN security model at the hypervisor layer.

## See also

- [[ppn-three-path-architecture]] — the three sequential seL4 architecture options for PPN infrastructure nodes
- [[sel4-microkernel-substrate]] — the seL4 microkernel as infrastructure substrate
- [[capability-based-security]] — the broader capability security model applied in the PointSav stack
- [[ppn-architecture-overview]] — how seL4 fits into the four-layer PPN stack
