---
schema: foundry-doc-v1
type: topic
content_type: topic
slug: worm-ledger-storage-architecture
short_description: "The storage architecture specifies C2SP tlog-tiles as the target storage primitive; the current service-fs build persists a per-tenant JSON append log pending the tile backend, with structural immutability and long-term readability as the intended design."
title: "WORM ledger storage architecture"
audience: vendor-public
bcsc_class: current-fact
language: en
paired_with: worm-ledger-storage-architecture.es.md
category: infrastructure
status: active
quality: complete
last_edited: 2026-06-23
editor: pointsav-engineering
---

The WORM ledger storage architecture describes how the [[worm-ledger-design|platform’s immutable ledger]] persists data to disk — and why the specific format and write discipline matter for long-term regulatory compliance. The storage layer **specifies** the C2SP tlog-tiles specification as its target primitive per the [[worm-ledger-architecture|four-layer ledger architecture]]. The current `service-fs` implementation persists records as a newline-delimited JSON append log (`log.jsonl`) with per-payload SHA-256 digests, pending the tile backend.

## 1. The tile-based storage engine

The storage architecture **specifies** the **C2SP tlog-tiles** format as its target storage primitive. This format, used by Sigstore Rekor and Google’s Certificate Transparency, breaks a Merkle tree into static, append-only files (tiles). The tile backend is planned and not yet implemented; the current deployment uses a per-tenant JSON append log.

* **Atomic Durability (current):** Records are written to a temporary file, synchronised with `fsync`, and renamed atomically to the canonical path. This ensures that partial writes never corrupt the ledger state.
* **Plain-Text Transparency (planned):** Under the target tile format, tiles are stored as newline-delimited base64 text, inspectable using standard Unix utilities (`cat`, `base64`, `sha256sum`).
* **Merkle-Based Integrity (planned):** The design chains every entry into a Merkle structure to allow inclusion proofs and consistency checks. **This is the intended model — the current `service-fs` build records per-payload digests and does not yet construct a Merkle tree or serve proofs.**

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

- [[worm-ledger-architecture]] — the four-layer architectural overview: tile storage, WORM API, wire protocol, anchoring
- [[worm-ledger-design]] — regulatory compliance mapping and customer key sovereignty rationale
- [[service-fs-architecture]] — the `service-fs` implementation that applies this storage architecture in production
- [[cryptographic-ledgers]] — the broader cryptographic ledger context for the C2SP tlog-tiles format
