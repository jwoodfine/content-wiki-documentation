---
schema: foundry-doc-v1
title: "Contributing to PointSav Knowledge"
slug: contribute
category: governance
type: governance
quality: complete
short_description: "How to propose additions, corrections, and new articles for PointSav Knowledge."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-27
editor: pointsav-engineering
---

PointSav Knowledge is an open-content engineering wiki. Contributions from engineers, architects, technical writers, and subject-matter experts are welcome.

## Content standards

All articles in this wiki are written to institutional standard: precise, verifiable, and free of marketing vocabulary. The writing target is a technically literate reader who is not already familiar with PointSav internals — an engineer evaluating the platform, a compliance reviewer, or a financial analyst.

Key principles:

- Claims are specific and independently falsifiable.
- Forward-looking statements are marked as planned, intended, or targeted.
- Third-party tools and standards are named accurately, not compared by implication.
- Articles describe what the platform does, not how distinctive it is.

## What to contribute

**New articles** should cover one of the ten categories documented in this wiki — architecture, substrate, patterns, systems, services, applications, governance, infrastructure, reference, or design-system. Check the [[all-pages|all-pages index]] and the [[wanted|wanted articles]] page before proposing a topic that may already exist.

**Corrections** to existing articles are the highest-value contributions. If a technical claim is inaccurate, out of date, or underspecified, submit a correction with the corrected text and the basis for the change.

**Translations** (Spanish) of existing English articles are tracked under the [[all-pages|all-pages index]]. Each English article should have a paired `.es.md` sibling.

## Slug discipline

Article filenames are slugs — they are permanent once published. Two rules govern naming:

- **No legacy prefixes.** Do not name new articles `topic-foo.md`, `guide-foo.md`, or `research-foo.md`. Free-standing concept articles use plain kebab slugs (`foo-bar.md`). Nomenclature Matrix entity-type prefixes (`os-*`, `service-*`, `app-*`, `sys-adr-*`) remain required for their entity types.
- **Zero dead links.** Every `[[wikilink]]` in a committed article must resolve to a published article or a `status: stub` placeholder. If a target article does not yet exist, create a one-sentence stub, or remove the link. See `naming-convention.md` §5.1 for the full rule.

Full naming rules: [`.agent/rules/naming-convention.md`](.agent/rules/naming-convention.md).

## How to submit

Submit contributions as pull requests to the `pointsav/media-knowledge-documentation` repository on GitHub.

Each pull request should include:

1. The Markdown file for the new or updated article.
2. A brief description of what changed and why.
3. A Spanish translation pair (`.es.md`) if the article is new.

**GitHub:** [github.com/pointsav](https://github.com/pointsav)

## Licensing

By contributing to this wiki, you agree that your contribution is licensed under [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).

## Questions

[open.source@pointsav.com](mailto:open.source@pointsav.com)
