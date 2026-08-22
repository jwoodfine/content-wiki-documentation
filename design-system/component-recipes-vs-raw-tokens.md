---
schema: foundry-doc-v1
title: "Component recipes vs. raw tokens"
slug: component-recipes-vs-raw-tokens
short_description: "What the PointSav Design System's component tier adds beyond a token value: the recipe.json format — variants, markup, token references, CSS, ARIA guidance, and WCAG targets in one machine-readable artifact — demonstrated against the shipped Button recipe and the registry's real documentation state (53 components: 20 fully documented, 33 with a recipe plus at least a usage document)."
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
paired_with: component-recipes-vs-raw-tokens.es.md
cites: []
---

A design token answers one question: what is the value? `interactive-primary`
is a color, `space-5` is a length, `speed-2` is a duration. Tokens are the
smallest unit of design decision the system versions, and everything above
them resolves by reference. But a working interface element is not a bag of
values. A button is markup, a set of state styles, a focus behavior, an
accessibility contract, and a handful of usage rules about when each
variant is appropriate — and none of that lives in a token.

The PointSav Design System's answer to that gap is the component recipe: a
single machine-readable JSON artifact per component that composes token
references into a working element. This article explains what the recipe
tier adds beyond raw token values, using the shipped Button recipe as the
worked example, and describes the registry's actual documentation state
rather than an idealized one.

## What a raw token gives you — and where it stops

A token in the system's DTCG-format bundle carries a value, a type, and a
description that records the decision's rationale. That is enough for the
problems tokens solve: one source of truth per value, theme-level
substitution, and drift-free reuse. It is not enough to build with. A
developer holding `interactive-primary` still has to decide what element to
render, which states to style, how hover and pressed relate to the base
color, what the focus ring does, and what the disabled state looks like.
Every consumer who makes those decisions independently reintroduces exactly
the divergence tokens were meant to remove — one tier up.

## The recipe format

The Button recipe demonstrates the shape. It is a JSON document declaring a
schema, an identity (`name`, `display_name`, a one-sentence description, a
category, a registry type), and then the substance:

**Variants as named decisions.** Each variant — primary, secondary, ghost,
critical — carries its own description, its HTML template, its CSS class,
and the list of tokens it consumes. The descriptions are usage rules, not
captions: primary is "the most prominent action on a surface. One per
surface"; critical is "destructive action. Always paired with a
confirmation step." The rule ships inside the data, where a code generator
or a reviewing agent reads it, rather than only in prose a human may not
open.

**Markup with slots.** Each variant's `html` field is a template — a native
`<button type="button">` with a `{{label}}` slot — so consumers inherit the
correct element and structure rather than reconstructing it.

**Token references, not values.** A variant's `tokens` array lists semantic
references: `{semantic.interactive-primary}`,
`{semantic.interactive-primary-hover}`, `{semantic.ink-on-interactive}`.
The recipe never hardcodes a color. In the CSS these resolve as custom
properties with fallbacks (`var(--ps-interactive-primary, #234ed8)`), so
the component re-themes when the token graph re-themes.

**The complete CSS.** The recipe carries the full base-plus-variant rules,
including the states a value-only view omits: hover, active, disabled, and
`:focus-visible` with a 2-pixel ring and 2-pixel offset.

**The accessibility contract.** An `aria` field states screen-reader
guidance in prose — native button role, `aria-label` for icon-only use, and
the rule that destructive actions must not be one click from completion. A
structured `wcag` block declares the target (2.2 AA, AAA where
achievable), focus visibility, the real per-variant contrast figures — 6.66:1
for the primary variant, which passes AA but not the 7:1 AAA floor, and
7.33:1 for the critical variant, which clears both — and the 44-by-44
minimum touch target.

**Provenance links.** `research_links` points at the design-rationale
documents behind the component, and `registry_dependencies` declares what
other registry entries the component needs — for Button, none.

The distinction from a raw token is now concrete: the token tier says what
`interactive-primary` is; the recipe tier says what a button *is* — and
everything it says resolves back to tokens by reference, so the two tiers
cannot disagree about a value.

## Two documentation tiers, one registry

The registry currently holds 53 components, and they are not uniformly
documented. Twenty carry the full five-file set — the recipe plus four
human-facing documents covering usage, style, code, and accessibility.
The rest are not bare data, either: 30 carry the recipe plus a usage
document, and 3 carry the recipe plus a bilingual usage pair — every
component in the registry ships at least one prose document alongside its
recipe, not just the machine-readable artifact. The components reference
presents this as three labeled tiers rather than pretending 53 uniformly
finished entries.

The tiered state is a fact about sequencing, and the recipe's role in it
is the point: the recipe is the floor. Every component is already
machine-consumable at minimum — its markup, tokens, CSS, and WCAG block
exist — while the remaining style and code documentation is owed for
33 of the 53. The inverse (prose documentation with no data artifact) is
not a state the registry permits.

## Prior art: the component tier is well established

Naming a component tier above semantic tokens is standard practice across
the major published design systems, and this article makes no novelty claim
for it. Google's Material Design 3 documents three token classes —
reference, system, and component — where a component token such as
`md.comp.fab.container.color` resolves to a system token such as
`md.sys.color.primary-container`. IBM's Carbon documents the equivalent
global/alias/component structure and scopes component tokens to their own
component. The pattern is the shared inheritance of hyperscaler design
systems, not a PointSav idea.

What the recipe format does with that established tier is pack more of the
component's contract into the one data artifact: where a component token is
still a value assignment, a recipe additionally carries the markup, the
complete CSS, the ARIA guidance, and the WCAG targets. That is an
integration choice — one artifact instead of several — and its merit is
practical, not conceptual: a consumer, human or machine, gets the whole
buildable component from a single fetch.

## Licensing: two artifacts, two licenses

Precision is required here because the recipe and this article are licensed
differently. The recipe data — button/recipe.json and every other recipe
and DTCG token file in the `pointsav-design-system` repository — is
licensed Apache-2.0, the same convention IBM Carbon and Adobe Spectrum use
for their design-system code and data. The text of this article is
published in the documentation wiki under CC BY 4.0. Copying a recipe into
your own registry is an Apache-2.0 matter; republishing this article's
prose is a CC BY 4.0 matter. A sentence about "the license" of the design
system must say which of the two it means; this one has.

## Scope and honest limits

The worked example is one component, and the registry census is a snapshot
dated to this article's writing — the tier split will change as
components gain their remaining documentation sets. An earlier draft of
this article flagged a description/variants-array mismatch in the shipped
Button recipe (the description once named a fifth "link" variant not
present in the `variants` array); that mismatch has since been corrected
at the source, which now describes four variants and explains the prior
miscount — no open inconsistency remains. The recipe
schema is versioned (`component-recipe-v1`), and nothing in this article
should be read as a compatibility promise for future schema versions.

---

*This article is background for readers of the PointSav Design System
documentation, ahead of the per-component reference pages. See also: the
primitive vocabulary article for the token naming scheme recipes resolve
against, and the wiki component library article for how a set of these
components composes a complete page.*
