---
schema: foundry-doc-v1
title: "Moonshot initiatives"
slug: moonshot-initiatives
category: governance
type: topic
quality: complete
short_description: "Moonshot initiatives are active engineering programs that build native replacements for quarantined third-party dependencies, with the goal of eliminating vendor lock-in and reducing the platform's external attack surface over time."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-19
editor: pointsav-engineering
cites: []
paired_with: moonshot-initiatives.es.md
---


> Moonshot initiatives are long-running engineering programs that replace quarantined third-party dependencies with internally built, formally verifiable equivalents — reducing vendor lock-in and shrinking the platform's external attack surface.

The platform actively tracks third-party engineering debt in
a structured ledger. Foreign architectural components are contained
in isolated directories, called quarantined component silos, until
a **moonshot initiative** delivers a native replacement. The
[[sovereign-replacement-initiative|Sovereign Replacement Initiative]]
is the governance program that coordinates these efforts. Each
moonshot initiative is a distinct engineering effort targeting one
dependency class; completion is defined as structural parity with
the component it replaces, at which point the native implementation
physically supersedes the quarantined directory.

## Technical debt tracking

The ledger records every identified foreign dependency alongside its
isolation status and the associated moonshot initiative, if one has
been opened. Entries remain active until replacement is confirmed.
This gives auditors and contributors a live picture of the
platform's outstanding external exposure.

## Quarantine protocol

Until a legacy component can be replaced, it is physically isolated
into a quarantined component silo (for example, `vendor-azure-auth`
or `vendor-microsoft-graph`). These directories act as structural
boundaries. The foreign code may not execute outside a tightly
controlled capability sandbox. Isolation prevents a dependency from
spreading coupling into adjacent platform layers.

## Replacement pipeline

For every quarantined dependency, the engineering team opens a
corresponding moonshot directory (for example, `moonshot-database`
or `moonshot-kernel`). Work in these directories targets native,
formally verified implementations in Rust. Once a moonshot component
reaches structural parity with its quarantined counterpart, it
replaces the isolated directory. The ledger entry closes at that
point.

## Active initiative areas

Each moonshot targets a distinct dependency class. The following classes have open initiatives in the engineering platform:

| Initiative | Target dependency | Rationale |
|---|---|---|
| `moonshot-database` | External database engine | Data layer sovereignty; replace foreign engine with a formally verified flat-file or embedded store |
| `moonshot-gpu` | Cloud GPU inference services | Inference sovereignty; platform-local GPU capacity removes reliance on cloud inference APIs |
| `moonshot-hypervisor` | External hypervisor layer | Substrate sovereignty; a verified hypervisor closes the gap between the seL4 microkernel and commodity hardware |
| `moonshot-index` | External search and index backends | Search sovereignty; a platform-native index eliminates dependency on third-party search infrastructure |
| `moonshot-kernel` | Commodity Linux kernel | Kernel sovereignty; the [[sel4-microkernel-substrate|seL4 formally verified microkernel]] replaces the quarantined systemd/Linux dependency recorded in [[architecture-decisions|ADR-08]] |
| `moonshot-network` | External network control plane | Network sovereignty; a native WireGuard-native mesh eliminates reliance on managed network services |
| `moonshot-protocol` | Proprietary communication protocols | Protocol sovereignty; replace proprietary wire protocols with open, formally specified equivalents |
| `moonshot-sel4-vmm` | Commodity virtual machine monitor | Verification layer; a seL4-native VMM closes the verified boundary below all guest operating systems |
| `moonshot-toolkit` | External build and CI tooling | Build sovereignty; a Rust-native build orchestrator replaces reliance on external CI infrastructure |

Completion status of each initiative is tracked in the [[sovereign-replacement-initiative|Sovereign Replacement Initiative]] ledger.

## Vendor and customer roles

- The Vendor (PointSav Digital Systems) maintains the moonshot ledgers and engineers the native replacements.
- The Customer (Woodfine Management Corp.) audits the pipeline to verify progress toward operational independence.

## See also

- [[sovereign-replacement-initiative|Sovereign Replacement Initiative]] — governance program that coordinates these engineering efforts
- [[sel4-microkernel-substrate]] — the formally verified microkernel that `moonshot-kernel` and `moonshot-sel4-vmm` target
- [[architecture-decisions]] — ADR-08 records the systemd quarantine that moonshot-kernel is designed to close
- [[ontological-governance|Ontological Governance]] — the taxonomy governance that provides nomenclature for quarantined components
- [[verification-surveyor|Verification Surveyor]] — the audit agent that tracks completion status of each initiative
