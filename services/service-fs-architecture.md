---
schema: foundry-doc-v1
type: topic
slug: service-fs-architecture
title: "Service-FS Architecture: The WORM Backbone"
category: services
audience: vendor-public
bcsc_class: current-fact
status: active
language: en
last_edited: 2026-05-08
editor: pointsav-engineering
paired_with: service-fs-architecture.es.md
---

Every record written to the PointSav platform — identity anchors, email communications, document artifacts — lands in `service-fs`, a per-tenant Write-Once-Read-Many (WORM) immutable ledger. Once written, records cannot be modified or deleted; the ledger is the tamper-evident backbone that Ring 2 services query and Ring 1 services write to. For a regulated operator, this means every data event has a provable, auditable history from the moment it enters the platform.

## The Four-Layer Architecture

To ensure modularity and survivability, `service-fs` is implemented as a decoupled four-layer stack:

- **L4: Anchoring (Workspace-Tier):** Monthly periodic work that anchors signed checkpoints to the public Sigstore Rekor log.
- **L3: Wire Protocol:** The communication interface (HTTP/axum today; MCP long-term) that enforces per-tenant `moduleId` boundaries.
- **L2: WORM Ledger API (Rust Trait):** The stable core contract (`append`, `read_since`, `checkpoint`) that survives changes to the layers above or below.
- **L1: Tile Storage Primitive:** The envelope-specific storage engine (POSIX on Linux; capability-mediated on seL4) utilizing the **C2SP tlog-tiles** format.

## Dual Boot Envelopes

A core design property of `service-fs` is its ability to operate across two distinct runtime envelopes using the same codebase:

1. **Envelope A (Current):** A Linux/BSD daemon under systemd. It utilizes standard POSIX file I/O and process isolation.
2. **Envelope B (Intended):** A verified seL4 Microkit Protection Domain. It is intended to utilize `moonshot-database` (PSDB) for capability-addressed storage, providing formally verified tenant isolation.

## Durability and Compliance

The platform achieves structural WORM compliance by structurally denying record modification at the storage layer. This is reinforced by:

- **C2SP tlog-tiles:** An open-standard text-based format ensuring 100-year readability.
- **C2SP signed-note Checkpoints:** Compact, signed artifacts that prove the state of the ledger at any point in time.
- **Audit-Log Sub-Ledger:** A dedicated WORM ledger that records every read event to satisfy SOC 2 processing integrity requirements.

This architecture ensures that `service-fs` remains portable, verifiable, and resilient to vendor obsolescence.

## See Also

- [[fs-anchor-emitter]]
- [[service-fs-security-compliance]]
- [[worm-ledger-architecture]]
- [[sel4-foundation]]
