---
schema: foundry-doc-v1
title: "How to read the command ledger"
slug: read-the-command-ledger
category: how-to
content_type: how-to
type: how-to
status: active
last_edited: 2026-06-14
editor: pointsav-engineering
paired_with: read-the-command-ledger.es.md
---

The Command Ledger is the append-only audit record of everything a Totebox operator session has produced — commands executed, records verified, messages sent, and session boundaries. Reading the ledger is how you understand the history of a session, audit what changed during a window, and verify that a record was written in the sequence you expected.

For the Command Ledger's place in the session architecture, see [[console-os]]. For how the underlying storage layer works, see [[service-fs-architecture]].

## Prerequisites

- An active Totebox session (see [[open-first-totebox-session]])
- F12 Input Machine available (see [[app-console-input]])

## Read the ledger in the Input Machine (F12)

The Input Machine at F12 surfaces ledger activity alongside the verification queue.

1. Press **F12** to open the Input Machine.
2. Use the tab or arrow keys to navigate to the **Ledger** view (shown in the navigation strip as `LEDGER`).
3. The ledger displays entries in chronological order, newest at the bottom. Each entry shows a timestamp, entry type, and a short summary.
4. Use **Page Up** / **Page Down** to scroll; **/** to search entries by keyword.

## Entry types

| Type | Meaning |
|---|---|
| `SESSION_OPEN` | A Totebox session was started with the listed identity |
| `SESSION_CLOSE` | The session was closed; duration recorded |
| `RECORD_VERIFIED` | A human operator confirmed a record through F12 |
| `RECORD_REJECTED` | A record was rejected; routed to quarantine |
| `MESSAGE_SENT` | An outbound message was dispatched |
| `CHECKPOINT` | A signed proof of ledger state was written (periodic) |

## Verify a specific entry

To confirm that a record is genuinely in the ledger (and not altered after the fact):

1. Note the entry's position (row index) and its displayed hash suffix.
2. Export the corresponding tile using the `read_since` operation on the CLI or the service-fs API.
3. Compute the SHA-256 hash of the tile and compare it to the checkpoint hash for that position.

A mismatch indicates tampering — the WORM guarantee covers the chain from the first write, not just the visible summary.

For the verification procedure in detail, see [[verify-worm-ledger]].

## Export ledger entries

In the Input Machine's Ledger view, press **e** to export a date range as a local text file. The file format is plain-text C2SP tlog-tiles — readable without any PointSav tooling.

## Key takeaways

- The Command Ledger is append-only; no entry can be modified or deleted
- The Input Machine (F12) surfaces ledger activity alongside the verification queue — they are two views of the same audit trail
- Checkpoint hashes enable third-party verification without a live service
- Exporting tiles produces standard C2SP tlog-tiles format; any SHA-256 implementation can verify the chain

## See also

- [[console-os]] — the Command Ledger's role in the session architecture
- [[service-fs-architecture]] — the WORM storage layer that persists ledger entries
- [[worm-ledger-architecture]] — what the WORM guarantee covers and what it does not
- [[verify-worm-ledger]] — step-by-step ledger verification procedure
- [[app-console-input]] — the Input Machine and its ledger view
