---
schema: foundry-doc-v1
title: "What a design token is"
slug: what-is-a-design-token
short_description: "Entry-level background article defining design tokens, the W3C Design Tokens Community Group Format Module (first stable version, October 2025), and the primitive/semantic/component three-tier architecture, grounded in the PointSav Design System's published 146-token DTCG bundle."
category: design-system
type: topic
content_type: topic
quality: complete
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-08-01
editor: pointsav-engineering
paired_with: what-is-a-design-token.es.md
cites: []
---

A design token is a design decision recorded as data: a name, a value, and —
in a mature system — a type and a description explaining when to use it. The
decision "our primary interactive color is this specific blue" becomes an
entry in a JSON file rather than a hex code repeated across stylesheets.
Everything downstream — CSS, component libraries, documentation sites, native
platforms — consumes the entry by name, so the decision is made once and
referenced everywhere.

The PointSav Design System publishes its tokens as a single machine-readable
bundle, `tokens.full.json`, containing 146 leaf tokens across two top-level
groups: a primitive layer of 82 tokens and a themed semantic layer of 64 (37
light-theme roles plus 27 dark-mode entries). Every count, name, and value in
this article comes from that published file, not from an idealized example.
(Correction, 2026-08-02: this is stale — every count has moved. Real
`primitive` = 100 leaves (includes 18 `orgchart.*` tokens this article never
mentions), real `theme.semantic` = 53, real `theme.dark` = 28, plus an
unmentioned `theme.accessibility` group (5). Two entire top-level pillars,
`paper` (167 leaves) and `writing` (32 leaves), were folded into the same
export file and aren't mentioned anywhere in this article. Git history shows
146 was accurate three weeks before this article's own `last_edited` date and
has moved twice since. The specific hex value and color-family count cited
elsewhere in this article are independently confirmed accurate. Flagged, not
resolved.)

## A decision with a name

The simplest way to see what a token buys is to compare the two ways of
writing the same button. Without tokens, a stylesheet says
`background: #234ed8` — a value with no history and no meaning. If the brand
color changes, every occurrence must be found and edited, and nothing
distinguishes the occurrences that meant "primary action" from ones that
happened to use the same blue for an unrelated reason.

With tokens, the stylesheet references a name, and the name carries the
intent. In the published PointSav bundle, `#234ed8` exists in exactly one
place: the primitive token `primitive.color.primary-60`. A semantic token,
`theme.semantic.interactive-primary`, points at it by alias —
`{color.primary-60}` — and buttons consume the semantic name. Change the
primitive once and every surface that means "primary interactive" follows;
surfaces that meant something else are untouched because they reference a
different name.

Tokens also carry documentation in place. The bundle's duration token
`speed-2` is not just `120ms`; its description field reads "Quick — button
press, focus ring fade." The spacing token `space-3` records "8px @ 16px base
— paragraph rhythm floor." The usage rule travels with the data, where a
build tool, a linter, or an AI agent reading the file at generation time can
see it — not in a style guide that drifts separately.

## One format across tools: the DTCG Format Module

For most of the last decade every token tool used its own file shape. That
ended when the Design Tokens Community Group, a W3C community group,
published the first stable version of its Format Module — version 2025.10 —
announced on October 28, 2025. The specification defines a vendor-neutral
JSON format: tokens declare `$value`, `$type`, and `$description`; groups
nest; aliases use curly-brace references such as `{color.primary-60}`; and
the stable version added support for modern color spaces and for theming and
multi-brand inheritance. Design tools and token pipelines on both the design
and engineering side support the format, which is what makes a token file a
portable interchange artifact rather than a private convention.

The PointSav bundle is written to this specification and declares it
explicitly: both top-level groups carry
`"$schema": "https://schemas.designtokens.org/2025-10-01/draft.json"`. The
bundle uses the specification's core mechanisms — typed groups, description
fields, and curly-brace aliasing — and does not yet use the newer `$extends`
group-inheritance feature; that is an evaluation still to be done, noted in
this article's open questions rather than glossed over.

## Three tiers: primitive, semantic, component

The architecture the field has converged on — and the one this design system
teaches on its foundations page — arranges tokens in three tiers, each
answering a different question.

**Primitive tokens answer "what values exist?"** They are the raw palette:
options, not decisions about use. The documentation site's teaching example
is `ps-blue-600: #234ed8` — a blue with a scale position and no opinion about
where it appears. In the published bundle this tier is the `primitive` group:
36 colors in role-named families (`primary`, `neutral`, `positive`,
`caution`, `critical`, each on a numeric 10–100 scale, plus black and white),
a 13-step spacing scale, 14 typography styles, 6 durations, 4 easing curves,
5 border dimensions, 3 viewport breakpoints, and a focus-ring composite — 82
tokens in all.

**Semantic tokens answer "what does this value mean here?"** They alias a
primitive and attach a role. The teaching example is
`cds-interactive: {ps-blue-600}` — "anything a person can act on." The
bundle's counterpart is `theme.semantic.interactive-primary:
{color.primary-60}`, one of 37 semantic roles covering surfaces (`surface-base`,
`surface-elevated`), text ("ink" in this system's vocabulary: `ink-primary`,
`ink-secondary`), borders, focus, interactive states with their hover and
pressed variants, and status support colors. The semantic tier is where a
theme lives: a tenant re-points the aliases at its own primitives without
touching any component. The companion article on theming covers this
mechanism in detail.

**Component tokens answer "what does this specific part use?"** The teaching
example is `btn-primary-bg: {cds-interactive}` — this button, this surface,
nothing else. Scoping one more name to one component costs a line and buys
precision: if primary buttons alone ever need to diverge, one alias is
re-pointed and nothing else moves. One honest caveat, stated plainly: the
exported bundle currently ships the primitive and semantic tiers; the
component tier exists as the documented naming convention consumed by
component recipes, not as a third group inside `tokens.full.json`. The chain
`ps-blue-600 → cds-interactive → btn-primary-bg` is how the site teaches the
architecture; the first two links are load-bearing in the published data
today, and formalizing the third in the export is an open decision.

The direction of reference is the discipline that keeps the graph coherent:
components point at semantics, semantics point at primitives, and nothing
points the other way. A component never reaches past the semantic tier to
grab `primary-60` directly, because doing so re-embeds the raw value the
token system exists to centralize.

## Why this structure earns its place

The three-tier structure is not PointSav's invention, and this design system
does not claim otherwise — numeric primitive scales, semantic aliasing, and
component scoping are the shared vocabulary of the modern design-system
field, formalized by the DTCG specification's aliasing model. What the
structure buys any adopter is the same: decisions made once; intent readable
in the name; themes expressed as substitution rather than duplication; and a
file that tools and agents can consume without a human interpreting a style
guide. The design system's separate primitive-vocabulary article documents
which structural patterns were kept from the field and which names and
values are PointSav-original, so practitioners arriving from other systems
know what will feel familiar and why.

## Licensing: the data and this article are licensed differently

Two artifacts are in play here, under two different licenses, and precision
about which is which matters. The token data itself — the DTCG JSON bundle in
the `pointsav-design-system` repository — is published under Apache-2.0,
following the convention of open-source design systems. This article's text,
like the rest of the documentation wiki it belongs to, is licensed CC BY 4.0.
Neither license extends to the other artifact: reusing the token file is an
Apache-2.0 question; reusing or adapting this explanation is a CC BY 4.0
question.

## Scope and limits

Stated plainly: the token counts and values cited here describe the
published PointSav bundle as of this writing and were recomputed from the
file during drafting; they will drift as the bundle evolves, and the file —
not this article — is authoritative. The component tier is a documented
convention rather than a shipped group in the export. And the bundle
exercises the DTCG 2025.10 core rather than the specification's full feature
set. Each of these is a status, not a defect, and this design system prefers
to publish statuses visibly.

---

*This article is entry-level background for readers new to design tokens,
ahead of the design system's reference material. For why the primitive
vocabulary looks the way it does, see the primitive-vocabulary rationale
article; for how themes work, see "Theming via semantic tokens."*
