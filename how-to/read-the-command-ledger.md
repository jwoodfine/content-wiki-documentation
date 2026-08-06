---
schema: foundry-doc-v1
title: "Read the command ledger"
slug: read-the-command-ledger
short_description: "Reads the append-only WORM ledger over service-fs's real HTTP API — paging entries with a cursor and fetching a signed checkpoint — since no ledger-browsing UI exists in the console."
category: how-to
content_type: how-to
type: how-to
quality: complete
status: active
audience: "Engineers (hands on keyboard); customer operators"
last_edited: 2026-08-06
editor: pointsav-engineering
paired_with: read-the-command-ledger.es.md
research_trail:
  sources: [pointsav-monorepo service-fs/src/http.rs (GET /v1/entries, GET /v1/checkpoint routes), service-fs/src/ledger.rs (Checkpoint struct, signing)]
  verification_method: "independently source-verified against pointsav-monorepo on 2026-08-06 by reading the Rust source directly, with file:line citations recorded per claim; this guide replaces its own prior premise entirely — there is no F12 LEDGER tab, no in-console browsing UI of any kind, and service-fs has no CLI, so the real read path is service-fs's HTTP API directly"
---

## Prerequisites

- Network access to your `service-fs` instance
- Your module identifier for the required `X-Foundry-Module-ID` header

## Purpose

Read ledger history and fetch a verifiable checkpoint over `service-fs`'s real HTTP API — a couple of minutes. There is no ledger-browsing screen anywhere in `os-console`; F12 only shows an inline height/root indicator while a submission is in progress, not a history you can page through.

## Procedure

1. Fetch entries from a cursor, starting at 0 for the full history:

   ```bash
   curl -s -H "X-Foundry-Module-ID: <your-module-id>" \
     "http://<service-fs-host>/v1/entries?since=0"
   ```

   The header is required — a missing `X-Foundry-Module-ID` returns a 400, and a mismatched one returns a 403. Each entry in the response carries a `cursor`, a `payload_id`, and the `payload` itself.

2. Page forward using the response's own `next_cursor` field:

   ```bash
   curl -s -H "X-Foundry-Module-ID: <your-module-id>" \
     "http://<service-fs-host>/v1/entries?since=<next_cursor>"
   ```

   Repeat until the returned entry list is empty — that's the end of the ledger as of your request.

3. Fetch the current checkpoint to anchor what you just read:

   ```bash
   curl -s -H "X-Foundry-Module-ID: <your-module-id>" \
     "http://<service-fs-host>/v1/checkpoint"
   ```

   The response carries `tree_size` (the ledger's height — total entry count), `root_hash` (a hex-encoded SHA-256 tip hash), `algorithm` (`"sha256"`), a `timestamp`, and a `signature`.

   > **Note:** `signature` is only present if the `service-fs` instance was started with a signing key configured. An unsigned deployment returns `signature: null` — that's a real, valid configuration state, not a broken response.

## Expected outcome

The full set of ledger entries from your starting cursor onward, plus a checkpoint giving you the ledger's current height and root hash to check them against.

## Verification

Confirm the number of entries you paged through is consistent with the checkpoint's `tree_size` at the time you fetched it — fetching entries and the checkpoint aren't atomic against each other, so a small gap from activity between the two calls is expected, not an error. For a full step-by-step tamper-verification procedure using the checkpoint's hash and signature, see [[verify-worm-ledger]] — this guide covers reading the ledger, not proving it hasn't been altered.

## Rollback

Reading is non-destructive — there's nothing to undo. Re-running any of the calls above is always safe.

## Next steps

- [[verify-worm-ledger]] — verify a checkpoint's hash and signature against the entries it covers
- [[run-first-slm-query]] — a separate real HTTP path, for inference rather than ledger reads

## See also

- [[service-fs]] — the WORM storage layer these endpoints belong to
- [[worm-ledger-architecture]] — what the WORM guarantee covers and what it does not
- [[app-console-input]] — the F12 Input Machine that writes the entries you're reading here
