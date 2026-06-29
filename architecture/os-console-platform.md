---
schema: foundry-doc-v1
title: "os-console: platform and cartridge architecture"
slug: os-console-platform
category: architecture
type: concept
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-06-29
editor: pointsav-engineering
paired_with: os-console-platform.es.md
short_description: "os-console is a single Rust binary that hosts independent TUI workspaces — cartridges — within a unified keyboard-navigation chassis built on app-console-keys; this article covers the platform structure, the F-key cartridge map, MBA connectivity, and Three-Ring Architecture placement."
cites: []
references: []
---

`os-console` is the keyboard-native console interface for Woodfine's Totebox Archive operations. It compiles as a single Rust binary, runs natively on Linux and macOS, renders full-featured terminal user interfaces, and connects to backend `os-*` services through [[machine-based-auth|Machine-Based Authorization]]. The binary delivers a console that starts in milliseconds, responds at keyboard speed, and continues operating on locally-cached content when backend services are temporarily unavailable.

The internal design — how the binary implements the Cartridge trait and chassis event dispatch — is covered in [[os-console-architecture]]. This article covers the platform itself: what the binary is, how the cartridge model works, the F-key map, and placement within the Three-Ring Architecture.

> **Planned direction.** A rebuild program is intended to evolve os-console into a host-native, dual-input sovereign desktop: multiple cartridges visible simultaneously, full mouse support with keyboard parity, and a live capability-visibility surface. The descriptions below reflect the current platform as built; forward-looking capabilities are marked as planned or intended.

## The binary

`os-console` is one compiled binary containing all cartridges. No dynamic plugin loading occurs at runtime. No subprocesses are launched. All workspaces, all navigation logic, and all backend clients compile together into a single deployable artifact.

This compilation model produces predictable runtime behaviour: a cartridge absent from a build is not linked in, and its F-key slot appears unavailable in the tab strip. The operator cannot install or remove cartridges at runtime — the set of available workspaces is fixed at build time.

The binary runs on two platforms:

**Linux (primary deployment).** The reference deployment runs on a Linux system on the operator's primary workstation. Any VTE-based terminal emulator is compatible; the Kitty terminal is recommended for full pixel-graphics capability, including in-terminal PDF rendering.

**macOS (executive workstations).** Native macOS binaries built via CI on macOS runners. Compatible terminals include Kitty, Ghostty, iTerm2, and WezTerm.

## The base chassis: app-console-keys

`app-console-keys` is the always-present base chassis inside `os-console`. Its relationship to `os-console` is analogous to `service-fs`'s relationship to `os-totebox`: it is the minimum required component — everything else is additive.

A minimal installation — serving an operator who wants only F-key navigation and a connection to one Totebox Archive — needs only `app-console-keys`. Every other cartridge extends that base.

`app-console-keys` provides four core capabilities:

**The Cartridge trait.** The interface that every cartridge implements. The trait is the only contract between a cartridge and the chassis — there are no other public APIs, no shared memory, and no direct coupling between cartridges.

**F-key navigation framework.** The tab strip rendered at the top of the console, the event dispatcher that routes keyboard input to the active cartridge, and the mechanism by which F12 always triggers the Input Machine regardless of the active cartridge (see [[input-machine]]).

**The status bar.** A persistent bottom-of-screen panel showing a live situational picture: operator identity, MBA connection state, active cartridge, SLM tier in use, and session duration. A representative rendering:

```
operator@tenant | MBA LINK ACTIVE | F4: Content | Tier A | 00:04:23
```

**MBA client.** The outbound connection manager for [[machine-based-auth|Machine-Based Authorization]]: reads the pairing configuration, initiates connections to paired `os-*` services, and presents the aggregate connection state in the status bar.

One naming note: `app-console-keys` refers to F-keys (keyboard function keys), not cryptographic keys. The MBA cryptographic implementation is in `system-gateway-mba`, a separate system-layer crate.

## Cartridges

Each `app-console-*` crate is a Rust library that implements the `Cartridge` trait and compiles directly into `os-console`. Cartridges are not loaded dynamically. The cartridge list at build time is the cartridge list at runtime.

The single-trait interface enforces strict isolation: one cartridge cannot directly call another. All inter-cartridge data flow passes through backend `os-*` services. Each cartridge's internal state is invisible to every other cartridge — a design that simplifies both implementation and security review.

Cartridges are optional except `app-console-keys`. An installation including only the editorial cartridge (F4) and the Input Machine (F12) is a complete, valid deployment for editorial work.

## The F-key map

The console presents twelve addressable slots via F-keys. F12 is permanently assigned to the Input Machine — it is The Anchor, immovable by design. The remaining slots are organized by operational domain, with high-frequency operations at lower F-numbers:

| F-key | Cartridge | Domain |
|---|---|---|
| F1 | `app-console-help` | Help overlay — always available |
| F2 | `app-console-people` | Identity and contacts |
| F3 | `app-console-email` | Communications |
| F4 | `app-console-content` | Editorial — proofread, draft, verify |
| F5 | `app-console-minutebook` | Governance — minutes, resolutions |
| F6 | `app-console-bookkeeper` | Financial ledger |
| F7 | `app-console-bim` | Building information management |
| F8 | `app-console-gis` | Geographic information |
| F9 | `app-console-slm` | AI management and adapter marketplace |
| F10 | `app-console-mesh` | PPN mesh management |
| F11 | `app-console-system` | Live `os-*` service health and MBA status |
| F12 | `app-console-input` | **The Anchor** — Input Machine ([[sys-adr-10]]) |

F12's permanent assignment to document ingest is the constraint recorded in [[sys-adr-10]]. The F-key that anchors the compliance boundary does not move regardless of how other slots evolve.

## MBA connectivity

`app-console-keys` maintains outbound MBA connections to each paired `os-*` service independently. The console can be active with `os-totebox` and inactive with `os-privategit` simultaneously; the status bar shows the aggregate state. When `MBA LINK INACTIVE`, the console operates in local-only mode: cached content remains accessible and service requests fail gracefully. For the MBA mechanism see [[machine-based-auth]].

## PDF rendering

`os-console` supports in-terminal PDF rendering using Rust bindings to the pdfium library. PDF pages are rendered to RGB bitmaps and displayed using the Kitty graphics protocol on compatible terminals, with the Sixel protocol as a fallback. The rendering is pixel-accurate — a faithful reproduction of the PDF's layout, typefaces, and graphics — not a text extraction or reflow. A compatible terminal is required; the capability is disabled on terminals that support neither protocol.

## Three-Ring Architecture placement

`os-console` is a client of the Three-Ring Architecture, not a ring itself. It connects to Ring 1 and Ring 2 services through the MBA layer:

- **Ring 1 services:** `service-input` (via F12 Input Machine), `service-people` (via F2), `service-email` (via F3), `service-fs`
- **Ring 2 services:** `service-content`, `service-search`
- **Ring 3 service:** `service-slm` (the Doorman inference gateway)

`os-console` is the human interface through which an operator instructs the rings. It does not perform the work of any ring; the rings operate independently and the console connects to them.

## See also

- [[os-console-architecture]] — internal Cartridge trait implementation and chassis event dispatch
- [[input-machine]] — F12: The Anchor; mandatory document ingest gate
- [[machine-based-auth]] — the authorization mechanism os-console uses to connect to os-* services
- [[ppn-mesh-architecture]] — the infrastructure layer the os-* services run on
- [[three-ring-architecture]] — the service architecture within which os-console operates as a client
- [[sys-adr-10]] — the architectural decision record establishing F12 as the mandatory ingest checkpoint
