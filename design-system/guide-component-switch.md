---
schema: foundry-doc-v1
title: "Component Guide — Switch"
slug: guide-component-switch
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

On/off toggle for settings that take effect immediately. Use when the action is reversible and binary.

## Technical Recipe

### HTML

```html
<label class="ps-switch">
  <input type="checkbox" role="switch" class="ps-switch__input" id="{{id}}">
  <span class="ps-switch__track" aria-hidden="true">
    <span class="ps-switch__thumb"></span>
  </span>
  <span class="ps-switch__label">{{label}}</span>
</label>
```

### CSS

```css
.ps-switch{display:inline-flex;align-items:center;gap:var(--ps-space-3,8px);cursor:pointer}.ps-switch__input{position:absolute;opacity:0;width:1px;height:1px;clip:rect(0,0,0,0)}.ps-switch__track{position:relative;display:inline-flex;align-items:center;width:2.25rem;height:1.25rem;background-color:var(--ps-border-strong,#aab0bb);border-radius:999px;transition:background-color var(--ps-speed-2,120ms) var(--ps-ease-utility,cubic-bezier(.2,0,.4,1))}.ps-switch__thumb{position:absolute;left:2px;width:1rem;height:1rem;background-color:var(--ps-surface-base,#fff);border-radius:50%;transition:transform var(--ps-speed-2,120ms) var(--ps-ease-utility,cubic-bezier(.2,0,.4,1))}.ps-switch__input:checked~.ps-switch__track{background-color:var(--ps-interactive-primary,#234ed8)}.ps-switch__input:checked~.ps-switch__track .ps-switch__thumb{transform:translateX(1rem)}.ps-switch__input:focus-visible~.ps-switch__track{outline:2px solid var(--ps-focus-ring,#234ed8);outline-offset:2px}.ps-switch__label{font-size:.875rem;color:var(--ps-ink-primary,#0e0f12)}
```

## Accessibility

Native `<input type="checkbox" role="switch">` announces as a switch (instead of a checkbox) on conformant screen readers. Visual track and thumb are `aria-hidden` decorative. Action takes effect immediately on toggle — pair with a status notification when the change is non-trivial.

## See Also

- [[guide-component-checkbox]]
- [[guide-component-notification]]

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*
