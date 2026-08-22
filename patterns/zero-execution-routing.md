---
schema: foundry-doc-v1
type: topic
content_type: topic
index_group: sovereignty-and-infrastructure-patterns
slug: zero-execution-routing
short_description: "The platform's public homepage templates use a native-CSS checkbox pattern for language toggling and interactive elements, alongside a small amount of client-side JavaScript for page-integrity display and analytics."
title: "Presentation-layer routing and client-side script"
audience: vendor-public
bcsc_class: current-fact
language: en
paired_with: zero-execution-routing.es.md
category: patterns
last_edited: 2026-08-22
editor: pointsav-engineering
---

The platform's public homepage templates use native CSS checkbox state — not JavaScript — for their interactive elements: language toggles and download buttons switch visible content via `:checked` selectors rather than a script listening for click events. **A reader toggling between languages on the homepage is not running any script to do it.** That interaction works even with JavaScript disabled entirely. The same templates do carry a small amount of client-side JavaScript for a different purpose: computing and displaying a page-integrity checksum, and reporting basic page-view analytics on navigation away from the page.

## The CSS checkbox pattern

Interactive interface elements — language toggles, download-variant buttons — operate on native CSS checkbox state rather than script-driven state. The DOM loads all language blocks and button variants at once; CSS `display` rules tied to a hidden checkbox's `:checked` state show or hide the relevant block. Switching languages or button variants involves no script execution and no page reload — it is a pure CSS state change. The two language blocks currently live in a single template file, toggled by one checkbox, rather than as separate documents at distinct URL paths.

## What client-side script the pages do run

The homepage templates load one small inline script for two purposes unrelated to routing or language switching: it computes a SHA-256 checksum of page content for display in the page's metadata block, and it fires a page-view beacon (`navigator.sendBeacon`) when the reader navigates away. **This means the presentation layer is not entirely script-free** — a reader auditing the page's actual behavior will find this script running on both `pointsav.com` and `woodfinegroup.com` today. The checkbox-based routing and toggle behavior described above genuinely runs without script; the checksum display and analytics beacon are a separate, smaller piece of functionality layered on top of that CSS-driven page.

## See also

- [[sovereign-ai-routing]] — the sovereign AI routing architecture that pairs with this presentation layer
- [[machine-based-auth]] — machine-based authentication layer operating in the same presentation context
- [[decode-time-constraints]] — decode-time constraints that enforce deterministic execution boundaries
- [[sel4-microkernel-substrate]] — the microkernel substrate that grounds the execution isolation model
