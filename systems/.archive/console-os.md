---
schema: foundry-doc-v1
title: "Command ledger"
slug: console-os
category: systems
type: concept
content_type: topic
quality: complete
status: archived
archived: 2026-07-31
archived_reason: "Genuine content fragmentation with os-console-architecture.md and os-console-platform.md — all three described the same product (os-console) at overlapping technical depths, with real inconsistencies (differing F-key/cartridge-state tables). Also carried a reversed slug (console-os instead of os-console, the name used throughout its own body). Merged into one canonical systems/os-console.md."
superseded_by: os-console
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-07-18
editor: pointsav-engineering
paired_with: console-os.es.md
short_description: "os-console is the human-facing surface of the PointSav platform — a Command Ledger connecting to a Totebox and rendering its state via a keyboard-driven interface."
cites: []
references:
  - id: 1
    text: "Green, C. 'Improved Alpha-Tested Magnification for Vector Textures and Special Effects.' ACM SIGGRAPH 2007 courses, 2007."
    url: "https://dl.acm.org/doi/10.1145/1281500.1281665"
  - id: 2
    text: "ISO 19650-1:2018 — Organization and digitization of information about buildings and civil engineering works, including building information modelling (BIM)."
    url: "https://www.iso.org/standard/68078.html"
---

`os-console` is the human-facing surface of the PointSav platform — a Command Ledger that connects to one [[totebox-os|Totebox]] and renders its state to the operator. It does not store data and does not run services; it is a high-fidelity terminal purpose-built around keyboard-driven operator flow. The reference point is the professional financial terminal: a single keyboard, a small set of [[os-console-platform|function keys]], and a relentless focus on the operator's context. The binary is written from scratch in Rust for sub-50-millisecond cold start and a 15-megabyte footprint. This article covers how os-console runs, the F-key surface, the [[three-ring-architecture|rendering stack]], and the two operating modes.

## How it runs

`os-console` ships as a single executable and runs today as a standard terminal
application, built on `ratatui` and `crossterm`. **Planned, not current**: a
hardware-isolated runtime where the host operating system's native virtualisation API
(Windows Hypervisor Platform, `Hypervisor.framework`, or KVM) boots a small, isolated
[[sel4-microkernel-substrate|seL4]] environment around the application. This is roadmap
work, not a description of the binary as it ships today — reserve "kernel-enforced" and
similar claims for that future state, not the present one.

The security model relies on [[machine-based-auth|hardware-bound pairings]] rather than
usernames or passwords, independent of the VM-isolation roadmap item above.

## The F-key surface

The interface organises every entity's reality into a fixed set of pillars. Each pillar is a function key:

| Key | Pillar | Service |
|---|---|---|
| F1 | HELP | Read-only operating procedures |
| F2 | PEOPLE | [[service-people|service-people]] — the identity ledger |
| F3 | EMAIL | [[service-email|service-email]] — the Comm Diode |
| F4 | CONTENT | [[service-content|service-content]] — the drafting and synthesis engine |
| F5 | MINUTEBOOK | service-minutebook — deep records |
| F6 | BOOKKEEPER | service-bookkeeper — the financial ledger |
| F12 | INPUT MACHINE | [[app-console-input]] — the human-in-the-loop ingestion gateway |

F12 is mandatory per [[architecture-decisions|SYS-ADR-10]]. The [[app-console-input|Input Machine]] is the only surface through which raw external files can enter a Totebox. Files dropped into F12 have execution permissions stripped, are tagged against the operator's [[archetypes-and-chart-of-accounts|Chart of Accounts]], and are routed to F5 or F6.

## The rendering stack

`os-console` today is a terminal interface: widget logic and rendering are built on
`ratatui`, with `crossterm` handling the terminal backend. **Planned, not current**: a
standalone, GPU-native rendering pipeline (a WGPU-based Vulkan/Metal/DX12 abstraction with
a Signed Distance Field [^1] glyph renderer for infinite-zoom fidelity, variable-weight
headers, and bloom effects) that would replace the terminal-hosted renderer entirely. The
design intent for that future pipeline shares its philosophy with
[[design-philosophy|the broader PointSav design system]], but it is not the stack running
today.

## Direct mode and aggregate mode

`os-console` operates in two modes determined by what it pairs with:

| Mode | Pair | Use case |
|---|---|---|
| Direct | One [[totebox-os|Totebox]] | A single entity's deep view; the default for individual operators |
| Aggregate | One [[os-orchestration|os-orchestration]] (which aggregates many Toteboxes) | A portfolio view for executives and commercial-tier deployments |

Both modes use the same `os-console` binary. The aggregator does not require a different Console. The complexity lives in `os-orchestration`.

## Single, unified, universal

`os-console` is one product. There is no "Home" edition and no "Pro" edition. An individual hosting one Totebox uses the same Command Ledger as the administrator of a [[compliance-and-continuous-disclosure|Reporting Issuer]] aggregating hundreds. Commercial differentiation is determined by the presence or absence of `os-orchestration`, never by a tiered Console. The [[six-tier-sovereignty-matrix|six-tier sovereignty model]] governs how commercial tiers are structured across the platform.

## See also

- [[totebox-os]] — the Totebox archive that os-console connects to and renders
- [[app-console-input]] — the F12 Input Machine; deep coverage of the mandatory ingestion gateway
- [[diode-standard]] — why commands flow in one direction through the established pair
- [[os-family-overview]] — the five OS surfaces and how os-console fits among them
- [[deployment-patterns]] — how os-console appears in each of the six canonical deployment configurations
