---
schema: foundry-doc-v1
title: "Corporate wiki profile"
slug: profile-corporate
category: internal
type: reference
content_type: reference
quality: complete
status: active
audience: contributor
bcsc_class: public-disclosure-safe
governs: [corporate-wiki-TOPIC]
last_edited: 2026-07-01
editor: pointsav-engineering
---

> House profile for the corporate wiki (`corporate.woodfinegroup.com`). Layers on
> [[guide-reference]] — every article here is a TOPIC. Restates neither it nor [[house-core]];
> it adds only what is specific to this wiki's reader. The register facts come from
> [[editorial-language-registers]] (institutional financial-press register). Where this profile
> is silent, the reference guide governs.

## 1. Purpose and audience

The reader is an institutional decision-maker — a banker, a family-office principal, an
institutional investor, an auditor. They have financial literacy and no obligation to understand
software architecture. They read to make or defend a capital-allocation decision, or to evaluate
the platform's structure and sponsors.

The register is institutional financial-press: neutral, exact, consequence-first. The governing
test for every sentence is one question, stated without naming any firm: *does this serve a
senior finance reader who understands contracts, risk, and regulation but does not read source
code?* If a sentence only lands for an engineer, it fails here.

## 2. The shape

Inherits the reference TOPIC shape — lead, context, mechanism section by section, limits and
relations. No structured-record variants; corporate articles are continuous prose.

### Bilingual pair — adaptation, not translation

The Spanish pair (`.es.md`) is a strategic adaptation for the Spanish-speaking allocator, not a
sentence-for-sentence rendering. Emphasis, examples, and even the H2 order may reorganise where
that reader enters the subject differently. What survives unchanged is every figure, every
disclosure sentence, and the forward-looking posture — the facts and their regulatory framing
are identical in both languages.

## 3. Opening — consequence first

Inherits the reference lead, sharpened to one rule: the most important fact for a capital
allocator goes in sentence one. Not the history, not the mechanism's origin — the consequence
for the reader who must decide. The isolation test is a capital-allocator test: lift the lead
out, and a principal who sees nothing else must know what changes for their capital.

## 4. Paragraph and sentence rhythm

The financial-press delta on the reference guide: consequence and disclosure sentences target
14–18 words and stay under 25 — tighter than the reference default. An analytical sentence that
carries a single multi-condition test — a covenant, a debt-sizing constraint, a rate mechanism —
may run longer when splitting it would fragment one logical unit; prefer the split wherever it
does not fragment the logic. Numbers are always specific: "$7 per month," not "low cost";
"top-400 development markets," not "major markets." (The ≤25 target is a target, not a hard gate —
calibrated 2026-07-01 against strong analytical articles; see the calibration report.)

## 5. Headings and scannability

Inherits the reference guide's density. No tables of commands, no code callouts — the recurring
structure here is prose punctuated by named figures, not records.

## 6. Voice and tone — prose only

No code. Ever. The corporate reader does not need a terminal command, and a code block signals
the wrong register to a capital allocator. Every platform-internal term is translated to a
plain-language equivalent on first use — the plain equivalent precedes the term, never the
reverse — and the term wikilinks at that first mention and only there ([[house-core]]
§Cross-references governs). Passive voice reads as evasion to this reader; name the actor and
the consequence.

The accessibility cue for the finance reader mirrors the documentation wiki's "why it matters"
sentence, inverted: wherever a technical mechanism must appear, its consequence stands alone in
plain financial terms *before* the mechanism is named, so the reader who skips the mechanism
still keeps the fact that moves their decision.

The move this profile turns on is the consequence-first factual clause:

> The Direct-Hold framework removes the pool. Each property is its own legal and financial unit.

## 7. Code and examples

None. This is the code policy: prose only. Where a mechanism is genuinely technical, describe its
*consequence* in institutional terms and link to the documentation wiki for the reader who wants
the mechanism.

## 8. Worked examples

**Mechanism-first → consequence-first.**

> Weaker: The redemption engine processes unit-level exit requests through a per-property ledger.
> Stronger: An investor can exit one property without disturbing the others. Each holding
> redeems on its own ledger.

*The consequence for the allocator leads; the mechanism follows in plain terms.*

**Asserted future as fact → BCSC forward-looking posture.**

> Weaker: The Sovereign Data Foundation audits every holding and holds the governance mandate.
> Stronger: The Sovereign Data Foundation is the intended future audit and governance body;
> the platform plans to place holdings under its mandate.

*Sovereign Data Foundation appears only in planned/intended/may/target terms — never as a
current equity holder, active auditor, or governance body. This is the critical check for this
wiki: the article and the `index.md` lede must both satisfy it. If in doubt, flag and do not
publish.*

## 9. Pre-publish checklist

- Does sentence one carry the consequence for a capital allocator, not the history or mechanism?
- Would a senior finance reader who does not read source code follow every sentence?
- Is the article prose-only, with zero code blocks?
- Is every platform-internal term preceded by a plain-language equivalent on first use, and
  wikilinked at that first mention only?
- Where a mechanism appears, does its plain-financial consequence stand alone before it?
- Are all numbers specific, and are consequence and disclosure sentences within the 25-word
  target (with only genuine single-test analytical sentences running longer)?
- Does every forward-looking claim carry planned/intended/may/target, and is the Sovereign Data
  Foundation referenced only in those terms?
- Does the Spanish pair adapt for its reader while keeping every figure, disclosure sentence,
  and forward-looking frame identical?
