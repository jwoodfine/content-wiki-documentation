---
schema: foundry-doc-v1
title: "Federation via content mounts"
slug: federation-via-content-mounts
short_description: "The pattern for combining curated editorial content with declarative mounts from domain-specific repositories into a single wiki surface — intended for Phase 6 of the knowledge engine."
category: patterns
type: topic
status: pre-build
bcsc_class: public-disclosure-safe
last_edited: 2026-06-01
editor: pointsav-engineering
paired_with: federation-via-content-mounts.es.md
---

# Federation via content mounts

The content-federation pattern combines two complementary authoring modes in a single wiki instance: curated editorial articles committed directly to the knowledge repository, and declarative mounts that pull content from domain-specific repositories. The two modes share a URL surface, navigation chrome, and search index while keeping their source repositories independent. This pattern is planned for Phase 6 of [[app-mediakit-knowledge]]; the single-repository model is the current deployed form.

---

## The hybrid model

A deployed wiki instance is configured by a `knowledge.toml` manifest at the content directory root. The manifest declares zero or more mounts alongside any articles committed directly to the repository. Both sources render into the same URL namespace; readers encounter no visible distinction between a curated article and a mounted article.

Direct commits are the correct choice for content that is editorial in nature — platform reference articles, design-system notes, governance documents — where the knowledge repository is the canonical home and editing flows through the standard staging-tier commit path. Declarative mounts are the correct choice for content that originates in a domain-specific repository — per-project documentation, per-deployment operational records, architectural decision records — where the source repository is the canonical home and the wiki is a read surface over it.

---

## How mounts work

A mount entry in `knowledge.toml` is intended to specify four elements:

- *Source repository.* A git remote URL or a local path that the engine can pull.
- *Mount path.* The local directory path under which the fetched content is placed.
- *Blueprint.* The named schema that validates and routes files in the mount.
- *Edit URL template.* A URL pattern the engine uses to construct the "edit this page" link for mounted articles, routing editors back to the source repository rather than accepting writes locally.

The engine is intended to fetch the source repository on startup and on a configured refresh interval, write fetched content to the mount path, and process it identically to directly committed articles.

---

## Blueprints

A blueprint is a named schema that constrains what content a mount may contain. Two blueprints are intended to be built in:

*`topic`.* The standard wiki article format. Files must conform to the content contract's frontmatter schema and body conventions. Rendered at `/:category/:slug` and included in the primary article index and search.

*`guide`.* Operational documents addressed to practitioners. Rendered with a distinct chrome that emphasises procedural steps over prose sections. Excluded from the primary article index but discoverable via search and the [[guide-catalog|guide catalog]].

Operators are intended to register additional blueprints as plugins when Phase 6 ships. Candidate domain-specific blueprints include `regional-market` (structured location articles), `adr` (architectural decision records with a fixed decision/status/context schema), and `changelog` (time-ordered release notes). Each plugin blueprint would define its frontmatter schema, the URL pattern it occupies, and the chrome template it uses.

---

## Per-instance isolation

Each wiki instance is intended to read only the mounts declared in its own `knowledge.toml`. Two instances sourcing the same repository may present entirely different article sets depending on their mount configurations. There is no global mount registry — isolation is a configuration property of the instance, not a coordination problem.

This isolation property is what allows a single canonical content repository to serve multiple distinct wiki deployments. The content repository is the source of truth; each deployment is a view over it shaped by its mount manifest.

---

## Provenance and edit-routing

Every article rendered from a declarative mount is intended to carry provenance fields in its frontmatter:

- `source_repo` — the remote URL of the source repository.
- `source_path` — the file path within the source repository.
- `edit_url` — the URL the engine renders as the "edit this page" link.

The `edit_url` is intended to route editors to the canonical editing path in the source repository rather than accepting writes locally. This keeps the source-of-truth inversion intact across a federated content surface: a mounted article's canonical home is the source repository; the wiki instance is a read surface over it, not a second canonical store.

---

## Relationship to source-of-truth inversion

This pattern is intended to extend [[source-of-truth-inversion]] from a single-repository topology to a multi-repository topology. The invariant is the same: git is canonical; the running binary is a view. The extension is that "git" may be one of several named repositories, each the canonical home for its domain, and the wiki instance a view over all of them simultaneously.

The federation model is not intended to introduce a central coordination layer. Each source repository is autonomous; the mount manifest is a per-instance declaration; and the engine's fetch-and-render pipeline is stateless with respect to source repositories.

---

## See also

- [[app-mediakit-knowledge]] — the engine that implements this pattern
- [[source-of-truth-inversion]] — the foundational design choice this pattern extends
- [[knowledge-wiki-leapfrog-architecture]] — the broader IA and navigation philosophy
