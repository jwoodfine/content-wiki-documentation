---
schema: foundry-doc-v1
title: "Style guide — chat"
slug: style-guide-chat
category: reference
type: topic
quality: complete
short_description: "Editorial standards for chat messages in the platform (COMMS genre): one-point discipline, channel header, maximum three sentences, and the distinction between chat and email."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-24
editor: pointsav-engineering
cites: []
paired_with: style-guide-chat.es.md
---

> A chat message carries one point. If a second point is needed, send a second message.

A **chat message** (COMMS genre) is a short synchronous or near-synchronous communication sent to a team channel or direct recipient. It is addressed to people who are present or will be present soon. Chat is not a substitute for a memo, an email, or a ticket comment — each serves a different archival purpose. This article is the human-facing standard; the machine-readable counterpart lives in `service-disclosure/templates/chat.toml`.

## When to use this template

Use a chat message when:

- The communication is short, time-sensitive, and low-stakes.
- The recipient is on the same platform and likely to respond within the same working session.
- The message does not need to be formally archived or retrieved later.

If the content needs to be traceable, retrievable, or acted on by someone not currently present, use a ticket comment, email, or inbox message instead.

## Structure

**Header** (optional, for channel messages):

```
Channel: #<channel-name>   [or]   To: <@recipient>
```

Body: one point, three sentences maximum. If an ask is included, it is the last sentence and is phrased as a direct question.

```
<Context sentence — what is happening or what changed.>
<Detail sentence — the one thing the recipient needs to know.>
<Ask — optional: a direct question or request in one sentence.>
```

Do not include a signoff. Do not write a paragraph. Do not combine multiple topics in one message — send one message per point.

## Register and tone

Conversational but professional. Contractions are acceptable. Emoji are acceptable where they replace a word or carry genuine tonal meaning, not as decoration.

Abbreviations and internal terminology are fine for established team channels. For external-facing channels or recipients unfamiliar with platform vocabulary, spell out the first use.

One-line replies are preferred. If a paragraph is needed, the reply belongs in a ticket comment or email, not in chat.

## See also

- [[style-guide-email|Style Guide — Email]]
- [[style-guide-ticket-comment|Style Guide — Ticket Comment]]
- [[language-protocol-substrate|Language Protocol Substrate]]
