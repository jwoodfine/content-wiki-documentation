---
schema: foundry-doc-v1
title: "Wiki Component Library"
slug: wiki-component-library
category: design-system
type: topic
quality: core
status: active
bcsc_class: vendor-public
last_edited: 2026-05-07
editor: pointsav-engineering
cites: []
paired_with: wiki-component-library.es.md
---

The PointSav wiki component library defines nine reusable interface units that together
render a complete wiki article page. Each component targets Wikipedia's established
layout muscle-memory while applying modern accessibility standards and the PointSav
token system. All components draw exclusively from CSS custom properties defined in
`dist/tokens.css`; no component introduces raw colour or dimension values. The library
was specified by a 24-agent design research pass (2026-05-06).

## Architecture Overview

A wiki article page is composed from a stack of components:

```
┌─────────────────────────────────────────────────────┐
│  wiki-drawer-mobile-nav  (compact only — hamburger) │
├──────────────────────────────────────────────────────┤
│  wiki-article-header  (breadcrumb + H1 + badge + meta)│
├──────────────────┬──────────────────────────────────┤
│                  │  wiki-toc-sidebar  (right rail)  │
│  Article body    │  (desktop only)                  │
│  (prose)         ├──────────────────────────────────┤
│                  │  wiki-badge-tag (quality/category)│
├──────────────────┴──────────────────────────────────┤
│  wiki-article-footer  (categories + refs + edit)     │
├─────────────────────────────────────────────────────┤
│  wiki-pagination  (prev/next article in category)    │
└─────────────────────────────────────────────────────┘

Overlays (triggered by user action):
  wiki-modal-dialog     — image lightbox, search overlay
  wiki-dark-mode-toggle — persistent theme switch (site header)

Search:
  wiki-search-results   — results list (own page or in modal)
```

## Components

### wiki-article-header

Top-of-article surface. Renders four elements in order: (1) slug breadcrumb showing the
article's category path, (2) the article H1 title from frontmatter, (3) an optional
quality badge, and (4) a byline showing last-edited date, editor name, and a history link.

Quality grades: Featured Article (gold), Good Article (green), A-class (blue), B-class
(light blue), C-class (grey), Stub (light grey). Ungraded articles omit the badge slot.

**Token:** `--ps-wiki-text-h1` = 2.25rem (38px at 17px base).

### wiki-article-footer

Bottom-of-article surface. Three sections: (1) category tag links, (2) numbered
references list using `<ol id="ref-N">` for in-article back-links, and (3) an
edit-on-GitHub link for contributors.

### wiki-toc-sidebar

Sticky right-rail sidebar listing article headings (H2 and H3). On desktop (≥800px):
`position: sticky; top: 1rem`. On compact (≤799px): collapses to an inline
`<details>`/`<summary>` toggle above the article body.

Active section is highlighted by JavaScript using `IntersectionObserver`. When a heading
enters the viewport, its TOC entry receives `aria-current="true"` and the active visual
style.

### wiki-search-results

Ordered list of search hits returned by the Tantivy search engine. Each hit displays:
article title (as a link) and a plain-text excerpt (~180 characters, truncated at word
boundary with ellipsis). The component wraps in `aria-live="polite"` so screen readers
announce result count updates.

**API shape:** `POST /mcp`, JSON-RPC 2.0, method `search`. Response:
`{query, count, hits: [{slug, title, snippet}]}`. No HTML in snippets — plain text only.
A zero-results state is toggled with the `[hidden]` attribute.

### wiki-modal-dialog

Overlay using the native `<dialog>` element with `showModal()`. Native `<dialog>`
provides a built-in focus trap — all content outside the dialog is unreachable by
keyboard until the dialog closes. Used for image lightboxes, the search overlay, and
confirmation prompts. Dismisses on Escape (native browser behaviour) and on backdrop
click.

### wiki-dark-mode-toggle

A toggle button that sets `data-theme="dark"` on `<html>` and persists the user choice
in `localStorage` under key `ps-theme`. On each page load, an inline script reads this
value before the stylesheet renders, preventing a flash of the wrong theme. Falls back
to `prefers-color-scheme: dark` if no explicit choice has been stored. See
[[wiki-dark-mode]] for the full palette and initialisation detail.

### wiki-badge-tag

Dual-purpose chip: (1) article quality grade badge (non-interactive `<span>` with
`aria-label` providing the full grade name), and (2) category tag links (`<a>` chips).
Used in the article header (quality badge) and article footer (category tags).

### wiki-pagination

Prev/Next article navigation within a category. Three-column grid: previous article link
(left), current category name link (centre), next article link (right). Each directional
link carries `rel="prev"` / `rel="next"` for SEO, and an `aria-label` providing the full
adjacent article title for screen readers.

This is article-level navigation, not numeric pagination. A numeric pagination component
for search results and category listings is intended for a future release.

### wiki-drawer-mobile-nav

Slide-in left-panel navigation for compact (≤799px) viewports. A hamburger trigger
button opens the drawer. When open, the `inert` attribute is applied to the page's main
content region and header, locking keyboard focus inside the drawer until dismissed.
Closes on Escape or backdrop click.

`inert` is natively supported in Chrome 102+, Firefox 112+, Safari 15.5+. A WICG
polyfill (~3 KB gzipped) covers older browsers.

## See Also

- [[wiki-dark-mode]]
- [[wiki-typography-system]]
- [[design-primitive-vocabulary]]
