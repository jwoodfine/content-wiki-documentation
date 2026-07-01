---
schema: foundry-doc-v1
title: "Legal guide — plain-language legal and governance prose"
slug: guide-legal
category: internal
type: reference
content_type: reference
quality: complete
status: active
audience: contributor-internal
bcsc_class: internal-only
governs: [LEGAL-MANIFEST, LEGAL-DISCLAIMER, LEGAL-CORRECTIONS, contract, CLA, terms, policy, license-explainer]
last_edited: 2026-07-01
editor: pointsav-engineering
---

> The register guide for legal and governance prose. Builds on [[house-core]]; adds only the
> legal specialization. The register's insight: precision and plain language are not opposites.
> Modern legal drafting reaches precision *through* clarity — short sentences, active voice,
> a defined term used identically every time — not through archaic density. Teach the reader
> what they may and must do, not how a clause sounds authoritative.

## 1. Purpose and audience

A legal artifact tells a specific party what they must do, may do, or must not do, and what
follows if they fail. The primary reader is the party bound by the text: a contributor signing a
grant, a user accepting terms, an organization stating a limitation. That reader is usually not a
lawyer, and the license-explainer reader never is. A second reader — counsel, a regulator, a
future editor resolving a dispute — reads over their shoulder and must find the same meaning.

The register inherits the house voice and narrows it: every sentence is an obligation, a
permission, a prohibition, or a definition that supports one of those three. The writer makes the
binding meaning survive both readers without a lawyer present to interpret it.

## 2. The shape

- **Title and scope** — what this document governs and over whom.
- **Definitions** — each defined Term, capitalized, stated once, in a list.
- **Operative clauses** — numbered; one obligation, permission, or prohibition each.
- **Consequences** — what happens on non-compliance, stated explicitly.
- **Limitations and disclaimers** — the boundary of what the text promises.
- **Forward-looking note** (where present) — planned/intended framing with basis.
- **Reference to canonical text** — for a license-explainer, a link to the authoritative file.

## 3. Opening

The lead states what the document governs and whom it binds, in that order, as continuous prose.
The first sentence names the document type and its parties: "These terms govern the reader's use
of the service." The next sentences establish the stakes — the core obligation and the headline
consequence — so a reader who stops after the lead knows what they are agreeing to.

The isolation test: lift the lead out, and the bound party must be able to say who is obligated,
to what, and what happens if they do not comply. A lead that opens with recitals or jurisdiction
before naming the obligation fails the test.

## 4. Paragraph and sentence rhythm

Operative clauses are measured, not dense. Keep one at or under 25 words — a duty a reader must
rely on should hold in one breath. One obligation per sentence; a clause carrying two duties
splits into two numbered clauses. Do not nest *provided that* / *notwithstanding* — a stack of
provisos is a defect, not rigor. State the base rule in one sentence and each exception in its own.

## 5. Headings and scannability

Numbered clauses and definition lists are the native structure of this register; prefer them over
running prose for anything operative. Definitions belong in a list, one Term per entry. Headings
in sentence case, keyword first — "Termination", "Contributor grant", "Limitation of liability".
A short document needs a heading per obligation cluster; a long one needs one per clause group.
Tables suit a rights matrix ("the reader may / the reader must not"); reserve callouts for a
single load-bearing caution, not decoration.

## 6. Voice and tone

Name the party and the action. Write "the Licensee must file within thirty days", never "it is
required that filing occur". Use **must** for an obligation, **may** for a permission, **must not**
for a prohibition — and never mix them for variety. Use a defined Term identically on every
appearance; a synonym reached for elegance ("the agreement" one line, "the arrangement" the next)
is ambiguity a court will exploit. Retire archaic doublets: one word does the work of "null and
void", "cease and desist", "terms and conditions". The move the register turns on is the
consequence-bearing clause: *the obligated party, the action, the deadline, the consequence.*

## 7. Code and examples

No code, with one exception: a license identifier (`CC-BY-4.0`, `Apache-2.0`) or a defined Term on
first definition may appear in monospace to mark it as an exact token. A license-explainer never
reproduces the license text — it links to the canonical file and explains it. The explanation
carries the plain meaning; the canonical file carries the binding words. That is the
reference-versus-how-to line: the explainer points to the authority rather than restating it.

## 8. Worked examples

**Archaic doublets → one plain word each.**
Weaker: "This license shall be null and void, and the Licensee shall forthwith cease and desist
from any and all use whatsoever." Stronger: "The license ends. The Licensee must stop using the
software." *One verb per duty; the doublets and the empty intensifier are gone; the consequence
leads.*

**Passive, agentless obligation → named party and action.**
Weaker: "Attribution must be provided when the work is redistributed." Stronger: "If the reader
redistributes the work, the reader must name the original author and link to this license."
*Names who owes the duty, states the trigger, and gives the concrete action instead of an abstract
noun.*

**License-explainer: legalese reproduced → plain reader-facing terms.**
Weaker: "The Licensor grants a perpetual, irrevocable, non-exclusive, worldwide license to
reproduce, prepare derivative works of, and distribute the Work." Stronger: "The reader may copy
this work, change it, and share it — anywhere, for free, permanently — as long as they credit the
author. They may not remove the author's name. The full terms are in the canonical `CC-BY-4.0`
license file." *Translates the grant into what the reader may and may not do, in their terms, and
links to the authority rather than copying it.*

## 9. Pre-publish checklist

- Does the lead name the parties, the core obligation, and the headline consequence in isolation?
- Is each defined Term capitalized, defined once, and used identically everywhere after?
- Does every operative clause carry exactly one obligation, permission, or prohibition?
- Does each duty name the obligated party and the action, in the active voice?
- Are **must** / **may** / **must not** used for their fixed meanings, with no synonym drift?
- Is the consequence of non-compliance stated explicitly, not implied?
- Does every forward-looking statement carry *planned* / *intended* / *may* / *target* with a
  reasonable basis and cautionary framing — and defer to any regulated context's own requirements?
- Does the license-explainer link to the canonical text rather than reproducing it?
- Do the title and slug lead with the keyword, not a leading article (*the/a/an*)? (see [[house-core]] §Capitalization)
