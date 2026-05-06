---
schema: foundry-doc-v1
title: "Component Guide — Tab"
slug: guide-component-tab
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

URL-reflected page-section navigation. Each tab is a separate route; state lives in the URL, not in client memory.

## Technical Recipe

### HTML

```html
<nav class="ps-tabs" aria-label="Page sections">
  <ul class="ps-tabs__list">
    <li class="ps-tabs__item">
      <a class="ps-tabs__link ps-tabs__link--active" aria-current="page" href="#">Usage</a>
    </li>
    <li class="ps-tabs__item">
      <a class="ps-tabs__link" href="#">Style</a>
    </li>
    <li class="ps-tabs__item">
      <a class="ps-tabs__link" href="#">Code</a>
    </li>
    <li class="ps-tabs__item">
      <a class="ps-tabs__link" href="#">Accessibility</a>
    </li>
  </ul>
</nav>
```

### CSS

```css
.ps-tabs{border-bottom:1px solid var(--ps-border-subtle,#e6e8ec)}.ps-tabs__list{display:flex;list-style:none;padding:0;margin:0;gap:var(--ps-space-2,4px)}.ps-tabs__link{display:inline-block;padding:var(--ps-space-3,8px) var(--ps-space-5,16px);text-decoration:none;color:var(--ps-ink-secondary,#4a4f59);border-bottom:2px solid transparent;font-weight:500}.ps-tabs__link:hover{color:var(--ps-ink-primary,#0e0f12)}.ps-tabs__link--active{color:var(--ps-interactive-primary,#234ed8);border-bottom-color:var(--ps-interactive-primary,#234ed8)}.ps-tabs__link:focus-visible{outline:2px solid var(--ps-focus-ring,#234ed8);outline-offset:2px;border-radius:2px}
```

## Accessibility

Each tab is a real `<a href>` link to a real page. `aria-current="page"` marks the active tab. The substrate's tab pattern is URL-reflected — clicking a tab navigates to a separate route, not an in-page state change. This makes deep-linking, back/forward navigation, and sharing canonical.

## See Also

- [[guide-component-navigation-bar]]
- [[guide-component-breadcrumb]]

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*
