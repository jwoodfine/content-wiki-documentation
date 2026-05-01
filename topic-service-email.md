---
schema: foundry-doc-v1
title: "service-email: Email Transport Bridge"
slug: topic-service-email
category: services
type: topic
quality: complete
short_description: "service-email is the Ring 1 boundary-ingest service that polls a Microsoft 365 mailbox via the Microsoft Graph API, extracts raw email payloads, and writes them to a local queue without interpreting their content."
status: pre-build
last_edited: 2026-04-30
editor: pointsav-engineering
cites: []
paired_with: topic-service-email.es.md
---

# service-email: Email Transport Bridge

> service-email is the Ring 1 boundary-ingest service that polls a Microsoft 365 mailbox via the Microsoft Graph API, extracts raw email payloads, and writes them to a local queue without interpreting their content.

**service-email** is a Ring 1 boundary-ingest service in the PointSav three-ring architecture. It functions as a transport interceptor: it authenticates against the Microsoft Graph API, retrieves inbound email messages, and writes the raw payloads to a local temporary queue for downstream processing by Ring 2 services. The service deliberately maintains no knowledge of message content or semantic meaning — its only job is reliable, authenticated extraction across the cloud boundary.

## Overview

The service addresses a structural limitation of IMAP and SMTP: both protocols require maintaining a persistent connection and expose message state management through legacy mechanisms. service-email uses OAuth2 authentication against the Microsoft Graph API instead, making each polling cycle a discrete, authenticated HTTP exchange. This approach confines the cloud-trust boundary to a single well-defined point in the pipeline.

## Ring and Role

service-email occupies **Ring 1 — Boundary Ingest** in the three-ring architecture. Ring 1 services are per-tenant and implement an MCP (Model Context Protocol) server interface. Each Ring 1 service handles one inbound channel; service-email handles the email channel. Other Ring 1 services cover filesystem, people records, and structured input. No Ring 1 service processes content semantically — that is Ring 2's scope.

## Architecture

The extraction loop operates in three steps:

1. **Authenticate.** An OAuth2 handshake against the Microsoft Graph API produces a bearer token scoped to mail read operations for the configured mailbox.
2. **Extract.** The service polls for unread messages (excluding drafts stored only in the local UI). It retrieves the raw OData JSON payload for each message found.
3. **Write and mark.** The payload is written to the local temporary queue at `assets/tmp-maildir/`. The service then issues an authorized `PATCH` request to mark each extracted message as read on the remote server, preventing re-extraction on the next polling cycle.

The service surrenders execution to the downstream parser (`service-extraction`) once the payload lands in the queue. No parsing, classification, or content inspection occurs within service-email.

## Configuration

| Parameter | Purpose |
|---|---|
| OAuth2 credentials | Client ID and secret for the registered Microsoft Graph application |
| Mailbox address | The Microsoft 365 mailbox to monitor |
| Poll interval | How often the extraction loop runs |
| Queue path | Local filesystem path for the temporary maildir queue |

## See Also

- [[topic-service-extraction]]
- [[topic-service-people]]
- [[topic-service-slm]]
- [[topic-trajectory-substrate]]

## References

- DOCTRINE.md §XI — Ring 1 boundary-ingest architecture
- `pointsav-monorepo/service-email/` — implementation crate
- SYS-ADR-07 — structured data never routes through AI (governs downstream handling of service-email output)

---
Copyright © 2026 Woodfine Capital Projects Inc.
Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).
PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.