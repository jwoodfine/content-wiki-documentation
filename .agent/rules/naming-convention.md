# Naming convention and information architecture — content-wiki-documentation

> **Status: Draft.** Proposed 2026-04-23. Awaiting operator
> decisions on the items in §10 before ratification. Once ratified,
> the proposed rules become binding and this file is promoted from
> Draft to Active. Existing content is normalised against it per
> entries in `cleanup-log.md`.
>
> **Scope.** This document governs the human-facing design of the
> wiki: category taxonomy, slug conventions, front-matter
> extensions beyond what the app structurally requires, category-
> landing pattern, stub and redirect conventions. Companion to
> `content-contract.md` (which governs what the rendering app
> structurally enforces).

Last updated: 2026-04-23.

---

## 1. Why this file exists

The content repo feeds a public wiki (`app-mediakit-knowledge`
serving `documentation.pointsav.com`). The rendering app enforces
a small number of structural rules — front-matter schema, two-
level URL depth, wikilink syntax, footnote syntax. Those rules are
in `content-contract.md`. They are necessary but not sufficient.

What they do not specify:

- Which top-level categories exist and what goes in each.
- How slugs are composed across a corpus that must stay coherent
  for decades.
- What front-matter fields a machine-readable 2030-era wiki needs
  beyond the minimum the current app parses.
- How category landing pages are organised so a flat IA remains
  legible to human readers.
- How stub articles, redirects, and the "wanted articles" backlog
  are represented.
- How the wiki addresses a non-engineering audience (the financial
  community) alongside engineers, writers, and designers.

This file fills those gaps.

## 2. Design intent — "leapfrog 2030 Wikipedia"

The operator's stated design goal: *"a leapfrog 2030 coding
version of Wikipedia, with the same muscle memory as Wikipedia,
but built on a flat architecture so it stays machine readable."*

Translated into concrete design principles:

1. **Muscle memory.** A reader who knows Wikipedia recognises the
   layout immediately — article title, lead paragraph, TOC on the
   side, references footer, red links for missing articles,
   hatnotes for disambiguation.
2. **Flat architecture.** URL depth is capped at two, categories
   are siblings not parents, and hierarchical meaning is recovered
   through metadata and MOC landing pages rather than filesystem
   nesting.
3. **Machine readable by default.** Every article carries rich,
   predictable front-matter. The contract is written down and
   versionable. Semantic relationships between articles are
   explicit fields, not implicit prose. Machine consumers (search
   crawlers, RAG systems, future ML agents) can parse the corpus
   without bespoke adapters.
4. **Multi-audience.** The same wiki serves engineers, writers,
   designers, and the financial community. Taxonomy accommodates
   this explicitly rather than by accident.

## 3. Research basis

The naming and IA conventions below are informed by a research
pass conducted 2026-04-23 covering current (2024–2026) practice
in git-backed Markdown wikis, machine-readable documentation
standards, and the information architectures of major engineering
documentation sites (Stripe, Cloudflare, Astral, Linear, Vercel,
ClickHouse).

**Caveat on research method.** The research pass did not have live
web access; findings are knowledge-based as of January 2026 and
should be treated as high-confidence on well-established patterns
and medium-confidence on emerging conventions. Source links are
preserved in §12 for spot-checking when conventions firm up.

Compressed findings that drove the proposal below:

- **Highest-leverage single change to the current schema: add a
  stable `id:` field separate from `slug:`.** Without a stable ID,
  slugs must be immortal; renames break every inbound link. This
  is the mistake MDN, Stripe, and Notion all corrected after
  scale. Cheap now; expensive to retrofit.
- **`subcategory:` is rotting.** The URL ignores it; no build
  reads it; the contract does not constrain its values. Every
  modern system treats front-matter either as routing input or as
  search-facet input. A field that is neither will decay.
- **Category landing pages should be Maps of Content (MOCs), not
  auto-generated file listings.** Prose + curated groupings. This
  is what makes a flat IA legible to humans.
- **`type:` field with a closed entity vocabulary** is mainstream
  2024–2026 practice. Enables JSON-LD emission, search facets,
  and RAG chunk typing.
- **Keep entity-type prefixes in slugs** (`service-email`,
  `os-totebox`, `sys-adr-07`). Aligns with the workspace
  Nomenclature Matrix and makes a flat filesystem self-
  documenting. Cost: longer slugs. Worth it.
- **The "serve both engineers and investors" design call is
  unusual.** Every major precedent (Stripe, Cloudflare, Linear)
  splits these audiences across domains. The operator's vision
  wants both here; the right response is a first-class `company/`
  category with a non-technical MOC landing, not burying investor
  material inside engineering sections.
- **`status: stub` + auto-generated `/wanted` page** from
  unresolved wikilinks is a contributor-experience win at near-
  zero cost.

## 4. Proposed top-level category set

Nine categories. Placed at repo root as sibling directories. Each
maps to the URL `/<category>` route and carries a `_index.md`
MOC landing.

| Category | Purpose | Primary audience | Example articles |
|---|---|---|---|
| `architecture/` | Cross-cutting platform architecture — layers, principles, invariants | Engineers | `three-layer-stack`, `archive-types`, `platform-invariants` |
| `systems/` | Operating systems (`os-*`) — one article per OS | Engineers | `os-totebox`, `os-workplace`, `os-mediakit`, `os-orchestration` |
| `services/` | Autonomous services (`service-*`) — one article per service | Engineers | `service-email`, `service-people`, `service-slm`, `service-content`, `service-egress` |
| `applications/` | User-facing and internal apps (`app-*`) | Engineers, designers | `app-mediakit-knowledge`, `app-workplace-presentation` |
| `governance/` | ADRs, licensing, release engineering, compliance | Engineers, financial community | `sys-adr-07`, `sys-adr-19`, `licensing-matrix`, `release-engineering-process` |
| `infrastructure/` | Fleet deployment, cloud topology, operational runtime | Engineers, financial community | `fleet-infrastructure-cloud`, `deployment-topology`, `observability` |
| `company/` | Organisational structure, roles, roadmap, financial disclosures | **Financial community**, general public | `pointsav`, `woodfine-management-corp`, `woodfine-capital-projects`, `roadmap-2026-2028`, `bcsc-disclosures` |
| `reference/` | Glossary, nomenclature, style guide, templates | Writers, engineers | `glossary`, `nomenclature-matrix`, `style-guide`, `article-template` |
| `help/` | Contributor onboarding per audience | Future contributors | `contributing-as-engineer`, `contributing-as-writer`, `contributing-as-designer`, `proposing-an-adr` |

Rationale:

- Nine sits in the 6–10 range the research identifies as common
  across major engineering documentation sites.
- Each is materially distinct from its neighbours:
  - `architecture` (cross-cutting logical) vs `systems` (per-OS)
    vs `services` (per-service) vs `applications` (per-app) — the
    platform's own taxonomy from the Nomenclature Matrix.
  - `governance` (formal technical decisions, ADRs) vs `company`
    (organisational, financial, investor-facing) — kept separate
    because they serve different audiences at different depths.
  - `infrastructure` (physical / deployed runtime) vs
    `architecture` (abstract / logical). Blurry edge; the rule is
    deployment artefacts go in `infrastructure`, design intent
    goes in `architecture`.
  - `reference` (definitional) vs `help` (procedural). "What is
    X" vs "how do I do X".

Mapping of existing legacy files to the new taxonomy is a separate
migration tracked in `cleanup-log.md`.

## 5. Slug rules

Extends `content-contract.md` §3.

| Rule | Value |
|---|---|
| Case | Lowercase ASCII only |
| Word separator | Single hyphen (kebab) |
| Length | Target 3–6 words, under 60 characters |
| Singular vs plural | Singular for concept / entity articles; plural for collection landings (`services/_index.md`, not `service/_index.md`) |
| Entity-type prefix | Keep for entities named in the Nomenclature Matrix: `os-*`, `service-*`, `app-*`, `sys-adr-*`, `fleet-*`. Do not prefix concept articles. |
| Plain slug | For concepts not covered by a Nomenclature prefix: `three-layer-stack`, `capability-based-security`, `glossary`, `style-guide` |
| Uniqueness | Globally unique across all categories (the wikilink resolver is flat) |
| Immortality | A published slug is never changed. Renames happen via redirects (see §8), not mutation. |

**Why entity prefixes are kept.** The workspace Nomenclature
Matrix assigns prefixes to Matrix-listed entity types. Preserving
the prefix in the article slug keeps the filesystem self-
documenting and the slug self-disambiguating (no `email.md` that
could mean the service, the app feature, or the protocol). Stripe-
style docs do not prefix because their platform has a broader
public taxonomy; PointSav's is closed and Matrix-defined.

## 6. Proposed front-matter schema (extends `content-contract.md` §4)

The current schema carries 8 fields. The proposed final schema
carries 14 — six additions, one removal, one value extension.
This is a **structural change to the contract**: the rendering
app's `ArticleMeta` struct must update in lockstep.

**Window for this change.** The crate is currently a ZIP awaiting
handoff to `pointsav-monorepo` per `handoffs-outbound.md`. Schema
changes land cleanly if adopted before the crate's first build in
the monorepo. After that, it becomes a versioned contract
migration.

| Field | In contract today | Proposed action | Rationale |
|---|---|---|---|
| `id` | — | **Add** (required). ULID or UUIDv7. Stable for article life. | Survives renames. Single highest-leverage change. |
| `title` | yes | keep | — |
| `slug` | yes | keep; **now immortal after publish** | URL stability |
| `type` | — | **Add** (required). Closed enum: `concept \| os \| service \| app \| adr \| person \| organization \| governance \| financial-disclosure \| reference \| help` | Entity typing, JSON-LD, RAG chunk typing, search facets |
| `category` | yes | keep | — |
| `subcategory` | yes | **Remove** | Rotting; no build reads it |
| `tags` | — | **Add** (optional). List of kebab strings. Cross-cutting dimensions: `foundation-layer`, `delivery-layer`, `q3-2026`, `public`, `internal`, etc. | Proper multi-dimensional classification; replaces what subcategory tried to be |
| `status` | yes | **Extend** enum: `stable \| pre-build \| draft \| stub` | Explicit stub state enables `/wanted` generation |
| `last_edited` | yes | keep | — |
| `editor` | yes | keep | — |
| `aliases` | — | **Add** (optional). List of old slugs that redirect to this article. | Rename-without-breakage |
| `relates_to` | — | **Add** (optional). List of slugs. | Named-relations vocabulary |
| `supersedes` | — | **Add** (optional). Slug. | ADR / policy succession |
| `superseded_by` | — | **Add** (optional). Slug. Auto-derivable from reverse `supersedes`. | Reverse relation |
| `implements` | — | **Add** (optional). Slug. | e.g., a service `implements: sys-adr-07` |
| `see_also` | — | **Add** (optional). List of slugs. | Lightweight cross-reference |
| `references` | yes | keep | Numeric footnote bibliography |

## 7. Category landings — MOCs, not listings

Each `<category>/_index.md` is a **curated Map of Content**:

- A prose paragraph introducing what the category covers and why.
- Hand-grouped links organised by sub-theme, not alphabetical
  listing. E.g., `services/_index.md` groups services under
  "Content services" / "Identity services" / "Communication
  services".
- May include cross-category pointers where helpful.
- Auto-generated completeness list comes from the app's separate
  route walker — it is not maintained by hand.

The app renders `_index.md` content *above* the auto-list.
Category landings supply editorial context; the auto-list supplies
completeness. Both are shown, not one or the other.

## 8. Stubs, redirects, wanted articles

**Stubs.** `status: stub` on a minimal article (title, one-
sentence stub summary, `TODO` body). Renders normally; counted
separately in build-time reports so contributors can find
gaps.

**Redirects — two mechanisms.**

1. **Front-matter `aliases:`** for slugs that formerly pointed to
   the current article. The app consults `aliases` at wikilink-
   resolution time: `[[old-slug]]` resolves to the article that
   lists `old-slug` under `aliases`. Keep the alias forever once
   it has been published in any URL.
2. **Root-level `redirects.yaml`** for URL-path redirects without
   a current article equivalent (e.g., old `/topic-service-email`
   → `/services/service-email`). Maintained as part of the
   migration sweep. The app emits 301 responses for these paths.

**Wanted articles.** The app builds `/wanted` at render time by
scanning every rendered article's unresolved wikilinks, sorted by
inbound-link count. This is a new category landing served by the
app but not backed by a file in this repo. Contributors browse
`/wanted` to choose what to write next.

## 9. The investor-audience design call

**Proposed disposition:** accept the operator's vision to serve
engineers and the financial community from the same wiki, and
give investor material a first-class category (`company/`) with a
non-technical MOC landing.

`company/` holds:

- **Corporate entities**: one article per legal entity
  (`pointsav`, `woodfine-management-corp`,
  `woodfine-capital-projects`).
- **Leadership and roles**: at the level the BCSC disclosure rule
  permits; no individual personal data beyond roles and published
  titles.
- **Roadmap**: forward-looking but framed in planned / intended
  terms per the BCSC disclosure rule (workspace §6).
- **Financial disclosures**: formal disclosure documents, BCSC
  filings, and related governance-to-market communications.

`company/_index.md` opens with plain-language framing ("What
PointSav does and how it is organised"), not with engineering
vocabulary. First link targets on the landing are `pointsav`,
`roadmap-2026-2028`, `bcsc-disclosures`.

**Alternative if this proposal is rejected.** Investor material
splits to a separate domain (e.g., `about.pointsav.com`) and this
wiki drops `company/` entirely. Either disposition is coherent.
The one to avoid is "serve both audiences without naming the
tradeoff," which produces compromised IA for both.

## 10. Pending operator decisions

Ratification of this draft requires the operator to decide:

1. **Category set.** Accept the nine-category proposal, or revise?
   Specifically: are `company/` and `governance/` both needed?
   Is `infrastructure/` distinct from `architecture/` at this
   scale?
2. **Investor audience.** Accept `company/` as first-class
   category (§9 primary proposal), or redirect investors
   elsewhere and drop `company/`?
3. **Front-matter schema changes.** Accept the six additions
   (`id`, `type`, `tags`, `aliases`, named relations, extended
   `status`) and one deletion (`subcategory`)? Staged adoption
   is acceptable — which go in the first pass?
4. **ID format.** ULID (26 chars, time-ordered, typographically
   compact), UUIDv7 (36 chars, time-ordered, standard), or other?

Decisions are recorded as an addendum to this file below §13
when made.

## 11. Relationship to other rule files

| File | What it governs |
|---|---|
| `content-contract.md` | **Structural rules the app enforces.** Front-matter schema as the app parses it, URL routes, wikilink syntax, footnote syntax. Changes require crate-side changes in lockstep. |
| `naming-convention.md` *(this file)* | **Human-design rules layered on top of the contract.** Category taxonomy, slug composition, front-matter extensions proposed, MOC pattern, stub / redirect / wanted conventions, investor-audience design. |
| `repo-layout.md` | **File-placement rules.** Allowed files at repo root, defect-closure procedure. |
| `cleanup-log.md` | **In-flight cleanup state.** Records decisions made during migrations against the rules above. |
| `handoffs-outbound.md` | **Cross-repo file moves.** Currently tracking the crate move to `pointsav-monorepo`. |

All are read at session start by a Root Claude opening in this
repo, per workspace §10.

## 12. Source references

External references consulted during the 2026-04-23 research
pass:

- Wikipedia:Article_titles — <https://en.wikipedia.org/wiki/Wikipedia:Article_titles>
- Wikipedia:Disambiguation — <https://en.wikipedia.org/wiki/Wikipedia:Disambiguation>
- Quartz v4 — <https://quartz.jzhao.xyz/>
- Astro Starlight — <https://starlight.astro.build/>
- Docusaurus — <https://docusaurus.io/>
- MkDocs Material — <https://squidfunk.github.io/mkdocs-material/>
- VitePress — <https://vitepress.dev/>
- Nextra — <https://nextra.site/>
- Fumadocs — <https://fumadocs.vercel.app/>
- schema.org — <https://schema.org/>
- Dublin Core — <https://www.dublincore.org/specifications/dublin-core/dcmi-terms/>
- SKOS — <https://www.w3.org/2004/02/skos/>
- llms.txt — <https://llmstxt.org/>
- ADR community — <https://adr.github.io/>
- Anthropic contextual retrieval — <https://www.anthropic.com/engineering/contextual-retrieval>
- Major engineering docs studied: Stripe (<https://stripe.com/docs>),
  Cloudflare Developers (<https://developers.cloudflare.com/>),
  Astral (<https://docs.astral.sh/>),
  Linear (<https://linear.app/docs>),
  Vercel (<https://vercel.com/docs>),
  ClickHouse (<https://clickhouse.com/docs>)

## 13. Decision log

*(empty until operator decisions are recorded)*
