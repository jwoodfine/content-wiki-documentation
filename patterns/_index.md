---
schema: foundry-doc-v1
title: "Design Patterns"
slug: patterns-index
category: patterns
type: topic
quality: complete
short_description: "The patterns category collects named design patterns realised across the platform — the editorial reverse funnel, the source-of-truth inversion, pairing-as-permission, the article-shell leapfrog, the Wikipedia-leapfrog chrome — each a recurring shape applied at the editorial, interface, or coordination layer."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-19
editor: pointsav-engineering
paired_with: _index.es.md
---

The **patterns** category collects named design patterns realised across the platform. A pattern in this category is a recurring shape — applied at the editorial, interface, or coordination layer — that solves a structural problem in a way other parts of the platform reuse.

Patterns differ from substrates: a substrate is a load-bearing mechanism the platform depends on (and that compounds over time); a pattern is a design choice that can be applied or not. Patterns differ from architecture: an architecture article describes how a specific system is composed; a pattern describes a shape that recurs across systems.

## Start here

Read [[source-of-truth-inversion]] and [[pairing-as-permission]] first — they are the load-bearing patterns that others build on.

## Sovereignty and infrastructure patterns

The structural commitments that define what a PointSav deployment is and is not.

- [[source-of-truth-inversion]] — Designates one layer as canonical (signed, committed), a second as a deterministically rebuilt view, and a third as session-ephemeral; eliminates entire classes of sync and data-loss bugs.
- [[pairing-as-permission]] — A cryptographic pairing between two nodes is the permission; the absence of a pairing makes the connection structurally impossible — not access-denied, but no pathway.
- [[zero-container-runtime]] — Every deployment runs as a Linux binary under systemd on a plain VM or bare-metal host; no container runtime, no container orchestrator, no managed-runtime platform.
- [[zero-execution-routing]] — Presentation layers adhere to a zero-execution mandate: bilingual routing via structural determinism and interactive elements via native CSS state machines, eliminating client-side JavaScript for core DOM manipulation.
- [[customer-first-ordering]] — A software vendor building something a customer will install should build it in the same order the customer will install it, on the same substrate the customer will use.

## Deployment and configuration

- [[deployment-patterns]] — The six canonical configurations in which the PointSav substrate is deployed — each built on the same five primitives and OS surface, with the Chart of Accounts and compliance surface adapted per segment.

## Collaboration and editorial workflow

- [[collab-via-passthrough-relay]] — The passthrough relay pattern holds no document state on the server and forwards CRDT updates directly between clients, keeping the canonical git tree as the sole authoritative record at every point in time.
- [[model-tier-discipline]] — Routing work to the appropriate AI model tier — deep-think, implementation, or mechanical — to match model capability to work shape and control inference cost.

## Interface and user experience

- [[knowledge-wiki-leapfrog-architecture]] — The app-mediakit-knowledge engine design: Wikipedia-shaped interface elements over flat Markdown git files, with citation verification, research trail provenance, and AI-integrated editing as the differentiation layer.
- [[location-intelligence-ux]] — The Location Intelligence Conclusion-First design philosophy: ranked tier conclusions rather than individual data points, so users see the most defensible commercial nodes at national zoom before drilling into individual operators.

## See also

- [Substrate](/substrate/) — foundational mechanisms patterns build on
- [Architecture](/architecture/) — concrete platform architecture
