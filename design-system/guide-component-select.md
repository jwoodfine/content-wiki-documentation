---
schema: foundry-doc-v1
title: "Component Guide — Select"
slug: guide-component-select
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

Single-choice picker from a known list. Native `<select>` element for keyboard and screen-reader behaviour out of the box.

## Technical Recipe

### HTML

```html
<div class="ps-field">
  <label class="ps-field__label" for="{{id}}">{{label}}</label>
  <select id="{{id}}" class="ps-select">
    <option value="">Choose…</option>
    <option>Option one</option>
    <option>Option two</option>
    <option>Option three</option>
  </select>
</div>
```

### CSS

```css
.ps-select{appearance:none;-webkit-appearance:none;height:2.5rem;padding:0 var(--ps-space-7,32px) 0 var(--ps-space-4,12px);border:1px solid var(--ps-border-strong,#aab0bb);border-radius:var(--ps-corner-2,4px);background-color:var(--ps-surface-base,#fff);background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='6' viewBox='0 0 10 6'%3E%3Cpath fill='%234a4f59' d='M0 0l5 6 5-6z'/%3E%3C/svg%3E");background-repeat:no-repeat;background-position:right var(--ps-space-4,12px) center;color:var(--ps-ink-primary,#0e0f12);font:inherit}.ps-select:focus-visible{outline:2px solid var(--ps-focus-ring,#234ed8);outline-offset:0;border-color:var(--ps-focus-ring,#234ed8)}.ps-select[disabled]{background-color:var(--ps-surface-subtle,#f5f6f8);color:var(--ps-ink-disabled,#878d99);cursor:not-allowed}
```

## Accessibility

Native `<select>` handles keyboard (arrow keys, Home/End, type-ahead) and screen-reader announcement automatically. Bind label via `for`/`id`. Use `aria-required` when the field is required.

## See Also

- [[guide-component-input-text]]
- [[guide-component-checkbox]]

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*
