---
schema: foundry-doc-v1
title: "Style Guide — Meeting Notes"
slug: topic-style-guide-meeting-notes
category: reference
type: topic
quality: core
short_description: "Editorial standards for the meeting-notes template in Foundry's service-disclosure library, covering the three required sections, the action-item discipline, what to omit, and the operational register."
status: pre-build
last_edited: 2026-04-30
editor: pointsav-engineering
cites: []
paired_with: topic-style-guide-meeting-notes.es.md
---

**Meeting notes** are the durable record of a meeting — who attended, what was decided, and who owes what by when — not a narrative of the conversation that led there.

The meeting-notes template is part of the COMMS family in Foundry's `service-disclosure` genre-template registry. It sits inside the same editorial pipeline as other operational documents and is subject to the same voice and vocabulary standards. This style guide is the human-facing companion to `service-disclosure/templates/meeting-notes.toml`.

## When to use this template

Use the meeting-notes template any time a meeting produces decisions or follow-up actions that need a durable record — architecture reviews, sprint planning sessions, stakeholder briefings, and operational standups alike.

Do not use this template to produce a transcript. Discussion that does not produce a decision or an action item does not belong in meeting notes.

## Frontmatter fields

Meeting notes are internal operational documents. Frontmatter is optional but useful for longer-lived records:

| Field | Notes |
|---|---|
| `title` | Meeting name and ISO 8601 date (e.g., "Service-SLM Architecture Review — 2026-04-30") |
| `status` | `stable` once actions are assigned; `draft` while the record is being written up |
| `last_edited` | ISO 8601 date |

The `cites` field is not typically used in meeting notes. If the meeting discussed an external document (a regulatory filing, a third-party specification), reference it inline in the relevant section.

## Structure

The template defines three required sections:

**Attendees** — A list of everyone who was present. Include name and role. If attendance was partial (someone joined late or left early), note it. A reader who opens these notes a year later needs to know who was in the room and what decisions they were party to.

**Decisions** — A list of what was decided, not how it was decided. Each entry names the decision and, where relevant, the reasoning in one sentence. "Adopted OLMo 3 7B Q4 as Tier A local model — open weights, Apache 2.0, sufficient quality for initial editorial assist" is a complete decision entry. "We had a long discussion and eventually agreed that the OLMo model was probably the right choice for local inference" is not.

**Action items** — Each item names an owner, a verb, an object, and a due date. These four elements are all required. An item without an owner is a wish. An item without a due date is a backlog entry. The form is: "`<owner>` to `<verb>` `<object>` by `<date>`."

Two optional sections are available:

**Context** — One paragraph if the meeting required framing that is not self-evident from the Decisions section. Omit this section when the decisions speak for themselves.

**Open questions** — Items raised but not decided. Each entry states the question clearly and names who will close it if known.

## Register and tone

The register is operational, not narrative. Sentences describe facts and actions; they do not reflect tone, express opinions, or summarise argument. The sentence-length target for this template is short: mean around fourteen words, maximum around twenty-two.

Active voice throughout. "Jennifer will draft the policy by 2026-05-07" is correct. "The policy will be drafted by Jennifer" loses the assignment clarity that makes minutes useful.

The global banned-vocabulary list applies.

## Example

```markdown
## Attendees

- Jennifer Woodfine (Woodfine Management Corp., staging contributor)
- ps-administrator (PointSav Digital Systems, System Administrator)

## Decisions

- Selected cluster-wiki-draft-pipeline as the mechanism for TOPIC
  production. Rationale: bilingual pair requirement and BCSC
  posture need a single editorial gateway.

## Action items

- Jennifer to draft `topic-style-guide-memo.md` in
  `content-wiki-documentation` by 2026-05-03.
- ps-administrator to ratify Tetrad legs for project-language
  cluster by 2026-05-07.

## Open questions

- Does the wiki TOPIC pipeline need a separate review gate before
  `status: stable`? Owner: ps-administrator. Expected close: next
  architecture review.
```

## See Also

- [[topic-style-guide-memo|Style Guide — Memo]]
- [[topic-style-guide-ticket-comment|Style Guide — Ticket Comment]]
- [[topic-language-protocol-substrate|Language Protocol Substrate]]

## References

---
Copyright © 2026 Woodfine Capital Projects Inc.
Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).
PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.