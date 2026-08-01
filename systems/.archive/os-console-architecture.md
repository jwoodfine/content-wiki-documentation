---
schema: foundry-doc-v1
title: "os-console Internal Architecture"
slug: os-console-architecture
aliases:
  - topic-os-console-architecture
category: systems
type: topic
content_type: topic
quality: complete
status: archived
archived: 2026-07-31
archived_reason: "Genuine content fragmentation with console-os.md and os-console-platform.md — all three described the same product (os-console) at overlapping technical depths, with real inconsistencies (differing F-key/cartridge-state tables — this article's own 'four active' claim was incomplete against the platform's project registry). Merged into one canonical systems/os-console.md."
superseded_by: os-console
audience: vendor-public
bcsc_class: current-fact
language_protocol: PROSE-TOPIC
last_edited: 2026-07-09
editor: pointsav-engineering
paired_with: os-console-architecture.es.md
short_description: "os-console hosts multiple independent TUI workspaces — cartridges — in a unified keyboard-navigation chassis: the Cartridge trait, capability negotiation, OSC 8 hyperlinks."
cites: []
---

`os-console` is a single compiled Rust binary that hosts multiple independent TUI
workspaces — cartridges — within a unified keyboard-navigation framework. This article
describes the internal design of that framework: how cartridges are defined, how the
chassis dispatches events, how terminal capabilities are negotiated, and how cartridges
communicate UI-layer linking intent back to the terminal.

## The Cartridge trait

Every `app-console-*` crate exposes exactly one type that implements the `Cartridge`
trait, defined in `app-console-keys`. The trait is the only interface between a cartridge
and the chassis — there are no other public APIs:

```
trait Cartridge {
    fn fkey(&self) -> FKey;
    fn title(&self) -> &str;
    fn tick(&mut self);
    fn render(&mut self, frame, area);
    fn handle_event(&mut self, event) -> CartridgeAction;
    fn set_graphics_caps(&mut self, kitty, sixel, font_size, truecolor);
    fn flush_hyperlinks(&mut self, writer);
}
```

`tick()` and `render()` are called on every iteration of the event loop. `handle_event()`
is called only when a keyboard or mouse event arrives. `set_graphics_caps()` is called
once at startup, after the chassis queries the connected terminal for its capabilities.
`flush_hyperlinks()` is called after each `render()` call, allowing cartridges to emit
buffered OSC 8 hyperlink sequences into the terminal output stream. Both
`set_graphics_caps()` and `flush_hyperlinks()` have default no-op implementations in the
trait, so cartridges that do not use graphics or hyperlinks incur no additional code.

## Cartridge registration

Cartridges are registered at startup via `chassis.register(Box<dyn Cartridge>)`.
Registration is order-independent with respect to rendering, but the order determines
tab-strip presentation when [[use-f-key-model|F-key slots]] are not unique. Each registered cartridge must
claim a distinct `FKey` slot.

The default build registers six cartridges:

| F-key | Cartridge | Connects to |
|---|---|---|
| F2 | `app-console-people` | `service-people` |
| F3 | `app-console-email` | `service-email` |
| F4 | `app-console-content` | `service-content`, `service-slm` |
| F9 | `app-console-slm` | Doorman / `service-slm` |
| F11 | `app-console-system` | pairing server |
| F12 | `app-console-input` | ingest service |

The F12 cartridge (`app-console-input`) is mandatory in every deployment. It is the ingest gate through which all operator-sourced text must pass before entering the platform's data layer. Omitting it is a build constraint violation.

## Active panels (current deployment)

Of the six default-build cartridges, four are active workspace members today. Their
current functional scope:

- **F3 — Email (`app-console-email`).** `EmailCartridge` connects to Exchange Web
  Services (EWS) via the `service-email` backend and presents three views: an inbox
  list (threaded message summaries with unread counts), a read view (full message
  body with attachment indicators), and compose/send (plain-text composition with
  `To:` and `Subject:` fields). Plain mode (no Kitty/Sixel) is supported for terminals
  that lack graphics protocol support.
- **F9 — SLM (`app-console-slm`).** `SlmCartridge` renders a live health dashboard for
  the [[doorman-protocol|local inference gateway]], polling the gateway health endpoint
  every 10 seconds and displaying Tier A/B/C availability and circuit-breaker state,
  entity count from the local data store, and corpus queue depth with daily cost
  summary. The operator can force a manual refresh with `R`.
- **F11 — System (`app-console-system`).** `SystemCartridge` provides the operator
  panel for Totebox session management. Its primary function in the current phase is
  displaying pending-pair approvals — staging sessions awaiting Command Session
  sign-off before a commit is promoted.

| Crate | State | Notes |
|---|---|---|
| `app-console-keys` | Active | Chassis |
| `app-console-email` | Active | EmailCartridge |
| `app-console-slm` | Active | SlmCartridge |
| `app-console-system` | Active | SystemCartridge |

Additional console surfaces (`app-console-bim`, `app-console-bookkeeper`,
`app-console-content`, `app-console-input`, `app-console-mesh`,
`app-console-minutebook`, `app-console-people`, `app-console-vault`) are at
Reserved-folder or Scaffold-coded state and are not workspace members.

## Terminal capability negotiation

At startup, the chassis queries the connected terminal using standard escape sequences
and environment inspection:

- **Kitty graphics protocol:** detected via APC response to a probe sequence.
- **Sixel:** detected via `TERM` environment and DA2 device attributes.
- **Font cell size:** queried via xtwinops (CSI 16 t) when available; falls back to a
  10×20 px estimate.
- **Truecolor:** detected via `COLORTERM=truecolor` or `COLORTERM=24bit`.

The resolved capabilities are passed to every registered cartridge via
`set_graphics_caps(kitty, sixel, font_size, truecolor)`. Cartridges use this to select
between 24-bit RGB colours and the named eight-colour fallback palette. The chassis never
calls `set_graphics_caps()` again after initial negotiation — capabilities are fixed for
the session lifetime.

### Truecolor colour conventions

When truecolor is available, cartridges use a consistent colour set:

- Accent (borders, highlights): `Rgb(32, 178, 170)` — a teal close to CSS LightSeaGreen.
- Selection background: `Rgb(0, 95, 135)` — a dark teal-blue.
- Danger / error: `Rgb(200, 0, 0)` — deep red.

When truecolor is unavailable — plain terminals, serial consoles — cartridges fall back
to named colours: Cyan for accents, DarkGray for selection backgrounds, Red for errors.
The visual hierarchy is preserved; only the precision changes.

## OSC 8 hyperlinks

`ContentCartridge` (F4) implements `flush_hyperlinks()`. During `render()`, it collects
URL targets from search results and citations into an internal buffer. After the ratatui
draw cycle completes, the chassis calls `flush_hyperlinks()`, which emits OSC 8
sequences:

```
OSC 8 ; params ; uri ST   (open link)
OSC 8 ; ; ST              (close link)
```

Links are only emitted when the Kitty graphics protocol is active — terminals that support
Kitty graphics also support OSC 8 reliably. The default `flush_hyperlinks()` no-op in
the trait means non-participating cartridges incur no overhead.

## Customer-rooted deployment intent

All default service endpoints in the console's configuration resolve to localhost
addresses. The binary is operable without a configuration file, and it has no hard
dependency on any external network. The intent is that `os-console` starts and renders
fully on a machine that has no outbound internet access, connecting only to services
running on the same node or within the same [[ppn-mesh-architecture|PPN mesh]].

## See also

- [[ppn-small-business-compute]] — the network substrate os-console connects into
- [[architecture-decisions]] — architectural decisions governing the platform data layer
