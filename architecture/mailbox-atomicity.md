---
schema: foundry-doc-v1
title: "Mailbox atomicity — flock-based prepend and msg-id idempotency"
slug: mailbox-atomicity
language: en
category: architecture
type: topic
content_type: topic
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-25
editor: pointsav-engineering
cites: []
paired_with: mailbox-atomicity.es.md
---

Sessions communicate by prepending messages to flat-file mailboxes at `.agent/inbox.md` and `.agent/outbox.md`. Messages carry a YAML envelope (from, to, re, created, status, optional msg-id) followed by a free-text body. Newest messages live at the top so the hub session reading an outbox sees the most recent activity first.

## Key Takeaways

- `mailbox-prepend` acquires an exclusive `flock` lock before any read-modify-write. Two concurrent prepends serialize rather than race — the slower caller blocks up to 30 seconds, then proceeds after the first releases the lock.
- `msg-id` idempotency: if the message carries a `msg-id:` field, the script scans the first 200 lines of the target for an existing entry with that id and skips the prepend if found. A timer firing twice or an operator retrying a script will not double-send.
- The failure mode without this discipline is silent. A lost message simply never arrives — no error is surfaced to either the sender or the recipient. The helper script exists precisely because silent data loss is worse than a brief serialization delay.
- The script is the enforcement point. Atomicity holds only when all sessions and automation call `mailbox-prepend` rather than writing to the mailbox file directly.

The atomicity problem: two sessions prepending to the same mailbox without coordination produce the classic read-modify-write race. Session A reads the current file, prepends its message, and writes back. Session B does the same simultaneously. Whichever write lands last wins; the other message is lost. This is reproducible with parallel AI-coding sub-agents; cross-user concurrency makes it inevitable.

The `mailbox-prepend` helper script solves this with `flock`. It takes the target mailbox path, derives a lock path for archive-scoped mailboxes, and acquires an exclusive lock with a 30-second timeout before performing the read-modify-write. Two simultaneous calls serialise rather than collide.

A second safety: msg-id idempotency. If the message body contains a `msg-id:` field, the script scans the first 200 lines of the target for an existing entry with the same id and skips the prepend if found. This means a script that gets retried — a timer firing twice, an operator re-running, a hook misfiring — will not double-send. The 200-line window is generous enough to catch same-day duplicates without making the scan expensive on large archives.

This is two-line wrapping around `flock` and `grep`. The failure mode without it is silent — a lost message simply never arrives, and the sender has no indication. Building the discipline into a shared script that sessions and automation call is cheaper than building a more sophisticated queue.

## See also

- [[multi-engine-session-coordination]] — the session-lock protocol this mailbox discipline supports
- [[totebox-session]] — the session model whose inter-session communication this atomicity protects
- [[totebox-orchestration-development]] — the orchestration layer that routes messages between sessions
- [[learning-datagraph-architecture]] — the audit ledger whose capture hooks face the same concurrent-write race conditions
