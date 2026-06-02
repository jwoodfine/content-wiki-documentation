---
schema: foundry-doc-v1
title: "Wiki component library"
slug: wiki-component-library
short_description: "Nine reusable interface components that compose a complete wiki article page on the PointSav knowledge platform."
category: design-system
type: topic
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-25
editor: pointsav-engineering
paired_with: wiki-component-library.es.md
---

# Wiki component library

The PointSav wiki component library defines nine reusable interface units that together render a complete wiki article page in the [[app-mediakit-knowledge]] wiki engine. Each component targets Wikipedia's established layout conventions — following the [[wikipedia-leapfrog-design|leapfrog design philosophy]] — while applying current accessibility standards and the [[design-system-substrate|PointSav token system]].

---

## Architecture overview

A wiki article page is composed from a stack of components:

```
┌─────────────────────────────────────────────────────┐
│  wiki-drawer-mobile-nav  (compact viewports only)   │
├─────────────────────────────────────────────────────┤
│  wiki-article-header  (breadcrumb + H1 + badge + meta)│
├──────────────────┬──────────────────────────────────┤
│                  │  wiki-toc-sidebar  (right rail)  │
│  Article body    │  (desktop only)                  │
│  (prose)         ├──────────────────────────────────┤
│                  │  wiki-badge-tag (quality/category)│
├──────────────────┴──────────────────────────────────┤
│  wiki-article-footer  (categories + refs + edit)    │
├─────────────────────────────────────────────────────┤
│  wiki-pagination  (prev/next article in category)   │
└─────────────────────────────────────────────────────┘

Overlays (triggered by user action):
  wiki-modal-dialog     — image lightbox, search overlay
  wiki-dark-mode-toggle — persistent theme switch (site header)

Search:
  wiki-search-results   — results list (own page or in modal)
```

---

## Components

### wiki-article-header

Top-of-article surface. Renders four elements in sequence: (1) slug breadcrumb showing the article's category path, (2) the article H1 title from frontmatter, (3) an optional quality badge, and (4) a byline showing last-edited date and a history link.

Quality grades: Featured Article (gold), Good Article (green), A-class (blue), B-class (light blue), C-class (grey), Stub (light grey). Ungraded articles omit the badge slot.

**Token:** `--ps-wiki-text-h1` = 2.25 rem (36 px at 17 px base).

---

### wiki-article-footer

Bottom-of-article surface. Three sections: (1) category tag links, (2) a numbered references list using `<ol id="ref-N">` for in-article back-links, and (3) an edit-on-GitHub link for contributors.

---

### wiki-toc-sidebar

Sticky right-rail sidebar listing article headings (H2 and H3). On desktop (≥ 800 px) it uses `position: sticky; top: 1rem`. On compact viewports (≤ 799 px) it collapses to an inline `<details>` / `<summary>` toggle above the article body.

The active section is highlighted via a JavaScript `IntersectionObserver` watching all `[id]` heading anchors. When a heading enters the viewport, its table-of-contents entry receives `aria-current="true"` and the active visual style.

---

### wiki-search-results

Ordered list of search hits returned by the Tantivy search engine. Each result displays the article title as a link and a plain-text excerpt of approximately 180 characters, truncated at a word boundary. The component wraps in `aria-live="polite"` so assistive technologies announce result-count updates.

**API shape:** `POST /mcp`, JSON-RPC 2.0, method `search`. Response: `{query, count, hits: [{slug, title, snippet}]}`. Snippets are plain text only. A zero-results state is toggled with the `[hidden]` attribute.

---

### wiki-modal-dialog

Overlay using the native `<dialog>` element with `showModal()`. The native dialog element provides a built-in focus trap: all content outside the dialog is unreachable by keyboard until the dialog closes. Used for image lightboxes, the search overlay, and confirmation prompts. Closes on Escape (native browser behaviour) and on backdrop click.

---

### wiki-dark-mode-toggle

A toggle button that sets `data-theme="dark"` on `<html>` and persists the choice in `localStorage` under the key `ps-theme`. On each page load, an inline script reads this value before the stylesheet renders, preventing a flash of the unintended theme. Falls back to `prefers-color-scheme: dark` if no explicit choice is stored.

---

### wiki-badge-tag

Dual-purpose chip: (1) article quality grade badge — a non-interactive `<span>` with `aria-label` providing the full grade name — and (2) category tag links using `<a>` chips. Used in the article header (quality badge) and article footer (category tags).

---

### wiki-pagination

Prev/Next article navigation within a category. The component is a three-column grid: previous article link (left), current category name link (centre), next article link (right). Each directional link carries `rel="prev"` / `rel="next"` for SEO and an `aria-label` providing the full adjacent article title for assistive technologies.

This component handles sequential article navigation. Numbered pagination for search results and category listings is a separate planned component.

---

### wiki-drawer-mobile-nav

Slide-in left-panel navigation for compact (≤ 799 px) viewports. A hamburger trigger button opens the drawer. When open, the `inert` attribute is applied to the main content region and header, locking keyboard focus inside the drawer until it is dismissed. Closes on Escape or backdrop click.

The `inert` attribute is natively supported in Chrome 102+, Firefox 112+, and Safari 15.5+. A WICG polyfill (approximately 3 KB gzipped) covers older browsers.

---

## Mobile discipline

All nine components are designed mobile-first against a 375 px reference viewport. The Inter typeface (UI and headings) and Source Serif 4 (body prose) are loaded as variable fonts via `font-display: swap`; fallback system fonts render immediately on slow connections — see [[wiki-typography-system]].

Touch-target discipline applies across all interactive elements: trigger buttons, TOC entries, edit pencils, pagination links, toggle controls, and modal close targets each carry a 44 px × 44 px minimum touch target (WCAG 2.2 SC 2.5.8). No interaction depends on hover state — every hover affordance (page preview, citation tooltip, quality-badge popover) degrades to a tap-triggered equivalent.

Safe-area padding (`env(safe-area-inset-*)`) is applied to the shell chrome (`wiki-drawer-mobile-nav` trigger and footer region) to accommodate notched and dynamic-island displays. Content columns do not apply safe-area insets; only chrome elements that sit at the screen edge do.

## Token dependency

All nine components draw exclusively from the PointSav token system defined in `dist/tokens.css`. No component introduces raw colour or dimension values. New wiki pages and templates add components without introducing new CSS variables.

---

## See also

- [[wiki-dark-mode]] — light and dark colour schemes with WCAG-verified palettes and theme persistence
- [[wiki-typography-system]] — Inter and Source Serif 4 type stack used across these components
- [[design-system-substrate]] — the token and component vault these nine components draw from
- [[app-mediakit-knowledge]] — the wiki engine that composes these components into rendered article pages
