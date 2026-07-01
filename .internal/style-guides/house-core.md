---
schema: foundry-doc-v1
title: "House core — the shared craft of the writing machine"
slug: house-core
category: internal
type: reference
content_type: reference
quality: complete
status: active
audience: contributor
bcsc_class: public-disclosure-safe
last_edited: 2026-07-01
editor: pointsav-engineering
---

> This is the shared foundation every style guide builds on. It is not published on any
> wiki. Each register guide and house profile references this document and adds only what is
> specific to its artifact type or audience. When a specific guide is silent on a point, this
> document governs. This is the single source of truth for drafting language across the
> workspace; every other voice, register, or vocabulary note defers to the style-guide set.

## What this is

A writing machine is not a list of forbidden words. It is four things working together: a
positive standard that shows the target voice, a structural skeleton that constrains the shape
of each document, a quiet regression net that flags candidates without blocking anyone, and a
review loop that makes each draft better than the last. This document is the first of the
four. It teaches the craft that every artifact — an encyclopedia entry, a runbook, an investor
memo, a licence explainer — shares, before any register or house specialization applies.

The model is the encyclopedia, not the newspaper and not the product page. A reader who
finishes a piece should understand the subject, not merely have retrieved a fact or been sold
a feeling. Prose is scannable: short paragraphs, frequent headings, a summary that leads.
Voice is neutral and precise. Credibility comes from what is verifiable in the writing itself,
never from borrowing another institution's name for prestige.

## The opening

Every document opens with a lead that a reader can stop after and still leave with the point.

The lead states what the subject is and why it matters, in that order. The first sentence
defines the subject in plain terms. The next few sentences establish significance — the
consequence for the reader who must decide, operate, or comply. A mature article's lead runs
roughly 100 to 400 words depending on length; a short one is proportionally shorter. The lead
carries no bullet lists and no headings; it is continuous prose.

The test is isolation. Lift the lead out, show it to a reader who will see nothing else, and
the essential point must survive. If it does not, revise the lead before touching anything
else.

This is a front-loaded summary in the encyclopedic sense — a definition and its stakes — not a
newspaper's narrative hook that withholds the point for effect. Open with the news, then
develop it.

## Paragraph and sentence rhythm

One idea per paragraph. When the idea changes, the paragraph ends.

Vary paragraph length deliberately. A one-sentence paragraph that states a definition is
correct and often the strongest way to open a section:

> **Capitalisation rate:** net operating income divided by market value.

Then expand. Most paragraphs run three to seven lines. A paragraph that pushes past that is
usually carrying two ideas — split it. Do not lengthen sentences to reduce the paragraph
count; prefer more short paragraphs to fewer dense ones.

Sentences average roughly fifteen to twenty words. A sentence that states a fact of record — a
definition, a compliance claim, a regulatory statement — stays at or under twenty-five words,
because a claim a reader must rely on should be short enough to hold in one breath. Vary the
rhythm: give every paragraph at least one short declarative sentence, so the prose reads as an
accordion rather than a monotone. Avoid chaining more than two clauses with *and*, *or*, or
*but*; a sentence with several commas is usually two sentences.

## Headings and scannability

Headings are navigation, not decoration. They let a reader find the section they need without
reading the ones they do not.

Aim for a heading roughly every 90 to 150 words of body — denser than a report, closer to an
encyclopedia. A 600-word article carries four to seven headings. Treat anything above about 200
words per heading as too sparse: the section has become a wall the reader cannot navigate.
Sections run one to four paragraphs; a section longer than that wants a subheading. Do not
over-section either: a heading above a single short paragraph adds clutter, not navigation.
(Band calibrated 2026-07-01 against mature articles that read well at ~120–140 words/heading; the
earlier 75–100 target flagged good prose as thin — see the calibration report.)

Write headings in sentence case, with the most important word first, so a reader scanning the
left margin lands on the keyword. "Rollback procedure" beats "How to roll back the change."
The document title comes from frontmatter; the body never carries a top-level `#` heading.

## Capitalization

Casing is authored into the artifact, never left to rendering. The wiki engine prints a title and
a heading exactly as written — it applies no title-case or sentence-case transform, and no
automatic transform could, because it cannot know that `WORM`, `BIM`, `seL4`, `os-console`, or
`service-email` carry canonical casing a title-caser would corrupt. The author owns the casing.

One rule for every title and every heading: **sentence case, keyword first.** Capitalize the first
word and nothing after it except proper nouns, acronyms, and code identifiers, which keep their
canonical form. "Debt service and financing structure," not "Debt Service and Financing Structure."
"WORM ingest," not "Worm ingest." "seL4 capability topology," never "Sel4 Capability Topology." The
slug stays lowercase-kebab regardless (`debt-service-and-financing-structure`).

**Keyword first means no leading article.** No `title:`, no heading, and no slug begins with *the*,
*a*, or *an* — drop it, so the first word a reader scans and the first character the wiki files on is
the meaningful one. Write `title: "Citation substrate"` / `slug: citation-substrate`, never
`title: "The citation substrate"` or `slug: the-citation-substrate`. This is keyword-first applied to
the first word: a category page sorts its list by slug and *displays* the title, so a column of
entries all opening with *The* is unscannable, and on any title-sorted surface it mis-files every one
under T. The article returns naturally in body prose ("The citation substrate records every claim…");
only the title and the slug — the display's first word and the index key — shed it. The Spanish pair
follows: no title opens with *el/la/los/las/un/una*. The one exception is a proper name whose article
is genuinely part of the name; even then the slug drops the article (`ledger`, not `the-ledger`) so
the filing key stays clean.

This applies to the frontmatter `title:` and to every `##` / `###` heading, in every artifact type.
It is the same rule the headings section already assumes, now stated once for titles as well —
because the engine passes both through verbatim, and consistency has to live in the source.

**File names are cased differently — lowercase, always.** The file name is not display text; it is
an identifier, and it is the slug. Use lowercase ASCII, kebab-case: words joined by single hyphens,
no spaces, no underscores, no capitals — `debt-service-and-financing-structure.md`, never
`Debt-Service.md` or `debt_service.md`. The filename stem equals the `slug:` field exactly. A
bilingual pair adds `.es.md` (`debt-service-and-financing-structure.es.md`). Once published a slug
is immortal — rename through an alias, never by re-casing the file. So three casings, one per layer:
**lowercase-kebab for the file/slug, sentence case for the title, sentence case for the headings.**

## Voice and tone

Write in the active voice by default. Active voice names the actor and the consequence: "the
gateway holds every key" tells the reader who is responsible; "keys are held centrally" hides
it. Use the passive only when the actor is genuinely irrelevant or the object is the true
subject of the sentence.

Name actors and consequences. Every claim of fact says who does what, and what follows if they
do not. Abstract nouns and agentless constructions are where precision goes to hide.

The tone is neutral and exact. Do not editorialize, do not flatter, and do not reach for the
promotional register of a product page. The words that carry no information — the reflexive
intensifiers of marketing copy — dilute prose rather than sharpen it; the positive move is
always to state the specific fact instead. The advisory linter will surface these as
candidates, but the discipline lives here: prefer the concrete noun and the named number.

Analogy is a ceiling, not a quota. One analogy per few hundred words at most; prose with none
is fully compliant. An analogy in every paragraph is a tell that the mechanism was never
explained plainly.

## Establishing credibility without names

Credibility comes from what is visible in the subject itself — the mechanism, the number, the
verifiable claim — not from association with a named institution.

Do not use a real company or publication as a stand-in for quality or prestige. "Written to
the standard a senior analyst would expect" is a benchmark; "written to satisfy a [named bank]
analyst" borrows a name the writing has not earned. The first is positive craft; the second is
the pattern to avoid, and once this principle is held it simply does not appear.

Naming a company for a *factual* reason is different and allowed. A payment rail the system
actually integrates, a standards body a specification actually cites — these are facts, and
facts get named. The line is between a factual reference and a borrowed benchmark.

## Forward-looking language

State present facts in the present tense and the active voice. A capability, timeline, or
outcome that is not yet true does not get asserted as accomplished; it carries *planned*,
*intended*, *may*, or *target*, with a reasonable basis and, where the context is regulated,
the cautionary framing the disclosure posture requires. Never give a system human intent or
feeling.

## Cross-references

Link the reader to the definition rather than repeating it. When a term has its own article or
section, reference it once and move on; do not re-explain the mechanism a linked article
already carries. This keeps each document to a single job and lets the web of references do the
work of building understanding. A document that re-explains everything it touches is doing four
documents' jobs badly.

## The draft-improves-the-draft loop

No single pass has to be perfect. The standard for any given sweep is "draft two of ten" — good
enough that the next pass, human or machine, produces a clearly better draft three. Perfection
in one pass wastes effort better spent establishing the frame that makes every later pass
better. Each edit against this standard is also a training example: the machine that drafts the
next version learns from the one the editor accepted.

## How the specific guides use this document

Each register guide (reference, how-to, communications, legal) and each house profile
(documentation, corporate, projects) opens by pointing here, then specifies only its
differences: the section skeleton for its artifact type, its register and audience, its code
policy, and two or three worked examples in its own voice. Everything above is assumed. When a
specific guide and this document appear to conflict, the specific guide governs for its own
artifact type — but it should rarely need to, because the craft is shared.
