---
schema: foundry-doc-v1
title: "Command ledger"
slug: console-os
category: systems
type: concept
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-15
editor: pointsav-engineering
paired_with: console-os.es.md
short_description: "os-console is the human-facing surface of the PointSav platform — a Command Ledger that connects to a Totebox and renders its state to the operator via a keyboard-driven, F-key-structured interface."
cites: []
references:
 - id: 1
 text: "Green, C. 'Improved Alpha-Tested Magnification for Vector Textures and Special Effects.' ACM SIGGRAPH 2007 courses, 2007."
 url: "https://dl.acm.org/doi/10.1145/1281500.1281665"
 - id: 2
 text: "ISO 19650-1:2018 — Organization and digitization of information about buildings and civil engineering works, including building information modelling (BIM)."
 url: "https://www.iso.org/standard/68078.html"
---

`os-console` is the human-facing surface of the PointSav platform — a Command Ledger that connects to one [[totebox-os|Totebox]] and renders its state to the operator. It does not store data and does not run services; it is a high-fidelity terminal purpose-built around keyboard-driven operator flow. The reference point is the Bloomberg Terminal: a single keyboard, a small set of function keys, and a relentless focus on the operator's context. The binary is written from scratch in Rust for sub-50-millisecond cold start and a 15-megabyte footprint. This article covers how os-console runs, the F-key surface, the rendering stack, and the two operating modes.

## How it runs

`os-console` ships as a single executable. On the host operating system — Windows, macOS, or Linux — it acts as a Virtual Machine Monitor: it uses the host's native virtualisation API to create a small, isolated VM in RAM and boots an seL4 environment inside it.

| Host | Native VMM API |
|---|---|
| Windows | Windows Hypervisor Platform (WHPX) |
| macOS | `Hypervisor.framework` |
| Linux | KVM |

The operator thinks they opened an application. What they have done is spun up a hardware-isolated secure environment in roughly 50 milliseconds. When the application closes, the secure memory is wiped. Nothing touches the host hard drive.

## The F-key surface

The interface organises every entity's reality into a fixed set of pillars. Each pillar is a function key:

| Key | Pillar | Service |
|---|---|---|
| F1 | HELP | [[app-console-input|content-wiki-documentation]] (read-only operating procedures) |
| F2 | PEOPLE | [[service-people|service-people]] — the identity ledger |
| F3 | EMAIL | [[service-email|service-email]] — the Comm Diode |
| F4 | CONTENT | [[service-content|service-content]] — the drafting and synthesis engine |
| F5 | MINUTEBOOK | [[service-minutebook|service-minutebook]] — deep records |
| F6 | BOOKKEEPER | [[service-bookkeeper|service-bookkeeper]] — the financial ledger |
| F12 | INPUT MACHINE | [[app-console-input]] — the human-in-the-loop ingestion gateway |

F12 is mandatory per [[architecture-decisions|SYS-ADR-10]]. The [[app-console-input|Input Machine]] is the only surface through which raw external files can enter a Totebox. Files dropped into F12 have execution permissions stripped, are tagged against the operator's [[archetypes-and-chart-of-accounts|Chart of Accounts]], and are routed to F5 or F6.

## The rendering stack

`os-console` is not a TUI inside a host terminal. It is a standalone graphics application that happens to display text. The stack is owned end-to-end:

| Layer | Component | Notes |
|---|---|---|
| Window | `pointsav-window` | Custom Win32 / Cocoa / X11/Wayland wrapper |
| GPU | `pointsav-gpu` | WGPU (Vulkan / Metal / DX12 abstraction); licence embedded in binary |
| Text | `pointsav-text` | Signed Distance Field (SDF) glyph renderer [^1]; infinite-zoom fidelity |
| Layout | `pointsav-layout` | Recursive row/column grid in roughly 500 lines of Rust |
| Widget logic | Forked from ratatui core | Logic only; ratatui's renderer replaced by the WGPU pipeline |

The result is a terminal interface with variable-weight headers, bloom effects, and smooth scrolling — while remaining purely keyboard-driven and rendering at the fidelity required by ISO 19650 [^2] document-state suffixes.

## Direct mode and aggregate mode

`os-console` operates in two modes determined by what it pairs with:

| Mode | Pair | Use case |
|---|---|---|
| Direct | One [[totebox-os|Totebox]] | A single entity's deep view; the default for individual operators |
| Aggregate | One [[os-orchestration|os-orchestration]] (which aggregates many Toteboxes) | A portfolio view for executives and commercial-tier deployments |

Both modes use the same `os-console` binary. The aggregator does not require a different Console. The complexity lives in `os-orchestration`.

## Single, unified, universal

`os-console` is one product. There is no "Home" edition and no "Pro" edition. An individual hosting one Totebox uses the same Command Ledger as the administrator of a Reporting Issuer aggregating hundreds. Commercial differentiation is determined by the presence or absence of `os-orchestration`, never by a tiered Console.

## See also

- [[totebox-os]] — the Totebox archive that os-console connects to and renders
- [[app-console-input]] — the F12 Input Machine; deep coverage of the mandatory ingestion gateway
- [[diode-standard]] — why commands flow in one direction through the established pair
- [[os-family-overview]] — the five OS surfaces and how os-console fits among them
- [[deployment-patterns]] — how os-console appears in each of the six canonical deployment configurations
