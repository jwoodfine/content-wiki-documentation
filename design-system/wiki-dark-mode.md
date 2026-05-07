---
schema: foundry-doc-v1
title: "Wiki Dark Mode"
slug: wiki-dark-mode
category: design-system
type: topic
quality: core
status: active
bcsc_class: vendor-public
last_edited: 2026-05-07
editor: pointsav-engineering
cites: []
paired_with: wiki-dark-mode.es.md
---

The PointSav wiki dark mode system provides a fully themed light and dark colour scheme,
controlled by a `data-theme="dark"` attribute on the `<html>` element. It reduces eye
strain in low-light environments and is preferred by a significant proportion of readers.
A 24-agent design research pass (2026-05-06) audited the full colour palette; all dark
mode colour pairs pass WCAG 2.1 AAA. The system shipped as Phase A of the wiki design
system in 2026-05-06.

## How It Works

Only semantic tokens (surfaces, ink, borders, status colours) change between modes.
Primitive tokens — the raw colour palette — remain unchanged in both modes. This means
adding dark mode support to a new component requires only using semantic tokens;
no per-component `[data-theme="dark"]` selectors are needed.

```css
/* Light (default) — defined on :root */
:root {
  --ps-surface-base: #ffffff;
  --ps-ink-primary: #0e0f12;
}

/* Dark — overrides only semantic tokens */
[data-theme="dark"] {
  --ps-surface-base: #1f2125;
  --ps-ink-primary: #f5f6f8;
}
```

## Initialisation

Theme preference is stored in `localStorage` under the key `ps-theme`. An inline script
in `<head>` reads this value before the browser renders any content, preventing the flash
of the wrong theme (FOUT-theme) that would occur if the script ran after paint:

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

Explicit user choice (localStorage) overrides the OS preference (`prefers-color-scheme`).
If no choice has been stored, the OS preference is honoured.

## Toggle Component

The wiki dark mode toggle button is defined in the `wiki-dark-mode-toggle` component
(`dtcg-vault/components/wiki-dark-mode-toggle/recipe.json`). It uses `aria-pressed` and
updates `aria-label` to describe the pending action (not the current state):

- In light mode: label = "Switch to dark mode"
- In dark mode: label = "Switch to light mode"

On click, the toggle sets `document.documentElement.dataset.theme` and writes the new
value to `localStorage`.

## Colour Palette

### Light Mode

| Token | Value | Use |
|---|---|---|
| `--ps-surface-base` | #ffffff | Page background |
| `--ps-surface-subtle` | #f5f6f8 | Sidebar, code surface |
| `--ps-ink-primary` | #0e0f12 | Body text |
| `--ps-ink-secondary` | #4a4f59 | Secondary text, metadata |
| `--ps-wiki-link` | #234ed8 | Hyperlinks |
| `--ps-wiki-redlink` | #a52323 | Redlinks (non-existent articles) |
| `--ps-wiki-code-keyword` | #7c3aed | Code syntax keyword |

### Dark Mode

| Token | Value | Use | WCAG vs background |
|---|---|---|---|
| `--ps-surface-base` | #1f2125 | Page background | — |
| `--ps-surface-code` | #151618 | Code block background | — |
| `--ps-ink-primary` | #f5f6f8 | Body text | 14.5:1 (AAA) |
| `--ps-ink-secondary` | #aab0bb | Secondary text | 6.2:1 (AAA) |
| `--ps-wiki-link` | #6ab0f5 | Hyperlinks | 8.47:1 page / 8.22:1 code (AAA) |
| `--ps-wiki-redlink` | #f56565 | Redlinks | 6.42:1 (AA+) |
| `--ps-wiki-code-keyword` | #c792ea | Code syntax keyword | 7.85:1 vs code surface (AAA) |

All dark mode colour pairs pass WCAG 2.1 AAA, verified 2026-05-06 by hand computation
and automated audit.

### Wiki Surface Aliases

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

## See Also

- [[wiki-typography-system]]
- [[wiki-component-library]]
- [[design-color]]
