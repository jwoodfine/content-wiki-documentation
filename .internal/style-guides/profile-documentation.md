---
schema: foundry-doc-v1
title: "Documentation wiki profile"
slug: profile-documentation
category: internal
type: reference
content_type: reference
quality: complete
status: active
audience: contributor-internal
bcsc_class: internal-only
governs: [documentation-wiki-TOPIC, documentation-wiki-GUIDE, documentation-wiki-ARCHITECTURE]
last_edited: 2026-07-01
editor: pointsav-engineering
---

> House profile for the documentation wiki (`documentation.pointsav.com`). Layers on
> [[guide-reference]] for TOPIC and ARCHITECTURE work and on [[guide-how-to]] for GUIDE work.
> Restates neither, nor [[house-core]]; it adds only what is specific to this wiki's audience.
> The register facts come from [[editorial-language-registers]]. Where this profile is silent,
> the register guide it names governs.

## 1. Purpose and audience

The primary reader is a software engineer or platform developer who can read code and wants to
understand how the platform works, deploy it, or contribute to it. The register is
developer-platform: peer-level, confident, engineer to engineer. Field jargon (gRPC, systemd,
async, JSON) is used freely; platform-specific terms are defined once in plain language, then
used.

A second reader looks over their shoulder — an institutional reader (a technology committee, an
incoming principal, a senior developer from a top-400 firm) evaluating whether the platform is
credible enough to fund or approve. This reader is technically literate but does not know the
platform's internal vocabulary. Serving both readers at once is the whole job of this profile.

## 2. The shape

Inherit the reference shape for TOPIC and ARCHITECTURE and the operational shape for GUIDE. The
one addition is the per-section internal order this wiki uses inside a body section:

**Concept → Why it matters → How it works → Code → Edge cases.**

The "Why it matters" line is the delta — see §6.

### Bilingual pair — adaptation, not translation

The Spanish pair (`.es.md`) is a strategic adaptation, not a sentence-for-sentence rendering.
It serves the same two readers in their own language, so examples, emphasis, and even the H2
order may reorganise where the Spanish-language reader enters the subject differently. What
survives unchanged is every factual claim, each section's "why it matters" sentence, and the
forward-looking posture. Adapt the structure; never the facts.

## 3. Opening

Inherits the reference lead (TOPIC/ARCHITECTURE) or the Purpose-then-Prerequisites lead (GUIDE).
No wiki-specific change.

## 4. Paragraph and sentence rhythm

Inherits the reference guide. No delta.

## 5. Headings and scannability

Inherits the reference guide's density. The one wiki-specific check: a non-engineer scanning the
left margin of headings and "why it matters" sentences must be able to reconstruct what the
subject does and why it is credible, without reading a line of code.

## 6. Voice and tone — the corporate accessibility layer

Each body section carries one **"why it matters" sentence**: consequence-first, no jargon,
standing entirely alone. It is the sentence the institutional reader keeps when they skip the
mechanism and the code. Write it so it survives being lifted out of its section.

> **service-slm** routes every AI request to the cheapest compute tier that meets the deadline,
> without the caller naming a tier. A request that resolves locally never leaves the customer's
> infrastructure — and never appears on a cloud billing statement.

The last sentence is the accessibility layer: the non-engineer gets "it can run locally, and you
pay nothing when it does" without touching the mechanism.

Linking carries the same first-mention discipline as the definition. Wikilink every term of art
at its first mention and only there ([[house-core]] §Cross-references governs); on this wiki
the first mention is also where the plain-language definition lands, so one sentence hands the
engineer the link and the institutional reader the meaning.

## 7. Code and examples — code as reference, not tutorial

Code is allowed and belongs here — but as *reference*, not as a copy-run procedure. A TOPIC or
ARTICLE shows the short, illustrative fragment (a signature, a schema shape, a one-line
invariant) that clarifies the mechanism, introduced by a sentence that says what it shows.
Abbreviate long blocks with `# ...`. A runnable, step-by-step sequence belongs in a GUIDE
(governed by [[guide-how-to]]); the TOPIC links to it rather than pasting it. Tutorial dumps —
long blocks a reader is expected to execute in order — are a defect in a TOPIC.

## 8. Worked examples

**Missing accessibility layer → added.**

> Weaker: The Doorman selects a tier per request based on a deadline budget and circuit state.
> Stronger: The Doorman selects a tier per request based on deadline and circuit state. Local
> inference stays on the customer's own hardware and costs nothing when it resolves there.

*The second version adds the standalone consequence a non-engineer keeps.*

**Tutorial dump in a TOPIC → fragment plus a link.**

> Weaker: (forty lines of shell setting up the fleet controller, pasted into the article)
> Stronger: The controller exposes `GET /v1/vms` for fleet state. To bring a controller up, see
> the deployment guide; this article covers what the endpoint returns and why.

*Reference keeps the illustrative surface; the runnable steps move to the GUIDE.*

## 9. Pre-publish checklist

- Does every body section carry one jargon-free "why it matters" sentence that survives in
  isolation?
- Can a non-engineer reconstruct the subject from headings and those sentences alone?
- Is inline code an illustrative fragment, not a runnable procedure a GUIDE should own?
- Are platform-internal terms defined in plain language on first use?
- Is every term of art wikilinked at its first mention — and only there?
- Is the voice peer-level — no over-explaining HTTP, SSH, or git to an engineer?
- Does the Spanish pair adapt for its reader while preserving every factual claim and each
  "why it matters" sentence?
