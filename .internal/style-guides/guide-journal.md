---
schema: foundry-doc-v1
title: "Journal guide — academic complete-idea papers"
slug: guide-journal
category: internal
type: reference
content_type: reference
quality: complete
status: active
audience: contributor
bcsc_class: public-disclosure-safe
governs: [JOURNAL]
last_edited: 2026-07-14
editor: pointsav-engineering
---

> The register guide for JOURNAL artifacts — academic papers written to real-journal standard.
> Builds on [[house-core]] and adds only the academic specialization. Structure and schema —
> the mandatory section apparatus, the `foundry-journal-v1` frontmatter, author rules, the
> forbidden-vocabulary list, promotion criteria, and public-posting blocks — are governed by
> [[journal-artifact-discipline]] and are not restated here. This guide teaches the craft:
> how a complete idea is argued from abstract to conclusion.

## 1. Purpose and audience

A JOURNAL is a complete idea. One thesis enters at the abstract's first sentence, is
developed, tested, and stress-tested through every section, and is answered in the
conclusion. This is what makes it a distinct kind, not a long article. A lookup-TOPIC is a
reference fragment: the reader arrives with a question, reads one section, and leaves — no
section depends on having read another, and there is no arc. A procedure-GUIDE is a task: the
reader executes steps and verifies each one — the discipline is per-step, not cumulative. A
JOURNAL's sections are not independently consumable and are not meant to be; each one exists
to advance a single claim, and the paper succeeds only if the whole argument holds.

The primary reader is a peer reviewer — a professional skeptic who reads to find where the
argument breaks: the unsupported claim, the hypothesis that cannot fail, the result that
outruns its evidence. Write every sentence as if that reader will test it, because one will.
A second audience reads over the reviewer's shoulder: the public reader of the self-published
working paper, who meets the same text on a preprint surface before any venue accepts it.
Both are served by the same discipline — an argument built to survive review is also the
honest public record.

## 2. The shape

The section apparatus — abstract through data-availability statement — is fixed by
[[journal-artifact-discipline]]; consult it before drafting and defer to it on every
structural question. What that convention does not teach, and this section does, is the
intellectual shape that must run through the apparatus: one thesis, threaded.

### Abstract as microcosm

The abstract is a scale model of the paper: every sentence in it is a promissory note that
exactly one part of the paper redeems. The capability-geometry paper is the worked exemplar.
Its abstract opens with the gap as a falsifiable statement about the world ("no production
deployment in 2026 makes capability state visible to a transparency log and consultable by
the kernel…"); the introduction and related-work sections redeem that sentence by surveying
the field until the gap is undeniable. The second sentence names the composition of three
primitives; the architecture section redeems it. The two-bottom sentence is redeemed by the
compatibility section, the ownership-ceremony sentence by the ledger section, the
evaluation sentence — named crates, test counts — by the implementation section. The final
sentence carries the quantified result (11.2 ns against 4.01 ms, a 358,000× ratio), and the
discussion redeems it by arguing what the ratio makes structurally load-bearing.

Draft the abstract first as an outline of obligations, and audit it last: any abstract
sentence no section redeems is a broken promise; any major section no abstract sentence
covers is smuggled cargo. Word count, sentence order, and the falsifiable-claim-first rule
are set by [[journal-artifact-discipline]] §Abstract.

### Thesis threading

Each section opens by advancing the single claim — a sentence that says what this section
does *to the thesis*, not what topics it contains. The exemplar's related-work sections model
the move: "This section examines three categories of existing trustworthy operating system
designs and explains why each fails to close the gap identified in §1.1." Every survey
paragraph re-touches the gap; nothing is background for its own sake. A section that could
be deleted without weakening the argument is not yet part of the paper.

### Conclusion answers the abstract

The conclusion is not a restatement of contributions — the introduction already listed them.
It answers the claim the abstract opened. The exemplar's abstract asserts that no system
makes a deployment an inheritable, auditable cryptographic object; its conclusion answers in
kind: the proofs are mathematics, they transfer, and the deployment becomes a single
inheritable artifact. Read the abstract's first sentence, then the conclusion's last
paragraph: the second must resolve the first, the way a chord resolves.

### Discussion and limitations stress-test the thesis

Discussion and Limitations are where the authors attack their own claim before a reviewer
does — they sharpen the thesis, never dilute it. The exemplar's limitations section names
each soft spot with its consequence and its remedy: benchmark variance on one measurement
(±11% confidence interval, 22 outliers) is declared, tied to the affected claim, and gated on
a re-run; the pre-production runtime layer is declared and its claims re-classified as
forward-looking. A limitation stated precisely converts a reviewer's objection into evidence
of rigor; a limitation omitted converts it into a rejection.

### Plain narrative, technical apparatus appended

A JOURNAL argues its thesis in narrative prose any informed reader — not only a specialist
peer reviewer — can follow start to finish. Operator benchmark (2026-07-14): a
Bessembinder-style finance working paper states its claim, method, and result in plain
sentences a generalist reader follows without special training, while the actual
mathematical derivation (the wealth-creation formula, its assumptions, the double-counting
caveat) lives in a single labeled Appendix the main text cites but never interrupts itself
with. This is not a relaxation of rigor — the appendix carries the same falsifiable
precision this guide requires elsewhere — it is a relocation: derivations, proofs, extended
formula manipulation, and dense statistical apparatus belong in an Appendix; the body stays
narrative.

**The test:** could a competent generalist reader — the institutional finance audience this
platform's own wikis are written for (see [[house-core]]) — read the body start to finish
and state the thesis, the method, and the result, without needing to parse an equation
inline? If a paragraph requires stopping to work through notation to continue reading the
argument, that paragraph's derivation belongs in an Appendix, referenced from the body by a
single sentence ("see Appendix A for the derivation"), not embedded in it. Length discipline
follows from the same test: rigor is carried by precision and appendiced evidence, not by
main-body length — a paper that can make its case in fewer narrative pages should.

**Applies retroactively.** Existing JOURNAL papers written before this was made explicit
should be reviewed against this test as part of their own publish-blocker resolution
(`.agent/rules/journal-registry.md` tracks per-paper status) — not rewritten wholesale, but
audited for passages where technical apparatus crowds out the narrative and could move to an
appendix without losing anything the main argument needs.

## 3. Opening

The abstract is this register's lead, and the isolation test is exact: a program-committee
member who reads nothing else must be able to state the claim, the method, and the quantified
result — and decide whether to read on. Sentence one carries the falsifiable claim; method
follows; the result appears as a number, not an adjective. Nothing in the abstract may be
forward-looking without wearing its hedge.

The introduction has a different job: make the reader feel the gap before naming the
contributions. The exemplar walks the existing design space system by system — each a
factual, citable subject — until the structural consequence states itself: every path roots
trust somewhere the customer is not. Only after the reader can articulate the missing thing
does the paper say "this paper makes three contributions" and enumerate them. An introduction
that leads with its contributions is asking for credit before establishing the debt; a reader
who has felt the gap receives the contribution list as the obvious next sentence rather than
as a claim to be resisted.

Close the introduction with a one-paragraph structure map ("§2 reviews…, §3 specifies…, §8
concludes") — the academic equivalent of the scanning reader's heading skeleton.

## 4. Paragraph and sentence rhythm

Two house rules are explicitly suspended for a JOURNAL body, so that future wiki-register
sweeps do not wrongly flag it: the heading-density band (a heading every 90–150 words) does
not bind — academic section lengths govern, and a methods subsection may legitimately run
several hundred words under one heading; and the wikilink discipline does not bind — a
JOURNAL body carries no wikilinks at all (see §7). Everything else in [[house-core]] holds.

Within those longer sections, paragraph discipline tightens rather than relaxes. One idea per
paragraph, and the topic sentence carries the paragraph's contribution to the argument —
reviewers triage papers by sampling topic sentences exactly as scanning readers sample
first lines. An academic paragraph may run eight to ten lines when it is developing a single
mechanism, but the moment the idea changes, the paragraph ends.

Claims of record — a measured number, a formal property, a hypothesis — stay short enough to
hold in one breath and to quote in a review. Explanatory prose keeps the house average.
Definitional precision beats elegance everywhere: a reviewer forgives a plain sentence and
never forgives an ambiguous one.

## 5. Headings and scannability

Sections are numbered (§1, §2.1, §2.2), because the paper cross-references itself constantly
— "the gap identified in §1.1," "the ceremony in §4.4" — and numbered anchors are how a
reviewer navigates and how the falsification programme points at its test subjects. Heading
names follow the venue's conventions for a submission and the discipline's section list for
the self-published form; within that frame, headings stay sentence case and keyword first as
the house sets, and each heading is a promise its section keeps.

Tables carry measurements; prose carries meaning. Every results table is numbered, captioned,
and names its harness, hardware, sample count, and run date, so the number can be reproduced
or challenged. Numbered algorithm listings do the same for procedures. The prose around a
table states what the numbers mean for the thesis — the exemplar does not stop at "cache hits
measure 11.2 ns"; it argues that the ratio makes the cache structurally load-bearing rather
than optional. A table the surrounding prose never interprets is data, not argument.

## 6. Voice and tone

Measured first person, active, owned: "This paper presents…," "We describe…." The authors
claim their claims. Neutrality here is not the absence of a position — the paper has exactly
one position, its thesis — but the absence of anything the evidence has not paid for.

### Hypothesis phrased so it could fail

The formal hypothesis is this register's verification discipline — the equivalent of the
how-to's "name the check and its expected value." H₁ states what the system does, under what
conditions, in terms an independent party could test; H₀ states the world in which the claim
is false; and the falsification conditions are enumerated so a skeptic knows exactly what
observation would kill the claim. The exemplar's transferability hypothesis models the form:
H₁ names the actor (a customer holding only an apex key and a 32-byte anchor), the action
(full reconstitution of a deployment), and the conditions (any hardware booting the
compatibility kernel, no vendor involvement); it is then falsified if any recovery step
requires a vendor-controlled resource, if the reconstituted deployment diverges, or if an
independent audit needs vendor infrastructure. A hypothesis that no observation could refute
is marketing wearing a subscript.

### Hedging runs in both directions

A capability not yet delivered wears *planned*, *intended*, *may*, or *target* — and a result
already delivered wears nothing. Under-hedging a roadmap item is a disclosure violation;
over-hedging a measured result is a factual error that surrenders the paper's own evidence.
The rule and its regulatory basis live in [[journal-artifact-discipline]]; the craft is the
audit: for every claim, ask "has this happened?" — if yes, state it as fact with its number;
if no, hedge it and name the basis.

### Structural gaps, never foils

The gap that motivates the paper is stated structurally — as a property of the design space —
never as a ranking against a named product. A real system may appear as a factual technical
subject, cited, when the paper genuinely analyses it; it never appears as a prestige
comparison, a dismissal, or a benchmark of quality. "Per-tenant trust roots are incompatible
with multi-tenant billing economics" forecloses a whole architectural class and lets the
reader draw the ranking; "vendor X's inferior product" invites the reviewer to referee a
fight the paper did not need to pick.

## 7. Code and examples

Code appears as evidence, not tutorial. A struct shape, a wire format, a trait signature —
the minimum fragment that makes a mechanism checkable, introduced by a sentence saying what
it shows. Multi-step procedures become numbered algorithm listings. Nothing in a JOURNAL is
meant to be copy-pasted and run; a reader who needs the runnable form is directed to the data
availability statement, not to an embedded script.

### Formal citations, never wikilinks

Every load-bearing claim that rests on prior work carries a formal citation, written as a
stable bracket ID — `[rfc-9162]`, `[c2sp-signed-note]` — resolved against the `cites:` list
in the `foundry-journal-v1` frontmatter and expanded in the references section in the
venue's format. The bracket ID is the source convention because it is portable across render
forms: a PDF pipeline can number it, a wiki render can link it, and plain Markdown leaves it
legible — the citation survives every surface without rewriting. A wikilink survives none of
them outside the wiki, which is why a JOURNAL body carries no `[[wikilink]]` anywhere. When a
paper needs to cite one of the platform's own wiki articles, it does so as a formal reference
with a full URL in the references section, exactly as it would cite any external web source.
Placeholder citations (`[external: url]`) are drafting scaffolding; promotion to a stable ID
is a pre-submission gate, not an option. The exact in-text syntax, the forbidden forms, and
the resolution invariant the render engine enforces are pinned in §9.

### Two surfaces, one artifact

A JOURNAL lives on two surfaces, and different rules bind on each.

- **Wiki / self-published render** — public from the moment it posts. The public-posting
  notice blocks (working-paper notice and forward-looking-statements advisory, per
  [[journal-artifact-discipline]] §Public posting) survive into every render — the engine
  generates them from frontmatter; the author never writes them into the body (§9); the internal
  and forbidden vocabulary is fully scrubbed; the complete apparatus — hypotheses,
  falsification programme, disclosures, data availability — shows. The paper is presented
  exactly as the honest working draft it is.
- **External venue submission** (optional) — the venue's rules take over: double-blind
  anonymization (the vocabulary scrub doubles as the anonymization pass), the venue's
  citation and layout format, its word and reference-count budgets. The notice blocks come
  off because the venue supplies its own review framing.

What binds on both: the falsifiable-hypothesis discipline, bidirectional hedging, formal
citations, and the structural-gap rule. What differs is dress, never argument.

### One source, many render forms

One Markdown source renders as an academic two-column layout, a PDF, and a wiki-category
article. The invariant across every form: the apparatus sections, the formal citations, the
notice blocks on public surfaces, and the scrubbed vocabulary all survive rendering intact.
Building those render targets is engine work owned by the knowledge-platform project
(project-knowledge); an author's obligation ends at a source file whose citations, blocks,
and structure are render-form-agnostic — which the bracket-ID and fixed-apparatus disciplines
above guarantee.

## 8. Worked examples

All three pairs are mined from the capability-geometry paper's subject matter; the systems
named are the paper's own cited technical subjects.

### Over-claimed result, correctly-hedged result — in both directions

> *Over-claimed:* The substrate runs in production on verified AArch64 hardware, giving
> deployed customers formally verified capability enforcement today.
>
> *Over-hedged:* A checkpoint cache is planned that may reduce verification cost
> substantially once implemented.
>
> *Correct:* The substrate is implemented and benchmarked — 95 passing tests; cache hits
> measure 11.2 ns against 4.01 ms for full Ed25519 verification. The AArch64 production
> deployment path is planned; present benchmark hardware is x86_64.

Annotation: hedging is bidirectional. The first version asserts a future as a fact — a
disclosure violation. The second states a measured, shipping result as if it were roadmap —
surrendering the paper's own evidence. The third states each delivered fact with its number
and hedges exactly the claims that have not happened yet.

### Competitor-named foil, structural gap statement

> *Foil:* Unlike the leading commercial zero-trust products, which lag far behind, this
> architecture is the first serious attempt at customer-controlled trust.
>
> *Structural:* Hyperscaler attestation architectures root trust in the vendor's keys, and
> per-tenant ledger roots are incompatible with the multi-tenant billing model that underpins
> their economics. The gap is structural: business-sovereign cryptographic root has no
> precedent at any scale.

Annotation: the foil ranks by name and asks the reviewer to referee a product fight; the
structural statement names the mechanism that forecloses the alternative and lets the gap
argue for the contribution. Named systems appear only as cited technical subjects under
analysis, never as prestige comparisons.

### Wiki register, academic register — the same mechanism

> *Wiki (TOPIC):* The apex handover is a [[worm-ledger]] event. When ownership transfers,
> both the old and the new operator sign the same checkpoint, and the kernel stops accepting
> the old signature afterward. See [[capability-substrate]] for how capabilities are
> anchored.
>
> *Academic (JOURNAL):* Ownership transfer is realised as a co-signed checkpoint: at ledger
> height N+2 the departing and incoming apex keys both sign the same signed-note body
> [c2sp-signed-note], and the kernel refuses checkpoints carrying only the departing
> signature at heights N+3 and above. The post-handover invariant is verified end-to-end by
> an integration test exercising all four ceremony heights.

Annotation: the TOPIC defines, links onward, and stops — a reference fragment doing lookup
work. The JOURNAL states the claim precisely, cites the format it depends on with a bracket
ID, and points at the evidence that could falsify it. Same mechanism, two registers; the
boundary is arc and evidence, not subject matter.

## 9. Wiki render contract

Everything above is craft; this section is contract. A JOURNAL renders as a **landing page**
on the `/research/` namespace — a generated masthead, the abstract, the generated references,
the notice banners, and read/download links — with the full ~22-section body as a **separate
full-text rendition** one click away. It is never interleaved into the ordinary `/wiki/{slug}`
article route. The documentation wiki and the gis `/research` surface share the source file,
`~/Foundry/citations.yaml`, the canonical notice text, this contract, and a golden-fixture
suite — but each has its own renderer. The rules below are what an author must do so the same
source renders deterministically, and identically in the parts that matter, on every surface.

### The six habits

1. Mint `slug:` + `category: research` in the first commit (the stub, not the publish pass).
2. Write the abstract in frontmatter (`abstract: |`), never as a body section.
3. Cite by registry ID from the first draft (`[id]`, one per bracket; add the registry entry
   in the same commit — never park an author-year bracket "to fix later").
4. Never write a References section, a title h1, or a notice blockquote — the engine owns all
   three.
5. Keep every non-citation bracket inside code formatting.
6. Bump `version:` in frontmatter, never in the filename. One file per paper, forever.

### Citation convention — one system, engine-resolved

Exactly one citation mechanism: the registry-resolved bracket ID, resolved against
`~/Foundry/citations.yaml`. Any second convention in one paper produces silent corruption.

| Form | Syntax | Example |
|---|---|---|
| Single | `[citation-id]` | `[rfc-9162]` |
| Multiple | Adjacent brackets, one ID each, no space | `[rfc-9162][c2sp-signed-note]` |
| Pinpoint | ID, space, locator, same bracket | `[ni-51-102 §4A.2]` |

Forbidden in a publishable body: author-year brackets (`[Rose et al. 2020]`); narrative
author-year ("Lipp et al. [2019]…"); a hand-typed `## References` section; `[[wikilinks]]`;
`[CITATION NEEDED]` / `[external: url]` scaffolding; bare URLs in prose; trailing changelog
footers.

The resolution invariant, checked at the publish gate:

```
in-text IDs  ⊆  frontmatter cites:  ⊆  citations.yaml keys
```

Bracket hygiene: in a JOURNAL body, a square-bracket token in prose **is** a citation. Code
brackets (`[u8; 32]`, `[Peer]`) sit inside backticks or fences, where the renderer does not
look; a prose bracket that is not a resolvable ID is a gate failure. A registry entry lands
in the same commit as the prose that first cites it — `citations.yaml` is workspace-root
scope, so from an archive the entry routes via Command.

### Mandatory frontmatter — the render fields

| Field | Requirement | Rule |
|---|---|---|
| `schema` | REQUIRED | `foundry-journal-v1` |
| `title` | REQUIRED | Masthead; no body h1 |
| `slug` | REQUIRED | Kebab, keyword-first; no `journal-`/version/state residue |
| `category` | REQUIRED | Literally `research` |
| `abstract` | REQUIRED | `abstract: \|`, 150–250 words; replaces the body `## Abstract` |
| `state` | REQUIRED | `draft\|under-review\|accepted\|published\|archived`; drives banners |
| `version` | REQUIRED | SemVer; feeds the working-paper banner |
| `authors` | REQUIRED | Existing schema; feeds the masthead |
| `license` | REQUIRED to publish | `CC BY 4.0`; feeds the banner |
| `cite_as` | REQUIRED to publish | Must agree with `version` + `preprint_posted_date` |
| `preprint_posted_date` | REQUIRED to publish | Banner date |
| `cites` | REQUIRED | Exactly the in-text ID set |
| `forbidden_terms_cleared` | REQUIRED `true` to publish | Vocabulary gate |
| `keywords`, `subject_codes` | REQUIRED | Landing apparatus summary |
| `paper_class` | OPTIONAL | `standard` (default) \| `geospatial` |

The abstract moves to frontmatter and the body `## Abstract` is removed — one source, two
renditions, zero drift. A body `## Abstract` at publish is a gate failure.

### Filename and slug — version-free, stable

Version lives in `version:`; lifecycle in `state:`; neither ever appears in the filename or
the slug. `slug:` is the permanent public name, keyword-first kebab (`customer-rooted-mesh`).
Working file: `JOURNAL-<slug>.md` — no `vN`, no `.draft`/`.stub` suffix. Content repo:
`research/<slug>.md`. One file per paper, forever.

### Notice blocks — generated, never authored

The working-paper notice and the forward-looking-statements advisory are engine-generated
banners, built from frontmatter fields plus the shared canonical notice text. The body
contains neither; a notice blockquote in the body is a gate failure. The author's whole
obligation is the fields: `state`, `version`, `preprint_posted_date`, `license`, `cite_as`,
`corresponding_author` — populated and mutually consistent.

### Headings and the TOC

The TOC is built from h2/h3 only.

- No body h1 — title, authors, and correspondence are the generated masthead.
- Nothing before the first `##` — no abstract section, no notices, no epigraphs.
- Numbered argument sections, exact style `## 1. Introduction`, `### 2.1 …`.
- Unnumbered back matter after the body, **exact heading strings, exact order**:
  `## AI Use Disclosure`, `## CRediT Contributor Roles`, `## Conflict of Interest`,
  `## Funding`, `## Data Availability`. These strings are load-bearing — the landing page
  derives its apparatus summary by detecting them, and a paraphrase silently drops that item.
- Appendices after Data Availability as `## Appendix A: …`.

### Geospatial papers

Map- and figure-heavy papers declare `paper_class: geospatial`. The static-PNG baseline is
mandatory: every map figure is a committed export at `figures/<id>.png`; an interactive map
embed is a gis-surface-only enhancement, never the only form. Every figure carries a numbered
caption and a data-source line — dataset and build provenance plus basemap attribution (a
licensing requirement, not a courtesy). SYS-ADR-07 applies: figures depict structured data
computed by the deterministic pipeline, never a generative-model rendering of geography.

### Publish gate — what the author can check

- [ ] The YAML frontmatter parses (malformed YAML renders silently blank).
- [ ] `slug:` present, kebab, no version/state/`journal-` residue.
- [ ] `category: research`; `abstract:` present at 150–250 words; no body `## Abstract`.
- [ ] Citations clean: no author-year, no wikilinks, no placeholders, no bare URLs, no
      hand-typed References, no changelog footer; every prose bracket resolves; code
      brackets fenced.
- [ ] The resolution invariant holds; no unused `cites:` IDs; new registry entries carry
      authors, year, venue, and DOI where available.
- [ ] Notice fields present and mutually consistent; no hand-authored notice blockquotes.
- [ ] Heading contract: no h1, nothing before the first `##`, numbered sections, back-matter
      headings verbatim and in order.
- [ ] `forbidden_terms_cleared: true`.
- [ ] If `paper_class: geospatial`: every figure has a stable `#fig-*` ID, a numbered
      caption, a data-source line, and a committed `figures/<id>.png`.

The full contract — renderer conformance, golden fixtures, the per-surface gate, and the gis
`/research` surface — lives in `SPEC-journal-wiki-render-contract.md` (project-knowledge).
Structure and schema remain governed by [[journal-artifact-discipline]].

## 10. Pre-publish checklist

- Does every abstract sentence resolve to exactly one part of the paper, and does every
  major section redeem an abstract sentence?
- Is the abstract's first sentence a claim that could fail — and does the conclusion answer
  it, rather than restating the contribution list?
- Does the introduction make the gap felt, system by system, before the contributions are
  named?
- Does each section open with a sentence that advances the thesis, and would deleting any
  section weaken the argument?
- Are H₁ and H₀ both stated, with falsification conditions enumerated so an independent
  skeptic knows what observation would kill the claim?
- Is every delivered result stated as fact with its number, and every undelivered capability
  hedged with *planned*, *intended*, *may*, or *target*?
- Does every load-bearing claim carry a formal bracket-ID citation resolved against the
  `cites:` list, with zero wikilinks and zero placeholder citations in the body?
- Do Limitations name each soft spot with its consequence and remedy, and is the gap stated
  structurally with named systems appearing only as cited subjects?
- For the public surface: do the notice blocks, the vocabulary scrub, and the full apparatus
  all pass the checks in [[journal-artifact-discipline]]?
- Does the paper pass the §9 render-contract gate — frontmatter render fields, the citation
  resolution invariant, the heading contract, and nothing hand-authored that the engine
  generates?
