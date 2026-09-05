---
schema: foundry-doc-v1
type: topic
content_type: topic
slug: service-fs
title: "service-fs — the WORM ledger backbone"
short_description: "The per-tenant Write-Once-Read-Many immutable ledger that backs every record written to the platform — a real, implemented HTTP and MCP interface over a hash-chained append log, with monthly external anchoring to a public transparency log."
category: services
index_group: ring-1-boundary-ingest
quality: complete
audience: vendor-public
bcsc_class: current-fact
language_protocol: PROSE-TOPIC
status: active
aliases: [service-fs-architecture, service-fs-security-compliance]
last_edited: 2026-09-05
editor: pointsav-engineering
paired_with: service-fs.es.md
---

Every record written to the PointSav platform — identity anchors, email communications, document artifacts — lands in `service-fs`, a per-tenant Write-Once-Read-Many (WORM) immutable ledger. Once written, records cannot be modified or deleted; the ledger is the tamper-evident backbone that [[three-ring-architecture|Ring 2]] services query and Ring 1 services write to. The [[worm-ledger-design]] article describes the WORM design philosophy in detail.

`service-fs` is not a general-purpose filesystem. A local filesystem permits reads, writes, modifications, and deletions through a standard directory tree. `service-fs` exposes a narrow, append-and-verify surface: writing a new record, reading forward from a point in the log, and producing a signed proof of the ledger's current state — plus the cryptographic operations that let a caller verify a specific entry or confirm two checkpoints are consistent with each other. This narrow surface is what makes the ledger's integrity guarantees structurally sound rather than policy-enforced.

## Key takeaways

- The service exposes append, read, checkpoint, and both single-entry and cross-checkpoint verification, over HTTP and over MCP — all implemented, not planned.
- The ledger is per-tenant — each Totebox holds its own isolated ledger; no cross-tenant reads are possible at the storage layer.
- Every entry chains cryptographically into the one before it (a linear SHA-256 hash chain), and a dedicated audit-log sub-ledger records every read event alongside the primary record ledger.
- Recurring Sigstore Rekor anchoring by [[fs-anchor-emitter]] creates an external, publicly verifiable timestamp chain for the entire ledger, running on a monthly cadence.
- Today's deployment is a standard Linux/BSD daemon with process-level isolation — a real but weaker guarantee than a microkernel-enforced boundary would provide. A seL4 microkernel envelope was explored as a bare-metal unikernel design under this same package name; that design now lives in its own separate vendor package, and no seL4 target is under active development inside the current `service-fs` codebase.

## The layered architecture

`service-fs` separates concerns into layers that can change independently:

- **Anchoring:** monthly work performed by [[fs-anchor-emitter]], anchoring signed checkpoints to the public Sigstore Rekor log.
- **Wire protocol:** an HTTP interface (via axum) and an MCP server interface, both exposing the same underlying operations to different kinds of callers.
- **Ledger contract:** a stable Rust trait — append, read since a cursor, checkpoint, and both proof operations — that the wire layer and the storage layer both compose against, so either can change without breaking the other.
- **Storage:** today, a per-tenant POSIX-file-based hash-chain log using the C2SP tlog-tiles format for the on-disk tile structure and C2SP signed-note format for checkpoints.

## Durability

The ledger's on-disk format follows open standards rather than a proprietary schema — C2SP tlog-tiles for the log itself, C2SP signed-note for checkpoints — so a future reader could decode the raw files with standard tools even without the platform's own software. Every write also lands in the audit-log sub-ledger, an independent WORM record of read activity alongside the primary data.

## Threat model

- **Operator tampering.** Even an administrator with direct access to the storage can't alter a past record without breaking the hash chain — and a broken chain is detectable both locally and against the externally-anchored Rekor checkpoints.
- **Vendor obsolescence.** The open-standard on-disk format is designed to outlast any particular vendor's software.

## See also

- [[fs-anchor-emitter]] — the periodic anchor emitter that checkpoints the ledger to Sigstore Rekor
- [[worm-ledger-design]] — the design philosophy behind the WORM approach
- [[machine-based-auth]] — the authentication system that governs who can act on the ledger's behalf
- [[service-content]] — a Ring 2 consumer of records `service-fs` holds
