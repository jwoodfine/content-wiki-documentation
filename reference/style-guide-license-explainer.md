---
schema: foundry-doc-v1
title: "Style guide — license explainer"
slug: style-guide-license-explainer
category: reference
type: topic
quality: complete
short_description: "Editorial standards for license explainer documents (PROSE genre) in the platform: lede discipline, permits/requires/forbids structure, where binding text lives, and the distinction between an explainer and the license itself."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-24
editor: pointsav-engineering
cites: []
paired_with: style-guide-license-explainer.es.md
---

> A license explainer translates a legal instrument into plain terms. It is not the license. If the explainer and the license conflict, the license wins.

A **license explainer** (PROSE genre) is a plain-language companion to a formal license document. It helps a reader understand what the license permits, requires, and forbids without having to parse legal text. An explainer is not legally binding — it is a reading aid. The binding text is always the formal license document linked from the explainer. This article is the human-facing standard; the machine-readable counterpart lives in `service-disclosure/templates/license-explainer.toml`.

## When to use this template

Write a license explainer when:

- A repository carries a license that affects contributors or consumers in non-obvious ways.
- The audience includes people who are not legal professionals.
- The license has conditions (attribution, share-alike, CLA requirement) that need to be understood to comply.

The explainer is not a substitute for legal review. For agreements that bind individuals or organisations to specific obligations, route through the responsible governance party (`factory-release-engineering` or the system administrator at `open.source@pointsav.com`) before publishing.

## Structure

The template requires five sections in this order:

| Section | Purpose |
|---|---|
| **Lede** | One to two sentences: what license this is and what it is designed to accomplish. No legal jargon. |
| **What it permits** | A bulleted list of what this license explicitly allows. Plain verbs: "Use commercially", "Modify the source", "Distribute copies". |
| **What it requires** | A bulleted list of conditions. Plain verbs: "Include the copyright notice", "State changes made", "Provide access to source". |
| **What it forbids** | A bulleted list of restrictions. Plain verbs: "Hold the author liable", "Use the trademark without permission". Omit this section if the license forbids nothing. |
| **Where binding text lives** | A direct link to the full formal license document and a statement that the formal text governs wherever the explainer and the formal text disagree. |

## Register and tone

Plain English. No "aforementioned," "notwithstanding," or "herein." The goal is comprehension, not impressiveness.

Sentence-length budget: mean around eighteen words, maximum thirty. Bullet items are imperative phrases beginning with a verb, not full sentences. The Lede may be two sentences maximum.

## See also

- [[style-guide-policy|Style Guide — Policy]]
- [[style-guide-cla|Style Guide — CLA]]
- [[language-protocol-substrate|Language Protocol Substrate]]
