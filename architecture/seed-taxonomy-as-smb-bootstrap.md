---
schema: foundry-doc-v1
title: "Seed Taxonomy as SMB Bootstrap"
slug: seed-taxonomy-as-smb-bootstrap
category: architecture
type: topic
quality: published
short_description: "Every Foundry tenant deployment provisions a four-part seed taxonomy — Archetypes, Chart of Accounts, Domains, Themes — as the knowledge graph bootstrap."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-01
editor: pointsav-engineering
cites: []
paired_with: seed-taxonomy-as-smb-bootstrap.es.md
---

Every Foundry tenant deployment begins with a **seed taxonomy**: a compact, hand-tunable four-part structure that forms the initial scaffold of the per-tenant knowledge graph. The four parts are Archetypes, Chart of Accounts, Domains, and Themes. Each entity carries gravity keywords — explainable keyword anchors that drive classification of incoming content. This pattern encodes Doctrine claim #47.

## The four parts

**Archetypes — who acts.** Five to seven role-by-cognitive-pattern identities. The Foundry default carries five universal roles that appear in some form in every business regardless of industry: the Executive (Strategic Direction), the Guardian (Risk and Compliance), the Fiduciary (Resource Integrity), the Architect (System Design), and the Constructor (Physical Realization). Industry-specific roles are added via [[vertical-seed-packs-marketplace]].

**Chart of Accounts — what business this is.** Five to ten industry-specific business profiles, each with an identifier, a profile name, a sub-domain, and gravity keywords. The profiles mirror the business's actual revenue and expense categories. A property development firm's Chart of Accounts looks different from a law firm's or a regional hospital's; the form is consistent while the substance is industry-specific.

**Domains — macro categories of work.** Three to five macro categories that group work units. The Foundry default provides Corporate, Projects, and Documentation. Each Domain holds a Glossary and Topic collection that structure the wiki content, composed through the editorial pipeline.

**Themes — time-bound initiatives.** Four to ten active themes representing current strategic focus. Each Theme carries an identifier, a short name, and gravity keywords. Themes are the most volatile part of the taxonomy — they may change quarterly as initiatives open and close.

## The gravity_keywords mechanism

Classification of new content into the taxonomy uses keyword matching rather than embedding similarity. When a document arrives, the extraction service counts keyword matches against each Archetype, Chart of Accounts profile, Domain, and Theme entity. The entity with the highest match count is the proposed classification.

This approach is deliberate. Keyword-based classification is explainable: "this document was classified as Real Estate because the terms Leasing, Office, and Industrial matched" is a statement an operator can read and verify. An embedding similarity score is not. Keyword classification is auditable — the classification path is reproducible across model versions, which matters for regulatory record-keeping. And it is hand-tunable: an operator who sees a misclassification edits the gravity keywords list. Retraining an embedding model is not a practical operation for a small business.

Embedding similarity is provided at a separate layer to augment keyword classification when explicit keywords miss. It does not replace the keyword mechanism.

## Provisioning a new tenant

When a new Foundry tenant is provisioned, the operator selects a Vertical Seed Pack (see [[vertical-seed-packs-marketplace]]) appropriate to their industry. The service imports the pack's JSON files into the per-tenant graph. The operator then customizes the result — adding, editing, or removing entities — using the TUI. A typical small business is intended to complete the review and customization in approximately 30 minutes.

## Structural difference from enterprise ontology approaches

Enterprise software platforms tend to optimize their ontologies for completeness across all possible customers. Any specific customer faces an extensive hierarchy and typically requires specialist staff to configure it for their needs.

Foundry's seed taxonomy optimizes for actionability for one specific customer. The entire taxonomy is intended to be readable and understandable by the customer's own operators in a single session. The trade-off is that the taxonomy does not transfer unchanged between customers — each vertical pack is industry-specific. The benefit is that the customer can operate the taxonomy themselves without engaging ontology specialists.

## Relationship to the knowledge graph

The seeded taxonomy becomes the initial structure of the per-tenant knowledge graph in `service-content`. Every Archetype, Chart of Accounts profile, Domain, and Theme entity is a graph node. As the deployment operates, new entities discovered during inference (with accepted verdicts) are added to the graph, growing the taxonomy organically from actual use.

The [[knowledge-graph-grounded-apprenticeship]] pattern depends on this seeded graph: the graph provides the grounding context for every subsequent inference request.

## See Also

- [[vertical-seed-packs-marketplace]] — industry-specific packs that populate the seed taxonomy at provisioning
- [[knowledge-graph-grounded-apprenticeship]] — the seeded graph is the grounding source for inference
- [[customer-owned-graph-ip]] — the customer's customized taxonomy is their intellectual property

## References

1. Doctrine claim #47 — Seed Taxonomy as SMB Bootstrap (ratified v0.1.0).
2. Reference implementation: `vendor/pointsav-monorepo/service-content/seeds/` — Woodfine deployment seed (five Archetypes, four Chart of Accounts profiles, three Domains, four active Themes).

---

## Provenance

Source: `convention-seed-taxonomy-as-smb-bootstrap.md` (refined 2026-04-30). Workspace-internal file paths and open questions removed. No forward-looking commercial claims present in this convention.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*

*Woodfine Capital Projects™, Woodfine Management Corp™, PointSav Digital Systems™, Totebox Orchestration™, and Totebox Archive™ are trademarks of Woodfine Capital Projects Inc., used in Canada, the United States, Latin America, and Europe. All other trademarks are the property of their respective owners.*
