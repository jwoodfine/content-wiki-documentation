---
schema: foundry-doc-v1
title: "Component Guide — Freshness Ribbon"
slug: guide-component-freshness-ribbon
category: design-system
type: reference
quality: complete
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-06
editor: pointsav-engineering
---

A per-section date badge that signals content review currency. Three semantic stops: fresh (≤90 days, green), stale (91–365 days, amber), archived (>365 days, muted). ISO date (YYYY-MM-DD) displayed in monospace — datestamp register. Attaches to `<h2>`/`<h3>` section headings via flex layout. Toggle off globally via `:root[data-freshness-display='off']`. All three variants pass WCAG 2.2 AA contrast.

## Technical Recipe

### HTML

```html
<h2 class="ps-article__section-heading">
  Section title
  <span class="ps-freshness-ribbon ps-freshness-ribbon--{{stop}}"
        data-source="{{source}}"
        data-iso="{{date}}"
        aria-label="Last reviewed {{date}} — {{stop}}">{{date}}</span>
</h2>
```

### CSS

```css
.ps-article__section-heading{display:flex;align-items:baseline;gap:.625rem;flex-wrap:wrap}.ps-freshness-ribbon{margin-left:auto;flex-shrink:0;display:inline-block;padding:.125rem .375rem;border-radius:var(--primitive-radius-xs,2px);font-family:var(--primitive-font-family-mono,'IBM Plex Mono',monospace);font-size:var(--primitive-font-size-1,.625rem);line-height:1.4;letter-spacing:.02em;white-space:nowrap;border:1px solid transparent;transition:opacity .1s ease}.ps-freshness-ribbon--fresh{background-color:var(--article-freshness-ribbon-bg-fresh,#e8f6ed);color:var(--article-freshness-ribbon-color-fresh,#16602b);border-color:var(--article-freshness-ribbon-border-fresh,#9fd4ae)}.ps-freshness-ribbon--stale{background-color:var(--article-freshness-ribbon-bg-stale,#fff5e1);color:var(--article-freshness-ribbon-color-stale,#7a520a);border-color:var(--article-freshness-ribbon-border-stale,#f5c843)}.ps-freshness-ribbon--archived{background-color:var(--article-freshness-ribbon-bg-archived,#f5f6f8);color:var(--article-freshness-ribbon-color-archived,#4a4f59);border-color:var(--article-freshness-ribbon-border-archived,#cdd1d8)}:root[data-freshness-display='off'] .ps-freshness-ribbon{display:none}@media(prefers-reduced-motion:reduce){.ps-freshness-ribbon{transition:none}}
```

## Accessibility

Each ribbon carries an `aria-label` announcing the ISO date and semantic stop (`Last reviewed 2026-03-15 — fresh`). Colour is not the sole differentiator — the stop name (`fresh`/`stale`/`archived`) is in the `aria-label`. The `data-iso` attribute is the machine-readable date surface. Archived variant: #4a4f59 on #f5f6f8 = 5.2:1 (passes WCAG 4.5:1 AA).

## See Also

- [[guide-component-citation-authority-ribbon]]
- [[guide-component-research-trail-footer]]

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*
