---
schema: foundry-doc-v1
title: "documentation.pointsav.com — Home"
slug: index
category: root
status: pre-build
last_edited: 2026-04-30
editor: pointsav-engineering
---

<!-- ENGINE: render this file at the URL `/` — it is the wiki home,
     served as index.md per content-contract.md §1/§2/§7. -->

PointSav Digital Systems builds the platform substrate for regulated small and
mid-size businesses that need permanent, portable, and verifiable records on
infrastructure they control. This wiki documents the platform's architecture,
services, operating systems, and governance conventions. Articles are written
for engineers, writers, designers, and readers with a financial interest in
the platform. All content is published under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

<!-- ENGINE: insert live TOPIC count: "N articles across 9 categories,
     last updated YYYY-MM-DD." Derive N from count of *.md files in
     category directories (excluding _index.md). Derive date from
     max(last_edited:) across all articles. -->

---

## Platform areas

<!-- ENGINE: render this section as a card grid — 3 columns × 3 rows.
     Each card: category name as heading, description paragraph, link
     to category landing (_index.md), and TOPIC count for that category.
     Category TOPIC counts derive from file count in each directory.
     If a category directory has 0 articles (infrastructure/, company/,
     help/ at launch), still render the card with count "0 articles —
     in preparation." -->

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

**Company** <!-- BCSC: no forward-looking statements in the category
description; company/ articles carry their own FLI labels per Rule 1 -->
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

## Featured article

<!-- ENGINE: read the file `featured-topic.yaml` from the repo root.
     Parse the pinned slug. Fetch that article's title and first
     paragraph. Render as a framed panel with the title, lead
     paragraph, and a "Read more →" link. If the pin file is absent,
     suppress this section entirely — do not render an empty frame.
     featured-topic.yaml schema: slug: (required), since: (optional
     YYYY-MM-DD), note: (optional one-liner; engine ignores). -->

<!-- ENGINE: read featured-topic.yaml, fetch slug article's title + first 100–150 words
     of its lead section. Render as: title (bold), excerpt, "Read more →" link.
     If pin file absent, suppress section. -->

**[[compounding-substrate|The Compounding Substrate]]**

The **Compounding Substrate** is the architectural pattern PointSav builds
and stewards. It answers a single structural question: how does a software
platform let customers own their data, run on their own infrastructure, and
compose AI in or out at will — while still benefiting from collective
improvement without surrendering that ownership? Five structural properties
combine to produce a substrate where every operational interaction generates
training signal that compounds across deployments.

[Read more →](/architecture/compounding-substrate)

*Featured articles represent the wiki's most complete and carefully reviewed content.*

---

## Recent additions

<!-- ENGINE: sort all article files by last_edited: frontmatter date
     descending (fall back to git commit date if last_edited: is
     absent). Render the top 5 as an unordered list:
     "- [Title](/category/slug) — YYYY-MM-DD"
     If fewer than 5 articles exist, render however many there are.
     Do not render this section if the article count is 0.
     Per Q5.A operator ratification: dated-announcement TOPICs
     (filename pattern `topic-*-YYYY-MM-DD.md`) route here rather than
     to permanent category articles. -->

*Most recently added or updated articles:*

<!-- ENGINE: dynamic list — 5 items, last_edited desc -->

---

## Latest updates

<!-- ENGINE: render the 3 most recent entries from CHANGELOG.md or git log
     on the content-wiki-documentation repository (canonical main branch).
     Format: "- YYYY-MM-DD — brief description of what changed"
     If no changelog is available, render the 3 most recent commit messages.
     Static fallback (remove when engine supports dynamic): -->

- 2026-04-29 — Category landing pages added for all nine platform areas
- 2026-04-29 — Home page and featured-article pin established
- 2026-04-27 — Initial platform documentation published

---

## Other areas

Related resources outside this wiki:

- **[PointSav on GitHub](https://github.com/pointsav)** — canonical engineering source; `pointsav/*` organisations host the vendor-tier repositories.
- **[Woodfine Management Corp. on GitHub](https://github.com/woodfine)** — customer-tier mirror; `woodfine/*` organisations host the downstream consumer repositories.
- **[design-system](https://github.com/pointsav/pointsav-design-system)** — visual design tokens, component recipes, and brand conventions.
- **[factory-release-engineering](https://github.com/pointsav/factory-release-engineering)** — licensing matrix, contributor agreements, and governance policies.

<!-- EDITORIAL NOTE: a Woodfine customer-facing wiki is planned.
     Add the link here once the deployment is live. -->

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

---

## Provenance

This artifact derives from research captured at draft time. Q1 and Q2
are now closed; all open questions resolved before this refinement pass.

- Citations consulted: [external:en.wikipedia.org/wiki/Main_Page] (home-page structural patterns); [conventions/cluster-wiki-draft-pipeline.md §3] (velocity tiers, bilingual requirement); [conventions/bcsc-disclosure-posture.md Rule 1] (forward-looking labelling, company/ card and customer-wiki placeholder)
- Workspace references: [naming-convention.md §4, §7, §9] (nine-category set, MOC landing pattern, investor-audience design); [content-contract.md §1, §2, §4, §7, §9] (index.md as home, category: root, URL routing)
- Q1 resolved at refinement: `index.md` confirmed as canonical home filename; `category: root` required.
- Q2 resolved at refinement: `featured-topic.yaml` at repo root with schema `slug:` (required) + `since:` (optional) + `note:` (optional).
- Open editorial item deferred: verify the featured-TOPIC lead paragraph paraphrase against [[compounding-substrate]] §1–2 before the editorial pin is updated post-launch.
