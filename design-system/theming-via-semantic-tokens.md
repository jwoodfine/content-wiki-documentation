---
schema: foundry-doc-v1
title: "Theming via semantic tokens"
slug: theming-via-semantic-tokens
short_description: "Background article on light/dark theming as semantic-token substitution rather than a parallel stylesheet, grounded in the PointSav bundle's shipped theme.dark group (28 tokens, [data-theme=\\"dark\\"] switch) and situated against the same pattern in Carbon, Material 3, and Radix — an established technique, not a novelty claim."
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
paired_with: theming-via-semantic-tokens.es.md
cites: []
---

Dark mode, in this design system, is not a second stylesheet. It is a
substitution: the same 53 semantic roles that style every light surface —
`surface-base`, `ink-primary`, `border-subtle`, `interactive-primary` — are
re-bound to dark-optimized values when a single attribute,
`data-theme="dark"`, appears on the document's root element. Components never
learn that a theme exists. They reference roles; the theme decides what the
roles resolve to.

This is an established industry technique, not a PointSav invention, and this
article makes no novelty claim for it. What the article does is show the
mechanism concretely in the design system's published token bundle — real
token names, real values, shipped and in use on the documentation wiki — and
situate it against the systems that popularized the pattern.

## The mechanism, as shipped

The published bundle, `tokens.full.json`, carries the entire dark theme as
one group: `theme.dark`, 28 tokens sitting alongside the 53 light-theme roles
in `theme.semantic`. The group's own description field states the switching
mechanism — "Dark mode semantic overrides — applied via `[data-theme='dark']`
on the root element" — and its composition tells the architectural story:

- **Most of the group overrides a semantic role by name.** `surface-base`,
  which resolves to white in the light theme, becomes `#1f2125` (the
  neutral-90 primitive step) in dark. `ink-primary` flips from near-black to
  `#f5f6f8` (neutral-10). `border-subtle`, `focus-ring`,
  `interactive-primary`, the caution/critical/positive support colors — each
  keeps its name and changes its value.
- **A smaller set exists only in dark.** `surface-code` (a near-black code-block
  background darker than the page, to preserve depth), `ink-on-inverse`, and
  several wiki-specific colors — link, missing-link, and syntax-highlighting
  roles — cover cases where dark mode is not a mirror of light but needs its
  own decisions.

Two details in the dark map repay attention. First, hover direction reverses:
in the light theme, `interactive-primary` is the primary-60 blue and its
hover state darkens to primary-70; in dark, the fill is the lighter
primary-50 and hover moves lighter still, to primary-40. A naive "invert the
palette" scheme misses this; a hand-tuned substitution map encodes it.
Second, accessibility is recorded in place: the group declares WCAG 2.2 AA
minimum for all text pairs on the verified surfaces, and individual tokens
carry their measured contrast pairs in their description fields (dark
`ink-primary` against dark `surface-base` is documented at 14.5:1;
recomputation during drafting confirms the cited pairs meet or exceed the AA
floors, with several recorded ratios conservative).

Because only the semantic layer changes, the cost of dark mode does not scale
with the number of components. A component built on semantic tokens acquires
dark support the day it is written, with no per-component dark selectors. The
wiki that serves this article runs exactly this scheme; the separate
[[wiki-dark-mode]] article documents that surface's implementation details — how
the attribute is set, persisted across visits, and applied before first paint
— which this article deliberately does not repeat.

## The alternative this replaces

The pre-token approach to dark mode was a parallel stylesheet: a second CSS
file, or a large `@media (prefers-color-scheme: dark)` block, restating every
rule that mentions a color. The restatement is the defect. Every new
component adds rules in two places; every palette adjustment must be made
twice; and nothing enforces that the two copies describe the same interface.
Drift between light and dark is not a risk in that architecture — it is the
default trajectory.

Token substitution removes the second copy. There is one set of component
styles, written once against semantic names, and one compact map per theme
saying what the names mean there. The theme map is data, so it can be
validated — checked for completeness against the semantic roster, checked for
contrast floors — in a way that a parallel stylesheet cannot.

## The same pattern elsewhere: Carbon, Material 3, Radix

Three widely used systems implement the same idea, which is worth seeing both
as prior art and as confirmation that the pattern is load-bearing at scale.

**IBM Carbon** structures its themes as value-swaps over a fixed role
vocabulary: each theme shares the same variables and roles, and only the
value changes per theme. Carbon's color documentation is explicit that
mode-switching is only possible because color tokens are used everywhere —
hard-coded values simply do not respond when the theme changes. Products
choose a light theme and a dark theme from the same role set.

**Material Design 3** expresses its scheme as color roles — the named slots
components attach to — with the system generating light and dark scheme
values for every role, including from dynamic (wallpaper-derived) source
color on Android. The role layer is what stays stable; the resolved values
per scheme are what change.

**Radix Colors** binds each color scale's CSS variables twice: light scales
to `:root` and a `.light` class, dark scales to a `.dark` class. The variable
names are identical in both, so the same style rule renders correctly under
either class — switching themes is applying a class to a container, the same
gesture as this design system's `data-theme` attribute.

The differences among the four (including PointSav's) are surface-level —
attribute versus class selectors, hand-tuned maps versus generated schemes —
and the invariant is the same everywhere: components consume stable role
names; themes re-bind values; no component is rewritten to gain a theme.

## What this means for tenants

The same substitution mechanism that carries dark mode carries brand theming.
The bundle's `theme` group describes itself as the PointSav brand's
semantic-layer override and notes that customers fork it as their own theme
file, re-pointing the same semantic roles at their own primitive values. Dark
mode and a tenant re-brand are the same operation at different scales: a map
from stable role names to different values. That is the practical argument
for keeping the semantic tier disciplined — every role a component consumes
is a slot a theme can re-bind, and every hard-coded value is a place theming
silently fails.

## Licensing: the data and this article are licensed differently

As with every article in this series that quotes the token bundle: the token
data itself — the DTCG JSON in the `pointsav-design-system` repository,
including the `theme.dark` group described here — is licensed Apache-2.0.
This article's text, as part of the documentation wiki, is licensed CC BY
4.0. The two licenses cover two different artifacts; quoting token names and
values here does not place this text under Apache-2.0, and reusing this
explanation does not license the token file.

## Scope and limits

Stated plainly: the shipped dark map is verified, per its own description
fields, on wiki surfaces — extending the same contrast verification to other
surfaces is open work, not a completed claim. The dark overrides carry
literal hex values annotated with the primitive step they correspond to,
rather than live aliases into the primitive layer; that is a maintenance
consideration (a primitive change does not propagate into the dark map
automatically) recorded as an open question, not hidden. And the comparison
section above describes Carbon, Material 3, and Radix as prior art from
their public documentation; it asserts pattern similarity, not equivalence of
scope or quality between those systems and this one.

---

*This article is background on the theming mechanism of the PointSav Design
System. For what a token is and the three-tier architecture, see
[[what-is-a-design-token|What a design token is]]. For the wiki surface's
dark-mode implementation — toggle, persistence, first-paint handling — see
[[wiki-dark-mode]].*
