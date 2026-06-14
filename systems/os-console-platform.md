---
schema: foundry-doc-v1
title: "os-console platform and cartridge architecture"
slug: os-console-platform
short_description: "os-console is a single Rust binary with a cartridge architecture that provides keyboard-native access to Totebox Archive workflows through F-key-navigated modules."
category: systems
type: topic
content_type: topic
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-25
editor: pointsav-engineering
paired_with: os-console-platform.es.md
---

`os-console` is Woodfine's keyboard-native console interface — a single Rust binary that provides direct access to the [[totebox-archive|Totebox Archive]], editorial workflows, governance records, and infrastructure management from a terminal. It connects to backend `os-*` services through [[machine-based-auth|machine-based authorization]] and operates fully offline when backend services are unavailable.

The design principle is end-to-end ownership: every component is compiled into a single binary, with no dynamic plugin loading, no subprocess launching, and no nesting. The console starts in milliseconds and responds at keyboard speed.

## The binary

`os-console` is the deployable artifact: one binary, one process, all cartridges compiled in. It runs as a native application on the host operating system. Platform targets include Linux Mint on the on-premises iMac workstation and macOS 13 or later on executive workstations.

An optional SSH server mode, compiled with the `--features ssh-server` flag, enables remote access over port 2222 for use on a GCE VM, providing the same TUI experience over an SSH session.

## The base chassis: app-console-keys

`app-console-keys` is the always-installed base chassis inside `os-console`. Its relationship to `os-console` is analogous to [[service-fs-architecture|`service-fs`]]'s relationship to `os-totebox`: it is the minimum required component that must be present; everything else is optional.

`app-console-keys` provides the `Cartridge` trait (the interface all cartridges implement), the F-key navigation framework (the horizontal tab strip, F-key input dispatch, and active-cartridge routing), the status bar showing [[machine-based-auth|machine-based authorization]] connection state and session identity, the authorization client that manages connections to paired `os-*` services, and profile-based configuration stored at `~/.config/os-console/config.toml`.

**Naming note:** "keys" in `app-console-keys` refers to F-keys — keyboard function keys. It does not refer to cryptographic keys. Machine-based authorization is implemented by `system-gateway-mba`, a separate crate.

## Cartridges

Each `app-console-*` crate is a library crate that implements the `Cartridge` trait. Cartridges are compiled into `os-console` directly — not loaded dynamically and not launched as subprocesses. A cartridge that is not installed has its F-key slot greyed in the tab strip.

Cartridges are optional except for `app-console-keys` and `app-console-input` (F12). An installation that includes only `app-console-content` (F4) and `app-console-input` (F12) is a complete, valid os-console deployment for editorial work.

## F-key map

The console presents twelve addressable slots via F-keys. F12 is fixed as The Anchor — the [[input-machine]] — and is never moved. The complete [[console-os|os-console]] article describes the broader product design and deployment context.

| F-key | Cartridge | Domain |
|---|---|---|
| F1 | `app-console-help` | Help overlay |
| F2 | `app-console-people` | Identity and contacts |
| F3 | `app-console-email` | Communications |
| F4 | `app-console-content` | Editorial — proofread, draft, verify |
| F5 | `app-console-minutebook` | Governance — minutes, resolutions |
| F6 | `app-console-bookkeeper` | Financial ledger |
| F7 | `app-console-bim` | Building information management |
| F8 | `app-console-gis` | Geographic information |
| F9 | `app-console-slm` | AI management and adapter marketplace |
| F10 | `app-console-mesh` | Network mesh management |
| F11 | `app-console-system` | Live `os-*` service health and pairing status |
| F12 | `app-console-input` | The Anchor — Input Machine (SYS-ADR-10) |

## The status bar

The `app-console-keys` status bar is always visible at the bottom of the console and provides the operator with a live situational picture:

```
jennifer@woodfine | MBA LINK ACTIVE | F4: Content | Tier A | 00:04:23
```

The identity component shows the username and tenant set during the pairing ceremony. The authorization state shows `MBA LINK ACTIVE`, `MBA LINK INACTIVE <reason>`, or `MBA LINK PENDING`. The active cartridge slot name, the SLM tier in use (A for local, B for cloud burst, C for frontier API), and session duration complete the bar.

## Authorization connectivity

`app-console-keys` maintains outbound connections to paired `os-*` services. Each pairing is independent: the console can be active with `os-totebox` and inactive with `os-privategit` simultaneously.

When the authorization link is inactive, os-console operates in local-only mode. Locally-cached content remains accessible. Backend service requests to `service-proofreader`, `service-input`, and `service-content` fail gracefully rather than crashing.

## PDF rendering

`os-console` supports in-terminal PDF rendering using the `pdfium-render` library — Rust bindings to Chromium's pdfium. PDF pages are rendered to RGB bitmaps and displayed using the Kitty graphics protocol as the primary path, with Sixel as a fallback and an error for terminals that support neither. This is pixel rendering, not text extraction.

## Three-Ring Architecture placement

`os-console` is a client of the [[three-ring-architecture|Three-Ring Architecture]], not a ring itself. It connects to Ring 1 services through the authorization layer — `service-input` via F12, [[service-people|`service-people`]] via F2, [[service-email|`service-email`]] via F3, and `service-fs`; to Ring 2 services including [[service-content|`service-content`]] and [[service-search|`service-search`]]; and to the Ring 3 service [[service-slm|`service-slm`]] via [[compounding-doorman|Doorman]] at `http://localhost:8011`. `os-console` is the human interface through which an operator instructs the rings.

## See also

- [[console-os]] — architectural overview of os-console as Command Ledger
- [[machine-based-auth]] — the authorization mechanism os-console uses
- [[input-machine]] — The Anchor; mandatory ingest gate at F12
- [[three-ring-architecture]] — the Ring 1/2/3 architecture os-console connects to
- [[os-family-overview]] — the eight-OS family and how os-console fits
- [[compounding-doorman]] — the Doorman audit boundary for service-slm access
