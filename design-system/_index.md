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
last_edited: 2026-05-29
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

The four foundation-layer token families: colour, typography, spacing, and motion. Full specifications maintained in `pointsav-design-system` and published at `design.pointsav.com/foundations/`.

- [[design-color]] — Colour token foundations: primitive palette, semantic aliases, and dark-mode pairings in DTCG format.
- [[design-typography]] — Typography token foundations: type scale, font stacks, fluid type variables, and reading rhythm tokens.
- [[design-spacing]] — Spacing token foundations: base unit, geometric scale, component gap tokens, and layout margin tokens.
- [[design-motion]] — Motion token foundations: duration scale, easing curves, and reduced-motion variants.

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
