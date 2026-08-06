---
schema: foundry-doc-v1
title: "Rotate keys and capability tokens"
slug: rotate-keys
short_description: "Replaces a service-content credential within the real system's limits: tokens expire on a fixed 24-hour clock, overlap is unavoidable, and no mechanism cuts a live token short."
category: machine-authorization
index_group: pairing-and-tokens
content_type: how-to
type: how-to
quality: complete
status: active
audience: "Engineers (hands on keyboard); service operators"
last_edited: 2026-08-06
editor: pointsav-engineering
paired_with: rotate-keys.es.md
research_trail:
  sources: [pointsav-monorepo service-content pairing module (token issuance, pair registration, capability verification), service-content HTTP route table]
  verification_method: "independently source-verified against pointsav-monorepo on 2026-08-06 by reading the Rust source directly, with file:line citations recorded per claim; the absence of any revoke, delete, or invalidate function across the pairing and capability code was confirmed by reading the module's full public surface rather than by searching for an expected route name"
---

## Prerequisites

- Familiarity with [[issue-capability-token]], which covers the wire format, both payload shapes, and the issuance call — this guide does not repeat them
- HTTP access to the issuing `service-content` instance
- The issuance time of the credential you are replacing, or its decoded `expiry` field

## Purpose

Replace a live capability credential with a fresh one — about five minutes of work, after which the credential you replaced stays valid for the remainder of its own 24 hours.

## Procedure

> **Warning:** there is no revoke, delete, or invalidate operation anywhere in this system. Issue-new-then-retire-old is not available. Plan the cutover on the assumption that the old credential keeps working until its clock runs out.

1. Decode the payload of the credential you are replacing and read its `expiry`. That timestamp is 24 hours after issuance and is the moment the old credential stops working.

2. Request a replacement token with the same role and scope you intend to keep:

   ```bash
   curl -s 'http://<service-content-host>/v1/pair/token?role=<role>&node_label=<label>&archive_scope=<archive-a>,<archive-b>'
   ```

3. Register the replacement with the receiving peer:

   ```bash
   curl -s -X POST http://<peer-host>/v1/pair \
     -H 'Content-Type: application/json' \
     -d '{"token":"<new-token>","public_key":"<issuer-public-key>","node_label":"<label>"}'
   ```

4. Point the calling service at the new credential and confirm its next request succeeds before you stop using the old one.

5. Let the old credential expire on its own clock. No further action shortens it.

## Expected outcome

Two credentials are valid at once: the new one for the next 24 hours, and the old one until the `expiry` you read in step 1. The overlap is a property of the system, not a transition window you configure, and it cannot be shortened.

## Verification

Confirm the new credential works by exercising a capability-gated route with it and checking the request reaches its handler.

Confirm the old credential's retirement by reading its `expiry` field, not by testing for rejection. Testing the old credential before that timestamp will show it still passing the gate — that is the expected result, not a failed rotation.

## Rollback

Rotation is safe to re-run and safe to abandon. Requesting another token does not disturb any token already issued, and the credential you were replacing is still valid until its expiry, so pointing the caller back at it restores the prior state exactly.

## Next steps

- [[issue-capability-token]] — the issuance call, both payload shapes, and the scoping decision
- [[service-content]] — the service that signs and verifies these credentials
- [[capability-based-security]] — the authorization model these tokens operate within

## Known limitations, as built (2026-08-06)

- **No per-token invalidation.** If a credential is suspected compromised, nothing in this system stops that specific token before its 24-hour expiry.
- **The one immediate recourse is service-wide.** Regenerating the issuing service's own signing keypair — deleting its persisted key file and restarting the service — does invalidate the compromised credential, along with every other token and pairing that service has signed. There is no command for this, it is not a documented supported operation, and it is not a rotation procedure.
- **Scope narrowly at issue time.** Because the 24-hour clock is the only control available, the `archive_scope` and `role` chosen at issuance are the practical limit on a compromised credential's reach.
