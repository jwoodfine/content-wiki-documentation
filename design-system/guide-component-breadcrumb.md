---
schema: foundry-doc-v1
title: "Component Guide — Breadcrumb"
slug: guide-component-breadcrumb
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

Hierarchy trail to the current page. Useful when the user is nested deeper than two levels.

## Technical Recipe

### HTML

```html
<nav class="ps-crumbs" aria-label="Breadcrumb">
  <ol class="ps-crumbs__list">
    {{#each items}}<li class="ps-crumbs__item"><a class="ps-crumbs__link" href="{{href}}">{{label}}</a></li>{{/each}}
    <li class="ps-crumbs__item ps-crumbs__item--current" aria-current="page">{{currentLabel}}</li>
  </ol>
</nav>
```

### CSS

```css
.ps-crumbs__list{display:flex;flex-wrap:wrap;gap:var(--ps-space-2,4px);list-style:none;padding:0;margin:0;font-size:.875rem}.ps-crumbs__item:not(:last-child)::after{content:'/';margin-left:var(--ps-space-2,4px);color:var(--ps-ink-secondary,#4a4f59)}.ps-crumbs__link{color:var(--ps-interactive-primary,#234ed8);text-decoration:none}.ps-crumbs__link:hover{text-decoration:underline}.ps-crumbs__item--current{color:var(--ps-ink-primary,#0e0f12);font-weight:500}
```

## Accessibility

`<nav aria-label="Breadcrumb">` wraps an ordered list. The current page is marked with `aria-current="page"` and is not rendered as a link.

## See Also

- [[guide-component-navigation-bar]]
- [[guide-component-tab]]

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*
