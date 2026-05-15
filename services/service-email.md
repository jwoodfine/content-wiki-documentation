---
schema: foundry-doc-v1
title: "service-email — The WORM Ingest"
slug: service-email
category: services
type: concept
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-15
editor: pointsav-engineering
paired_with: service-email.es.md
short_description: "service-email is the Totebox's email server — it ingests SMTP and IMAP traffic, sanitises every payload, and writes raw text to an append-only Maildir on local block storage. Content interpretation is handled upstream by service-content."
cites: []
---

`service-email` is the Totebox's email server. It listens for SMTP and IMAP traffic, sanitises every payload — stripping HTML rendering logic and tracking pixels — and writes the raw text into an append-only Maildir on local block storage. The service does not interpret content; that work happens upstream in `service-content`. This article covers the ingest pipeline, the Sovereign properties that distinguish it from a conventional email client, and its relationship with the Microsoft 365 integration path.

## The ingest pipeline

The service operates in six stages, each carrying a specific Sovereign property:

| Stage | Action | Sovereign property |
|---|---|---|
| Boot | The Rust binary scans the local audit store and recovers pending jobs | Self-healing — no work is lost across restarts |
| Auth | OAuth2 token refresh via Microsoft Entra (client-credentials flow) | Immunity — no legacy username/password authentication |
| Sync | IMAP mirror loop writes verified mail into Maildir using atomic filesystem operations | Resilience — atomic writes prevent partial records |
| Clean | Hygiene agent enforces TTL rules on the cloud source while the Maildir copy remains permanent | Sovereignty — the vendor cloud cannot retroactively erase the operator's record |
| Render | When the operator drafts a templated email, the engine renders the HTML payload and stages it for manual forwarding | Human-in-the-loop discipline |
| Audit | The audit logger writes non-blocking JSONL entries that downstream services consume | Independent ingest by `service-people` and the Gravity Engine |

## Microsoft 365 integration

The OAuth2 setup uses a Confidential Client registration in Microsoft Entra. Three Graph permissions are required: `Mail.ReadWrite` (to sync into Maildir), `Mail.Send` (to stage templates), and `User.Read.All` (to verify sender identities). Admin consent is granted once so the service runs as a daemon without per-message human interaction.

This approach confines the cloud-trust boundary to a single, well-defined point in the pipeline. Each polling cycle is a discrete, authenticated HTTP exchange — rather than a persistent IMAP connection — making the ingest boundary auditable and stateless.

## The WORM discipline

`service-email` writes payloads to the WORM Maildir — an append-only structure on the Totebox's local block storage. There is no delete operation. A payload written to the Maildir cannot be erased, even if the cloud source (the Microsoft 365 mailbox) is later modified, deleted, or the subscription lapses. The operator's email record is sovereign: it belongs to the archive, not the cloud provider.

## What service-email is not

`service-email` is the ingest boundary, not the email client. It does not render HTML emails for the operator to read. It does not synthesise content. It does not classify or route messages. It hands the sanitised raw payload to `service-content` and `service-extraction` and surrenders execution. Downstream services handle everything from entity extraction to the F3 EMAIL surface the operator sees in `os-console`.

## See also

- [[service-people]] — the identity ledger that receives sender records from service-email via service-extraction
- [[service-content]] — the Gravity Engine that synthesises content from the WORM Maildir
- [[app-console-input]] — the F12 Input Machine; companion ingest surface for non-email payloads
- [[sys-adr-07]] — structured data never routes through AI (governs downstream handling of service-email output)
- [[totebox-os]] — the Totebox that hosts service-email and its WORM storage
