---
schema: foundry-doc-v1
title: "Style Guide — License Explainer"
slug: topic-style-guide-license-explainer
category: reference
type: topic
quality: core
short_description: "Editorial standards for the license-explainer template in Foundry's service-disclosure library, covering structure, the four required sections, bilingual pair requirements, reading-level targets, and the relationship to the canonical license file."
status: pre-build
last_edited: 2026-04-30
editor: pointsav-engineering
cites:
  - ni-51-102
paired_with: topic-style-guide-license-explainer.es.md
---

A **license explainer** is a plain-language summary of a license — readable in five minutes by a non-lawyer — that always directs the reader to the canonical license file rather than replacing it.

The license-explainer template is part of the PROSE family in Foundry's `service-disclosure` genre-template registry. It serves contributors, customers, and the public alike: a newcomer opening a repository should be able to understand what they may and may not do with the code without needing to parse the full license text. This style guide is the human-facing companion to `service-disclosure/templates/license-explainer.toml`.

## When to use this template

Use the license-explainer template when you need to publish a plain-language interpretation of a license alongside the canonical license file — for example, in a repository README, in a wiki article explaining the licensing posture of a project, or in onboarding materials for contributors.

Do not use this template to replace the canonical license file. The canonical file at the repository root governs; the explainer is a reading aid, not a legal artefact.

## Frontmatter fields

License-explainer documents are public-facing, so they carry the standard `foundry-doc-v1` frontmatter. Required fields:

| Field | Notes |
|---|---|
| `schema` | `foundry-doc-v1` |
| `title` | Identifies the license covered (e.g., "CC BY 4.0 — License Explainer") |
| `status` | `stable` when matched to the live canonical file; `pre-build` while under review |
| `last_edited` | ISO 8601 date — must be updated when the canonical license changes |

Because a license explainer makes claims about a legal instrument, the `cites` field is used when the canonical license is a published external standard (e.g., `cc-by-4`). Where the license is a proprietary text without a stable external URI, a reference in the Authoritative text section suffices.

## Structure

The template defines four required sections:

**What you may do** — Bullet points in plain language. Each bullet names one permission the license grants. Avoid conditional language that mirrors the license exactly; the goal is comprehension, not reproduction. If the license grants broad use with minor conditions, say so directly.

**What you must do** — The obligations. Attribution, share-alike, notice-preservation, and similar requirements. State each as a plain instruction — "Include a copy of this license in every distribution" — not as a paraphrase of the license clause.

**What you must not do** — The prohibitions. Trademark use, patent claims, relicensing, commercial restrictions if any. Same plain-instruction form as obligations.

**Authoritative text** — A direct link to or quotation of the canonical license file. The section closes with an explicit note that the canonical file governs. This section is mandatory and must be the last in the document.

## Register and tone

The register is Bloomberg — precise, professional, and understandable to a financially literate reader without a legal background. The sentence-length target for this template is short: mean around fourteen words, maximum around twenty-two. This is deliberately tighter than the memo or TOPIC templates because license explainers are often read on mobile or in terminal contexts where short lines matter.

Avoid legalese. "The licensor grants you a worldwide, royalty-free, non-exclusive license to reproduce" should become "You may copy and distribute this work worldwide at no cost." Accuracy matters; the goal is not to water down the license but to make it accessible without an interpreter.

The global banned-vocabulary list applies. No `leverage`, no `seamless`, no `world-class`.

## Example

A CC BY 4.0 license explainer follows this shape:

```markdown
## What you may do

- Copy and distribute the work in any medium or format.
- Adapt, remix, and build upon the work for any purpose, including commercial use.

## What you must do

- Give appropriate credit — name the original author and the project.
- Include a link to the license.
- Indicate if you made changes to the original work.

## What you must not do

- Imply that the licensor endorses your use.

## Authoritative text

The full text of CC BY 4.0 is at <https://creativecommons.org/licenses/by/4.0/legalcode>.
The `LICENSE` file at the root of this repository is the canonical licence for this project.
The above is a reading aid only — that file governs.
```

## See Also

- [[topic-style-guide-readme|Style Guide — README]]
- [[topic-style-guide-topic|Style Guide — TOPIC]]
- [[topic-style-guide-terms|Style Guide — Terms of Service]]
- [[topic-language-protocol-substrate|Language Protocol Substrate]]
- [[topic-canadian-simple-copyright|Canadian Simple Copyright]]

## References
