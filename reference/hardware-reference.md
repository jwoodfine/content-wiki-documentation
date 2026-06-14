---
schema: foundry-doc-v1
title: "Hardware reference"
slug: hardware-reference
short_description: "Reference hardware profiles for developer workstations and fleet devices, specifying CPU architectural requirements including Haswell-generation x86_64 and fsgsbase support, and defining three infrastructure deployment patterns from on-premise to cloud."
category: reference
type: reference
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-15
editor: pointsav-engineering
paired_with: hardware-reference.es.md
---

The PointSav hardware reference defines the device profiles and infrastructure configurations against which the substrate is tested and deployed. Three tiers cover the developer workstation, the fleet device, and the legacy build host; three infrastructure patterns extend from on-premise to leased bare metal to cloud. Hardware fragmentation is the primary enemy of OS stability; the reference list is narrow by design, selecting for driver compatibility under a hardened FreeBSD or seL4 base. By the end of this article, a reader will understand the reference device list, the CPU architectural requirements, the infrastructure deployment patterns, and the Tier-1 cloud baseline constraint.

## Reference hardware profiles

[[os-workplace|os-workplace]] and [[console-os|os-console]] target a deliberate set of devices:

| Tier | Device | Rationale |
|---|---|---|
| Flagship | Dell XPS 13 / 14 (Developer Edition) | Dell ships an official Linux profile; Intel WiFi and graphics drivers mature into FreeBSD quickly |
| Fleet | HP ProBook 400 series (445 / 450) | Enterprise-grade WiFi chipsets with BSD compatibility; suitable for larger SMB and customer deployments |
| Build host (legacy) | iMac 12.1 (Sandy Bridge, 2011) | The original build machine through early 2026; subsequently superseded for `service-content` development work |

The selection criterion is driver availability, not brand preference. Consumer laptops with proprietary WiFi modules that lack BSD-compatible drivers are excluded on that basis alone.

## CPU architectural requirements

Three constraints govern what hardware can run the PointSav substrate:

| Constraint | Requirement |
|---|---|
| Instruction set | Haswell-generation x86_64 or later |
| Required extension | `fsgsbase` — used by optimised seL4 microkernel paths |
| Memory paging | 1 GB Huge Pages enabled (`+pdpe1gb` CPU flag) |

Pre-Haswell CPUs — Nehalem and earlier — lack `fsgsbase`. Attempting to run the kernel on pre-Haswell hardware triggers a `UserException` on the first kernel print. The constraint is a functional prerequisite, not a performance preference.

## Infrastructure deployment patterns

[[infrastructure-os|os-infrastructure]] deploys in three patterns, each with a distinct trust profile:

| Pattern | Hardware | Trust profile |
|---|---|---|
| On-premise | Server in the customer's office (Dell PowerEdge T160 tower or R760 rack are reference configurations) | Highest trust — the operator owns the metal |
| Leased | Colocated bare metal at an external data centre | Hybrid trust — the boot process cannot be physically verified |
| Cloud | Hyperscaler VMs (Google Cloud at the canonical baseline) | Lowest trust — used for stateless edge relay |

## Bare-metal vendor research — Vancouver region

Archive research from 2026 assessed the Vancouver, British Columbia market for bare-metal options closest to the primary customer deployment region. The table records research findings and does not constitute a commercial recommendation:

| Vendor | Physical location | Latency to Vancouver | Characteristics |
|---|---|---|---|
| Atal Networks | Vancouver, BC | <1–2 ms | True local bare metal with IPMI/KVM; unmanaged; direct peering with regional ISPs |
| GTHost | Vancouver, BC | <1–2 ms | Instant-activation provisioning; automation-first |
| Vultr | Seattle, WA | ~3–10 ms | API-driven bare metal; hourly billing |
| OVHcloud | Montreal, QC | ~60–80 ms | Lower cost; high cross-continent latency |

Sub-2-millisecond latency is favoured for production Toteboxes serving local operators. Cloud bare metal in the Seattle region is acceptable for stateless edge functions.

## The Tier-1 baseline node

The most-tested cloud target is a single canonical profile: Google Cloud `e2-micro` at approximately seven US dollars per month. This profile anchors the Compute Matrix Tier-1 baseline:

| Property | Value |
|---|---|
| Approximate cost | ~$7 USD / month (2026 baseline) |
| RAM | ≤1 GB |
| Hardware virtualisation | Disabled by provider — nested VMs unavailable |
| Storage | Persistent disk |
| Role | [[worm-ledger-design|WORM ledger]] + cryptographic router; defers SLM inference to the relay |

The architectural constraint is that a complete Totebox must be able to operate on this footprint. The system must be functional for an operator who cannot provision premium hyperscaler resources.

## Hardware virtualisation constraints

The `e2-micro` baseline disables hardware virtualisation, which prevents running Micro-VMs on that tier. The architectural response is two-pronged:

1. The substrate uses true unikernels (Nanos, Unikraft) rather than Micro-VMs where the cloud provider forbids nested virtualisation.
2. Higher-tier deployments that require Micro-VMs run on bare metal or KVM-capable cloud instances.

## See also

- [[os-workplace]] — the workstation OS that runs on the reference device profiles
- [[infrastructure-os]] — the infrastructure OS covering the three deployment patterns
- [[worm-ledger-design]] — the WORM ledger deployed on the Tier-1 baseline node
- [[sel4-microkernel-substrate]] — the seL4 microkernel that enforces the CPU architectural constraints
