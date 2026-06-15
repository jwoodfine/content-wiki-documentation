---
schema: foundry-doc-v1
title: "How to read and write Totebox archives"
slug: read-write-totebox-archives
category: how-to
content_type: how-to
type: how-to
status: active
last_edited: 2026-06-14
editor: pointsav-engineering
paired_with: read-write-totebox-archives.es.md
---

A Totebox Archive is a scoped working environment: a git repository cloned from an upstream source, configured with session rules, inbox and outbox mailboxes, and a drafts pipeline. Reading an archive means understanding its current state — the inbox, active work, and session context. Writing to an archive means committing to its git history using the staging-tier commit flow. This guide covers both operations.

For the session model that governs archive access, see [[totebox-session]] and [[totebox-orchestration-development]].

## Prerequisites

- A paired device with INPUT-tier access (see [[pair-a-new-device]])
- A Totebox Archive opened in your working directory
- An active session (see [[open-first-totebox-session]])

## Reading an archive at session start

Before doing any work in an archive, read its current state in this order:

1. **Read the inbox** — open `.agent/inbox.md` and review pending messages. These represent work or information relayed from other sessions.
2. **Read the session start file** — open `.agent/session-start.md` if present. It contains orientation notes from the last session that closed in this archive.
3. **Read the session context** — open `.agent/memory/session-context.md` for a rolling 5-session summary including carry-forward items and operator preferences.
4. **Check git status** — run `git status` to see any uncommitted changes. If files are staged or modified without a commit, read them before starting new work.
5. **Read the NEXT.md** — the archive's open items queue; what is in progress and what is blocked.

## Writing to an archive

All commits use the staging-tier flow. Do not use `git commit` directly — use the `commit-as-next.sh` helper, which sets the correct author identity and signs the commit.

The sequence for any write:

1. Make your changes.
2. Stage specific files: `git add <file> <file>` — never `git add .` or `git add -A`.
3. Commit: `~/Foundry/bin/commit-as-next.sh "<message>"`.
4. Verify: `git status` should show a clean tree.

Commits in an archive stay on the local feature branch until Stage 6 promotion by the Command Session.

## Staging editorial drafts for handoff

If your work produces an article draft, stage it to `.agent/drafts-outbound/` with the correct `foundry-draft-v1` frontmatter before closing the session. Do not commit draft content directly to the wiki repos from an archive — the draft flows through the editorial pipeline first.

A staged draft has:
- Frontmatter with `artifact`, `schema: foundry-draft-v1`, `status: staged`, `route-to:`
- Body content suitable for the destination wiki article

## Cross-archive communication

Use the mailbox system to communicate with other sessions rather than editing state files directly:

- **Inbox** — messages arrive at `.agent/inbox.md` from other sessions; read at session start
- **Outbox** — prepend new messages to `.agent/outbox.md`; the Command Session sweeps these at intervals

Write to another archive's inbox only via the Command Session or an approved MCP tool (`send_mailbox_message`). Never edit another session's inbox directly.

## Key takeaways

- Always read inbox → session-start → session-context → git status → NEXT.md before starting work
- Use `commit-as-next.sh` for every commit; direct `git commit` is blocked by the pre-commit gate
- Stage drafts to `.agent/drafts-outbound/`; don't commit draft content to wiki repos from this archive
- Cross-session communication uses the mailbox protocol — never write another session's state files directly

## See also

- [[totebox-session]] — the scoped working environment model
- [[totebox-orchestration-development]] — the orchestration model governing how archives interoperate
- [[open-first-totebox-session]] — opening a session from scratch on a newly paired device
- [[machine-based-auth]] — how INPUT-tier pairing grants write access to archives
- [[worm-ledger-architecture]] — the append-only ledger that records all platform events
