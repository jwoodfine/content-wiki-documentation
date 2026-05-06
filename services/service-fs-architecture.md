---
schema: foundry-doc-v1
type: topic
slug: service-fs-architecture
title: "Service-FS Architecture: The WORM Backbone"
audience: vendor-public
bcsc_class: current-fact
language: en
paired_with: service-fs-architecture.es.md
## See Also

- [[fs-anchor-emitter]]
- [[service-fs-security-compliance]]
- [[worm-ledger-architecture]]
- [[sel4-foundation]]

---


`service-fs` is the per-tenant Write-Once-Read-Many ({{gli|WORM}}) immutable ledger substrate. It serves as the durable backbone for the Foundry Three-Ring Architecture, providing the primary landing zone for all Ring 1 boundary-ingest services. Every critical record—including identity anchors, email communications, and document artifacts—is persisted through this substrate to guarantee tamper-evidence and long-term availability.

## The Four-Layer Architecture

To ensure modularity and survivability, `service-fs` is implemented as a decoupled four-layer stack:

*   **L4: Anchoring (Workspace-Tier):** Monthly periodic work that anchors signed checkpoints to the public Sigstore Rekor log.
*   **L3: Wire Protocol:** The communication interface (HTTP/axum today; MCP long-term) that enforces per-tenant `moduleId` boundaries.
*   **L2: {{gli|WORM}} Ledger API (Rust Trait):** The stable core contract (`append`, `read_since`, `checkpoint`) that survives changes to the layers above or below.
*   **L1: Tile Storage Primitive:** The envelope-specific storage engine (POSIX on Linux; capability-mediated on seL4) utilizing the **C2SP tlog-tiles** format.

## Dual Boot Envelopes

A core innovation of `service-fs` is its ability to operate across two distinct runtime envelopes using the same codebase:

1.  **Envelope A (Current):** A Linux/BSD daemon under systemd. It utilizes standard POSIX file I/O and process isolation.
2.  **Envelope B (Intended):** A verified seL4 Microkit Protection Domain. It is intended to utilize `moonshot-database` (PSDB) for capability-addressed storage, providing formally verified tenant isolation.

## Durability and Compliance

Foundry achieves structural {{gli|WORM}} compliance by structurally denying record modification at the storage layer. This is reinforced by:
*   **C2SP tlog-tiles:** An open-standard text-based format ensuring 100-year readability.
*   **C2SP signed-note Checkpoints:** Compact, signed artifacts that prove the state of the ledger at any point in time.
*   **Audit-Log Sub-Ledger:** A dedicated {{gli|WORM}} ledger that records every read event to satisfy SOC 2 processing integrity requirements.

This architecture ensures that `service-fs` remains portable, verifiable, and resilient to vendor obsolescence.


---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*

*Woodfine Capital Projects™, Woodfine Management Corp™, PointSav Digital Systems™, Totebox Orchestration™, and Totebox Archive™ are trademarks of Woodfine Capital Projects Inc., used in Canada, the United States, Latin America, and Europe. All other trademarks are the property of their respective owners.*
