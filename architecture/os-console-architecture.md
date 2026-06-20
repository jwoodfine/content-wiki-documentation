---
schema: foundry-doc-v1
title: "os-console Internal Architecture"
slug: os-console-architecture
category: architecture
type: topic
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: current-fact
language_protocol: PROSE-TOPIC
last_edited: 2026-06-13
editor: pointsav-engineering
paired_with: os-console-architecture.es.md
short_description: "os-console hosts multiple independent TUI workspaces — cartridges — within a unified keyboard-navigation chassis. This article covers the Cartridge trait, capability negotiation, and the OSC 8 hyperlink protocol."
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
tab-strip presentation when F-key slots are not unique. Each registered cartridge must
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

## Sovereign deployment intent

All default service endpoints in the console's configuration resolve to localhost
addresses. The binary is operable without a configuration file, and it has no hard
dependency on any external network. The intent is that `os-console` starts and renders
fully on a machine that has no outbound internet access, connecting only to services
running on the same node or within the same PPN mesh.

## See also

- [[ppn-small-business-compute]] — the network substrate os-console connects into
- [[architecture-decisions]] — architectural decisions governing the platform data layer
