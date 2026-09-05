---
schema: foundry-doc-v1
title: "Wiki typography system"
slug: wiki-typography-system
short_description: "The Inter and Source Serif 4 type stack, heading scale, and spacing tokens governing every wiki article page across the PointSav knowledge platform."
category: design-system
type: topic
content_type: topic
index_group: wiki-surface-design
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-06-01
editor: pointsav-engineering
paired_with: wiki-typography-system.es.md
---

The [[app-mediakit-knowledge|PointSav wiki]]'s typographic system uses Source Serif 4 for the article title and section headings, Inter for body reading prose, and a system-provided monospace stack for code and technical notation, built on [[design-system-substrate|the platform token system]] following the [[design-primitive-vocabulary|primitive vocabulary conventions]]. This article explains the font choices, the heading scale, the spacing tokens, and how the system achieves broad linguistic coverage for bilingual (English/Spanish) content.

---

## Font stack

**Article title and section headings:** Source Serif 4 (variable font). Source Serif 4 is Adobe's open-source text typeface, published under the SIL Open Font License 1.1 (SIL OFL 1.1), which permits use, modification, and redistribution without restriction. Its slightly higher stroke contrast than a sans-serif face gives the title and headings a distinct register from the running text beneath them.

**Body reading prose:** Inter (variable font). Inter is a community open-source typeface designed by Rasmus Andersson, published under SIL OFL 1.1. It is a neo-grotesque designed specifically for screen readability, with high legibility at small sizes and clear differentiation between commonly confused glyphs (l, 1, I; O, 0). It carries no corporate brand association and is the modern UI workhorse across the design-system field.

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

| Level | Token | rem | px | Use |
|---|---|---|---|---|
| H1 | `--k-title-fs` | 2.125 rem | 34 px | Article title |
| H2 | `--k-h2-fs` | 1.5 rem | 24 px | Major section |
| H3 | `--k-h3-fs` | 1.2 rem | 19 px | Subsection |
| H4 | (unnamed, set directly) | 1.05 rem | 16.8 px | Minor heading |
| Body | `--k-prose-fs` | 1 rem | 16 px | Running prose |

Base body size is the 16 px browser default. Headings render in Source Serif 4 (`--k-title-font`); body prose renders in Inter (`--k-prose-font`).

---

## Reading measure and line height

| Property | Value | Token |
|---|---|---|
| Measure (max-width) | 44 rem (~72 ch) | `--k-prose-measure` |
| Body line-height | 1.6 | `--k-prose-leading` |

A wide measure keeps the reading column full-width in the Wikipedia-style layout rather than narrowing it artificially. A 1.6 line-height at 16 px base gives 25.6 px leading.

---

## CSS tokens

All values are CSS custom properties defined in the engine's token stylesheet:

```css
--k-font-sans:  'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;
--k-font-serif: 'Source Serif 4', Georgia, 'Times New Roman', serif;
--k-font-mono:  ui-monospace, 'SFMono-Regular', 'Menlo', 'Consolas', monospace;

--k-prose-font:  var(--k-font-sans);
--k-title-font:  var(--k-font-serif);
--k-code-font:   var(--k-font-mono);

--k-prose-fs:      1rem;      /* 16px body */
--k-title-fs:      2.125rem;  /* 34px h1 */
--k-h2-fs:         1.5rem;    /* 24px */
--k-h3-fs:         1.2rem;    /* 19px */
--k-prose-leading: 1.6;
--k-prose-measure: 44rem;     /* ~72ch */
```

---

## See also

- [[wiki-component-library]] — the nine components that use this type stack
- [[wiki-dark-mode]] — the colour scheme system that pairs with these typographic tokens
- [[design-system-substrate]] — the token vault where font stack and scale variables are defined
