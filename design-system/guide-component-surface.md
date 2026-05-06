---
schema: foundry-doc-v1
title: "Component Guide — Surface"
slug: guide-component-surface
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

A container that groups related content. Three elevation levels — subtle, base, elevated — communicate visual hierarchy without coupling to specific use cases.

## Technical Recipe

### HTML

```html
<section class="ps-surface ps-surface--{{variant}}">{{children}}</section>
```

### CSS

```css
.ps-surface{padding:var(--ps-space-6,24px);border-radius:var(--ps-corner-3,8px)}.ps-surface--subtle{background-color:var(--ps-surface-subtle,#f5f6f8);border:1px solid var(--ps-border-subtle,#e6e8ec)}.ps-surface--base{background-color:var(--ps-surface-base,#fff);border:1px solid var(--ps-border-subtle,#e6e8ec)}.ps-surface--elevated{background-color:var(--ps-surface-elevated,#fff);box-shadow:0 4px 16px rgba(14,15,18,.08),0 1px 4px rgba(14,15,18,.04)}
```

## Accessibility

A surface is a container — it has no implicit role. Add `role="region"` with `aria-labelledby` when the surface contains a labelled section. Modal surfaces add `role="dialog"` `aria-modal="true"`.

## See Also

- [[design-color]]
- [[guide-component-notification]]

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*
