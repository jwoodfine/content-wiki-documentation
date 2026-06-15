---
schema: foundry-doc-v1
title: "How to use the F-key cartridge model"
slug: use-f-key-model
category: how-to
content_type: how-to
type: how-to
status: active
last_edited: 2026-06-14
editor: pointsav-engineering
paired_with: use-f-key-model.es.md
---

The F-key model is the operator interface of `os-console`. Each F-key slot hosts a Cartridge — a self-contained module compiled into the binary that owns its rendering, keyboard handling, and lifecycle. Understanding the slot assignments and how each Cartridge works lets you move efficiently between platform functions without leaving the terminal.

For the Cartridge trait and how slots are compiled in, see [[app-console-keys]]. For navigation fundamentals, see [[navigate-console-tui]].

## Default slot assignments

| F-key | Cartridge | Primary function |
|---|---|---|
| F3 | Email | Read and compose messages; see [[app-console-email]] |
| F9 | SLM | Local inference and Doorman health dashboard; see [[app-console-slm]] |
| F12 | Input Machine | Human-verified record entry; mandatory per SYS-ADR-10; see [[app-console-input]] |

Slots not listed above are reserved or unloaded. A dimmed label in the navigation strip indicates the slot is unloaded in the current session.

## How a Cartridge works

A Cartridge is compiled into the `os-console` binary. It is not a plugin or runtime script. When you press an F-key, the binary hands control to the Cartridge registered for that slot.

Each Cartridge:
- Renders its own full-screen view in the slot area
- Handles keyboard events for that slot
- Reports to the status bar which slot is active
- Connects to the relevant platform service (email, SLM, ledger) using the active MBA connection

A Cartridge that cannot reach its backing service shows a status indicator in the slot area rather than failing silently.

## Using the Email Cartridge (F3)

1. Press **F3** to open the Email Cartridge.
2. The inbox list appears showing unread counts and sender summaries.
3. Navigate with arrow keys; press **Enter** to open a message.
4. Press **c** to compose a new message.

Outbound messages route through `service-email`. Direct SMTP connections are not used — the Cartridge acts as a Comm Diode, applying tenant communication policy before sending.

For detail on the email flow, see [[app-console-email]].

## Using the SLM Cartridge (F9)

1. Press **F9** to open the SLM Cartridge.
2. The Doorman health dashboard shows which inference tier (A, B, or C) is active and the entity count from the DataGraph.
3. Press **R** to manually refresh the health status.
4. Submit a prompt at the input line. The response streams into the slot area.

All inference requests route through Doorman. No prompt data leaves the operator's hardware.

For the inference architecture, see [[app-console-slm]] and [[doorman-protocol]].

## Using the Input Machine (F12)

The F12 slot is the human-in-the-loop gate required by SYS-ADR-10. It is the only path through which an operator-verified record can enter the WORM ledger.

1. Press **F12** to open the Input Machine.
2. Review the record or document displayed for verification.
3. Confirm or reject using the labelled key bindings shown in the navigation strip.

A confirmed record is written to the ledger immediately. A rejected record is routed to quarantine.

For the design rationale, see [[app-console-input]] and [[worm-ledger-architecture]].

## Key takeaways

- Each slot is compiled in at build time — there is no plugin runtime or slot hot-swap
- A Cartridge that loses its backing service degrades gracefully and shows a status indicator
- F12 cannot be reassigned; it is structurally the human-verification gate for the ledger
- The Comm Diode model in F3 means email routing applies tenant policy — you cannot bypass it from within the Cartridge

## See also

- [[app-console-keys]] — chassis architecture, Cartridge trait, status bar components
- [[app-console-email]] — Email Cartridge: inbox, reading, compose, and plain-text mode
- [[app-console-slm]] — SLM Cartridge: Doorman dashboard and local inference
- [[app-console-input]] — Input Machine: the F12 human-verification gate
- [[navigate-console-tui]] — overall TUI layout and slot navigation
- [[worm-ledger-architecture]] — the ledger that F12 writes into
