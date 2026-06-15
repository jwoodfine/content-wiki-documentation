---
schema: foundry-doc-v1
title: "How to scale user access tiers"
slug: scale-user-tiers
category: how-to
content_type: how-to
type: how-to
status: active
last_edited: 2026-06-14
editor: pointsav-engineering
paired_with: scale-user-tiers.es.md
---

User access tiers determine what platform operations a session can perform. As a deployment grows, the administrator needs to promote users from read-only access (`READ`) to standard session access (`USER`) or full operator access (`INPUT`). This guide covers identifying current tier assignments, promoting individual users, and bulk-updating a set of users as a team scales.

For the authorization model that defines tiers, see [[machine-based-auth]]. For issuing the tokens that encode tier assignments, see [[issue-capability-token]].

## Prerequisites

- Administrator access to the token issuance service
- A list of users to promote with their current public keys or device identifiers
- A tenant namespace already configured (see [[configure-tenant-namespace]])

## The three access tiers

| Tier | Scope value | Typical use case |
|---|---|---|
| `READ` | read | External partners, audit reviewers, data consumers |
| `USER` | user | Core team members; DataGraph queries, SLM inference, wiki reads |
| `INPUT` | input | Platform operators; WORM ledger writes, F12 Input Machine, full console access |

Promote users to the minimum tier that their role requires. Over-privileged sessions create unnecessary audit surface.

## Step 1: List current tier assignments

Query the tenant's active tokens to see current tier assignments:

```
curl -s "http://<issuance-service-host>:<port>/v1/tenants/<tenant-id>/tokens" \
  -H "Authorization: Bearer <admin-token>"
```

The response lists active tokens with their `scope`, `subject_pubkey`, and `expires_at` fields. Note which users are at `READ` or `USER` scope if they need promotion to `INPUT`.

## Step 2: Promote an individual user

To promote a user, issue a new token at the higher scope. The old token remains valid until it expires or is explicitly revoked — there is no in-place upgrade.

Issue a new token:

```
curl -X POST http://<issuance-service-host>:<port>/v1/tokens \
  -H "Authorization: Bearer <admin-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "subject_pubkey": "<user-pubkey>",
    "scope": "input",
    "tenant_id": "<tenant-id>",
    "expires_in_seconds": 86400
  }'
```

Deliver the new token to the user. Once they load it, their console session gains the new tier.

## Step 3: Revoke the old lower-tier token

After the user confirms the new token is working, revoke the old lower-tier token to close the transition window:

```
curl -X DELETE http://<issuance-service-host>:<port>/v1/tokens/<old-token-id> \
  -H "Authorization: Bearer <admin-token>"
```

Revoking the old token ensures there is no simultaneous READ and INPUT credential for the same device — a single session holds exactly one tier at any time.

## Step 4: Bulk-update a team

For team-scale promotions, prepare a list of public keys and issue tokens in sequence. A simple shell loop over a JSON file of public keys works:

```
while IFS= read -r pubkey; do
  curl -X POST http://<issuance-service-host>:<port>/v1/tokens \
    -H "Authorization: Bearer <admin-token>" \
    -H "Content-Type: application/json" \
    -d "{\"subject_pubkey\": \"$pubkey\", \"scope\": \"user\", \"tenant_id\": \"<tenant-id>\", \"expires_in_seconds\": 86400}"
done < pubkeys.txt
```

Log each issued token ID. After the team confirms their new tokens work, run a corresponding revoke loop over the old token IDs.

## Key takeaways

- Tier promotions require issuing a new token; existing tokens cannot be upgraded in place
- Keep the transition window short — revoke the old token after the user confirms the new one works
- Over-privileged sessions inflate audit surface; issue the minimum tier for each role
- WORM ledger entries are created for every token issuance and revocation — tier changes are permanently auditable

## See also

- [[machine-based-auth]] — the authorization model that defines what each tier permits
- [[issue-capability-token]] — detailed steps for issuing a single capability token
- [[rotate-keys]] — replacing a token at expiry or after a suspected compromise
- [[configure-tenant-namespace]] — setting up the namespace before user tiers are assigned
- [[verify-worm-ledger]] — confirming token issuance events in the audit ledger
