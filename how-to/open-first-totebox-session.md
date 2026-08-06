---
schema: foundry-doc-v1
title: "Open your first Totebox session"
slug: open-first-totebox-session
short_description: "Opens a first Totebox session in a single archive: read the manifest, check your inbox, understand what the session can and can't write, and complete the shutdown sweep before closing."
category: how-to
index_group: getting-started
content_type: how-to
type: how-to
quality: complete
status: active
audience: "Engineers (hands on keyboard); customer operators"
last_edited: 2026-08-06
editor: pointsav-engineering
paired_with: open-first-totebox-session.es.md
research_trail:
  sources: [pointsav-monorepo architecture/totebox-session.md (session scope, Tetrad, inbox/outbox protocol, permission tiers — corrected 2026-08-06), architecture/os-console.md (customer entry point via os-console Direct mode)]
  verification_method: "grounded directly in totebox-session.md after independently re-verifying and correcting a false claim on that same page (its PermissionTier/PairingRole conflation, fixed 2026-08-06); this guide describes only mechanics stated as current on that page, hedging anything the source itself marks planned/intended rather than shipped"
---

## Prerequisites

- A device already paired to the workspace (see [[pair-a-new-device]])
- At least one Totebox Archive your account has access to
- A permission tier sufficient for the work you intend to do (see [[personnel-permissions]])

## Purpose

Open a Totebox Session — the scoped, AI-assisted working environment bound to a single archive — and understand what it can and can't do before you start. Every development task in Totebox Orchestration begins this way, whether you're a contributor working in the development workspace or a customer connecting through [[os-console]].

## Procedure

1. Identify the archive you're opening a session in. A session is always scoped to exactly one archive; there is no cross-archive session.

2. Read the archive's manifest before doing anything else. It carries the archive's mission, its [[totebox-orchestration-development|Tetrad]] status (which of vendor, customer, deployment, and wiki legs are active), and its AI gateway endpoint.

3. Check the archive's inbox. A non-zero pending count means another archive or session has left you a message — a decision, a blocker, or context that may change what you do this session. Read it before starting work; archive each message as actioned once you've addressed it.

4. Confirm your permission tier covers the work ahead. Tiers are enforced by pairings, not by a role you type in — see [[personnel-permissions]] for what each tier can reach.

5. Work within the session's scope (see below). The boundary is structural, not a policy you have to remember to follow.

6. Before closing, run the shutdown sweep:

   1. Update or create the archive's durable work-in-progress record for anything still open
   2. Prepend any outbound messages for other archives to the outbox
   3. Commit uncommitted changes to the archive's staging branch

## Expected outcome

A working session scoped to a single archive: you can read and write the repositories that archive declares, your inbox has been reviewed, and any cross-archive requests are queued as outbox messages rather than direct writes.

## Verification

- Confirm the session cannot write outside the archive's declared repositories — this is enforced structurally, not by convention, so a write attempt outside scope fails rather than merely being discouraged.
- Confirm the inbox's pending count is zero, or that every remaining pending message is one you've deliberately deferred, not overlooked.
- Before ending the session, confirm `git status` shows nothing left uncommitted that the shutdown sweep should have caught.

## Rollback

Closing a session without the shutdown sweep isn't destructive, but it leaves work unstaged and undocumented — the next session (yours or someone else's) starts without knowing what was in progress. There's no separate "undo" for a skipped sweep; the recovery is to open a new session in the same archive and run the sweep late, checking `git status` and the archive's own carry-forward notes for whatever was left open.

## Next steps

- [[navigate-console-tui]] — work the console once your session is open
- [[explore-the-console]] — a first-time tour of the console's layout and function-key slots
- [[read-write-totebox-archives]] — the full read/write flow for working in an archive

## See also

- [[totebox-session]] — the full architecture: session scope, the Tetrad, and permission tiers in depth
- [[pairing-as-permission]] — how session access boundaries are enforced
- [[os-console]] — the customer-facing entry point that performs the same function
