---
schema: foundry-doc-v1
title: "Design Patterns"
slug: patterns-index
category: patterns
type: topic
content_type: topic
quality: complete
short_description: "Named design patterns realised across the platform — source-of-truth inversion, pairing-as-permission, zero-container runtime, zero-execution routing, model-tier discipline, and the passthrough relay among them — each a recurring shape applied at the editorial, interface, or coordination layer."
index_type: thematic
index_scope: patterns
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-09-04
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

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: sovereignty-and-infrastructure-patterns -->
- [[source-of-truth-inversion]] — Source-of-truth inversion designates one storage layer canonical (signed record), a second derived (rebuilt on demand), and a third session-ephemeral (discarded).
- [[pairing-as-permission]] — The Object Capability access-control principle — a cryptographic pairing is the permission, and its absence means no pathway exists to ask for one — as embodied in the platform's machine-based node admission.
- [[zero-container-runtime]] — The structural commitment that every PointSav deployment runs as a Linux binary under systemd on a plain host, with no container runtime or orchestrator.
- [[zero-execution-routing]] — The platform's public homepage templates use a native-CSS checkbox pattern for language toggling and interactive elements, alongside a small amount of client-side JavaScript for page-integrity display and analytics.
- [[customer-first-ordering]] — The principle that a vendor building something a customer will install should build it in the same order the customer installs it, on the same substrate.
- [[totebox-archives-as-the-asset]] — Why a Totebox Archive is designed as a self-contained, freely transferable data unit rather than a database record owned by the platform that created it.
- [[city-code-as-composable-geometry]] — A composition-first pattern that encodes regulatory requirements into element specifications as geometric and numeric constraints rather than applying them post-design, so a non-compliant configuration cannot be placed in the first place.
<!-- END AUTO-GENERATED -->

## Deployment and configuration

The canonical configurations in which the substrate is shipped and the disciplines that keep deployments composable.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: deployment-and-configuration -->
- [[deployment-patterns]] — The six canonical configurations the PointSav substrate is deployed in — each built on the same five primitives and OS surface, adapted per segment.
- [[customer-tier-catalog-pattern]] — Catalog-versus-instance discipline at the customer tier — reusable deployment definitions tracked in git, tenant-specific instances kept out of shared repositories.
<!-- END AUTO-GENERATED -->

## Collaboration and editorial workflow

Patterns that govern how multiple sessions, multiple engines, and multiple humans collaborate without corrupting the canonical record.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: collaboration-and-editorial-workflow -->
- [[collab-via-passthrough-relay]] — A real-time collaborative editing design that held no document state on the server, forwarding CRDT updates directly between clients — implemented in the wiki engine, then removed.
- [[model-tier-discipline]] — The Doorman routes every inference request to one of three compute tiers — local, burst GPU, or external API — based on a complexity hint and live budget state, not a caller's direct choice.
<!-- END AUTO-GENERATED -->

## Interface and user experience

Patterns that recur in the operator-facing chrome — the wiki, the location-intelligence surface, the desktop family.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: interface-and-user-experience -->
- [[knowledge-wiki-leapfrog-architecture]] — Wiki engine strategy serving flat Markdown from git with Wikipedia-shaped chrome, reaching muscle-memory parity before adding a citation and provenance layer.
- [[location-intelligence-ux]] — Conclusion-First interface philosophy rendering ranked tier conclusions rather than individual data points, so defensible commercial nodes surface immediately.
- [[federation-via-content-mounts]] — The wiki engine renders curated articles committed directly to its repository alongside content mounted from separate local directories, sharing one URL surface and search index.
- [[aec-interface-conventions]] — BIM authoring tools across the industry share a common interface vocabulary — a spatial hierarchy, an element properties panel, a 3D viewport, and saved views — because they build on the same underlying IFC data model. The Building Design System's planned interface layer reuses this vocabulary rather than inventing a new one, and is intended to extend it into facility-management workflows.
<!-- END AUTO-GENERATED -->

## See also

- [Building Blocks](/substrate/) — foundational mechanisms patterns build on
- [How It's Built](/architecture/) — concrete platform architecture
- [Applications](/applications/) — operator-facing applications that compose these patterns
- [Operating Systems](/systems/) — the operating systems on which the patterns are realised
