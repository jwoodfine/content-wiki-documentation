---
schema: foundry-doc-v1
type: topic
slug: zero-execution-routing
title: Zero-Execution Routing and Presentation
audience: vendor-public
bcsc_class: current-fact
language: en
paired_with: zero-execution-routing.es.md
## See Also

- [[sovereign-ai-routing]]
- [[machine-based-auth]]
- [[decode-time-constraints]]
- [[sel4-foundation]]

---


Foundry’s public presentation layers adhere to a "Zero-Execution" mandate, eliminating client-side JavaScript for core DOM manipulation, language routing, and file serving. This architectural constraint minimizes the attack surface and guarantees SOC 3 compliance by relying entirely on deterministic files and native CSS state management.

## 1. Deterministic Bilingual Routing

Foundry avoids the security risks and latency of IP-sniffing scripts or conditional server-side redirects. Language routing is achieved through structural determinism:
*   **English (Root):** The primary `index.html` resides in the root directory.
*   **Spanish (/es/):** A structurally identical `index.html` resides in the `/es/` sub-directory, with the `checked` attribute natively applied to the language-state checkbox.

## 2. The Pure CSS State Machine

Interactive interface elements, such as language toggles and dynamic download buttons, operate via native CSS checkbox patterns rather than script-driven state:
*   **Simultaneous Loading:** The DOM loads all language blocks and button variations simultaneously.
*   **Native Switching:** CSS rules (`display: block` / `none`) are tied to the `:checked` state of hidden inputs.
*   **Zero Latency:** This method provides the illusion of a high-performance Web 2.0 application with zero execution latency and no client-side script vulnerability.

This "Leapfrog 2030" standard ensures that Foundry interfaces are accessible, secure, and instantaneous across all network environments.


---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*

*Woodfine Capital Projects™, Woodfine Management Corp™, PointSav Digital Systems™, Totebox Orchestration™, and Totebox Archive™ are trademarks of Woodfine Capital Projects Inc., used in Canada, the United States, Latin America, and Europe. All other trademarks are the property of their respective owners.*
