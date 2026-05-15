---
schema: foundry-doc-v1
title: "Design System — Typography"
slug: design-typography
category: design-system
type: reference
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-15
editor: pointsav-engineering
paired_with: design-typography.es.md
cites:
 - wcag-22
 - dtcg-spec
---

The PointSav design system organises every typeface across the product family into six functional families and two brand assets, then divides the typographic load between two rendering scales — Utility for functional UI text and Display for expressive surfaces. Each family ships as a self-hosted binary; no surface calls an external font service. Screen-to-print fidelity is a regulatory requirement, not a stylistic preference: a signed record must render identically in 2026 and in 2030. This article covers the two scales, six families, packaging model, and the fidelity requirement underlying them all.

## Two design systems, not one

PointSav operates two design systems. The distinction is structural:

| Design system | Repository | Purpose | Audience |
|---|---|---|---|
| `pointsav-design-system` | `pointsav` vendor org | UI/UX substrate for the Command Ledger and the entire PointSav OS family | PointSav contributors and fleet operators |
| `woodfine-design-bim` | `woodfine` customer org | Building Information Modelling tokens and components for real-property surfaces | Architects, engineers, and real-property operators |

The two systems share methodology — the [[six-tier-sovereignty-matrix|six-tier sovereignty model]] and the strict kebab-case naming rule — but do not share content. A BIM design token does not belong in the PointSav UI substrate; a console interface token does not belong in the BIM library. This article covers the first system.

## The two scales

| Scale | Use for | Steps |
|---|---|---|
| **Utility** | UI text — body, labels, captions, table cells, button labels | 4 (12/14/16/16-bold) |
| **Display** | Expressive type — sub-headings, section headings, page titles, hero | 4 (20/24/32/42) |

The split is structural, not decorative. Utility text uses optimised letter-spacing for screen-readability at small sizes; Display text uses negative letter-spacing for a tighter heading rhythm. Mixing scales breaks the system's visual hierarchy.

## The six typographic families

The design system organises every typeface into five functional families plus two brand assets:

| Family | Role | Reference implementation | Used by |
|---|---|---|---|
| `font-ui-variable` | Variable-weight sans for all UI; single file replaces separate desktop and mobile weights | Inter Variable or Roboto Flex | `os-workplace` desktop, Command Ledger chrome |
| `font-mono-code` | Nerd-Font-patched monospace; coding ligatures; slashed zero; distinguishable `1 l I` | Custom mono with NF patches | Command Ledger body text, the Forge |
| `font-document-serif` | Transitional serif optimised for screen and print | Noto Serif or Literata | Documentation wiki, long-form reading, PDF-A output |
| `font-tabular-nums` | Specialised numeric subset with perfect vertical alignment | Variant of the UI sans with tabular figures | [[service-bookkeeper\|service-bookkeeper]], IronCalc, financial tables |
| `font-iconography` | SVG-in-OTF vector symbol set | PointSav-owned | All `os-*` UI icons |

| Brand asset | Role |
|---|---|
| `asset-brand-pointsav` | The vendor brand — marketing, public keynotes, the vendor mark. Never used for UI text. |
| `asset-brand-wcp` | The Woodfine Capital Projects sub-brand — legally distinct from PointSav to maintain corporate hierarchy. |

`font-ui-variable` ships with a system-stack fallback chain so every surface remains functional if the variable font binary is not loaded:

```
'Inter Variable', 'Roboto Flex', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif
```

A tenant theme can substitute any font family at the primitive layer. Self-hosting the font binary is the customer's responsibility; the substrate references the family by name.

## Font packages

Typography is split into a binary store and an engine:

| Package | Contents | Rationale |
|---|---|---|
| `package-fonts` | Pure asset storage — `.woff2`, `.ttf`, `.otf` binaries | Isolating binaries prevents logic packages from inheriting filesystem bloat |
| `package-typography` | Rust-native logic for fallback control, text shaping, variable-font interpolation | Engineering quality belongs with the engine, not the assets |

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

A heading-level skip — `h1` followed by `h3` with no `h2` between — breaks accessibility; screen readers rely on the hierarchy to navigate.

## Typography as law

The most stringent typography requirement is screen-to-print fidelity. A PDF generated from a Totebox record in 2030 must render identically to the on-screen version the auditor signed in 2026. This is what [[compliance-and-continuous-disclosure|continuous-disclosure]] obligations require; it is what ISO 19650 document-state suffixes (`_JW`, `_FIN`, `_PUB`, `_EXE`, `_MCH`/`_DAT`) presume; it is what the Digital Asset Resolution Package standard demands when a record is severed from the vendor and returned to its legal owner.

Typography fidelity is regulatory compliance, not aesthetic preference.

## Strict kebab-case

All directory names, package names, repository names, and binary names are lowercase with hyphens. Capital letters are banned across the design system. The rule holds across Docker registries (which reject uppercase), Linux filesystems (case-sensitive), macOS (case-insensitive), and DNS subdomains. One exception creates permanent infrastructure drift; enforcing the rule costs one rule.

## Brand voice

The substrate's voice rules live in the active theme's `voice` block. PointSav-brand:

- **Confident** — no hedging, no apology
- **Direct** — action verbs first, single-clause sentences where possible
- **Professional** — precise register, no marketing vocabulary

Banned vocabulary applies to all body and heading copy.

## See also

- [[design-color]]
- [[design-spacing]]
- [[design-philosophy]]
- [[six-tier-sovereignty-matrix]] — the sovereignty model shared across both design systems
- [[compliance-and-continuous-disclosure]] — the regulatory framework underlying typography fidelity
