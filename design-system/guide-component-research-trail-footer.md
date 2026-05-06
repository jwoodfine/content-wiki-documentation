---
schema: foundry-doc-v1
title: "Component Guide — Research Trail Footer"
slug: guide-component-research-trail-footer
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

A collapsible disclosure at article foot showing the research pipeline trail — Done, Suggested, and Open questions subsections. Collapsed by default. Uses native `<details>`/`<summary>` — no JavaScript required. Placed after "See also", before "References". Only rendered for articles with `research_trail: true` frontmatter and non-zero counts.

## Technical Recipe

### HTML

```html
<details class="ps-research-trail">
  <summary class="ps-research-trail__summary">
    Research trail — {{done}} done · {{suggested}} suggested · {{open}} open question(s)
  </summary>
  <section class="ps-research-trail__body" aria-label="Research trail detail">
    <!-- done / suggested / open subsections -->
  </section>
</details>
```

### CSS

```css
.ps-research-trail{background:var(--semantic-surface-layer-accent,#f0f2f5);border:1px solid var(--semantic-border-subtle,#e6e8ec);border-radius:var(--primitive-radius-xs,2px);margin:var(--primitive-space-4,2rem) 0 var(--primitive-space-3,1.5rem);padding:0}.ps-research-trail[open]{padding-bottom:var(--primitive-space-3,1.5rem)}.ps-research-trail__summary{cursor:pointer;padding:var(--primitive-space-2,1rem) var(--primitive-space-3,1.5rem);font-size:var(--primitive-font-size-3,.875rem);font-weight:600;color:var(--semantic-text-primary,#0e0f12);user-select:none;list-style:none}.ps-research-trail__summary::-webkit-details-marker{display:none}.ps-research-trail__summary::before{content:'▶';display:inline-block;margin-right:.5rem;font-size:.625rem;transition:transform .15s ease;vertical-align:.1em}.ps-research-trail[open]>.ps-research-trail__summary::before{transform:rotate(90deg)}.ps-research-trail__body{padding:0 var(--primitive-space-3,1.5rem)}.ps-research-trail__heading{font-size:var(--primitive-font-size-3,.875rem);font-weight:600;margin:var(--primitive-space-2,1rem) 0 .375rem;padding-left:.625rem;border-left:3px solid transparent}.ps-research-trail__heading--done{border-left-color:var(--ps-support-positive,#16602b);color:var(--ps-support-positive,#16602b)}.ps-research-trail__heading--suggested{border-left-color:var(--ps-support-info,#234ed8);color:var(--ps-support-info,#234ed8)}.ps-research-trail__heading--open{border-left-color:var(--ps-support-caution,#7a520a);color:var(--ps-support-caution,#7a520a)}.ps-research-trail__list{margin:0;padding-left:1.5rem;font-size:var(--primitive-font-size-3,.875rem);color:var(--semantic-text-primary,#0e0f12)}.ps-research-trail__list li{margin-bottom:.25rem}
```

## Accessibility

Uses native `<details>`/`<summary>` — browsers provide keyboard (Space/Enter to toggle), `aria-expanded`, and screen-reader announcements natively. The summary announces the count summary line. The `<section aria-label="Research trail detail">` provides a landmark for the expanded body. Three `<h3>` headings (Research done / Research suggested / Open questions) use coloured left-borders as subsection signals; colour is supplemental — heading text is the primary differentiator.

## See Also

- [[guide-component-citation-authority-ribbon]]
- [[guide-component-freshness-ribbon]]

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*
