---
schema: foundry-topic-v1
title: "Template Ledger (service-email-template)"
slug: topic-template-ledger
category: services
status: published
last_edited: 2026-04-30
editor: pointsav-engineering
---

The Template Ledger is the distribution mechanism within `service-email-template` that ensures all outbound corporate communications use the current, approved version of each template. It eliminates version drift between template design and operator execution by maintaining a single authoritative copy per template identifier and synchronizing it to the operator's mail environment automatically.

## Design intent

Operators at Woodfine Management Corp. do not draft routine corporate emails from scratch. Each template type — compliance notices, financial disclosures, client correspondence — exists as a versioned record in the Template Ledger. Operators retrieve the current version by key and send it directly. The distinction between drafting and deploying is structural, not procedural.

## Operator workflow

1. The operator opens their `Template Ledger` folder in Microsoft 365.
2. The root folder contains a single email (`[TMPL-000]`) with an attached offline `.html` catalog.
3. The operator opens the catalog, filters by category (for example, *Compliance* or *Finance*), and copies the key for the desired template.
4. The operator pastes the key (for example, `[TMPL-042]`) into the M365 search bar. The current version of that template appears immediately.
5. The operator clicks **Forward**, updates the recipient, removes the routing metadata block at the top of the email body, and sends.

The key is the only input the operator supplies. The template content is sourced from the ledger, not typed or pasted.

## Silent synchronization via Microsoft Graph

When a PointSav engineer updates a template — for example, adding a revised Direct-Hold Solutions rider — the synchronization service uses the Microsoft Graph API to:

1. Remove the previous version of the template from the operator's sub-folder.
2. Insert the updated version in its place.

No push notification is sent to the operator. The current template is always present in the folder; no operator action is required to receive an update. The absence of notifications is deliberate: unnecessary alerts reduce the operator's ability to recognize a genuinely significant event.

## See also

- [[topic-service-email]] — the Ring 1 email ingest service that handles inbound messages
- [[topic-style-guide-guide]] — operational register conventions for deployment runbooks
- [[topic-disclosure-substrate]] — the disclosure architecture that governs outbound communications

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
