---
schema: foundry-doc-v1
title: "FS anchor emitter"
slug: fs-anchor-emitter
category: services
type: topic
content_type: topic
quality: complete
index_group: specialist-and-domain-services
short_description: "A one-shot binary that fetches a signed WORM-ledger checkpoint from service-fs, anchors it to the public Sigstore Rekor transparency log, and writes the resulting log entry back — making ledger state auditable from outside the platform."
status: active
audience: vendor-public
bcsc_class: current-fact
last_edited: 2026-08-22
editor: pointsav-engineering
paired_with: fs-anchor-emitter.es.md
---

`fs-anchor-emitter` connects the platform's immutable [[worm-ledger-design|Write-Once-Read-Many ledger]] to a public, third-party transparency log. It doesn't generate the ledger checkpoint itself — [[service-fs-architecture|service-fs]] does that — the emitter's job is to fetch an already-signed checkpoint, submit it to Sigstore Rekor, and record the result. This design keeps checkpoint generation and public anchoring as separate, independently-auditable steps.

## What it does, in order

The emitter is a one-shot binary, invoked on a schedule by an external process rather than running its own timer:

1. **Fetch.** `GET /v1/checkpoint` from `service-fs`, scoped to the running tenant's module ID. The checkpoint carries an origin string, a monotonic tree size, a base64 Merkle root hash, and — already applied by `service-fs` — a signature and public key.
2. **Anchor to Rekor.** The checkpoint is serialised, hashed with SHA-256, and wrapped in a Sigstore `hashedRekordRequestV002` entry (Rekor v0.0.2's request shape). The emitter generates a fresh Ed25519 keypair for this step alone, on every run — that ephemeral key exists only to produce the Rekor timestamp and inclusion proof, not to assert a persistent identity. The request is posted to the configured Rekor endpoint.
3. **Write back.** The resulting transparency-log entry is posted to `service-fs`'s `/v1/append`, so the platform's own record shows exactly what was anchored publicly and when.

## Configuration

Three environment variables, read once at startup:

| Variable | Purpose | Default |
|---|---|---|
| `FS_ENDPOINT` | Base URL of the `service-fs` instance to fetch from and write back to | none — required |
| `FS_MODULE_ID` | Tenant module scoping the checkpoint fetch | none — required |
| `REKOR_URL` | Rekor log-entries endpoint | `log2025-1.rekor.sigstore.dev`'s v2 API |

A distinct exit code identifies where a run failed: configuration error, checkpoint fetch failure, Rekor submission failure, or the final write-back to `service-fs`.

## Cadence and scope

The binary itself has no internal generation or consistency-proof logic — both would require holding ledger state, which this design deliberately keeps out of the anchoring step. Its own source identifies it as "Doctrine Invention #7," documented as monthly Rekor anchoring of `service-fs` checkpoints — a deliberate balance between evidentiary density and network overhead, not a technical ceiling on how often it could run.

## See also

- [[service-fs-architecture]] — generates and signs the checkpoints this emitter fetches
- [[worm-ledger-design]] — the ledger the checkpoint attests to
- [[service-fs-security-compliance]] — the compliance posture this anchoring supports
