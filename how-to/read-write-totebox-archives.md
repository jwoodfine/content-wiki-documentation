---
schema: foundry-doc-v1
title: "How to read and write Totebox archives"
slug: read-write-totebox-archives
short_description: "Reads a Totebox archive's state at session start — inbox, session context, git status, NEXT.md — and writes changes through the staging-tier commit flow."
category: how-to
index_group: records-storage
content_type: how-to
type: how-to
quality: complete
status: active
audience: "Engineers (hands on keyboard); customer operators"
last_edited: 2026-08-06
editor: pointsav-engineering
paired_with: read-write-totebox-archives.es.md
research_trail:
  sources: [pointsav-monorepo .agent/ mailbox and drafts-outbound conventions, bin/commit-as-next.sh]
  verification_method: "verified against the same staging-tier commit flow and mailbox protocol already source-verified in install-toolchain.md and this wiki's sibling how-to guides"
---

A Totebox Archive is a scoped working environment: a git repository cloned from an upstream source, configured with session rules, inbox and outbox mailboxes, and a drafts pipeline. Reading an archive means understanding its current state — the inbox, active work, and session context. Writing to an archive means committing to its git history using the staging-tier commit flow. This guide covers both operations.

For the session model that governs archive access, see [[totebox-session]] and [[totebox-orchestration-development]].

## Prerequisites

- A device paired to the workspace, with write access to the archive (see [[pair-a-new-device]])
- A Totebox Archive opened in your working directory
- An active session (see [[open-first-totebox-session]])

## Purpose

Read a Totebox Archive's current state at session start, write changes through the staging-tier commit flow, stage editorial drafts correctly, and communicate across archives through the mailbox protocol rather than by editing another session's state files.

## Procedure

1. **Read an archive's state at session start**, in this order:
   - Open `.agent/inbox.md` and review pending messages — these represent work or information relayed from other sessions.
   - Open `.agent/session-start.md` if present — it contains orientation notes from the last session that closed in this archive.
   - Open `.agent/memory/session-context.md` for a rolling 5-session summary including carry-forward items and operator preferences.
   - Run `git status` to see any uncommitted changes. If files are staged or modified without a commit, read them before starting new work.
   - Read `NEXT.md` — the archive's open items queue; what is in progress and what is blocked.

2. **Write to the archive using the staging-tier flow.** Do not use `git commit` directly — use the `commit-as-next.sh` helper, which sets the correct author identity and signs the commit:
   - Make your changes.
   - Stage specific files: `git add <file> <file>` — never `git add .` or `git add -A`.
   - Commit: `~/Foundry/bin/commit-as-next.sh "<message>"`.
   - Verify: `git status` should show a clean tree.

   Commits in an archive stay on the local feature branch until Stage 6 promotion by the Command Session.

3. **Stage editorial drafts for handoff, if applicable.** If your work produces an article draft, stage it to `.agent/drafts-outbound/` with the correct `foundry-draft-v1` frontmatter before closing the session. Do not commit draft content directly to the wiki repos from an archive — the draft flows through the editorial pipeline first. A staged draft carries frontmatter with `artifact`, `schema: foundry-draft-v1`, `status: staged`, `route-to:`, plus body content suitable for the destination wiki article.

4. **Communicate across archives via the mailbox, never by editing another session's state files.** Messages arrive at `.agent/inbox.md` from other sessions and are read at session start; new outbound messages are prepended to `.agent/outbox.md`, which the Command Session sweeps at intervals. Write to another archive's inbox only via the Command Session or an approved MCP tool (`send_mailbox_message`) — never edit another session's inbox directly.

## Expected outcome

The archive's state (inbox, session context, git status, NEXT.md) is understood before new work starts; any commits land through `commit-as-next.sh` with a clean working tree afterward; any draft output is staged to `.agent/drafts-outbound/` rather than committed directly to a wiki repo.

## Verification

`git status` shows a clean tree after each commit. A staged draft's frontmatter validates against the `foundry-draft-v1` schema. No direct edits appear in another session's `.agent/inbox.md` or `.agent/outbox.md`.

## Rollback

An uncommitted change can be discarded with `git checkout -- <file>` or `git restore <file>` before staging. A committed change on the local feature branch has not yet promoted to canonical (Stage 6 is a separate, later step), so reverting it is a normal local git operation, not a production rollback.

## Next steps

- [[open-first-totebox-session]] — opening a session from scratch on a newly paired device
- [[pair-a-new-device]] — how pairing grants write access to an archive in the first place

## See also

- [[totebox-session]] — the scoped working environment model
- [[totebox-orchestration-development]] — the orchestration model governing how archives interoperate
- [[machine-based-auth]] — how pairing grants write access to archives
- [[worm-ledger-architecture]] — the append-only ledger that records all platform events
