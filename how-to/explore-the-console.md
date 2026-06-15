---
schema: foundry-doc-v1
title: "How to explore the console for the first time"
slug: explore-the-console
category: how-to
content_type: how-to
type: how-to
status: active
last_edited: 2026-06-14
editor: pointsav-engineering
paired_with: explore-the-console.es.md
---

The platform console is a terminal application that organises operator-facing tools into a set of function-key slots, each running a distinct Cartridge. When you open the console for the first time, the interface may look unfamiliar — this guide walks you through the layout, how to move between slots, and how to confirm the system is working before you start your first real task.

For the full TUI reference, see [[navigate-console-tui]]. For the F-key slot model in depth, see [[use-f-key-model]].

## Prerequisites

- A paired device with appropriate tier access (see [[pair-a-new-device]])
- The console binary built and available in your PATH, or the workspace binary at `~/Foundry/clones/<archive>/os-console/`
- A terminal emulator that supports 24-bit colour and at least 80×24 characters

## Step 1: Launch the console

Start the console from the command line:

```
os-console
```

If the binary is not in PATH, run it directly from the build output:

```
~/Foundry/clones/<archive>/target/debug/os-console
```

The console opens in full-screen mode. You will see a three-zone layout: a status bar at the top, a main content area in the centre, and a navigation strip at the bottom.

## Step 2: Read the status bar

The status bar at the top of the screen shows the system's current state at a glance. Left to right:

- **Identity** — the active operator identity (a short name string set at pairing time)
- **Auth state** — `INPUT`, `USER`, or `READ` — the access tier of the current session
- **Active slot** — the F-key currently active (e.g., `F3`)
- **SLM tier** — the Doorman tier in use: `A` (DataGraph live), `B` (SLM only), or `C` (local fallback)
- **Session duration** — time since the console was launched

If the auth state reads `READ` and you expected `INPUT` or `USER`, the device has not completed the pairing sequence for the requested tier. See [[pair-a-new-device]] to resolve.

## Step 3: Navigate to the Doorman health slot

Press **F9** to activate the SLM Cartridge. This slot shows the Doorman health dashboard — the current state of the Tier A/B/C inference circuit.

Each tier shows its status:

- `A — DataGraph` — green if the entity store is reachable; `OPEN` if the circuit has tripped
- `B — SLM` — green if the local inference model is loaded and responding; `OPEN` if it failed to start
- `C — Local fallback` — always `AVAILABLE` unless the local OLMo model binary is missing

Doorman health is the first thing to check when starting a session. A green A and B means the full inference and entity-lookup stack is available. An open circuit on either tier means some features are degraded; the console falls back automatically but you should note which tier is affected.

## Step 4: Press R to refresh

While in F9, press **R** to force a Doorman health refresh. The status line updates within a second. This confirms the console is polling the Doorman service and the keyboard is responding correctly.

## Step 5: Navigate to the Input Machine slot

Press **F12** to activate the Input Machine Cartridge. This is the mandatory input checkpoint required by SYS-ADR-10 — every operator input that modifies platform state passes through this slot.

You will see a prompt area. Try submitting a simple text note. The console shows whether the input was **confirmed** (written to the WORM ledger) or **rejected** (quarantined with a reason code).

## Step 6: Review the status bar changes

As you move between slots, the status bar's **Active slot** indicator changes. Confirm that switching between F3, F9, and F12 updates the indicator correctly. If the indicator does not update, the TUI rendering loop may have encountered an error — exit and restart the console, then check `journalctl -u os-console` for error output.

## Key takeaways

- The three main zones are: status bar (top), content area (centre), navigation strip (bottom)
- F9 = Doorman health dashboard; check this first at every session start
- R refreshes the current slot without switching slots
- F12 is the mandatory input checkpoint; all platform-state modifications route through it
- `READ` auth state means INPUT or USER pairing has not completed for this session

## See also

- [[navigate-console-tui]] — full TUI reference: key bindings, status bar field definitions
- [[use-f-key-model]] — the F-key slot architecture, Cartridge model, all default slot assignments
- [[pair-a-new-device]] — how to acquire higher auth tiers for the console session
- [[run-first-slm-query]] — submitting an SLM inference query once F9 shows Tier B live
- [[read-the-command-ledger]] — reading the WORM ledger from the F12 LEDGER tab
