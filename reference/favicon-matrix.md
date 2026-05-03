---
schema: foundry-doc-v1
type: topic
slug: favicon-matrix
title: Favicon Matrix and Tab Identity
audience: vendor-public
bcsc_class: current-fact
language: en
paired_with: favicon-matrix.es.md
---

# Favicon Matrix and Tab Identity

The PointSav Building Design System utilizes high-fidelity SVG data URIs to manage browser tab identification. This approach optimizes performance and visual clarity across all display types while reinforcing corporate identity at the infrastructure level.

## Engineering Logic

By embedding SVG icons directly into the `<link rel="icon">` header as URL-encoded data URIs, Foundry achieves two primary technical objectives:

1.  **Zero Latency Execution:** The elimination of external `.ico` or `.png` requests removes unnecessary network overhead during initial page load.
2.  **Resolution Independence:** Vector-based rendering ensures that icons remain perfectly sharp on high-DPI (Retina) displays without requiring multiple raster assets.

## Entity Visual Dichotomy

The favicon matrix defines specific visual signatures to distinguish between infrastructure and operational layers:

| Entity | Symbol | Color | Role |
| :--- | :--- | :--- | :--- |
| **Vendor (PointSav)** | Square | Steel-Blue (`#869FB9`) | Represents foundational infrastructure. |
| **Customer (Woodfine)** | Circle | Woodfine Blue (`#164679`) | Represents the operating enterprise. |

## Implementation Standard

Icons are encoded as follows:
```html
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' fill='%23869FB9'/%3E%3C/svg%3E">
```
This standardized implementation ensures that tab identity is established immediately and consistently across the entire suite of Foundry applications.
