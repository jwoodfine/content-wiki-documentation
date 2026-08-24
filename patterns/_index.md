---
schema: foundry-doc-v1
title: "Design patterns"
slug: patterns-index
category: patterns
type: topic
content_type: topic
quality: complete
short_description: "The patterns category collects named design patterns realised across the platform — source-of-truth inversion, pairing-as-permission, zero-container runtime, zero-execution routing, customer-first ordering, model-tier discipline, deployment patterns, the passthrough relay, the knowledge-wiki leapfrog architecture, and the location-intelligence UX — each a recurring shape applied at the editorial, interface, or coordination layer."
index_type: thematic
index_scope: patterns
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-08-06
editor: pointsav-engineering
paired_with: _index.es.md
---

The **patterns** category collects named design patterns realised across the platform. A pattern in this category is a recurring shape — applied at the editorial, interface, or coordination layer — that solves a structural problem in a way other parts of the platform reuse. Patterns differ from substrates: a substrate is a load-bearing mechanism the platform depends on (and that compounds over time); a pattern is a design choice that can be applied or not. Patterns differ from architecture: an architecture article describes how a specific system is composed; a pattern describes a shape that recurs across systems.

Patterns in this collection sit on top of the [[compounding-substrate]] and the [[three-ring-architecture]] — they describe how the platform expresses those foundations in recurring, named shapes.

<!-- START-HERE-HIGHLIGHT: engine reads this block to render the single "start here" card
     (reuses the existing cluster-card--start-here component). Do not add more than one. -->

**Start here:** read [[source-of-truth-inversion]] and [[pairing-as-permission]] first — they are the load-bearing patterns that the others build on.

<!-- END-START-HERE-HIGHLIGHT -->

## Sovereignty and infrastructure patterns

The structural commitments that define what a PointSav deployment is and is not.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: sovereignty-and-infrastructure -->
- [[source-of-truth-inversion]] — Designates one layer as canonical (signed, committed), a second as a deterministically rebuilt view, and a third as session-ephemeral; eliminates entire classes of sync and data-loss bugs.
- [[pairing-as-permission]] — The Object Capability access-control principle — a cryptographic pairing is the permission, its absence means no pathway — as embodied in the platform's machine-based node admission.
- [[zero-container-runtime]] — Every deployment runs as a Linux binary under systemd on a plain VM or bare-metal host; no container runtime, no container orchestrator, no managed-runtime platform.
- [[zero-execution-routing]] — The platform's public homepage templates use a native-CSS checkbox pattern for language toggling and interactive elements, alongside a small amount of client-side JavaScript for page-integrity display and analytics.
- [[customer-first-ordering]] — A software vendor building something a customer will install should build it in the same order the customer will install it, on the same substrate the customer will use.
- [[customer-hostability]] — The architectural commitment that every artefact runs on the customer's own hardware, against the customer's own keys, with the customer's own audit ledger.
- [[totebox-archives-as-the-asset]] — Why a Totebox Archive is a self-contained, freely transferable data unit rather than a database record owned by the platform that created it.
<!-- END AUTO-GENERATED -->

## Deployment and configuration

The canonical configurations in which the substrate is shipped and the disciplines that keep deployments composable.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: deployment-and-configuration -->
- [[deployment-patterns]] — The six canonical configurations in which the PointSav substrate is deployed — each built on the same five primitives and OS surface, with the Chart of Accounts and compliance surface adapted per segment.
- [[three-layer-architecture]] — How PointSav deliverables move through SOFTWARE, SHOWCASE, and INSTANCE layers with a strict one-way vendor-to-customer flow.
- [[3-layer-stack]] — The three-layer infrastructure decomposition: raw compute capability, isolated platform execution, and secure operator access.
- [[customer-tier-catalog-pattern]] — Separates deployment catalog entries (tenant-agnostic, git-tracked in the fleet-deployment repository) from numbered instances (tenant-specific, gitignored); the prefix taxonomy and path structure make catalog-versus-instance visible without reading a MANIFEST.
<!-- END AUTO-GENERATED -->

## Collaboration and editorial workflow

Patterns that govern how multiple sessions, multiple engines, and multiple humans collaborate without corrupting the canonical record.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: collaboration-and-editorial-workflow -->
- [[collab-via-passthrough-relay]] — A real-time collaborative editing design that held no document state on the server, forwarding CRDT updates directly between clients — implemented in the wiki engine, then removed.
- [[model-tier-discipline]] — The Doorman routes every inference request to one of three compute tiers — local, burst GPU, or external API — based on a complexity hint and live budget state, not a caller's direct choice.
- [[multi-engine-session-coordination]] — How multiple AI engines coordinate on the same workspace without racing on the `.git/index` or each other's session state.
- [[mailbox-atomicity]] — The atomic mailbox primitive that keeps inbox / outbox handoffs across sessions consistent under concurrent writes.
<!-- END AUTO-GENERATED -->

## Interface and user experience

Patterns that recur in the operator-facing chrome — the wiki, the location-intelligence surface, the desktop family.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: interface-and-user-experience -->
- [[knowledge-wiki-leapfrog-architecture]] — The wiki engine design: Wikipedia-shaped interface elements over flat Markdown git files, with citation verification, research trail provenance, and AI-integrated editing as the differentiation layer.
- [[location-intelligence-ux]] — The Conclusion-First design philosophy: ranked tier conclusions rather than individual data points, so users see the most defensible commercial nodes at national zoom before drilling into individual operators.
- [[wikipedia-leapfrog-design]] — What the wiki engine inherits from Wikipedia, what it adds beyond it, and what the five-percent leapfrog headroom means.
- [[federation-via-content-mounts]] — The wiki engine renders curated articles committed directly to its repository alongside content mounted from separate local directories, sharing one URL surface and search index.
<!-- END AUTO-GENERATED -->

## See also

- [Substrate](/substrate/) — foundational mechanisms patterns build on
- [Architecture](/architecture/) — concrete platform architecture
- [Applications](/applications/) — operator-facing applications that compose these patterns
- [Systems](/systems/) — the operating systems on which the patterns are realised
