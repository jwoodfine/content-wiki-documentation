---
schema: foundry-doc-v1
title: "Component Guide — Home Grid"
slug: guide-component-home-grid
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

A 3-column responsive category-browse grid for knowledge-wiki home pages. Shows operator-ratified categories with article count, top-3 child links, and a More → entry point. Collapses to 2-column at 960px, 1-column at 640px. Empty categories always rendered with empty-state copy.

## Technical Recipe

### HTML

```html
<section class="ps-home-grid" aria-label="Browse by category">
  <h2 class="ps-home-grid__heading">Browse by category</h2>
  <div class="ps-home-grid__row">
    <!-- ps-home-grid__card elements, one per category -->
  </div>
</section>
```

### CSS

```css
.ps-home-grid{}.ps-home-grid__heading{font-family:var(--primitive-font-family-heading,Georgia,'Times New Roman',serif);font-size:var(--primitive-font-size-9,2rem);font-weight:700;color:var(--semantic-text-primary,#0e0f12);margin:0 0 var(--component-home-grid-gap,1rem);line-height:1.2}.ps-home-grid__row{display:grid;grid-template-columns:repeat(3,1fr);gap:var(--component-home-grid-gap,1rem);margin-bottom:var(--primitive-space-4,2rem)}@media(max-width:960px){.ps-home-grid__row{grid-template-columns:repeat(2,1fr)}}@media(max-width:640px){.ps-home-grid__row{grid-template-columns:1fr}}.ps-home-grid__card{background:var(--component-home-grid-card-surface,#fff);border:var(--component-home-grid-card-border-width,1px) solid var(--component-home-grid-card-border-color,#e6e8ec);border-radius:var(--component-home-grid-card-radius,2px);padding:var(--component-home-grid-card-padding,1rem);transition:border-color .15s ease}.ps-home-grid__card:hover{border-color:var(--semantic-interactive-link,#3366cc)}.ps-home-grid__title{margin:0 0 .25rem;font-size:var(--primitive-font-size-6,1.125rem);font-weight:600}.ps-home-grid__title a{color:var(--semantic-text-primary,#0e0f12);text-decoration:none}.ps-home-grid__title a:hover{text-decoration:underline}.ps-home-grid__count{margin:0 0 .5rem;font-size:var(--primitive-font-size-2,.75rem);color:var(--semantic-text-secondary,#4a4f59)}.ps-home-grid__list{margin:0 0 .75rem;padding-left:1.25rem;list-style:disc}.ps-home-grid__list li{margin-bottom:.25rem}.ps-home-grid__list a{font-size:var(--primitive-font-size-3,.875rem);color:var(--semantic-interactive-link,#3366cc)}.ps-home-grid__more{font-size:var(--primitive-font-size-3,.875rem);color:var(--semantic-interactive-link,#3366cc);text-decoration:none}.ps-home-grid__card--empty{opacity:.75}.ps-home-grid__empty{font-size:var(--primitive-font-size-3,.875rem);color:var(--semantic-text-secondary,#4a4f59);font-style:italic}
```

## Accessibility

Use `<section aria-label="Browse by category">` as the outer wrapper. Each card is an `<article>` with an `<h3>` title (`<h2>` if no `<h1>` above). Badge and child links are native `<a>` elements — no custom keyboard handling needed. Empty-state card uses `ps-home-grid__card--empty` modifier; screen readers read the empty-state message as body text after the heading.

## See Also

- [[guide-component-navigation-bar]]
- [[guide-component-surface]]

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*
