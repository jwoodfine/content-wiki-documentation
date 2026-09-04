---
schema: foundry-doc-v1
title: "Design and Brand"
slug: design-system-index
category: design-system
type: reference
content_type: topic
quality: complete
short_description: "The PointSav design system as a platform component — its foundational vocabulary, design philosophy, brand surface context, and the typographic, colour, spacing, and motion foundations that compose the visual identity carried across every operator surface."
index_type: thematic
index_scope: design-system
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-09-04
editor: pointsav-engineering
paired_with: _index.es.md
---

The design-system category covers the PointSav design system as a platform component — its foundational vocabulary, design philosophy, brand surface context, and the foundation-layer token families that the operator-facing surfaces inherit. It addresses the design system as a concept within the platform: why it exists, how it is structured, what brand identity it carries, and where the foundational token vocabulary aligns with field convention. Component implementation guides, accessibility specifications, and the working surface live in the design system repository at `design.pointsav.com`; this category supplies the architectural framing.

The design system is itself one of the platform's load-bearing substrates — see [[design-system-substrate]] for the substrate framing — and inherits the same customer-ownership, machine-readability, and editor-agnostic interoperability disciplines that the rest of the platform applies to its data layers. Every surface the design system renders is designed mobile-first; **Inter** is the UI and heading typeface, chosen for screen legibility and the absence of corporate ownership.

<!-- START-HERE-HIGHLIGHT: engine reads this block to render the single "start here" card
     (reuses the existing cluster-card--start-here component). Do not add more than one. -->

**Start here:** [[design-philosophy]] — why the substrate exists, and the three structural inversions of the enterprise-tier pattern that everything else in this category builds on.

<!-- END-START-HERE-HIGHLIGHT -->

## Philosophy and primitive vocabulary

The foundational decisions: why the substrate exists, what it preserved from convention, what it replaced.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: philosophy-and-primitive-vocabulary -->
- [[design-philosophy]] — The PointSav design system is a self-hosted, customer-owned substrate at design.pointsav.com publishing design decision research alongside DTCG-format token values.
- [[design-primitive-vocabulary]] — Rationale for the primitive token layer's structural patterns — numeric color scales, semantic aliasing, and type splits — using PointSav-specific naming and values.
- [[design-system-substrate]] — The substrate framing: self-hosted design-system engine storing tokens and components in the customer's own git repository; W3C DTCG token format; machine-readable MCP endpoint.
<!-- END AUTO-GENERATED -->

## Token concepts and tooling

Background articles on what tokens are, how they compose into components, how they theme, and how they reach designers, AI agents, and other organizations.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: token-concepts-and-tooling -->
- [[what-is-a-design-token]] — Entry-level background article defining design tokens, the W3C Design Tokens Community Group Format Module (first stable version, October 2025), and the primitive/semantic/component three-tier architecture, grounded in the PointSav Design System's published DTCG bundle (130 primitive + 86 theme tokens, plus separate paper and writing pillars).
- [[theming-via-semantic-tokens]] — Light/dark theming as semantic-token substitution, grounded in the published `theme.dark` group and the same pattern in Carbon, Material 3, and Radix.
- [[component-recipes-vs-raw-tokens]] — What the PointSav Design System's component tier adds beyond a token value: the recipe.json format — variants, markup, token references, CSS, ARIA guidance, and WCAG targets in one machine-readable artifact — demonstrated against the shipped Button recipe and the registry's real documentation state (53 components: 20 fully documented, 33 with a recipe plus at least a usage document).
- [[design-tokens-and-accessibility]] — How the PointSav Design System expresses accessibility requirements — minimum touch targets, focus-ring color, contrast relationships — as named design tokens, so that WCAG conformance is enforced by the token graph's structure rather than checked ad hoc per component, demonstrated against the shipped Button accessibility specification.
- [[figma-tokens-studio-integration]] — Explains how designers bring the PointSav Design System's published DTCG token export into Figma with the Tokens Studio plugin's URL sync — a read-only pull from the system's own hosted JSON, with no export/import step — and why the read-only direction is a governance feature, with an honest comparison to Penpot's native token support.
- [[mcp-ai-agent-consumable-design-systems]] — Explains why the PointSav Design System exposes a machine-readable surface — an on-prem Model Context Protocol endpoint, a token search API, and a DTCG token export — so AI coding agents can query current token and component data from the same registry that renders the human-facing documentation, without any query leaving the host's own infrastructure.
- [[registry-driven-releases]] — Explains the registry-driven architecture behind the design-system site's releases: navigation, homepage statistics, the machine-readable registry endpoint, MCP responses, and release packaging all resolve against one registry file, so they cannot drift apart — illustrated with two real defects from the system's own history rather than hypotheticals.
- [[self-hosting-customer-controlled-design-systems]] — Explains the two distinct offers of the PointSav Design System — using the Apache-2.0 token data directly, which requires nothing, and separately self-hosting the serving engine to run a different organization's own in-house design system — including the real five-step fork procedure, the three-variable configuration surface, git-based governance, and the precise license boundaries between token data, server source, and article text.
<!-- END AUTO-GENERATED -->

## Brand surface

How the brand identity is encoded as colour families and typographic stacks across PointSav and Woodfine product surfaces.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: brand-surface -->
- [[brand-family-swatch]] — The brand color families assigned to retail and institutional anchor categories in the co-location GIS surface, providing consistent color-coded map and table identifiers.
- [[brand-typography]] — PointSav's web surfaces render in Inter, Source Serif 4, and Playfair Display, self-hosted rather than loaded from a system font stack. A separate, documented OFL print-typography matrix exists but has no shipped generation pipeline yet.
<!-- END AUTO-GENERATED -->

## Wiki surface design

The component vocabulary, typographic system, and dark-mode palette that compose the `documentation.pointsav.com` reading surface.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: wiki-surface-design -->
- [[wiki-component-library]] — The shared chrome — header, off-canvas mobile nav, left sidebar, and footer — plus the page templates it wraps, that together render every page on the PointSav knowledge platform.
- [[wiki-typography-system]] — The Inter and Source Serif 4 type stack, heading scale, and spacing tokens governing every wiki article page across the PointSav knowledge platform.
- [[wiki-dark-mode]] — Light and dark colour schemes for the PointSav wiki, driven by semantic-token overrides on a data-theme attribute, with theme persistence via localStorage.
<!-- END AUTO-GENERATED -->

## Related foundations

The architectural and substrate articles that frame the design system within the wider platform.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: related-foundations -->
- [[knowledge-wiki-leapfrog-architecture]] — How the wiki engine consumes the design system's tokens and components to render Wikipedia-shaped chrome over flat Markdown.
<!-- END AUTO-GENERATED -->

Additional planned articles — design-system tooling for BIM and AEC interface conventions — are not yet written.

## Foundation tokens

The four foundation-layer token families: colour, typography, spacing, and motion. Full specifications are maintained in `pointsav-design-system` and published on the design system's own site — these are external links, not wiki articles.

- [Colour tokens](https://design.pointsav.com/elements/color/overview) — primitive palette, semantic aliases, and dark-mode pairings in DTCG format.
- [Typography tokens](https://design.pointsav.com/elements/typography/overview) — type scale, font stacks, fluid type variables, and reading rhythm tokens.
- [Spacing tokens](https://design.pointsav.com/elements/spacing/overview) — base unit, geometric scale, component gap tokens, and layout margin tokens.
- [Motion tokens](https://design.pointsav.com/elements/motion/overview) — duration scale, easing curves, and reduced-motion variants.

## See also

- [Building Blocks](/substrate/) — the design-system substrate framing alongside the other foundational mechanism substrates
- [Design Patterns](/patterns/) — named design patterns that the design system encodes at the interface layer
- [Applications](/applications/) — operator-facing applications that consume the design system through the token and component layers
