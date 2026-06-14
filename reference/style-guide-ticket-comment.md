---
schema: foundry-doc-v1
title: "Style guide — ticket comment"
slug: style-guide-ticket-comment
category: reference
type: topic
content_type: topic
quality: complete
short_description: "Editorial standards for ticket comments in the platform (COMMS genre): header discipline, what-changed-and-next structure, status field conventions, and when to comment versus when to update the ticket description."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-24
editor: pointsav-engineering
cites: []
paired_with: style-guide-ticket-comment.es.md
---

> A ticket comment records a state change or a decision — not a thought. Every comment advances the ticket.

A **ticket comment** (COMMS genre) is a structured update on an issue, task, or work item. It is addressed to anyone who reads the ticket's history after the comment is posted. Unlike a [[style-guide-chat|chat message]] (which is synchronous and ephemeral), a ticket comment is a permanent record and may be read months later by someone with no context from the thread. This article is the human-facing standard; the machine-readable counterpart lives in `service-disclosure/templates/ticket-comment.toml`.

## When to use this template

Write a ticket comment when:

- The status of the work has changed and stakeholders need to know.
- A decision was made that affects the ticket's scope, timeline, or owner.
- A blocker has been identified or resolved.
- An action was completed and the completion needs to be on record.

Do not comment to say you are working on the item — update the Status field instead. Do not post exploratory thoughts or half-formed questions as comments; draft them privately and post when the conclusion is clear.

## Structure

**Header block** (before any body text):

```
Ticket: <ticket-id or title>
Status: <new status — Open | In progress | Blocked | Review | Done>
```

| Section | Purpose |
|---|---|
| **What changed** | One to three sentences: the specific change in state, decision made, or fact established. Name the artifact, commit SHA, or decision explicitly. |
| **Next** | The concrete next step, with owner. A ticket comment with no "Next" is a dead end — the reader cannot act on it. If the ticket is Done, "Next" is "Closed." |

## Register and tone

Factual and brief. Past tense for what changed ("Committed X at hash Y"); present or future for next steps ("Owner: Jennifer; due 2026-06-01"). No hedges — either the state changed or it did not.

Status field values are a closed set: `Open`, `In progress`, `Blocked`, `Review`, `Done`. No custom values.

Sentence-length budget: one to two sentences per section. If "What changed" needs more than three sentences, the change is complex enough to warrant a brief or a memo — reference it from the ticket comment rather than writing it inline.

## See also

- [[style-guide-chat|Style Guide — Chat]]
- [[style-guide-meeting-notes|Style Guide — Meeting Notes]]
- [[language-protocol-substrate|Language Protocol Substrate]]
