# Naming convention and information architecture — content-wiki-documentation

> **Status: Active.** Proposed 2026-04-23. Ratified 2026-05-07.
> Operator decisions on the four §10 items are recorded in §13.
> The rules in this file are binding. Existing content is
> normalised against it per entries in `cleanup-log.md`.
>
> **Scope.** This document governs the human-facing design of the
> wiki: category taxonomy, slug conventions, front-matter
> extensions beyond what the app structurally requires, category-
> landing pattern, stub and redirect conventions. Companion to
> `content-contract.md` (which governs what the rendering app
> structurally enforces).

Last updated: 2026-05-07.

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

## 4. Top-level category set

Ten categories. Placed at repo root as sibling directories. Each
maps to the URL `/<category>` route and carries a `_index.md`
MOC landing.

| Category | Purpose | Primary audience | Example articles |
|---|---|---|---|
| `architecture/` | Cross-cutting platform architecture, doctrine, concrete systems composition | Engineers | `three-ring-architecture`, `foundry-doctrine-architecture`, `doorman-protocol`, `totebox-orchestration-development` |
| `substrate/` | Foundational mechanism concepts — substrates, primitives, disciplines | Engineers, financial community | `compounding-substrate`, `apprenticeship-substrate`, `citation-substrate`, `disclosure-substrate`, `language-protocol-substrate` |
| `patterns/` | Named design patterns recurring across the platform | Engineers, designers | `source-of-truth-inversion`, `pairing-as-permission`, `reverse-funnel-editorial-pattern`, `wikipedia-leapfrog-design` |
| `systems/` | Operating systems (`os-*`) — one article per OS | Engineers | `os-totebox`, `os-workplace`, `os-mediakit`, `os-orchestration` |
| `services/` | Autonomous services (`service-*`) — one article per service | Engineers | `service-email`, `service-people`, `service-slm`, `service-content`, `service-egress` |
| `applications/` | User-facing and internal apps (`app-*`) | Engineers, designers | `app-mediakit-knowledge`, `app-workplace-presentation` |
| `governance/` | ADRs, licensing, release engineering, compliance | Engineers, financial community | `sys-adr-07`, `sys-adr-19`, `licensing-matrix`, `release-engineering-process` |
| `infrastructure/` | Fleet deployment, cloud topology, storage, network, telemetry | Engineers, financial community | `fleet-infrastructure-cloud`, `worm-ledger-architecture`, `sovereign-mesh`, `sovereign-telemetry` |
| `reference/` | Glossary, nomenclature, style guide, templates | Writers, engineers | `glossary`, `nomenclature-matrix`, `style-guide`, `article-template` |
| `design-system/` | Design system as a platform component — architectural framing and brand surface context. Component guides, token specs, and accessibility documentation live in `pointsav-design-system/` (see naming-convention.md §13 Decision #7). | Engineers, designers, financial community | `design-philosophy`, `design-primitive-vocabulary`, `brand-family-swatch`, `brand-typography` |

Rationale:

- Ten categories. The split of the original `architecture/` into
  `architecture/` + `substrate/` + `patterns/` (ratified 2026-05-09)
  was a balance fix — the pre-split `architecture/` carried 75 articles,
  ~3× the wiki mean. The new three-way split puts foundational mechanism
  concepts in `substrate/`, named recurring design patterns in `patterns/`,
  and cross-cutting platform/doctrine articles in `architecture/`.
- `company/` and `help/` were retired 2026-05-09 (operator decision —
  empty categories carry no editorial value; if their TOPICs come up
  they can be re-added). Originally they were investor-facing and
  contributor-onboarding categories; in practice no articles were
  authored.
- Each remaining category is materially distinct:
  - `architecture` (cross-cutting + doctrine + concrete systems composition)
    vs `substrate` (mechanism concepts) vs `patterns` (recurring shapes).
  - `architecture` (composition + doctrine) vs `systems` (per-OS)
    vs `services` (per-service) vs `applications` (per-app) — the
    platform's own taxonomy from the Nomenclature Matrix.
  - `governance` (formal technical decisions, ADRs) — financial-community
    facing material lives here in disclosure articles + ADRs.
  - `infrastructure` (physical / deployed runtime + storage + network +
    telemetry) vs `architecture` (abstract / logical). The rule is
    deployment artefacts and runtime concerns go in `infrastructure`;
    cross-cutting design intent and doctrine go in `architecture`.
  - `reference` (definitional and stylistic) — what something is, how
    style is determined.

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

## 10. Ratified operator decisions (2026-05-07)

Four decisions required for ratification. All ratified 2026-05-07.
Full decision text in §13.

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

Ratified 2026-05-07 by operator.

**1. Category set.** Accept with amendment. Nine-category proposal accepted.
`company/` and `governance/` both kept. `infrastructure/` kept distinct from
`architecture/`. `design-system/` added as tenth category (per project-editorial
commit 4d5a499, 2026-05-06 — 30 articles published). Final category set is the
ten categories listed in §4.

**2. Investor audience.** `company/` accepted as first-class category (§9 primary
proposal). Investor-facing content lives in `company/`. No split to a separate
domain at this scale.

**3. Front-matter schema changes.** Staged adoption. First pass: `id` (ULID),
`type`, `bcsc_class`, `status` (extended values). `tags`, `aliases`, and named
relations deferred to second pass when search-facet infrastructure is wired.
`subcategory:` field to be retired — existing values are treated as metadata-only
until removal completes in a future normalisation pass.

**4. ID format.** ULID (26 chars, time-ordered, typographically compact). Rationale:
time-ordered enables chronological sort without a separate field; 26-char
alphanumeric is copy-paste friendly; no hyphen breakage in URLs. UUIDv7 is a
valid alternative but not chosen — ULID is already in use in Foundry tooling.

---

Ratified 2026-05-09 by operator (category-balance audit).

**5. architecture/ split into architecture/ + substrate/ + patterns/.**
Pre-split `architecture/` carried 75 articles after schema and slug-collision
cleanup, ~3× the wiki mean — too big to navigate or browse usefully. Split
into three categories:

- `substrate/` (30 articles): foundational mechanism concepts — the
  X-substrate articles, plus the disciplines and primitives that compose
  them. Named to match the workspace's "substrate" vocabulary used in
  doctrine claims.
- `patterns/` (10 articles): named design patterns recurring across the
  platform at the editorial / interface / coordination layer (e.g.,
  source-of-truth-inversion, pairing-as-permission, reverse-funnel-editorial-pattern).
- `architecture/` retained (~35 articles): cross-cutting platform
  architecture, doctrine articles, concrete systems composition.

The names were chosen for distinctiveness and stability — `substrate` and
`patterns` are recognised industry vocabulary (Christopher Alexander → GoF
patterns; Apache / Red Hat substrate model) while still carrying the
workspace-specific meaning we use in doctrine. Earlier candidate names
considered and rejected: `concepts/` (too generic), `doctrine/` (ambiguous
with the Foundry Doctrine document), `frameworks/` (too engineering-specific).

**7. design-system/ category split (2026-05-16).** Ratified by OPUS editorial analysis and operator acceptance. Trigger: 48 of 57 articles in `design-system/` were design-system implementation specifications (token docs, component guides, accessibility specs) — not platform-documentation articles. The category had grown into a mirror of `pointsav-design-system/` rather than a commentary on the design system as a platform component. Decision: move 48 files (3 batches) to `pointsav-design-system/`. Retain 4 EN+ES pairs (design-philosophy, design-primitive-vocabulary, brand-family-swatch, brand-typography) which cover the design system as a platform concept. Permanent routing boundary: articles *about* the design system as a platform component → `content-wiki-documentation/design-system/`; component specs, token docs, implementation guides → `pointsav-design-system/`. Batches: Batch 1 (8 files) foundation token docs → `pointsav-design-system/docs/foundations/`; Batch 2 (22 files) component guides + wiki-surface → `pointsav-design-system/components/<name>/guide.md` + `docs/wiki-surface/`; Batch 3 (18 files) spatial/accessibility → `pointsav-design-system/components/<name>/guide.md` + `docs/accessibility/`. Redirects: `content-wiki-documentation/redirects.yaml` (48 entries).

**6. Empty categories company/ + help/ retired.** Both categories were
ratified at decision #1 above (2026-05-07) but no articles were authored
in either. They render as empty surfaces, which carries no editorial
value. Operator decision: retire from §4 taxonomy now; re-add if and
when their first TOPICs are authored. The retirement reduces taxonomy
from 11 categories (after the architecture split would have been 12) to
10 active.
