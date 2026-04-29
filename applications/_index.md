---
schema: foundry-doc-v1
title: "Applications — Category Landing"
slug: _index
category: applications
status: pre-build
last_edited: 2026-04-29
editor: pointsav-engineering
---

## Applications

This category covers user-facing and internal applications built on the PointSav platform substrate. Applications sit above the three-ring service layer; they consume the deterministic data and optional AI services that the rings produce and present that output to users through a defined interface.

Applications in this category include the wiki engine that renders this site, workplace productivity tooling, and the presentation surface for data extracted by the platform's Ring 2 services. Each article describes one application: its purpose, the substrate services it depends on, the audience it serves, and the architectural decisions that shaped it. Articles are written for engineers building or extending an application, and for designers working with the application's interface substrate.

## Articles in this category

- [[topic-app-mediakit-knowledge]] — The Rust wiki engine that renders this documentation site; Markdown pipeline, wikilink resolver, full-text search, and browser editor.

<!-- ENGINE: this list is editorial in iteration-1; iteration-2+
generates it from category-directory file listing once PL.7
chunked-migration moves articles into category subdirectories. -->

## See also

- [Wiki home](/)
- [Services](/services/)
- [Architecture](/architecture/)

<!-- EDITORIAL NOTE: PL.7 chunked normalization sweep will migrate
     root-prefixed TOPICs into this category subdirectory. Until
     migration lands, the existing root TOPICs render at their current
     URLs (topic-<slug>.md); this landing references them by current slug. -->
