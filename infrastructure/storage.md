---
schema: foundry-doc-v1
title: "Immutable storage and secure backup"
slug: storage
short_description: "The platform enforces hardware-level append-only writes to provide an unalterable, tamper-evident record while supporting legal deletion through cryptographic key destruction and backup protection via cryptographically paired secondary drives."
category: infrastructure
type: topic
content_type: topic
quality: complete
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-09
editor: pointsav-engineering
paired_with: storage.es.md
---

The platform is designed to provide auditors and investors with a tamper-evident record: once data is written, it cannot be secretly overwritten or deleted. This property is enforced at the hardware level as part of the [[worm-ledger-design|WORM ledger substrate]], not solely by software policy.

## Key Takeaways

- Append-only enforcement operates at the drive controller level, not software policy. A system administrator with full credentials cannot overwrite or delete existing blocks — the hardware controller rejects the write. This makes the tamper-evident guarantee non-circumventable by internal actors with elevated privileges.
- Legal deletion works through cryptographic key destruction, not ledger modification. The encrypted record's ciphertext remains on disk after the key is destroyed, proving the record existed at the time of writing while making it permanently unreadable. Access-revocation obligations are met without breaking the append-only ledger's structural integrity.
- Backup drives are cryptographically paired with the primary system's identity keys at provisioning time. A drive physically removed from the system produces unreadable ciphertext — protecting against physical theft of backup media without requiring an additional encryption layer.
- Storage immutability is the physical foundation of the [[worm-ledger-architecture|WORM ledger design]]. The ledger specification formalises the four-layer guarantee built on top of this hardware substrate.

## Hardware-enforced append-only writes

Standard storage hardware allows an administrator with sufficient privileges to overwrite or delete any file. The platform's storage subsystem uses drives configured in an append-only mode enforced by the hardware controller. The drive accepts new writes but rejects modification of existing blocks. This produces an unalterable history of every record added to the system — no administrative action can retroactively change what was written.

The append-only property is the foundation of the WORM (Write Once, Read Many) ledger design. See [[worm-ledger-architecture]] for the full ledger specification.

## Legal deletion without breaking the ledger

Some legal frameworks require that specific records be made inaccessible on request. The platform satisfies these requirements without modifying the ledger itself. When a record must be made unreadable:

1. The encryption key for that record is cryptographically destroyed.
2. The record's ciphertext remains on the drive, proving the record existed at the time of writing.
3. The record is permanently unreadable without the key.

This approach maintains the integrity of the append-only ledger while meeting the access-revocation obligations a regulatory authority may impose.

## Paired backup drives

When the primary drive reaches capacity, backup copies are made to a secondary drive that is cryptographically paired with the primary system. A backup drive removed from the primary system produces unreadable ciphertext. This protects against physical theft of backup media.

The pairing is established at provisioning time and is specific to the primary system's identity keys. Restoring from a backup drive requires access to those keys, which are held in the primary system's key store.

## See also

- [[worm-ledger-architecture]] — the full WORM ledger four-layer specification
- [[worm-ledger-design]] — the regulatory compliance mapping and customer key sovereignty rationale
- [[edge-deployment]] — how data is sanitized at the boundary before it reaches storage
