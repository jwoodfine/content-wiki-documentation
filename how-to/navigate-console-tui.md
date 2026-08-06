---
schema: foundry-doc-v1
title: "Navigate the console TUI"
slug: navigate-console-tui
short_description: "Navigates os-console by keyboard — the F-key strip at the top, the status bar's real fields at the bottom, and switching slots without losing state."
category: how-to
content_type: how-to
type: how-to
quality: complete
status: active
audience: "Engineers (hands on keyboard); customer operators"
last_edited: 2026-08-06
editor: pointsav-engineering
paired_with: navigate-console-tui.es.md
research_trail:
  sources: [pointsav-monorepo app-console-keys (chassis layout, status bar widget, F-key strip widget)]
  verification_method: "independently source-verified against pointsav-monorepo on 2026-08-06 by reading the Rust source directly, with file:line citations recorded per claim; corrected the guide's own prior layout error (status bar and F-key strip positions were reversed) and its status bar field claims, both against the actual chassis render function"
---

## Prerequisites

- A paired device (see [[pair-a-new-device]])
- `os-console` installed and launched
- An active session (see [[open-first-totebox-session]])

## Purpose

Learn the console's real screen layout and status bar fields well enough to navigate confidently — a few minutes, and it stays accurate for every cartridge you'll use later.

## Procedure

1. Launch `os-console` and observe the three fixed regions, top to bottom: a one-row F-key strip, the active cartridge's content filling the rest of the screen, and a one-row status bar at the very bottom.

2. Read the F-key strip. It shows a label for every F-key slot, with the currently active one highlighted and unloaded slots dimmed.

3. Read the status bar. Left to right: your identity as `username@tenant`; the Machine-Based Authorization link state (`MBA LINK ACTIVE`, `MBA LINK INACTIVE: <reason>`, or `MBA LINK PENDING`); the active slot's full label (e.g. `F9: SLM`, not a bare number); and elapsed session time. A `[N pending]` badge appears only when you have pending pairing requests.

   > **Note:** there is no SLM-tier indicator in the status bar. Inference tier and circuit state are shown inside the F9 dashboard itself, not in the persistent status bar.

4. Press any F-key to switch to that slot. The content area updates immediately, and the F-key strip's highlight and the status bar's active-slot field both confirm which slot is live.

5. Switch away from a slot and back. Cartridges hold their own state — a document you were editing or a dashboard you were viewing is exactly as you left it.

6. Check each cartridge's own hint line for its specific key bindings. They aren't universal — F9's dashboard responds to **R** (refresh) and **?** (help), for example, but a different cartridge's bindings are its own and shown in its own interface, not in a shared reference table.

## Expected outcome

You can read every field in the status bar correctly, switch between loaded F-key slots without losing a cartridge's state, and know to check each cartridge's own hint line for bindings specific to it.

## Verification

Switch to at least two different loaded slots and confirm both the F-key strip's highlighted label and the status bar's active-slot field update to match each time.

## Rollback

Navigation has no state to roll back — switching slots or exiting the console changes nothing persistent by itself. If a cartridge's own action does write something (submitting input at F12, for example), that cartridge's own guide covers its own rollback.

## Next steps

- [[use-f-key-model]] — what each default cartridge actually does, corrected against real source
- [[explore-the-console]] — a guided first tour combining layout, F9, and F12

## See also

- [[app-console-keys]] — the chassis, the Cartridge trait, and the status bar's implementation
- [[machine-based-auth]] — what the MBA link states mean
- [[pair-a-new-device]] — register a device before opening the console
