---
schema: foundry-doc-v1
title: "Design System — Typography"
slug: design-typography
category: design-system
type: reference
quality: complete
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-06
editor: pointsav-engineering
paired_with: design-typography.es.md
cites:
  - wcag-22
  - dtcg-spec
---

Two type scales — Utility and Display — split the typographic load between functional UI text and expressive surfaces.

## The two scales

| Scale | Use for | Sizes |
|---|---|---|
| **Utility** | UI text — body, labels, captions, table cells, button labels | 4 steps (12/14/16/16-bold) |
| **Display** | Expressive type — sub-headings, section headings, page titles, hero | 4 steps (20/24/32/42) |

The split is structural, not decorative. Utility text uses optimised letter-spacing for screen-readability at small sizes; Display text uses negative letter-spacing for a tighter, more confident heading rhythm. Mixing scales (Utility-3 used as a heading, Display-1 used for a button label) breaks the system's visual hierarchy.

## Font stack

The substrate ships Inter as the canonical sans-serif, with a system-stack fallback chain:

```
'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif
```

Inter is a modern, open-source workhorse face (SIL OFL 1.1), optimised for UI rendering at small sizes. The system stack fallback ensures the substrate is fully functional even if the Inter binary is not loaded — degradation is graceful.

A tenant theme can substitute any font family at the primitive layer. Common substitutions:

- IBM Plex Sans (open-source, SIL OFL 1.1)
- Source Sans 3 (Adobe, open-source)
- Public Sans (USWDS, public domain)
- A tenant's own brand face

Self-hosting the font binary is the customer's responsibility; the substrate references the family by name.

## The scale

### Utility

| Token | Size / Line / Weight | Use for |
|---|---|---|
| `typography.utility-1` | 12 / 16 / 400 | Caption, label, table cell |
| `typography.utility-2` | 14 / 20 / 400 | Secondary body, helper text |
| `typography.utility-3` | 16 / 24 / 400 | Primary body floor |
| `typography.utility-4` | 16 / 24 / 600 | UI heading, button label |

### Display

| Token | Size / Line / Weight | Use for |
|---|---|---|
| `typography.display-1` | 20 / 28 / 500 | Sub-heading |
| `typography.display-2` | 24 / 32 / 500 | Section heading |
| `typography.display-3` | 32 / 40 / 400 | Page title |
| `typography.display-4` | 42 / 50 / 300 | Hero / landing |

## Heading hierarchy

| HTML | Token |
|---|---|
| `<h1>` | `display-3` |
| `<h2>` | `display-2` |
| `<h3>` | `display-1` |
| `<h4>` | `utility-4` |
| Body `<p>` | `utility-3` |
| `<small>`, helper, caption | `utility-2` |

A heading-level skip (h1 → h3 with no h2 between) breaks accessibility — screen readers rely on the hierarchy to navigate. The substrate enforces this in subsequent-milestone audit work.

## Brand voice

The substrate's voice rules live in the active theme's `voice` block. PointSav-brand:

- **Confident** — no hedging, no apology
- **Direct** — action verbs first, single-clause sentences where possible
- **Professional** — Bloomberg article standard, no marketing register

Banned vocabulary applies to all body and heading copy.

## See Also

- [[design-color]]
- [[design-spacing]]
- [[design-philosophy]]

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*

*Woodfine Capital Projects™, Woodfine Management Corp™, PointSav Digital Systems™, Totebox Orchestration™, and Totebox Archive™ are trademarks of Woodfine Capital Projects Inc., used in Canada, the United States, Latin America, and Europe. All other trademarks are the property of their respective owners.*
