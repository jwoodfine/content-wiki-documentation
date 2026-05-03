---
schema: foundry-doc-v1
type: guide
slug: fs-anchor-emitter
title: FS Anchor Emitter Configuration Guide
audience: vendor-public
bcsc_class: current-fact
language: en
paired_with: fs-anchor-emitter.es.md
---

# FS Anchor Emitter Configuration Guide

The `fs-anchor-emitter` is the component responsible for generating signed checkpoints of the {{gli|WORM}} ledger and preparing them for external anchoring. This guide details the setup and operational requirements for ensuring ledger integrity across both Vendor (Foundry) and Customer (Totebox) environments.

## Overview of Operation

The emitter operates at Layer 4 of the {{gli|WORM}} stack. It periodically reads the latest state of the per-tenant tile tree, generates a `signed-note` checkpoint, and stores it in the authoritative `$FS_LEDGER_ROOT/<moduleId>/checkpoint` file. These checkpoints are then consumed by the monthly workspace anchoring process to be posted to the Sigstore Rekor transparency log.

## Configuration Requirements

The emitter requires the following environment variables to be defined at runtime:

| Variable | Description | Standard Value |
| :--- | :--- | :--- |
| **FS_LEDGER_ROOT** | Path to the tenant storage root. | `/srv/foundry/ledgers/` |
| **FS_SIGNING_KEY** | Path to the tenant private key (Ed25519). | `/etc/foundry/keys/tenant.key` |
| **FS_ANCHOR_INTERVAL** | Frequency of checkpoint generation. | `3600s` (1 hour) |

## Implementation of the Signed-Note Format

Checkpoints must strictly follow the **C2SP signed-note** format to ensure interoperability with the Sigstore ecosystem. A valid emitter output includes:
1.  **Origin:** The service identifier (e.g., `service-fs.foundry.example`).
2.  **Tree Size:** The current monotonic entry count.
3.  **Root Hash:** The base64-encoded SHA-256 Merkle root.
4.  **Signature:** A detached Ed25519 signature from the tenant key.

## Operational Procedures

### Bootstrapping a New Emitter
Upon first initialization, the emitter verifies the presence of the `FS_SIGNING_KEY`. If no prior state exists, it generates a "Tree Size 0" checkpoint to establish the ledger’s origin.

### Verification of Consistency
Before emitting a new checkpoint, the emitter is intended to perform an internal consistency proof against the previously signed state. If the new hash-chain does not append cleanly to the old one, the emitter must abort and trigger an infrastructure alert (SOC 2 CC7 alignment).

## External Anchoring
While the emitter produces checkpoints hourly, external publication to Rekor is currently planned for a monthly cadence. This provides a balance between evidentiary density and network overhead.
