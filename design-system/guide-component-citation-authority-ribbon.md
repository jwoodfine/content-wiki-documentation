---
schema: foundry-doc-v1
title: "Component Guide — Citation Authority Ribbon"
slug: guide-component-citation-authority-ribbon
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

A leading source-classification badge in a references list. Six source types — Academic (A), Regulator (R), Industry (I), Direct source (D), News (N), Web-informal (W) — each with a distinct colour and single-letter glyph. Colour is never the sole differentiator; each badge carries a letter glyph and an `aria-label` with the full class name. Designed for Wikipedia-style references sections.

## Technical Recipe

### HTML

```html
<ol class="ps-references">
  <li data-source-authority="academic">
    <span class="ps-citation-badge ps-citation-badge--academic" aria-label="Academic source" title="Academic source">A</span>
    <span>Klein et al. 2009 — seL4: Formal Verification of an OS Kernel.</span>
    <a href="#cite-ref-1" aria-label="Back to reference 1">↑</a>
  </li>
</ol>
```

### CSS

```css
.ps-references{list-style:none;padding:0;margin:0}.ps-references li{display:grid;grid-template-columns:1.5rem 1fr 1.5rem;gap:.5rem;align-items:baseline;padding:.375rem 0;border-bottom:1px solid var(--semantic-border-subtle,#e6e8ec)}.ps-references li:last-child{border-bottom:none}.ps-citation-badge{display:inline-flex;align-items:center;justify-content:center;width:1.25rem;height:1.25rem;border-radius:var(--primitive-radius-xs,2px);font-size:.625rem;font-weight:700;line-height:1;flex-shrink:0}.ps-citation-badge--academic{background-color:var(--ps-support-info,#234ed8);color:#fff}.ps-citation-badge--regulator{background-color:var(--ps-support-positive,#16602b);color:#fff}.ps-citation-badge--industry{background-color:var(--semantic-surface-layer-accent,#e6e8ec);color:var(--semantic-text-primary,#0e0f12);border:1px solid var(--semantic-border-subtle,#cdd1d8)}.ps-citation-badge--direct{background-color:var(--ps-support-teal-bg,#d9fbfb);color:var(--ps-support-teal,#009d9a);border:1px solid var(--ps-support-teal,#009d9a)}.ps-citation-badge--news{background-color:var(--ps-support-warning-bg,#fff5e1);color:var(--ps-support-warning,#7a520a)}.ps-citation-badge--web{background-color:transparent;color:var(--semantic-text-secondary,#878d99);border:1px solid var(--semantic-border-subtle,#e6e8ec)}.ps-references a[href^='#']{color:var(--semantic-text-secondary,#4a4f59);text-decoration:none;font-size:.75rem}
```

## Accessibility

Each badge carries an `aria-label` with the full source class name (`Academic source`, `Regulator source`, etc.) and a single-letter glyph — colour is never the sole differentiator. The badge is a `<span>`, not interactive. Only `<a>` elements (citation URL, backref arrow) are keyboard-reachable. Use `<ol class="ps-references">` as the outer wrapper — the ordered list preserves citation numbering. The `data-source-authority` attribute is the machine-readable surface for JSON-LD consumers.

## See Also

- [[guide-component-freshness-ribbon]]
- [[guide-component-research-trail-footer]]

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*
