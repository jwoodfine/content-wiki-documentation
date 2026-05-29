---
schema: foundry-doc-v1
title: "Style guide — memo"
slug: style-guide-memo
category: reference
type: topic
quality: complete
short_description: "Editorial standards for internal memoranda (PROSE-MEMO genre) in the platform: header discipline, section order, the recommendation-first convention, and when a memo is the right artifact."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-24
editor: pointsav-engineering
cites: []
paired_with: style-guide-memo.es.md
---

> A memo records a decision, analysis, or recommendation addressed to a named audience. It is complete when the reader knows what was decided and what happens next — without reading anything else.

A **memo** (PROSE-MEMO genre) is an internal document addressed to a specific recipient for a specific decision or recommendation. It is not a status update, not a design document, and not a policy. A memo closes open questions; it does not catalogue them. For register and tone discipline applied to all prose artifacts, see [[editorial-language-registers]]. This article describes the human-facing standard; the machine-readable counterpart lives in `service-disclosure/templates/memo.toml`.

## When to use this template

Use a memo when:

- A decision has been reached and needs to be communicated with the analysis that led to it.
- A recommendation is ready for a named decision-maker and the recommendation cannot be delivered in a single paragraph.
- A complex cross-functional question is settled and the settlement needs to be on record.

Do not use a memo for ongoing discussion, for project status, or for questions that remain open. An open question belongs in an inbox message, a NEXT.md item, or a brief.

## Structure

The template requires a header block and five sections:

**Header block** (before any heading):

```
To:   <recipient name or role>
From: <author name or role>
Date: <YYYY-MM-DD>
Re:   <one-line subject — specific, actionable>
```

| Section | Purpose |
|---|---|
| **Summary** | The conclusion, stated first. One to three sentences: what was decided or recommended and the key constraint. The reader who reads only this section must be able to act on it. |
| **Context** | What precipitated the memo. The facts a recipient needs to evaluate the recommendation. Not the full history — only what is load-bearing. |
| **Analysis** | The reasoning. Structured as numbered points or short paragraphs. Acknowledges the strongest counterargument and explains why it was not decisive. |
| **Recommendation** | The specific action requested, with owner and timeline. A memo with no recommendation is a brief; restructure it accordingly. |
| **Next steps** | Concrete follow-on actions, owners, and dates. This is the section that gets executed. |

## Register and tone

Formal but plain. The register is professional prose, not legalese. State the recommendation before the analysis — readers at the recipient level do not need to reconstruct the conclusion from the evidence. The Subject (`Re:`) line must be specific: "Approve Q3 content freeze — 2026-08-15" rather than "Content freeze update."

Sentence-length budget: mean around twenty-two words, maximum forty. Active voice throughout the body. The Analysis section may use numbered points; the Recommendation and Next steps use imperative sentences.

The banned-vocabulary list applies. No `"leverage"`, `"facilitate"`, or `"synergize"` in professional correspondence — state the specific action directly.

## See also

- [[style-guide-topic|Style Guide — TOPIC]]
- [[style-guide-guide|Style Guide — GUIDE]]
- [[language-protocol-substrate|Language Protocol Substrate]]
