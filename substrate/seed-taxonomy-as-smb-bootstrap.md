---
schema: foundry-doc-v1
title: "Seed taxonomy as SMB bootstrap"
slug: seed-taxonomy-as-smb-bootstrap
category: substrate
type: topic
content_type: topic
quality: complete
index_group: platform-mechanics
short_description: "Every tenant deployment provisions a four-part seed taxonomy — Archetypes, Chart of Accounts, Domains, Themes — as the knowledge graph bootstrap."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-08-22
editor: pointsav-engineering
cites: []
paired_with: seed-taxonomy-as-smb-bootstrap.es.md
---

Every tenant deployment begins with a **seed taxonomy**: a compact, hand-tunable four-part structure that forms the initial scaffold of the per-tenant [[knowledge-graph-grounded-apprenticeship|knowledge graph]]. The four parts are Archetypes, Chart of Accounts, Domains, and Themes. Each entity carries gravity keywords — explainable reference text an operator reads while classifying new content into [[service-content|the taxonomy]].

## The four parts

**Archetypes — who acts.** Eleven role-by-cognitive-pattern identities, each with a name, a signature (its core function), a "healing trigger" (the failure mode the role exists to catch), and gravity keywords — for example the Executive (Strategic Direction, triggered by Stagnation) or the Guardian (Risk and Compliance, triggered by Breach). The set spans strategic, operational, and physical-realization roles. Industry-specific roles are added via [[vertical-seed-packs-marketplace]].

**Chart of Accounts — who holds what role, not what business this is.** Despite the name, this is not an industry or revenue/expense classification — it is a personnel-role taxonomy, organized into sub-domains (personal governance roles, compliance, finance, and several others), each entry carrying a reference number, a role type, and gravity keywords for classifying a person's title or function against it.

**Domains — macro categories of work.** Macro categories that group work units, each backed by its own seed file. The default provides Corporate, Projects, and Documentation. Each Domain holds a Glossary and Topic collection that structure the wiki content, composed through the editorial pipeline.

**Themes — time-bound initiatives.** Active themes representing current strategic focus, each with an identifier, a name, a scope (tactical or strategic), a one-line thesis, and gravity keywords. Themes are the most volatile part of the taxonomy and are genuinely tenant-specific — real deployments seed real, often commercially sensitive strategic priorities here, not a generic template set.

## The gravity_keywords field

Every taxonomy entity carries gravity keywords, but their role today is narrower than an automated matcher: they are reference text a human operator reads before making a classification decision, not an input to an automated match-counting or embedding-similarity system. In the platform's one confirmed real consumer — the [[radical-proofreader-ui|Verification Surveyor]] workflow — an operator reviewing a discovered entity is shown the list of Archetype names and picks one manually; the gravity keywords guide that human judgment rather than driving it programmatically.

The explainability goal the field is designed for still holds even under manual selection: an operator can read a taxonomy entity's gravity keywords and understand why an entity would or wouldn't belong to it, and can hand-edit the keyword list when a category needs to be redefined. Whether an automated keyword-match or embedding-based classifier is added on top of this manual step is a design the platform has not yet built.

## Provisioning a new tenant

When a new tenant is provisioned, the operator selects a Vertical Seed Pack (see [[vertical-seed-packs-marketplace]]) appropriate to their industry. The [[service-content|service]] imports the pack's JSON files into the per-tenant graph. The operator then customizes the result — adding, editing, or removing entities — using the [[tui-corpus-producer|TUI]]. A typical small business is intended to complete the review and customization in approximately 30 minutes.

## Structural difference from enterprise ontology approaches

Enterprise software platforms tend to optimize their ontologies for completeness across all possible customers. Any specific customer faces an extensive hierarchy and typically requires specialist staff to configure it for their needs.

The platform's seed taxonomy optimizes for actionability for one specific customer. The entire taxonomy is intended to be readable and understandable by the customer's own operators in a single session. The trade-off is that the taxonomy does not transfer unchanged between customers — each vertical pack is industry-specific. The benefit is that the customer can operate the taxonomy themselves without engaging ontology specialists.

## Relationship to the knowledge graph

The seeded taxonomy becomes the initial structure of the per-tenant knowledge graph in [[service-content]]. Every Archetype, Chart of Accounts profile, Domain, and Theme entity is a graph node. As the deployment operates, new entities discovered during inference (with accepted verdicts from the [[compounding-doorman|Doorman]]) are added to the graph, growing the taxonomy organically from actual use.

The [[knowledge-graph-grounded-apprenticeship]] pattern depends on this seeded graph: the graph provides the grounding context for every subsequent inference request.

## See also

- [[vertical-seed-packs-marketplace]] — industry-specific packs that populate the seed taxonomy at provisioning
- [[knowledge-graph-grounded-apprenticeship]] — the seeded graph is the grounding source for inference
- [[customer-owned-graph-ip]] — the customer's customized taxonomy is their intellectual property
