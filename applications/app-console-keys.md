---
schema: foundry-doc-v1
title: "app-console-keys — console chassis and F-key framework"
slug: app-console-keys
category: applications
type: app
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-06-14
editor: pointsav-engineering
paired_with: app-console-keys.es.md
short_description: "app-console-keys is the always-installed base chassis of os-console. It provides the Cartridge trait that all console modules implement, the F-key navigation strip, the status bar, and the machine-based authorization client."
cites: []
---

`app-console-keys` is the always-installed base chassis of [[console-os|os-console]]. All other console modules — email, content, SLM monitoring, and the rest — are optional cartridges that plug into the framework `app-console-keys` defines. The module is mandatory: an `os-console` binary built without it will not compile.

**Naming note:** "keys" in `app-console-keys` refers to keyboard function keys — the F1 through F12 strip that navigates between cartridge slots. It does not refer to cryptographic keys. Cryptographic pairing and machine-based authorization are implemented by `system-gateway-mba`, a separate crate.

## The Cartridge trait

`app-console-keys` defines the `Cartridge` trait — the interface every `app-console-*` module must implement. The trait is minimal: a module declares which F-key slot it occupies, what to render when that slot is active, and how to handle keyboard input while active. The chassis handles everything else: slot registration, input dispatch, focus management, and the status bar.

Because cartridges are compiled directly into the `os-console` binary rather than loaded at runtime, the trait is a compile-time contract. A module that fails to implement it produces a build error, not a runtime failure.

## The F-key navigation strip

The primary interface element managed by `app-console-keys` is the horizontal F-key tab strip at the top of the console. The strip shows one slot per registered cartridge. The active slot is highlighted; inactive slots are greyed when not installed.

The strip does not re-order slots at runtime. Each cartridge's slot position is fixed at the F-key number it claims. [[app-console-input]] is permanently fixed at F12 per [[architecture-decisions|SYS-ADR-10]].

## The status bar

The `app-console-keys` status bar runs along the bottom of the console and is always visible, regardless of which cartridge slot is active. It displays:

| Component | Content |
|---|---|
| Identity | Username and tenant set during the pairing ceremony |
| Authorization state | `MBA LINK ACTIVE`, `MBA LINK INACTIVE <reason>`, or `MBA LINK PENDING` |
| Active slot | Name of the currently focused cartridge |
| SLM tier | `Tier A` (local), `Tier B` (cloud burst), or `Tier C` (frontier API) |
| Session duration | Elapsed time since console start |

The tier indicator reflects the last routing decision made by the inference gateway. It does not poll the gateway — it updates when a request is routed.

## Authorization client

`app-console-keys` maintains the outbound [[machine-based-auth|machine-based authorization]] connections to paired `os-*` services. Each pairing is independent: the console can hold an active link to `os-totebox` while the link to `os-privategit` is inactive.

When an authorization link is inactive, the affected cartridge degrades gracefully. Locally cached content remains accessible; backend requests fail with an explicit status rather than silently. No cartridge crashes the chassis when its backend is unreachable.

## Configuration

Profile-based configuration is stored at `~/.config/os-console/config.toml`. The configuration file controls which backend services the console attempts to pair with at startup, display preferences, and the SSH server port (if the SSH server feature is compiled in).

## PDF rendering and graphics support

`app-console-keys` provides the graphics infrastructure used by cartridges that render images or PDFs. PDF pages are rendered to RGB bitmaps using the `pdfium-render` library. The display path uses the Kitty graphics protocol as the primary path, with Sixel encoding as a fallback, and an error message for terminal environments that support neither.

## See also

- [[console-os]] — the os-console product overview, including the F-key surface and operating modes
- [[os-console-platform]] — the complete cartridge architecture and F-key map
- [[app-console-input]] — the F12 mandatory input gate; always compiled alongside app-console-keys
- [[machine-based-auth]] — the authorization mechanism the chassis client manages
- [[three-ring-architecture]] — the Ring 1/2/3 architecture the authorization client connects to
