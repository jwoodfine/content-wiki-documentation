---
schema: foundry-doc-v1
title: "Moonshot initiatives"
slug: moonshot-initiatives
category: governance
type: topic
content_type: topic
quality: complete
index_group: engineering-sovereignty
short_description: "Moonshot initiatives are active engineering programs building native replacements for quarantined third-party dependencies, reducing vendor lock-in."
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
or `vendor-microsoft-graph`) — each carrying a "Quarantined Foreign
Component" warning banner in its `README.md`. No foreign code runs
inside a capability sandbox behind these banners yet; the directories
today are placeholders marking the boundary, not active containment.

## Replacement pipeline

For every quarantined dependency, the engineering team opens a
corresponding moonshot directory (for example, `moonshot-database`
or `moonshot-kernel`). Work in these directories targets native,
formally verified implementations in Rust. Once a moonshot component
reaches structural parity with its quarantined counterpart, it
replaces the isolated directory. The ledger entry closes at that
point.

## Initiative areas and real status

Nine moonshot directories exist. Three carry substantial, active engineering today; the remaining six are named directories with a 4-file Cargo scaffold and no implementation yet:

| Initiative | Target dependency | Status |
|---|---|---|
| `moonshot-index` | External search and index backends | Active — a working trigram substring index plus a planned ranked-search layer, pure `std`, no external dependency |
| `moonshot-sel4-vmm` | Commodity virtual machine monitor | Active — a real seL4 protection-domain runtime with multiple working binaries, including a confirmed HTTP call over VirtIO-net DMA |
| `moonshot-toolkit` | External build and CI tooling | Active — a working Rust build orchestrator that produces a bootable system image |
| `moonshot-database` | External database engine | Scaffold — directory and Cargo manifest exist, no implementation |
| `moonshot-gpu` | Cloud GPU inference services | Scaffold — directory and Cargo manifest exist, no implementation |
| `moonshot-hypervisor` | External hypervisor layer | Scaffold — directory and Cargo manifest exist, no implementation |
| `moonshot-kernel` | Commodity Linux kernel | Scaffold — directory and Cargo manifest exist, no implementation. The [[sel4-microkernel-substrate|seL4 formally verified microkernel]] is the intended eventual replacement for the quarantined systemd/Linux dependency recorded in [[architecture-decisions|ADR-08]], but that replacement work currently lives in `moonshot-sel4-vmm`, not here |
| `moonshot-network` | External network control plane | Scaffold — directory and Cargo manifest exist, no implementation |
| `moonshot-protocol` | Proprietary communication protocols | Scaffold — directory and Cargo manifest exist, no implementation |

Completion status of each initiative is tracked in the [[sovereign-replacement-initiative|Sovereign Replacement Initiative]] ledger.

## Vendor and customer roles

- The Vendor (PointSav Digital Systems) maintains the moonshot ledgers and engineers the native replacements.
- The Customer (MCorp) audits the pipeline to verify progress toward operational independence.

## See also

- [[sovereign-replacement-initiative|Sovereign Replacement Initiative]] — governance program that coordinates these engineering efforts
- [[sel4-microkernel-substrate]] — the formally verified microkernel that `moonshot-kernel` and `moonshot-sel4-vmm` target
- [[architecture-decisions]] — ADR-08 records the systemd quarantine that moonshot-kernel is designed to close
- [[ontological-governance|Ontological Governance]] — the taxonomy governance that provides nomenclature for quarantined components
- [[verification-surveyor|Verification Surveyor]] — the audit agent that tracks completion status of each initiative
