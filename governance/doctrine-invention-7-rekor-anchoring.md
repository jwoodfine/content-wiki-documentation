---
schema: foundry-doc-v1
type: topic
content_type: topic
slug: doctrine-invention-7-rekor-anchoring
title: "Doctrine Invention #7 — The Integrity Anchor"
short_description: "How Foundry's anchor-emitter binary posts a signed ledger checkpoint to Sigstore Rekor each month, providing independently verifiable, third-party evidence of workspace state."
audience: vendor-public
bcsc_class: current-fact
language: en
paired_with: doctrine-invention-7-rekor-anchoring.es.md
category: governance
status: active
quality: complete
last_edited: 2026-06-23
---

# Doctrine Invention #7 — The Integrity Anchor

Doctrine §III.7 defines the Integrity Anchor pattern: a monthly operation that bundles the workspace state hash, manifest hashes, and ledger hash, then posts the result to Sigstore Rekor — a public, append-only transparency log. The result is independently verifiable: anyone can confirm that this state existed at this time, under this identity, without trusting Foundry's own infrastructure.

The pattern is modelled on notarization combined with public timestamping. Notarization proves that a document existed; public timestamping proves it existed at or before a specific moment. The Rekor transparency log provides both: the inclusion proof in the log constitutes independent, third-party evidence.

---

## 1. Why a Transparency Log

A signed checkpoint stored inside the same ledger it describes has a circularity problem: if the ledger is compromised, the signature is also under the attacker's control. A second copy in the operator's own backup store shifts custody but not trust — the same entity controls both.

A public transparency log breaks this. The Sigstore Rekor log is operated by the Sigstore project (a collaboration of Google, Red Hat, and Purdue University, launched 2021) and is append-only by construction. Once an entry is published, no party — including Sigstore — can remove it without breaking the log's cryptographic consistency proofs. An auditor with access to the Rekor log and the original checkpoint can verify the anchor independently of Foundry.

This is the same structural property that Certificate Transparency (RFC 9162) provides for TLS certificates: the CA cannot selectively show or hide certificates to different verifiers, because the log's inclusion proofs would not match. Sigstore Rekor extends this model to arbitrary artifacts.

---

## 2. What Is Published

Each anchor operation publishes a `hashedRekordRequestV002` entry to Rekor. The artifact being anchored is the JSON-serialised checkpoint from `service-fs/v1/checkpoint`:

```json
{
  "origin": "<module_id>",
  "tree_size": <entry count at time of anchoring>,
  "root_hash": "<hex SHA-256 of the chain tip>",
  "algorithm": "sha256",
  "timestamp": <unix epoch seconds>,
  "signature": "<base64 Ed25519 signed-note signature>",
  "public_key": "<base64 Ed25519 verifying key>"
}
```

The `root_hash` field is the SHA-256 chain tip of the `service-fs` hash chain at the time of anchoring. The `signature` field is the Ed25519 signed-note signature produced by the operator's signing key (`FS_SIGNING_KEY`). Together, these fields constitute a signed declaration of the ledger's state at a specific `tree_size`.

The Rekor entry wraps this artifact:

- **digest** — SHA-256 of the checkpoint JSON (raw bytes, base64-encoded)
- **signature.content** — Ed25519 signature of the checkpoint bytes, produced by an ephemeral keypair generated per run
- **signature.verifier.publicKey.rawBytes** — 44-byte SPKI DER of the ephemeral verifying key (base64-encoded)
- **signature.verifier.keyDetails** — `PKIX_ED25519` (signs arbitrary bytes, not a pre-hashed message)

The ephemeral keypair is discarded after each run. Its purpose is to satisfy the Rekor v0.0.2 wire format, which requires a signed artifact. The durable identity is the Rekor-assigned timestamp and inclusion proof — not the ephemeral key.

---

## 3. The Tlog Writeback Loop

After Rekor accepts the entry, the anchor-emitter posts the full Rekor response back to `service-fs/v1/append` with a payload ID of `anchor-rekor-<unix-timestamp>`.

This means the ledger contains a record of its own external anchoring. An auditor reading the ledger can find the Rekor tlog entry directly in the ledger's own history — they do not need to query Rekor separately to confirm that anchoring occurred. The `tree_size` in the anchored checkpoint provides the cursor at which to look for the anchor record (the anchor record appears at a cursor greater than `tree_size`, because the anchoring happens after the checkpoint is computed).

The closed loop means that the anchoring evidence is as durable as the ledger itself, while remaining independently verifiable via Rekor.

---

## 4. The Shard Rotation Protocol

Sigstore deploys Rekor on yearly log shards. Each shard has its own signing key and log identity. The 2025 shard is:

```
https://log2025-1.rekor.sigstore.dev/api/v2/log/entries
```

When the 2026 shard becomes active, the 2025 shard will be turned down. The Rekor v2 API (`/api/v2/`) is not available on the legacy hostname (`rekor.sigstore.dev`) — only on the explicit shard hostnames.

The anchor-emitter defaults to the 2025 shard. The `REKOR_URL` environment variable lets the operator pin a different shard without rebuilding the binary. The annual shard rotation requires updating this variable and restarting the systemd timer — the operator runbook documents this procedure.

Old shard entries remain readable for an extended period after rotation. Historical anchors from the 2025 shard remain verifiable against the 2025 shard log for as long as Sigstore operates that shard in read-only mode. The anchor record in the ledger (the tlog writeback) preserves the full Rekor response, so the anchoring evidence is retained in the ledger even if the shard is later decommissioned.

---

## 5. The Four-Step Operational Flow

The anchor-emitter binary (`fs-anchor-emitter`) executes four steps in sequence:

1. **Checkpoint fetch** — `GET /v1/checkpoint` from service-fs, with `X-Foundry-Module-ID` header set to `FS_MODULE_ID`. Returns the signed checkpoint JSON. Exit 2 on failure.

2. **Hashedrekord construction** — SHA-256 digest of the checkpoint JSON computed in-process; ephemeral Ed25519 keypair generated via OS RNG; checkpoint bytes signed; SPKI DER of the verifying key encoded. The `hashedRekordRequestV002` JSON body is assembled.

3. **Rekor POST** — `POST` to `REKOR_URL` (default: 2025 shard). On success, Rekor returns a JSON response containing the tlog entry (including the Rekor-assigned timestamp and inclusion proof). Exit 3 on failure.

4. **Tlog writeback** — `POST /v1/append` to service-fs with the full Rekor JSON response as the payload and `payload_id: anchor-rekor-<ts>`. Exit 4 on failure.

Exit 0 on complete success. The binary exits with a non-zero code at the first failed step; a systemd `OnFailure=` unit can alert the operator.

---

## 6. Independent Verification

A third party verifying an anchor needs:

1. The ledger's anchor record (the tlog writeback — readable from `service-fs/v1/entries` with the appropriate cursor range)
2. Access to the Sigstore Rekor log for the active shard

From the anchor record, the verifier extracts the Rekor tlog entry (which contains the Rekor-assigned log index and inclusion proof). From the Rekor log, the verifier retrieves the same entry by log index and confirms:

- The artifact digest in the Rekor entry matches `SHA-256(checkpoint JSON)`
- The Rekor timestamp is consistent with the claimed anchoring date
- The inclusion proof is valid against the Rekor log's root hash at that tree size

From the checkpoint JSON itself, the verifier confirms:

- The `root_hash` in the checkpoint matches the expected SHA-256 chain tip by recomputing the chain from the ledger's entries
- The `signature` in the checkpoint is a valid Ed25519 signed-note signature under the operator's published verifying key

This verification is end-to-end operator-independent: it uses the Rekor log (not Foundry's infrastructure) and the ledger's own hash chain (not Foundry's attestation of the chain).

---

## 7. TUF Key Discovery

The current implementation pins the Rekor shard URL via environment variable. The long-term path for key discovery is TUF (The Update Framework) — Sigstore publishes a TUF root that allows clients to discover the active shard's keys and endpoint without hardcoding a URL. This approach is intended to survive shard rotation without any operator configuration change.

TUF-based SigningConfig discovery is intended for a future version of `fs-anchor-emitter`. Until then, the `REKOR_URL` environment variable provides a functionally equivalent mechanism for shard transitions, at the cost of requiring an annual operator configuration update.
