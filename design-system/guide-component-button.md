---
schema: foundry-doc-v1
title: "Component Guide — Button"
slug: guide-component-button
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

A trigger that initiates an action. Five variants — primary, secondary, ghost, critical, link — each with its own emphasis and use context.

## Technical Recipe

### HTML

```html
<button type="button" class="ps-btn ps-btn--{{variant}}">{{label}}</button>
```

### CSS

```css
/* Button — base + variant rules. CSS custom properties resolve from the active theme; component never hardcodes color. */
.ps-btn{display:inline-flex;align-items:center;justify-content:center;gap:var(--ps-space-3,8px);min-height:2.5rem;padding:0 var(--ps-space-5,16px);border:0;border-radius:var(--ps-corner-2,4px);font-family:inherit;font-size:.875rem;font-weight:600;line-height:1.43;cursor:pointer;transition:background-color var(--ps-speed-2,120ms) var(--ps-ease-utility,cubic-bezier(.2,0,.4,1));white-space:nowrap}
.ps-btn:focus-visible{outline:2px solid var(--ps-focus-ring,#234ed8);outline-offset:2px}
.ps-btn[disabled]{cursor:not-allowed;background-color:var(--ps-interactive-primary-disabled,#e6e8ec);color:var(--ps-ink-disabled,#878d99)}
.ps-btn--primary{background-color:var(--ps-interactive-primary,#234ed8);color:var(--ps-ink-on-interactive,#fff)}
.ps-btn--primary:hover{background-color:var(--ps-interactive-primary-hover,#173ab1)}
.ps-btn--primary:active{background-color:var(--ps-interactive-primary-pressed,#0c2785)}
.ps-btn--secondary{background-color:var(--ps-interactive-secondary,#33373e);color:var(--ps-ink-on-interactive,#fff)}
.ps-btn--secondary:hover{background-color:var(--ps-interactive-secondary-hover,#1f2125)}
.ps-btn--secondary:active{background-color:var(--ps-interactive-secondary-pressed,#0e0f12)}
.ps-btn--ghost{background-color:transparent;color:var(--ps-ink-primary,#0e0f12)}
.ps-btn--ghost:hover{background-color:var(--ps-interactive-ghost-hover,#f5f6f8)}
.ps-btn--ghost:active{background-color:var(--ps-interactive-ghost-pressed,#e6e8ec)}
.ps-btn--critical{background-color:var(--ps-interactive-critical,#d24747);color:var(--ps-ink-on-critical,#fff)}
.ps-btn--critical:hover{background-color:var(--ps-interactive-critical-hover,#a52323)}
.ps-btn--critical:active{background-color:var(--ps-interactive-critical-pressed,#7d1414)}
```

## Accessibility

Native `<button type="button">` carries the button role implicitly. Set `aria-label` when the visible label is not descriptive (icon-only buttons). Critical variants must be paired with a confirmation step (modal, dialog, or undo affordance) — destructive actions one click away from completion are an anti-pattern.

## See Also

- [[design-color]]
- [[design-motion]]
- [[guide-component-link]]

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*
