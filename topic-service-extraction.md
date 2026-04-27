# TOPIC: Active Intelligence Router (service-parser)
**Classification:** Totebox Service (Refinery & Router)
**Domain:** pointsav-monorepo

## 1. Abstract
The `service-parser` is the central traffic controller of the Totebox ecosystem. It violently strips proprietary third-party formatting (JSON, MIME, Base64) from raw payloads and constructs machine-readable Entity Bundles.

## 2. The Entity Bundle Protocol
The engine rejects traditional database storage. It isolates every communication into a self-contained Unix directory named via its Timestamp and Routing ID.
* **Structured Plaintext:** The core payload is reduced to an immortal `payload.txt` file utilizing plain-text frontmatter.
* **Binary Decoupling:** Physical attachments (PDFs, Images) are stored natively alongside the text payload, eliminating split-brain metadata tracking.

## 3. The Multi-Path Routing Matrix
The parser dictates the lifecycle of the data based on its physical UI origin tags:
1. **The Immutable Ledger:** Standard assets are finalized and written to cold storage.
2. **The Identity Ledger:** Sender intelligence is appended to a flat-file database for downstream CRM ingestion.
3. **The Ephemeral Purge:** Consumable media (e.g., newsletters) are routed directly to local AI synthesis engines and mathematically deleted from the server, preventing storage bloat.
