---
schema: foundry-doc-v1
title: "Style guide — email"
slug: style-guide-email
category: reference
type: topic
content_type: topic
quality: complete
short_description: "Editorial standards for external and formal email in the platform (COMMS-EMAIL genre): lead-with-ask discipline, header requirements, body structure, and the professional register."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-25
editor: pointsav-engineering
cites: []
paired_with: style-guide-email.es.md
---

> Every external email has one point. The reader knows what is wanted by the end of the first paragraph.

A **formal email** (COMMS-EMAIL genre) is any external or semi-formal communication sent to a recipient outside the Foundry workspace — a vendor, a regulator, a counterparty, or a collaborator. It differs from an inbox message in that it is addressed to a named recipient, carries a subject, and may be archived. This article is the human-facing standard; the machine-readable counterpart lives in `service-disclosure/templates/email.toml`.

## When to use this template

Use the email template for any communication that:

- Leaves the Foundry workspace (external recipient, external platform).
- Requires a written record (formal ask, vendor confirmation, regulatory contact).
- Is addressed to a specific person or role, not to a group channel.

Internal messages to the inbox or outbox use the inbox-message format from workspace §12. Slack or chat messages use the [[style-guide-chat|chat template]].

## Structure

The template requires a header and three body sections:

**Header** (before any body text):

```
To:      <recipient name and email, or role>
Subject: <specific subject — what this email is about, not "Update" or "Follow-up">
```

| Section | Purpose |
|---|---|
| **Opening** | One sentence: context and the ask, together. The recipient understands what is wanted without reading further. |
| **Body** | The detail the recipient needs to respond or act. One point per paragraph. No more than three paragraphs. |
| **Close** | The specific next step and who owns it. A concrete date where possible. Followed immediately by the signoff. |

## Register and tone

Professional, plain. Address the recipient by name or role in the opening where the relationship warrants it. Do not bury the ask in paragraph three.

Subject lines must be specific: "Request for NDA — Woodfine Management Corp. / [Counterparty]" rather than "Partnership discussion." Ambiguous subjects delay responses and reduce traceability in archives.

Sentence-length budget: mean around twenty words, maximum thirty-five. Active voice. The [[editorial-language-registers|banned-vocabulary list]] applies: state the action directly rather than using marketing-register phrases.

When the recipient may be a current or prospective investor, forward-looking claims about the platform, products, or roadmap carry "planned / intended / may / target" language. This applies to all statements about future capability, timeline, or commercial outcome.

## See also

- [[style-guide-chat|Style Guide — Chat]]
- [[style-guide-memo|Style Guide — Memo]]
- [[language-protocol-substrate|Language Protocol Substrate]]
