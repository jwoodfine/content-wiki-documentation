---
schema: foundry-doc-v1
title: "Template ledger"
slug: template-ledger
category: services
type: topic
content_type: topic
quality: complete
index_group: specialist-and-domain-services
short_description: "Distribution mechanism in service-email-template that syncs one authoritative copy of every approved template to the operator's mail environment, eliminating version drift."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-08-24
editor: pointsav-engineering
paired_with: template-ledger.es.md
cites: []
---

The Template Ledger is the distribution mechanism within [[service-email|`service-email-template`]] that synchronises a single authoritative copy of every approved template to the operator's mail environment automatically. It eliminates version drift between template design and operator execution by maintaining one canonical copy per template identifier; the operator retrieves the current version by key and sends it directly. The distinction between drafting and deploying becomes structural rather than procedural — the operator is not authoring routine corporate correspondence, only selecting which approved [[disclosure-substrate|template]] to dispatch.

## Design intent

Operators at MCorp do not draft routine corporate emails from scratch. Each template type — compliance notices, financial disclosures, client correspondence — exists as a versioned record in the Template Ledger. Operators retrieve the current version by key and send it directly. The distinction between drafting and deploying is structural, not procedural.

## Operator workflow

Retrieval is key-based, not folder-browsing: a `Template Ledger` folder in Microsoft 365 holds an offline `.html` catalog the operator filters by category (*Compliance*, *Finance*) to find a template's key, then pastes that key into the M365 search bar to surface the current version instantly. Forwarding it — after removing the routing metadata block at the top of the email body and updating the recipient — is the only manual step; the key is the only input the operator supplies, and the template content itself is always sourced from the ledger, never typed or pasted from memory.

The exact click-by-click retrieval procedure is operator runbook material, not covered step by step here — this article describes why the mechanism is structured this way, not how to execute it.

## Silent synchronization via Microsoft Graph

When a PointSav engineer updates a template — for example, adding a revised Direct-Hold Solutions rider — the synchronization service uses the Microsoft Graph API to:

1. Remove the previous version of the template from the operator's sub-folder.
2. Insert the updated version in its place.

No push notification is sent to the operator. The current template is always present in the folder; no operator action is required to receive an update. The absence of notifications is deliberate: unnecessary alerts reduce the operator's ability to recognize a genuinely significant event.

## See also

- [[service-email]] — the Ring 1 email ingest service that handles inbound messages
- [[disclosure-substrate]] — the disclosure architecture that governs outbound communications
