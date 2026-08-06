---
schema: foundry-doc-v1
title: "Issue a capability token"
slug: issue-capability-token
short_description: "Issues an Ed25519-signed pairing token from service-content over plain HTTP, registers it with the receiving peer, and covers the separate X-Foundry-Capability request header."
category: machine-authorization
index_group: pairing-and-tokens
content_type: how-to
type: how-to
quality: complete
status: active
audience: "Engineers (hands on keyboard); service operators"
last_edited: 2026-08-06
editor: pointsav-engineering
paired_with: issue-capability-token.es.md
research_trail:
  sources: [pointsav-monorepo service-content pairing module (token issuance, pair registration, capability verification), service-content HTTP route table]
  verification_method: "independently source-verified against pointsav-monorepo on 2026-08-06 by reading the Rust source directly, with file:line citations recorded per claim; query-parameter names, both token payload field sets, the two distinct wire formats, the 24-hour expiry, the absence of any revocation path, and the count of routes actually gated on the capability header were each confirmed at their definition site"
---

## Prerequisites

- A running `service-content` instance you can reach over HTTP, holding its persistent Ed25519 keypair on disk
- `curl` or an equivalent HTTP client — no CLI tool exists for any part of this
- The role string you intend to grant
- Optionally, a node label and a comma-separated archive scope list to narrow the token
- The receiving peer's reachable `POST /v1/pair` endpoint

## Purpose

Mint an Ed25519-signed pairing token from `service-content` and register it with a peer service, so the two can authenticate to each other over HTTP — about five minutes.

## Procedure

> **Warning:** no revocation mechanism exists for either token type described here. An issued token is live for its full 24 hours and nothing invalidates it early. Scope every token as narrowly as the work allows before you issue it.

1. Request a pairing token from the issuing service. `node_label` and `archive_scope` are optional; `role` is not:

   ```bash
   curl -s 'http://<service-content-host>/v1/pair/token?role=<role>&node_label=<label>&archive_scope=<archive-a>,<archive-b>'
   ```

2. Read the response, which is JSON carrying two fields:

   ```json
   {"token": "<signed-token>", "public_key": "<issuer-public-key>"}
   ```

3. Optional: decode the token to confirm what you just issued. The wire format is `<base64url(payload_json)>.<base64url(ed25519_signature)>`, so base64url-decoding the first dot-separated segment yields the payload: `issuer`, `role`, `nonce`, `expiry`, `archive_scope`, and `peer_type`.

4. Record the expiry. It is set 24 hours from issuance, and it is the only thing that ever ends the token's validity.

5. Register the token with the receiving peer. This is the step that creates the pairing — the other party makes this call, not the issuer:

   ```bash
   curl -s -X POST http://<peer-host>/v1/pair \
     -H 'Content-Type: application/json' \
     -d '{"token":"<signed-token>","public_key":"<issuer-public-key>","node_label":"<label>"}'
   ```

   The receiving service verifies the signature against the supplied public key and records the pairing.

6. Send subsequent calls to capability-gated routes with the `X-Foundry-Capability` header:

   ```bash
   curl -s -H 'X-Foundry-Capability: <capability-value>' http://<host>/<capability-gated-path>
   ```

## Expected outcome

The receiving peer holds a recorded pairing whose signature it has verified, and it expires 24 hours after the token was issued. Requests carrying a well-formed, correctly-signed, in-date `X-Foundry-Capability` header reach their handler on the gated routes.

## Verification

Confirm the pairing token first, before registering it: base64url-decode the payload segment and check that `role`, `archive_scope`, and `expiry` match what you asked for. A token whose `archive_scope` is wider than intended cannot be narrowed after issue and cannot be withdrawn.

Confirm the capability header by using it. Exercise a capability-gated route with the header attached and confirm the request reaches the handler; a missing, malformed, badly-signed, or expired header is rejected at the gate before the handler runs. There is no dedicated verification endpoint — the gate itself is the check.

> **Note:** the two credentials are genuinely distinct, not one credential under two names. The pairing token establishes the pairing and carries `issuer`/`role`/`nonce`/`expiry`/`archive_scope`/`peer_type`. The `X-Foundry-Capability` header proves identity on each later call and carries `from_instance`, `user_scope`, `archive_scope`, `nonce`, `expiry`, `peer_type`, and an optional `forwarded_for`. They share the base64url-payload-plus-Ed25519-signature shape and nothing else.

> **Note:** exactly two API routes are gated on the capability header today. The rest of the service's routes do not check it, so the header's presence is not a general-purpose access control across the whole API.

## Rollback

There is nothing to roll back and no way to undo an issue. A token you did not mean to create stays valid for the remainder of its 24 hours; issuing a replacement does not disturb it.

The one action that makes an issued token permanently unusable before its expiry is a change to the signing service's underlying keypair, which happens only if its persisted key file is deleted and the service restarts. That is a manual operator action, it is not a supported feature, and it invalidates every token and pairing that service has ever signed rather than just the one you regret. [[rotate-keys]] covers what replacement actually looks like given these constraints.

## Next steps

- [[rotate-keys]] — replace a credential within the 24-hour expiry model
- [[service-content]] — the service that issues and verifies these tokens
- [[capability-based-security]] — the authorization model behind the header
