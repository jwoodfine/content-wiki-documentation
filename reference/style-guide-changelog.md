---
schema: foundry-doc-v1
title: "Style guide — changelog"
slug: style-guide-changelog
category: reference
type: topic
quality: complete
short_description: "Editorial standards for CHANGELOG.md files in platform repositories: versioning discipline, entry format, newest-first ordering, and the distinction between a changelog and a commit log."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-24
editor: pointsav-engineering
cites: []
paired_with: style-guide-changelog.es.md
---

> A changelog answers one question for every version: what changed, stated in one line, from the reader's point of view.

A **CHANGELOG.md** records meaningful changes to a repository at each version boundary. It is addressed to a reader who wants to know what a new version contains without reading a diff. A changelog is not a commit log — it selects, compresses, and reframes the commit history for a consumer who cares about impact, not implementation. This article is the human-facing standard; the machine-readable counterpart lives in `service-disclosure/templates/changelog.toml`.

## When to use this template

Every repository that carries version numbers uses a `CHANGELOG.md`. The file is created when the first meaningful entry exists — not as a placeholder. Repositories that do not version (pure content stores without a semantic version) may omit it; they track meaningful changes in `NEXT.md` or `cleanup-log.md`.

## Structure

The changelog is a flat list of version blocks, newest at the top:

```markdown
## M.m.P — YYYY-MM-DD

- <one-line entry, reader-facing>
- <one-line entry, reader-facing>

## M.m.P-1 — YYYY-MM-DD

- <one-line entry, reader-facing>
```

Each version block:

- Heading level `##`. Version number and ISO 8601 date on the same line.
- One bullet per meaningful change. Bullets are reader-facing: describe the effect, not the mechanism. "Adds X" rather than "Implemented the X module."
- Grouping labels (`### Added`, `### Fixed`, `### Changed`) are permitted when a version has more than five entries. Omit them when a version has five or fewer — grouping adds noise below that threshold.

## What counts as a changelog entry

Include:

- New capabilities available to consumers.
- Breaking changes to the public surface.
- Significant bug fixes with user-visible impact.
- Major structural changes (module split, rename).

Exclude:

- Internal refactors with no consumer-visible effect.
- Test additions or CI changes.
- Documentation-only commits (these are implicit in the version date).
- Version-bump commits (the heading captures this).

## Register and tone

Plain. Active voice, present tense: "Adds support for X", "Fixes the Y parsing failure." Not "We've added" or "This version includes." Not "Various improvements" — name what changed.

Sentence-length budget: one line per entry, target under twenty words. The date on the version heading uses ISO 8601 (`YYYY-MM-DD`). The version number follows the workspace versioning rule (MAJOR.MINOR.PATCH per workspace §7): PATCH increments per accepted commit; MINOR increments per feature milestone.

## See also

- [[style-guide-readme|Style Guide — README]]
- [[style-guide-architecture|Style Guide — ARCHITECTURE]]
- [[language-protocol-substrate|Language Protocol Substrate]]
