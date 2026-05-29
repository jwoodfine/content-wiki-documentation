---
schema: foundry-doc-v1
title: "Design patterns"
slug: patterns-index
category: patterns
type: topic
quality: complete
short_description: "The patterns category collects named design patterns realised across the platform — source-of-truth inversion, pairing-as-permission, zero-container runtime, zero-execution routing, customer-first ordering, model-tier discipline, deployment patterns, the passthrough relay, the knowledge-wiki leapfrog architecture, and the location-intelligence UX — each a recurring shape applied at the editorial, interface, or coordination layer."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-29
editor: pointsav-engineering
paired_with: _index.es.md
---

The **patterns** category collects named design patterns realised across the platform. A pattern in this category is a recurring shape — applied at the editorial, interface, or coordination layer — that solves a structural problem in a way other parts of the platform reuse. Patterns differ from substrates: a substrate is a load-bearing mechanism the platform depends on (and that compounds over time); a pattern is a design choice that can be applied or not. Patterns differ from architecture: an architecture article describes how a specific system is composed; a pattern describes a shape that recurs across systems.

Patterns in this collection sit on top of the [[compounding-substrate]] and the [[three-ring-architecture]] — they describe how the platform expresses those foundations in recurring, named shapes.

## Start here

Read [[source-of-truth-inversion]] and [[pairing-as-permission]] first — they are the load-bearing patterns that the others build on.

## Sovereignty and infrastructure patterns

The structural commitments that define what a PointSav deployment is and is not.

- [[source-of-truth-inversion]] — Designates one layer as canonical (signed, committed), a second as a deterministically rebuilt view, and a third as session-ephemeral; eliminates entire classes of sync and data-loss bugs.
- [[pairing-as-permission]] — A cryptographic pairing between two nodes is the permission; the absence of a pairing makes the connection structurally impossible — not access-denied, but no pathway.
- [[zero-container-runtime]] — Every deployment runs as a Linux binary under systemd on a plain VM or bare-metal host; no container runtime, no container orchestrator, no managed-runtime platform.
- [[zero-execution-routing]] — Presentation layers adhere to a zero-execution mandate: bilingual routing via structural determinism and interactive elements via native CSS state machines, eliminating client-side JavaScript for core DOM manipulation.
- [[customer-first-ordering]] — A software vendor building something a customer will install should build it in the same order the customer will install it, on the same substrate the customer will use.
- [[customer-hostability]] — The architectural commitment that every artefact runs on the customer's own hardware, against the customer's own keys, with the customer's own audit ledger.

## Deployment and configuration

The canonical configurations in which the substrate is shipped and the disciplines that keep deployments composable.

- [[deployment-patterns]] — The six canonical configurations in which the PointSav substrate is deployed — each built on the same five primitives and OS surface, with the Chart of Accounts and compliance surface adapted per segment.
- [[three-layer-architecture]] — How PointSav deliverables move through SOFTWARE, SHOWCASE, and INSTANCE layers with a strict one-way vendor-to-customer flow.
- [[3-layer-stack]] — The three-layer infrastructure decomposition: raw compute capability, isolated platform execution, and secure operator access.

## Collaboration and editorial workflow

Patterns that govern how multiple sessions, multiple engines, and multiple humans collaborate without corrupting the canonical record.

- [[collab-via-passthrough-relay]] — The passthrough relay pattern holds no document state on the server and forwards CRDT updates directly between clients, keeping the canonical git tree as the sole authoritative record at every point in time.
- [[model-tier-discipline]] — Routing work to the appropriate AI model tier — deep-think, implementation, or mechanical — to match model capability to work shape and control inference cost.
- [[multi-engine-session-coordination]] — How multiple AI engines coordinate on the same workspace without racing on the `.git/index` or each other's session state.
- [[mailbox-atomicity]] — The atomic mailbox primitive that keeps inbox / outbox handoffs across sessions consistent under concurrent writes.

## Interface and user experience

Patterns that recur in the operator-facing chrome — the wiki, the location-intelligence surface, the desktop family.

- [[knowledge-wiki-leapfrog-architecture]] — The wiki engine design: Wikipedia-shaped interface elements over flat Markdown git files, with citation verification, research trail provenance, and AI-integrated editing as the differentiation layer.
- [[location-intelligence-ux]] — The Conclusion-First design philosophy: ranked tier conclusions rather than individual data points, so users see the most defensible commercial nodes at national zoom before drilling into individual operators.
- [[wikipedia-leapfrog-design]] — What the wiki engine inherits from Wikipedia, what it adds beyond it, and what the five-percent leapfrog headroom means.

## See also

- [Substrate](/substrate/) — foundational mechanisms patterns build on
- [Architecture](/architecture/) — concrete platform architecture
- [Applications](/applications/) — operator-facing applications that compose these patterns
- [Systems](/systems/) — the operating systems on which the patterns are realised
