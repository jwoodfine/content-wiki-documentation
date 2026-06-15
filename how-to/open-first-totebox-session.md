---
schema: foundry-doc-v1
title: "How to open your first Totebox session"
slug: open-first-totebox-session
category: how-to
content_type: how-to
type: how-to
status: active
last_edited: 2026-06-14
editor: pointsav-engineering
paired_with: open-first-totebox-session.es.md
---

A Totebox session is the scoped working environment for a single archive — the boundary within which you read records, commit changes, and route requests to other archives. Every development task begins by opening a session in the archive that owns the work.

This guide covers the initial setup from a freshly paired device. If your device is not yet paired, complete [[pair-a-new-device]] first.

For architecture details, see [[totebox-session]] and [[totebox-orchestration-development]].

## Prerequisites

- A device paired at INPUT tier or above (see [[pair-a-new-device]])
- `os-console` installed and authenticated
- At least one archive provisioned on your account

## Steps

### 1. Launch os-console

Open `os-console` on your paired device. The home screen lists your account's archives. If no archives appear, your account has not yet been assigned archive access — contact the system administrator.

### 2. Select an archive

Tap or click the archive you want to work in. The console reads the archive manifest and displays:

- Archive name and module identifier
- Tetrad status — which of the four delivery legs (vendor, customer, deployment, wiki) are active
- Pending inbox count — messages from other archives or sessions awaiting your attention
- The AI gateway endpoint the session will use for inference

### 3. Review your inbox

If the pending inbox count is non-zero, review inbox messages before starting work. Messages may carry decisions, blockers, or context that should inform what you do this session. Mark each message actioned when you have addressed it.

### 4. Start a task

In the session view, tasks appear as BRIEF cards — durable project artifacts that survive session boundaries. Each BRIEF shows its status (active, reference, archived), the current carry-forward items, and the artifact types the work produces.

Select a BRIEF to see its work log and open items. If this is a new archive with no BRIEFs, the session is in bootstrap state — your first task is typically to write the archive's BRIEF.

### 5. Save your work before closing

Before ending a session, the console prompts a shutdown sweep:

1. Update or create BRIEFs for in-progress work
2. Prepend outbound messages to the outbox for other archives or the hub
3. Commit any uncommitted changes on the archive's staging branch

Closing without completing the shutdown sweep leaves work in an unstaged state that may conflict with the next session.

## What a session can do

A Totebox session writes only to its own archive's declared repositories. It cannot write workspace configuration, identity keys, or any file in a sibling archive. Cross-archive requests are routed as messages through the outbox — the hub session delivers them.

| Allowed | Not allowed |
|---|---|
| Edit files in this archive's repos | Write to another archive's files |
| Commit on the archive's staging branch | Push to canonical without Stage 6 |
| Send messages via the outbox | Write workspace-level config |
| Stage wiki drafts in drafts-outbound | Write to the identity store |

## Key takeaways

- Every session opens inside a single archive — scope is enforced structurally, not by policy
- Read your inbox before starting work; messages may change your task priorities
- BRIEFs are the durable record of in-progress work — they survive session close
- Complete the shutdown sweep to avoid lost work and staging conflicts

## See also

- [[totebox-session]] — what a session is and its full capability model
- [[pair-a-new-device]] — enroll the device this session runs on
- [[pairing-as-permission]] — how the session's access boundaries are enforced
- [[totebox-orchestration-development]] — the development architecture a session participates in
