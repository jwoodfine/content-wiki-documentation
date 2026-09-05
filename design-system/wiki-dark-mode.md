---
schema: foundry-doc-v1
title: "Wiki dark mode"
slug: wiki-dark-mode
short_description: "Light and dark colour schemes for the PointSav wiki, driven by semantic-token overrides on a data-theme attribute, with theme persistence via localStorage."
category: design-system
type: topic
content_type: topic
index_group: wiki-surface-design
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-25
editor: pointsav-engineering
paired_with: wiki-dark-mode.es.md
---

The [[app-mediakit-knowledge|PointSav wiki]] supports light and dark colour schemes using [[design-system-substrate|semantic tokens]] from the platform design system. Dark mode reduces eye strain in low-light environments and is preferred by a significant proportion of readers. This article describes the implementation: how the theme is set, persisted across sessions, and toggled, together with the full colour palette for each mode.

---

## How it works

Dark mode is controlled by a `data-theme="dark"` attribute on the `<html>` element. The wiki's CSS uses this attribute as a selector override:

```css
/* Light (default) — defined on :root */
:root {
  --k-surface: #ffffff;
  --k-ink: #202122;
  /* ... */
}

/* Dark — overrides semantic tokens only */
:root[data-theme="dark"] {
  --k-surface: #101418;
  --k-ink: #e7e9ea;
  /* ... */
}
```

Only semantic tokens (surfaces, ink, borders, status colours) change between modes. Primitive tokens — the raw colour palette — remain unchanged. Adding dark mode support to a new component requires only that the component uses semantic tokens; no per-component `[data-theme="dark"]` selectors are needed.

---

## Initialisation

Theme preference is stored in `localStorage` under the key `k-theme`. The chrome script resolves the initial theme by checking that stored value first and falling back to the operating system's `prefers-color-scheme` only when nothing has been stored, then applies it by setting `data-theme` on the document root and updating the toggle button's `aria-pressed` state and label. An integrator embedding this engine is expected to also inline an equivalent pre-paint snippet in `<head>` so the correct theme applies before first paint, rather than flashing the wrong one and correcting after load.

An explicit user choice stored in `localStorage` overrides the operating-system preference (`prefers-color-scheme`). If no choice has been stored, the OS preference is honoured.

On mobile, `prefers-color-scheme` is the primary trigger — most mobile readers rely on their OS setting and never encounter the manual toggle. The toggle component is the progressive-enhancement layer for readers who want to override. The `<meta name="color-scheme" content="light dark">` declaration in the `<head>` prevents the browser from drawing a white flash before the inline script reads `localStorage`.

---

## Toggle component

The theme control (`.k-control--theme`) uses `aria-pressed` and updates `aria-label` to describe both the action available and the current state — "Switch to dark theme (current: light)" and its inverse — rather than a bare action-only label. On click, the toggle sets `data-theme` on the document root and writes the new value to `localStorage`.

---

## Colour palette

### Light mode

| Token | Value | Use |
|---|---|---|
| `--k-surface` | #ffffff | Page background |
| `--k-ink` | #202122 | Body text |
| `--k-ink-secondary` | (defined alongside `--k-ink`) | Secondary text, metadata |
| `--k-link` | (defined alongside `--k-ink`) | Hyperlinks |

### Dark mode

| Token | Value | Use |
|---|---|---|
| `--k-surface` | #101418 | Page background |
| `--k-surface-sunken` | #171c22 | Site notice, footer |
| `--k-surface-raised` | #1b2027 | Mobile drawer |
| `--k-ink` | #e7e9ea | Body text |
| `--k-ink-secondary` | #a6abb1 | Secondary text |
| `--k-border` | #3a4149 | Borders |
| `--k-link` | #7aa6f0 | Hyperlinks |
| `--k-link-hover` | #a3c1f5 | Hyperlink hover state |
| `--k-code-block-bg` | #2b303b | Code block background |

Code blocks stay dark in dark mode, with syntax highlighting switching to its own dark palette rather than following the same tokens as prose text. Two instance-specific overrides exist for the `documentation` and `projects`/`corporate` deployments, adjusting the accent color while the rest of the dark palette stays shared.

### Wiki surface aliases

The wiki CSS names its semantic surfaces directly rather than through a
separate short-form alias layer — `--k-surface`, `--k-ink`, `--k-link`, and
the rest are the names components reference. There is no second `--color-*`
naming tier over them.

---

## See also

- [[theming-via-semantic-tokens]] — the concept background for this article: why theming is semantic-token substitution, not a parallel stylesheet, and how the same pattern appears in Carbon, Material 3, and Radix
- [[wiki-component-library]] — the nine components that consume these dark-mode token overrides
- [[wiki-typography-system]] — the type stack that pairs with these colour settings
- [[design-system-substrate]] — the token vault where semantic token values are defined and versioned
