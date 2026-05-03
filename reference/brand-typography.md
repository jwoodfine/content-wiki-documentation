---
schema: foundry-doc-v1
type: topic
slug: brand-typography
title: Brand Typography and Print Standards
audience: vendor-public
bcsc_class: current-fact
language: en
paired_with: brand-typography.es.md
---

# Brand Typography and Print Standards

Foundry enforces a strict boundary between web interface presentation and institutional print output. While web layers prioritize performance via native system fonts, brand typography is reserved for offline print and PDF generation to project institutional authority and ensure DARP compliance.

## 1. The Execution Boundary

All web-based user interfaces utilize native System UI fonts to maintain a Zero-Execution state and minimize latency. High-fidelity brand typography is strictly embedded during the `service-content` compilation phase for physical PDF binaries. This ensures that brand identity is projected through the resulting artifact rather than the delivery mechanism.

## 2. The OFL Typography Matrix

To guarantee absolute compliance with the Digital Asset Resolution Package (DARP), all proprietary fonts have been replaced with 100% SIL Open Font License (OFL) equivalents. These binaries are secured within air-gapped vaults to prevent unauthorized distribution.

| Token | Active Font | Legacy Equivalent | Strategic Application |
| :--- | :--- | :--- | :--- |
| **serif_primary** | **Zilla Slab** | Caecilia LT Std | High-level institutional trust (White papers). |
| **sans_condensed**| **Barlow Condensed** | Trade Gothic | Data-dense financial ledgers and tables. |
| **sans_primary** | **Nunito Sans** | Avenir LT Std | Standard body copy and operational text. |
| **serif_secondary**| **Sahitya** | N/A | Editorial pull-quotes and contrast markers. |

## 3. Institutional Authority in Output

Brand typography is utilized to establish a professional "White Paper" aesthetic for all generated documents. The use of **Zilla Slab** for headers and **Barlow Condensed** for financial data ensures that PointSav and Woodfine disclosures are immediately recognizable as authoritative, high-precision reports.


---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*

*Woodfine Capital Projects™, Woodfine Management Corp™, PointSav Digital Systems™, Totebox Orchestration™, and Totebox Archive™ are trademarks of Woodfine Capital Projects Inc., used in Canada, the United States, Latin America, and Europe. All other trademarks are the property of their respective owners.*
