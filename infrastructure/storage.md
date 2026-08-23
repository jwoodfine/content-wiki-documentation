---
schema: foundry-doc-v1
title: "Immutable storage and secure backup"
slug: storage
short_description: "The platform's tamper-evident record rests on filesystem read-only permissions and a cryptographic hash chain, not a hardware write-block — a privileged administrator can still bypass it, and any bypass is detectable, not prevented."
category: infrastructure
index_group: storage-substrate
type: topic
content_type: topic
quality: complete
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-09
editor: pointsav-engineering
paired_with: storage.es.md
---

The platform is designed to provide auditors and investors with a tamper-evident record: any retroactive change to written data is detectable. Detectable is the accurate word — the guarantee rests on filesystem permissions and cryptography, not a hardware write-block that would make a bypass impossible outright.

## Key Takeaways

- Append-only enforcement operates in three layers, none of them hardware: the ledger's own API surface (no method removes or modifies an entry), filesystem permissions (a finalized record is marked read-only), and cryptography (a hash chain plus externally-anchored checkpoints). A privileged administrator with root access can still change the underlying file permissions and edit a finalized record — the guarantee is that doing so breaks the hash chain and is therefore detectable, not that the write itself is blocked.
- There is no cryptographic-key-destruction path for legal deletion, and no cryptographically-paired backup-drive scheme. Neither exists in the platform today.
- Storage immutability is the foundation of the [[worm-ledger-architecture|WORM ledger design]]. The ledger specification formalises the full guarantee built on top of this filesystem-and-cryptography substrate.

## Filesystem- and cryptography-enforced append-only writes

The platform's storage subsystem marks each finalized record read-only at the filesystem level once it's written, and chains every record's hash into the one before it. Reversing a write means either restoring root privileges to change the file's permissions and content, or accepting that the hash chain — and any checkpoint already anchored to a public transparency log — will no longer match. Neither path is blocked outright; both are detectable after the fact.

The append-only property is the foundation of the WORM (Write Once, Read Many) ledger design. See [[worm-ledger-architecture]] for the full ledger specification.

## Legal deletion

The platform has no cryptographic-key-destruction mechanism for making a specific record unreadable on request. Any legal-deletion obligation today has to be met by a process outside the ledger itself, not by a built-in ledger feature.

## Backup

The platform has no cryptographically-paired backup-drive scheme protecting removed media from being read outside the primary system. Backup and restore, where they exist, don't carry that specific protection today.

## See also

- [[worm-ledger-architecture]] — the full WORM ledger four-layer specification
- [[worm-ledger-design]] — the regulatory compliance mapping and customer key sovereignty rationale
- [[edge-deployment]] — how data is sanitized at the boundary before it reaches storage
