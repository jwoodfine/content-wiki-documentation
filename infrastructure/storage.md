---
schema: foundry-topic-v1
title: "Immutable Storage and Secure Backup"
slug: storage
category: infrastructure
status: published
last_edited: 2026-04-30
editor: pointsav-engineering
---

The platform is designed to provide auditors and investors with a tamper-evident record: once data is written, it cannot be secretly overwritten or deleted. This property is enforced at the hardware level, not solely by software policy.

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

- [[worm-ledger-architecture]] — the full WORM ledger specification
- [[architecture]] — archive portability and sovereign bootability
- [[edge-deployment]] — how data enters the system before reaching storage

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
