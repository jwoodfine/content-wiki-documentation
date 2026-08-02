---
schema: foundry-doc-v1
title: "Immutable storage and secure backup"
slug: storage
short_description: "The platform enforces hardware-level append-only writes for a tamper-evident record, supporting legal deletion via key destruction and backup via paired secondary drives."
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

**Correction (2026-08-02) — compliance-relevant, escalated:** the "hardware controller" / "drive-level" enforcement claimed throughout this article does not match the real mechanism. Verified against canonical `origin/main`, `service-fs/ARCHITECTURE.md` documents the real enforcement as three layers, none of them hardware: (1) Rust API surface — no public `WormLedger` method removes or modifies an entry; (2) **filesystem level** — finalised tiles are marked read-only (`chmod 0o444`), with `chattr +i` immutability planned as *future* hardening once a systemd unit lands and the operator grants `CAP_LINUX_IMMUTABLE`; (3) cryptographic — a Merkle hash chain and Rekor-anchored checkpoints detect retroactive modification. This is materially weaker than "the hardware controller rejects the write" — a privileged administrator today *can* `chmod` a finalized tile back to writable (detection would still catch it via the hash chain, but the write itself isn't hardware-blocked). No evidence was found anywhere in `service-fs` of a "paired backup drive" cryptographic-pairing scheme or key-destruction-based legal deletion — both confirmed absent, zero hits. This directly contradicts the more careful, filesystem-level framing already correctly stated in this wiki's own `[[worm-ledger-architecture]]` article, which this article cites as its "full specification." Escalated to Command given the compliance stakes (tamper-evidence strength claims for regulated recordkeeping). **Flagged, not resolved.**

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
