---
schema: foundry-doc-v1
title: "Component Guide — Checkbox"
slug: guide-component-checkbox
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

Boolean choice. Use when each option is independent of the others.

## Technical Recipe

### HTML

```html
<label class="ps-check">
  <input type="checkbox" class="ps-check__input" id="{{id}}">
  <span class="ps-check__box" aria-hidden="true"></span>
  <span class="ps-check__label">{{label}}</span>
</label>
```

### CSS

```css
.ps-check{display:inline-flex;align-items:center;gap:var(--ps-space-3,8px);cursor:pointer}.ps-check__input{position:absolute;opacity:0;width:1px;height:1px;clip:rect(0,0,0,0)}.ps-check__box{display:inline-flex;align-items:center;justify-content:center;width:1.125rem;height:1.125rem;border:1px solid var(--ps-border-strong,#aab0bb);border-radius:var(--ps-corner-1,2px);background-color:var(--ps-surface-base,#fff);transition:background-color var(--ps-speed-2,120ms) var(--ps-ease-utility,cubic-bezier(.2,0,.4,1))}.ps-check__input:checked~.ps-check__box{background-color:var(--ps-interactive-primary,#234ed8);border-color:var(--ps-interactive-primary,#234ed8)}.ps-check__input:checked~.ps-check__box::after{content:'';width:.5rem;height:.25rem;border-left:2px solid var(--ps-ink-on-interactive,#fff);border-bottom:2px solid var(--ps-ink-on-interactive,#fff);transform:rotate(-45deg) translate(1px,-1px)}.ps-check__input:focus-visible~.ps-check__box{outline:2px solid var(--ps-focus-ring,#234ed8);outline-offset:2px}.ps-check__label{font-size:.875rem;color:var(--ps-ink-primary,#0e0f12)}
```

## Accessibility

The hidden native `<input type="checkbox">` drives keyboard and screen-reader behaviour. The visual `<span class="ps-check__box">` is decorative (`aria-hidden`). Click target is the entire `<label>`, which works for both mouse and touch.

## See Also

- [[guide-component-switch]]
- [[guide-component-input-text]]

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*
