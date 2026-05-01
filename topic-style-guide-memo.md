---
schema: foundry-doc-v1
title: "Style Guide — Memo"
slug: topic-style-guide-memo
category: reference
type: topic
quality: core
short_description: "Editorial standards for the memo template in Foundry's service-disclosure library, covering the Background–Decision–Consequences structure, frontmatter citation requirements, Bloomberg register, and the edit-in-place rule for revisions."
status: pre-build
last_edited: 2026-04-30
editor: pointsav-engineering
cites:
  - ni-51-102
  - osc-sn-51-721
paired_with: topic-style-guide-memo.es.md
---

A **memo** in Foundry is an internal architecture or decision record — a durable account of what problem existed, what was chosen, and what changes as a result — written to a grade-12 reading level with citations for every non-obvious claim.

The memo template is part of the PROSE family in Foundry's `service-disclosure` genre-template registry. It is the written form of an Architecture Decision Record (ADR): a memo explains a decision fully enough that a reader who joins the project years later can understand why the system is the way it is. This style guide is the human-facing companion to `service-disclosure/templates/memo.toml`.

## When to use this template

Use the memo template when a decision affects the architecture, governance, or operational posture of the platform and needs a durable first-person record — not a ticket comment or a README update, but a self-contained document a future engineer can read cold. Architectural choices, library selections, security posture decisions, and governance changes all warrant a memo.

Do not use a memo for operational instructions ("run these commands"). Those belong in GUIDE files. Do not use a memo for conceptual background without a decision. That belongs in a TOPIC.

## Frontmatter fields

Memos carry full frontmatter. Required fields:

| Field | Notes |
|---|---|
| `schema` | `foundry-doc-v1` |
| `title` | Identifies the decision — e.g., "Selecting OLMo 3 7B Q4 as Tier A Local Model" |
| `cites` | Required when the memo makes claims resolving to external documents. See §16 of `CLAUDE.md` for citation discipline |
| `forward_looking` | Boolean. Set `true` when the memo describes a planned or intended outcome, not a settled fact |
| `status` | `stable` when the decision is settled; `pre-build` when under active review |
| `last_edited` | ISO 8601 date — keep current across revisions |

The `forward_looking` field triggers the BCSC disclosure posture per `[ni-51-102]` and `[osc-sn-51-721]`: forward-looking statements carry `planned`, `intended`, `may`, or `target` language, a stated reasonable basis, cautionary language, and material assumptions.

## Structure

The template defines three required sections:

**Background** — The problem and the relevant constraints. A reader who knows nothing about the decision should understand, after reading this section, why a decision was necessary. Name the alternatives that were considered only briefly here; the reasoning for the choice comes in the next section.

**Decision** — What was chosen and why. This is the core of the memo. One or two paragraphs that state the choice clearly in the first sentence, then give the reasoning. Cite non-obvious claims. Reference prior memos by canonical name when the decision builds on an earlier one.

**Consequences** — What changes downstream and what trade-offs are accepted. This section is as important as the Decision section. A decision that seems correct in isolation may be costly when its consequences are spelled out. Name the costs explicitly; future reviewers will thank you.

## Register and tone

The register is Bloomberg — precise, professional, and understandable to a financially literate reader without a technical background. The sentence-length target is longer than operational templates: mean around eighteen words, maximum around thirty. Memos carry arguments and nuance; sentence length reflects that complexity.

Active voice unless passive carries specific meaning. Cite every non-obvious claim. Flag every forward-looking statement with reasonable basis.

The global banned-vocabulary list applies in full: `leverage`, `empower`, `next-generation`, `industry-leading`, `seamless`, `robust`, `cutting-edge`, `world-class`.

## Edit-in-place rule

A memo is never versioned by creating a `_V2` or `_V3` copy. Edit the existing file; rely on Git history for prior versions. This is workspace policy per `CLAUDE.md` §6. When a memo is substantially revised — a decision reversed, a new constraint identified, a consequence that was not anticipated — update `last_edited` in frontmatter and add a brief note at the bottom of the Consequences section describing what changed and why.

Do not restart numbering for memo series. If MEMO-2026-03-30 is revised, it remains MEMO-2026-03-30. The date in the title reflects the original decision date, not the revision date.

## See Also

- [[topic-style-guide-topic|Style Guide — TOPIC]]
- [[topic-style-guide-guide|Style Guide — GUIDE]]
- [[topic-style-guide-meeting-notes|Style Guide — Meeting Notes]]
- [[topic-citation-substrate|Citation Substrate]]
- [[topic-language-protocol-substrate|Language Protocol Substrate]]

## References

---
Copyright © 2026 Woodfine Capital Projects Inc.
Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).
PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.