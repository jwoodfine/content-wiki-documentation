---
schema: foundry-doc-v1
title: "Capability-Based Security"
slug: topic-capability-based-security
category: architecture
type: topic
quality: core
short_description: "Capability-based security is the access-control model PointSav uses at the hardware and operating-system layers, where each software component must hold a mathematically verified cryptographic token to communicate with any other component."
status: pre-build
last_edited: 2026-04-30
editor: pointsav-engineering
cites: []
paired_with: topic-capability-based-security.es.md
---

# Capability-Based Security

> Capability-based security is the access-control model PointSav uses at the hardware and operating-system layers, where each software component must hold a mathematically verified cryptographic token to communicate with any other component.

**Capability-based security** is the access-control model that replaces traditional operating-system privilege hierarchies in the PointSav platform. Where conventional operating systems (Windows, macOS, Linux) grant broad permissions through administrative accounts and assume components at the same privilege level can be trusted, capability-based security requires each isolated component to hold an explicit, mathematically verified cryptographic token — called a capability — before it can communicate with any other component. A capability cannot be forged or copied; it is granted by the kernel at process start and revoked when the capability is withdrawn. This makes the blast radius of any compromise mathematically bounded to the components the compromised process held capabilities for.

## Overview

Standard operating systems are vulnerable to privilege escalation: a single compromised application can, in many architectures, reach the core memory of the host machine and gain access to other components on the network. The capability model eliminates this class of vulnerability at the architecture level rather than through policy controls.

The PointSav implementation builds on a microkernel foundation. The microkernel handles only the most primitive routing of physical memory and CPU time. Every driver, network interface, and service process runs in isolated memory, and none holds general administrative rights. To communicate with another isolated component, a process presents a cryptographic capability token. The kernel validates the token and either permits or denies the operation.

## Architecture

The capability layer sits between the seL4 microkernel and the Rust service processes that make up the PointSav Ring 1 and Ring 2 services. The Rust-based capability managers engineer the isolation wrappers and hypervisor bridges that mediate communication between components.

The platform enforces a strict, one-way command flow between isolation domains. An isolated edge delivery process — for example, the MediaKit OS — cannot issue commands back into the secure ToteboxOS vault. If the edge process is compromised, the attacker is contained within the memory sandbox of that process with no capability grants reaching the broader system. The boundary is enforced by the kernel, not by a policy document.

## Properties

- **Formal verification.** The seL4 microkernel underlying the capability manager is formally verified in Isabelle/HOL, which means the isolation properties are mathematically proven for the verified configuration — not asserted.
- **Least privilege by default.** Components start with no capabilities; the system grants the minimum set required for their declared function. Unused capabilities are never held.
- **Blast-radius containment.** Compromise of one component cannot propagate to components it holds no capability grants for. The scope of a breach is bounded at grant time.
- **Auditability.** Capability grants are recorded; the set of grants in force at any time is inspectable. There is no hidden administrative path.

## How It Works

At deployment time, the PointSav capability manager reads a system policy file that declares which processes communicate with which others and what operations each is permitted. The microkernel enforces this policy at runtime: when process A attempts to send a message to process B, the kernel checks A's capability set and either delivers the message or returns a denial. The capability set cannot be modified by the processes themselves — only the capability manager, running with kernel authority, can issue or revoke grants.

## Applications

The capability model applies across the full PointSav deployment stack:

- **ToteboxOS** — the primary secure vault OS; all data at rest is accessible only to processes holding the appropriate capability token.
- **MediaKit OS** — the edge delivery environment; deliberately holds no capability grants reaching ToteboxOS, so a compromised delivery node cannot reach stored data.
- **service-fs** — the WORM ledger; append capability is granted to Ring 1 ingest services; no read-modify-write capability exists at the API surface.

## See Also

- [[sel4-foundation]]
- [[worm-ledger-architecture]]
- [[3-layer-stack]]
- [[machine-based-auth]]
- [[compounding-substrate]]

## References

- `conventions/system-substrate-doctrine.md` — capability ledger substrate specification
- `DOCTRINE.md §XIV` — Compounding Substrate and the seL4 foundation context
- `conventions/three-ring-architecture.md` — Ring 1 / Ring 2 service isolation model
- `IT_SUPPORT_Nomenclature_Matrix_V8.md` — canonical OS names (ToteboxOS, MediaKit OS)
