---
schema: foundry-doc-v1
title: "Component Guide — Notification"
slug: guide-component-notification
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

Inline messaging — informational, positive, caution, critical. Toast variant is subsequent-milestone work.

## Technical Recipe

### HTML

```html
<aside class="ps-notif ps-notif--{{variant}}" role="status" aria-live="polite">
  <span class="ps-notif__title">{{title}}</span>
  <p class="ps-notif__body">{{body}}</p>
</aside>
```

### CSS

```css
.ps-notif{padding:var(--ps-space-4,12px) var(--ps-space-5,16px);border-left:4px solid;border-radius:var(--ps-corner-2,4px)}.ps-notif--info{background-color:var(--ps-support-info-bg,#eef3ff);border-color:var(--ps-support-info,#234ed8)}.ps-notif--positive{background-color:var(--ps-support-positive-bg,#e8f6ed);border-color:var(--ps-support-positive,#26823f)}.ps-notif--caution{background-color:var(--ps-support-caution-bg,#fff5e1);border-color:var(--ps-support-caution,#a87514)}.ps-notif--critical{background-color:var(--ps-support-critical-bg,#fceaea);border-color:var(--ps-support-critical,#a52323)}.ps-notif__title{display:block;font-weight:600;margin-bottom:var(--ps-space-2,4px)}.ps-notif__body{margin:0;font-size:.875rem;line-height:1.43}
```

## Accessibility

`role="status"` announces inline (`aria-live="polite"`). Critical notifications use `role="alert"` `aria-live="assertive"` for time-sensitive failures. Notifications never auto-disappear without an undo affordance.

## See Also

- [[guide-component-badge]]
- [[design-color]]

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*
