---
schema: foundry-doc-v1
type: topic
content_type: topic
slug: os-totebox-sovereign-archive
title: "os-totebox: The Sovereign WORM Data Vault"
short_description: "os-totebox is a Type I bare-metal operating system built on a formally verified seL4 microkernel, providing a WORM data vault whose storage immutability is enforced by a compiled capability graph rather than administrative policy."
audience: vendor-public
bcsc_class: current-fact
language: en
paired_with: os-totebox-sovereign-archive.es.md
category: architecture
status: active
quality: complete
last_edited: 2026-06-23
---

# os-totebox: The Sovereign WORM Data Vault

Every organisation that relies on a third-party platform to store its records is making an implicit wager: that the platform provider will remain solvent, accessible, and free of security failures for as long as those records matter. os-totebox is designed for operators who have decided that wager is unacceptable.

## What os-totebox Is

os-totebox is a Type I bare-metal operating system — meaning it runs directly on physical hardware with no general-purpose operating system underneath it. There is no Linux shell, no package manager, no root process, and no init system. The software that runs on os-totebox hardware is a seL4 Microkit image: a formally verified microkernel with a statically compiled set of services and no runtime modification path.

The defining characteristic of the platform is its storage model. os-totebox operates as a WORM vault — Write Once, Read Many. Records written to the system cannot be altered or deleted through any software pathway. This is not a policy enforced by an access-control list or a permission flag that an administrator could override; it is a property of the capability graph that governs every service on the machine.

## Capability Geometry on Server Hardware

seL4 is a microkernel developed and formally verified by CSIRO's Data61. The verification proves, mathematically, that the kernel's access-control model is enforced without exception. On os-totebox, this property extends to the inter-service architecture.

Each service on os-totebox runs inside a seL4 Protection Domain — an isolated execution environment that holds only the capabilities the system design explicitly grants it. The capability DAG (directed acyclic graph) that defines these grants has been formally proved. There is no path in the graph from a service that processes external input to the service that holds the storage capability.

This matters in a concrete failure scenario. If service-slm — the component that handles language model inference, and therefore the component most directly exposed to adversarial inputs — were to be fully compromised, the compromised code would find itself bounded by its Protection Domain. It holds no capability to reach service-fs. It cannot read the WORM block device. It cannot write to it. The attacker's foothold is geometrically isolated from the data store. This is the property the platform calls Capability Geometry.

## The Ring Architecture

os-totebox organises its services into two concentric rings based on their proximity to storage.

**Ring 1** comprises the services that interact directly with durable data and external I/O: service-fs, service-input, service-extraction, and service-egress. service-fs holds the WORM block device capability exclusively — it is the only Protection Domain on the machine that can perform storage operations. No other service can reach the block device directly, regardless of its execution state.

**Ring 2** comprises the services that process, classify, and reason about data: service-content, service-people, service-email, and service-slm. These services communicate with Ring 1 through a defined and bounded inter-domain communication protocol. They can request that service-fs write a record; they cannot hold the capability to do so themselves.

This separation is not an architectural preference that future developers might relax. The capability graph is compiled into the seL4 image at build time. Modifying the capability structure requires rebuilding and re-deploying the image — a step that produces a new, auditable artifact rather than a silent runtime change.

## The Sovereign Data Archive

The operating model that os-totebox enables is one where the operator's hardware and the operator's capability graph are the complete system. There is no cloud dependency in the storage path. Ingested records are written to a physical device under the operator's physical control and cannot leave the machine through any software pathway that the capability DAG does not permit.

This has practical implications beyond security. An organisation whose records exist only on its own hardware is not subject to a vendor's data-residency policies, a cloud provider's outage window, or a platform's terms-of-service change. The audit trail is local, the retention schedule is the operator's to set, and the physical device can be decommissioned under the operator's procedures.

For sectors where records carry legal weight — corporate minute books, real property files, financial ledgers, regulated correspondence — the immutability of a WORM vault is not merely a technical feature. It is the evidence that a record existed in a given state at a given time and has not been altered since.

## Operational Surface for Small and Mid-Size Organisations

Enterprise-grade formal verification and hardware-rooted immutability have historically required dedicated security infrastructure teams to deploy and operate. os-totebox is designed to deliver those properties on commodity hardware with an operational surface that does not assume a specialist security organisation.

The absence of a shell is not an inconvenience — it is a feature. A system with no shell has no interactive attack surface. A system with no root process has no privilege escalation path. A system with no package manager cannot be updated in ways that introduce unaudited code. The seL4 image that runs on the hardware is the complete and auditable software inventory of the machine.

An organisation deploying os-totebox is not relying on an administrator's diligence to enforce data protection policies. It is relying on a formally proved capability graph. The distinction is the difference between a policy and a proof.

## Relationship to the Broader Platform

os-totebox is one of three purpose-specific bare-metal operating systems in the platform architecture. It operates alongside os-console, which provides the keyboard-native operator interface, and os-orchestration, which manages the Totebox Archive execution environment. The three systems share no kernel code paths and communicate only through defined network channels.

The intended deployment pattern is operator-owned hardware with a single physical network interface. The WORM vault is not a service accessible from the public internet; it is a node in a private network segment whose ingress paths are controlled by the same capability discipline that governs its storage.

The seL4 Microkit image for os-totebox is planned for Phase H1 of the platform roadmap. The capability DAG and ring architecture described here represent the intended design; implementation status is tracked in the platform's engineering registry.
