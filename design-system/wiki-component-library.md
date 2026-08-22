---
schema: foundry-doc-v1
title: "Wiki component library"
slug: wiki-component-library
short_description: "The shared chrome — header, off-canvas mobile nav, left sidebar, and footer — plus the page templates it wraps, that together render every page on the PointSav knowledge platform."
category: design-system
type: topic
content_type: topic
index_group: wiki-surface-design
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-08-22
editor: pointsav-engineering
paired_with: wiki-component-library.es.md
---

The PointSav wiki is built from a small set of shared chrome elements — header, off-canvas mobile navigation, left sidebar, and footer — wrapped around one of several page templates, all composed in the [[app-mediakit-knowledge]] wiki engine. Class names follow a `k-*` manifest shared across every template, so styling one surface styles them all.

---

## Shared chrome

### Header

A sticky white header (`k-header`) with three regions: the site logo and wordmark on the left, a search box centred, and a controls cluster on the right — a light/dark theme toggle and a menu button that opens the mobile nav drawer.

### Off-canvas mobile nav

A left-side drawer (`k-nav-drawer`), not a bottom tab bar. The menu button in the header opens it as a modal dialog (`role="dialog"`, `aria-modal="true"`) with a dimming overlay behind it. Inside, a mobile copy of the search box sits above three link sections — Navigate, Resources, and PointSav network — each rendered as a labelled list. A close button and Escape both dismiss it.

### Left sidebar

A single sticky sidebar (`k-sidebar`) on desktop, not a split left/right layout. It stacks, in order: a "Main page" link, a "Browse by area" category list, a "Guides" link (on wikis that serve how-to content), and — only on pages with headings — a table of contents built from the page's H2/H3s. The table of contents is part of this same sidebar, not a separate right-rail component.

### Footer

A site-wide footer (`k-footer`), not a per-article one. Three link columns — Browse, This site, Network — followed by a base row: city list and copyright on the left, a "Powered by" badge on the right. Category tags and reference lists are not footer elements; where an article has footnotes, they render inline in the article body as part of the same content pipeline that produces the rest of the prose.

---

## Page templates

Each template wraps in the shared chrome above and fills the content region.

**Article** (`k-article`). A two-tab bar (Article / History), an optional "last updated" or point-in-time revision line, an optional historical-revision banner when viewing a past commit, the H1 title, and the rendered prose body.

**History** (`k-history`). The article's revision list — one entry per commit, each linking to that revision's diff.

**Diff**. A single revision's line-by-line change view, reached from the History tab.

**Home** (`k-home`). The site lede, a total-article count, a "Browse by area" grid of category cards, and — where guides exist — a "How-to guides" list.

**Category index / search results / special listings** (`k-catpage`). One shared template for four distinct listing views — a category's articles, search results, the full index of record, and recent changes — differing only in heading and source list.

**404** (`k-catpage` variant). A minimal chrome-wrapped message page; the wiki never serves a bare error.

There is no modal-dialog component, no numbered pagination between articles, and no quality-grade badge (Featured/Good/Stub, etc.) anywhere in this template set — none of the three exist in the current engine.

---

## Search

Search is server-rendered, not an API a client calls separately: the header's search box submits to `/search?q=`, which renders through the same `k-catpage` template as a category listing, with a result count and one card per match.

---

## Mobile discipline

Touch-target discipline applies across all interactive elements — the header's controls, sidebar links, drawer triggers, and tab links each carry a 44px × 44px minimum touch target (WCAG 2.2 SC 2.5.8).

---

## Token dependency

Every component draws its colours, spacing, and type from the `k-*` semantic tokens defined in [[design-system-substrate|the token vault]] — see [[wiki-dark-mode]] for the light/dark token pairs and [[wiki-typography-system]] for the type stack. No component introduces a raw colour or dimension value of its own.

---

## See also

- [[wiki-dark-mode]] — the theme toggle in the header and the semantic tokens each mode swaps
- [[wiki-typography-system]] — the Inter/Source Serif 4 type stack these templates render with
- [[design-system-substrate]] — the token vault every component draws from
- [[app-mediakit-knowledge]] — the wiki engine that renders this chrome and these templates
- [[component-recipes-vs-raw-tokens]] — the design-system's own separate component registry, distinct from this wiki-surface chrome
