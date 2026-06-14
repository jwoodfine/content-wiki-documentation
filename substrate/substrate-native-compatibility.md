---
schema: foundry-doc-v1
title: "Substrate-native compatibility — why the Action API shim was dropped"
slug: substrate-native-compatibility
short_description: "Establishes structural compatibility with MediaWiki reader and integrator conventions while deliberately declining API mimicry, maintaining substrate-native interfaces that reduce maintenance burden and avoid disclosure obligations tied to compatibility guarantees."
status: active
category: substrate
type: topic
content_type: topic
quality: complete
last_edited: 2026-05-25
editor: pointsav-engineering
audience: vendor-public
bcsc_class: no-disclosure-implication
language_protocol: PROSE-TOPIC
paired_with: substrate-native-compatibility.es.md
cites:
 - ni-51-102
 - osc-sn-51-721
---

The PointSav wiki at `documentation.pointsav.com` provides structural compatibility with MediaWiki's reader-facing conventions — URL patterns, wikilink syntax, footnote syntax — while deliberately declining to replicate MediaWiki's internal API surface. Every interface the substrate does not replicate is a [[compliance-and-continuous-disclosure|compliance obligation]] it does not assume.

That decision has a concrete cost and a concrete benefit. The cost: contributors migrating automation workflows from MediaWiki-compatible tools re-implement against new interfaces. The benefit: every Action API endpoint MediaWiki ships, deprecates, or modifies would have generated a maintenance event; the platform has no control over that velocity, and every public interface the platform exposes is a continuous-disclosure surface under Canadian securities law (National Instrument 51-102 and OSC Staff Notice 51-721). Declining the shim means the wiki's disclosure commitments are bounded to what the substrate actually provides.

The result is a wiki with the reader and integrator ecosystem reach of a MediaWiki-replacement — resolving wikilinks, serving `sitemap.xml`, accepting Wikipedia-style markup — and a maintenance surface that scales with the [[app-mediakit-knowledge|platform's own velocity]], not MediaWiki's.

## The choice

The PointSav engineering wiki at `documentation.pointsav.com` is a substrate-native wiki. It accepts a one-shot MediaWiki XML import, serves URLs in MediaWiki's familiar `/wiki/{slug}` shape, accepts Wikipedia-style `[[wikilink]]` and `[^footnote]` syntax, and stops there. It does not implement MediaWiki's Action API, does not support MediaWiki templates, does not run a bot framework compatible with pywikibot, and does not provide a write surface that mimics MediaWiki's REST endpoints.

The core architectural distinction: when an existing platform's role is substituted by the substrate, the substrate replicates *structural compatibility* — the surfaces a reader or external integrator encounters — without replicating *interface mimicry* — the API shape an internal-system integration would consume. The distinction is load-bearing.

The MediaWiki Action API shim was scoped during the [[app-mediakit-knowledge|wiki engine's]] initial design phase at version 0.1.10 and dropped at version 0.1.14 after the maintenance burden and the [[disclosure-substrate|disclosure-posture]] risk the shim would have introduced were surfaced. This article covers the rationale.

## Ecosystem moat — what compatibility actually buys

The MediaWiki ecosystem is real. Approximately 1,500 extensions, hundreds of thousands of templates, a mature bot framework (pywikibot), Wikidata integration, the Wikimedia Commons asset library, and a deep archive of operational practice across Wikipedia, Wiktionary, Wikiquote, and a long tail of self-hosted installations. A wiki engine that promises MediaWiki compatibility inherits a portion of that moat by reference.

But the moat has two parts, and the parts have different costs to participate in.

The first part is **reader and external-integrator structural compatibility**: a reader who knows Wikipedia's URL pattern and markup can navigate and edit the wiki without retraining; an external system that ingests `sitemap.xml` or follows wikilinks discovers the corpus without bespoke adapters. This part is low-cost to provide — `/wiki/{slug}`, `[[wikilink]]`, and `[^1]` are conventions the substrate adopts because they are useful, not mimicry.

The second part is **internal-system interface mimicry**: extensions that read and write through the Action API, bots that authenticate against MediaWiki's login flow, templates that expand server-side using the MediaWiki parser. This part is high-cost to provide — every API endpoint mimicked is an interface that must be maintained against MediaWiki's evolution, hardened against MediaWiki's known attack surfaces, and audited under whatever compliance posture the substrate has committed to.

The substrate's choice is to participate in the first part fully and decline the second part deliberately. The cost calculus favours [[citation-substrate|decline]]:

- Reader and integrator ecosystem effects scale via conventions, which are stable across a decade. The substrate adopts the convention once and benefits indefinitely.
- Internal-system extension ecosystem effects scale via interfaces, which evolve with MediaWiki releases. The substrate would inherit a maintenance burden that grows with MediaWiki's ecosystem velocity, not the substrate's.
- Every interface the substrate exposes to the public is a continuous-disclosure surface under applicable securities regulation. An Action API shim would commit the substrate to disclosure-grounding every Action API endpoint's behaviour, which is a moving target.

## What was kept

Four substrate-compatibility surfaces are preserved, all in the low-cost-to-provide category:

**The xml-dump import path.** A future `import-mediawiki-xml` tool (planned) consumes Special:Export-style XML dumps and emits the wiki's Markdown plus frontmatter shape. The migration is one-shot per corpus; no live MediaWiki API runs alongside the substrate afterward. Importing 30 articles, 3,000 articles, or 30,000 articles is the same operational shape — read the dump, write Markdown files, commit. The pattern composes with version control naturally.

**URL conventions.** `/wiki/{slug}` matches MediaWiki's URL layout. External sites that link to articles via this URL pattern continue to resolve without 404s. The route is one line in the wiki engine's axum router and costs nothing to maintain. Adopting the convention is a low-cost ecosystem-reach choice.

**Wikilink syntax.** `[[slug]]` and `[[slug|display text]]` match Wikipedia's markup. Contributors who know Wikipedia recognise the form. The wiki's renderer parses wikilinks at render time, resolves them against the in-memory link graph (the redb-backed graph lights up in Phase 4), and emits HTML with red-link styling for unresolved targets.

**Footnote syntax.** `[^1]` matches CommonMark's footnote extension. The bibliography resolves footnotes against the article's frontmatter `references:` list. The implementation ships with `comrak` and adds no maintenance burden specific to the substrate.

These four surfaces give the substrate's wiki the reader and integrator ecosystem reach a MediaWiki-replacement deployment expects. None of them require running a MediaWiki parser, a MediaWiki API, or a MediaWiki extension framework.

## What was dropped

Three surfaces in the high-cost-to-provide category were declined:

**The MediaWiki Action API shim.** The shim was scoped at workspace v0.1.10 as an interface that would have replicated `?action=parse`, `?action=edit`, `?action=query`, `?action=login`, and the remaining Action API surface against the substrate's wiki engine. At v0.1.14 the shim was removed from scope. The reasoning:

- *Maintenance scales with MediaWiki's velocity.* Every Action API endpoint MediaWiki ships, deprecates, or modifies generates a shim-side maintenance event. The substrate cannot govern that velocity.
- *Compliance audit scales with the API surface.* Every interface the substrate exposes to the public must be disclosure-grounded under applicable continuous-disclosure requirements. The Action API shim would have multiplied the audit surface by an order of magnitude with no commensurate ecosystem benefit on the substrate's actual customer base.
- *Substrate-native interfaces cover the use cases.* The wiki's route surface (`/wiki/{slug}`, JSON-LD, Atom, JSON Feed, sitemap, `llms.txt`, raw Markdown via `/git/{slug}`, `/search?q=`, `POST /edit/{slug}`) covers what the Action API shim would have served, without committing the substrate to Wikipedia's API contract.

**MediaWiki templates and parser functions.** The wiki's renderer is `comrak` (CommonMark) plus PointSav-specific extensions for wikilinks, footnotes, table of contents, and section anchors. It is not a MediaWiki parser. Templates do not expand server-side. The workaround for content that would be a template in MediaWiki is Markdown partials, inlined by the contributor at edit time; the substrate accepts the duplication cost in exchange for a deterministic rendering pipeline that can be audited without parsing a Turing-complete template language at render time.

**The pywikibot ecosystem.** The substrate's automation path is the platform's existing tooling — the commit workflow, the corpus capture, the session protocol, the editorial pipeline's draft intake. None of these implement the pywikibot interface. A contributor migrating from pywikibot to the substrate's tooling re-implements against the new interfaces; the substrate accepts the migration cost in exchange for keeping its automation path coherent with the rest of the workspace's session model.

## The substrate-native API surface set

What the Action API shim would have served, the substrate's native interfaces serve coherently:

| Action API need | Substrate-native interface |
|---|---|
| `?action=parse` (render Markdown to HTML) | `GET /wiki/{slug}` (rendered HTML directly) |
| `?action=raw` (raw wikitext) | `GET /git/{slug}` (raw Markdown) |
| `?action=edit` (write articles) | `POST /edit/{slug}` (atomic write with frontmatter validation) |
| `?action=query&list=allpages` (enumerate articles) | `GET /sitemap.xml` (sitemaps.org compliant) |
| `?action=query&prop=links` (link graph) | `GET /backlinks/{slug}` (Phase 4) |
| `?action=query&prop=revisions` (history) | `GET /history/{slug}` (Phase 4) |
| `?action=opensearch` / `?action=query&list=search` | `GET /search?q=` (Tantivy / BM25) |
| `?format=json` (machine-readable per article) | JSON-LD `<script type="application/ld+json">` in every article's `<head>` |
| RSS / Atom feeds | `GET /feed.atom` + `GET /feed.json` |
| `?action=expandtemplates` | not provided; the substrate's renderer does not expand templates |
| `?action=login` / authentication | not provided over HTTP; authenticated edits use the Mutual Bidirectional Auth (MBA) path |

The interfaces compose with the substrate's other invariants. The JSON-LD is generated from the article's frontmatter by the same code path that emits the article HTML, so the structured data cannot drift from the rendered content. The Atom feed shares its data source with the JSON Feed, the sitemap, and the index page; a content tree change updates all four atomically. The [[worm-ledger-design|search backend]] (Tantivy) reads the same content tree as the HTML renderer; no separate write path needs to keep the search index synchronised with the article store, because the article store is the file system.

## The `verify://` URL scheme (planned)

A future substrate-specific URL scheme — `verify://{citation-id}` — is *intended* to resolve a citation reference to its verifiable source through the substrate's verification path, not through public DNS. The scheme is *planned* for Phase 7 of the wiki engine; it is not implemented as of v0.1.29.

The motivation: a `[citation-id]` in an article is a structured reference that the substrate can resolve to an authoritative source through the citation registry. The registry maps the ID to a (title, URL, optional clause reference) tuple, and a future Information Verifiability Citation (IVC) machinery is *intended* to harden the resolution to a cryptographically-verifiable proof of provenance. This is forward-looking. Cautionary language applies per [ni-51-102] and [osc-sn-51-721]. The reasonable basis is the citation-registry substrate already operating at v0.1.29. The material assumption is that the IVC machinery is ratified before Phase 7 implementation begins.

## Disclosure posture as compatibility lens

The deeper reason the substrate-native posture wins is that the wiki engine's compatibility-surface choices are continuous-disclosure choices in disguise. Every interface the substrate exposes to the public commits the substrate to a disclosure obligation under applicable continuous-disclosure requirements. What the substrate does not expose, it does not need to disclose about.

A few concrete cases:

An Action API shim returning `?action=query&prop=revisions` would have committed the substrate to a continuous-disclosure representation of every article's revision history. The substrate already commits to this through its git history (every edit is a signed commit, every commit is a published claim). But a parallel Action API representation would have introduced a second canonical record that needs to stay in sync with the git history; any drift is a disclosure failure. The substrate declines the shim and keeps git canonical.

An Action API shim returning `?action=parse` server-side would have committed the substrate to a server-side rendering contract independent of the Markdown source. If the rendered HTML drifts from the Markdown source, the substrate has a disclosure conflict. The substrate declines the shim and keeps the rendered HTML a deterministic function of the Markdown source plus the renderer version.

An Action API shim supporting `?action=edit` would have committed the substrate to an authenticated write path with weaker provenance than the substrate's edit surface. The `POST /edit/{slug}` route requires MBA-verified authorship per SYS-ADR-19; a MediaWiki-style API edit would have permitted token-bearer auth over a session that does not bind the editor's identity to a human-verified key chain. The substrate declines the shim and keeps the provenance guarantee.

The pattern: every interface the substrate does not replicate is an obligation it does not assume.

## The pattern generalises

Substrate substitution applies beyond MediaWiki. Several additional substitution cases follow the same pattern:

- **Disclosure-distribution platforms.** The substrate's continuous-disclosure record (signed git history on `documentation.pointsav.com`) is itself the disclosure channel; no third-party disclosure-distribution platform integration is required.
- **CRM platforms.** The substrate's people record is canonical. No CRM-style API mimicry is in scope.
- **Corporate-records platforms.** The substrate's corporate-records ledger is canonical. No enterprise-platform API mimicry.
- **Vendor SaaS for document storage.** The substrate stores documents in version-controlled Markdown trees; no SaaS integration is needed for storage.

The common thread: the substrate replicates structural compatibility where it pays and declines interface mimicry where the maintenance and disclosure costs would exceed the ecosystem benefit. Each substitution is analysed under the same lens: what does the existing platform's interface obligate the substrate to, and what does the substrate gain in return.

## See also

- [[source-of-truth-inversion]] — the storage-layer designation this pattern depends on (git as canonical record)
- [[app-mediakit-knowledge]] — the wiki engine this pattern governs
- [[disclosure-substrate]] — the continuous-disclosure posture and broader substitution cases
