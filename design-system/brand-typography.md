---
schema: foundry-doc-v1
type: topic
content_type: topic
index_group: brand-surface
slug: brand-typography
short_description: "PointSav's web surfaces render in Inter, Source Serif 4, and Playfair Display, self-hosted rather than loaded from a system font stack. A separate, documented OFL print-typography matrix exists but has no shipped generation pipeline yet."
title: "Brand typography and print standards"
audience: vendor-public
bcsc_class: current-fact
language: en
paired_with: brand-typography.es.md
category: design-system
status: active
last_edited: 2026-08-22
editor: pointsav-engineering
---



Web and print typography are governed separately. The web layer — the documentation wiki, the marketing surface — self-hosts a fixed font set rather than falling back to whatever the visitor's OS provides, so the same page reads identically on every device. Print typography is a separate, currently-aspirational specification: a documented OFL font matrix with no shipped tool that embeds it into a real document yet.

## The web layer: self-hosted, not system fonts

`app-mediakit-knowledge`, the wiki engine, ships three self-hosted `.woff2` families — Inter for interface and body text, Source Serif 4 for long-form reading, and Playfair Display for display headings. All three are compiled into the engine's static assets and served from the same origin as the page; nothing is fetched from a font CDN or a visitor's installed system fonts. A visitor without Inter installed still sees Inter.

## The print matrix: documented, not yet built

A separate typography specification exists for printed and PDF output — white papers, financial tables, formal disclosures. It is built on SIL Open Font License (OFL) equivalents of proprietary references:

| Token | Active Font | Legacy Reference | Intended Application |
| :--- | :--- | :--- | :--- |
| **serif_primary** | **Zilla Slab** | Caecilia LT Std | Institutional trust marks (white paper covers). |
| **sans_condensed**| **Barlow Condensed** | Trade Gothic | Data-dense financial ledgers and tables. |
| **sans_primary** | **Nunito Sans** | Avenir LT Std | Standard body copy and operational text. |

These font names are real design tokens, defined as CSS custom-property fallback chains at the monorepo's `templates/tokens.css`. No PDF-generation or document-compilation tool currently consumes them — the matrix specifies what a print pipeline should use once one exists, not a live mechanism embedding fonts into shipping PDFs today.

## Digital Asset Resolution

The platform's asset-licensing principle — every embedded asset must be freely distributable — applies to both the shipped web fonts and the documented print matrix: all listed typefaces are OFL, chosen specifically so no font-licensing review blocks a future print pipeline from using them.

## See also

- [[brand-family-swatch]]
- [[news-release-standards]]
