---
schema: foundry-doc-v1
title: "Component Guide — Text Input"
slug: guide-component-input-text
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

Single-line text entry with label, helper text, and error state.

## Technical Recipe

### HTML

```html
<div class="ps-field">
  <label class="ps-field__label" for="{{id}}">{{label}}</label>
  <input type="text" id="{{id}}" class="ps-input" placeholder="{{placeholder}}" />
  <span class="ps-field__helper">{{helper}}</span>
</div>
```

### CSS

```css
.ps-field{display:flex;flex-direction:column;gap:var(--ps-space-2,4px)}.ps-field__label{font-size:.75rem;font-weight:600;color:var(--ps-ink-secondary,#4a4f59)}.ps-input{height:2.5rem;padding:0 var(--ps-space-4,12px);border:1px solid var(--ps-border-strong,#aab0bb);border-radius:var(--ps-corner-2,4px);background-color:var(--ps-surface-base,#fff);color:var(--ps-ink-primary,#0e0f12);font:inherit;transition:border-color var(--ps-speed-2,120ms) var(--ps-ease-utility,cubic-bezier(.2,0,.4,1))}.ps-input:focus-visible{outline:2px solid var(--ps-focus-ring,#234ed8);outline-offset:0;border-color:var(--ps-focus-ring,#234ed8)}.ps-input::placeholder{color:var(--ps-ink-placeholder,#878d99)}.ps-input[disabled]{background-color:var(--ps-surface-subtle,#f5f6f8);color:var(--ps-ink-disabled,#878d99);cursor:not-allowed}.ps-field--error .ps-input{border-color:var(--ps-support-critical,#a52323)}.ps-field--error .ps-field__helper{color:var(--ps-support-critical,#a52323)}.ps-field__helper{font-size:.75rem;color:var(--ps-ink-secondary,#4a4f59)}
```

## Accessibility

The label is bound to the input via `for`/`id`. Error messages set `aria-describedby` on the input and `aria-live="polite"` on the helper to announce changes. Required fields use `aria-required="true"` — do not rely on the visual asterisk alone.

## See Also

- [[guide-component-select]]
- [[guide-component-checkbox]]

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*
