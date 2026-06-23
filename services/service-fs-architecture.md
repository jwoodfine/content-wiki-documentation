---
schema: foundry-doc-v1
type: topic
content_type: topic
slug: service-fs-architecture
short_description: "A per-tenant Write-Once-Read-Many immutable ledger serving as the tamper-evident backbone for all platform records, designed as a four-layer decoupled stack with a Linux runtime envelope today and a planned seL4 microkernel envelope."
title: "FS architecture and the WORM backbone"
category: services
audience: vendor-public
bcsc_class: current-fact
status: active
language: en
last_edited: 2026-06-23
editor: pointsav-engineering
paired_with: service-fs-architecture.es.md
---

Every record written to the PointSav platform — identity anchors, email communications, document artifacts — lands in `service-fs`, a per-tenant Write-Once-Read-Many (WORM) immutable ledger. Once written, records cannot be modified or deleted; the ledger is the tamper-evident backbone that [[three-ring-architecture|Ring 2]] services query and Ring 1 services write to. For a regulated operator, this means every data event has a provable, auditable history from the moment it enters the platform. The [[worm-ledger-design]] article describes the WORM design philosophy in detail.

`service-fs` is not a general-purpose filesystem. A local filesystem permits reads, writes, modifications, and deletions through a standard directory tree. `service-fs` exposes three operations only: `append` (add a record), `read_since` (read forward from a checkpoint), and `checkpoint` (create a signed proof of state). The narrowed API surface is what makes the ledger's integrity guarantees structurally sound rather than policy-enforced.

## The Four-Layer Architecture

To ensure modularity and survivability, `service-fs` is implemented as a decoupled four-layer stack:

- **L4: Anchoring (Workspace-Tier):** Monthly periodic work performed by [[fs-anchor-emitter]] that anchors signed checkpoints to the public Sigstore Rekor log.
- **L3: Wire Protocol:** The communication interface (HTTP/axum today; [[mcp-substrate-protocol|MCP]] long-term) that enforces per-tenant `moduleId` boundaries.
- **L2: WORM Ledger API (Rust Trait):** The stable core contract (`append`, `read_since`, `checkpoint`) that survives changes to the layers above or below.
- **L1: Tile Storage Primitive:** The envelope-specific storage engine (POSIX on Linux; capability-mediated on [[sel4-microkernel-substrate|seL4]]) using the **C2SP tlog-tiles** format.

## Dual Boot Envelopes

`service-fs` is **designed** to operate across two runtime envelopes from one codebase. The [[worm-ledger-storage-architecture|WORM storage architecture]] article describes the intended storage model for each envelope.

1. **Envelope A (Current):** A Linux/BSD daemon under systemd. It uses standard POSIX file I/O and process isolation. This is the only implemented envelope; it exposes `POST /v1/append` and `GET /healthz`.
2. **Envelope B (seL4 — deferred):** A verified [[sel4-microkernel-substrate|seL4]] Microkit Protection Domain is the planned future target. It is intended to use `moonshot-database` (PSDB) for capability-addressed storage, providing formally verified tenant isolation. Envelope B exists only as a reference entry point (`main_sel4_stub.rs`) that is not compiled into the current build.

## Durability and Compliance

The platform achieves structural WORM compliance by structurally denying record modification at the storage layer. This is reinforced by:

- **C2SP tlog-tiles:** An open-standard text-based format ensuring 100-year readability.
- **C2SP signed-note Checkpoints:** Compact, signed artifacts that prove the state of the ledger at any point in time.
- **Audit-Log Sub-Ledger:** A dedicated WORM ledger that records every read event to satisfy SOC 2 processing integrity requirements.

This architecture ensures that `service-fs` remains portable, verifiable, and resilient to vendor obsolescence.

## Key takeaways

- `service-fs` is a WORM ledger, not a filesystem. The implemented API surface is two operations: `append` and health. The `read_since`, `checkpoint`, and proof operations are planned.
- The ledger is per-tenant — each Totebox holds its own isolated ledger; no cross-tenant reads are possible at the storage layer.
- The four-layer architecture is designed to decouple wire protocol, API contract, and storage engine, so the seL4 Envelope B swap does not require rewriting the service.
- The target durability format is open standards: C2SP tlog-tiles (100-year readability) and C2SP signed-note Checkpoints (compact provability). The tile backend is planned; the current build uses a per-tenant JSON append log with per-payload SHA-256 digests.
- Recurring Sigstore Rekor anchoring by [[fs-anchor-emitter]] is **intended** to create an external, publicly verifiable timestamp chain for the entire ledger. The anchoring operation is planned and not yet running.

## See also

- [[fs-anchor-emitter]] — the periodic anchor emitter that checkpoints the ledger to Sigstore Rekor
- [[service-fs-security-compliance]] — compliance profile: SOC 2, WORM regulatory alignment
- [[worm-ledger-architecture]] — infrastructure-level WORM architecture
- [[worm-ledger-design]] — the design philosophy behind the WORM approach
- [[sel4-microkernel-substrate]] — the seL4 Microkit envelope (Envelope B) that is the intended runtime
- [[service-content]] — the Gravity Engine that writes L0 base geometry records to service-fs
- [[service-pointsav-link|PointSav Link Service]] — hot-pluggable adapter connecting os-* nodes to the fleet fabric
