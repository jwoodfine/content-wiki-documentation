---
schema: foundry-doc-v1
title: "WORM ledger design"
slug: worm-ledger-design
category: infrastructure
type: topic
quality: complete
short_description: "The four-layer Write-Once-Read-Many ledger substrate used across PointSav Ring 1 services: a tile-based, hash-chained, cryptographically signed persistence format that satisfies US broker-dealer recordkeeping, EU qualified preservation, and SOC 2 requirements by structure rather than by policy."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-22
editor: pointsav-engineering
forward_looking: true
cites:
 - c2sp-tlog-tiles
 - c2sp-signed-note
 - sigstore-rekor-v2
 - rfc-9162
 - sec-17a-4-f
references:
 - id: 1
 text: "C2SP. 'tlog-tiles: Tile-based logs specification.' C2SP.org, 2024."
 url: "https://c2sp.org/tlog-tiles"
 - id: 2
 text: "Sigstore Project. 'Rekor — Software Supply Chain Transparency Log.' Sigstore.dev, 2024."
 url: "https://rekor.sigstore.dev/"
 - id: 3
 text: "C2SP. 'signed-note: Signed checkpoint note format.' C2SP.org, 2024."
 url: "https://c2sp.org/signed-note"
 - id: 4
 text: "Laurie, B. et al. 'RFC 9162: Certificate Transparency Version 2.0.' IETF, 2021."
 url: "https://www.rfc-editor.org/rfc/rfc9162"
paired_with: worm-ledger-design.es.md
---

A regulated firm's records are only as trustworthy as the weakest hand that can reach them. An administrator flag, a software upgrade, a backup restore — any of these can silently alter a historical record. A policy that promises they will not is not the same as a structure that does not let them.

PointSav's [[three-ring-architecture|Ring 1 services]] persist every boundary record — filesystem, people data, email, structured input — to a Write-Once-Read-Many ledger via [[service-fs-architecture|the service-fs substrate]]. <!--claim id=tile-format-c2sp cites=[c2sp-tlog-tiles] valid_at=2024 confidence=established-->The on-disk format follows the C2SP tlog-tiles transparency-log specification verbatim; every record is hash-chained, so any modification to a written record breaks the chain.<!--/claim-->

<!--claim id=immutability-structural confidence=structural cites=[]-->The ledger is built in four layers — tile storage, a WORM API, a wire protocol, and monthly anchoring of signed checkpoints to a public transparency log. Immutability is a property of the storage substrate, not of operational policy.<!--/claim-->

For a regulated buyer the consequence is concrete. One architecture satisfies three recordkeeping regimes at once — US broker-dealer rules under SEC Rule 17a-4(f), EU qualified preservation under eIDAS, and the SOC 2 Trust Services Criteria — and an external auditor can verify any record without the platform operator's cooperation.

## The four-layer stack

The ledger is built in four layers.

**Layer 1 — tile storage.** <!--claim id=tile-ecosystem cites=[c2sp-tlog-tiles,sigstore-rekor-v2] confidence=established-->The on-disk format is the C2SP tlog-tiles specification [^1] — the same tile format used internally by Trillian-Tessera and externally by Sigstore Rekor v2 [^2].<!--/claim--> The alignment is deliberate: every tile the platform writes can be verified by any tool in the transparency-log ecosystem, with no format conversion.

**Layer 2 — WORM ledger API.** A Rust trait exposes five operations: open a ledger for a tenant, append a payload and receive a cursor, read entries since a cursor, produce a signed checkpoint [^3], and verify inclusion and consistency proofs. The trait has an in-memory implementation for testing and a POSIX filesystem implementation for production. A future capability-mediated storage backend can implement the same trait with no change to any code above it.

**Layer 3 — wire protocol.** An HTTP service layer exposes the ledger API over the network, with the MCP server protocol — the 2026 standard for tool-bearing AI services — layered on top. The same wire shape runs on a standard Linux daemon and on a seL4 Microkit unikernel; the execution envelope changes, the protocol does not.

**Layer 4 — anchoring.** <!--claim id=external-anchor cites=[sigstore-rekor-v2] confidence=established-->Tile checkpoints are published monthly to the Sigstore Rekor v2 transparency log, an external and publicly verifiable record of the ledger's state at a point in time.<!--/claim--> A third-party auditor can confirm a record's integrity without involving the platform operator.

## How immutability is enforced structurally

The POSIX filesystem implementation follows a four-step write pattern: write the tile bytes to a temporary file, call `fsync` to commit to disk, rename atomically to the canonical tile path, and set the file mode to read-only. <!--claim id=hash-chain-detection confidence=structural cites=[]-->The hash-chain structure of the tile format means any modification to a written tile changes the chain — the next tile's recorded hash of the previous tile no longer matches. Modification is detectable without a separate audit log.<!--/claim-->

Filesystem journal mode adds a second layer. A deployment running in a hardened systemd environment may also set the Linux immutable flag on tile files, which requires an operating-system capability to remove. This is defence-in-depth, not a requirement of the current production baseline.

## Per-tenant structure

<!--claim id=per-tenant-moduleid confidence=structural cites=[]-->Every ledger is bound to a `moduleId` — a tenant identifier the wire layer enforces on every API call. A request whose `moduleId` does not match the open ledger is rejected. Tile files are stored under a per-tenant path, and per-tenant signing keys produce per-tenant signed checkpoints.<!--/claim-->

An auditor inspecting one tenant's ledger therefore need not trust that the vendor maintained separation between tenants. The cryptographic structure makes the separation verifiable.

## Compliance mapping

**SEC Rule 17a-4(f)** <!--claim id=sec-mapping cites=[sec-17a-4-f] confidence=established-->requires records to be preserved in a non-rewriteable, non-erasable format with verifiable timestamps and an independent third-party verification capability.<!--/claim--> The tile format satisfies the format requirement structurally. Each signed checkpoint carries a timestamp under the per-tenant signing key. Monthly publication to the Rekor transparency log supplies third-party verification that does not need the operator's cooperation.

**EU qualified preservation under eIDAS** requires long-term preservation independent of future technological change, integrity preservation, and authentication of the originator. The ledger carries an explicit hash-algorithm field in each checkpoint, so migrating to a different hash function is a per-tenant decision that does not require rewriting historical tiles. The tile format is an open specification — RFC 9162 [^4] and C2SP — readable with standard tools that remain available regardless of future commercial software. Integrity and originator authentication use the same mechanisms as the SEC mapping.

**SOC 2 Trust Services Criteria.** Logical access control is enforced at the wire layer by per-tenant `moduleId` validation. Change management is covered by the audit sub-ledger — a separate ledger instance that records every read and write to the primary ledger, itself a WORM record. Processing integrity rests on the hash chain and the public anchor.

## Dual anchoring and customer sovereignty

A customer's ToteboxOS deployment runs its own ledger instances with its own signing keys. <!--claim id=customer-key-sovereignty confidence=structural cites=[]-->The customer is the subject of its own records and holds the signing key that attests them. The vendor workspace independently anchors the same tile checkpoints, giving redundant verifiability; the customer can remove the vendor from the anchoring arrangement at any time, and the integrity guarantee does not depend on vendor participation.<!--/claim-->

This property — customer key sovereignty with optional vendor redundancy — is not something a managed cloud service can offer. A managed cloud service is architecturally the custodian of both the data and the signing key.

## Implementation state

The `service-fs` Ring 1 service implements the WORM ledger substrate in production. It binds at the standard Ring 1 port, enforces per-tenant `moduleId` separation, and writes tile files following the structural immutability discipline above. The `/v1/checkpoint` endpoint returns the latest signed checkpoint. <!--claim id=monthly-anchor-planned confidence=projected cites=[sigstore-rekor-v2] valid_at=2026-->Monthly Rekor anchoring of production checkpoints is planned as a formal recurring operation; the checkpoint format is already compatible.<!--/claim-->

## See also

- [[three-ring-architecture]] — the Ring 1 boundary where the WORM ledger operates
- [[worm-ledger-architecture]] — the four-layer architectural integration: tile storage, WORM API, wire protocol, anchoring
- [[worm-ledger-storage-architecture]] — storage-layer detail: C2SP tlog-tiles format, atomic write discipline, dual-target runtime
- [[service-fs-architecture]] — the `service-fs` implementation that runs this substrate in production
- [[compounding-doorman]] — the Ring 3 service whose audit ledger uses the same primitive
- [[trajectory-substrate]] — the training-corpus capture that will use the same ledger format when its archival shape stabilises
