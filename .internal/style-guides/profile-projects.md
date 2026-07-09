---
schema: foundry-doc-v1
title: "Projects wiki profile"
slug: profile-projects
category: internal
type: reference
content_type: reference
quality: complete
status: active
audience: contributor
bcsc_class: public-disclosure-safe
governs: [projects-wiki-TOPIC]
last_edited: 2026-07-01
editor: pointsav-engineering
---

> House profile for the projects wiki (`projects.woodfinegroup.com`). Layers on
> [[guide-reference]] — every article here is a TOPIC. Restates neither it nor [[house-core]];
> it adds only what is specific to this wiki's reader and subject. The register is the same
> institutional financial-press register as the corporate wiki (see [[profile-corporate]] and
> [[editorial-language-registers]]); this profile records only where the subject and audience
> differ. Where it is silent, the reference guide governs.

## 1. Purpose and audience

The register is identical to the corporate wiki — institutional financial-press, consequence-first,
prose-only, 14–18 word sentences under a 25-word ceiling. The audience is dual. The first reader
is a development-industry practitioner: a top-400 development firm, a commercial architect, a
construction programme manager. The second is the same institutional investor who reads the
corporate wiki, now reading project subject matter.

What changes from the corporate wiki is not the reader's frame — it is the subject. Here the
material is commercial real estate and development: co-location methodology, regional site
markets, GIS site scoring, BIM methodology, and architectural styles in an evaluation context. A
family-office principal reading direct-hold structures and then reading co-location sites is the
same person applying the same evaluative frame to different subject matter.

## 2. The shape

Inherits the reference TOPIC shape. Continuous prose, no code, no command tables — the same
constraints as [[profile-corporate]] §2.

### Bilingual pair — adaptation, not translation

The Spanish pair (`.es.md`) is a strategic adaptation, not a sentence-for-sentence rendering.
Market examples, emphasis, and even the H2 order may reorganise for the Spanish-speaking
practitioner or allocator — a reader whose reference markets may differ. What survives unchanged
is every figure, every scoring claim, and the forward-looking posture.

## 3. Opening

Inherits the corporate consequence-first lead. The delta is only the reader's second hat: the
lead must land for both a capital allocator *and* a development practitioner, without dropping to
a register that reads as promotional to either.

## 4. Paragraph and sentence rhythm

Inherits the financial-press rhythm from [[profile-corporate]] §4 — 14–18 word target, 25-word
limit, specific numbers. No delta.

## 5. Headings and scannability

Inherits the reference guide's density. Prose punctuated by named markets and figures, not
records.

## 6. Voice and tone — link every term of art

The register is corporate's; the subject brings its own vocabulary. Every industry term of art —
floor plate, BOMA measurement, cap rate, gateway city, anchor taxonomy — links on its first
mention, and only there, to its definition (a glossary or reference article; [[house-core]]
§Cross-references governs the once-only discipline). The investor reader who does not carry the
development lexicon is never stranded, and the practitioner reader is never slowed by a page of
repeated blue. The move is the same consequence-first factual clause as corporate:

> Each co-location development site is underwritten as an independent capital event. Site
> performance is not pooled; convergence at a node is validated before capital is committed.

## 7. Code and examples — prose only, specialist sites carry the specs

No code. Where an article touches deep specification — climate-zone token schemas, IFC mappings,
co-location scoring criteria, zoning rules — it states the *consequence* in institutional prose
and routes the specification itself to the specialist site by full URL: BIM detail to
`bim.woodfinegroup.com`, GIS scoring to `gis.woodfinegroup.com`. The projects TOPIC stays readable
by a general institutional audience; the specialist site is where a practitioner goes to build or
verify.

## 8. Worked examples

**Undefined term of art → linked on first use.**

> Weaker: Sites are ranked by ADI against the regional floor-plate distribution.
> Stronger: Sites are ranked by [[anchor-density-index|anchor density]] against the regional
> [[floor-plate|floor-plate]] distribution.

*The investor reader reaches the definition in one click; the practitioner reads straight
through.*

**Specification pasted into the article → consequence plus a routed link.**

> Weaker: (a table of IFC entity mappings and climate-zone token identifiers)
> Stronger: Each site inherits its climate-zone assumptions from the regional token set. For the
> full token specifications and IFC mappings, see `bim.woodfinegroup.com`.

*The consequence stays in the TOPIC; the specification lives at the specialist destination.*

## 9. Pre-publish checklist

- Does the lead land for both a capital allocator and a development practitioner?
- Is the article prose-only, within the 25-word sentence limit, with specific numbers?
- Does every industry term of art link to its definition at first mention — and only there?
- Is deep BIM/GIS specification routed to the specialist site rather than pasted in?
- Does every forward-looking claim carry planned/intended/may/target?
- Does the Spanish pair adapt markets and structure for its reader while keeping every figure
  and scoring claim unchanged?
