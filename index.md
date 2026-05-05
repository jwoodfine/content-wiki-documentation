---
schema: foundry-doc-v1
title: "documentation.pointsav.com — Home"
slug: index
category: root
status: pre-build
last_edited: 2026-05-05
editor: pointsav-engineering
---

<!-- ENGINE: render this file at the URL `/` — it is the wiki home,
     served as index.md per content-contract.md §1/§2/§7. -->

PointSav's platform documentation covers the architecture, services,
operating systems, and governance conventions of the PointSav substrate.
Articles are written for engineers, writers, designers, and readers with
a financial interest in the platform. All content is published under
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

**Company**
<!-- BCSC: no forward-looking statements in the category description;
     company/ articles carry their own FLI labels per Rule 1 -->
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

[[compounding-substrate]] — The Compounding Substrate describes how
PointSav's platform is designed so that each capability a customer installs
makes the next capability easier to operate. The substrate pattern is the
design philosophy behind the three-ring architecture and the leapfrog-2030
trajectory.

[Read more →](/architecture/compounding-substrate)

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

Corrections and additions follow the staging-tier commit flow described
in [[style-guide-topic]].

---

<div style="font-size: 0.85em; text-align: center; margin-top: 3em; padding-top: 1em; border-top: 1px solid #eaecf0; color: #54595d;">
  <p>Text is available under the <a href="https://creativecommons.org/licenses/by/4.0/" style="color: #0645ad;">Creative Commons Attribution 4.0 International License</a>; additional terms may apply.</p>
  <p>Woodfine Capital Projects™, Woodfine Management Corp™, PointSav Digital Systems™, Totebox Orchestration™, and Totebox Archive™ are trademarks of Woodfine Capital Projects Inc., used in Canada, the United States, Latin America, and Europe. All other trademarks are the property of their respective owners.</p>
</div>
