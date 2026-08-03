---
title: "Capability-based security"
slug: capability-based-security
category: security
type: topic
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: forward-looking
language_protocol: PROSE-TOPIC
last_edited: 2026-08-03
editor: pointsav-engineering
short_description: "Capability-based security grants each component an unforgeable, scoped token it must present to act, replacing ambient privilege. One software layer implements it today; kernel-level enforcement is planned."
paired_with: capability-based-security.es.md
---

**Capability-based security** is an access-control model in which a component may perform an
operation only by presenting an unforgeable token that names both the operation and its scope.
There is no ambient privilege: holding a capability *is* the permission, and a component that
holds none can do nothing, regardless of which user account it runs under or which machine it
sits on. The model dates to Lampson's 1974 protection matrix and reached its best-known modern
expression in the seL4 microkernel, where every kernel object — memory frames, threads,
communication endpoints — is reachable only through an explicit capability held in a per-process
table.

The distinction from the access-control lists most systems use is structural rather than
cosmetic. Under an access-control list, the subject's *identity* is checked against a policy at
the moment of use, and a compromised process inherits everything that identity is permitted to
do. Under a capability model, the subject's *possession* is what matters, and a compromised
process can reach only the specific objects whose capabilities it was handed. Privilege is
therefore bounded at the moment of delegation rather than at the moment of use.

## What is enforced today

One capability mechanism is implemented, tested, and running in platform code: the request gate
in `service-content`. It is a software layer, not a hardware or kernel one, and its scope is
cross-instance authorisation rather than process isolation.

The gate reads an `X-Foundry-Capability` header, resolves the calling peer's registered public
key, verifies an Ed25519 signature over a base64url-encoded payload, checks the payload's nonce
against a replay cache, and confirms that the archive scope named in the capability permits the
request being made. Expired tokens, scope mismatches, replayed nonces, and unregistered peers are
each rejected with distinct status codes, and the outcomes are appended to an interface audit
log. Ten integration tests exercise the gate directly — covering the pass-through case, exact and
wildcard scope matching, scope mismatches, unregistered peers, expired tokens, and nonce replay —
each asserting the specific status code the gate returns.

Two properties of this gate matter for an accurate reading. First, the capability is *signed*,
not merely presented — a token cannot be minted by anyone but the holder of a registered private
key. Second, and more importantly, a request arriving with **no** capability header passes
through unchanged, by design, to preserve the existing locally-trusted call path. The gate is
therefore a real, tested instance of capability-based access control — an unforgeable signed
token stands in for identity — but it is additive and optional rather than a mandatory
chokepoint through which all traffic must pass.

A second, adjacent enforcement layer exists in `service-vm-tenant`, which extracts a bearer
token, applies per-tenant quota checks, and serialises virtual-machine creation behind a lock
explicitly documented as a guard against time-of-check/time-of-use races. This is conventional
token authorisation rather than a capability model proper — the token names a tenant, not an
object and an operation — but it is the other place in the platform where authority is checked
against a presented credential rather than assumed from context.

## The intended architecture

The design most of this platform's security writing describes is broader than the gate above: a
capability layer sitting on a [[sel4-microkernel-substrate|microkernel foundation]], with every
driver, network interface, and platform service running as an isolated component holding no
general administrative rights. To communicate with another component, a process would invoke a
capability, which the kernel — not an application-level middleware — validates before permitting
the operation.

Above the kernel, the design envisions a capability-management layer: at deployment time, a
policy declaration would state which components may communicate with which others and what
operations each is permitted, and the resulting capability grants would be distributed at system
start. The plan applies this model across the intended deployment stack — the secure archive
operating system holding data at rest, the edge delivery environment serving public content, and
the [[worm-ledger-architecture|append-only ledger]] whose write path would be reachable only by
components holding an explicit append grant.

None of this deployment-time policy layer exists in running code today. Verified by searching the
entire canonical source tree rather than any single component: there is no capability-manager, no
isolation wrapper, and no hypervisor-bridge component anywhere. The `moonshot-hypervisor` package
that would house a mediation layer is a four-file placeholder whose dependency list is empty and
whose only function returns a scaffold-verification string.

Genuine seL4 work does exist, but it is bare-metal experimentation rather than a platform runtime.
The seL4 kernel source is vendored into the platform's source tree, and a standalone development
workspace, `moonshot-sel4-vmm`, contains early protection-domain runtime code with a series of
test binaries exercising console output, inter-process communication, serial and UART handling,
and VirtIO networking under emulation. No shipped PointSav component runs on seL4 today; the
platform's live services, including the fleet, host, and tenant services of the private compute
network, are ordinary Rust processes built on `axum` and `tokio`, with no seL4 dependency in any
of their manifests. This work is described further in [[sel4-capability-topology]] and
[[sel4-microkernel-substrate]].

The seL4 project's own published material quantifies why this foundation is attractive as a
target. A well-designed microkernel is on the order of ten thousand lines of code, against
roughly twenty million in a mainstream monolithic kernel — a trusted computing base three orders
of magnitude smaller. The project's analysis of critical Linux kernel compromises found that a
microkernel design would have fully eliminated about 29 percent of them and mitigated a further 55
percent below critical severity. Those figures describe the seL4 architecture in general, as
published by the seL4 project, not any PointSav deployment; they are recorded here as the
rationale for the platform's choice of intended foundation, not as a claim about work already
done.

## Why the two layers are not interchangeable

It is tempting to treat the software capability gate as an early increment of the planned kernel
model. They defend different things, and one does not grow into the other.

### Different threat boundaries

The software gate assumes a correct operating system, a correct language runtime, and a correct
process boundary; it protects one service's data from another organisation's caller. Kernel
capability enforcement assumes far less — it is intended to hold even when a service is fully
compromised, because the kernel, not the service, is what refuses the unauthorised operation.

### Different failure modes

A defect in the software gate is a bypassed authorisation check on one service's HTTP surface. A
defect in a kernel capability distribution is a breached isolation boundary between every domain
on the machine. This asymmetry is why seL4's formal proofs are addressed at the kernel and not at
applications above it.

### Different verification stories

The software gate's assurance is integration tests. The planned model's assurance would rest on
seL4's own machine-checked proofs — established in the Isabelle/HOL proof assistant, showing that
its implementation matches its specification and that a correctly configured system enforces
confidentiality, integrity, and availability — plus the integrity and confidentiality results
published for specific architectures. Those are third-party results about the kernel itself, and
they hold whether or not this platform ever adopts it.

## What this is not

**This is not a description of a running, mandatory capability system.** With the single
exception of the tested request gate described above, capability-based access control on this
platform is intended architecture. Statements about hardware-rooted capabilities, per-service
protection domains, and policy-driven capability distribution describe what is planned, not what
is deployed.

**seL4 is not running anywhere in the platform today.** The only capability enforcement that
exists inside seL4 itself is a formally verified property of that kernel — real, but not yet
placed into production by this platform.

**The software capability gate is not a mandatory chokepoint.** A request with no capability
header is not rejected. Any characterisation of the platform as one where "every request carries
a capability" would be inaccurate today.

**Formal verification of seL4 is not formal verification of this platform.** The Isabelle/HOL
proofs are properties of the microkernel as an artefact in its own right. They say nothing about
the correctness of software built above it, and this platform has published no formal proof of
its own.

**Capabilities are not a substitute for the other controls described in this category.** Even
under the planned model, commit-time secret scanning, ledger immutability, and pairing-based
device authorisation each address a class of risk that object capabilities do not touch. Nor does
this article claim that capability hardware or exotic processors are required — the intended
design uses a software capability model enforced by a microkernel on commodity hardware.

## See also

- [[sel4-capability-topology]]
- [[sel4-microkernel-substrate]]
- [[machine-based-auth]]
- [[cryptographic-ledgers]]
- [[worm-ledger-architecture]]
- [[pre-commit-defense-in-depth]]
