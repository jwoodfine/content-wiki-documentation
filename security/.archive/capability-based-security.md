---
schema: foundry-doc-v1
title: "Capability-based security"
slug: capability-based-security
category: security
type: topic
content_type: topic
quality: complete
short_description: "Capability-based security is the access-control model PointSav uses at the hardware and OS layers, where each component must hold a verified cryptographic token."
status: archived
archived: 2026-08-03
archived_reason: "superseded by fresh-draft-first authoring pilot against new content-schema tokens (schema-topic.yaml)"
superseded_by: capability-based-security
bcsc_class: forward-looking
last_edited: 2026-07-30
editor: pointsav-engineering
cites: []
references:
  - id: 1
    text: "Klein, G. et al. 'seL4: Formal Verification of an OS Kernel.' ACM SOSP, 2009."
    url: "https://dl.acm.org/doi/10.1145/1629575.1629596"
  - id: 2
    text: "Lampson, B. W. 'Protection.' ACM SIGOPS Operating Systems Review, 8(1):18–24, 1974."
    url: "https://dl.acm.org/doi/10.1145/775265.775268"
paired_with: capability-based-security.es.md
---

**Correction — rehedged to planned/intended (2026-07-30):** this article originally
described a live, enforced capability system in unhedged present tense. No matching
code exists today: neither a single-archive check nor a subsequent broader
cross-archive sweep (grep for "capability manager"/`CapabilityManager` across every
`.rs` file in all ~25 Totebox archives) found any implementation; `moonshot-hypervisor`
— the crate that would house a hypervisor-mediation layer — is a 4-file scaffold with
an empty dependency list. This is consistent with the separately-confirmed finding that
seL4 itself is not yet running anywhere in the platform today. Per operator direction,
this describes real, intended design rather than a fabrication — the body below is
rewritten to present it as planned/intended architecture, not current state.

> Capability-based security is the access-control model PointSav is designed to use at the hardware and operating-system layers, where each software component will be required to hold a mathematically verified cryptographic token to communicate with any other component. This is a planned architecture, not yet implemented.

**Capability-based security** is the access-control model intended to replace traditional operating-system privilege hierarchies in the [[pointsav-overview|PointSav]] platform, once implemented. Where conventional operating systems (Windows, macOS, Linux) grant broad permissions through administrative accounts and assume components at the same privilege level can be trusted, the design calls for each isolated component to hold an explicit, mathematically verified [[crypto-attestation|cryptographic token]] — called a capability — before it can communicate with any other component. A capability would be unforgeable and uncopyable, granted by the kernel at process start and revoked when withdrawn. [^2] The intended effect is that the blast radius of any compromise is mathematically bounded to the components the compromised process held capabilities for. See also [[capability-ledger-substrate|the capability ledger substrate]] and [[pairing-as-permission|pairing as permission]].

## Overview

Standard operating systems are vulnerable to privilege escalation: a single compromised application can, in many architectures, reach the core memory of the host machine and gain access to other components on the network. The capability model is designed to eliminate this class of vulnerability at the architecture level rather than through policy controls.

The [[pointsav-overview|PointSav]] implementation is planned to build on a [[sel4-microkernel-substrate|microkernel foundation]]. In the intended design, the microkernel would handle only the most primitive routing of physical memory and CPU time, with every driver, network interface, and service process running in isolated memory and none holding general administrative rights. To communicate with another isolated component, a process would present a cryptographic capability token, which the kernel would validate before permitting or denying the operation. **As of this writing, no such implementation exists** — no capability-manager code, isolation-wrapper, or hypervisor-bridge crate was found anywhere in the monorepo, and seL4 itself is not yet running in any shipped component.

## Architecture (planned)

The intended capability layer would sit between the [[sel4-microkernel-substrate|seL4 microkernel]] and the Rust service processes that make up the PointSav [[three-ring-architecture|Ring 1 and Ring 2]] services, with Rust-based capability managers engineering the isolation wrappers and hypervisor bridges that mediate communication between components.

The design calls for a strict, one-way command flow between isolation domains: an isolated edge delivery process — for example, the [[mediakit-os|MediaKit OS]] — would be unable to issue commands back into the secure [[totebox-os|ToteboxOS]] vault, so a compromised edge process would be contained within its own memory sandbox with no capability grants reaching the broader system, enforced by the kernel rather than a policy document.

## Intended properties

- **Formal verification.** The [[sel4-microkernel-substrate|seL4 microkernel]] that would underlie the capability manager is formally verified in Isabelle/HOL [^1] as a kernel in its own right — meaning the isolation properties *of seL4 itself* are mathematically proven, independent of whether PointSav's own capability-manager layer has been built on top of it.
- **Least privilege by default.** Intended: components start with no capabilities; the system grants only the minimum set required for their declared function.
- **Blast-radius containment.** Intended: compromise of one component could not propagate to components it holds no capability grants for.
- **Auditability.** Intended: capability grants would be recorded, with the set of grants in force at any time inspectable.

## How it is intended to work

At deployment time, a PointSav capability manager would read a system policy file declaring which processes communicate with which others and what operations each is permitted. The [[sel4-microkernel-substrate|microkernel]] would enforce this policy at runtime. No such capability manager or policy-file mechanism exists today.

## Intended applications

Once built, the capability model is intended to apply across the full [[pointsav-overview|PointSav]] deployment stack:

- **[[totebox-os|ToteboxOS]]** — the primary secure vault OS; data at rest would be accessible only to processes holding the appropriate capability token.
- **[[mediakit-os|MediaKit OS]]** — the edge delivery environment; intended to hold no capability grants reaching ToteboxOS, so a compromised delivery node could not reach stored data.
- **[[service-fs-architecture|service-fs]]** — the [[worm-ledger-architecture|WORM ledger]]; append capability would be granted to [[three-ring-architecture|Ring 1]] ingest services only.

## See also

- [[sel4-microkernel-substrate]]
- [[worm-ledger-architecture]]
- [[3-layer-stack]]
- [[machine-based-auth]]
- [[compounding-substrate]]

