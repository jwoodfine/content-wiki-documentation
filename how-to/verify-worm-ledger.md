---
schema: foundry-doc-v1
title: "How to verify a WORM ledger entry"
slug: verify-worm-ledger
category: how-to
content_type: how-to
type: how-to
status: active
last_edited: 2026-06-14
editor: pointsav-engineering
paired_with: verify-worm-ledger.es.md
---

The WORM ledger guarantees that records cannot be modified or deleted after they are written. Verification confirms that guarantee holds for a specific entry: that the hash chain is intact and that no post-write alteration occurred. This guide covers verification using the service-fs API and the standard SHA-256 toolchain — no proprietary tooling is required.

For what the WORM guarantee covers and does not cover, see [[worm-ledger-architecture]]. For the storage format, see [[worm-ledger-storage-architecture]].

## Prerequisites

- Access to a Totebox ledger (local file access or service-fs API)
- A SHA-256 utility (`sha256sum` on Linux, `shasum -a 256` on macOS, or equivalent)
- The position (row index) or timestamp range of the entry you want to verify

## Step 1: Export the tile containing your entry

Using the service-fs API, call `read_since` with the checkpoint immediately preceding your target entry:

```
read_since(checkpoint_id: "<checkpoint-id>", limit: 1)
```

This returns the tile file for that segment of the ledger. On a local deployment you can also read the C2SP tlog-tiles files directly from the ledger directory.

## Step 2: Locate the entry in the tile

The tile is plain text in C2SP tlog-tiles format. Each line is a base64-encoded log entry followed by its hash. Find the row matching your target entry by timestamp or sequence number.

## Step 3: Verify the hash chain

For each row in the tile, the hash of that row is included in the hash computation for the next row. To verify entry N:

1. Take the hash from row N−1 (or the genesis hash for the first entry).
2. Concatenate it with the raw bytes of entry N.
3. Compute SHA-256 of the concatenation.
4. Compare the result to the hash recorded in row N.

A match confirms the chain is intact from the genesis to that point. A mismatch at row N means either row N or some earlier row was altered — inspect each row backwards from N to isolate the point of tampering.

## Step 4: Verify against a signed checkpoint

If a signed checkpoint covers the range containing your entry, you can verify that checkpoint's signature to extend the guarantee to the anchor point:

1. Retrieve the C2SP signed-note for the relevant checkpoint.
2. Verify the note's Ed25519 signature using the public key published for the Sigstore Rekor anchor.
3. Confirm that the checkpoint covers a sequence number that includes your entry.

A valid signature from Sigstore Rekor means the chain state was externally timestamped at that point, providing verifiability independent of the live service.

## Automated verification

The `service-fs` CLI provides a `verify` subcommand that runs steps 2–4 automatically:

```
service-fs verify --from <checkpoint-id> --to <entry-id>
```

Use the manual procedure above when you want to inspect the chain without trusting the CLI.

## Key takeaways

- Verification requires only a SHA-256 utility and the raw tile files — no live service needed
- A mismatch in the hash chain at row N means alteration at or before N; inspect backwards to isolate it
- Signed checkpoints extend verification to a public timestamp anchor, enabling third-party audits
- The C2SP tlog-tiles format ensures these steps remain executable with standard tools for decades

## See also

- [[worm-ledger-architecture]] — what the WORM guarantee covers and its structural properties
- [[worm-ledger-storage-architecture]] — the tile format, atomic writes, and checkpoint structure
- [[service-fs-architecture]] — the service that implements and serves the ledger
- [[read-the-command-ledger]] — reading ledger entries from within os-console
- [[worm-ledger-design]] — the design philosophy and regulatory compliance rationale
