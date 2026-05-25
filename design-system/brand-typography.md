---
schema: foundry-doc-v1
type: topic
slug: brand-typography
short_description: "The PointSav typography system separates web interface system fonts from institutional print typography, reserving open-licence serif typefaces for PDF generation and formal disclosures while the UI defaults to platform system fonts."
title: "Brand typography and print standards"
audience: vendor-public
bcsc_class: current-fact
language: en
paired_with: brand-typography.es.md
category: design-system
status: active
last_edited: 2026-05-25
editor: pointsav-engineering
---



The platform enforces a strict boundary between web interface presentation and institutional print output. Web layers use native system fonts for performance; brand typography is reserved for PDF generation and formal printed documents. All typefaces are licensed under the SIL Open Font License (OFL) to ensure the Digital Asset Resolution Package (DARP) — the platform's principle requiring all embedded assets to be freely distributable — is satisfied.

## 1. The execution boundary

All web-based user interfaces use native system UI fonts to minimize latency without loading external font files. High-fidelity brand typography is embedded during the `service-content` compilation phase for PDF binaries. Brand identity is expressed through the resulting document artifact rather than the delivery mechanism.

## 2. The OFL typography matrix

All typefaces in the platform are SIL Open Font License (OFL) equivalents of the legacy proprietary fonts they replaced. Font binaries are embedded directly in generated PDFs.

| Token | Active Font | Legacy Equivalent | Strategic Application |
| :--- | :--- | :--- | :--- |
| **serif_primary** | **Zilla Slab** | Caecilia LT Std | High-level institutional trust (White papers). |
| **sans_condensed**| **Barlow Condensed** | Trade Gothic | Data-dense financial ledgers and tables. |
| **sans_primary** | **Nunito Sans** | Avenir LT Std | Standard body copy and operational text. |
| **serif_secondary**| **Sahitya** | N/A | Editorial pull-quotes and contrast markers. |

## 3. Institutional authority in output

Brand typography establishes a professional, high-precision aesthetic for all generated documents. Zilla Slab for headers and Barlow Condensed for financial data give PointSav and Woodfine disclosures a consistent, recognizable institutional register.

## See also

- [[brand-family-swatch]]
- [[news-release-standards]]
