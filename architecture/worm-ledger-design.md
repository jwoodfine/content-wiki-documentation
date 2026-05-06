---
schema: foundry-doc-v1
title: "WORM Ledger Design"
slug: worm-ledger-design
category: architecture
type: topic
quality: published
short_description: "The four-layer Write-Once-Read-Many ledger substrate used across PointSav Ring 1 services: a tile-based, hash-chained, cryptographically signed persistence format that satisfies US broker-dealer recordkeeping, EU qualified preservation, and SOC 2 requirements by structure rather than by policy."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-01
editor: pointsav-engineering
cites: []
paired_with: worm-ledger-design.es.md
---

The PointSav platform's Ring 1 services — the boundary ingest layer that handles filesystem records, people data, email, and structured input — require persistence that cannot be silently modified. A record written to a Ring 1 ledger must remain exactly as written for the life of the deployment. No administrator flag, no software upgrade, and no operational intervention should be able to alter a historical record without leaving a cryptographically detectable trace.

This requirement is not unique to PointSav. US broker-dealer recordkeeping regulations under SEC Rule 17a-4(f), EU qualified preservation requirements under the 2025 implementing regulation for eIDAS, and the SOC 2 Trust Services Criteria all specify variants of the same constraint. The platform's WORM ledger design is structured to satisfy all three by the same architectural mechanism — by the storage substrate itself, not by operational policy.

## The four-layer stack

The ledger is built in four layers.

**Layer 1 — Tile storage.** On-disk format follows the C2SP tlog-tiles specification verbatim — the same tile format used internally by Trillian-Tessera and externally by Sigstore Rekor v2. This is not an incidental alignment: it means every tile Foundry writes can be verified by any tool in the transparency-log ecosystem without format conversion.

**Layer 2 — WORM ledger API.** A Rust trait that exposes five operations: open a ledger for a given tenant, append a payload and receive a cursor, read entries since a cursor, produce a signed checkpoint, and verify inclusion and consistency proofs. This trait has an in-memory implementation for testing and a POSIX filesystem implementation for production. A future capability-mediated storage backend can implement the same trait without changing any code above it.

**Layer 3 — Wire protocol.** An HTTP service layer that exposes the ledger API over the network. The MCP server protocol — the 2026 standard for tool-bearing AI services — is layered on top. The same wire shape operates on a standard Linux daemon and on a seL4 Microkit unikernel; the execution envelope changes but the protocol does not.

**Layer 4 — Anchoring.** Monthly publication of tile checkpoints to the Sigstore Rekor v2 transparency log. This produces an external, publicly verifiable record that attests the ledger's state at a point in time. A third-party auditor can confirm a record's integrity without involving the platform operator at all.

## How immutability is enforced structurally

The POSIX filesystem implementation follows a four-step write pattern: write tile bytes to a temporary file, call fsync to commit to disk, rename atomically to the canonical tile path, and set the file mode to 0o444 (owner read, no write). The hash-chain structure of the tile format means any modification to a written tile changes the chain — the next tile's hash record of the previous tile no longer matches. Modification is detectable without an audit log.

Filesystem-level journal mode provides an additional layer. Future deployments running in a hardened systemd environment may add the Linux immutable flag to tile files, which requires an operating-system capability to remove. This is not required for the current production baseline but is available as defense-in-depth.

## Per-tenant structure

Every ledger is associated with a `moduleId` — a tenant identifier that the wire layer enforces on every API call. A request arriving with a `moduleId` that does not match the open ledger is rejected. Tile files are stored under a per-tenant path. Per-tenant signing keys produce per-tenant signed checkpoints, so an auditor inspecting one tenant's ledger need not trust that the vendor has maintained separation between tenants — the cryptographic structure makes that separation verifiable.

## Compliance mapping

**SEC Rule 17a-4(f)** requires records to be preserved in a non-rewriteable, non-erasable format with verifiable timestamps and independent third-party verification capability. The tile format satisfies the first requirement structurally. Each signed checkpoint carries a timestamp field under the per-tenant signing key. Monthly publication to the Rekor transparency log provides third-party verification that does not require the platform operator's cooperation.

**EU qualified preservation under eIDAS** requires long-term preservation independent of future technological changes, integrity preservation, and authentication of the originator. Algorithm agility — the ledger carries an explicit hash-algorithm field in each checkpoint, so migration to a different hash function is a per-tenant decision that does not require rewriting historical tiles — addresses the first requirement. The tile format is an open specification (RFC 9162 and C2SP); it is readable with standard tools that will remain available regardless of what commercial software exists in the future. The second and third requirements are satisfied by the same mechanisms as SEC Rule 17a-4(f).

**SOC 2 Trust Services Criteria.** Logical access controls are enforced at the wire layer via per-tenant `moduleId` validation. System operations are captured via standard process management and log collection. Change management is covered by the audit sub-ledger — a separate ledger instance that records every read and write to the primary ledger, itself a WORM record. Processing integrity is satisfied by the hash chain and public anchoring.

## Dual anchoring and customer sovereignty

Customer ToteboxOS deployments operate their own ledger instances with their own signing keys. The customer is the subject of their own records and holds the signing key that attests them. The vendor workspace independently anchors the same tile checkpoints, providing redundant verifiability: an external auditor can confirm that a customer record appears in both the customer's anchor and the vendor's anchor at the same cryptographic hash. The customer can remove the vendor from the anchoring arrangement at any time; the architecture does not depend on vendor participation for its integrity guarantees.

This structural property — customer key sovereignty with optional vendor redundancy — is not something a managed cloud service can offer, because managed cloud services are architecturally the custodian of both the data and the signing key.

## Implementation state

The `service-fs` Ring 1 service implements the WORM ledger substrate in production. It binds at the standard Ring 1 port, enforces per-tenant `moduleId` separation, and writes tile files following the structural immutability discipline described above. The `/v1/checkpoint` endpoint returns the latest signed checkpoint. Monthly Rekor anchoring of production checkpoints is planned as a formal recurring operation; the format is already compatible.

## See Also

- [[three-ring-architecture]] — the Ring 1 boundary where the WORM ledger operates
- [[compounding-doorman]] — the Ring 3 service whose audit ledger uses the same primitive
- [[trajectory-substrate]] — the training corpus capture that will use the same ledger format when its archival shape stabilises

## References

1. C2SP tlog-tiles specification — <https://c2sp.org/tlog-tiles>
2. C2SP signed-note specification — <https://c2sp.org/signed-note>
3. RFC 9162 — Certificate Transparency Version 2.0 — <https://www.rfc-editor.org/rfc/rfc9162>
4. Sigstore Rekor v2 — <https://rekor.sigstore.dev/>
5. SEC Rule 17a-4(f) — electronic recordkeeping requirements for broker-dealers.
6. Commission Implementing Regulation (EU) 2025/1946 — qualified electronic preservation service requirements under eIDAS.
7. `conventions/worm-ledger-design.md` — source convention for this article.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*

*Woodfine Capital Projects™, Woodfine Management Corp™, PointSav Digital Systems™, Totebox Orchestration™, and Totebox Archive™ are trademarks of Woodfine Capital Projects Inc., used in Canada, the United States, Latin America, and Europe. All other trademarks are the property of their respective owners.*
