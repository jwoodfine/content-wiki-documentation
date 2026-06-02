---
schema: foundry-doc-v1
title: "Wiki dark mode"
slug: wiki-dark-mode
short_description: "Light and dark colour schemes for the PointSav wiki, with WCAG-verified palettes and theme-persistence via localStorage."
category: design-system
type: topic
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-25
editor: pointsav-engineering
paired_with: wiki-dark-mode.es.md
---

# Wiki dark mode

The [[app-mediakit-knowledge|PointSav wiki]] supports light and dark colour schemes using [[design-system-substrate|semantic tokens]] from the platform design system. Dark mode reduces eye strain in low-light environments and is preferred by a significant proportion of readers. This article describes the implementation: how the theme is set, persisted across sessions, and toggled, together with the full colour palette for each mode.

---

## How it works

Dark mode is controlled by a `data-theme="dark"` attribute on the `<html>` element. The wiki's CSS uses this attribute as a selector override:

```css
/* Light (default) — defined on :root */
:root {
  --ps-surface-base: #ffffff;
  --ps-ink-primary: #0e0f12;
  /* ... */
}

/* Dark — overrides semantic tokens only */
[data-theme="dark"] {
  --ps-surface-base: #1f2125;
  --ps-ink-primary: #f5f6f8;
  /* ... */
}
```

Only semantic tokens (surfaces, ink, borders, status colours) change between modes. Primitive tokens — the raw colour palette — remain unchanged. Adding dark mode support to a new component requires only that the component uses semantic tokens; no per-component `[data-theme="dark"]` selectors are needed.

---

## Initialisation

Theme preference is stored in `localStorage` under the key `ps-theme`. On each page load, an inline script in `<head>` reads this value and sets `data-theme` before the browser renders any content. This prevents a flash of the wrong theme that would otherwise occur if the script ran after the initial paint:

```html
<head>
  <script>
    (function() {
      var stored = localStorage.getItem('ps-theme');
      var prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      if (stored === 'dark' || (!stored && prefersDark)) {
        document.documentElement.dataset.theme = 'dark';
      }
    })();
  </script>
  <link rel="stylesheet" href="/static/tokens.css">
</head>
```

An explicit user choice stored in `localStorage` overrides the operating-system preference (`prefers-color-scheme`). If no choice has been stored, the OS preference is honoured.

On mobile, `prefers-color-scheme` is the primary trigger — most mobile readers rely on their OS setting and never encounter the manual toggle. The toggle component is the progressive-enhancement layer for readers who want to override. The `<meta name="color-scheme" content="light dark">` declaration in the `<head>` prevents the browser from drawing a white flash before the inline script reads `localStorage`.

---

## Toggle component

The `wiki-dark-mode-toggle` component uses `aria-pressed` and updates `aria-label` to describe the action available, not the current state:

- In light mode: label = "Switch to dark mode"
- In dark mode: label = "Switch to light mode"

On click, the toggle sets `document.documentElement.dataset.theme` and writes the new value to `localStorage`.

---

## Colour palette

### Light mode

| Token | Value | Use |
|---|---|---|
| `--ps-surface-base` | #ffffff | Page background |
| `--ps-surface-subtle` | #f5f6f8 | Sidebar, code surface |
| `--ps-ink-primary` | #0e0f12 | Body text |
| `--ps-ink-secondary` | #4a4f59 | Secondary text, metadata |
| `--ps-wiki-link` | #234ed8 | Hyperlinks |
| `--ps-wiki-redlink` | #a52323 | Non-existent article links |
| `--ps-wiki-code-keyword` | #7c3aed | Code syntax keywords |

### Dark mode

| Token | Value | Use | WCAG contrast vs background |
|---|---|---|---|
| `--ps-surface-base` | #1f2125 | Page background | — |
| `--ps-surface-code` | #151618 | Code block background | — |
| `--ps-ink-primary` | #f5f6f8 | Body text | 14.5:1 (AAA) |
| `--ps-ink-secondary` | #aab0bb | Secondary text | 6.2:1 (AAA) |
| `--ps-wiki-link` | #6ab0f5 | Hyperlinks | 8.47:1 vs page (AAA) |
| `--ps-wiki-redlink` | #f56565 | Non-existent article links | 6.42:1 vs page (AA+) |
| `--ps-wiki-code-keyword` | #c792ea | Code syntax keywords | 7.85:1 vs code surface (AAA) |

All dark mode colour pairs pass WCAG 2.1 Level AAA, verified 2026-05-06.

### Wiki surface aliases

The wiki CSS uses short-form aliases that map to the semantic tokens:

```css
--color-surface-page:    var(--ps-surface-base);
--color-surface-sidebar: var(--ps-surface-subtle);
--color-surface-code:    var(--ps-surface-code);
--color-text-primary:    var(--ps-ink-primary);
--color-text-secondary:  var(--ps-ink-secondary);
--color-text-link:       var(--ps-wiki-link);
--color-text-redlink:    var(--ps-wiki-redlink);
--color-border-subtle:   var(--ps-border-subtle);
--color-accent-primary:  var(--ps-interactive-primary);
--color-code-keyword:    var(--ps-wiki-code-keyword);
```

---

## See also

- [[wiki-component-library]] — the nine components that consume these dark-mode token overrides
- [[wiki-typography-system]] — the type stack that pairs with these colour settings
- [[design-system-substrate]] — the token vault where semantic token values are defined and versioned
