---
schema: foundry-doc-v1
title: "Applications"
slug: _index
category: applications
type: topic
quality: complete
short_description: "User-facing and internal applications built on the PointSav platform substrate — the wiki engine, marketing surface, GIS analytics engine, the browser developer workbench, the structured-input gate, and the design-intent articles that frame how those surfaces are composed."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-29
editor: pointsav-engineering
paired_with: _index.es.md
---

Applications sit above the three-ring service layer. They consume deterministic data and optional AI output from the rings and present it through a defined interface. An application holds no canonical data — it is a view over the service layer, and can be re-provisioned without data loss by pointing a fresh instance at the immutable data underneath. The articles in this category cover both the named applications themselves and the design-intent material that explains how each surface is composed.

Each application here corresponds to an `app-*` directory in the monorepo and inherits the [[three-ring-architecture]] separation; none holds the authoritative record. Reader-facing chrome and design rationale articles are gathered alongside the application articles so that operators evaluating a surface can move from the engineering article to the design intent without leaving the category.

## Knowledge and editorial applications

The wiki engine, the marketing surface, and the design-intent articles that describe their reader-facing chrome.

- [[app-mediakit-knowledge]] — The single-binary Rust wiki engine that renders PointSav's engineering documentation; a view over a Markdown tree where the git commits are canonical and every running binary is throwaway derived state.
- [[app-mediakit-marketing]] — Multi-tenant marketing landing pages from a single statically-compiled Rust binary; WordPress.org muscle memory at the operator-facing URL, sovereign infrastructure underneath.
- [[knowledge-wiki-home-page-design]] — How the documentation home page inherits Wikipedia's structural conventions and extends them for engineering and financial-community readers.
- [[wikipedia-leapfrog-design]] — What the wiki engine inherits from Wikipedia, what it adds beyond it, and what the five-percent leapfrog headroom means for readers and engineers.
- [[documentation-pointsav-com-launch-2026-04-27]] — The April 2026 TLS launch of `documentation.pointsav.com`: serving stack, placeholder posture, and verification commands.

## Location intelligence applications

The GIS analytics engine, the platform article that frames it alongside the rendering layer, and the user-experience design intent.

- [[app-orchestration-gis]] — The stateless spatial analytics engine for linear-geometry calculations and co-location ranking; a pure function that holds no canonical data and can be re-provisioned by pointing a fresh instance at the data layer.
- [[location-intelligence-platform]] — The full location intelligence platform: `app-orchestration-gis` (analytics) paired with the rendering engine; every dataset, algorithm, and rendering decision under customer control.
- [[location-intelligence-ux]] — The Conclusion-First design philosophy: ranked tier conclusions rather than individual data points, so users see the most defensible commercial nodes at national zoom before drilling into individual operators.

## Input and developer surfaces

The structured-input gate that admits external files to a Totebox, and the browser workbench for working with archive files outside a terminal.

- [[app-console-input]] — The F12 surface in os-console: the structured input gate through which raw external files enter a Totebox before being sealed into the verified ledger.
- [[app-privategit-workbench]] — A browser-based three-column file editor included in os-privategit; for working with archive files without a terminal session.

## Domain applications

Surfaces dedicated to a specific operational domain — Building Information Modelling and real-property workflows.

- [[bim-and-real-property-surfaces]] — How PointSav treats Building Information Modelling as a first-class operational domain, with dedicated design-system tooling and ISO 19650 record-keeping discipline.
- [[building-design-system-bim]] — Design-system tooling adapted for BIM and real-property workflows.
- [[flat-file-bim-leapfrog]] — How Building Information Modelling is handled as flat-file ISO 19650 records rather than hosted database instances.
- [[aec-interface-conventions]] — Interface conventions for AEC surfaces that BIM applications inherit and extend.
- [[property-manager-bim-gap]] — The gap between BIM authoring tools and property-manager workflows, and how the application surfaces close it.

## See also

- [Services](/services/) — the service layer that applications build on
- [Systems](/systems/) — the operating systems that host applications
- [Architecture](/architecture/) — the three-ring model and the customer-ownership principles
- [Design system](/design-system/) — the token and component vocabulary the application chrome inherits
