---
schema: foundry-doc-v1
title: "Design system — primitive vocabulary rationale"
slug: design-primitive-vocabulary
short_description: "Documents the structural patterns preserved in the design system's primitive token layer — numeric color scales, layered semantic aliasing, productive-versus-expressive type split, and numeric spacing scales — aligned with 2018 to 2026 field conventions while using PointSav-specific naming and values."
category: design-system
type: reference
quality: complete
status: active
audience: public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-06
editor: pointsav-engineering
paired_with: design-primitive-vocabulary.es.md
cites:
 - wcag-22
 - dtcg-spec
 - doctrine-38
---

## What the substrate kept structurally

The substrate's primitive token layer preserves four structural patterns the modern design-system field has converged on (2018–2026):

1. **Numeric color scales (10 / 20 / ... / 100)** — established across the modern design-system field. A practitioner arriving from any major design system recognises the scale on first encounter.
2. **Primitive → Semantic → Component layering** — primitives ground the value; semantics map the role; components consume semantics. DTCG 2025.10 formalised aliasing across layers; the substrate uses the canonical alias syntax (`{semantic.token}`).
3. **Productive vs Expressive type split** — the field's two-track typography model (UI-functional vs marketing-expressive) is structurally the right answer; most modern systems implement it under different names. The substrate ships Utility + Display.
4. **Numeric spacing scale (1..13)** — every modern design system ships ~12–15 step spacing scales aligned to a 4px or 8px base. The substrate uses 8px-base 13-step.

These patterns are not the intellectual property of any single design system — they are the field's shared vocabulary. Re-implementing them is the correct architectural choice for any 2026 design system that wants practitioner pickup without re-teaching basics.

## What the substrate replaced

The substrate uses PointSav-original vocabulary, hex values, font choices, and content. Specifically:

| Surface | Common field convention | Substrate choice | Why replaced |
|---|---|---|---|
| Color family names | `gray`, `blue`, `red`, `green`, `yellow` | `neutral`, `primary`, `positive`, `caution`, `critical` | Role-names per Agent B research §9. PointSav's names describe role, not chromatic family — tenants who shift their brand from blue to teal don't have to rename tokens. |
| Hex values | Vendor-specific shades | PointSav-chosen shades (e.g., Primary 60 = `#234ed8`) | Avoid IP entanglement; the substrate stands on its own values. |
| Spacing token name | `spacing-01` through `spacing-13` (zero-padded) | `space-1` through `space-13` (no zero-pad) | Slightly cleaner; same numeric scale; same 8px-base structure. |
| Type-scale family names | `productive-01..N`, `expressive-01..N` | `utility-1..4`, `display-1..4` | Same conceptual split; PointSav-original names. |
| Motion easing names | `ease-productive`, `ease-expressive`, `ease-entrance`, `ease-exit` | `ease-utility`, `ease-display`, `ease-enter`, `ease-exit` | Same four-curve set; aligned to the type-scale renaming. |
| Duration names | `fast-01`, `fast-02`, `moderate-01`, `moderate-02`, `slow-01`, `slow-02` | `speed-1` through `speed-6` | Same six-step scale; cleaner naming. |
| Border radius names | `radius-01`, `radius-02`, `radius-03` | `corner-1`, `corner-2`, `corner-3` | Same three-step scale; differentiated naming. |
| Default font | A corporate-sponsored open-source face | Inter (community open-source, SIL OFL 1.1) + system stack fallback | No corporate brand association; Inter is the modern UI workhorse; system stack ensures graceful degradation. |
| Theme names | Brand-specific light/dark labels | `pointsav-brand` (canonical), per-tenant variants | PointSav ships the canonical brand and SMB customers ship their own. |

## What the substrate kept verbatim from broader convention

These are field-shared, not vendor-proprietary:

- `$type: "color"`, `$value`, `$description` — DTCG 2025.10 spec syntax
- `{path.to.token}` reference syntax — DTCG aliasing
- WCAG 2.2 AAA contrast floor — accessibility standard
- `prefers-reduced-motion` query — CSS Media Queries Level 5
- 8px base grid for spacing — common across the field

These are the open standards the substrate inherits as an open standards consumer.

## Why the muscle-memory matters

A designer or developer arriving from any modern design-system background recognises the substrate's structural patterns within seconds:

- "Numeric color scale, lower numbers lighter — same as everywhere else."
- "Primitive → semantic → component layering — same as DTCG aliasing."
- "Two type tracks for UI vs expressive — same as the productive/expressive split."

This recognition is the cognitive on-ramp. It is the substrate's biggest piece of free leverage — a practitioner ramps in days, not weeks. Discarding it for novelty's sake would be a bad trade.

## Why the vocabulary matters

A token named for a chromatic family in PointSav's code that uses a vendor's exact shade puts the substrate one trademark dispute away from a rebrand. A token named by role with a PointSav-chosen shade does not.

The structural patterns are field-shared; the literal tokens are not.

## See also

- [[design-philosophy]]

## References

- W3C Design Tokens Community Group format — https://design-tokens.github.io/community-group/format/
- WCAG 2.2 — https://www.w3.org/TR/WCAG22/
