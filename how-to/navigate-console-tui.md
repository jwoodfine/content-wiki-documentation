---
schema: foundry-doc-v1
title: "How to navigate the console TUI"
slug: navigate-console-tui
category: how-to
content_type: how-to
type: how-to
status: active
last_edited: 2026-06-14
editor: pointsav-engineering
paired_with: navigate-console-tui.es.md
---

`os-console` is a full-screen terminal application that organises platform functions into numbered F-key slots. Navigating the console means switching between slots, reading the status bar, and understanding what the active slot is showing you. No mouse is required — the keyboard model is complete.

For the architecture behind this model, see [[app-console-keys]] and [[os-console-platform]].

## Prerequisites

- A paired device (see [[pair-a-new-device]])
- `os-console` installed and launched
- An active session (see [[open-first-totebox-session]])

## Layout

The console occupies the full terminal window with three persistent regions:

| Region | Location | Contents |
|---|---|---|
| Status bar | Top of screen | Identity label, authorization state, active slot name, SLM tier, session duration |
| Slot area | Main body | Output from whichever slot is currently active |
| Navigation strip | Bottom of screen | F-key labels showing which slots are loaded |

The navigation strip displays the slot names bound to each F-key. Unloaded slots appear dimmed.

## Switching slots with F-keys

Press any labelled F-key to activate that slot. The slot area updates immediately. The active slot name in the status bar confirms which slot is live.

Loaded slots hold their state when you switch away — an email inbox you scrolled to a particular message stays at that position when you return to F3.

## Reading the status bar

The status bar updates continuously. Left to right:

- **Identity** — the paired device identity and its permission tier
- **Auth state** — `LINKED` when machine-based authorization is active; `LINK INACTIVE` when unavailable
- **Active slot** — the name of the currently displayed cartridge (e.g., `INPUT`, `EMAIL`, `SLM`)
- **SLM tier** — the Doorman circuit state: `A` (DataGraph live), `B` (SLM only), or `C` (local fallback)
- **Session duration** — elapsed time since the session was opened

## Key bindings that work in every slot

| Key | Action |
|---|---|
| F1–F12 | Switch to that slot |
| ? | Show contextual help for the active slot |
| q or Esc | Exit the active slot back to the home view (slot-dependent) |
| Ctrl-C | Quit `os-console` |

Slot-specific bindings are shown in the navigation strip of the active slot.

## Key takeaways

- Navigation is entirely keyboard-driven — F-key number = slot number
- Slots hold their state; switching away and back is non-destructive
- The status bar is the ground truth for authorization state and SLM availability
- F12 is the Input Machine; it is always present and cannot be reassigned

## See also

- [[app-console-keys]] — the chassis and Cartridge trait that all slots implement
- [[os-console-platform]] — the full F-key taxonomy and which cartridge occupies each slot
- [[use-f-key-model]] — how to work with the F-key cartridge model
- [[machine-based-auth]] — what the `LINKED`/`LINK INACTIVE` auth state means
- [[pair-a-new-device]] — register a device before opening the console
