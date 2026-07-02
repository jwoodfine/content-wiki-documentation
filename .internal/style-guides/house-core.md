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

Everything here is taught as the better move, never as a prohibition. Where a weaker habit
exists, the guide shows the stronger one beside it and lets the contrast do the arguing. An
advisory linter runs separately and flags candidates; the craft lives on this page.

## Reader and the model

The model is the encyclopedia, not the newspaper and not the product page. A reader who
finishes a piece should understand the subject, not merely have retrieved a fact or been sold
a feeling.

Write for a scanning reader, because that is the reader you have. Eye-tracking studies of
on-screen reading are unanimous: most readers scan headings and openings first and sample the
prose between them; the reader who reads every word is the exception. Craft for this reality
rather than resenting it — front-load the point, keep paragraphs short, make every heading a
promise the section keeps. Voice is neutral and precise. Credibility comes from what is
verifiable in the writing itself, never from borrowing another institution's name for
prestige.

## Opening and the lead

Every document opens with a lead a reader can stop after and still leave with the point.

The lead states what the subject is and why it matters, in that order. The first sentence
defines the subject in plain terms a nonspecialist can hold — a concise definition, not a
gesture toward one. The next few sentences establish significance: the consequence for the
reader who must decide, operate, or comply. Then the lead compresses the article's most
important points, so it works as a miniature of the whole. A mature article's lead runs
roughly 100 to 400 words depending on length; a short one is proportionally shorter. The lead
carries no bullet lists and no headings; it is continuous prose, moving from the general to
the specific.

### Isolation test

Lift the lead out, show it to a reader who will see nothing else, and the essential point must
survive. If it does not, revise the lead before touching anything else. This is the single
highest-leverage edit available on any draft: the lead is the most-read hundred words of the
document, and for a scanning reader it may be the only hundred.

The lead is a front-loaded summary in the encyclopedic sense — a definition and its stakes —
not a narrative hook that withholds the point for effect. Open with the news, then develop it.

> **Before:** "Storage decisions in distributed systems involve many trade-offs. This article
> explores the considerations that arise when data must survive tampering, and later sections
> explain the design that was ultimately chosen."
>
> **After:** "A write-once ledger is an append-only store whose records cannot be altered
> after commit. It exists so an auditor can trust a system's history without trusting its
> operator: every entry is evidence, not testimony."

The first opening promises a point; the second delivers one. Nothing in the "after" version
requires the reader to continue — which is exactly why they will.

## Paragraph and sentence rhythm

One idea per paragraph. When the idea changes, the paragraph ends.

Vary paragraph length deliberately. A one-sentence paragraph that states a definition is
correct and often the strongest way to open a section:

> **Capitalisation rate:** net operating income divided by market value.

Then expand. Most paragraphs run three to seven lines. A paragraph that pushes past that is
usually carrying two ideas — split it. Do not lengthen sentences to reduce the paragraph
count; prefer more short paragraphs to fewer dense ones. The paragraph's first sentence
carries its point, because the scanning reader samples first sentences and skips the rest —
a paragraph that buries its point in line four has hidden it from most of its audience.

### Sentence length and variation

Sentences average roughly fifteen to twenty words — the range plain-language research has
converged on for sustained comprehension. A sentence that states a fact of record — a
definition, a compliance claim, a regulatory statement — targets twenty-five words or fewer,
because a claim a reader must rely on should be short enough to hold in one breath. Treat
twenty-five as a target, not a gate: a claim that needs twenty-eight words to be true takes
twenty-eight, but every word past the target earns its place or goes.

Vary the rhythm. Give every paragraph at least one short declarative sentence, so the prose
reads as an accordion rather than a monotone. Avoid chaining more than two clauses with *and*,
*or*, or *but*; a sentence with several commas is usually two sentences. One idea per
sentence, one topic per paragraph — the same discipline at two scales.

> **Before:** "It should be noted that the utilization of encryption keys is handled
> centrally, and various security benefits are thereby achieved."
>
> **After:** "The gateway holds every encryption key. One custodian means one audit trail: a
> reviewer checks a single log, not a fleet."

## Headings and scannability

Headings are navigation, not decoration. They let a reader find the section they need without
reading the ones they do not, and for the scanning reader they *are* the first read — a
skeleton the eye walks before the prose earns any attention.

### Density band

Aim for a heading roughly every 90 to 150 words of body, with about 120 to 140 as the sweet
spot — denser than a report, closer to an encyclopedia. A 600-word article carries four to
seven headings. Treat anything above about 200 words per heading as too sparse: the section
has become a wall the reader cannot navigate. Sections run one to four paragraphs; a section
longer than that wants a subheading. Do not over-section either: a heading above a single
short paragraph adds clutter, not navigation. (Band calibrated 2026-07-01 against mature
articles that read well at ~120–140 words per heading; the earlier 75–100 target flagged
good prose as thin.)

### Writing the heading itself

Write headings in sentence case, with the most important word first, so a reader scanning the
left margin lands on the keyword. "Rollback procedure" beats "How to roll back the change."
Make each heading descriptive and unique within the document — a heading is a promise, and the
section beneath it keeps exactly that promise, nothing more. Keep sibling headings parallel in
grammar: if one section is "Rollback procedure," its sibling is "Cutover procedure," not
"Performing the cutover." A heading that could sit above any section ("Overview,"
"Considerations") is furniture; replace it with the section's actual subject.

The document title comes from frontmatter; the body never carries a top-level `#` heading.

## Capitalization

Casing is authored into the artifact, never left to rendering. The wiki engine prints a title
and a heading exactly as written — it applies no title-case or sentence-case transform, and no
automatic transform could, because it cannot know that `WORM`, `BIM`, `seL4`, `os-console`, or
`service-email` carry canonical casing a title-caser would corrupt. The author owns the casing.

### Sentence case, keyword first

One rule for every title and every heading: **sentence case, keyword first.** Capitalize the
first word and nothing after it except proper nouns, acronyms, and code identifiers, which
keep their canonical form. "Debt service and financing structure," not "Debt Service and
Financing Structure." "WORM ingest," not "Worm ingest." "seL4 capability topology," never
"Sel4 Capability Topology." The slug stays lowercase-kebab regardless
(`debt-service-and-financing-structure`). This applies to the frontmatter `title:` and to
every `##` / `###` heading, in every artifact type — the engine passes both through verbatim,
so consistency has to live in the source.

### No leading article

**Keyword first means no leading article.** No `title:`, no heading, and no slug begins with
*the*, *a*, or *an* — drop it, so the first word a reader scans and the first character the
wiki files on is the meaningful one. Write `title: "Citation substrate"` /
`slug: citation-substrate`, never `title: "The citation substrate"` or
`slug: the-citation-substrate`. A category page sorts its list by slug and *displays* the
title, so a column of entries all opening with *The* is unscannable, and on any title-sorted
surface it mis-files every one under T. The article returns naturally in body prose ("The
citation substrate records every claim…"); only the title and the slug — the display's first
word and the index key — shed it. The Spanish pair follows: no title opens with
*el/la/los/las/un/una*. The one exception is a proper name whose article is genuinely part of
the name; even then the slug drops the article (`ledger`, not `the-ledger`) so the filing key
stays clean.

### File names and slugs

**File names are cased differently — lowercase, always.** The file name is not display text;
it is an identifier, and it is the slug. Use lowercase ASCII, kebab-case: words joined by
single hyphens, no spaces, no underscores, no capitals —
`debt-service-and-financing-structure.md`, never `Debt-Service.md` or `debt_service.md`. The
filename stem equals the `slug:` field exactly. A bilingual pair adds `.es.md`
(`debt-service-and-financing-structure.es.md`). Once published a slug is immortal — rename
through an alias, never by re-casing the file. So three casings, one per layer:
**lowercase-kebab for the file/slug, sentence case for the title, sentence case for the
headings.**

## Voice and tone

Write in the active voice by default. Active voice names the actor and the consequence: "the
gateway holds every key" tells the reader who is responsible; "keys are held centrally" hides
it. Use the passive only when the actor is genuinely irrelevant or the object is the true
subject of the sentence.

Name actors and consequences. Every claim of fact says who does what, and what follows if
they do not. Abstract nouns and agentless constructions are where precision goes to hide.
State claims affirmatively: say what a system does, not what it does not fail to prevent —
a sentence built on stacked negatives makes the reader do algebra to find the meaning.

### Concrete words and named numbers

Prefer the everyday word to its formal synonym — *use* over *utilize*, *end* over *terminate*,
*explain* over *elucidate* — and prefer the named number to the vague quantifier: "seven
services" beats "several services"; "within four hours" beats "promptly." The tone is neutral
and exact: do not editorialize, do not flatter, and do not reach for the promotional register
of a product page. Where an intensifier tempts, the stronger move is always the specific fact
it was standing in for — the reader trusts "restores in under a minute" in a way no adverb can
buy. The advisory linter surfaces candidates; the discipline lives here.

### Analogy as ceiling

Analogy is a ceiling, not a quota. One analogy per few hundred words at most; prose with none
is fully compliant. A good analogy earns its place by carrying a mechanism the reader could
not otherwise hold; an analogy in every paragraph is a tell that the mechanism was never
explained plainly. Explain first, illustrate second, and let the explanation stand alone.

## Lists and tables

Prose is the default; a list or table is a deliberate upgrade for material that is genuinely
parallel or comparative. Three or more items doing the same grammatical job read better as a
bulleted list than as a comma chain. Values compared across two or more dimensions — options
against criteria, tiers against limits — belong in a table, where the reader's eye can do in
one pass what a paragraph forces into working memory. Keep list items grammatically parallel
and front-load each with its keyword, exactly as headings are. And keep the boundary: the lead
is always continuous prose, and a document that is mostly bullets has stopped explaining and
started inventorying.

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
*intended*, *may*, or *target*, with a reasonable basis the writing can point to and, where
the context is regulated, the cautionary framing the disclosure posture requires. The
discipline reads as honesty, not hedging: "the ledger anchors daily" is a present fact;
"anchoring is planned to extend to hourly in 2027" is a forward claim wearing its status
visibly. Never give a system human intent or feeling.

## Cross-references and linking

Link the reader to the definition rather than repeating it. When a term has its own article or
section, reference it once and move on; do not re-explain the mechanism a linked article
already carries. This keeps each document to a single job and lets the web of references do
the work of building understanding. A document that re-explains everything it touches is doing
four documents' jobs badly.

### Link once, at first mention

Wikilink every term of art at its **first mention** — the point where a reader first needs the
definition — and never re-link later mentions in the same document. A very long article may
repeat one link at the first occurrence inside a major section readers are likely to enter
directly; that is the only exception. Overlinking has a ceiling for a reason: a paragraph
where every third phrase is a link becomes a sea of blue in which the reader can no longer
tell which links matter, and an over-linked page is as hard to use as an unlinked one. Link
terms of art and entities with their own articles; leave everyday words unlinked. Every
committed link resolves — a dead link in published prose is a defect, not a placeholder.

## Outside voice

Before anything reaches a public wiki, the internal machinery comes off. The reader meets the
idea in institutional prose — never the workspace's paths, governance vocabulary, or
operational plumbing. Strip, and re-express in plain terms: internal file paths and repository
names; governance citations of the form "DOCTRINE §N," "conventions/…," "CLAUDE §N," or
"Doctrine claim #N" (state the rule itself instead); systemd unit paths; SSH ports and
localhost endpoints; and personal names, which become role nouns.

> **Before:** "Per DOCTRINE §14 and conventions/worm-ledger.md, the ledger runs as a systemd
> unit on localhost:9202; Jennifer reviews entries per Doctrine claim #31."
>
> **After:** "The ledger runs as a supervised service. An editor reviews every entry before
> publication — a control the platform treats as non-negotiable."

The rule the citation pointed at survives; the citation apparatus does not. If a claim cannot
stand without its internal reference, the claim is not yet written.

## Draft-improves-the-draft loop

No single pass has to be perfect. The standard for any given sweep is "draft two of ten" —
good enough that the next pass, human or machine, produces a clearly better draft three.
Perfection in one pass wastes effort better spent establishing the frame that makes every
later pass better.

Revise at one altitude per pass, from the top down: structure first (does the lead survive the
isolation test; does every heading keep its promise), then paragraphs (one idea each, points
in first sentences), then sentences (length, voice, the concrete word). A sentence polished
inside a paragraph about to be cut is effort spent twice. Reading a passage aloud remains the
cheapest test of rhythm ever devised — the ear catches the monotone the eye forgives. Each
edit against this standard is also a training example: the machine that drafts the next
version learns from the one the editor accepted.

## How the specific guides use this document

Each register guide (reference, how-to, communications, legal, journal) and each house profile
(documentation, corporate, projects) opens by pointing here, then specifies only its
differences: the section skeleton for its artifact type, its register and audience, its code
policy, and two or three worked examples in its own voice. Everything above is assumed. When a
specific guide and this document appear to conflict, the specific guide governs for its own
artifact type — but it should rarely need to, because the craft is shared.
