---
schema: foundry-doc-v1
title: "Style Guide — Chat message"
slug: topic-style-guide-chat
category: reference
type: topic
quality: core
short_description: "Editorial standards for chat messages routed through the Foundry language-protocol stack, covering the COMMS family, the six-line cap, casual register, and the channel-tone discipline."
status: pre-build
last_edited: 2026-04-30
editor: pointsav-engineering
cites: []
paired_with: topic-style-guide-chat.es.md
---

> A chat message carries one idea, stays under six lines, and matches the channel's existing tone — when a message needs more than that, it belongs in a different channel.

A **chat message** in the Foundry language-protocol stack belongs
to the COMMS family alongside email. It represents
instant-messaging output: a Slack message, a Teams post, an
in-application notification. The shape is constrained: one idea
per message, no structural headers, casual register, a default
cap of six lines. The machine-readable counterpart lives in
`service-disclosure/templates/chat.toml`.

## When to use this template

Use the chat template when the Doorman (`service-slm`) is
generating or improving a message destined for an
instant-messaging channel. Common cases: a project-status
update in a team channel, a notification to a colleague, a
short answer to an in-channel question.

When a message genuinely requires more than six lines — a
multi-step procedure, a formal decision, a record that will be
cited later — consider whether email (`topic-style-guide-email`)
or a written document is the correct channel. The chat template
is not a substitute for more structured output; it is the right
tool when brevity and conversational tone are the requirements.

## Frontmatter fields

Chat messages are transient artefacts; they do not carry
YAML frontmatter in the way that documents do. The key
per-request parameters are set by the `ProtocolRequest` at
routing time:

| Field | Notes |
|---|---|
| `tenant` | Required. The tenant slug identifies which per-tenant adapter shapes the voice. |
| `genre_template` | `GenreTemplate::Chat` |
| `register` | Defaults to `casual`. The Doorman may override per channel context. |

The `tenant_required = true` flag in the template means the
Doorman will reject a chat request that does not name a tenant.
Every chat message belongs to a voice; there is no
tenant-agnostic chat output.

## Structure

The chat template has no required sections. A chat message is
a single prose block, occasionally a numbered list when the
content is a literal sequence of steps. Headers, subheadings,
and horizontal rules are not used.

Content discipline:

- One idea per message. If two distinct ideas are present, send
  two messages.
- Default cap: six lines. Messages longer than six lines are
  flagged in the prompt scaffolding; the writer must either
  cut or signal the length ("longer one — fyi") before
  sending.
- No bullet lists unless the content is an actual enumerable
  sequence. A prose thought broken into bullets is not a list;
  it is fragmented prose.

## Register and tone

The register is casual. Sentence-length budget: mean around ten
words, maximum around eighteen. Short sentences — one clause per
sentence is the target shape.

When writing a reply, mirror the asker's register. A formal
question warrants a more considered tone; a conversational
question warrants a conversational answer. The Doorman applies
the per-tenant adapter to keep the voice consistent.

The banned-vocabulary list applies. Even in casual writing,
terms like "leverage", "seamless", and "robust" carry no
information. The list exists precisely because AI-generated text
tends toward these terms at high frequency.

Hedging adverbs — "just", "simply", "basically", "honestly" —
weaken the message. They are not casual register; they are noise.

## Example

```
Reviewed the routing logic. The issue is in the tenant-adapter
lookup — it checks the wrong field at line 47. I'll have a fix
up by noon.
```

A message like this example: one idea, three sentences, plain
language, no headers.

## See also

- [[topic-style-guide-email|Style Guide — Email]]
- [[topic-language-protocol-substrate|Language Protocol Substrate]]
- [[topic-anti-homogenization-discipline|Anti-Homogenization Discipline]]

## References

---
Copyright © 2026 Woodfine Capital Projects Inc.
Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).
PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.