---
schema: foundry-doc-v1
title: "Style Guide — Ticket Comment"
slug: topic-style-guide-ticket-comment
category: reference
type: topic
quality: core
short_description: "Editorial standards for the ticket-comment template in Foundry's service-disclosure library, covering conclusion-first structure, reference conventions for commits and files, the durable-record principle, and the operational register."
status: pre-build
last_edited: 2026-04-30
editor: pointsav-engineering
cites: []
paired_with: topic-style-guide-ticket-comment.es.md
---

A **ticket comment** is a conclusion-first, durable record on an issue tracker, pull-request review, or support thread — written for an asynchronous audience that may read it cold years after it was posted.

The ticket-comment template is part of the COMMS family in Foundry's `service-disclosure` genre-template registry. It covers comments on GitHub Issues, pull-request reviews, support tickets, and similar asynchronous threads. Unlike meeting notes (which record decisions) or memos (which document reasoning), a ticket comment is the primary unit of communication in a distributed workflow: it is both the message and the record. This style guide is the human-facing companion to `service-disclosure/templates/ticket-comment.toml`.

## When to use this template

Use the ticket-comment template whenever you are writing a comment that will become part of a tracked record — a PR review, a bug report reply, a feature-request response, a status update on a support ticket.

Do not use this template for ephemeral messages (Slack, email threads that will not be archived) where a durable-record discipline would be out of place.

## Frontmatter fields

Ticket comments do not carry frontmatter in the rendered output — they appear as plain Markdown inside an issue tracker's comment field. The template's `tenant_required: true` setting is a routing signal, not a rendered field; it tells the editorial pipeline which tenant adapter applies.

If you are producing a ticket-comment as a standalone document (a prepared review statement, a detailed incident explanation), the standard `foundry-doc-v1` frontmatter fields apply.

## Structure

The template defines no required sections — ticket comments vary too much in size and context to enforce a fixed structure. The required discipline is a **conclusion-first ordering**:

1. **State what you did or what you propose** — the bottom line, in the first sentence. A reviewer skimming ten comments should be able to read only the first sentence of each and still know what each commenter decided.
2. **The reasoning** — the supporting argument, evidence, or analysis, in as much detail as the ticket requires. Reference specific commits, files, and prior tickets rather than restating their contents.
3. **Open questions** — items the commenter could not resolve and needs the thread to address. State each question precisely.

This ordering matches the Bloomberg standard applied to all Foundry documents: a reader who stops after the first paragraph leaves with the news.

## Reference conventions

Ticket comments use a consistent reference vocabulary:

| Reference type | Format |
|---|---|
| Commit | Short SHA in backticks: `` `4244a02` `` |
| File and line | Path:line in backticks: `` `service-disclosure/src/validate.rs:47` `` |
| Prior ticket | Tracker ID: `#123`, `ISSUE-456` |
| PR | `PR #789` or the platform's native reference syntax |
| External document | Inline link or footnote — not bare URL |

Avoid restating what the linked artefact says. Write "the validation logic at `validate.rs:47` rejects empty required fields" rather than "looking at the code, I noticed that there is some validation logic which checks for empty fields and if they are empty it returns an error".

## Register and tone

The register is operational. Sentence-length target: mean around fourteen words, maximum around twenty-two. Active voice. First-person where the comment expresses a personal assessment; neutral voice where reporting a fact.

A ticket comment is durable. Write nothing you would not want a future incident reviewer, auditor, or new team member to read without context. This is not a chilling caution — it is an accuracy standard. A comment that would embarrass you under review is a comment that lacks the precision or care the record deserves.

The global banned-vocabulary list applies.

## See Also

- [[topic-style-guide-meeting-notes|Style Guide — Meeting Notes]]
- [[topic-style-guide-memo|Style Guide — Memo]]
- [[topic-style-guide-guide|Style Guide — GUIDE]]
- [[topic-language-protocol-substrate|Language Protocol Substrate]]

## References

---
Copyright © 2026 Woodfine Capital Projects Inc.
Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).
PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.