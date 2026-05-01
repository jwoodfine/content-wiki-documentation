---
schema: foundry-topic-v1
status: published
last_edited: 2026-04-30
category: applications
audience: vendor-public
bcsc_class: no-disclosure-implication
language_protocol: PROSE-TOPIC
cites:
  - ni-51-102
  - osc-sn-51-721
  - c2sp-tlog-tiles
  - constitutional-ai-2212-08073
references:
  - vendor/pointsav-monorepo/app-mediakit-knowledge/ARCHITECTURE.md
  - vendor/pointsav-monorepo/app-mediakit-knowledge/UX-DESIGN.md
  - vendor/pointsav-monorepo/app-mediakit-knowledge/INVENTIONS.md
  - https://commonmark.org/
  - https://github.com/kivikakk/comrak
  - https://www.tantivy-search.org/
  - https://schema.org/TechArticle
  - https://datatracker.ietf.org/doc/html/rfc4287
  - https://www.jsonfeed.org/version/1.1/
  - https://llmstxt.org/
  - https://en.wikipedia.org/wiki/Wikipedia:Manual_of_Style/Layout
  - DOCTRINE.md claim #29 (Substrate Substitution)
  - DOCTRINE.md claim #31 (Constitutional Constrained Author)
  - DOCTRINE.md claim #16 (Optional Intelligence Layer)
  - conventions/disclosure-substrate.md
  - conventions/three-ring-architecture.md
---

`app-mediakit-knowledge` is the wiki engine that serves PointSav's engineering documentation at `https://documentation.pointsav.com`. The engine is a single-binary Rust service composed of an `axum` HTTP server, a `comrak` CommonMark renderer with PointSav-specific extensions for wikilinks, footnotes, table of contents, and section anchors, a `tantivy` full-text search backend, and a `maud` templating layer that ships four article templates and static-asset bundles. The engine reads markdown files from a content directory the operator names at startup, renders them on demand into HTML, and returns them with caching headers tuned for a documentation audience.

The engine is a *view* over a markdown tree, not a content repository. The markdown tree is canonical; the running binary is a view that any number of operators can stand up over the same content tree, or different content trees, with no shared mutable state on the binary side. This source-of-truth inversion is the single most important design choice and is treated in detail in §2.

The engine's first public deployment went live on 2026-04-27 at 16:25 UTC, serving a four-file placeholder content tree at `https://documentation.pointsav.com`. The full route surface from build phases 1, 1.1, 2, and 3 is operational; phases 4 through 8 are planned but not yet implemented.

## Source-of-truth inversion

The substrate's load-bearing design choice: **git is canonical; the running binary is a view; CRDT, when collaborative editing is enabled, is session-ephemeral**.

Every concrete artefact a reader encounters — the HTML page, the Atom feed entry, the JSON-LD block, the search-result hit, the wikilink graph — is derived at request time from the markdown tree on disk. The disk state is what gets committed, reviewed, replicated, and disclosed. The HTML is throwaway. The Tantivy index is throwaway, rebuilt from the markdown tree on startup. The redb wikilink graph (Phase 4) is throwaway. The collab CRDT (Phase 2 Step 7, default-off) is throwaway between sessions.

This inversion reverses the traditional MediaWiki model, where the database is canonical and the file system is a derived working copy. Here, the file system is canonical and the database (search index, link graph) is a derived working copy. The motivation is operational simplicity — a content-tree backup is a `git clone`; a content-tree replication is a `git pull`; a content-tree audit is a `git log` — and a substrate-level invariant: every published claim is a signed git commit; the disclosure record is the git history; the BCSC continuous-disclosure posture is enforced by structure rather than by policy alone.

Other patterns follow from the inversion. The wiki has no preview-then-publish workflow because the canonical state is what got committed; an edit committed is a publication. The wiki has no scheduled-publish workflow because the same property holds. The wiki has no server-side draft state because drafts live in the contributor's git working copy or in the cluster's drafts-outbound port, not in a database the wiki engine owns.

## Route surface

The engine exposes a tight set of HTTP routes. Each is independent; no route depends on session state or on a database the engine owns.

| Route | Purpose | Phase |
|---|---|---|
| `/healthz` | Liveness check (returns the literal string `ok`) | 1 |
| `/` | Index page (lists all articles in the served content tree) | 1 |
| `/wiki/{slug}` | Rendered article HTML | 1 |
| `/static/{*path}` | Static assets (CSS, JS, fonts) | 1 |
| `/edit/{slug}` | In-browser editor (CodeMirror 6) | 2 |
| `POST /edit/{slug}` | Atomic-write edit endpoint with squiggle linting | 2 |
| `/search?q=` | Full-text search results (Tantivy / BM25) | 3 |
| `/feed.atom` | RFC 4287 Atom syndication feed | 3 |
| `/feed.json` | JSON Feed 1.1 syndication | 3 |
| `/sitemap.xml` | sitemaps.org compliant sitemap | 3 |
| `/robots.txt` | Crawler discovery | 3 |
| `/llms.txt` | llmstxt.org convention for LLM crawlers | 3 |
| `/git/{slug}` | Raw markdown source for git-clone-style ingestion | 3 |
| `/ws/collab/{slug}` | WebSocket passthrough relay (default-off behind `--enable-collab`) | 2.7 |

Phase 4 is planned to add `/history/{slug}`, `/blame/{slug}`, `/diff/{a}/{b}`, `/backlinks/{slug}`, an MCP server route, and a read-only Git remote over smart-HTTP. Phases 5 through 8 are planned; cautionary language applies per [ni-51-102] and [osc-sn-51-721].

The engine emits JSON-LD `TechArticle` and `DefinedTerm` schema in every rendered article's `<head>` block for search-engine and LLM-crawler comprehension. The structured data is generated from the article's frontmatter, not hand-authored per page; the schema is the same shape across the corpus.

## Wikipedia muscle-memory chrome

The engine ships with a deliberately Wikipedia-recognisable chrome. A reader of any Wikipedia article will navigate the engine without prompting, and a reader unfamiliar with Wikipedia will pick up the patterns quickly because they are well-documented conventions.

What was kept (per `UX-DESIGN.md` §1):

- Article / Talk tabs at the top of the page
- Read / Edit / View history tabs alongside the Article/Talk pair
- Per-section `[edit]` pencils on every `## H2` and `### H3` heading
- End-of-article ordering: References, See also, Categories, with a footer band naming the article's licence and the substrate
- Hatnote band at the top of the article for disambiguation and cross-references
- Lead first-sentence convention (bolded subject plus copula plus definition)
- Tagline directly under the article title
- Collapsible left-rail table of contents
- Language switcher (currently English / Spanish)

What was added beyond Wikipedia:

- Citation badges next to inline `[citation-id]` references, with hover-card showing the registry entry
- Forward-Looking-Information cautionary banner when an article's frontmatter sets `forward_looking: true`
- BCSC `disclosure_class` field rendered in JSON-LD (not visible in default chrome)
- Information Verifiability Citation (IVC) masthead band placeholder (Phase 7 will provide the verification machinery)
- Reader density toggle (compact / comfortable; settings persist client-side)

The chrome is implemented in four `maud` HTML templates and a CSS bundle that tracks Vector 2022's spacing and typography rather than its colour palette. The aim is muscle memory, not literal mimicry — a reader who knows Wikipedia recognises the layout, but the visual identity is distinct.

## Editor surface

The wiki's editor is a CodeMirror 6 instance vendored into the binary's static-asset bundle, served at `/edit/{slug}`. It supports markdown highlighting with line numbers, configurable line wrap, and undo/redo history, with atomic disk write via `POST /edit/{slug}`.

Three substrate-aware features distinguish the implementation:

**Squiggle linting.** Seven deterministic rules flag editorial issues at typing time, each with a cited authority in a hover-card. The rules cover banned vocabulary, forward-looking framings without the cautionary-banner pattern, BCSC-discipline checks, and Bloomberg-article-standard register checks.

**Citation autocomplete.** Pressing `[` triggers a typeahead populated from the workspace citation registry at `~/Foundry/citations.yaml`. Selecting an entry inserts the canonical `[citation-id]` form and adds the citation to the article's frontmatter `cites:` list.

**Three-keystroke ladder for Doorman stubs.** Tab opens a ladder of "ask Doorman" affordances — find a citation, suggest a hatnote target, generate a disambiguation link, propose a section heading. These return 501 stubs in the v0.1.29 binary; Phase 4 is planned to wire them to the service-slm Doorman.

The editor's atomic-write semantics are conservative: the engine writes new file content to a temporary path in the same directory, fsyncs, and renames over the destination.

## Search, feeds, and ingestion

The engine indexes the content tree on startup and incrementally on edit. The index is on-disk Tantivy (BM25 by default) at `<state-dir>/search/`, rebuilt from the content tree if it is missing.

Three syndication formats render the corpus to crawlers: **`/feed.atom`** (RFC 4287 Atom), **`/feed.json`** (JSON Feed 1.1), and **`/sitemap.xml`** (sitemaps.org compliant). Two crawler-discovery files round out the surface: **`/robots.txt`** and **`/llms.txt`**.

The `/git/{slug}` route serves raw markdown source. An LLM crawler or a future federation peer can ingest the content tree by following `/llms.txt` to discover the article list, then fetching `/git/{slug}` for each article's source. The route accepts an optional `.md` suffix for tools that expect markdown URLs to end in `.md`.

## Real-time collaboration

The engine optionally supports real-time collaborative editing via the Yjs CRDT. The feature is default-off behind the `--enable-collab` CLI flag; the production deployment at v0.1.29 does not enable it.

The implementation follows the source-of-truth inversion: **the server is a passthrough WebSocket relay, not a Yjs server**. Yjs document state never lives on the server. The relay is a thin `tokio::sync::broadcast` per-slug room with a 256-message lag buffer; clients send Yjs update packets, the server forwards them to other clients in the room, and persistence flows through the existing `POST /edit/{slug}` save path on deliberate save. When all clients leave the room, the room closes and any unsaved CRDT state is discarded.

The client lazy-loads `cm-collab.bundle.js` (302 KB) only when the template's `window.WIKI_COLLAB_ENABLED` flag is set by the server, so production deployments without `--enable-collab` never load any Yjs JavaScript.

## Substrate-native compatibility surface

The engine is a substrate-native wiki, not a MediaWiki shim. This reflects Doctrine claim #29 (Substrate Substitution) ratified at workspace v0.1.10 and refined at v0.1.14.

What was kept: the **`xml-dump` import path** for one-time corpus migration; **URL conventions** (`/wiki/{slug}`); **wikilink syntax** (`[[slug]]` and `[[slug|display text]]`); **footnote syntax** (`[^1]`).

What was dropped: the **MediaWiki Action API shim** (maintenance scales with MediaWiki's velocity; compliance audit scales with the API surface); **MediaWiki templates and parser functions** (the renderer is CommonMark, not a MediaWiki parser); the **pywikibot ecosystem** (the substrate's automation path is the workspace tooling).

The trade-off is a narrower compatibility surface against a substrate-coherent posture. A reader migrating from a MediaWiki deployment loses templates and the Action API; gains source-of-truth inversion, deterministic rendering, BCSC-grounded disclosure posture, and a smaller attack surface.

A separate sibling TOPIC ([[topic-substrate-native-compatibility]]) covers the rationale in full.

## Inventions catalogue

`INVENTIONS.md` at the crate root catalogues eight engine-specific inventions (count as of v0.1.29):

1. **Source-of-truth inversion** — git canonical, binary view, CRDT ephemeral
2. **Substrate-native compatibility** — Doctrine claim #29
3. **Constitutional Constrained Author (CCA)** — Doctrine claim #31; squiggle linter at edit time
4. **Information Verifiability Citation (IVC)** — Phase 7 planned; masthead band placeholder
5. **Substrate-Authored Affordances (SAA)** — the squiggle linter's seven deterministic rules
6. **`verify://` URL scheme** — Phase 7 planned; resolves a citation ID to its verifiable source
7. **The passthrough WebSocket relay** — collab implementation that does not introduce a parallel authoritative record
8. **The substrate-native API surface set** — the route table above; what the Action API shim would have replicated, done coherently with the substrate's other invariants

The catalogue is open. New inventions land in `INVENTIONS.md` with a brief, the substrate justification, the implementation phase, and the references that anchor it.

## Build phases trajectory

As of 2026-04-27 the engine is at the end of Phase 3:

- **Phase 1** — axum server, comrak rendering, four templates, static assets, core routes (shipped, 8 tests)
- **Phase 1.1** — Wikipedia muscle-memory chrome (shipped, 19 tests)
- **Phase 2** — JSON-LD baseline, atomic edit endpoint, CodeMirror editor, squiggle linter, citation autocomplete, Doorman ladder stubs, collab passthrough relay (shipped, 97 tests)
- **Phase 3** — Tantivy search backend, syndication feeds, sitemap, crawler discovery (shipped)
- **Phase 4** — git2 commit-on-edit, history and blame, redb wikilink graph, backlinks, blake3 federation seam, MCP server, smart-HTTP read-only Git remote, OpenAPI 3.1 specification (planned; awaiting operator clearance of seven open questions before implementation begins)
- **Phases 5–8** — image and asset handling; per-tenant shaping; federation and content-addressed retrieval; disclosure-class linter that hardens BCSC invariants into compile-time-equivalent checks (planned)

Phases 4–8 are *planned*; cautionary language applies per [ni-51-102] and [osc-sn-51-721]. Material changes to the build plan are recorded in the phase plan documents and the workspace `CHANGELOG.md`.

## See also

- [[topic-source-of-truth-inversion]] — the canonical / view / ephemeral pattern generalised across the substrate
- [[topic-substrate-native-compatibility]] — the Action API drop rationale and the substrate-native surface set
- [[topic-collab-via-passthrough-relay]] — the WebSocket relay implementation in depth
- [[topic-wikipedia-leapfrog-design]] — chrome design intent and the 95%/5% muscle-memory contract
- [[topic-documentation-pointsav-com-launch-2026-04-27]] — the v0.1.29 public launch narrative

## Provenance

Authored 2026-04-27 by the project-knowledge cluster based on `app-mediakit-knowledge/ARCHITECTURE.md`, `UX-DESIGN.md`, and `INVENTIONS.md`. Refined by project-language 2026-04-30. Doctrine-claim references and invention-catalogue counts are current as of v0.1.29; the catalogue grows as phases ratify.

Forward-looking statements about Phases 4–8 follow [ni-51-102] and [osc-sn-51-721] continuous-disclosure posture. Material assumptions: the workspace VM remains available; operator clearance of the Phase 4 design review; editorial labour at the project-language gateway is sustained.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
