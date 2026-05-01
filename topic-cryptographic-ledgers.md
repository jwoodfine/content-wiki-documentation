---
schema: foundry-doc-v1
title: "Cryptographic Ledgers"
slug: topic-cryptographic-ledgers
category: architecture
type: topic
quality: core
short_description: "Cryptographic ledgers are the immutable-state storage pattern used in the PointSav platform, enforcing mathematical immutability so that any alteration to a recorded fact breaks a verifiable cryptographic hash chain rather than requiring trust in administrative access controls."
status: pre-build
last_edited: 2026-04-30
editor: pointsav-engineering
cites: []
paired_with: topic-cryptographic-ledgers.es.md
---

# Cryptographic Ledgers

> Cryptographic ledgers are the immutable-state storage pattern used in the PointSav platform, enforcing mathematical immutability so that any alteration to a recorded fact breaks a verifiable cryptographic hash chain rather than requiring trust in administrative access controls.

**Cryptographic ledgers** are the immutable-state storage architecture used across the PointSav platform to guarantee that once a corporate fact is recorded, any subsequent alteration — down to a single byte — breaks a mathematical lock that any third party can independently verify. In traditional database systems, a system administrator with sufficient privileges can silently edit a record, altering a financial entry or compliance log without triggering any automatic alarm. The cryptographic ledger eliminates this vulnerability by removing the concept of a privileged mutable path: the storage architecture enforces append-only writes at the code level, and every record's integrity is bound into a cryptographic hash chain where modifying any prior entry produces a detectable inconsistency in all subsequent entries.

## Overview

The PointSav platform implements cryptographic ledger discipline through `service-fs`, the per-tenant WORM (Write-Once-Read-Many) immutable ledger. The architecture physically separates every incoming payload into two entities: the asset and its state record.

**The asset** — when a user submits a file (a PDF contract, a spreadsheet, a document) into the system, the storage layer places it in an isolated vault and strips all execution permissions. It becomes an inert binary object.

**The state record** — the system concurrently generates a deterministic record containing human-readable metadata (author, date, taxonomy, type) and a SHA-256 cryptographic checksum of the original asset. The state record is appended to the ledger; it cannot be modified after appending.

## How It Works

The cryptographic lock works through the Merkle hash chain structure. Each new entry is hashed; the hash of the new entry is combined with the hash of the prior entry to produce the hash of the current tree state (the "tree head" or checkpoint). The checkpoint is signed by the tenant key and published.

If an auditor or compliance engine needs to verify the integrity of a historical record:

1. Re-hash the physical asset.
2. Compare the computed hash to the checksum in the state record.
3. Verify the state record is present in the Merkle tree at the claimed position by computing an inclusion proof against the signed checkpoint.
4. Verify the checkpoint signature against the tenant's public key.

If the hashes match and the inclusion proof verifies, the record is intact. If either check fails, the asset has been altered or the ledger has been tampered with — and the Merkle chain makes tampering externally detectable even without access to the original file.

## Architecture

The PointSav cryptographic ledger uses C2SP tlog-tiles format — the same on-disk structure used by Certificate Transparency logs and Sigstore Rekor. Tiles are static, base64-encoded text files containing 256 entries each at the leaf level, with intermediate Merkle-level tiles above them. This format is human-readable (consistent with Doctrine Pillar 1: plain text only), independently verifiable, and compatible with standard Certificate Transparency tooling.

Monthly, each tenant's signed checkpoint is submitted to the Sigstore Rekor v2 public transparency log (Doctrine Invention #7 — Sigstore Rekor anchoring). Once anchored, the checkpoint is public and the tenant cannot retroactively alter any prior record without the tampered state being detectable against the anchored checkpoint.

## Applications

The cryptographic ledger applies across all customer-facing data in the platform:

- **Corporate records** — financial entries, compliance documents, and operational logs are all appended to the WORM ledger before any other processing.
- **SOC 2 compliance** — the ledger's append-only invariant and Rekor anchoring satisfy SOC 2 Processing Integrity requirements (PI4 — Outputs are complete, accurate, and timely).
- **Regulatory recordkeeping** — the architecture is structurally aligned with SEC Rule 17a-4(f) broker-dealer electronic recordkeeping requirements (WORM path) and eIDAS qualified preservation service requirements for long-term proof-of-existence.
- **Audit trail** — every read of the ledger is itself logged to an audit sub-ledger, which is also WORM and also anchored.

## See Also

- [[worm-ledger-architecture]]
- [[crypto-attestation]]
- [[capability-based-security]]
- [[compounding-substrate]]
- [[sel4-foundation]]

## References

- `conventions/worm-ledger-design.md` — canonical WORM ledger specification; C2SP tlog-tiles format rationale; four-layer architecture detail
- `DOCTRINE.md §II.7` — Doctrine Invention #7: Integrity Anchor via Sigstore Rekor
- `DOCTRINE.md §IX` — SOC 2 posture and external WORM standard alignment
- `conventions/bcsc-disclosure-posture.md` — audit trail requirements for continuous-disclosure compliance

---
Copyright © 2026 Woodfine Capital Projects Inc.
Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).
PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.