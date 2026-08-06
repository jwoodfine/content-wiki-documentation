---
schema: foundry-doc-v1
title: "Scale user access"
slug: scale-user-tiers
short_description: "Grants role-scoped capability tokens to new users as a team scales, using service-content's real pairing API — there is no promote/demote or bulk-revoke operation, since no revocation mechanism exists at all."
category: how-to
content_type: how-to
type: how-to
quality: complete
status: active
audience: "Engineers (hands on keyboard); customer operators"
last_edited: 2026-08-06
editor: pointsav-engineering
paired_with: scale-user-tiers.es.md
research_trail:
  sources: [pointsav-monorepo service-content/src/pairing.rs and http.rs, already fully source-verified while rewriting issue-capability-token.md and rotate-keys.md earlier this session]
  verification_method: "reused the already-confirmed real service-content capability-token mechanism from this session's Machine authorization batch rather than re-deriving it; this guide's own prior Correction note had already flagged the same READ/USER/INPUT tier fiction and fictional /v1/tokens REST surface found across that whole batch"
---

## Prerequisites

- Access to the `service-content` instance issuing tokens for your team
- A list of users to add, with their public keys or device identifiers
- Familiarity with [[issue-capability-token]], which this guide builds directly on

## Purpose

Grant new team members a role-scoped token as your deployment grows — a few minutes per person, or a short scripted loop for a whole team at once. This is not a tier-promotion system: there's no in-place upgrade and no revocation, so read this before treating it as an access-management console.

## Procedure

> **Note:** the real role set is `User`, `Admin`, and `Interface` — not a `READ`/`USER`/`INPUT` scale. Choose the role that matches what the person actually needs; there's no numeric tier to "promote" someone up later, only a fresh token with a different role.

1. For each new user, issue a token scoped to the role and archives they need:

   ```bash
   curl -s "http://<service-content-host>/v1/pair/token?role=<role>&node_label=<user-label>&archive_scope=<archive-a>,<archive-b>"
   ```

   See [[issue-capability-token]] for the full response shape and the registration step that follows.

2. For a whole team at once, loop over a list of labels and scopes rather than issuing one at a time by hand:

   ```bash
   while IFS= read -r label; do
     curl -s "http://<service-content-host>/v1/pair/token?role=<role>&node_label=$label&archive_scope=<archive-a>"
   done < team-labels.txt
   ```

3. Deliver each token to its user. Record what you issued — since there's no listing endpoint for already-issued tokens, your own record is the only inventory that exists.

## Expected outcome

Each new user holds a token scoped to exactly the role and archives they need, valid for 24 hours from issuance.

## Verification

Confirm a new user's access by having them make a request using their token against a capability-gated route, per [[issue-capability-token]]'s verification steps.

## Rollback

> **Warning:** there is no way to promote a user's existing token in place, and no way to revoke a token you issued in error. If you granted the wrong role or scope, the fix is to issue a corrected token and have the user switch to it — the original keeps working until its own 24-hour expiry regardless. Plan team onboarding around this: get the role and scope right at issuance, since correcting it later doesn't remove the original grant.

## Next steps

- [[issue-capability-token]] — the full single-token issuance and registration procedure
- [[rotate-keys]] — what "rotation" really means in this system, and its honest limits

## See also

- [[machine-based-auth]] — the authorization model tokens operate within
- [[configure-tenant-namespace]] — a separate, unrelated system for tenant-level VM quotas, not user roles
