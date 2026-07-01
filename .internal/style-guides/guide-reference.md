---
schema: foundry-doc-v1
title: "Reference guide — encyclopedic reference and explanation"
slug: guide-reference
category: internal
type: reference
content_type: reference
quality: complete
status: active
audience: contributor-internal
bcsc_class: internal-only
governs: [PROSE-TOPIC, PROSE-ARCHITECTURE, PROSE-RESEARCH, PROSE-TEXT, PROSE-README, PROSE-INVENTORY, changelog, DESIGN-RESEARCH, JOURNAL]
last_edited: 2026-07-01
editor: pointsav-engineering
---

> The register guide for encyclopedic reference and explanation — the information-oriented
> prose a reader consults to look something up or to understand how a thing works. Builds on
> [[house-core]] and adds only the reference specialization. Where this guide is silent, the
> house core governs.

## 1. Purpose and audience

A reader comes to this prose with a question, not a task. They want to know *what a thing is*,
*how it fits*, or *why it works the way it does* — and they want the answer without reading to
the end. This is the reference-and-explanation half of the documentation quadrant: neutral,
information-oriented, built for lookup, not persuasion and not procedure.

The primary reader is anyone consulting the platform's own record — an engineer, a reviewer,
an analyst. A second reader looks over their shoulder: a machine indexing the corpus for
retrieval. Both are served by the same discipline. Pure reference is utilitarian and plain;
if a definition is boring and unmemorable, it is probably right. Explanation earns a little
more room to develop an idea thematically, but it never tips into advocacy.

## 2. The shape

Most articles follow one order: **lead → context → the mechanism, section by section → limits
and relations → references.** The lead defines and situates; the body develops one idea per
section; the close names what the thing is *not* and links to what it connects to.

Four artifact types fix part of that shape:

- **ARCHITECTURE** carries fixed sections in order: *position* (where it sits), *public
  surface* (what it exposes), *module layout* (how it decomposes), and *what this is not*
  (the boundary that prevents scope creep).
- **README** is orientation: a one-paragraph definition of the thing, how to enter it, and
  where to go next — the shortest article that still passes the isolation test.
- **INVENTORY and changelog** are structured records. Here a table or a dated list *is* the
  correct structure; prose is the wrapper, not the payload.
- **RESEARCH / TEXT / DESIGN-RESEARCH** are explanation-forward: they may develop a finding
  thematically, but each still opens with the claim, not the journey to it.

## 3. Opening

Lead with a one-sentence definition, then establish significance — the house lead rule, applied
tightly. The strongest first paragraph is often a single declarative sentence that says what the
subject is; the next few sentences say why it matters to the reader who must decide, operate, or
comply. A mature article's lead runs roughly 100 to 400 words, shorter for a short article, with
no bullets and no heading.

The isolation test for reference is exact: lift the lead out, and a reader who sees nothing else
must be able to state what the subject is and where it fits. A lead that opens on history,
motivation, or a narrative hook has buried its definition — front-load it.

For an INVENTORY or changelog, the lead says what the record covers and how it is ordered; the
entries follow.

## 4. Paragraph and sentence rhythm

One idea per paragraph, three to seven lines, varied deliberately — as [[house-core]] sets it.
The reference delta is on facts of record. A definition, a compliance claim, or a structural
invariant stays at or under twenty-five words, because a reader relies on it verbatim. Ordinary
explanatory sentences average fifteen to twenty.

Do not pad a sentence to square off a paragraph, and do not chain three clauses where two
sentences read cleaner. Explanation may run a slightly longer thread than pure reference when it
is developing a single mechanism — but the moment the idea changes, the paragraph ends.

## 5. Headings and scannability

Aim for a heading roughly every 90 to 150 words; sections run one to four paragraphs, and a
longer one wants a subheading for navigation. Treat anything over about 200 words per heading as
too sparse. Headings are sentence case, keyword first, so a reader scanning the left margin lands
on the term. The body carries no top-level heading — the
title comes from frontmatter.

Tables and lists earn their place only where the content is genuinely structured: an INVENTORY's
rows, a changelog's dated entries, an ARCHITECTURE module map, a comparison of fixed options.
Prose that has been chopped into bullets to look scannable is a defect — reference reads as
continuous prose punctuated by real records, not as an outline.

## 6. Voice and tone

Neutral, exact, active. Name the actor and the consequence: *"the resolver rejects an unknown
slug"* tells the reader what acts and what follows; *"unknown slugs are rejected"* hides the
actor. The register turns on the *neutral factual clause* — a statement a reader can verify
against the system, carrying no adjective that the fact has not earned.

Do not editorialize, rank, or flatter. State the specific number, the named mechanism, the
verifiable claim, and let significance follow from it. When a term of art appears, link to its
article rather than re-defining it in place — the web of references does the work, and each
article keeps to one job. A capability not yet true carries *planned* or *intended*; it is never
asserted as done.

## 7. Code and examples

Explanatory prose is light on inline code. A mechanism is explained in words first; code appears
only when the words genuinely need it, introduced by a sentence that says what it shows, and kept
to the minimum that makes the point.

The reference-versus-how-to line is the rule here: an explanation links to runnable, step-by-step
material rather than embedding it. If a reader would copy and execute the block, it belongs in a
how-to, and this article links to it. What stays inline is the short, illustrative fragment — a
schema shape, a signature, a one-line invariant — that clarifies the idea without becoming a
procedure.

## 8. Worked examples

**Padded to precise.**

> *Before:* Our revolutionary platform delivers seamless, best-in-class performance that
> effortlessly scales to meet your needs.
> *After:* The controller places workloads across the fleet by advisory heuristic; it has been
> measured to 200 nodes per cluster.

Annotation: adjectives that carry no information give way to the named mechanism and the tested
number — significance the reader can check.

**Buried lead to front-loaded definition.**

> *Before:* After years of teams struggling with brittle scripts and manual handoffs, a new
> approach emerged that would change how deployments work.
> *After:* A deployment record is a versioned description of one running instance. It lets an
> operator recreate, audit, or retire that instance from a single file.
> Annotation: the definition moves to sentence one; the lead now survives in isolation.

**Editorial to neutral.**

> *Before:* Impressively, the ledger never loses a write — a truly remarkable guarantee.
> *After:* The ledger is write-once: an appended entry is never modified or deleted.
> Annotation: the judgment word is dropped and the guarantee is stated as a checkable property.

### JOURNAL — academic variant

A JOURNAL article is reference prose with three added disciplines. Its literature review
establishes the gap the work addresses by describing the state of the field in structural terms —
what is unsolved — never by naming a competing product or organization as the foil. Authorship is
attributed to natural persons, not the platform or an engine. Everything else — front-loaded
claim, neutral voice — is the base reference form.

Wiki-only rules do not bind a JOURNAL: it carries no wikilinks (it is a standalone external
submission), follows its target venue's citation format and section lengths rather than the
heading-density band above, and needs no bilingual pair. Score a JOURNAL against its venue's
conventions and these three disciplines, not against the wiki checklist. The extra requirements
(external submission, citation format, contribution statements) live in the journal-artifact
discipline convention, which this section points to; do not restate them here.

## 9. Pre-publish checklist

- Does the lead survive in isolation — definition first, then significance?
- Does every paragraph carry one idea, and every fact of record stay under twenty-five words?
- Are headings sentence case, keyword first, roughly one every 75 to 100 words?
- Is every claim active-voice, naming the actor and the consequence, with no unearned adjective?
- Does every term of art link to its article instead of being re-defined?
- Is inline code minimal and introduced, with runnable steps linked to a how-to?
- For a structured record, is the table or list the payload and the prose only its wrapper?
- For a JOURNAL, does the literature review establish the gap without naming a competitor, and
  are authors natural persons?
