---
schema: foundry-doc-v1
title: "PointSav Knowledge"
slug: index
category: root
status: stable
last_edited: 2026-05-01
editor: pointsav-engineering
---

The **Leapfrog 2030 Architecture** is a substrate commitment: customers own
their hardware, their data, their adapter weights, and their business
relationships. PointSav provides the substrate; the customer operates it.
Every operational interaction is intended to generate training signal that
compounds across deployments — building a specialist AI layer the customer
owns, not one they rent. This wiki documents that architecture, the services
built on it, and the governance conventions that hold it together.
All content is published under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

---

## Platform areas

**Architecture**
Design principles, substrate patterns, and cross-cutting invariants that
govern how the platform is built. Covers the three-ring stack, compounding
substrate, AI routing, cryptographic audit, and the editorial pipeline.
→ [Browse architecture](/architecture/)

**Services**
Autonomous services implementing Ring 1 and Ring 2 of the three-ring
architecture: ingest, processing, search, egress, and the linguistic
air-lock.
→ [Browse services](/services/)

**Systems**
The operating systems at the foundation layer: ToteboxOS and its
seL4-based capability model, orchestration, and tenant isolation.
→ [Browse systems](/systems/)

**Applications**
User-facing and internal applications built on the platform substrate,
including the wiki engine that serves this site.
→ [Browse applications](/applications/)

**Governance**
Architecture decision records, licensing posture, contributor model,
and compliance conventions.
→ [Browse governance](/governance/)

**Infrastructure**
Fleet deployment, cloud topology, and operational runtime.
In preparation — articles are planned for this category.
→ [Browse infrastructure](/infrastructure/)

**Company**
Corporate entities, organisational structure, and public disclosures.
→ [Browse company](/company/)

**Reference**
Glossary, nomenclature matrix, and style guides for contributors across
all audiences.
→ [Browse reference](/reference/)

**Help**
Onboarding guides for engineers, writers, and designers contributing to
the platform and its documentation.
→ [Browse help](/help/)

---

## Other areas

Related resources outside this wiki:

- **[PointSav on GitHub](https://github.com/pointsav)** — canonical engineering source; `pointsav/*` organisations host the vendor-tier repositories.
- **[Woodfine Management Corp. on GitHub](https://github.com/woodfine)** — customer-tier mirror; `woodfine/*` organisations host the downstream consumer repositories.
- **[design-system](https://github.com/pointsav/pointsav-design-system)** — visual design tokens, component recipes, and brand conventions.
- **[factory-release-engineering](https://github.com/pointsav/factory-release-engineering)** — licensing matrix, contributor agreements, and governance policies.

---

## Contributing

This wiki is published under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
Content originates from the PointSav and Woodfine contributor flow.
See [[contributing-as-engineer]], [[contributing-as-writer]], and
[[contributing-as-designer]] for onboarding guides. These articles are
planned for the help/ category; they will render as red links until written.

Articles are graded **Complete**, **Core**, or **Stub** based on lead length,
section count, and reference completeness. Stub articles display an
expansion notice and are the highest-priority contribution targets.

Corrections and additions follow the staging-tier commit flow described
in [[style-guide-topic]].
