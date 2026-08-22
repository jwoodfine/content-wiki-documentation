---
schema: foundry-doc-v1
title: "Design tokens and accessibility conformance"
slug: design-tokens-and-accessibility
short_description: "How the PointSav Design System expresses accessibility requirements — minimum touch targets, focus-ring color, contrast relationships — as named design tokens, so that WCAG conformance is enforced by the token graph's structure rather than checked ad hoc per component, demonstrated against the shipped Button accessibility specification."
category: design-system
type: topic
content_type: topic
quality: complete
index_group: token-concepts-and-tooling
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-08-01
editor: pointsav-engineering
paired_with: design-tokens-and-accessibility.es.md
cites: []
---

Most accessibility work is retroactive: build the interface, then audit it.
A checker crawls the page, flags a focus ring that vanished or a touch
target that shrank, and someone traces the defect back through the CSS to
whichever component introduced it. The audit finds the failure after it
ships, one page at a time, and finds it again the next time the same
mistake is made somewhere else.

The PointSav Design System takes the position that the values accessibility
conformance depends on — a minimum touch target, a focus-ring color, the
contrast relationship between two colors — are design tokens like any
other, and belong in the same versioned token graph as color, spacing, and
type. When the requirement is a token, every component that references the
token satisfies the requirement structurally. The audit question changes
from "does every button on every page happen to be big enough?" to "does
the button recipe reference the target-size token?" — a question with one
answer, checked in one place.

## Accessibility values are tokens

The focus ring anchors the pattern. `focus.ring` is a primitive token —
not a bare color, but a composite bundling the ring's color
(`{color.primary-60}`), width, style, and 2px offset — so a theme change
to the primary color propagates to every focus ring at once. Target size
is not a standalone token in the same way; it is met arithmetically at the
component tier — the button below shows exactly how.

The external requirements these tokens encode are worth stating precisely,
because the levels differ. WCAG 2.2, published as a W3C Recommendation in
October 2023, added SC 2.5.8 Target Size (Minimum) at Level AA — 24 by 24
CSS pixels, with exceptions for spacing and inline targets. The
pre-existing SC 2.5.5 at Level AAA requires 44 by 44 with no spacing
exception. This design system tokenizes the stricter AAA value. Focus
indicators are governed by two criteria working together: SC 2.4.7 Focus
Visible (Level AA) requires that a visible indicator exist, and SC 1.4.11
Non-text Contrast (Level AA) requires that the indicator — like any visual
information identifying a component's state — hold at least 3:1 contrast
against adjacent colors.

## The tier chain carries the requirement

The system's tokens resolve in three tiers — primitive, semantic,
component — and the focus-ring requirement travels down the chain the
same way a brand color does:

```
focus.ring (primitive: color {color.primary-60}, width, style, 2px offset)
  → every component recipe that needs a focus indicator references it directly
```

A component's focus ring is a reference to `{focus.ring}`, not a second
copy of the color and width values that could drift when the primitive
changes. If the ring color ever changes, the change is made once, at the
primitive, and every component consuming it follows — the same
maintenance property that motivates tokens for color, applied to a
conformance value instead.

## Contrast pairs are computed from the graph

Because color tokens are data, the contrast relationships between them are
computable rather than assertable. The system's color reference publishes
the pairs that matter most — a foreground token against a background
token — with ratios computed directly from the token hex values using the
WCAG relative-luminance formula: `ink-primary` on the default surface at
14.7:1 (AAA), `ink-secondary` on the default surface at 8.9:1 (AAA), and
button text (`ink-on-interactive`) on the primary interactive background at
7.4:1 (AAA).

Not every pair clears the same bar — the Button component below shows a
real example where a specific variant lands at AA rather than AAA, and the
component's own accessibility spec states that plainly rather than
rounding up. A registry that computes conformance from its own data
surfaces exactly this kind of gap instead of asserting a uniform standard
across every color pairing.

## A component inherits its conformance

The Button component's shipped accessibility specification shows what the
token approach produces at the component tier, including the parts that
don't clear the strictest bar. Its conformance target is WCAG 2.2 AA, AAA
where achievable — not a blanket AAA claim — and the spec is explicit
about which variant lands where: the primary variant's text contrast is
6.66:1, which passes AA (SC 1.4.3) but falls short of the 7:1 AAA floor
(SC 1.4.6); the critical variant clears both at 7.33:1. The focus ring
holds the 3:1 minimum of SC 1.4.11 at every variant. Target size is met by
arithmetic — the button renders at 40 pixels of height, and the focus ring
plus offset add 2 pixels per side, bringing the activatable area to the 44
pixels SC 2.5.5 requires.

The same specification shows requirements that are behavioral rather than
numeric being carried by tokens where a token can carry them: the CSS
transition-duration value resolves to zero when `prefers-reduced-motion:
reduce` matches, so consumers get reduced-motion support without writing
any code. And it records the rules no token can enforce — no state
communicated by color alone, native `<button>` elements rather than
`role="button"` on a `<div>`, no focus ring ever removed without a
replacement — as named anti-patterns in the specification, adjacent to the
token references rather than in a separate document that drifts.

The specification's own closing line is the right note of candor: a
per-component WCAG audit endpoint is future work, and until it exists, the
written specification is the canonical conformance statement.

## What structural enforcement does not replace

Stated plainly. The conformance claims above are self-declared by the
design system's maintainers against the cited criteria; no third-party
accessibility audit of the system has been performed. Tokens enforce the
values a criterion depends on, not the criterion itself — a component can
reference `{focus.ring}` and still fail keyboard users through broken
markup, and no token expresses the judgment-dependent criteria around
content, labels, and context. Assistive-technology testing with real
screen readers remains manual. The structural claim is narrower and, for
that reason, defensible: values that used to be re-decided per component
are now decided once, in data, where checking them is cheap.

## Prior art and licensing

The three-tier token architecture this pattern rides on is well
established, not a PointSav invention: IBM's Carbon documents global,
alias, and component token tiers, and Google's Material Design 3 documents
reference, system, and component token classes. Both systems publish
accessibility guidance alongside their tokens. What this article describes
is the application of that shared tier structure to conformance values
specifically — target size and focus color as first-class tokens with the
WCAG criterion recorded in the token's own description field.

On licensing, precision matters because two different licenses are in
play. The token data itself — `focus.ring`, the DTCG
token files and component recipes that reference them — ships in the
`pointsav-design-system` repository under the Apache-2.0 license. The text
of this article is published in the documentation wiki under CC BY 4.0.
Reusing the tokens means complying with Apache-2.0; reusing this article's
prose means complying with CC BY 4.0. Neither license governs the other
artifact.

---

*This article is background for readers of the PointSav Design System
documentation, ahead of the per-component accessibility specifications and
the foundations token reference. See also: the primitive vocabulary
article for the full token naming scheme, and the design philosophy
article for the research-rationale layer that records why each
accessibility decision was made.*
