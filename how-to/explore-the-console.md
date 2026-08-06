---
schema: foundry-doc-v1
title: "Explore the console for the first time"
slug: explore-the-console
short_description: "Orients a first-time operator to os-console — the status bar, the F9 inference-gateway dashboard, and the mandatory F12 input checkpoint that writes to the WORM ledger."
category: how-to
content_type: how-to
type: how-to
quality: complete
status: active
audience: "Engineers (hands on keyboard); customer operators"
last_edited: 2026-08-06
editor: pointsav-engineering
paired_with: explore-the-console.es.md
research_trail:
  sources: [pointsav-monorepo app-console-keys (status bar, F-key labels, chassis), app-console-slm (F9 SlmCartridge, health polling, refresh), app-console-input (F12 InputMachine cartridge, SYS-ADR-10), service-slm/slm-core (Tier A/B/C definitions), service-input + service-fs (the real WORM append chain), DOCTRINE.md + conventions/multi-agent-protocol.md (SYS-ADR-10 citation), infrastructure/systemd/console (deployment unit)]
  verification_method: "independently source-verified against pointsav-monorepo on 2026-08-06 by reading the Rust source directly, with file:line citations recorded per claim; corrected the guide's own prior tier-semantics error (A/B/C are not DataGraph/SLM-local/fallback), removed an invented F12 outcome-labeling scheme borrowed from an unrelated subsystem, fixed a wrong systemd unit name, and removed an unverifiable minimum-terminal-size claim"
---

## Prerequisites

- A paired device (see [[pair-a-new-device]])
- The `os-console` binary available in your PATH, or built locally from `os-console/`
- A terminal emulator — 24-bit color and the Kitty or Sixel graphics protocol are used when available and improve the display, but the console degrades gracefully to named colors and text-only rendering without them

## Purpose

Get oriented to `os-console` for the first time: the status bar's live situational picture, the F9 inference-gateway health dashboard, and the F12 input checkpoint every platform-state change passes through — before you start a real task.

## Procedure

1. Launch the console from the command line:

   ```
   os-console
   ```

2. Read the status bar at the bottom of the screen. It shows, left to right: your identity as `username@tenant`; the Machine-Based Authorization link state (`MBA LINK ACTIVE`, `MBA LINK INACTIVE: <reason>`, or `MBA LINK PENDING`); the active slot, shown as its full label (e.g. `F9: SLM`, not a bare F-key number); and elapsed session time. A `[N pending]` badge appears only when you have pending pairing requests to review.

3. Press **F9** to open the SLM Infrastructure dashboard. It polls the inference gateway every 10 seconds and shows five sections: **Gateway** (Tier A throughput, Tier B circuit state, node class), **YoYo Fleet** (per-node state for cloud GPU burst capacity), **DataGraph** (entity count and its own circuit state — DataGraph is a separate field, not a fourth tier), **Queue** (pending, in-flight, paused, done, quarantine, and poison counts), and **Cost Today**.

   > **Note:** the three inference tiers are Tier A (local model, on this machine), Tier B (Yo-Yo — burst to cloud GPU capacity), and Tier C (external API, narrow-precision tasks against an explicit allowlist). This is not the same three-way split as DataGraph availability, which the dashboard tracks separately.

4. Press **R** to force an immediate refresh of the F9 dashboard rather than waiting for the next 10-second poll. The on-screen hint line confirms the shortcut is live.

5. Press **F12** to open the Input Machine — the platform's mandatory ingestion checkpoint. Every operator input that modifies platform state passes through this slot; it cannot be bypassed by a menu or mouse path.

   > **Warning:** F12 is not a sandbox. A submission here is a real write. If it succeeds, it's appended to the platform's immutable WORM ledger and cannot be retracted — don't submit throwaway content to "just see what happens."

6. Submit a short, genuinely disposable test note if you want to see the flow complete. You'll see one of two outcomes: a confirmation showing a Payload ID and the ledger height/root it was written at (with a warning variant if the submission carried a non-fatal issue), or a plain error panel if the submission failed. There is no separate "quarantine" outcome in this flow — that concept belongs to a different subsystem (the inference queue shown on F9), not to F12.

7. Move between F3, F9, and F12 and confirm the status bar's active-slot label updates to match each time.

## Expected outcome

You can read the status bar's identity, link state, and active-slot fields at a glance; the F9 dashboard shows live Gateway/YoYo Fleet/DataGraph/Queue/Cost data and responds to a manual refresh; and F12 has accepted or rejected a real submission, with the outcome visible on screen.

## Verification

- The status bar's active-slot label changes correctly as you switch between F3, F9, and F12.
- F9's on-screen "updated" timestamp changes when you press **R**.
- A successful F12 submission shows a Payload ID and ledger position; the platform's WORM ledger records it as a genuine, permanent entry.

## Rollback

Exploring the status bar and F9 dashboard changes nothing — exit the console at any time with no cleanup needed. A real F12 submission is the one exception: it cannot be rolled back once confirmed, which is why step 6 above is optional and only worth doing with content you're comfortable being permanent.

If the console doesn't respond as expected, exit and restart it. Watch your own terminal's output for errors rather than checking system logs — a plain `os-console` launched from your own shell isn't running under any system service, so a system log has nothing to have captured.

## Next steps

- [[navigate-console-tui]] — the full TUI reference: every key binding and status bar field
- [[use-f-key-model]] — the F-key slot architecture and every Cartridge's default assignment
- [[run-first-slm-query]] — submit a real inference query once F9 shows Tier B live

## See also

- [[pair-a-new-device]] — how to acquire the device pairing this console session depends on
- [[read-the-command-ledger]] — reading the WORM ledger entries F12 writes
- [[os-console]] — the full architecture behind the console you just explored
