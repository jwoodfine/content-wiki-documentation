---
schema: foundry-doc-v1
type: topic
slug: service-fs-security-compliance
title: Service-FS Security and Compliance Posture
audience: vendor-public
bcsc_class: current-fact
language: en
paired_with: service-fs-security-compliance.es.md
---

# Service-FS Security and Compliance Posture

`service-fs` is engineered to meet the highest international standards for immutable storage and data sovereignty. By implementing a structural {{gli|WORM}} (Write-Once-Read-Many) architecture, Foundry provides a verifiable assurance that data records are non-rewriteable and non-erasable, satisfying the core requirements of global financial and trust regulations.

## 1. Regulatory Alignment

Foundry’s security posture is designed to satisfy multiple international regulatory frameworks:

*   **SEC Rule 17a-4(f):** Foundry targets the strict "{{gli|WORM}} path," structurally denying record modification. This exceeds the "Audit-Trail" alternative often used by cloud vendors to mask mutable underlying storage.
*   **eIDAS (EU 2025/1946):** Aligns with Qualified Preservation standards by ensuring long-term integrity, authenticity, and accessibility "irrespective of future technological changes."
*   **SOC 2 Trust Services Criteria:** Directly addresses Processing Integrity (PI1, PI4) through signed ingest and read-audit sub-ledgers, and Logical Access (CC6) via tenant-level isolation.

## 2. Security by Construction

The security of `service-fs` is not a policy layer but a fundamental architectural property:

1.  **Structural Immutability:** The Rust API surface and underlying storage engine physically lack the ability to delete or modify records.
2.  **Merkle-Chain Integrity:** Every entry is cryptographically linked to the next. Any attempt to alter history is instantly detectable via consistency proofs.
3.  **External Witnessing:** Monthly anchoring to the Sigstore Rekor public log (Doctrine Invention #7) provides an irrefutable proof-of-state that is independent of Foundry’s internal systems.
4.  **Tenant Isolation:** In the intended seL4 deployment, isolation is enforced by microkernel-level capabilities, making cross-tenant access mathematically impossible.

## 3. Data Archive Retrieval Protocol (DARP)

In alignment with Doctrine Pillar 1, `service-fs` utilizes a plain-text tile format (C2SP tlog-tiles). This ensures 100-year readability, allowing future archivists to decode storage using standard Unix utilities without the need for proprietary software or specific vendor assistance.

## 4. Threat Model Mitigation

Foundry’s posture is intended to defend against high-level institutional risks:
*   **Operator Tampering:** Even an administrator with root access cannot alter the ledger without breaking the Merkle chain and failing public Rekor consistency checks.
*   **Vendor Obsolescence:** Open-standard formats ensure data survival beyond the lifespan of the software vendor.
*   **Cryptographic Agility:** The system is designed to transition to post-quantum signature schemes (e.g., Dilithium) without requiring a full storage migration.
