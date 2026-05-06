---
schema: foundry-doc-v1
title: "Design System — Color"
slug: design-color
category: design-system
type: reference
quality: complete
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-06
editor: pointsav-engineering
paired_with: design-color.es.md
cites:
  - wcag-22
  - dtcg-spec
---

The substrate's color system has three layers — primitive, semantic, and component. Each tenant's brand lives at the semantic layer; primitives are stable across tenants; components reference semantics, never primitives directly.

## Three-layer model

```
   primitive    color.primary-60  →  #234ed8
        ↓
   semantic     interactive-primary  →  {color.primary-60}
        ↓
   component    button.background-default  →  {semantic.interactive-primary}
```

A tenant who wants their primary action to be teal instead of blue overrides only the semantic layer:

```json
"interactive-primary": { "$value": "{color.brand-teal-60}" }
```

Components don't change. Primitives don't change. The override ripples through every consumer of `interactive-primary`.

## Primitive families

The substrate ships five color families at the primitive layer. Names are generic — they describe role, not business meaning.

| Family | Use for | Steps |
|---|---|---|
| **Neutral** | Backgrounds, borders, ink, dividers | 10–100 (10 steps) |
| **Primary** | The tenant's most prominent interactive color | 10–90 |
| **Positive** | Successful state, positive feedback | 10–70 |
| **Caution** | Reversible problems, expiring states | 10–70 |
| **Critical** | Failures, destructive actions, errors | 10–70 |

Numbers indicate lightness — `10` is lightest, `90`/`100` is darkest. A designer arriving from a numeric-scale design system recognises the scale immediately; the muscle memory is intentional. Hex values are PointSav's own.

## Semantic roles

The semantic layer maps roles onto primitives. PointSav-brand ships one canonical mapping; SMB customers fork it.

### Ink (text)

| Token | Use for |
|---|---|
| `ink-primary` | Body text, headings on default surface |
| `ink-secondary` | Captions, helper text, supporting copy |
| `ink-on-interactive` | Text on interactive backgrounds |
| `ink-on-positive` / `-caution` / `-critical` | Text on support backgrounds |
| `ink-disabled` | Disabled controls |
| `ink-placeholder` | Input placeholder text |

### Surface (background)

| Token | Use for |
|---|---|
| `surface-base` | Default page background |
| `surface-subtle` | Backgrounded panels, sidebars |
| `surface-elevated` | Modals, popovers, layers above the page |
| `surface-inverse` | High-emphasis inversions |

### Border

| Token | Use for |
|---|---|
| `border-subtle` | Default border between sections, cards |
| `border-strong` | Emphasised divider, input border |
| `border-interactive` | Focus / active state |

### Interactive (background)

| Token | Use for |
|---|---|
| `interactive-primary` (+ hover, pressed, disabled) | Primary buttons, primary links |
| `interactive-secondary` (+ hover, pressed) | Secondary buttons |
| `interactive-ghost` (+ hover, pressed) | Ghost buttons |
| `interactive-critical` (+ hover, pressed) | Critical / destructive actions |

### Support (status feedback)

| Token | Use for |
|---|---|
| `support-positive` (+ -bg) | Successful state |
| `support-caution` (+ -bg) | Reversible problem |
| `support-critical` (+ -bg) | Failure |
| `support-info` (+ -bg) | Neutral context |

## Themes

A tenant theme is a `themes/<tenant>.json` file that overrides the semantic layer. The substrate ships `pointsav-brand.json`; SMB customers fork it.

A tenant can ship multiple themes:

- `<tenant>-light.json` and `<tenant>-dark.json` for theme switching
- `<tenant>-seasonal-2026-q4.json` for time-bounded campaigns
- `<tenant>-acquisition-x.json` for sub-brand fan-outs

The planned theme-composition endpoint (`GET /api/themes/compose?base=...&override=...`) is intended to let multiple themes resolve into one DTCG bundle at request time — see Doctrine claim #38 leapfrog target L8.

## WCAG contrast floor

The substrate's primitive choices guarantee WCAG 2.2 AAA contrast (7:1) for the canonical text-on-surface pairs:

- `ink-primary` on `surface-base`: 14.7:1
- `ink-on-interactive` on `interactive-primary`: 7.4:1
- `ink-secondary` on `surface-base`: 8.9:1

A tenant theme that overrides primitives below the WCAG 2.2 AA floor (4.5:1 normal text, 3:1 large text) fails the audit endpoint (subsequent milestone). The substrate enforces the floor; the tenant chooses everything above it.

## See Also

- [[design-typography]]
- [[design-spacing]]
- [[design-philosophy]]

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*

*Woodfine Capital Projects™, Woodfine Management Corp™, PointSav Digital Systems™, Totebox Orchestration™, and Totebox Archive™ are trademarks of Woodfine Capital Projects Inc., used in Canada, the United States, Latin America, and Europe. All other trademarks are the property of their respective owners.*
