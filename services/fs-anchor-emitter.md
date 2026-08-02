---
schema: foundry-doc-v1
title: "FS anchor emitter"
slug: fs-anchor-emitter
category: services
type: topic
content_type: topic
quality: complete
short_description: "Signed hourly checkpoints of the Write-Once-Read-Many ledger prepared for monthly anchoring to Sigstore Rekor, making ledger state auditable from outside the platform."
status: active
audience: vendor-public
bcsc_class: current-fact
last_edited: 2026-05-25
editor: pointsav-engineering
paired_with: fs-anchor-emitter.es.md
---

**Correction (2026-08-02, verified against canonical `origin/main`):** the architecture below is reversed and the env vars are wrong. The real `service-fs/anchor-emitter/src/main.rs` reads `FS_ENDPOINT`, `FS_MODULE_ID`, and `REKOR_URL` — not `FS_LEDGER_ROOT`/`FS_SIGNING_KEY`/`FS_ANCHOR_INTERVAL` (those are `service-fs`'s own variables, not the emitter's). The real flow is: (1) `GET /v1/checkpoint` from `service-fs` — the emitter *fetches* an already-generated checkpoint, it does not itself read the tile tree or generate the checkpoint; (2) build a Sigstore hashedrekord entry; (3) `POST` to the Rekor v2 log; (4) `POST` the tlog entry back to `service-fs /v1/append`. The general subject (monthly Rekor anchoring of WORM checkpoints) is real and accurate — see the separately-verified `governance/doctrine-invention-7-rekor-anchoring.md`, which describes this correctly. **Flagged, not resolved** — this article's specific config/architecture section needs rewriting to match the real fetch-not-generate flow.

`fs-anchor-emitter` is the component that generates signed checkpoints of the immutable [[worm-ledger-design|Write-Once-Read-Many ledger]] at hourly cadence and prepares them for external anchoring to the Sigstore Rekor transparency log on a monthly schedule — the mechanism that makes the platform's ledger state cryptographically auditable from outside the platform itself. The emitter operates at Layer 4 of the WORM stack as described in [[service-fs-architecture]], reads the latest state of the per-tenant tile tree, generates a `signed-note` checkpoint, and stores it at the authoritative path under `$FS_LEDGER_ROOT/<moduleId>/checkpoint`. The monthly workspace anchoring process consumes those checkpoints and posts them to the public transparency log.

## Configuration Requirements

The emitter requires the following environment variables to be defined at runtime:

| Variable | Description | Standard Value |
| :--- | :--- | :--- |
| **FS_LEDGER_ROOT** | Path to the tenant storage root. | `/srv/platform/ledgers/` |
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
Upon first initialization, the emitter verifies the presence of the `FS_SIGNING_KEY`. If no prior state exists, it generates a "Tree Size 0" checkpoint to establish the ledger’s origin. The [[machine-based-auth|machine-based authentication]] layer controls which identities may hold signing keys.

### Verification of Consistency
Before emitting a new checkpoint, the emitter is intended to perform an internal consistency proof against the previously signed state. If the new hash-chain does not append cleanly to the old one, the emitter must abort and trigger an infrastructure alert (SOC 2 CC7 alignment). The [[merkle-proofs-as-substrate-primitive|Merkle proof substrate]] underpins this consistency verification.

## External Anchoring
While the emitter produces checkpoints hourly, external publication to Rekor is currently planned for a monthly cadence. This provides a balance between evidentiary density and network overhead. The [[service-fs-security-compliance|security and compliance posture]] document describes how this anchoring satisfies SEC Rule 17a-4(f) and eIDAS requirements.

## See also

- [[service-fs-architecture]]
- [[service-fs-security-compliance]]
- [[worm-ledger-design]]
