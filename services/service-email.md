---
schema: foundry-doc-v1
title: "Email ingest"
slug: service-email
category: services
type: concept
content_type: topic
quality: complete
index_group: ring-1-boundary-ingest
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-08-22
editor: pointsav-engineering
paired_with: service-email.es.md
short_description: "service-email pulls mail out of a Microsoft Exchange mailbox over EWS, writes the raw message to local storage, and deletes it from the source mailbox immediately after extraction — the cloud mailbox is a transit point, not a copy of record."
cites: []
references:
  - id: 1
    text: "Hardt, D. (Ed.). 'The OAuth 2.0 Authorization Framework.' IETF RFC 6749, 2012."
    url: "https://www.rfc-editor.org/rfc/rfc6749"
---

`service-email` pulls mail out of a Microsoft Exchange mailbox and onto local storage. It authenticates with OAuth2 client-credentials, connects to Exchange Web Services (EWS) — the SOAP-based Exchange API, not the newer Microsoft Graph API — and, for each message it finds, extracts the raw MIME content, writes it as a local file, and issues a hard delete against the source mailbox. It does not interpret, classify, or route content; that happens downstream in `service-content` and `service-extraction`.

## The extraction cycle

For each folder it polls, the service:

1. Authenticates against Exchange using a client-credentials OAuth2 token, scoped to Exchange's own default scope rather than any Graph-specific permission.
2. Lists message IDs in the folder over EWS SOAP calls.
3. Fetches each message's raw MIME content, base64-decoded from the SOAP response, and writes it to a local file.
4. Issues an EWS hard-delete request for that message against the source mailbox.

This is an extract-then-delete flow, not a soft retention policy — a message is removed from the source mailbox as soon as its content has been written locally, not after some elapsed time.

## Why the cloud mailbox isn't the copy of record

Because extraction and deletion happen together, the Exchange mailbox never accumulates a durable archive of its own — the local file written at extraction time is the one copy that persists. This confines what the cloud provider ever holds to messages awaiting extraction, not a full historical record.

## What service-email is not

`service-email` is the ingest boundary, not the email client. It does not render HTML for an operator to read, does not synthesise content, and does not classify or route messages — it hands the raw local file to downstream services and stops. The [[three-ring-architecture|three-ring architecture]] positions `service-email` at Ring 1, the trust perimeter where payloads first enter the platform.

## See also

- [[service-egress]] — takes the locally-written mail forward for outbound transfer, using its own separate release mechanism
- [[service-content]] — consumes the raw local files this service produces
- [[app-console-input]] — the F12 Input Machine; companion ingest surface for non-email payloads
