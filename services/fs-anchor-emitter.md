---
schema: foundry-doc-v1
title: "fs-anchor-emitter"
slug: fs-anchor-emitter
category: services
type: topic
quality: complete
short_description: "fs-anchor-emitter generates signed checkpoints of the immutable Write-Once-Read-Many ledger at hourly cadence and prepares them for external anchoring to the Sigstore Rekor transparency log on a monthly schedule — the mechanism that makes the platform's ledger state cryptographically auditable from outside the platform."
status: active
audience: vendor-public
bcsc_class: current-fact
last_edited: 2026-05-08
editor: pointsav-engineering
paired_with: fs-anchor-emitter.es.md
---

`fs-anchor-emitter` is the component that generates signed checkpoints of the immutable Write-Once-Read-Many ledger at hourly cadence and prepares them for external anchoring to the Sigstore Rekor transparency log on a monthly schedule — the mechanism that makes the platform's ledger state cryptographically auditable from outside the platform itself. The emitter operates at Layer 4 of the WORM stack, reads the latest state of the per-tenant tile tree, generates a `signed-note` checkpoint, and stores it at the authoritative path under `$FS_LEDGER_ROOT/<moduleId>/checkpoint`. The monthly workspace anchoring process consumes those checkpoints and posts them to the public transparency log.

## Configuration Requirements

The emitter requires the following environment variables to be defined at runtime:

| Variable | Description | Standard Value |
| :--- | :--- | :--- |
| **FS_LEDGER_ROOT** | Path to the tenant storage root. | `/srv/foundry/ledgers/` |
| **FS_SIGNING_KEY** | Path to the tenant private key (Ed25519). | `/etc/foundry/keys/tenant.key` |
| **FS_ANCHOR_INTERVAL** | Frequency of checkpoint generation. | `3600s` (1 hour) |

## Implementation of the Signed-Note Format

Checkpoints must strictly follow the **C2SP signed-note** format to ensure interoperability with the Sigstore ecosystem. A valid emitter output includes:
1. **Origin:** The service identifier (e.g., `service-fs.foundry.example`).
2. **Tree Size:** The current monotonic entry count.
3. **Root Hash:** The base64-encoded SHA-256 Merkle root.
4. **Signature:** A detached Ed25519 signature from the tenant key.

## Operational Procedures

### Bootstrapping a New Emitter
Upon first initialization, the emitter verifies the presence of the `FS_SIGNING_KEY`. If no prior state exists, it generates a "Tree Size 0" checkpoint to establish the ledger’s origin.

### Verification of Consistency
Before emitting a new checkpoint, the emitter is intended to perform an internal consistency proof against the previously signed state. If the new hash-chain does not append cleanly to the old one, the emitter must abort and trigger an infrastructure alert (SOC 2 CC7 alignment).

## External Anchoring
While the emitter produces checkpoints hourly, external publication to Rekor is currently planned for a monthly cadence. This provides a balance between evidentiary density and network overhead.

## See also

- [[service-fs-architecture]]
- [[service-fs-security-compliance]]
- [[worm-ledger-design]]
