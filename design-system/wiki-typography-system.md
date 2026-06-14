---
schema: foundry-doc-v1
title: "Wiki typography system"
slug: wiki-typography-system
short_description: "Inter and Source Serif 4 type stack, heading scale, and spacing tokens for the PointSav wiki."
category: design-system
type: topic
content_type: topic
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-06-01
editor: pointsav-engineering
paired_with: wiki-typography-system.es.md
---

# Wiki typography system

The [[app-mediakit-knowledge|PointSav wiki]]'s typographic system uses Inter for user interface elements and navigation, Source Serif 4 for body reading prose, and a system-provided monospace stack for code and technical notation, built on [[design-system-substrate|the platform token system]] following the [[design-primitive-vocabulary|primitive vocabulary conventions]]. This article explains the font choices, the heading scale, the spacing tokens, and how the system achieves broad linguistic coverage for bilingual (English/Spanish) content.

---

## Font stack

**User interface and headings:** Inter (variable font, weight axis 100–900). Inter is a community open-source typeface designed by Rasmus Andersson, published under the SIL Open Font License 1.1 (SIL OFL 1.1), which permits use, modification, and redistribution without restriction. Inter is a neo-grotesque designed specifically for screen readability, with high legibility at small sizes and clear differentiation between commonly confused glyphs (l, 1, I; O, 0). It carries no corporate brand association and is the modern UI workhorse across the design-system field.

**Body reading prose:** Source Serif 4 (variable font, weight axis 200–900). Source Serif 4 is Adobe's open-source text typeface, published under the SIL Open Font License 1.1. It provides comfortable reading at a 68-character measure with slightly higher stroke contrast than Inter, which aids eye-tracking across long prose lines.

**Code and technical notation:** System-provided monospace stack — `ui-monospace`, `SFMono-Regular`, `Cascadia Code`, `Consolas`, `Liberation Mono`. No custom font file is loaded for code. The system stack covers all major platforms with zero additional network round-trip. Used for inline `code`, code blocks, command-line examples, and metadata fields (dates, identifiers).

**Fallback chains:** -apple-system, BlinkMacSystemFont, Segoe UI, Roboto (system UI sans-serif) for UI contexts before Inter loads; Georgia, Times New Roman (system serif) for prose contexts before Source Serif 4 loads.

---

## Delivery

Inter and Source Serif 4 are available through Google Fonts and direct download from their respective repositories. Both ship variable font files covering the full weight axis — a single variable file replaces multiple static-weight files, reducing total payload.

- **Inter variable** (`inter-var.woff2`) — Latin subset approximately 100–130 KB; the latin-ext subset, required for Spanish bilingual content, adds approximately 15–20%.
- **Source Serif 4 variable** (`SourceSerif4Variable-Roman.woff2`) — Latin subset approximately 80–100 KB; latin-ext adds approximately 10–20%.

**Self-hosting** from the deployment's `/static/fonts/` directory is the preferred delivery method. No requests reach external font CDNs, which protects reader privacy.

**`font-display: swap`** prevents invisible-text flash during font load. The fallback system font renders immediately; Inter and Source Serif 4 swap in when their downloads complete. For a text-heavy wiki, immediate readability takes precedence over font-swap layout shift.

---

## Type scale

| Level | Token | rem | px (17 px base) | Use |
|---|---|---|---|---|
| H1 | `--ps-wiki-text-h1` | 2.25 rem | 38 px | Article title |
| H2 | `--ps-wiki-text-h2` | 1.75 rem | 29.75 px | Major section |
| H3 | `--ps-wiki-text-h3` | 1.375 rem | 23.375 px | Subsection |
| H4 | `--ps-wiki-text-h4` | 1.125 rem | 19.125 px | Minor heading |
| Body | `--ps-wiki-font-size-base` | 1.0625 rem | 17 px | Running prose |

**Base:** 106.25% root font size (17 px) — slightly larger than the 16 px browser default for improved readability at a 68-character measure on desktop. Headings and navigation labels render in Inter; body prose renders in Source Serif 4.

---

## Reading measure and line height

| Property | Value | Token |
|---|---|---|
| Measure (max-width) | 68 ch | `--ps-wiki-measure` |
| Body line-height | 1.6 | `--ps-wiki-line-height-body` |

68 characters per line is the typographic optimum for sustained reading with a text-weight serifed face. A 1.6 line-height at 17 px base gives 27.2 px leading, matching the spacing rhythm of Wikipedia's body text.

---

## CSS tokens

All values are CSS custom properties defined on `:root` in `dist/tokens.css`:

```css
--ps-wiki-font-ui:    'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
--ps-wiki-font-prose: 'Source Serif 4', 'Georgia', 'Times New Roman', serif;
--ps-wiki-font-mono:  ui-monospace, 'SFMono-Regular', 'Cascadia Code', 'Consolas',
                      'Liberation Mono', monospace;
--ps-wiki-font-size-base:   1.0625rem;
--ps-wiki-line-height-body: 1.6;
--ps-wiki-measure:          68ch;
--ps-wiki-text-h1: 2.25rem;
--ps-wiki-text-h2: 1.75rem;
--ps-wiki-text-h3: 1.375rem;
--ps-wiki-text-h4: 1.125rem;

/* Short-form aliases used by wiki templates */
--font-ui:      var(--ps-wiki-font-ui);
--font-prose:   var(--ps-wiki-font-prose);
--font-mono:    var(--ps-wiki-font-mono);
--leading-body: 1.6;
--measure:      68ch;
--text-h1:      var(--ps-wiki-text-h1);
--text-h2:      var(--ps-wiki-text-h2);
--text-h3:      var(--ps-wiki-text-h3);
--text-h4:      var(--ps-wiki-text-h4);
```

---

## See also

- [[wiki-component-library]] — the nine components that use this type stack
- [[wiki-dark-mode]] — the colour scheme system that pairs with these typographic tokens
- [[design-system-substrate]] — the token vault where font stack and scale variables are defined
