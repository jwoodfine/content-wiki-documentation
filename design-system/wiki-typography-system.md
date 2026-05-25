---
schema: foundry-doc-v1
title: "Wiki typography system"
slug: wiki-typography-system
short_description: "IBM Plex Sans and IBM Plex Mono type stack, heading scale, and spacing tokens for the PointSav wiki."
category: design-system
type: topic
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-25
editor: pointsav-engineering
paired_with: wiki-typography-system.es.md
---

# Wiki typography system

The PointSav wiki typographic system uses IBM Plex Sans for body prose and IBM Plex Mono for code and technical notation. This article explains the font choice, the heading scale, the spacing tokens, and how the system achieves broad linguistic coverage for bilingual (English/Spanish) content.

---

## Font stack

**Body prose:** IBM Plex Sans (weights 400, 500, 600, 700). IBM Plex Sans is IBM's open-source typeface released under the SIL Open Font License 1.1 (SIL OFL 1.1), which permits use, modification, and redistribution without restriction. The typeface is a humanist sans-serif with high legibility at reading sizes and clear differentiation between commonly confused glyphs (l, 1, I; O, 0).

**Code and technical notation:** IBM Plex Mono (weights 400, 500). A proportionally designed monospaced companion to IBM Plex Sans. Used for inline `code`, code blocks, command-line examples, and metadata fields (dates, identifiers).

**Fallback stack:** -apple-system, BlinkMacSystemFont, Segoe UI, Roboto (system UI sans-serif chain) for body; SFMono-Regular, Consolas, Liberation Mono for code.

---

## Delivery

IBM Plex Sans and IBM Plex Mono are available through Google Fonts, the npm package `@ibm/plex`, and direct download from the IBM Plex GitHub repository.

IBM Plex Sans ships a variable font file (`IBM-Plex-Sans-Variable.woff2`) covering the full weight axis (100–700). A single variable font file replaces four separate static-weight WOFF2 files and runs approximately 60–80 KB for the Latin subset — smaller than four separate files combined.

**Self-hosting** from the deployment's `/static/fonts/` directory is the preferred delivery method. No requests reach external font CDNs, which protects reader privacy. The Latin subset is the minimum; the latin-ext subset, which adds accented characters required for Spanish bilingual content, adds approximately 10–20% to file size.

**`font-display: swap`** prevents invisible-text flash during font load. The fallback system font renders immediately; IBM Plex swaps in when the download completes. For a text-heavy wiki, immediate readability takes precedence over font-swap layout shift.

---

## Type scale

| Level | Token | rem | px (17 px base) | Use |
|---|---|---|---|---|
| H1 | `--ps-wiki-text-h1` | 2.25 rem | 38 px | Article title |
| H2 | `--ps-wiki-text-h2` | 1.75 rem | 29.75 px | Major section |
| H3 | `--ps-wiki-text-h3` | 1.375 rem | 23.375 px | Subsection |
| H4 | `--ps-wiki-text-h4` | 1.125 rem | 19.125 px | Minor heading |
| Body | `--ps-wiki-font-size-base` | 1.0625 rem | 17 px | Running prose |

**Base:** 106.25% root font size (17 px) — slightly larger than the 16 px browser default for improved readability at a 65-character measure on desktop.

---

## Reading measure and line height

| Property | Value | Token |
|---|---|---|
| Measure (max-width) | 65 ch | `--ps-wiki-measure` |
| Body line-height | 1.6 | `--ps-wiki-line-height-body` |

65 characters per line is the typographic optimum for sustained reading. A 1.6 line-height at 17 px base gives 27.2 px leading, matching the spacing rhythm of Wikipedia's body text.

---

## CSS tokens

All values are CSS custom properties defined on `:root` in `dist/tokens.css`:

```css
--ps-wiki-font-body: 'IBM Plex Sans', -apple-system, …;
--ps-wiki-font-mono: 'IBM Plex Mono', 'SFMono-Regular', …;
--ps-wiki-font-size-base:   1.0625rem;
--ps-wiki-line-height-body: 1.6;
--ps-wiki-measure:          65ch;
--ps-wiki-text-h1: 2.25rem;
--ps-wiki-text-h2: 1.75rem;
--ps-wiki-text-h3: 1.375rem;
--ps-wiki-text-h4: 1.125rem;

/* Short-form aliases used by wiki templates */
--font-sans:    var(--ps-wiki-font-body);
--font-mono:    var(--ps-wiki-font-mono);
--leading-body: 1.6;
--measure:      65ch;
--text-h1:      var(--ps-wiki-text-h1);
--text-h2:      var(--ps-wiki-text-h2);
--text-h3:      var(--ps-wiki-text-h3);
--text-h4:      var(--ps-wiki-text-h4);
```

---

## See Also

- [[wiki-component-library]]
- [[wiki-dark-mode]]
- [[design-system-substrate]]
