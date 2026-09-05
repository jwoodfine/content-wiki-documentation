---
schema: foundry-doc-v1
title: "Favicon matrix and tab identity"
slug: favicon-matrix
category: governance
type: topic
content_type: topic
quality: complete
index_group: platform-disciplines
short_description: "The wiki serves a single static SVG favicon — a navy document-page glyph, linked from a static file, the same mark on every tab regardless of tenant."
status: active
audience: vendor-public
bcsc_class: no-disclosure-implication
language_protocol: PROSE-TOPIC
last_edited: 2026-08-22
editor: pointsav-engineering
paired_with: favicon-matrix.es.md
---

The wiki serves one favicon: a navy (`#1a4480`) document-page glyph on a rounded square, defined as a static SVG file and linked from the page `<head>` with a standard `<link rel="icon">` element. Every tenant's tabs carry the same mark — there is no per-tenant colour or shape variant, and no inline data-URI encoding.

This article describes the mechanism as built.

## Key Takeaways

- The favicon is a static file (`static/favicon.svg`), served over HTTP and referenced by a normal `<link rel="icon">` tag — not an inline SVG data URI.
- `/favicon.ico`, the path browsers request by convention regardless of what `<head>` declares, redirects to the same static SVG file.
- One mark serves every tenant. There is no vendor/customer, square/circle, or steel-blue/Woodfine-blue distinction in the current build.

## The mechanism

`app-mediakit-knowledge`'s page layout links the icon in `<head>`:

```html
<link rel="icon" type="image/svg+xml" href="/static/favicon.svg">
```

The server also registers a `/favicon.ico` route that redirects to the same file, so browsers and crawlers that request that exact path by convention (independent of the `<head>` declaration) still resolve to the real icon rather than a 404.

## The mark

The icon is a single, un-parameterised SVG: a navy (`#1a4480`) rounded-square base with a white document-page glyph. It does not vary by tenant, deployment, or wiki — `documentation.pointsav.com`, `projects.woodfinegroup.com`, and `corporate.woodfinegroup.com` all serve the identical file.

## See also

- [[design-system-substrate]] — the design system substrate that defines the visual language these marks belong to
- [[anti-homogenization-discipline]] — the editorial discipline that preserves distinct brand voices alongside this visual identity
- [[disclosure-substrate]] — the outbound communications architecture served under the customer mark
