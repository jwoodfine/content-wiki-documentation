---
schema: foundry-doc-v1
title: "Component Guide — Link"
slug: guide-component-link
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

A navigation primitive — moves the user to a destination without state change.

## Technical Recipe

### HTML

```html
<a class="ps-link" href="{{href}}">{{label}}</a>
```

### CSS

```css
.ps-link{color:var(--ps-interactive-primary,#234ed8);text-decoration:underline;text-underline-offset:.2em;transition:color var(--ps-speed-1,70ms) var(--ps-ease-utility,cubic-bezier(.2,0,.4,1))}.ps-link:hover{color:var(--ps-interactive-primary-hover,#173ab1)}.ps-link:visited{color:var(--ps-interactive-primary-pressed,#0c2785)}.ps-link:focus-visible{outline:2px solid var(--ps-focus-ring,#234ed8);outline-offset:2px;border-radius:2px}
```

## Accessibility

Use semantic `<a>` with `href`. Never use a `<button>` styled as a link or vice versa. Distinguish links from buttons by behaviour: links navigate, buttons act.

## See Also

- [[guide-component-button]]
- [[guide-component-navigation-bar]]

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*
