---
schema: foundry-doc-v1
title: "Verify a WORM ledger entry"
slug: verify-worm-ledger
short_description: "Verifies WORM ledger entries against a fetched checkpoint over service-fs's real HTTP API, using a standard SHA-256 toolchain — no CLI or proprietary tooling exists or is required."
category: how-to
index_group: records-storage
content_type: how-to
type: how-to
quality: complete
status: active
audience: "Engineers (hands on keyboard); customer operators"
last_edited: 2026-08-06
editor: pointsav-engineering
paired_with: verify-worm-ledger.es.md
research_trail:
  sources: [pointsav-monorepo service-fs/src/http.rs (GET /v1/entries, GET /v1/checkpoint), service-fs/src/ledger.rs (Checkpoint struct, C2SP signed-note signing), architecture/worm-ledger-architecture.md]
  verification_method: "grounded directly in the real service-fs HTTP API confirmed while rewriting read-the-command-ledger.md in the same session (2026-08-06); the guide's own prior Correction note already confirmed service-fs has no CLI at all and no verify subcommand — this rewrite replaces the fabricated tool commands with the real routes, and is deliberately conservative about the exact Merkle-tree verification math of the underlying C2SP tlog-tiles format, which isn't independently re-derived here"
---

## Prerequisites

- Network access to your `service-fs` instance
- Your module identifier for the `X-Foundry-Module-ID` header
- A SHA-256 utility (`sha256sum` on Linux, `shasum -a 256` on macOS)

## Purpose

Confirm that a ledger entry hasn't been altered since it was written, using only `curl` and standard hashing tools — no CLI or proprietary verification tool exists for this, and none is needed.

## Procedure

1. Fetch the entry (or range of entries) you want to verify, per [[read-the-command-ledger]]:

   ```bash
   curl -s -H "X-Foundry-Module-ID: <your-module-id>" \
     "http://<service-fs-host>/v1/entries?since=<cursor>"
   ```

2. Fetch the current checkpoint:

   ```bash
   curl -s -H "X-Foundry-Module-ID: <your-module-id>" \
     "http://<service-fs-host>/v1/checkpoint"
   ```

   The checkpoint carries `tree_size` (total entry count at the time it was issued), `root_hash` (a hex-encoded SHA-256 commitment covering every entry up to `tree_size`), `algorithm` (`"sha256"`), a `timestamp`, and a `signature`.

3. Confirm your fetched entries are covered by the checkpoint: their cursors must fall within `tree_size`. If your target entry's cursor is higher than the checkpoint's `tree_size`, fetch a newer checkpoint first.

4. If the checkpoint carries a signature, verify it. `signature` holds an Ed25519 signature over the C2SP signed-note body (`origin`, `tree_size`, and the base64-encoded `root_hash`), using the platform's published verifying key. A valid signature means the chain state was attested at that point — independent of trusting the live service in the moment you read it.

   > **Note:** `signature` is only present if the `service-fs` instance was started with a signing key configured. An unsigned deployment's checkpoint is still a real, honest snapshot of `tree_size`/`root_hash` — it just carries no independent third-party attestation. Don't treat a missing signature as an error.

## Expected outcome

A checkpoint whose `root_hash` and `tree_size` you can independently hold as a commitment to the ledger state at that point, and — where a signature is present — cryptographic proof that commitment was attested, not merely asserted by the running service.

## Verification

Re-fetch the checkpoint later and confirm `tree_size` only ever increases and that the `root_hash` for any `tree_size` you've seen before never changes. A ledger entry that was covered by an earlier checkpoint's `root_hash` and is still present, unmodified, under a later checkpoint's larger `tree_size` has never been altered — that consistency across checkpoints over time is the practical, repeatable verification available with just these two endpoints.

## Rollback

Verification is read-only. Nothing to undo.

## Next steps

- [[read-the-command-ledger]] — the entry-reading procedure this guide verifies against

## See also

- [[worm-ledger-architecture]] — what the WORM guarantee covers and what it does not
- [[service-fs]] — the service that implements and serves the ledger
