---
schema: foundry-doc-v1
type: topic
slug: worm-ledger-storage-architecture
short_description: "The storage architecture adopts C2SP tlog-tiles as its fundamental primitive, supporting dual-target deployment from Linux daemons to seL4 microkernels while ensuring structural immutability and long-term readability through plain-text transparency and atomic durability."
title: "WORM ledger storage architecture"
audience: vendor-public
bcsc_class: current-fact
language: en
paired_with: worm-ledger-storage-architecture.es.md
category: infrastructure
status: active
quality: complete
last_edited: 2026-05-25
editor: pointsav-engineering
---

The WORM ledger storage architecture describes how the platform’s immutable ledger persists data to disk — and why the specific format and write discipline matter for long-term regulatory compliance. The storage layer adopts the C2SP tlog-tiles specification as its fundamental primitive, producing a tile-based, append-only store that remains verifiable and human-readable with standard Unix utilities for at least a century.

## 1. The tile-based storage engine

The platform adopts the **C2SP tlog-tiles** specification as its fundamental storage primitive. This format, used by Sigstore Rekor and Google’s Certificate Transparency, breaks a Merkle tree into static, append-only files (tiles).

* **Atomic Durability:** Finalized tiles are written using a write-then-rename discipline followed by a mandatory `fsync`. This ensures that partial writes never corrupt the ledger state.
* **Plain-Text Transparency:** Following the DARP principle, tiles are stored as newline-delimited base64 text. This ensures that the storage remains inspectable using standard Unix utilities (`cat`, `base64`, `sha256sum`).
* **MERKLE-Based Integrity:** Every entry is chained into a Merkle DAG, allowing for efficient inclusion proofs and consistency checks without re-reading the entire ledger.

## 2. Dual-target runtime envelopes

The architecture is designed to support two distinct operational environments using the same codebase:

### Envelope A: Hosted Daemon (Current)
Running as a standard Linux/BSD process, `service-fs` uses POSIX file I/O for storage. Per-tenant isolation is enforced through separate process address spaces and strict filesystem permissions.

### Envelope B: seL4 Unikernel (Intended)
The long-term trajectory involves deploying `service-fs` as an seL4 Microkit Protection Domain. In this envelope, storage is mediated by `moonshot-database` (PSDB), where access is governed by formally verified microkernel capabilities.

## 3. Cryptographic and compliance alignment

The storage engine is engineered to satisfy strict regulatory requirements:
* **SEC 17a-4(f):** Satisfies the "WORM path" by structurally denying modification at the storage layer.
* **eIDAS Qualified Preservation:** Ensures 100-year readability through open-standard plain-text encodings and algorithm-agile hash functions.
* **SOC 2 Processing Integrity:** Provides verifiable audit trails through a dedicated sub-ledger that records every read event.

## 4. Portability and sovereignty

The tile-based logs are portable, open-standard, and self-verifying across any hardware — from a virtual machine running as a Linux daemon today to an seL4-hardened ToteboxOS appliance in a future deployment. No proprietary hardware and no specific cloud vendor is required to verify or restore the ledger.

## See also

- [[worm-ledger-architecture]]
- [[worm-ledger-design]]
- [[service-fs-architecture]]
- [[cryptographic-ledgers]]
