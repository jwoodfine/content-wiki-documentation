---
schema: foundry-doc-v1
title: "Foundry WORM Ledger Substrate — Four-Layer Architecture, Two Boot Envelopes"
slug: topic-worm-ledger-architecture
category: architecture
type: topic
quality: complete
short_description: "The Foundry WORM ledger is the per-tenant Write-Once-Read-Many immutable storage layer that all customer-facing data lands in first, built on a four-layer architecture with cryptographic hash-chain enforcement and monthly public anchoring via Sigstore Rekor."
status: pre-build
last_edited: 2026-04-30
editor: pointsav-engineering
cites:
  - c2sp-tlog-tiles
  - c2sp-signed-note
  - rfc-9162
  - sigstore-rekor-v2
  - trillian-tessera
  - sec-17a-4-f
  - eidas-qualified-preservation
  - etsi-ts-119-511
  - etsi-en-319-401
  - cen-ts-18170-2025
  - opentimestamps
  - rfc-3161
  - ni-51-102
  - osc-sn-51-721
paired_with: topic-worm-ledger-architecture.es.md
---

# Foundry WORM Ledger Substrate — Four-Layer Architecture, Two Boot Envelopes

> The Foundry WORM ledger is the per-tenant Write-Once-Read-Many immutable storage layer that all customer-facing data lands in first, built on a four-layer architecture with cryptographic hash-chain enforcement and monthly public anchoring via Sigstore Rekor.

**Foundry's `service-fs`** is the per-tenant Write-Once-Read-Many (WORM) immutable ledger that all customer-facing data lands in first. Every other Ring 1 boundary-ingest service — the identity ledger (`service-people`), the communications ledger (`service-email`), the document ingest service (`service-input`) — writes through it. Every Ring 2 knowledge-extraction service reads from it via cursor-paged MCP queries. There is exactly one `service-fs` process per tenant `moduleId`; cross-tenant access is structurally impossible. The WORM property is enforced at three levels simultaneously: the Rust API surface exposes no method for removing or modifying an entry, the filesystem marks finalised tiles read-only, and the Merkle hash chain makes any retroactive modification detectable by any third party with access to the public Rekor anchor log.

This article describes the four-layer architecture that makes that work, the two operational envelopes (Linux/BSD daemon today, seL4 Microkit unikernel as a planned long-term trajectory item), the structural alignment with named external WORM standards, and how Doctrine Invention #7 — monthly Sigstore Rekor anchoring — closes the public-verifiability loop.

## Position in the System

`service-fs` sits at the boundary between the per-tenant data plane and the multi-tenant knowledge plane. The Three-Ring Architecture convention names this position explicitly: Ring 1 services are MCP-server processes per tenant; the WORM ledger is the durable backbone they share within a tenant.

```
                Ring 2 (multi-tenant via moduleId)
                service-extraction (reader)
                          ▲
                          │ MCP read (cursor-paged)
                          │
          ┌───────────────┴───────────────┐
          │     service-fs                │
          │     WORM Immutable Ledger     │
          │     per-tenant moduleId       │
          └───────────────▲───────────────┘
                          │ MCP append
          ┌───────────────┼───────────────┐
          │               │               │
   service-people  service-input    service-email
   (Ring 1)        (Ring 1)         (Ring 1)
```

Per-tenant boundary today: one daemon process per `moduleId` (separate process address spaces); filesystem permissions restricting per-tenant `FS_LEDGER_ROOT` access; request-time `X-Foundry-Module-ID` header check rejects mismatched callers with 403. Per-tenant boundary in the planned long-term envelope: seL4 microkernel-level capability enforcement, formally verified.

## The Four-Layer Stack

The architecture is intentionally layered so that each layer is independently replaceable. The middle layer (L2) is the durable Rust trait contract that survives changes above and below it. The four-layer pattern is governed by the workspace convention `~/Foundry/conventions/worm-ledger-design.md`.

### L1 — Tile Storage Primitive (envelope-specific)

The on-disk format is C2SP tlog-tiles `[c2sp-tlog-tiles]` — the same format used by RFC 9162 Certificate Transparency v2 `[rfc-9162]`, Trillian-Tessera `[trillian-tessera]`, and Sigstore Rekor v2 `[sigstore-rekor-v2]`. Tiles are static text files containing 256 entries (or 256 hashes at intermediate Merkle levels), base64-encoded for plain-text inspection per Doctrine Pillar 1 (DARP — direct, auditable, reproducible, plain-text).

Concrete on-disk layout per tenant:

```
$FS_LEDGER_ROOT/<moduleId>/
├── checkpoint            — latest signed tree head (signed-note format)
├── tile/0/x000.b64       — leaf tile 0, entries 0–255
├── tile/0/x001.b64       — leaf tile 1, entries 256–511
├── tile/1/x000.b64       — height-1 tile, hashes covering 256 leaves each
├── tile/2/x000.b64       — height-2 tile, hashes covering 65,536 leaves each
└── audit-log/
    ├── checkpoint        — separate sub-ledger for ADR-07 read events
    └── tile/0/x000.b64
```

Today's L1 implementation is `PosixTileLedger` — POSIX files under `FS_LEDGER_ROOT`, atomic write-then-rename per tile, fsync after each tile and each checkpoint, finalised tiles marked read-only (mode `0o444`). The planned long-term replacement is `MoonshotDatabaseLedger` over capability-mediated IPC to the `moonshot-database` substrate per MEMO §7. The bytes are identical across both — only the I/O mechanism differs.

### L2 — WORM Ledger API (Rust trait, target-independent)

The `LedgerBackend` Rust trait is the durable API contract. Current surface: `open` / `append` / `read_since` / `root` / `checkpoint` / `verify_inclusion` / `verify_consistency`. The append-only invariant lives at the API surface — no public method removes or modifies an entry. The audit-log sub-ledger for ADR-07 read tracking is a second instance of the same trait (one trait, two instances per tenant).

Two implementations exist today: `InMemoryLedger` (test fixture) and `PosixTileLedger` (production). Both pass an identical 18-test trait-surface suite. Future implementations slot in behind the same trait without touching wire-layer or boot code.

### L3 — Wire Protocol (per-tenant, MCP-aware)

Today: axum 0.7 HTTP routes — `GET /healthz`, `GET /readyz`, `GET /v1/contract`, `POST /v1/append`, `GET /v1/entries?since=N`, `GET /v1/checkpoint`, `POST /mcp` for the MCP-server interface. The `X-Foundry-Module-ID` header enforcement runs before any business handler; a mismatch returns 403 with the expected versus supplied `moduleId` in the response body. The wire shape is identical across both boot envelopes.

### L4 — Anchoring (workspace-tier, monthly)

Doctrine Invention #7 — Sigstore Rekor v2 anchoring of per-tenant checkpoints. A monthly cron bundles each tenant's latest signed checkpoint, submits to the Rekor v2 GA endpoint `[sigstore-rekor-v2]` (year-sharded; URL rotates annually), and writes the returned tlog entry back into the originating tenant's ledger as an `anchor-rekor-<unix-ts>` payload.

The implementation (`service-fs/anchor-emitter/`) is a standalone Rust binary with its own `[workspace]` to avoid openssl-sys conflicts. It uses `reqwest` blocking + rustls-tls (no tokio), generates an ephemeral Ed25519 keypair per anchor run, and exits with structured codes (0 success / 1 config / 2 fetch / 3 Rekor / 4 append). Master operates the systemd unit (`local-fs-anchor.{service,timer}` with `OnCalendar=*-*-01 02:30:00`); customer Toteboxes receive the same unit pinned at their per-tenant `FS_LEDGER_ROOT`.

## The Two Boot Envelopes

`service-fs` ships in two envelopes that share the same wire protocol and the same storage format.

### Envelope A — Linux/BSD Daemon under systemd (current)

Tokio async runtime, axum 0.7 HTTP server, std Rust. POSIX storage in `FS_LEDGER_ROOT/<moduleId>/`. Per-tenant boundary via separate process address spaces plus filesystem permissions plus the wire-layer header check. Deploys as a systemd unit. Runs anywhere with a Linux or BSD kernel — Foundry workspace VM, customer on-premises hardware, GCE or EC2, and inside a Linux/BSD guest VM hosted by seL4 on hardware where seL4 cannot boot natively.

### Envelope B — seL4 Microkit Protection Domain Unikernel (planned long-term)

`sel4-microkit` Rust runtime crate (per Microkit 1.3.0, rewritten from Python to Rust). Storage: capability-mediated IPC to `moonshot-database` per MEMO §7 Active Sovereign Replacements. Capability tokens are granted per tenant; cross-tenant access requires an explicit capability transfer — formal verification, not a header check.

The Linux/BSD wrapper case is a real production infrastructure pattern, not a degraded fallback. `libsel4vm` and `libsel4vmmplatsupport` plus a CAmkES VMM host a Linux/BSD guest where Envelope A code runs without modification. The seL4 hypervisor provides verified isolation around the guest VM for customers on hardware that does not support native seL4 boot.

### Why the Envelope Boundary Matters

Wire protocol and storage format are identical between envelopes. Customer migration from Envelope A to Envelope B is a runtime swap, not a data-format migration — every tile authored under POSIX storage is bit-identical to one authored under `moonshot-database` capability-mediated IPC. Customers on Envelope A receive the same WORM property and the same Rekor anchoring guarantee as customers on Envelope B; they receive formally-verified isolation by upgrading when their hardware supports native seL4 boot.

## Checkpoint Format — C2SP Signed-Note

Checkpoints adopt the C2SP signed-note format `[c2sp-signed-note]` verbatim. A checkpoint is a small text artefact:

```
service-fs.foundry.example
17                                                <-- tree size
HQC1ZP2bbV3Hr1cI4aXxFQ8vQwG4sQYwR0uW4cEAhvA=     <-- root hash (base64 SHA-256)

— foundry-tenant-foundry signed-note-key-id Wm8s...   <-- signature
```

Signed by the per-tenant key. Witnesses co-sign by appending additional signature lines — the Foundry workspace co-signs every customer Totebox by default per ratified decision D5; the customer may designate a third-party witness additionally.

## Append Flow

1. Client `POST /v1/append` with payload and `X-Foundry-Module-ID` header (and optionally `X-Foundry-Request-ID`).
2. Server validates `moduleId` against `FS_MODULE_ID` environment variable; rejects with 403 on mismatch.
3. Server generates a monotonic sequence number (cursor) and appends to the in-memory pending buffer.
4. Sequencer batches pending entries (every N ms or M entries — tunable per tenant load profile).
5. On batch finalisation: write leaf tile bytes (atomic write-then-rename, then `fsync`); if a tile boundary is crossed, compute and write any newly-completed intermediate tiles; sign and write new checkpoint atomically.
6. Return cursor plus checkpoint signature to client.

The append-only invariant lives at three places simultaneously:

- **Rust API surface** — no public `LedgerBackend` method removes or modifies an entry.
- **Filesystem level** — finalised tiles are marked read-only (`0o444`); planned hardening via `chattr +i` once the systemd unit is deployed and the operator has granted `CAP_LINUX_IMMUTABLE`.
- **Cryptographic level** — the Merkle hash chain detects any retroactive modification; consistency proofs against a Rekor-anchored checkpoint fail publicly if an operator alters history.

## Read Flow (Ring 2 Callers)

1. Client `GET /v1/checkpoint` — fetch the latest signed tree head.
2. Client `GET /v1/tile/0/xNNN.b64` — fetch specific leaf tiles for the cursor range of interest.
3. Client computes inclusion proof locally from intermediate tiles. No server-side database lookup; tiles are CDN-cacheable; verification is independent of the running daemon.
4. Server logs the read attempt to the `audit-log/` sub-ledger.

The current implementation also exposes `GET /v1/entries?since=N` as a convenience wrapper returning entries directly, without requiring the client to compute tile-level proofs.

## ADR-07 Audit-Log Sub-Ledger

Every read produces one append to `audit-log/` — its own sub-tile-tree, separate from the data ledger. Each audit entry is JSON: `moduleId`, `request-id`, `since-cursor`, `entries-returned`, `timestamp`.

The sub-ledger is itself WORM — auditors can verify retroactively that the audit log has not been tampered with. The sub-ledger checkpoint is anchored alongside the data ledger checkpoint in the monthly Rekor bundle. This satisfies SOC 2 PI4 (Processing Integrity — Outputs) and the BCSC continuous-disclosure requirement `[ni-51-102]` that material reads are externally provable.

## Cryptographic Agility

Hash function and signature scheme are algorithm-agile to support future migration without re-formatting existing tiles:

- **Today:** SHA-256 hashes, Ed25519 signatures.
- **Hash migration path:** SHA-3 family or BLAKE3 — the checkpoint format includes an algorithm identifier; new tiles use the new hash; checkpoints record both algorithms during the transition period.
- **Signature migration path:** post-quantum candidates (NIST PQC standardisation — Dilithium, SPHINCS+) — same signed-note format with algorithm-tagged signatures.

This addresses the eIDAS qualified preservation requirement `[eidas-qualified-preservation]` that proof-of-existence survive "irrespective of future technological changes" (Article 4(3) of Commission Implementing Regulation (EU) 2025/1946) and Doctrine Pillar 2 (100-year readability of every Foundry artefact).

## Bootstrapping a New Tenant

Per-tenant `FS_LEDGER_ROOT/<moduleId>/` is created on first `open()`:

1. Verify the directory is empty or contains a valid prior state.
2. Initialise an empty leaf tile and a checkpoint at tree size 0, signed by the tenant key.
3. On subsequent `open()` calls: read the latest checkpoint, validate the signature, walk tiles back to recompute the root, and refuse to start if the recomputed root does not match the signed root.

The tamper-detection failure is a hard failure mode — the daemon refuses to start, surfaces the discrepancy to the operator, and waits for manual intervention. Silently re-initialising a tampered ledger would defeat the WORM property; the hard failure is the correct design choice.

## Structural Alignment with External WORM Standards

`service-fs` is structurally aligned with two named external WORM standards alongside the Foundry-internal SOC 2 and DARP posture documented in `~/Foundry/DOCTRINE.md §IX`. **This section describes structural alignment, not a certification claim.** Neither standard requires formal certification today; the design is alignment-ready.

**SEC Rule 17a-4(f)** `[sec-17a-4-f]` (US broker-dealer electronic recordkeeping; 17 CFR §240.17a-4(f); 2022 amendment effective 2023-05-03). The 2022 amendment introduced an Audit-Trail alternative to WORM; Foundry targets the WORM path. The alignment is structural: the storage substrate denies modification through cryptographic hash-chain immutability plus filesystem-level write-once enforcement. That property is enforced by structure, not by policy.

**eIDAS qualified preservation service** `[eidas-qualified-preservation]` (Commission Implementing Regulation (EU) 2025/1946, in force 2026-01-06; ETSI TS 119 511 `[etsi-ts-119-511]`; ETSI EN 319 401 v3.2.1 `[etsi-en-319-401]`; CEN TS 18170:2025 `[cen-ts-18170-2025]`). Foundry's plain-text C2SP tlog-tiles format `[c2sp-tlog-tiles]` and algorithm-agility design address Article 4(3)'s requirement that proof-of-existence survive "irrespective of future technological changes."

The structural-versus-policy distinction is doctrinally important. A WORM property maintained by policy ("we promise not to modify") is rebuttable. A WORM property maintained by structure ("the bytes cannot be modified without breaking the published checkpoint signature") is verifiable by any third party with access to the public Rekor log.

## Long-Term Trajectory

> **Forward-looking information.** The statements below describe planned and intended development directions. They involve material uncertainties and are not guarantees of future results. Foundry's forward-looking information is governed by the continuous-disclosure posture at `~/Foundry/conventions/bcsc-disclosure-posture.md` per `[ni-51-102]` and `[osc-sn-51-721]`. Actual results may differ materially from the plans described.
>
> Material assumptions: (1) the rust-sel4 and sel4-microkit ecosystem continues to mature; (2) the moonshot-database substrate Phase 2 work lands per the Active Sovereign Replacements roadmap; (3) customer demand for formally-verified isolation justifies the development investment. None of these conditions is guaranteed.

The seL4 unikernel envelope (Envelope B) and the `moonshot-database` capability-aware persistence layer are intended v1.0.0+ trajectory items per MEMO §7 Active Sovereign Replacements. The migration path is intentional: Envelope A's POSIX backend is planned to remain as an indefinite fallback even after Envelope B ships, because the same C2SP tile bytes serialize identically across both backends.

## See Also

- [[compounding-substrate]]
- [[sel4-foundation]]
- [[capability-based-security]]
- [[crypto-attestation]]
- [[cryptographic-ledgers]]

## References

- `conventions/worm-ledger-design.md` — workspace WORM convention (canonical specification)
- `conventions/three-ring-architecture.md` — Ring 1 contract
- `DOCTRINE.md §II.7` — Invention #7 Integrity Anchor
- `DOCTRINE.md §IX` — SOC 2 + external WORM standards
- `clones/project-data/service-fs/RESEARCH.md` — full synthesis with alternatives and ten ratification decisions
- `clones/project-data/service-fs/ARCHITECTURE.md` — durable architecture overview
- `clones/project-data/service-fs/SECURITY.md` — compliance posture mapping
