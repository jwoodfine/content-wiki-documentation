---
schema: foundry-doc-v1
title: "Use the F-key cartridge model"
slug: use-f-key-model
short_description: "Works the os-console F-key cartridge model — F3 email, F9's monitoring-only SLM dashboard, F12's file-based Input Machine — where each compiled-in cartridge owns its slot's rendering and input."
category: how-to
index_group: working-in-the-console
content_type: how-to
type: how-to
quality: complete
status: active
audience: "Engineers (hands on keyboard); customer operators"
last_edited: 2026-08-06
editor: pointsav-engineering
paired_with: use-f-key-model.es.md
research_trail:
  sources: [pointsav-monorepo app-console-slm (F9 SlmCartridge, confirmed monitoring-only, no prompt UI), app-console-input (F12 InputMachine cartridge, real outcome states), app-console-email (F3 EmailCartridge)]
  verification_method: "independently source-verified against pointsav-monorepo on 2026-08-06 by reading the Rust source directly, with file:line citations recorded per claim; corrected two fabrications — F9 was described as an interactive prompt/chat interface (it has no text-input widget of any kind, confirmed by reading its full event-handling code) and F12 was described with a reject/quarantine outcome that doesn't exist (real outcomes are Done-with-payload-ID or a generic Error)"
---

## Prerequisites

- An active session with `os-console` open (see [[open-first-totebox-session]])
- Familiarity with the console's layout (see [[navigate-console-tui]])

## Purpose

Understand what each default cartridge actually does before you rely on one for real work — a few minutes, and it corrects two real fabrications that were in this guide previously: F9 is not a chat interface, and F12 does not have a reject/quarantine outcome.

## Procedure

1. Recognize that a Cartridge is compiled directly into the `os-console` binary — not a plugin, not a subprocess. Pressing its F-key hands control to that registered module, which owns its own rendering and keyboard handling until you switch away.

2. Use the Email Cartridge at **F3**: press **F3**, read the inbox list (unread counts and sender summaries), navigate with arrow keys, press **Enter** to open a message, and **c** to compose. Outbound mail routes through `service-email`, not a direct SMTP connection.

3. Use the SLM Cartridge at **F9** for what it actually is: a live monitoring dashboard, not a query tool. Press **F9** and read its five sections — Gateway, YoYo Fleet, DataGraph, Queue, and Cost Today. Press **R** to force an immediate refresh instead of waiting for the next poll.

   > **Note:** F9 has no prompt input of any kind — no text field, no submit key, no streaming response. If you're looking for how to actually run an inference query, see [[run-first-slm-query]], which covers the real path.

4. Use the Input Machine at **F12** for what it actually does: it's the platform's mandatory file-ingestion checkpoint, not a record-review-and-approve screen. Files entering through F12 have execution permissions stripped and are tagged before being routed onward — this is the only path raw external files can enter a Totebox.

   > **Warning:** a submission through F12 either succeeds (shown as Done, with a payload ID and ledger position — occasionally with a non-fatal warning attached) or fails with a generic error. There is no separate "reject and quarantine" outcome in this flow — a rejected submission simply shows as an error, not a distinct quarantine state.

## Expected outcome

You know which cartridge does what without guessing: F3 for mail, F9 for read-only inference-gateway health, F12 for the mandatory file-ingestion checkpoint — and you know F9 is not where you submit a query.

## Verification

Open each of F3, F9, and F12 in turn and confirm what you see matches this guide: an inbox at F3, a five-section health dashboard with no input field at F9, and a file-ingestion interface at F12.

## Rollback

Viewing F3 or F9 changes nothing. A real F12 submission is not reversible — see [[explore-the-console]] for that caution in more detail before you submit anything through it.

## Next steps

- [[run-first-slm-query]] — the real way to submit an inference query, since F9 isn't it
- [[read-the-command-ledger]] — read what F12 has written, via the ledger's real HTTP API

## See also

- [[app-console-keys]] — chassis architecture and the Cartridge trait every slot implements
- [[app-console-email]] — the Email Cartridge in full
- [[app-console-slm]] — the SLM Cartridge's dashboard in full
- [[app-console-input]] — the Input Machine in full
- [[navigate-console-tui]] — overall TUI layout and slot navigation
