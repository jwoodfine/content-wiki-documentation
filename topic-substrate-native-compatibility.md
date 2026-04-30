---
schema: foundry-doc-v1
title: "Substrate-Native Compatibility"
slug: topic-substrate-native-compatibility
category: architecture
type: topic
quality: complete
short_description: "Substrate-native compatibility describes the deliberate design choice to replicate structural surfaces that readers and external integrators rely on, while declining to mimic internal API interfaces whose maintenance cost exceeds their ecosystem benefit."
status: pre-build
last_edited: 2026-04-30
editor: pointsav-engineering
cites:
  - ni-51-102
  - osc-sn-51-721
  - mediawiki-action-api
  - mediawiki-xml-dump
  - c2sp-tlog-tiles
paired_with: topic-substrate-native-compatibility.es.md
---

# Substrate-Native Compatibility

> Substrate-native compatibility describes the deliberate design choice to replicate structural surfaces that readers and external integrators rely on, while declining to mimic internal API interfaces whose maintenance cost exceeds their ecosystem benefit.

The PointSav engineering wiki at `documentation.pointsav.com` operates on a **substrate-native** design. It accepts a one-shot MediaWiki XML import, serves URLs in MediaWiki's familiar `/wiki/{slug}` shape, and accepts Wikipedia-style `[[wikilink]]` and `[^footnote]` syntax. It does not implement the MediaWiki Action API, does not support MediaWiki templates, and does not provide a write surface that mimics MediaWiki's REST endpoints. This is the substrate-native posture per Doctrine claim #29 (Substrate Substitution).

The MediaWiki Action API shim was scoped during the wiki engine's initial design pass and dropped at workspace v0.1.14 after the maintenance burden and disclosure-posture risk the shim would introduce became clear. This article covers the rationale.

## The two parts of ecosystem compatibility

The MediaWiki ecosystem carries roughly 1,500 extensions, hundreds of thousands of templates, a bot framework (pywikibot), and deep operational practice across Wikipedia and a long tail of self-hosted installations. Compatibility with this ecosystem comes in two distinct parts.

The first part is **reader and external-integrator structural compatibility**: a reader who knows Wikipedia's URL pattern and markup can navigate and edit the wiki without retraining; an external system that ingests a sitemap or follows wikilinks discovers the corpus without bespoke adapters. This part is low-cost to provide — `/wiki/{slug}`, `[[wikilink]]`, and `[^1]` are conventions the substrate adopts because they are useful, not mimicry.

The second part is **internal-system interface mimicry**: extensions that read and write through the Action API, bots that authenticate against MediaWiki's login flow, templates that expand server-side using the MediaWiki parser. This part is high-cost to provide — every API endpoint mimicked is an interface that must be maintained against MediaWiki's evolution, hardened against its known attack surfaces, and audited under the substrate's disclosure posture.

The substrate participates fully in the first part and declines the second deliberately.

## What was kept

Four compatibility surfaces are preserved, all in the low-cost category:

**The xml-dump import path.** A future `import-mediawiki-xml` tool (planned) consumes Special:Export-style XML dumps `[mediawiki-xml-dump]` and emits the wiki's markdown plus frontmatter shape. The migration is one-shot per corpus.

**URL conventions.** `/wiki/{slug}` matches MediaWiki's URL layout. External sites that link to articles via this pattern continue to resolve without 404s.

**Wikilink syntax.** `[[slug]]` and `[[slug|display text]]` match Wikipedia's markup. The wiki's renderer parses wikilinks at render time and emits HTML with red-link styling for unresolved targets.

**Footnote syntax.** `[^1]` matches CommonMark's footnote extension. The bibliography resolves footnotes against the article's frontmatter `references:` list.

## What was dropped

Three surfaces in the high-cost category were declined:

**The MediaWiki Action API shim.** Scoped at workspace v0.1.10, dropped at v0.1.14. Every Action API endpoint MediaWiki ships, deprecates, or modifies generates a maintenance event the substrate has no control over. The disclosure posture `[ni-51-102]` requires every interface the substrate exposes to the public to be disclosure-grounded; an Action API shim would have multiplied the audit surface by an order of magnitude with no commensurate benefit.

**MediaWiki templates and parser functions.** The wiki's renderer is `comrak` (CommonMark) with PointSav-specific extensions. It is not a MediaWiki parser. The workaround for template-like content is markdown partials, inlined by the contributor at edit time.

**The pywikibot ecosystem.** The substrate's automation path is the workspace's existing tooling — `bin/commit-as-next.sh`, the trajectory-substrate corpus capture, the mailbox protocol, and the drafts-outbound input ports. None implement the pywikibot interface.

## Substrate-native API surface

The substrate's own routes cover the same use cases the Action API shim would have served:

| Action API need | Substrate-native interface |
|---|---|
| `?action=parse` (render markdown to HTML) | `GET /wiki/{slug}` (rendered HTML directly) |
| `?action=raw` (raw wikitext) | `GET /git/{slug}` (raw markdown) |
| `?action=edit` (write articles) | `POST /edit/{slug}` (atomic write with frontmatter validation) |
| `?action=query&list=allpages` (enumerate articles) | `GET /sitemap.xml` (sitemaps.org compliant) |
| `?action=query&prop=links` (link graph) | `GET /backlinks/{slug}` (Phase 4, planned) |
| `?action=opensearch` | `GET /search?q=` (Tantivy / BM25) |
| `?format=json` (machine-readable per article) | JSON-LD block in every article's `<head>` |
| RSS / Atom feeds | `GET /feed.atom` + `GET /feed.json` |

## Disclosure posture as the deciding lens

The deeper reason the substrate-native posture holds is that compatibility-surface choices are continuous-disclosure choices in disguise. Every interface the substrate exposes commits the substrate to a disclosure obligation under `conventions/bcsc-disclosure-posture.md` and the `[ni-51-102]` compliance posture. What the substrate does not expose, it does not need to disclose about.

A few concrete cases: an Action API shim returning `?action=query&prop=revisions` would have introduced a second canonical record of article revision history alongside the git log, and any drift between the two is a disclosure failure. A shim returning `?action=parse` would have committed the substrate to a server-side rendering contract independent of the markdown source. A shim supporting `?action=edit` would have permitted token-bearer auth weaker than the substrate's MBA-verified authorship chain.

The pattern generalises. Substrate substitution applies beyond MediaWiki to Q4 Inc-style disclosure platforms, CRM platforms, ERP-class corporate-records platforms, and vendor SaaS for document storage. In each case, the substrate replicates structural compatibility where it pays and declines interface mimicry where the cost exceeds the benefit.

## See Also

- [[topic-app-mediakit-knowledge]]
- [[topic-reverse-funnel-editorial-pattern]]
- [[topic-documentation-pointsav-com-launch-2026-04-27]]
- [[topic-customer-hostability]]

## References
