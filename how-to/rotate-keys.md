---
schema: foundry-doc-v1
title: "How to rotate keys and capability tokens"
slug: rotate-keys
category: how-to
content_type: how-to
type: how-to
status: active
last_edited: 2026-06-14
editor: pointsav-engineering
paired_with: rotate-keys.es.md
---

Key rotation replaces an Ed25519 keypair and its associated capability token before the old credentials expire or after a suspected compromise. Rotation is a planned operation with a brief transition window during which both the old and new tokens are valid. This guide covers the full rotation sequence: generating a new keypair, issuing a new token, transitioning the recipient, and revoking the old token.

For the authorization model, see [[machine-based-auth]]. For issuing a token from scratch, see [[issue-capability-token]].

## Prerequisites

- Access to the token issuance service at administrator scope
- The identity of the credential holder (the public key of the old keypair, or the device identifier)
- A coordination window: both the holder and the issuance service must be available

## Step 1: Generate a new keypair on the recipient device

The credential holder generates a new Ed25519 keypair on their device. The private key never leaves the device; only the public key is shared with the issuer.

For a console session:

```
os-console --generate-keypair --out new-key
```

For a PPN node:

```
service-vm-host --generate-keypair --out /etc/ppn/new-key
```

Both commands write a `new-key.pub` (public key, base64) and a `new-key` (private key, local only). Record the public key value for step 2.

## Step 2: Issue a new token against the new keypair

Using the new public key, request a new capability token at the same scope as the old one:

```
curl -X POST http://<issuance-service-host>:<port>/v1/tokens \
  -H "Authorization: Bearer <admin-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "subject_pubkey": "<new-base64-pubkey>",
    "scope": "<same-scope-as-old-token>",
    "expires_in_seconds": 86400
  }'
```

The response is a new signed token payload. Do not deliver it yet.

## Step 3: Deliver and load the new token

Deliver the new token to the credential holder through a trusted channel. The holder loads it alongside the old token — during the transition window, both are valid:

```
os-console --load-token <new-token-payload>
```

For a service:

```
export PLATFORM_TOKEN=<new-token-payload>
```

Verify the new token is accepted by the API before proceeding. If the new token is rejected, do not revoke the old token — investigate the rejection reason first.

## Step 4: Revoke the old token

Once the holder confirms the new token is working, revoke the old token:

```
curl -X DELETE http://<issuance-service-host>:<port>/v1/tokens/<old-token-id> \
  -H "Authorization: Bearer <admin-token>"
```

The old token ID is the `jti` (JWT ID) field from the original token payload, or the subject public key if the issuance service uses public key as the lookup key. After revocation, the old token returns 401 on any API call.

## Step 5: Remove the old keypair from the device

After confirming the old token is revoked and the new token is working, remove the old keypair:

```
rm -f /etc/ppn/old-key /etc/ppn/old-key.pub
```

For a console session, the old keypair is removed via:

```
os-console --remove-keypair <old-key-fingerprint>
```

Do not remove the old keypair before revoking the old token — if the new token fails and you need to fall back, the old keypair must still be present.

## Key takeaways

- Rotation is a three-phase process: new token issued → new token verified → old token revoked
- Never remove the old keypair before the old token is revoked and the new token is confirmed working
- Both tokens are valid during the transition window — keep the window short (minutes, not days)
- A rotation caused by suspected compromise should skip the transition window: revoke the old token immediately before the new one is loaded

## See also

- [[machine-based-auth]] — the authorization model that governs token validity and revocation
- [[issue-capability-token]] — how to issue a token from scratch when no previous token exists
- [[pair-a-new-device]] — the initial pairing sequence that precedes the first token issuance
- [[verify-worm-ledger]] — confirming that rotation events are recorded in the audit ledger
- [[service-vm-tenant]] — the tenant proxy that enforces token validation on API calls
