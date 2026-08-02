---
schema: foundry-doc-v1
type: topic
content_type: topic
slug: zero-execution-routing
short_description: "Presentation layers adhere to a zero-execution mandate, eliminating client-side JavaScript via structural determinism for routing and native CSS state machines."
title: "Zero-execution routing and presentation"
audience: vendor-public
bcsc_class: current-fact
language: en
paired_with: zero-execution-routing.es.md
category: patterns
last_edited: 2026-05-25
editor: pointsav-engineering
---



**Correction (2026-08-02) — compliance-relevant claim, does not match real code:** the real closest-matching implementation, `service-content/templates/pointsav-monolith.html` (and its sibling `woodfine-brutalist.html`), directly contradicts the "zero client-side JavaScript"/SOC 3 claim below — it contains a live `<script>` block that computes a SHA-256 hash on toggle and fires `navigator.sendBeacon` telemetry on page unload. There is also no root-vs-`/es/`-directory split anywhere in the repo for any presentation surface checked — the real template embeds both language blocks in one file, toggled by a single checkbox, not the structural two-file split this article describes. The CSS-checkbox toggle mechanism itself is real (confirmed in both templates), but "zero execution latency and no client-side script vulnerability" is false as a description of the real deployed page. **Flagged, not resolved** — this claim invokes SOC 3 compliance directly, so it needs correcting or re-scoping rather than left standing.

Platform presentation layers adhere to a zero-execution mandate, eliminating client-side JavaScript for core DOM manipulation, language routing, and file serving. This architectural constraint minimizes the attack surface and supports SOC 3 (Service Organization Control 3) compliance by relying entirely on deterministic files and native CSS state management. The pattern complements the [[machine-based-auth|machine-based authentication]] layer and the [[sovereign-ai-routing|sovereign AI routing]] architecture.

## Key Takeaways

- No client-side JavaScript for core DOM manipulation, language routing, or file serving. The zero-execution mandate reduces the presentation-layer attack surface and supports SOC 3 compliance by relying entirely on deterministic static files and native CSS.
- Bilingual routing is structural, not conditional. The English `index.html` sits at the root; the Spanish `index.html` sits at `/es/` with the language-state checkbox `checked` in static HTML — no IP sniffing, no server-side redirect logic.
- Interactive elements (language toggles, download buttons) use native CSS checkbox state machines: all language blocks load simultaneously, and CSS `display: block/none` switches between them on `:checked` state. Result: zero execution latency, zero script injection surface at the presentation layer.
- The pattern pairs with [[machine-based-auth]]. Presentation surfaces that execute no JavaScript cannot be exploited via script injection — authentication occurs at the machine layer, not the browser layer.

## 1. Deterministic Bilingual Routing

The platform avoids the security risks and latency of IP-sniffing scripts or conditional server-side redirects. Language routing is achieved through structural determinism:
* **English (Root):** The primary `index.html` resides in the root directory.
* **Spanish (/es/):** A structurally identical `index.html` resides in the `/es/` sub-directory, with the `checked` attribute natively applied to the language-state checkbox.

## 2. The Pure CSS State Machine

Interactive interface elements, such as language toggles and dynamic download buttons, operate via native CSS checkbox patterns rather than script-driven state:
* **Simultaneous Loading:** The DOM loads all language blocks and button variations simultaneously.
* **Native Switching:** CSS rules (`display: block` / `none`) are tied to the `:checked` state of hidden inputs.
* **Zero Latency:** This method provides the illusion of a high-performance Web 2.0 application with zero execution latency and no client-side script vulnerability.

This approach ensures that platform interfaces are accessible, secure, and instantaneous across all network environments.

## See also

- [[sovereign-ai-routing]] — the sovereign AI routing architecture that pairs with this zero-execution discipline
- [[machine-based-auth]] — machine-based authentication layer operating in the same zero-trust presentation context
- [[decode-time-constraints]] — decode-time constraints that enforce deterministic execution boundaries
- [[sel4-microkernel-substrate]] — the microkernel substrate that grounds the execution isolation model
