---
schema: foundry-doc-v1
title: "Style-guide template — the shared skeleton"
slug: style-guide-template
category: internal
type: reference
content_type: reference
quality: complete
status: active
audience: contributor-internal
bcsc_class: internal-only
last_edited: 2026-07-01
editor: pointsav-engineering
---

> The reusable skeleton for every register guide and house profile. Copy the nine headings
> below and fill each in for the specific artifact type. Every guide is "set up the same way"
> so a writer who knows one knows them all. Keep the whole document scannable — it must itself
> obey the craft it teaches. Do not restate [[house-core]]; reference it and add only the
> specialization.

## 1. Purpose and audience

One or two paragraphs. Who reads this artifact type, what decision or task they bring to it,
and what they must leave with. Name the register this guide inherits and any second audience
that reads over the primary reader's shoulder.

## 2. The shape

The section skeleton for this artifact type, in order, one line each. This is the structural
scaffold — the part of the writing machine that constrains form before a word is written. If
the artifact has required sections, list them; if it has a canonical order, fix it here.

## 3. Opening

How this artifact type leads, as a specialization of the house lead rule. Give the exact shape
of the first paragraph and what the lead must accomplish for this reader. State the isolation
test in this artifact's terms.

## 4. Paragraph and sentence rhythm

Only the deltas from [[house-core]]: the sentence-length target and ceiling for this register,
and any rhythm note specific to the type (a runbook is terser than an explanation; a legal
clause is more measured). If there is no delta, say so in one line and move on.

## 5. Headings and scannability

Heading density and any fixed heading names for this artifact type. Note whether tables, lists,
or callouts are the right structure for this type's recurring content.

## 6. Voice and tone

The register in positive, exemplary terms. Show the move this artifact type turns on — the
consequence-first sentence, the imperative step, the neutral clause — with a one-line model of
it. No forbidden-word tables; teach the positive alternative.

## 7. Code and examples

The code policy for this artifact type, stated positively. Where code belongs, how it is
introduced, and what is pulled out to a linked reference instead of embedded. Apply the
reference-versus-how-to distinction: an explanation links to the rationale; a how-to carries
the steps.

## 8. Worked examples

Two or three short pairs — a weaker version and a stronger one — each with a single line of
annotation naming what changed and why. This is the part that teaches the AI and the copy
editor the linguistic type by demonstration. Keep each example a few sentences at most.

## 9. Pre-publish checklist

Five to eight positive checks, each a question a writer answers yes to. "Does the lead survive
in isolation?" "Does every term of art link to its definition?" "Does each step name its
verification?" Checks, not prohibitions.

---

## Frontmatter every guide carries

```yaml
---
schema: foundry-doc-v1
title: "<Register or house> guide — <one line>"
slug: <kebab-slug>
category: internal
type: reference
content_type: reference
quality: complete
status: active
audience: contributor-internal
bcsc_class: internal-only
governs: [<ARTIFACT-TYPE>, <ARTIFACT-TYPE>]   # the artifact types this guide covers
last_edited: <YYYY-MM-DD>
editor: pointsav-engineering
---
```

The `governs:` list is what the coverage matrix reads to prove every prose artifact type maps
to exactly one guide. A white-label register guide names artifact types generically; a house
profile names the wikis it specializes and points to the register guide it layers on.
