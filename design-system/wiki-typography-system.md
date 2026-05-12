---
schema: foundry-doc-v1
title: "Wiki Typography System"
slug: wiki-typography-system
category: design-system
type: topic
quality: core
status: active
bcsc_class: vendor-public
last_edited: 2026-05-07
editor: pointsav-engineering
cites: []
paired_with: wiki-typography-system.es.md
---

The PointSav wiki typographic system uses IBM Plex Sans for body prose and IBM Plex Mono
for code and technical notation. Both typefaces are released under the SIL Open Font
License 1.1, permitting use, modification, and redistribution without restriction. A
24-agent editorial research pass (2026-05-06) set the heading scale, base size, and
measure; all contrast pairs pass WCAG 2.1 AAA. The system is defined in CSS custom
properties in `dist/tokens.css` and applies uniformly across all three wikis.

## Font Stack

**Body prose:** IBM Plex Sans (400, 500, 600, 700 weights). IBM Plex Sans is a
humanist sans-serif with high legibility at reading sizes and clear differentiation
between commonly confused glyphs (l, 1, I; O, 0).

**Code and technical notation:** IBM Plex Mono (400, 500 weights). A proportionally
designed monospaced companion to IBM Plex Sans. Used for inline `code`, code blocks,
command-line examples, and metadata fields (dates, identifiers).

**Fallback stack:** `-apple-system, BlinkMacSystemFont, Segoe UI, Roboto` for body;
`SFMono-Regular, Consolas, Liberation Mono` for code.

## Delivery

IBM Plex Sans ships a variable font file (`IBM-Plex-Sans-Variable.woff2`) covering the
full weight axis (100–700). A single variable font file replaces multiple static weight
files and runs approximately 60–80 KB for the Latin subset.

The wiki self-hosts fonts from the deployment's `/static/fonts/` directory. No requests
leave the deployment to external font CDNs. The `latin-ext` subset adds accented
characters for bilingual (English/Spanish) content at approximately 10–20% additional
file size.

`font-display: swap` is set for all wiki typefaces. The fallback system font renders
immediately; IBM Plex swaps in when loaded, appropriate for a text-heavy wiki where
immediate readability outweighs strict layout stability.

## Type Scale

| Level | Token | rem | px (17px base) | Use |
|---|---|---|---|---|
| H1 | `--ps-wiki-text-h1` | 2.25rem | 38px | Article title |
| H2 | `--ps-wiki-text-h2` | 1.75rem | 29.75px | Major section |
| H3 | `--ps-wiki-text-h3` | 1.375rem | 23.375px | Subsection |
| H4 | `--ps-wiki-text-h4` | 1.125rem | 19.125px | Minor heading |
| Body | `--ps-wiki-font-size-base` | 1.0625rem | 17px | Running prose |

The base font size is 106.25% of the root (17px). The 17px base produces the correct
line length at the 65ch measure on desktop; the browser default of 16px produces
slightly short lines at this measure.

## Reading Measure and Line Height

| Property | Value | Token |
|---|---|---|
| Measure (max-width) | 65ch | `--ps-wiki-measure` |
| Body line-height | 1.6 | `--ps-wiki-line-height-body` |
| H1 line-height | 1.22 | (inline) |

65 characters per line is the typographic optimum for sustained reading. The 1.6
line-height at 17px gives 27.2px leading, matching the spacing rhythm of Wikipedia's
body text.

## CSS Tokens

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

## See Also

- [[wiki-dark-mode]]
- [[wiki-component-library]]
- [[design-typography]]
