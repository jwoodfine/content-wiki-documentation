---
schema: foundry-doc-v1
type: topic
content_type: topic
slug: service-fs
title: "service-fs — the WORM ledger backbone"
short_description: "The per-tenant Write-Once-Read-Many immutable ledger that backs every record written to the platform — architecture, durability, and the regulatory posture it enables by construction."
category: services
index_group: ring-1-boundary-ingest
audience: vendor-public
bcsc_class: current-fact
status: active
aliases: [service-fs-architecture, service-fs-security-compliance]
last_edited: 2026-07-31
editor: pointsav-engineering
paired_with: service-fs.es.md
---

Every record written to the PointSav platform — identity anchors, email communications, document artifacts — lands in `service-fs`, a per-tenant Write-Once-Read-Many (WORM) immutable ledger. Once written, records cannot be modified or deleted; the ledger is the tamper-evident backbone that [[three-ring-architecture|Ring 2]] services query and Ring 1 services write to. For a regulated operator, this means every data event has a provable, auditable history from the moment it enters the platform. The [[worm-ledger-design]] article describes the WORM design philosophy in detail.

`service-fs` is not a general-purpose filesystem. A local filesystem permits reads, writes, modifications, and deletions through a standard directory tree. `service-fs` exposes three operations only: `append` (add a record), `read_since` (read forward from a checkpoint), and `checkpoint` (create a signed proof of state). The narrowed API surface is what makes the ledger's integrity guarantees structurally sound rather than policy-enforced — this same structural narrowness is what lets the compliance posture below follow from architecture, not from configurable controls.

## Key takeaways

- `service-fs` is a WORM ledger, not a filesystem. The implemented API surface is two operations: `append` and health. The `read_since`, `checkpoint`, and proof operations are planned. (Correction, 2026-08-02, verified against canonical `origin/main`: this understates real capability — `src/http.rs` also registers `/v1/checkpoint`, `/v1/entries`, `/v1/contract`, and `/mcp` as real, implemented routes, not planned. Flagged, not resolved.)
- The ledger is per-tenant — each Totebox holds its own isolated ledger; no cross-tenant reads are possible at the storage layer.
- Compliance with SEC Rule 17a-4(f), eIDAS, and SOC 2 follows from architectural properties, not configurable controls: the storage engine physically lacks the ability to delete or modify records.
- Recurring Sigstore Rekor anchoring by [[fs-anchor-emitter]] creates an external, publicly verifiable timestamp chain for the entire ledger. **Verified live**: the `local-fs-anchor.timer` systemd unit is active and runs monthly (confirmed against the running system).
- Tenant isolation via microkernel-level capability-based security is the intended [[sel4-microkernel-substrate|seL4]] deployment target, not the current one — today's isolation is process-level, under a standard Linux/BSD daemon.

## The four-layer architecture

To ensure modularity and survivability, `service-fs` is implemented as a decoupled four-layer stack:

- **L4: Anchoring (Workspace-Tier):** Monthly periodic work performed by [[fs-anchor-emitter]] that anchors signed checkpoints to the public Sigstore Rekor log.
- **L3: Wire Protocol:** The communication interface (HTTP/axum today; [[mcp-substrate-protocol|MCP]] long-term) that enforces per-tenant `moduleId` boundaries.
- **L2: WORM Ledger API (Rust Trait):** The stable core contract (`append`, `read_since`, `checkpoint`) that survives changes to the layers above or below.
- **L1: Tile Storage Primitive:** The envelope-specific storage engine (POSIX on Linux; capability-mediated on [[sel4-microkernel-substrate|seL4]]) using the **C2SP tlog-tiles** format.

## Dual boot envelopes

`service-fs` is **designed** to operate across two runtime envelopes from one codebase. The [[worm-ledger-storage-architecture|WORM storage architecture]] article describes the intended storage model for each envelope.

1. **Envelope A (Current):** A Linux/BSD daemon under systemd. It uses standard POSIX file I/O and process isolation. This is the only implemented envelope; it exposes `POST /v1/append` and `GET /healthz`.
2. **Envelope B (seL4 — deferred):** A verified [[sel4-microkernel-substrate|seL4]] Microkit Protection Domain is the planned future target. It is intended to use `moonshot-database` (PSDB) for capability-addressed storage, providing formally verified tenant isolation. Envelope B exists only as a reference entry point (`main_sel4_stub.rs`) that is not compiled into the current build.

## Durability

The target durability format is open standards:

- **C2SP tlog-tiles:** An open-standard text-based format ensuring 100-year readability, allowing future archivists to decode storage using standard Unix utilities without proprietary software or vendor assistance.
- **C2SP signed-note Checkpoints:** Compact, signed artifacts that prove the state of the ledger at any point in time.

The tile backend is planned; the current build uses a per-tenant JSON append log with per-payload SHA-256 digests. An **Audit-Log Sub-Ledger** — a dedicated WORM ledger that records every read event — satisfies SOC 2 processing integrity requirements independently of the tile format's completion.

## Regulatory alignment and compliance

`service-fs`'s security posture is not a policy layer but a fundamental architectural property, designed to satisfy multiple international regulatory frameworks:

- **SEC Rule 17a-4(f):** The platform targets the strict "WORM path," structurally denying record modification. This exceeds the "audit-trail" alternative often used by cloud vendors to mask mutable underlying storage.
- **eIDAS (EU 2025/1946):** Aligns with Qualified Preservation standards, ensuring long-term integrity, authenticity, and accessibility "irrespective of future technological changes."
- **SOC 2 Trust Services Criteria:** Directly addresses Processing Integrity (PI1, PI4) through signed ingest and read-audit sub-ledgers, and Logical Access (CC6) via tenant-level isolation.

Three structural properties underpin this posture:

1. **Structural immutability.** The Rust API surface and underlying storage engine physically lack the ability to delete or modify records.
2. **Merkle-chain integrity.** Every entry is cryptographically linked to the next using [[merkle-proofs-as-substrate-primitive|Merkle consistency proofs]]; any attempt to alter history is instantly detectable.
3. **External witnessing.** Monthly anchoring to the Sigstore Rekor public log by [[fs-anchor-emitter]] provides a proof-of-state independent of the platform's own internal systems.

**Tenant isolation** is the one property still in progress: in the intended [[sel4-microkernel-substrate|seL4]] deployment, isolation is enforced by microkernel-level [[capability-based-security|capability-based security]], making cross-tenant access mathematically impossible. Today, under Envelope A, isolation is process-level under standard Linux/BSD daemon boundaries — a real but weaker guarantee than the seL4 target.

## Threat model mitigation

- **Operator tampering.** Even an administrator with root access cannot alter the ledger without breaking the Merkle chain and failing public Rekor consistency checks. The [[machine-based-auth|machine-based authentication]] system prevents unauthorised signing.
- **Vendor obsolescence.** Open-standard formats ensure data survival beyond the lifespan of the software vendor.
- **Cryptographic agility.** The system is designed to transition to post-quantum signature schemes (e.g., Dilithium) without requiring a full storage migration.

## See also

- [[fs-anchor-emitter]] — the periodic anchor emitter that checkpoints the ledger to Sigstore Rekor
- [[worm-ledger-architecture]] — infrastructure-level WORM architecture
- [[worm-ledger-design]] — the design philosophy behind the WORM approach
- [[sel4-microkernel-substrate]] — the seL4 Microkit envelope (Envelope B) that is the intended runtime
- [[capability-based-security]] — the microkernel-level isolation mechanism targeted for Envelope B
- [[machine-based-auth]] — the authentication system that prevents unauthorised signing
- [[service-content]] — the Gravity Engine that writes L0 base geometry records to service-fs
- [[service-pointsav-link|PointSav Link Service]] — hot-pluggable adapter connecting os-* nodes to the fleet fabric
