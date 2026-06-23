---
schema: foundry-doc-v1
type: topic
content_type: topic
slug: worm-ledger-architecture
title: "WORM ledger substrate: four-layer architecture and two boot envelopes"
short_description: "The per-tenant WORM immutable ledger that all Ring 1 boundary-ingest services write through, built on C2SP tlog-tiles with cryptographic hash-chaining, monthly Sigstore Rekor anchoring, and a dual-envelope design spanning Linux daemon and seL4 unikernel targets."
audience: vendor-public
bcsc_class: current-fact
language: en
paired_with: worm-ledger-architecture.es.md
category: infrastructure
status: active
quality: complete
last_edited: 2026-06-23
editor: pointsav-engineering
---

`service-fs` is the per-tenant Write-Once-Read-Many (WORM) immutable ledger that all customer-facing data lands in first. Every [[three-ring-architecture|Ring 1]] boundary-ingest service — the identity ledger (`service-people`), the communications ledger (`service-email`), the document ingest service (`service-input`) — writes through it. Every Ring 2 knowledge-extraction service reads from it via cursor-paged MCP queries. There is exactly one `service-fs` process per tenant `moduleId`; cross-tenant access is structurally impossible.

This article describes the four-layer architecture, the two operational envelopes (Linux/BSD daemon today; seL4 Microkit unikernel as the intended long-term target), alignment with named external WORM standards, and how Doctrine Invention #7 — monthly Sigstore Rekor anchoring — closes the public-verifiability loop.

## Position in the system

`service-fs` sits at the boundary between the per-tenant data plane and the multi-tenant knowledge plane. The [[three-ring-architecture]] convention names this position explicitly: Ring 1 services are MCP-server processes per tenant; the WORM ledger is the durable backbone they share within a tenant.

```
                    Ring 2 (multi-tenant via moduleId)
                    service-extraction (reader)
                              ▲
                              │ MCP read (cursor-paged)
                              │
              ┌───────────────┴───────────────┐
              │     service-fs                 │
              │     WORM Immutable Ledger      │
              │     per-tenant moduleId        │
              └───────────────▲───────────────┘
                              │ MCP append
              ┌───────────────┼───────────────┐
              │               │               │
       service-people  service-input    service-email
       (Ring 1)        (Ring 1)         (Ring 1)
```

**Current per-tenant boundary:** one daemon process per `moduleId` (separate process address spaces); filesystem permissions restricting per-tenant `FS_LEDGER_ROOT` access; request-time `X-Foundry-Module-ID` header check that rejects mismatched callers with 403.

**Intended long-term boundary:** seL4 microkernel-level capability enforcement, formally verified per the moonshot kernel substrate trajectory.

## The four-layer stack

The architecture is intentionally layered so each layer is independently swappable. The middle layer (L2) is the durable Rust trait contract that survives changes above and below it. The substrate-level four-layer pattern is governed by the workspace WORM ledger design convention (ratified workspace v0.1.7, commit `6c0b79a`); this article describes how `service-fs` specifically applies it.

### L1 — Tile storage primitive (envelope-specific)

The on-disk format is **C2SP tlog-tiles** — the same format used by RFC 9162 v2 (Certificate Transparency v2), Trillian-Tessera, and Sigstore Rekor v2. Tiles are static text files containing 256 entries (or 256 hashes at intermediate Merkle levels), base64-encoded for plain-text inspection per the DARP principle (direct, auditable, reproducible, plain-text).

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

Today's L1 implementation is `PosixTileLedger`: POSIX files under `FS_LEDGER_ROOT`, atomic write-then-rename per tile, fsync after each tile and each checkpoint, finalised tiles marked read-only (mode `0o444`). The intended long-term replacement is `MoonshotDatabaseLedger` over capability-mediated IPC to the `moonshot-database` substrate. The bytes are identical across both — only the I/O mechanism differs.

### L2 — WORM Ledger API (Rust trait, target-independent)

The `LedgerBackend` Rust trait is the durable API contract. Current surface: `open` / `append` / `read_since` / `root` / `checkpoint` / `verify_inclusion` / `verify_consistency`. The append-only invariant lives at the API surface — no public method removes or modifies an entry. An audit-log sub-ledger for ADR-07 read tracking runs behind the same trait (one trait, two instances per tenant).

Two implementations exist today: `InMemoryLedger` (test fixture) and `PosixTileLedger` (production). Both pass an identical 18-test trait-surface suite. Future implementations slot in behind the same trait without touching the wire layer or boot code.

### L3 — Wire protocol (per-tenant, MCP-aware)

Today: axum 0.7 HTTP routes — `GET /healthz`, `GET /readyz`, `GET /v1/contract`, `POST /v1/append`, `GET /v1/entries?since=N`, `GET /v1/checkpoint`, `POST /mcp` for the MCP-server interface. The `X-Foundry-Module-ID` header enforcement runs before any business handler; a mismatch returns 403 with the expected versus supplied moduleId in the response body. The same wire shape serves both boot envelopes.

The intended long-term evolution adds a fuller MCP-server interface: MCP resources for `/v1/checkpoint` and per-tile reads; MCP tools for `/v1/append`. Both wire surfaces (HTTP and MCP) are planned to coexist, so clients may use whichever fits their integration pattern.

### L4 — Anchoring (workspace-tier, monthly)

Doctrine Invention #7 specifies Sigstore Rekor v2 anchoring of per-tenant checkpoints. A monthly cron bundles each tenant's latest signed checkpoint, submits to the Rekor v2 GA endpoint (year-sharded; URL rotates annually), and writes the returned tlog entry back into the originating tenant's ledger as an `anchor-rekor-<unix-ts>` payload. The anchor flow is independent of request-time work — the daemon is stateless about anchoring; it produces signed checkpoints that the workspace anchoring run consumes.

The implementation (`service-fs/anchor-emitter/`) is a standalone Rust binary (own `[workspace]` to avoid openssl-sys conflicts in the parent monorepo). It uses `reqwest` blocking with rustls-tls (no tokio in this binary), generates an ephemeral Ed25519 keypair per anchor, and exits with structured codes (0 success / 1 config / 2 fetch / 3 Rekor / 4 append). The systemd unit (`local-fs-anchor.{service,timer}`) is configured with `OnCalendar=*-*-01 02:30:00`, `Persistent=true`, `RandomizedDelaySec=900`.

## The two boot envelopes

`service-fs` is intended to ship in two envelopes that share the same wire protocol and the same storage format.

### Envelope A — Linux/BSD daemon under systemd (current)

Tokio async runtime, axum 0.7 HTTP server, std Rust. POSIX storage in `FS_LEDGER_ROOT/<moduleId>/`. Per-tenant boundary via separate process address spaces, filesystem permissions, and the wire-layer header check. Deploys as a systemd unit (`infrastructure/local-fs/local-fs.service`). Runs on any Linux or BSD kernel — the Foundry workspace VM, customer on-premises hardware, cloud compute, or inside a Linux/BSD guest VM hosted by seL4 on hardware where seL4 cannot boot natively.

### Envelope B — seL4 Microkit Protection Domain unikernel (intended)

`sel4-microkit` Rust runtime crate (per Microkit 1.3.0, rewritten from Python to Rust). Storage: capability-mediated IPC to `moonshot-database`. Capability tokens are granted per tenant; cross-tenant access requires an explicit capability transfer — formal verification, not a header check. A System Description File declares the Protection Domain's capability allocations and IPC channels per tenant.

The Linux/BSD wrapper case is a real production infrastructure pattern, not a degraded fallback: `libsel4vm` + `libsel4vmmplatsupport` + CAmkES VMM hosts a Linux/BSD guest where Envelope A code runs unchanged, while the seL4 hypervisor provides verified isolation around the guest VM.

### Envelope portability

Wire protocol is identical between envelopes. Storage format is identical. Only the runtime envelope and storage I/O mechanism differ. Migration from Envelope A to Envelope B is a runtime swap, not a data-format migration — every tile authored under POSIX storage is bit-identical to one authored under `moonshot-database` capability-mediated IPC.

## Checkpoint format — C2SP signed-note

The C2SP signed-note format is adopted verbatim — the same format used by Sigstore Rekor v2. A checkpoint is a small text artefact:

```
service-fs.foundry.example
17                                                <-- tree size
HQC1ZP2bbV3Hr1cI4aXxFQ8vQwG4sQYwR0uW4cEAhvA=     <-- root hash (base64 SHA-256)

— foundry-tenant-foundry signed-note-key-id Wm8s...   <-- signature
```

Signed by the per-tenant key (today: workspace administrator key; intended long-term: per-Totebox identity key bound to customer hardware). Witnesses co-sign by appending additional signature lines — the Foundry workspace co-signs every Customer Totebox checkpoint by default; a customer-chosen third party may co-sign additionally.

The signed-note format is plaintext and line-oriented. Signature verification requires only Ed25519 (or a future post-quantum equivalent) — no proprietary toolchain.

## Append flow

1. Client `POST /v1/append` with payload and `X-Foundry-Module-ID` header (and optionally `X-Foundry-Request-ID`).
2. Server validates moduleId against `FS_MODULE_ID` env; rejects with 403 on mismatch.
3. Server generates a monotonic sequence number (cursor) and appends to the in-memory pending buffer.
4. Sequencer batches pending entries (every N ms or M entries — tunable per tenant load profile).
5. On batch finalisation: write leaf tile bytes (atomic write-then-rename, then `fsync`); if a tile boundary is crossed, compute and write any newly-completed intermediate tiles; sign and write a new checkpoint atomically.
6. Return cursor and checkpoint signature to client.

The append-only invariant is enforced at three levels:

- **Rust API surface** — no public `LedgerBackend` method removes or modifies an entry.
- **Filesystem level** — finalised tiles are marked read-only (`0o444`); future hardening via `chattr +i` when the systemd unit is in place and the operator can grant `CAP_LINUX_IMMUTABLE`.
- **Cryptographic level** — the Merkle hash chain detects any retroactive modification; consistency proofs against a Rekor-anchored checkpoint fail publicly if history is altered.

## Read flow (Ring 2 callers)

1. Client `GET /v1/checkpoint` — fetch latest signed tree head.
2. Client `GET /v1/tile/0/xNNN.b64` — fetch specific leaf tile(s) for the cursor range of interest.
3. Client computes inclusion proof locally from intermediate tiles. No server-side database lookup; tiles are CDN-cacheable; verification is independent of the daemon.
4. Server logs the read attempt to the `audit-log/` sub-ledger.

The current skeleton also implements `GET /v1/entries?since=N` as a convenience wrapper that returns entries directly without client-side tile-level proof computation. This is a transitional shape suitable for the in-memory placeholder backend; the post-ratification implementation adds tile-level endpoints alongside.

## ADR-07 audit-log sub-ledger

Every read produces one append to `audit-log/` (its own sub-tile-tree, separate from the data ledger). Each audit entry is JSON: moduleId, request-id, since-cursor, entries-returned, timestamp.

The sub-ledger is itself WORM — auditors can verify retroactively that the audit log has not been tampered with. The sub-ledger checkpoint is anchored alongside the data ledger checkpoint in the monthly Rekor bundle. This satisfies SOC 2 PI4 (Processing Integrity — Outputs) and the requirement that material reads be externally provable.

## Cryptographic agility

Hash function and signature scheme are algorithm-agile to support future migration without reformatting tiles:

- **Today:** SHA-256 hashes, Ed25519 signatures.
- **Hash migration path:** SHA-3 family or BLAKE3 — the checkpoint format includes an algorithm identifier; new tiles use the new hash; checkpoints record both algorithms during the transition period.
- **Signature migration path:** post-quantum candidates (NIST PQC Dilithium or SPHINCS+) — same signed-note format with algorithm-tagged signatures.

This design addresses the eIDAS qualified preservation requirement that proof-of-existence survive irrespective of future technological changes (Article 4(3), Commission Implementing Regulation (EU) 2025/1946) and the platform goal of 100-year readability for every ledger artefact.

## Bootstrapping a new tenant

Per-tenant `FS_LEDGER_ROOT/<moduleId>/` is created on first `open()`:

1. Verify the directory is empty or contains a valid prior state.
2. Initialise an empty leaf tile and a checkpoint at tree size 0, signed by the tenant key.
3. On reload (subsequent `open()` calls): read the latest checkpoint, validate the signature, walk tiles back to recompute the root, and refuse to start if the recomputed root does not match the signed root.

The chain-tampered detection is a hard failure mode. The daemon refuses to start, surfaces the discrepancy to the operator, and waits for manual intervention. Silently re-initialising a tampered ledger would defeat the WORM property; this failure mode is intentional.

## External WORM standards alignment

`service-fs` is structurally aligned with two named external WORM standards alongside the internal SOC 2 and DARP posture:

- **SEC Rule 17a-4(f)** (US broker-dealer electronic recordkeeping; 17 CFR §240.17a-4(f); 2022 amendment effective 2023-05-03 added an Audit-Trail alternative to WORM). The platform targets the WORM path. Compliance is structural: the storage substrate denies modification through cryptographic hash-chain immutability and filesystem-level write-once enforcement, not through policy or process.

- **eIDAS qualified preservation service** (Commission Implementing Regulation (EU) 2025/1946 in force 2026-01-06; ETSI TS 119 511; ETSI EN 319 401 v3.2.1; CEN TS 18170:2025). The plain-text C2SP tlog-tiles format and algorithm-agility design address the Article 4(3) requirement that proof-of-existence survive irrespective of future technological changes.

Neither standard requires formal certification today. The design is alignment-ready; a future audit or qualified-service-provider designation is a planned v1.0.0+ trajectory item conditional on customer demand and corporate posture.

The structural-versus-policy distinction matters. A WORM property maintained by policy is rebuttable. A WORM property maintained by structure — where bytes cannot be modified without breaking a published checkpoint signature — is verifiable by any third party. The structural approach composes: every customer running the same substrate inherits the same property without trusting any promise made by the platform operator.

## What WORM guarantees — and what it does not

**The WORM guarantee covers (current):**
- **Immutability after write.** A record written to the ledger cannot be modified or deleted by any actor, including the platform itself. This is structural, not policy.
- **Tamper evidence at the record level.** Each appended record carries a per-payload SHA-256 digest. Modification of any stored record is detectable by recomputing the digest.

**The WORM guarantee is designed to cover (current tile-format implementation):**
- **Chain-level tamper evidence.** An auditor with the C2SP tile files and a SHA-256 implementation can verify the full hash chain without a live service.
- **External verifiability.** Monthly Sigstore Rekor anchoring creates a public timestamp chain that persists independently of the platform instance.
- **Readability across decades.** The plain-text C2SP tlog-tiles format requires only basic Unix utilities to decode. No proprietary tooling is needed.

**The WORM guarantee does not cover:**
- **Correctness of what was written.** WORM cannot detect or prevent an incorrect record from entering the ledger. Correctness is the responsibility of the human-in-the-loop verification gate at F12, not the storage layer.
- **Availability.** WORM guarantees durability; it does not guarantee that the ledger is reachable at any given moment. Uptime is an infrastructure concern.
- **Search or query access.** The ledger stores records; it does not index them. Full-text search and entity queries are provided by [[service-search]] and [[service-content]].
- **Cross-tenant isolation above the storage layer.** The WORM invariant is per-tenant. Cross-tenant access control is enforced by the wire protocol (`X-Module-ID` boundaries) and is intended to be enforced by seL4 capability mediation in Envelope B.

## Long-term trajectory

The seL4 unikernel envelope (Envelope B) and the `moonshot-database` capability-aware persistence layer are planned v1.0.0+ trajectory items. The migration path is intentional: Envelope A's POSIX backend is intended to remain as the indefinite fallback even after Envelope B ships, because the C2SP tile bytes serialise identically across both backends. Customers running Envelope A receive the same WORM property and the same Rekor anchoring; formally-verified isolation is available by migrating to Envelope B when hardware supports seL4 native boot.

Material assumptions for the seL4 transition: the rust-sel4 and sel4-microkit ecosystem continues maturing (Microkit 1.3.0 was rewritten in Rust during 2025–2026, signalling first-class Rust support); the Sovereign Substrate Phase 2 work for `moonshot-database` lands per the Active Sovereign Replacements roadmap; customer demand for formally-verified isolation justifies the development cost. None of these are guarantees.

## See also

- [[worm-ledger-design]] — regulatory compliance mapping and the structural immutability argument
- [[worm-ledger-storage-architecture]] — storage-layer detail: tile format, atomic durability, and dual-target envelopes
- [[service-fs-architecture]] — the service that implements this architecture as a per-tenant deployed ledger
- [[app-console-input]] — the F12 human-in-the-loop gate that is the quality control upstream of the ledger
- [[sel4-microkernel-substrate]] — the intended seL4 capability-enforcement trajectory for tenant isolation
- [[verify-worm-ledger]] — step-by-step guide: export a tile, verify the hash chain, and validate the signed checkpoint
- [[read-the-command-ledger]] — step-by-step guide: read WORM ledger entries from the F12 LEDGER tab
