---
schema: foundry-doc-v1
title: "Cryptographic ledgers"
slug: cryptographic-ledgers
category: security
type: topic
content_type: topic
quality: complete
short_description: "Cryptographic ledgers are the immutable-state storage pattern in the PointSav platform, where any alteration breaks a verifiable hash chain, not just an access-control rule."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-07-28
editor: pointsav-engineering
cites: []
paired_with: cryptographic-ledgers.es.md
---


> Cryptographic ledgers are the immutable-state storage pattern used in the PointSav platform, enforcing mathematical immutability so that any alteration to a recorded fact breaks a verifiable cryptographic hash chain rather than requiring trust in administrative access controls.

**Cryptographic ledgers** are the immutable-state storage architecture used across the [[pointsav-overview|PointSav]] platform to guarantee that once a corporate fact is recorded, any subsequent alteration — down to a single byte — breaks a mathematical lock that any third party can independently verify. In traditional database systems, a system administrator with sufficient privileges can silently edit a record, altering a financial entry or compliance log without triggering any automatic alarm. The cryptographic ledger eliminates this vulnerability by removing the concept of a privileged mutable path: the storage architecture enforces append-only writes at the code level, and every record's integrity is bound into a cryptographic hash chain where modifying any prior entry produces a detectable inconsistency in all subsequent entries. See also [[merkle-proofs-as-substrate-primitive|Merkle proofs as a substrate primitive]] and [[worm-ledger-design|the WORM ledger design]].

## Overview

The [[pointsav-overview|PointSav]] platform implements cryptographic ledger discipline through [[service-fs-architecture|service-fs]], the per-tenant [[worm-ledger-architecture|WORM (Write-Once-Read-Many) immutable ledger]]. The architecture physically separates every incoming payload into two entities: the asset and its state record.

**The asset** — when a user submits a file (a PDF contract, a spreadsheet, a document) into the system, the storage layer places it in an isolated vault and strips all execution permissions. It becomes an inert binary object.

**The state record** — the system concurrently generates a deterministic record containing human-readable metadata (author, date, taxonomy, type) and a SHA-256 cryptographic checksum of the original asset. The state record is appended to the ledger; it cannot be modified after appending.

## How It Works

The cryptographic lock works through the [[merkle-proofs-as-substrate-primitive|Merkle hash chain]] structure. Each new entry is hashed; the hash of the new entry is combined with the hash of the prior entry to produce the hash of the current tree state (the "tree head" or checkpoint). The checkpoint is signed by the tenant key and published.

If an auditor or compliance engine needs to verify the integrity of a historical record:

1. Re-hash the physical asset.
2. Compare the computed hash to the checksum in the state record.
3. Verify the state record is present in the Merkle tree at the claimed position by computing an inclusion proof against the signed checkpoint.
4. Verify the checkpoint signature against the tenant's public key.

If the hashes match and the inclusion proof verifies, the record is intact. If either check fails, the asset has been altered or the ledger has been tampered with — and the Merkle chain makes tampering externally detectable even without access to the original file.

## Architecture

The [[pointsav-overview|PointSav]] cryptographic ledger uses C2SP tlog-tiles format — the same on-disk structure used by Certificate Transparency logs and Sigstore Rekor. Tiles are static, base64-encoded text files containing 256 entries each at the leaf level, with intermediate [[merkle-proofs-as-substrate-primitive|Merkle-level]] tiles above them. This format is human-readable, independently verifiable, and compatible with standard Certificate Transparency tooling.

**Correction (2026-07-28):** the on-disk format is currently a single flat
newline-delimited JSON log file per tenant (`<root>/<moduleId>/log.jsonl`), not a
C2SP tlog-tiles multi-file structure — verified against `service-fs/src/posix_tile.rs`,
whose own doc comments describe "segment-batched tile files (256 entries per sealed
segment)" as "the natural performance upgrade and a follow-up commit," not yet
implemented; the file's `PosixTileLedger` struct holds one `log_path`, not a tile-file
set. The cryptographic properties this article describes — hash-chained entries,
Ed25519-signed checkpoints, inclusion and consistency proofs — are real and implemented
in that same file, just not in the specific tile-file on-disk layout named here. The
Monthly Rekor anchoring claim below, by contrast, **is verified accurate** — see the note
after that paragraph.

Monthly, each tenant's signed checkpoint is submitted to the Sigstore Rekor v2 public transparency log. Once anchored, the checkpoint is public and the tenant cannot retroactively alter any prior record without the tampered state being detectable against the anchored checkpoint.

**Verified accurate (2026-07-28):** confirmed against `service-fs/anchor-emitter` (580
lines, a real Sigstore Rekor v2 `hashedRekordRequestV002` submission client) and its
systemd timer `infrastructure/local-fs-anchoring/local-fs-anchor.timer`, which fires
monthly on the 1st at 02:30 UTC. This part of the article matches the live
implementation; only the tile-format paragraph above needed correcting.

## Applications

The cryptographic ledger applies across all customer-facing data in the platform:

- **Corporate records** — financial entries, compliance documents, and operational logs are all appended to the WORM ledger before any other processing.
- **SOC 2 compliance** — the ledger's append-only invariant and Rekor anchoring satisfy SOC 2 Processing Integrity requirements (PI4 — Outputs are complete, accurate, and timely).
- **Regulatory recordkeeping** — the architecture is structurally aligned with SEC Rule 17a-4(f) broker-dealer electronic recordkeeping requirements (WORM path) and eIDAS qualified preservation service requirements for long-term proof-of-existence.
- **Audit trail** — every read of the ledger is itself logged to an audit sub-ledger, which is also WORM and also anchored.

## See also

- [[worm-ledger-architecture]]
- [[crypto-attestation]]
- [[capability-based-security]]
- [[compounding-substrate]]
- [[sel4-microkernel-substrate]]
