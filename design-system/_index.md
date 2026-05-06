---
schema: foundry-doc-v1
title: "Design System"
slug: _index
category: design-system
type: reference
quality: complete
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-06
editor: pointsav-engineering
paired_with: _index.es.md
---

The PointSav design-system substrate is a self-hosted, customer-owned design-system engine. It delivers a complete token vocabulary, component recipe library, and editorial voice guide in a Git-tracked vault the customer owns outright — without dependency on Enterprise-tier design-system platforms.

The substrate serves three consumer types from the same vault: AI agents querying the MCP endpoint at codegen time, design tools synchronising against the DTCG token bundle, and human designers reading the component research.

## Foundation elements

The foundation layer defines the five primitives every surface is built from.

- [[design-color]] — three-layer color model (primitive, semantic, component) with five color families and WCAG 2.2 AAA contrast guarantees.
- [[design-typography]] — Utility and Display type scales; Inter canonical typeface; system-stack fallback.
- [[design-spacing]] — 13-step spacing scale on a 16 px base.
- [[design-motion]] — four easing curves and six duration steps; `prefers-reduced-motion` honoured unconditionally.

## Research

- [[design-philosophy]] — why the substrate exists; three structural inversions of the Enterprise-tier pattern.
- [[design-primitive-vocabulary]] — vocabulary rationale; what the substrate preserved from field convention and what it replaced.

## Component guides

Usage guides for individual components — HTML+CSS+ARIA recipes, token references, and accessibility requirements for each.

- [[guide-component-badge]]
- [[guide-component-breadcrumb]]
- [[guide-component-button]]
- [[guide-component-checkbox]]
- [[guide-component-citation-authority-ribbon]]
- [[guide-component-freshness-ribbon]]
- [[guide-component-home-grid]]
- [[guide-component-input-text]]
- [[guide-component-link]]
- [[guide-component-navigation-bar]]
- [[guide-component-notification]]
- [[guide-component-research-trail-footer]]
- [[guide-component-select]]
- [[guide-component-surface]]
- [[guide-component-switch]]
- [[guide-component-tab]]
