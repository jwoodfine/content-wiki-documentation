---
schema: foundry-doc-v1
title: "os-console"
slug: os-console
category: systems
type: concept
content_type: topic
quality: complete
index_group: operator-surfaces
status: active
audience: vendor-public
bcsc_class: current-fact
language_protocol: PROSE-TOPIC
last_edited: 2026-08-22
editor: pointsav-engineering
paired_with: os-console.es.md
aliases: [console-os, os-console-architecture, os-console-platform, topic-os-console-architecture]
cites: []
references:
  - id: 1
    text: "Green, C. 'Improved Alpha-Tested Magnification for Vector Textures and Special Effects.' ACM SIGGRAPH 2007 courses, 2007."
    url: "https://dl.acm.org/doi/10.1145/1281500.1281665"
short_description: "os-console is the human-facing surface of the PointSav platform — a single-binary, keyboard-native Command Ledger that connects to a Totebox and hosts independent TUI cartridges through a unified chassis."
---

`os-console` is the human-facing surface of the PointSav platform — a Command Ledger that connects to one [[totebox-os|Totebox]] and renders its state to the operator. It does not store data and does not run services; it is a high-fidelity terminal purpose-built around keyboard-driven operator flow. The reference point is the professional financial terminal: a single keyboard, a small set of function keys, and a relentless focus on the operator's context. The binary is written from scratch in Rust for sub-50-millisecond cold start and a 15-megabyte footprint.

`os-console` is a single compiled Rust binary that hosts multiple independent TUI workspaces — cartridges — within a unified keyboard-navigation framework. The design principle is end-to-end ownership: every component is compiled into a single binary, with no dynamic plugin loading, no subprocess launching, and no nesting.

## Key takeaways

- `os-console` ships today as a `ratatui`/`crossterm` terminal application, not the seL4-isolated or GPU-native rendering pipeline described in its roadmap — those are planned, not current. Reserve "kernel-enforced" and similar claims for that future state.
- Cartridges are compiled directly into the binary — not loaded dynamically, not launched as subprocesses. `app-console-keys` (the chassis) and `app-console-input` (F12) are the only mandatory cartridges; everything else is optional.
- `os-console`'s own startup code registers 7 cartridges today: people, email, content, search, slm, system, and input (F12, mandatory). Several other `app-console-*` directories exist on disk but have no working implementation behind them yet — see the F-key map below for which.
- Both modes (Direct and Aggregate) use the same binary; the aggregator does not require a different Console.
- All default service endpoints resolve to localhost addresses — the binary is operable without a configuration file and has no hard dependency on any external network.

## How it runs

`os-console` ships as a single executable and runs today as a standard terminal application, built on `ratatui` and `crossterm`. **Planned, not current**: a hardware-isolated runtime where the host operating system's native virtualisation API (Windows Hypervisor Platform, `Hypervisor.framework`, or KVM) boots a small, isolated [[sel4-microkernel-substrate|seL4]] environment around the application. This is roadmap work, not a description of the binary as it ships today.

The security model relies on [[machine-based-auth|hardware-bound pairings]] rather than usernames or passwords, independent of the VM-isolation roadmap item above.

Platform targets include Linux Mint on the on-premises workstation and macOS 13 or later on executive workstations. An optional SSH server mode, compiled with the `--features ssh-server` flag, enables remote access for use on a GCE VM. In this remote-PTY configuration the process emitting pixels and the terminal decoding them are on different machines, so the Kitty and Sixel graphics pipeline is disabled. The planned direction is host-native deployment — the binary runs on the operator's own machine in a local graphics-capable terminal, connecting to a remote Totebox Archive over the internet via [[machine-based-auth|machine-based authorization]].

## The rendering stack

`os-console` today is a terminal interface: widget logic and rendering are built on `ratatui`, with `crossterm` handling the terminal backend. **Planned, not current**: a standalone, GPU-native rendering pipeline (a WGPU-based Vulkan/Metal/DX12 abstraction with a Signed Distance Field[^1] glyph renderer for infinite-zoom fidelity, variable-weight headers, and bloom effects) that would replace the terminal-hosted renderer entirely. The design intent for that future pipeline shares its philosophy with [[design-philosophy|the broader PointSav design system]], but it is not the stack running today.

## The base chassis: app-console-keys

`app-console-keys` is the always-installed base chassis inside `os-console`. Its relationship to `os-console` is analogous to [[service-fs|`service-fs`]]'s relationship to `os-totebox`: it is the minimum required component that must be present; everything else is optional. It provides the `Cartridge` trait, the F-key navigation framework (the horizontal tab strip, F-key input dispatch, and active-cartridge routing), the status bar showing [[machine-based-auth|machine-based authorization]] connection state and session identity, the authorization client that manages connections to paired `os-*` services, and profile-based configuration stored at `~/.config/os-console/config.toml`.

**Naming note:** "keys" in `app-console-keys` refers to F-keys — keyboard function keys, not cryptographic keys. Machine-based authorization is implemented by `system-gateway-mba`, a separate crate.

## The Cartridge trait

Every `app-console-*` crate exposes exactly one type that implements the `Cartridge` trait, defined in `app-console-keys`. The trait is the only interface between a cartridge and the chassis — there are no other public APIs:

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

`tick()` and `render()` are called on every iteration of the event loop. `handle_event()` is called only when a keyboard or mouse event arrives. `set_graphics_caps()` is called once at startup, after the chassis queries the connected terminal for its capabilities. `flush_hyperlinks()` is called after each `render()` call, allowing cartridges to emit buffered OSC 8 hyperlink sequences into the terminal output stream. Both `set_graphics_caps()` and `flush_hyperlinks()` have default no-op implementations in the trait, so cartridges that do not use graphics or hyperlinks incur no additional code.

Cartridges are registered at startup via `chassis.register(Box<dyn Cartridge>)`. Registration is order-independent with respect to rendering, but the order determines tab-strip presentation when F-key slots are not unique. Each registered cartridge must claim a distinct `FKey` slot. A cartridge that is not installed has its F-key slot greyed in the tab strip. Cartridges are optional except for `app-console-keys` and `app-console-input` (F12) — an installation that includes only `app-console-content` (F4) and `app-console-input` (F12) is a complete, valid os-console deployment for editorial work.

## The F-key map

The console presents twelve addressable slots via F-keys. F12 is fixed as The Anchor — the [[input-machine|Input Machine]] — and is never moved. F12 is mandatory per [[architecture-decisions|SYS-ADR-10]]: it is the only surface through which raw external files can enter a Totebox. Files submitted through F12 are read once, deduplicated by content hash, tagged with a coarse routing label, and forwarded to `service-fs` — see [[input-machine|the Input Machine article]] for the exact mechanism.

Seven cartridges are registered in `os-console`'s own startup code today; the rest are unclaimed slots with no working implementation behind them.

| F-key | Cartridge | Domain | State |
|---|---|---|---|
| F1 | — | Help overlay | Unclaimed — `app-console-help` has no source files |
| F2 | `app-console-people` | Identity and contacts — [[service-people|service-people]] | Registered |
| F3 | `app-console-email` | Communications — [[service-email|service-email]] | Registered |
| F4 | `app-console-content` | Editorial — proofread, draft, verify — [[service-content|service-content]] | Registered |
| F5 | `app-console-search` | Search | Registered |
| F6 | — | Financial ledger | Unclaimed — `app-console-bookkeeper` is two static HTML files, no `Cartridge` implementation, not registered |
| F7 | — | Building information management | Unclaimed — `app-console-bim` has no source files |
| F8 | — | Geographic information | Unclaimed — no crate of this name exists in the monorepo |
| F9 | `app-console-slm` | AI management and adapter marketplace — Doorman / `service-slm` | Registered |
| F10 | — | Network mesh management | Unclaimed — `app-console-mesh` has no source files |
| F11 | `app-console-system` | Live `os-*` service health and pairing status | Registered |
| F12 | `app-console-input` | The Anchor — Input Machine (SYS-ADR-10) | Registered |

State reflects the console's own startup registration calls, not the crate's presence on disk — a directory existing under `app-console-*` does not mean it is wired into the running console. `app-console-vault`, `app-console-exchange`, and `app-console-market` (not F-key-mapped) are also unclaimed; `app-console-minutebook`, once assumed to hold F5, has no source files either.

### Registered cartridges today

- **F2 — People (`app-console-people`).** Identity and contact lookups against `service-people`.
- **F3 — Email (`app-console-email`).** `EmailCartridge` connects to Exchange Web Services (EWS) via the `service-email` backend and presents three views: an inbox list (threaded message summaries with unread counts), a read view (full message body with attachment indicators), and compose/send (plain-text composition with `To:` and `Subject:` fields). Plain mode (no Kitty/Sixel) is supported for terminals that lack graphics protocol support.
- **F4 — Content (`app-console-content`).** Editorial workflow against `service-content`.
- **F5 — Search (`app-console-search`).** Search across the connected Totebox's indexed content.
- **F9 — SLM (`app-console-slm`).** `SlmCartridge` renders a live health dashboard for the [[doorman-protocol|local inference gateway]], polling the gateway health endpoint every 10 seconds and displaying Tier A/B/C availability and circuit-breaker state, entity count from the local data store, and corpus queue depth with daily cost summary. The operator can force a manual refresh with `R`.
- **F11 — System (`app-console-system`).** `SystemCartridge` provides the operator panel for Totebox session management. Its primary function in the current phase is displaying pending-pair approvals — staging sessions awaiting Command Session sign-off before a commit is promoted.
- **F12 — Input (`app-console-input`).** The Anchor; see [[input-machine|Input Machine]] for the full ingest mechanism.

## Terminal capability negotiation

At startup, the chassis queries the connected terminal using standard escape sequences and environment inspection:

- **Kitty graphics protocol:** detected via APC response to a probe sequence.
- **Sixel:** detected via `TERM` environment and DA2 device attributes.
- **Font cell size:** queried via xtwinops (CSI 16 t) when available; falls back to a 10×20 px estimate.
- **Truecolor:** detected via `COLORTERM=truecolor` or `COLORTERM=24bit`.

The resolved capabilities are passed to every registered cartridge via `set_graphics_caps(kitty, sixel, font_size, truecolor)`. The chassis never calls `set_graphics_caps()` again after initial negotiation — capabilities are fixed for the session lifetime.

When truecolor is available, cartridges use a consistent colour set: accent (borders, highlights) `Rgb(32, 178, 170)` — a teal close to CSS LightSeaGreen; selection background `Rgb(0, 95, 135)` — a dark teal-blue; danger/error `Rgb(200, 0, 0)` — deep red. When truecolor is unavailable — plain terminals, serial consoles — cartridges fall back to named colours: Cyan for accents, DarkGray for selection backgrounds, Red for errors. The visual hierarchy is preserved; only the precision changes.

`ContentCartridge` (F4) implements `flush_hyperlinks()`. During `render()`, it collects URL targets from search results and citations into an internal buffer. After the ratatui draw cycle completes, the chassis calls `flush_hyperlinks()`, which emits OSC 8 sequences (`OSC 8 ; params ; uri ST` to open a link, `OSC 8 ; ; ST` to close it). Links are only emitted when the Kitty graphics protocol is active — terminals that support Kitty graphics also support OSC 8 reliably.

## The status bar

The `app-console-keys` status bar is always visible at the bottom of the console and provides the operator with a live situational picture:

```
operator@woodfine | MBA LINK ACTIVE | F4: Content | Tier A | 00:04:23
```

The identity component shows the username and tenant set during the pairing ceremony. The authorization state shows `MBA LINK ACTIVE`, `MBA LINK INACTIVE <reason>`, or `MBA LINK PENDING`. The active cartridge slot name, the SLM tier in use (A for local, B for cloud burst, C for frontier API), and session duration complete the bar.

## Authorization connectivity

`app-console-keys` maintains outbound connections to paired `os-*` services. Each pairing is independent: the console can be active with `os-totebox` and inactive with `os-privategit` simultaneously. When the authorization link is inactive, `os-console` operates in local-only mode. Locally-cached content remains accessible. Backend service requests to `service-proofreader`, `service-input`, and `service-content` fail gracefully rather than crashing.

## PDF rendering

`os-console` supports in-terminal PDF rendering using the `pdfium-render` library — Rust bindings to Chromium's pdfium. PDF pages are rendered to RGB bitmaps and displayed using the Kitty graphics protocol as the primary path, with Sixel as a fallback and an error for terminals that support neither. This is pixel rendering, not text extraction.

## Placement in the platform architecture

`os-console` is a client of the [[three-ring-architecture|Three-Ring Architecture]], not a ring itself. It connects to Ring 1 services through the authorization layer — `service-input` via F12, [[service-people|`service-people`]] via F2, [[service-email|`service-email`]] via F3, and [[service-fs|`service-fs`]]; to Ring 2 services including [[service-content|`service-content`]] and [[service-search|`service-search`]]; and to the Ring 3 service [[service-slm|`service-slm`]] via [[compounding-doorman|Doorman]]. `os-console` is the human interface through which an operator instructs the rings.

All default service endpoints in the console's configuration resolve to localhost addresses. The binary is operable without a configuration file, and it has no hard dependency on any external network. The intent is that `os-console` starts and renders fully on a machine that has no outbound internet access, connecting only to services running on the same node or within the same [[ppn-mesh-architecture|PPN mesh]].

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
- [[os-family-overview]] — the OS family and how os-console fits among them
- [[deployment-patterns]] — how os-console appears in each of the six canonical deployment configurations
- [[machine-based-auth]] — the authorization mechanism os-console uses
- [[input-machine]] — The Anchor; mandatory ingest gate at F12
- [[three-ring-architecture]] — the Ring 1/2/3 architecture os-console connects to
- [[compounding-doorman]] — the Doorman audit boundary for service-slm access
- [[os-console-totebox-browser]] — the browser-analogy explainer for os-console's design philosophy
- [[ppn-small-business-compute]] — the network substrate os-console connects into
- [[architecture-decisions]] — architectural decisions governing the platform data layer
