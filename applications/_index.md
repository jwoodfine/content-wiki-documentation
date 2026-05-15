---
schema: foundry-doc-v1
title: "Applications"
slug: _index
category: applications
type: topic
quality: complete
short_description: "User-facing and internal applications built on the PointSav platform substrate — the wiki engine, marketing surface, GIS analytics engine, and the structured-input gate through which external files enter a Totebox."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-15
editor: pointsav-engineering
paired_with: _index.es.md
---

Applications sit above the three-ring service layer. They consume deterministic data and optional AI output from the rings and present it through a defined interface. An application holds no canonical data — it is a view over the service layer, and can be re-provisioned without data loss by pointing a fresh instance at the immutable data underneath.

## Knowledge and editorial

- [[app-mediakit-knowledge]] — The single-binary Rust wiki engine that renders PointSav's engineering documentation; a view over a Markdown tree where the git commits are canonical and every running binary is throwaway derived state.
- [[app-mediakit-marketing]] — Multi-tenant marketing landing pages from a single statically-compiled Rust binary; WordPress.org muscle memory at the operator-facing URL, sovereign infrastructure underneath.

## GIS and location intelligence

- [[app-orchestration-gis]] — The stateless spatial analytics engine for linear-geometry calculations and co-location ranking; a pure function that holds no canonical data and can be re-provisioned by pointing a fresh instance at the data layer.
- [[location-intelligence-platform]] — The full location intelligence platform: app-orchestration-gis (analytics) and pointsav-gis-engine (rendering), with every dataset, algorithm, and rendering decision under customer control.

## Input and ingest

- [[app-console-input]] — The F12 surface in os-console: the structured input gate through which raw external files enter a Totebox before being sealed into the verified ledger.

## Domain applications

- [[bim-and-real-property-surfaces]] — How PointSav treats Building Information Modelling as a first-class operational domain, with dedicated design-system tooling and ISO 19650 record-keeping discipline.

## See also

- [Services](/services/) — the service layer that applications build on
- [Systems](/systems/) — the operating systems that host applications
- [Architecture](/architecture/) — the three-ring model and the customer-ownership principles
