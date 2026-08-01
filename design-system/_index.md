---
schema: foundry-doc-v1
title: "Design system"
slug: _index
category: design-system
type: reference
content_type: topic
quality: complete
short_description: "The PointSav design system as a platform component — its foundational vocabulary, design philosophy, brand surface context, and the typographic, colour, spacing, and motion foundations that compose the visual identity carried across every operator surface."
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-07-28
editor: pointsav-engineering
paired_with: _index.es.md
---

The design-system category covers the PointSav design system as a platform component — its foundational vocabulary, design philosophy, brand surface context, and the foundation-layer token families that the operator-facing surfaces inherit. It addresses the design system as a concept within the platform: why it exists, how it is structured, what brand identity it carries, and where the foundational token vocabulary aligns with field convention. Component implementation guides, accessibility specifications, and the working surface live in the design system repository at `design.pointsav.com`; this category supplies the architectural framing.

The design system is itself one of the platform's load-bearing substrates — see [[design-system-substrate]] for the substrate framing — and inherits the same customer-ownership, machine-readability, and editor-agnostic interoperability disciplines that the rest of the platform applies to its data layers. Every surface the design system renders is designed mobile-first; **Inter** is the UI and heading typeface, chosen for screen legibility and the absence of corporate ownership.

## Philosophy and primitive vocabulary

The foundational decisions: why the substrate exists, what it preserved from convention, what it replaced.

- [[design-philosophy]] — Why the substrate exists; three structural inversions of the enterprise-tier pattern; self-hosted, customer-owned, editor-agnostic token publishing.
- [[design-primitive-vocabulary]] — Vocabulary rationale: numeric colour scales, layered semantic aliasing, productive-versus-expressive type split, and numeric spacing scales aligned with 2018 to 2026 field convention.
- [[design-system-substrate]] — The substrate framing: self-hosted design-system engine storing tokens and components in the customer's own git repository; W3C DTCG token format; machine-readable MCP endpoint.

## Foundation tokens

The four foundation-layer token families: colour, typography, spacing, and motion. Full specifications are maintained in `pointsav-design-system` and published on the design system's own site — these are external links, not wiki articles.

- [Colour tokens](https://design.pointsav.com/elements/color/overview) — primitive palette, semantic aliases, and dark-mode pairings in DTCG format.
- [Typography tokens](https://design.pointsav.com/elements/typography/overview) — type scale, font stacks, fluid type variables, and reading rhythm tokens.
- [Spacing tokens](https://design.pointsav.com/elements/spacing/overview) — base unit, geometric scale, component gap tokens, and layout margin tokens.
- [Motion tokens](https://design.pointsav.com/elements/motion/overview) — duration scale, easing curves, and reduced-motion variants.

## Token concepts and tooling

Background articles on what tokens are, how they compose into components, how they theme, and how they reach designers, AI agents, and other organizations.

- [[what-is-a-design-token]] — A design token as a design decision recorded as data; the W3C DTCG Format Module; the primitive/semantic/component tier model.
- [[theming-via-semantic-tokens]] — Light/dark theming as semantic-token substitution, grounded in the published `theme.dark` group and the same pattern in Carbon, Material 3, and Radix.
- [[component-recipes-vs-raw-tokens]] — What the component tier adds beyond a token value: the `recipe.json` format and the registry's two-tier documentation state.
- [[design-tokens-and-accessibility]] — How accessibility requirements — touch targets, focus-ring colour, contrast — are expressed as tokens rather than checked ad hoc.
- [[figma-tokens-studio-integration]] — Bringing the published token export into Figma via the Tokens Studio plugin's read-only URL sync.
- [[mcp-ai-agent-consumable-design-systems]] — Why the design system exposes a machine-readable MCP endpoint and token search API for AI coding agents.
- [[registry-driven-releases]] — The registry-driven architecture that keeps navigation, homepage statistics, and release packaging from drifting apart.
- [[self-hosting-customer-controlled-design-systems]] — The two separate offers: using the published tokens directly, and self-hosting the serving engine for a different organization's own design system.

## Brand surface

How the brand identity is encoded as colour families and typographic stacks across PointSav and Woodfine product surfaces.

- [[brand-family-swatch]] — Brand colour families assigned to retail and institutional anchor categories in the co-location GIS surface; consistent colour-coded identifiers for map visualisation and tabular data.
- [[brand-typography]] — The typographic separation between web interface system fonts and institutional print typography; open-licence serif typefaces reserved for PDF generation and formal disclosures.

## Wiki surface design

The component vocabulary, typographic system, and dark-mode palette that compose the `documentation.pointsav.com` reading surface.

- [[wiki-component-library]] — Nine reusable interface components that compose a complete wiki article page; Wikipedia layout conventions, current accessibility standards, PointSav token system.
- [[wiki-typography-system]] — Inter and Source Serif 4 type stack, heading scale, and spacing tokens for the wiki; broad linguistic coverage for bilingual content.
- [[wiki-dark-mode]] — Light and dark colour schemes for the wiki: WCAG-verified palettes and theme persistence via localStorage.

## Related foundations

The architectural and substrate articles that frame the design system within the wider platform.

- Building design system for BIM — Design-system tooling adapted for BIM and real-property workflows, paired with ISO 19650 record-keeping discipline.
- AEC interface conventions — Interface conventions for AEC surfaces that the design system inherits and extends.
- [[knowledge-wiki-leapfrog-architecture]] — How the wiki engine consumes the design system's tokens and components to render Wikipedia-shaped chrome over flat Markdown.

## See also

- [Substrate](/substrate/) — the design-system substrate framing alongside the other foundational mechanism substrates
- [Patterns](/patterns/) — named design patterns that the design system encodes at the interface layer
- [Applications](/applications/) — operator-facing applications that consume the design system through the token and component layers
