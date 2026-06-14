---
schema: foundry-doc-v1
title: "Design system philosophy"
slug: design-philosophy
short_description: "The PointSav design system is a self-hosted, customer-owned substrate running at design.pointsav.com that publishes design decision research alongside token values in DTCG format, prioritizing editor-agnostic interoperability and structured rationale."
category: design-system
type: reference
content_type: topic
quality: complete
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-25
editor: pointsav-engineering
paired_with: design-philosophy.es.md
cites:
 - wcag-22
 - dtcg-spec
 - doctrine-38
---

The PointSav [[design-system-substrate|design system]] is a self-hosted, customer-owned substrate for managing design tokens, components, and design-decision research. It addresses four structural gaps in the 2026 design-system landscape — the absence of machine-readable design rationale, enterprise-tier pricing that excludes small and medium businesses (SMBs), editor lock-in, and insufficient AI-consumable structure — through three architectural inversions of the dominant platform model. The token vocabulary is documented in [[design-primitive-vocabulary]]; the wiki rendering surface built on this substrate is served by [[app-mediakit-knowledge]].

## Why the substrate exists

The substrate is a self-hosted, customer-owned design-system engine running at `design.pointsav.com` and at every SMB customer site that forks it. Its existence is a direct response to four structural gaps in the 2026 design-system landscape:

1. **Established design systems publish only the WHAT.** Major design system publications deliver token values and component shapes. None publish the design-decision research — the WHY — in a form an AI agent or a human at a new organisation can read at codegen time.

2. **Enterprise-tier design-system platforms charge enterprise-tier pricing.** SaaS platforms targeting design-system management serve the 5,000+ employee market. The 39% of practitioners working at that scale have options; the SMB beneath them has none.

3. **Every editor wants to be the editor.** All major design editors build to lock the customer into their platform. The W3C Design Tokens Community Group format is the editor-agnostic common denominator the substrate adopts as canonical.

4. **AI codegen is widening the design-system surface area faster than tooling catches up.** Only 23% of design systems are structured for AI consumption (December 2025 industry data). Existing editor-integrated design-system integrations are locked to specific cloud platforms and licensed customers. A self-hosted, editor-agnostic substrate with AI-readable research is intended to occupy a structural position no editor-locked platform can reach.

## What the substrate does

The substrate carries five elements per tenant, in a Git-tracked vault the customer owns:

- **`tokens/`** — DTCG-format design tokens. Primitive layer (PointSav-original color families, type scale, spacing, motion, focus ring — structural patterns aligned with the modern design-system field, hex values and family names PointSav's), semantic layer (interactive-primary, surface-elevated, ...), component layer.
- **`components/`** — HTML+CSS+ARIA recipe files. Framework-agnostic; the customer's chosen framework consumes the recipe, not the other way around.
- **`themes/<brand>/`** — per-tenant override layers that re-point semantic references at primitives.
- **`research/`** — AI-readable design-decision rationale, accessibility justifications, brand-voice rules, anti-patterns.
- **`exports/`** — derived caches (Figma Variables JSON, Tailwind config, CSS variables, Style Dictionary builds). Recomputable from the canonical four directories above.

The substrate engine (`app-privategit-design`) reads this vault and serves it as a public showcase, a DTCG bundle, an AI-readable research surface, and a Model Context Protocol (MCP) server. AI agents query the MCP endpoint at codegen time; design tools query `/tokens.json` for editor synchronisation; humans read the showcase.

## Three structural inversions of the Enterprise-tier pattern

1. **Customer ownership replaces platform hosting.** The design system lives in the customer's Git repository with the customer's `allowed_signers` chain. Migration cost falls toward zero — the customer always has the source.
2. **Research as canonical replaces research as marketing.** The WHY lives in the same vault as the WHAT, in the same machine-readable tier, served through the same MCP endpoint. AI agents and human designers read the same file.
3. **Editor-agnosticism replaces editor lock-in.** DTCG is the common denominator. Any design editor that supports DTCG export produces vault content the substrate accepts.

## The McLuhan position

In the AI era of 2026–2030, an SMB's design-system substrate is a medium — its form (machine-readability, editor-agnostic interop, self-hostability, AI-consumable research) shapes how the SMB's brand reaches every customer-facing surface.

The well-structured substrate IS the message the SMB sends to its implementation partners — human or AI. That is the McLuhan position the substrate operationalises.

## Mobile-first and Inter foundation

Every operator surface the design system renders is designed mobile-first. Layout, navigation, and interactive components are specified at 375 px before progressive enhancement for wider viewports. Touch targets meet WCAG 2.2 SC 2.5.8 — 44 px × 44 px minimum — and interactions do not rely on hover states. Safe-area padding (`env(safe-area-inset-*)`) is applied to shell chrome for notched and dynamic-island displays.

The UI typography foundation is **Inter** (SIL OFL 1.1) — a community-maintained neo-grotesque designed specifically for screen readability, with no corporate brand association. Inter is the practical output of choosing editor-agnosticism in typography: it is the single most interoperable, widely-available, screen-optimised typeface that no platform owns. See [[wiki-typography-system]] for the full wiki-surface type stack (Inter + Source Serif 4 + system mono).

## Anti-patterns the substrate refuses

- Storybook integration (parallel renderer; substrate owns rendering).
- Enterprise-tier design-system SaaS dependency.
- JS-framework-locked components (HTML+CSS+ARIA recipes are the canonical form).
- Container packaging (per [[zero-container-runtime]]).
- Editor lock-in (single-editor-only features rejected).
- Marketing vocabulary in research files (research files describe structural rationale, not product positioning).

## See also

- [[design-primitive-vocabulary]] — the token vocabulary layer: numeric color scales, semantic aliasing, and PointSav-original naming rationale
- [[design-system-substrate]] — the substrate architecture: Git-tracked vault, MCP endpoint, and multi-tenant override structure
- [[wiki-component-library]] — nine wiki components built on this token system
- [[app-mediakit-knowledge]] — the wiki engine that renders the design system's public showcase surface

## References

- W3C Design Tokens Community Group format — https://design-tokens.github.io/community-group/format/
- WCAG 2.2 (accessibility floor) — https://www.w3.org/TR/WCAG22/
- Marshall McLuhan, *Understanding Media: The Extensions of Man* (1964) ch. 1 "The Medium is the Message"
