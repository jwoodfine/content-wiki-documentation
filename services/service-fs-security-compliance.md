---
schema: foundry-doc-v1
title: "FS security and compliance posture"
slug: service-fs-security-compliance
category: services
type: topic
quality: complete
short_description: "service-fs is engineered for structural Write-Once-Read-Many storage that satisfies SEC Rule 17a-4(f), eIDAS, and SOC 2 — record modification is not denied at the policy layer; it is denied by the storage engine itself, and external Sigstore Rekor anchoring provides proof-of-state independent of the platform's own systems."
status: active
audience: vendor-public
bcsc_class: current-fact
last_edited: 2026-05-08
editor: pointsav-engineering
paired_with: service-fs-security-compliance.es.md
---

`service-fs` is engineered for structural Write-Once-Read-Many storage that meets the requirements of SEC Rule 17a-4(f), eIDAS, and SOC 2 — record modification is not denied at the policy layer; it is denied by the storage engine itself, and external Sigstore Rekor anchoring provides proof-of-state independent of the platform's own systems. The compliance posture follows from architectural properties, not from configurable controls: the Rust storage engine physically lacks the ability to delete or modify records; every entry is cryptographically linked to the next; and any attempt to alter history is detectable through Merkle consistency proofs.

## 1. Regulatory Alignment

The platform’s security posture is designed to satisfy multiple international regulatory frameworks:

* **SEC Rule 17a-4(f):** The platform targets the strict "WORM path," structurally denying record modification. This exceeds the "Audit-Trail" alternative often used by cloud vendors to mask mutable underlying storage.
* **eIDAS (EU 2025/1946):** Aligns with Qualified Preservation standards by ensuring long-term integrity, authenticity, and accessibility "irrespective of future technological changes."
* **SOC 2 Trust Services Criteria:** Directly addresses Processing Integrity (PI1, PI4) through signed ingest and read-audit sub-ledgers, and Logical Access (CC6) via tenant-level isolation.

## 2. Security by Construction

The security of `service-fs` is not a policy layer but a fundamental architectural property:

1. **Structural Immutability:** The Rust API surface and underlying storage engine physically lack the ability to delete or modify records.
2. **Merkle-Chain Integrity:** Every entry is cryptographically linked to the next. Any attempt to alter history is instantly detectable via consistency proofs.
3. **External Witnessing:** Monthly anchoring to the Sigstore Rekor public log provides an irrefutable proof-of-state that is independent of the platform’s internal systems.
4. **Tenant Isolation:** In the intended seL4 deployment, isolation is enforced by microkernel-level capabilities, making cross-tenant access mathematically impossible.

## 3. Data Archive Retrieval Protocol (DARP)

`service-fs` utilizes a plain-text tile format (C2SP tlog-tiles). This ensures 100-year readability, allowing future archivists to decode storage using standard Unix utilities without the need for proprietary software or specific vendor assistance.

## 4. Threat Model Mitigation

The platform’s posture is intended to defend against high-level institutional risks:
* **Operator Tampering:** Even an administrator with root access cannot alter the ledger without breaking the Merkle chain and failing public Rekor consistency checks.
* **Vendor Obsolescence:** Open-standard formats ensure data survival beyond the lifespan of the software vendor.
* **Cryptographic Agility:** The system is designed to transition to post-quantum signature schemes (e.g., Dilithium) without requiring a full storage migration.

## See also

- [[service-fs-architecture]]
- [[capability-based-security]]
- [[machine-based-auth]]
- [[sel4-microkernel-substrate]]
