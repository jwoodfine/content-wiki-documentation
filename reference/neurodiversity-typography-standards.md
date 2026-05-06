---
schema: foundry-doc-v1
type: topic
slug: neurodiversity-typography-standards
title: Neurodiversity and Typographic Standards
audience: vendor-public
bcsc_class: current-fact
language: en
paired_with: neurodiversity-typography-standards.es.md
## See Also

- [[brand-typography]]
- [[design-typography]]
- [[viewport-3d-accessibility]]

---


Foundry prioritizes cognitive accessibility by implementing strict typographic standards designed to accommodate neurodivergent users. By adhering to WCAG 2.2 institutional accessibility guidelines, the system ensures that complex technical and financial disclosures remain legible for individuals with dyslexia, astigmatism, and other processing variances.

## 1. Native System UI Stack

To eliminate layout shifts (Flash of Unstyled Text) and reduce network latency, Foundry bypasses external font services. All interfaces strictly utilize the native operating system font stack:
`-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif`.

## 2. Reducing Cognitive Load

The following constraints are mandatory for all dense text presentations:

*   **Left Alignment (Ragged Right):** Text must remain left-aligned. Justified text is strictly prohibited, as it creates erratic "rivers of white space" that disrupt reading flow for neurodivergent users.
*   **Optimal Line Height:** Line height must be maintained between `1.6` and `1.8` for all body copy.
*   **Orphan and Widow Control:** Utilize `text-wrap: pretty` to ensure balanced text blocks where supported by modern CSS Level 4 rendering engines.

## 3. Fluidity and Precision

*   **Mathematical Scaling:** Typography utilizes the CSS `clamp()` function to scale fluidly across viewports, eliminating the need for rigid media query breakpoints.
*   **Hit Area Standards:** All interactive elements, such as toggles and PDF links, must maintain a minimum physical boundary of 44x44 pixels to prevent input errors.

## 4. Institutional Print Engine

Every application must include a `@media print` CSS block. Upon execution of a print command, the DOM is instantly reformatted for physical output: removing UI navigation, stripping backgrounds, and applying 1-inch margins suitable for hardware printers or PDF archiving.


---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*

*Woodfine Capital Projects™, Woodfine Management Corp™, PointSav Digital Systems™, Totebox Orchestration™, and Totebox Archive™ are trademarks of Woodfine Capital Projects Inc., used in Canada, the United States, Latin America, and Europe. All other trademarks are the property of their respective owners.*
