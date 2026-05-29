---
schema: foundry-doc-v1
title: "Favicon matrix and tab identity"
slug: favicon-matrix
category: governance
type: topic
quality: complete
short_description: "The platform uses inline SVG data URIs for browser-tab favicons — eliminating a network call, scaling without pixelation on every display, and assigning two distinct vendor and customer marks to make the entity behind every tab unambiguous at a glance."
status: active
bcsc_class: no-disclosure-implication
last_edited: 2026-05-08
editor: pointsav-engineering
paired_with: favicon-matrix.es.md
---

The platform uses inline SVG data URIs for browser-tab favicons — eliminating a network call for the icon file, scaling without pixelation on every display, and assigning two distinct marks so the entity behind every browser tab is unambiguous at a glance. Vendor sites carry a steel-blue square; customer sites carry a Woodfine blue circle. The marks are encoded directly in the page `<head>`, so a tab identity is established before any other resource loads.

This article describes the engineering rationale and the entity-mark assignment.

## Engineering rationale

Embedding the SVG inline in the `<link rel="icon">` element as a URL-encoded data URI delivers two practical properties:

- **Zero HTTP requests.** No network call for an icon file. The favicon is parsed from the page `<head>` and rendered immediately. Tab identity is established on first paint.
- **Resolution-independent rendering.** Vector geometry scales without pixelation, so the same icon is sharp on a low-density laptop display and a high-density external monitor. No retina-suffixed asset variants are required.

The cost is a small payload increase per page (a few hundred bytes of inline SVG). The benefit — a faster first-paint and a single canonical asset path — is worth the trade.

## Entity-mark assignment

Two marks are in use across all platform-served pages:

| Mark | Colour | Shape | Identifies |
|---|---|---|---|
| Vendor | Steel blue (`#869FB9`) | Square | PointSav-served properties: documentation, design system, vendor-side wikis. |
| Customer | Woodfine blue (`#164679`) | Circle | Woodfine-served properties: project portfolios, [[disclosure-substrate|corporate disclosures]], customer-side wikis. |

A reader who has both vendor and customer sites open in adjacent browser tabs can identify the source of each tab without reading the title. The geometric distinction (square vs circle) is preserved when colour vision is reduced.

## See also

- [[design-system-substrate]] — the design system substrate that defines the visual language these marks belong to
- [[anti-homogenization-discipline]] — the editorial discipline that preserves distinct brand voices alongside this visual identity
- [[disclosure-substrate]] — the outbound communications architecture served under the customer mark
