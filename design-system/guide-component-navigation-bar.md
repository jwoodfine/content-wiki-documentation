---
schema: foundry-doc-v1
title: "Component Guide — Navigation Bar"
slug: guide-component-navigation-bar
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

Page-level navigation header. Logo, primary nav, optional actions, optional account menu.

## Technical Recipe

### HTML

```html
<header class="ps-nav">
  <a class="ps-nav__logo" href="/">{{brand}}</a>
  <nav class="ps-nav__primary" aria-label="Primary">
    <ul class="ps-nav__list">
      {{#each items}}<li><a class="ps-nav__link" href="{{href}}">{{label}}</a></li>{{/each}}
    </ul>
  </nav>
  <div class="ps-nav__actions">{{actions}}</div>
</header>
```

### CSS

```css
.ps-nav{display:flex;align-items:center;gap:var(--ps-space-7,32px);padding:0 var(--ps-space-6,24px);height:3.5rem;background-color:var(--ps-surface-base,#fff);border-bottom:1px solid var(--ps-border-subtle,#e6e8ec)}.ps-nav__logo{font-weight:700;font-size:1.125rem;color:var(--ps-ink-primary,#0e0f12);text-decoration:none}.ps-nav__primary{flex:1}.ps-nav__list{display:flex;gap:var(--ps-space-6,24px);list-style:none;padding:0;margin:0}.ps-nav__link{color:var(--ps-ink-secondary,#4a4f59);text-decoration:none;font-weight:500}.ps-nav__link:hover{color:var(--ps-ink-primary,#0e0f12)}.ps-nav__link[aria-current='page']{color:var(--ps-interactive-primary,#234ed8)}.ps-nav__link:focus-visible{outline:2px solid var(--ps-focus-ring,#234ed8);outline-offset:2px;border-radius:2px}.ps-nav__actions{display:flex;align-items:center;gap:var(--ps-space-3,8px)}
```

## Accessibility

Mark the active page with `aria-current="page"`. The `<nav>` element with `aria-label="Primary"` is the canonical landmark for top-level navigation. Mobile collapse pattern (drawer) is subsequent-milestone work.

## See Also

- [[guide-component-tab]]
- [[guide-component-breadcrumb]]

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*
