---
schema: foundry-doc-v1
title: "Design System — Spacing"
slug: design-spacing
category: design-system
type: reference
quality: complete
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-06
editor: pointsav-engineering
paired_with: design-spacing.es.md
cites:
  - dtcg-spec
---

A 13-step spacing scale on a 16 px base. Numeric — `space-1` through `space-13` — gives one canonical answer per layout decision.

## Scale

| Token | Value | Common use |
|---|---|---|
| `space-1` | 2px | Hairline gutter (rare; usually borders only) |
| `space-2` | 4px | Inline element gap |
| `space-3` | 8px | Paragraph rhythm floor; icon-label gap |
| `space-4` | 12px | Form field padding |
| `space-5` | 16px | Body grid unit; default container padding |
| `space-6` | 24px | Card padding; vertical rhythm between sections |
| `space-7` | 32px | Section gutter |
| `space-8` | 40px | Wider section gap |
| `space-9` | 48px | Major section break |
| `space-10` | 64px | Page-level section |
| `space-11` | 80px | Page-level section (looser) |
| `space-12` | 96px | Page-level section (loosest) |
| `space-13` | 160px | Hero / landing-page-only spacing |

## Composition

Compose larger spacing from the scale, never invent off-scale values:

- 4px + 12px + 4px = `space-2 + space-4 + space-2` for a labelled field
- Card with 24px padding: `space-6`
- Section break with title above and content below at 32px each: `space-7` × 2

Off-scale values (5px, 14px, 22px) break the rhythm and accumulate as drift. The 13-step scale is dense enough to cover every layout need without resorting to off-scale.

## Layout floor

The substrate uses a 16px (`space-5`) baseline grid. Body text and headings align to multiples of 16px in their line-height calculation; container padding aligns to multiples of 16px in the inline axis. This is structural — it ensures vertical rhythm remains consistent across surfaces.

## See Also

- [[design-color]]
- [[design-typography]]
- [[design-motion]]

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*

*Woodfine Capital Projects™, Woodfine Management Corp™, PointSav Digital Systems™, Totebox Orchestration™, and Totebox Archive™ are trademarks of Woodfine Capital Projects Inc., used in Canada, the United States, Latin America, and Europe. All other trademarks are the property of their respective owners.*
