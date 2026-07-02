---
schema: foundry-doc-v1
title: "Legal guide — plain-language legal and governance prose"
slug: guide-legal
category: internal
type: reference
content_type: reference
quality: complete
status: active
audience: contributor
bcsc_class: public-disclosure-safe
governs: [LEGAL-MANIFEST, LEGAL-DISCLAIMER, LEGAL-CORRECTIONS, contract, CLA, terms, policy, license-explainer]
last_edited: 2026-07-01
editor: pointsav-engineering
---

> The register guide for legal and governance prose — manifests, disclaimers, corrections
> notices, contracts, contributor agreements, terms, policies, and license explainers. Builds
> on [[house-core]]; adds only the legal specialization. The register's insight: precision and
> plain language are the same discipline. A clause is precise when a counterparty, a reviewer,
> and a first-time reader all land on one meaning — and short sentences, fixed verbs, and a
> defined term used identically every time are how one meaning is built. Density is not rigor.

## 1. Purpose and audience

A legal artifact tells a specific party what they must do, may do, or must not do, and what
follows if they fail. The primary reader is the party bound by the text: a contributor signing
a grant, a user accepting terms, an organization stating a limitation. That reader is usually
not a lawyer, and the license-explainer reader never is. A second reader — counsel, a
regulator, a future editor resolving a dispute — reads over their shoulder and must find the
same meaning.

The register inherits the house voice and narrows it: every sentence is an obligation, a
permission, a prohibition, or a definition that supports one of those three. The writer's job
is a binding meaning that survives both readers without a lawyer present to interpret it.

## 2. The shape

The common skeleton:

- **Title and scope** — what this document governs and over whom.
- **Definitions** — each defined Term, capitalized, stated once, in a list.
- **Operative clauses** — numbered; one obligation, permission, or prohibition each.
- **Consequences** — what happens on non-compliance, stated explicitly.
- **Limitations and disclaimers** — the boundary of what the text promises.
- **Forward-looking note** (where present) — planned/intended framing with basis.
- **Reference to canonical text** — for an explainer, a link to the authoritative file.

Per-genre deltas:

- **Contract / terms / CLA** — the full skeleton, numbered throughout.
- **Disclaimer** — a scope sentence, then what is promised, then what is not; the boundary
  *is* the content, so it gets stated affirmatively, not implied.
- **Corrections notice** — what was wrong, what is correct, when the correction was made,
  and a link to the corrected text. The notice is dated and permanent; the record shows the
  error was found and fixed, which is what earns the reader's trust in everything uncorrected.
- **License explainer** — the plain-language summary, an explicit note that the summary is
  not the license, and a link to the canonical text.

## 3. Opening

The lead states what the document governs and whom it binds, in that order, as continuous
prose. The first sentence names the document type and its parties: "These terms govern the
reader's use of the service." The next sentences establish the stakes — the core obligation
and the headline consequence — so a reader who stops after the lead knows what they are
agreeing to.

The isolation test: lift the lead out, and the bound party must be able to say who is
obligated, to what, and what happens if they do not comply. A lead that opens with recitals
or jurisdiction before naming the obligation fails the test.

## 4. Paragraph and sentence rhythm

Operative clauses are measured, not dense. Keep one at or under 25 words — a duty a reader
must rely on should hold in one breath. One obligation per sentence; a clause carrying two
duties splits into two numbered clauses.

State the rule first, in its own sentence. Then each exception, in its own sentence, opening
with its trigger: "Unless…", "If the work is redistributed commercially…". A stack of
*provided that* / *notwithstanding* provisos is a defect, not rigor — each proviso silently
amends everything before it, and the reader must re-parse the clause to learn what survived.

When a rule turns on several conditions, tabulate. Introduce the rule, then list the
conditions as (a), (b), (c) in parallel grammar, one condition each. A comma chain of
conditions hides the boundary between them; the list makes each condition separately
checkable — by the bound party before acting, and by the reviewer after.

## 5. Headings and scannability

Numbered clauses and definition lists are the native structure of this register; prefer them
over running prose for anything operative. Headings in sentence case, keyword first —
"Termination", "Contributor grant", "Limitation of liability". A short document needs a
heading per obligation cluster; a long one needs one per clause group.

Definitions belong in a list, one Term per entry — and the list stays short (see §6). In a
long document the list sits where the contract's conventions expect it; in a short one, a
Term may be defined in place at first use, bolded, so the reader never scrolls to decode a
sentence. Tables suit a rights matrix ("the reader may / the reader must not"); reserve
callouts for a single load-bearing caution, not decoration.

## 6. Voice and tone

Name the party and the action. Write "the Licensee must file within 30 days", never "it is
required that filing occur". The move the register turns on is the consequence-bearing
clause: *the obligated party, the action, the deadline, the consequence.*

### One word per meaning, one meaning per word

**Must** states an obligation, **must not** a prohibition, **may** a permission — and no
other word does those jobs. Retire *shall* entirely: in inherited drafting it drifts between
obligation, prediction, and mere formality, and disputes have turned on which sense a single
document meant. A verb with one fixed meaning cannot be argued about. Never rotate synonyms
for variety: a defined Term appears identically on every use, because "the agreement" in one
line and "the arrangement" in the next is ambiguity a court will exploit.

### Defined terms as a discipline

Define a Term only when it is used more than once and its scope is not the everyday meaning;
the strongest definition is the one the rewrite removed. Never define a word against its
ordinary meaning — a "Day" that means something other than a day is a trap, not a term.
Write "*Term* means…", never "shall mean": a definition states meaning and carries no
obligation, because duties live only in operative clauses. Every defined Term is used and
every capitalized Term is defined; an unused definition is a loose wire a later editor trips
over.

### Concrete words, named deadlines

Retire archaic doublets — one word does the work of "null and void", "cease and desist",
"terms and conditions". Name every deadline with a trigger and a number: "within 30 days
after delivery", never "promptly", "forthwith", or "as soon as practicable", each of which
every party reads in its own favor. The named number the house voice prefers is, in this
register, the difference between a duty and a dispute.

## 7. Code and examples

No code, with one exception: a license identifier (`CC-BY-4.0`, `Apache-2.0`) or a defined
Term at first definition may appear in monospace to mark it as an exact token.

A license explainer never reproduces the license text — it links to the canonical file and
explains it, and it says so on its own face: one sentence stating that the summary is not the
license and that the canonical text governs on any difference. The explanation carries the
plain meaning; the canonical file carries the binding words. The same one-source rule governs
a corrections notice: the notice links to the corrected text rather than restating it, so the
record has one authoritative version and one dated account of the change.

## 8. Worked examples

**Archaic doublets → one plain word each.**

> Weaker: "This license shall be null and void, and the Licensee shall forthwith cease and
> desist from any and all use whatsoever."
> Stronger: "The license ends immediately. The Licensee must stop using the software."

*One verb per duty; the doublets, the empty intensifier, and the vague* forthwith *are gone;
the consequence leads and the deadline is concrete.*

**Proviso stack → rule first, exceptions in their own sentences.**

> Weaker: "The Contributor may submit changes, provided that such changes are original,
> provided further that, notwithstanding the foregoing, no submission shall be accepted
> unless accompanied by a signed grant."
> Stronger: "The Contributor may submit original changes. Each submission must include a
> signed grant. The maintainer must reject a submission without one."

*The permission stands alone; each condition and its consequence gets one sentence with one
fixed verb; nothing amends anything silently.*

**License explainer: legalese reproduced → plain terms that disclaim themselves.**

> Weaker: "The Licensor grants a perpetual, irrevocable, non-exclusive, worldwide license to
> reproduce, prepare derivative works of, and distribute the Work."
> Stronger: "The reader may copy this work, change it, and share it — anywhere, for free,
> permanently — as long as they credit the author. They must not remove the author's name.
> This summary is not the license: the canonical `CC-BY-4.0` file governs, and it is linked
> below."

*Translates the grant into what the reader may and must not do, in their terms; states its
own non-authority; and points to the binding text rather than copying it.*

## 9. Pre-publish checklist

- Does the lead name the parties, the core obligation, and the headline consequence in
  isolation?
- Is each defined Term defined once with "means", used identically everywhere after, and is
  no definition unused?
- Does every operative clause carry exactly one obligation, permission, or prohibition, with
  the obligated party named in the active voice?
- Are **must** / **may** / **must not** used for their fixed meanings — no *shall*, no
  synonym drift?
- Is every rule stated before its exceptions, each exception in its own sentence, with no
  proviso stacks?
- Does every deadline carry a trigger and a number rather than a vague adverb?
- Is the consequence of non-compliance stated explicitly, not implied?
- Does a corrections notice state what was wrong, what is correct, and the correction date,
  with a link to the corrected text? Does an explainer state it is not the license and link
  to the canonical file?
- Does every forward-looking statement carry *planned* / *intended* / *may* / *target* with
  a reasonable basis and the framing any regulated context requires — and do the title and
  slug lead with the keyword, not a leading article? (see [[house-core]] §Capitalization)
