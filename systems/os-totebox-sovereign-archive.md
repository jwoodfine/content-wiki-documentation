---
schema: foundry-doc-v1
type: topic
content_type: topic
slug: os-totebox-sovereign-archive
title: "os-totebox: the sovereign WORM data vault"
short_description: "os-totebox is designed to become a Type I bare-metal OS built on a formally verified seL4 microkernel, with a WORM data vault enforced by a compiled capability graph — the intended end state, not the software running today."
audience: vendor-public
bcsc_class: forward-looking
language: en
language_protocol: PROSE-TOPIC
index_group: the-archive-layer
paired_with: os-totebox-sovereign-archive.es.md
category: systems
status: active
quality: complete
last_edited: 2026-08-24
---

**Status (2026-08-06):** the seL4 Microkit image described in this article has moved
from planned to live-verified. A real boot of the image is confirmed, with end-to-end
inference round-trips confirmed working — the capability-graph and Protection-Domain
design below is real, current engineering, not merely intended work or a paper design.
This is a verified boot milestone on the seL4 path specifically; it is not yet a
description of os-totebox's general deployment, which remains the conventional
Rust/tokio process (`service-content` + `service-slm`/Doorman run as one deployable
process) described in the platform's engineering registry. `bcsc_class` stays
`forward-looking`: the full production stack, capability-graph enforcement at scale, and
the persistence guarantees this article argues for are not yet real — see Known
limitations, below, before treating this as a deployed, persistent sovereign vault. Read
every other present-tense architectural claim in this article as the target design,
confirmed today only at the boot-and-inference layer described here.

## Known limitations (2026-08-06)

These same limitations — storage not yet persistent, graceful shutdown broken, nothing
anchoring or signing the ledger yet — are load-bearing for anyone evaluating the design
today. Rather than restate them here, see [[totebox-os]]'s own **"A known limitation —
data persistence inside the seL4 guest"** section for the canonical, single-sourced
version of this fact.

Every organisation that relies on a third-party platform to store its records is making an implicit wager: that the platform provider will remain solvent, accessible, and free of security failures for as long as those records matter. [[totebox-os]] is designed for operators who have decided that wager is unacceptable.

## What os-totebox Is Designed To Be

os-totebox's intended end state is a Type I bare-metal operating system — meaning it would run directly on physical hardware with no general-purpose operating system underneath it, with no Linux shell, no package manager, no root process, and no init system. The planned software for that hardware is a seL4 Microkit image: a formally verified [[sel4-microkernel-substrate|microkernel]] with a statically compiled set of services and no runtime modification path.

The defining characteristic of the design is its storage model. os-totebox is designed to operate as a [[worm-ledger-architecture|WORM vault]] — Write Once, Read Many — where records written to the system cannot be altered or deleted through any software pathway. The intent is for this to be a property of the capability graph that governs every service on the machine, not a policy enforced by an access-control list or a permission flag an administrator could override.

## Capability Geometry on Server Hardware (Planned)

seL4 is a microkernel developed and formally verified by CSIRO's Data61. The verification proves, mathematically, that the kernel's access-control model is enforced without exception. The design intent is for os-totebox to extend this property to its inter-service architecture once the seL4 image ships.

The plan is for each service on os-totebox to run inside its own seL4 Protection Domain — an isolated execution environment holding only the capabilities the system design explicitly grants it — with a capability DAG (directed acyclic graph) formally proved to contain no path from a service that processes external input to the service that holds the storage capability.

The concrete failure scenario this is designed to defend against: if [[service-slm]] — the component that handles language model inference, and therefore the component most directly exposed to adversarial inputs — were to be fully compromised in the end-state design, the compromised code would be bounded by its Protection Domain, with no capability to reach service-fs, read the WORM block device, or write to it. The attacker's foothold would be geometrically isolated from the data store. This is the property the platform calls [[capability-geometry|Capability Geometry]] — today it describes the target architecture, not the deployed one.

## The Ring Architecture (Planned)

os-totebox is designed to organise its services into two [[three-ring-architecture|concentric rings]] based on their proximity to storage, once the seL4 image lands.

**Ring 1** is planned to comprise the services that interact directly with durable data and external I/O: [[service-fs|service-fs]], service-input, service-extraction, and service-egress, with service-fs holding the WORM block device capability exclusively — the only Protection Domain on the machine able to perform storage operations, with no other service able to reach the block device directly regardless of execution state.

**Ring 2** is planned to comprise the services that process, classify, and reason about data: service-content, service-people, service-email, and service-slm, communicating with Ring 1 through a defined and bounded inter-domain communication protocol — able to request that service-fs write a record, without holding the capability to do so themselves.

The intent is for this separation to not be an architectural preference future developers could relax: the capability graph would be compiled into the seL4 image at build time, so modifying the capability structure would require rebuilding and re-deploying the image — a step producing a new, auditable artifact rather than a silent runtime change.

## The Sovereign Data Archive

The operating model that os-totebox enables is one where the operator's hardware and the operator's capability graph are the complete system. There is no cloud dependency in the storage path. Ingested records are written to a physical device under the operator's physical control and cannot leave the machine through any software pathway that the capability DAG does not permit.

This has practical implications beyond security. An organisation whose records exist only on its own hardware is not subject to a vendor's data-residency policies, a cloud provider's outage window, or a platform's terms-of-service change. The audit trail is local, the retention schedule is the operator's to set, and the physical device can be decommissioned under the operator's procedures.

For sectors where records carry legal weight — corporate minute books, real property files, financial ledgers, regulated correspondence — the immutability of a WORM vault is not merely a technical feature. It is the evidence that a record existed in a given state at a given time and has not been altered since.

## Operational Surface for Small and Mid-Size Organisations (Design Goal)

Enterprise-grade formal verification and hardware-rooted immutability have historically required dedicated security infrastructure teams to deploy and operate. os-totebox is designed to deliver those properties on commodity hardware with an operational surface that does not assume a specialist security organisation.

In the end-state design, the absence of a shell is treated as a feature, not an inconvenience: a system with no shell has no interactive attack surface, a system with no root process has no privilege escalation path, and a system with no package manager cannot be updated in ways that introduce unaudited code. The intent is for the seL4 image running on the hardware to be the complete and auditable software inventory of the machine — once that image ships.

The design goal is for an organisation deploying os-totebox to rely on a formally proved capability graph rather than an administrator's diligence to enforce data protection policies — the distinction between a policy and a proof. Today's deployed binary (a Rust/tokio process, not yet a seL4 image) does not yet carry this proof; the goal is stated here as the target, not the current guarantee.

## Relationship to the Broader Platform

os-totebox is designed as one of three purpose-specific operating systems in the platform architecture, alongside os-console (the keyboard-native operator interface) and [[os-orchestration]] (which manages the [[totebox-archive|Totebox Archive]] execution environment) — with the intent that, once all three reach their planned bare-metal/seL4 end states, they share no kernel code paths and communicate only through defined network channels. Today, os-console and os-totebox both run as conventional application processes, not bare-metal seL4 images.

The intended deployment pattern is operator-owned hardware with a single physical network interface, with the WORM vault as a node in a private network segment rather than a service accessible from the public internet, once that deployment model ships.

**The seL4 Microkit image for os-totebox has moved from planned to live-verified: a real boot of the image is confirmed, with end-to-end inference round-trips confirmed working.** Everything above describes the intended end-state design; the boot-and-inference milestone above is real progress on that path, but the persistence, graceful-shutdown, and ledger-anchoring gaps described in Known limitations remain open — see that section before treating this as a production-ready persistent vault. Implementation status is tracked in the platform's engineering registry — see `os-totebox`'s own crate description for further detail on the currently-deployed build (service-content + service-slm running as one conventional process, in general deployment).
