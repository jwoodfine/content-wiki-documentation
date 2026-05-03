---
schema: foundry-doc-v1
type: topic
slug: worm-ledger-storage-architecture
title: WORM Ledger Storage Architecture
audience: vendor-public
bcsc_class: current-fact
language: en
paired_with: worm-ledger-storage-architecture.es.md
---

# WORM Ledger Storage Architecture

Foundry’s storage architecture is built on the principle of structural immutability, ensuring that data archives remain tamper-evident and readable for the long term. This document synthesizes the engineering decisions behind the tile-based storage engine and the transition from hosted environments to verified microkernels.

## 1. The Tile-Based Storage Engine

Foundry adopts the **C2SP tlog-tiles** specification as its fundamental storage primitive. This format, utilized by Sigstore Rekor and Google’s Certificate Transparency, breaks a Merkle tree into static, append-only files (tiles).

*   **Atomic Durability:** Finalized tiles are written using a write-then-rename discipline followed by a mandatory `fsync`. This ensures that partial writes never corrupt the ledger state.
*   **Plain-Text Transparency:** In alignment with Doctrine Pillar 1 (DARP), tiles are stored as newline-delimited base64 text. This ensures that the storage remains inspectable using standard Unix utilities (`cat`, `base64`, `sha256sum`).
*   **MERKLE-Based Integrity:** Every entry is chained into a Merkle DAG, allowing for efficient inclusion proofs and consistency checks without re-reading the entire ledger.

## 2. Dual-Target Runtime Envelopes

The architecture is designed to support two distinct operational environments using the same codebase:

### Envelope A: Hosted Daemon (Current)
Running as a standard Linux/BSD process, `service-fs` utilizes POSIX file I/O for storage. Per-tenant isolation is enforced through separate process address spaces and strict filesystem permissions.

### Envelope B: seL4 Unikernel (Intended)
The long-term trajectory involves deploying `service-fs` as an seL4 Microkit Protection Domain. In this envelope, storage is mediated by `moonshot-database` (PSDB), where access is governed by formally verified microkernel capabilities.

## 3. Cryptographic and Compliance Alignment

The storage engine is engineered to satisfy strict regulatory requirements:
*   **SEC 17a-4(f):** Satisfies the "WORM path" by structurally denying modification at the storage layer.
*   **eIDAS Qualified Preservation:** Ensures 100-year readability through open-standard plain-text encodings and algorithm-agile hash functions.
*   **SOC 2 Processing Integrity:** Provides verifiable audit trails through a dedicated sub-ledger that records every read event.

## 4. Synthesis of Innovation

The primary innovation in Foundry’s storage layer is the integration of high-performance verifiable logs with a "sovereign-first" deployment model. Unlike legacy WORM solutions that require proprietary hardware or specific cloud vendors, Foundry’s tile-based logs are portable, open-standard, and self-verifying across any hardware from a virtual machine to an seL4-hardened Totebox appliance.


---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*

*Woodfine Capital Projects™, Woodfine Management Corp™, PointSav Digital Systems™, Totebox Orchestration™, and Totebox Archive™ are trademarks of Woodfine Capital Projects Inc., used in Canada, the United States, Latin America, and Europe. All other trademarks are the property of their respective owners.*
