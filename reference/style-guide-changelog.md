---
schema: foundry-doc-v1
title: "Style Guide — CHANGELOG"
slug: style-guide-changelog
category: reference
type: topic
quality: core
short_description: "Editorial standards for CHANGELOG.md files across Foundry repositories, covering keep-a-changelog format, the workspace versioning rule, per-line discipline, and the distinction between the changelog and git history."
status: pre-build
last_edited: 2026-04-30
editor: pointsav-engineering
cites: []
paired_with: style-guide-changelog.es.md
---

> A `CHANGELOG.md` records what changed and why in each version — one line per PATCH, one section per MINOR, one chapter per MAJOR — so readers can track the project's evolution without reading commit diffs.

A **CHANGELOG.md** is the human-readable record of a project's
version history. It is not a commit log — that exists in Git.
It is the curated summary a maintainer writes for contributors
who need to understand what changed between versions without
reading every commit. Foundry follows the
keep-a-changelog format, shaped by the workspace versioning rule
at `~/Foundry/CLAUDE.md` §7. The machine-readable counterpart
lives in
`service-disclosure/templates/changelog.toml`.

## When to use this template

Every active project in `pointsav-monorepo` and every
engineering repo in Foundry that ships version-tagged releases
carries a `CHANGELOG.md`. The file is created when the first
meaningful entry lands — not as an empty placeholder.

Content wikis (`content-wiki-*`) and deployment instances do not
maintain changelogs; their history is expressed through Git
commits and workspace-level `CHANGELOG.md` entries respectively.

## Frontmatter fields

`CHANGELOG.md` files do not carry YAML frontmatter. The
keep-a-changelog format opens directly with the `# Changelog`
heading and version sections. No citation-substrate fields are
required.

## Structure

The file structure follows three levels of the workspace
versioning rule:

| Level | When | Format |
|---|---|---|
| **Chapter** | Per MAJOR version | `## v<MAJOR>.0.0 — <date>` |
| **Section** | Per MINOR version | `### v<MAJOR>.<MINOR>.0 — <date>` |
| **Line** | Per PATCH (one per accepted commit) | `- <short SHA> — <what changed and why>` |

Newest version appears at the top. Within a MINOR section, the
optional subsection headers `Added`, `Changed`, `Deprecated`,
`Removed`, `Fixed`, and `Security` group related PATCH lines
when the section is long enough to warrant it. For short
sections, subsection headers add more noise than clarity.

Each line records what changed and why. The short commit SHA
links the entry to Git history. The who and when live in Git;
the changelog line does not repeat them.

## Register and tone

The register is operational. Short declarative sentences, past
tense, active voice where the subject is clear. Sentence-length
budget: mean around sixteen words, maximum around twenty-eight.

Every entry explains the change in terms of its effect on
consumers, not in terms of the implementation detail. "Added
`validate_frontmatter` to the public API" is informative;
"refactored the validation module's inner loop" is not.

The banned-vocabulary list applies. A changelog line that says
"improved robustness" or "enhanced functionality" says nothing
a reader can act on. Name the specific change.

Plain text renders cleanly in terminal readers (`less`,
`nano`). Do not use Markdown tables or code blocks inside
changelog entries. Short SHAs are formatted as inline
code when they appear (`abc1234`), but the line itself is
plain prose.

## Example

```markdown
# Changelog

## v0.2.0 — 2026-04-27

### Added
- `5e3b1a` — Phase 1C genre-template registry: 18 `.toml` + `.md`
  pairs and `get_template` / `get_template_description` accessors.
- `2f9c44` — `templates::ALL` const listing every `GenreTemplate`
  variant; required for exhaustive iteration at request-dispatch time.

## v0.1.0 — 2026-04-25

- `a1d0e9` — Phase 1A: `Family`, `GenreTemplate`, `ProtocolRequest`,
  `Frontmatter`, `validate_frontmatter`, `BANNED_VOCABULARY`;
  26 unit tests pass.
```

## See also

- [[style-guide-readme|Style Guide — README]]
- [[style-guide-architecture|Style Guide — ARCHITECTURE]]
- [[style-guide-inventory|Style Guide — INVENTORY]]

## References
