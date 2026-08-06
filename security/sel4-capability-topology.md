---
schema: foundry-doc-v1
title: "seL4 capability topology"
slug: sel4-capability-topology
category: security
index_group: isolation-boundaries
type: topic
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: forward-looking
language_protocol: PROSE-TOPIC
last_edited: 2026-08-03
editor: pointsav-engineering
short_description: "In an seL4 system the security policy is the shape of the capability graph established at boot, not a runtime policy layer. First-party work is nine bare-metal test binaries; no platform service runs on seL4."
paired_with: sel4-capability-topology.es.md
---

**A capability topology** is the arrangement of which components hold references to which kernel
objects — the graph of who can reach what. In a system built on the seL4 microkernel this graph
*is* the security policy. There is no separate policy engine consulted at runtime, no configuration
file describing permitted operations, and no identity checked against a rule set: a component can
invoke a kernel object if and only if it holds a capability naming that object in its capability
space, and the kernel's only question at each system call is whether the presented capability
exists and permits the requested operation. Draw the graph of which components hold capabilities to
which objects, and you have drawn — exactly, not approximately — what each component can ever
reach.

The practical consequence is that security review of an seL4 system is topology review. There is no
runtime enforcement layer to inspect for defects, because enforcement is a property of the graph
laid down when the system starts. If the graph is right, the isolation holds; if a domain was
handed a capability it should not have, no later check will catch it, because there is no later
check.

## The topology invariant

The kernel enforces one invariant above all others, the classical capability-systems rule that
*only connectivity begets connectivity*: a component can gain a new capability only by having it
transferred through a channel it already holds a capability to. Authority is never conjured; it
only flows along existing edges. If component A has no path to component B — directly or
transitively through any chain of intermediaries — then A cannot obtain information from B, cannot
modify B's state, and cannot cause B to act.

Two consequences follow. An architect who draws a system's capability topology has *specified* its
security policy — two components sharing no path have no channel, regardless of what code runs
inside them, and a compromised component cannot escape its partition because escape would require
an edge it does not have. And the model dissolves the confused-deputy problem that
access-control-list systems suffer: since the caller must pass along the specific capability
authorising each operation, a privileged intermediary cannot substitute its own broader authority
for its caller's narrower grant. This is fundamentally different from the coarse privilege flags
mainstream kernels also call "capabilities," which are ACL-style and retain the confused-deputy
weakness.

## How the topology comes into being

seL4 starts a single initial task and hands it capabilities to essentially everything — untyped
memory covering physical RAM, the interrupt controller, the input/output ports, and the root
capability space. Nothing else has any authority at all. That initial task then performs the
distribution: it retypes untyped memory into the specific kernel objects each domain needs — thread
control blocks, page tables, endpoints for communication — and grants each domain exactly the
capabilities its function requires, keeping none for itself that it does not need. Once
distribution is complete the initial task can revoke its own remaining authority.

Authority is therefore monotonically non-increasing during normal operation — a domain cannot
manufacture a capability it was not given — and delegation is explicit and traceable: every
reference one domain holds to another's resources was passed along a path that can be enumerated
from the boot description. Because domains share no memory by default, communication happens
through endpoint objects, and an endpoint capability is itself the permission to communicate — a
domain holding none toward another has no channel to it at all, not a blocked one. Restricting who
may talk to whom requires no firewall rule; it is expressed by never granting the capability.

In seL4's recommended component framework, the Microkit, a system's architecture is static:
protection domains, their communication channels, and their shared memory regions are declared in a
system description at build time, and the framework's toolchain maps that description onto kernel
objects and generates startup code that provably brings the booted system into the described state
— with the seL4 project itself noting that portions of the framework-level proofs are still being
completed.

## What the formal verification proves

seL4's distinguishing claim is that enforcement of this model is machine-checked, not asserted.
These are third-party results about the kernel as an artefact, published by the seL4 project and
cited here as its own claims rather than independently re-verified for this article; they establish,
in sequence:

- **Functional correctness** — the C implementation is a refinement of the kernel's abstract
  mathematical specification: the code can do nothing the specification does not allow, ruling out
  standard implementation-level attacks (memory-safety violations, code injection, control-flow
  hijacking) as behaviours the kernel can exhibit.
- **Translation validation** — the compiled binary is proven, by an automated toolchain, to
  correctly implement the verified C, removing the compiler from the trusted base.
- **Security enforcement** — proofs connecting the abstract specification to the classical
  confidentiality, integrity, and availability properties: in a correctly configured system, the
  kernel will not allow an entity to read data without read access or modify data without write
  access.

The proofs rest on stated assumptions — hardware behaves as specified, the specification captures
the intended properties, the proof checker's small core is sound, and the initial capability
distribution is itself correct — and carry an acknowledged boundary: they do not yet cover timing
behaviour, so covert timing channels are outside the current guarantees. Completeness also varies
by architecture; the seL4 project's own status pages, not this article, are the authoritative
record of which property is proven where. The scale is part of the credibility: the original
functional-correctness proof ran to roughly two hundred thousand lines of machine-checked proof
script, since grown past a million, checked against a trusted core of only a few tens of thousands
of lines. These remain properties of the microkernel as an artefact and do not transfer upward: a
proof about the kernel says nothing about software running above it, and this platform has
published no formal proof of its own.

## The state of first-party work

Real, working seL4 code exists in this platform's source tree, and it is bare-metal experimentation
rather than a service runtime. The `moonshot-sel4-vmm` package is a first-party Rust component
compiled `no_std` and `no_main` for an AArch64 bare-metal target, containing nine standalone
binaries, each corresponding to a numbered milestone and gated on a literal success string printed
to a serial log under emulation. They cover: a console banner through the kernel's debug output
call; two threads exchanging a message over an endpoint; a serial and a console protection domain
communicating by message passing; a direct memory-mapped write to a PL011 serial controller; a
status panel rendered through the serial domain; and a four-step sequence bringing up a
paravirtualised network device — probing and initialising it, driving its descriptor rings to
ready, transmitting raw Ethernet, ARP, and echo-request frames by direct memory access, and
finally completing a raw TCP request to a health endpoint on the host.

That last milestone is a genuine result: a `no_std` Rust program running on seL4 under emulation,
driving a virtual network device with no operating system beneath it, and completing an HTTP
exchange. It is also nine demonstration binaries, not a hypervisor and not a platform runtime. The
kernel itself, its build tooling, and a small project scaffold are present as vendored third-party
source under separate directories, carrying their upstream licence, with some build output checked
in alongside them.

## What runs the platform instead

The services that carry live traffic in the private compute network are conventional Rust services.
Reading their dependency manifests directly, the fleet controller, the per-node host agent, and the
tenant-facing proxy each depend on `axum`, `tokio`, `reqwest`, `serde`, `chrono`, and tracing
crates, plus a shared wire-types package. **None of the three carries any seL4 dependency.** They
are ordinary HTTP services listening on ordinary ports.

This matters because it contradicts a description that appeared in earlier writing about this
platform: that the mesh network interface, the pairing ceremony server, and the fleet management
service each occupy distinct seL4 protection domains. As a present-tense statement that is false.
Those three functions exist and are separated from one another, but they are separated as processes
and services on a general-purpose operating system, not as capability-isolated domains under a
verified microkernel. The component that would host a hypervisor mediation layer,
`moonshot-hypervisor`, is a four-file placeholder with an empty dependency list.

The platform's interest in seL4 is straightforward: a fleet built on kernel-enforced capability
topology would make the [[diode-standard|Diode Standard]]'s one-way rules and the
[[capability-based-security|capability model]]'s least-privilege defaults kernel properties rather
than application discipline. That remains the reason for the investment described above, not a
claim that it has already arrived.

## What this is not

**No platform service runs on seL4 today.** The fleet, host, and tenant services are plain Rust and
`axum` services with no seL4 dependency in any manifest. Any statement that platform services
occupy distinct seL4 protection domains describes intended architecture only.

**The first-party seL4 work is not a hypervisor.** It is nine emulator-gated demonstration binaries
establishing that basic kernel primitives — debug output, threads, endpoints, memory-mapped device
access, and direct memory access to a virtual network card — can be driven from `no_std` Rust. No
guest operating system is hosted, and no production workload runs on it.

**A capability topology is not an access-control list.** It is not consulted, evaluated, or checked
against an identity at runtime. Reviewing it means reviewing the boot-time distribution, because a
mistake there is not caught later.

**Formal verification of seL4 is not verification of this platform.** The proofs are properties of
the kernel under stated assumptions, most importantly that the initial capability distribution is
itself correct — which is precisely the part any adopting system must get right on its own. It is
also not a universal constant across hardware: the formal properties are per-architecture, at
varying completeness, and a deployment inherits only what is proven for its processor family.

**Correct topology is not confidentiality against every channel.** The published confidentiality
results address specified information flows under specified assumptions; timing and other physical
side channels are outside what a functional-correctness proof addresses, by the seL4 project's own
statement, and physical attacks and hardware defects sit outside any kernel's guarantees.

**Nor is it a claim that software inside a protection domain is correct.** A component can be as
buggy as any other program; the proof is that its reach is bounded by its capability holdings, not
that it behaves well within them.

## See also

- [[sel4-microkernel-substrate]] — the kernel itself and why it was selected
- [[sel4-aarch64-qemu-substrate-target]] — the emulated target the demonstration binaries run against
- [[sel4-unikernel-substrate]] — the single-address-space direction under consideration
- [[capability-based-security]] — the access-control model in its general form
- [[diode-standard]]
- [[ppn-tenant-vm-isolation]] — the isolation boundary carrying commercial load today
- [[os-totebox-service-pd-model]] — the protection-domain arrangement planned for the archive operating system
