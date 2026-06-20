---
schema: foundry-doc-v1
content_type: topic
title: "OS Console Architecture"
slug: topic-os-console-architecture
aliases:
  - topic-os-console-architecture
short_description: "The OS Console is a terminal-native operator interface for Totebox sessions, built on a chassis-and-cartridge model where each panel attaches at a function-key slot."
category: architecture
type: reference
quality: complete
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-06-20
editor: pointsav-engineering
paired_with: topic-os-console-architecture.es.md
cites: []
---

# OS Console Architecture

The OS Console is a terminal-native operator interface for Totebox sessions. It presents
a multi-surface panel system driven by function keys, where each panel is implemented as
an independent `Cartridge` that attaches to the console chassis at a designated F-key
slot.

## Chassis and Cartridge Model

`app-console-keys` provides the chassis: a ratatui-based TUI skeleton that owns the
terminal lifecycle, event loop, and Kitty/Sixel graphics rendering pipeline. The chassis
exposes the `Cartridge` trait, which every panel crate implements:

```rust
pub trait Cartridge {
    fn title(&self) -> &str;
    fn render(&self, frame: &mut Frame, area: Rect);
    fn handle_event(&mut self, event: &Event) -> CartridgeAction;
}
```

At runtime the chassis loads exactly one active `Cartridge` at a time. The operator
switches panels via function keys. The chassis handles QR code generation (Ed25519 key
fingerprints rendered as Kitty/Sixel inline images) independent of panel content.

## Active Panels

### F3 — Email (`app-console-email`)

`EmailCartridge` connects to Exchange Web Services (EWS) via the `service-email` backend.
It presents three views:

- Inbox list — threaded message summaries with unread counts
- Read — full message body with attachment indicators
- Compose/send — plain-text composition with `To:` and `Subject:` fields

Plain mode (no Kitty/Sixel) is supported for terminals that lack graphics protocol
support.

### F9 — SLM (`app-console-slm`)

`SlmCartridge` renders a live health dashboard for the local inference gateway. It polls
the gateway health endpoint every 10 seconds and displays:

- Tier A/B/C availability and circuit-breaker state
- Entity count from the local data store
- Corpus queue depth and daily cost summary

The operator may force a manual refresh with `R`.

### F11 — System (`app-console-system`)

`SystemCartridge` provides the operator panel for Totebox session management. Its primary
function in the current phase is displaying pending-pair approvals: staging sessions
awaiting Command Session sign-off before a commit is promoted.

## Terminal Capabilities

The console detects terminal capabilities at startup:

| Feature | Detection method |
|---|---|
| Kitty graphics protocol | `TERM` / `TERM_PROGRAM` environment variables |
| Sixel fallback | `$COLORTERM` and terminal capability query |
| Plain mode | Explicit `--plain` flag or capability absent |

QR code rendering (used by `app-console-keys` for key fingerprint display) uses Kitty
inline image protocol when available and falls back to ratatui block-character rendering
otherwise.

## Workspace Membership

The console crates that are active workspace members:

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

## See Also

- [[topic-os-console-totebox-browser|os-console: The Totebox Orchestration Browser]] —
  the Totebox-native browser surface within the console
- [[topic-ppn-small-business-compute|PPN Small-Business Compute]] — fleet management
  surface accessible through the operator panel
- [[topic-software-distribution-substrate|Software Distribution Substrate]] — the
  licensing layer that gates deployment of console binaries

---

*Woodfine Capital Projects™, MCorp™, PointSav Digital Systems™, Totebox Orchestration™, Totebox Archive™, and Capability Geometry™ are trademarks of Woodfine Capital Projects Inc., used in Canada, the United States, Latin America, and Europe. All other trademarks are the property of their respective owners.*
