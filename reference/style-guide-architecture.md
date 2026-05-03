---
schema: foundry-doc-v1
title: "Style Guide — ARCHITECTURE"
slug: style-guide-architecture
category: reference
type: topic
quality: core
short_description: "Editorial standards for ARCHITECTURE.md files at project roots in the Foundry monorepo, covering required sections, technical register, module-layout conventions, and the non-goals discipline."
status: pre-build
last_edited: 2026-04-30
editor: pointsav-engineering
cites: []
paired_with: style-guide-architecture.es.md
---

> An `ARCHITECTURE.md` at a project root explains where the project sits in the larger system, what it exposes, how its modules are organised, and — equally important — what it is not.

An **ARCHITECTURE.md** is the technical reference for a single
project in `pointsav-monorepo`. It is written for an audience
that already knows the platform's vocabulary and wants to
understand one project's place in the system, its outward-facing
interface, and the internal organisation of its code. It is not
a tutorial and not a runbook. This article is the
human-facing operational form; the machine-readable counterpart
lives in
`service-disclosure/templates/architecture.toml`.

## When to use this template

An `ARCHITECTURE.md` belongs at a project root whenever the
project's design is complex enough that a contributor picking
it up cold could not reconstruct its structure from the source
files alone. Projects with more than two significant modules,
a non-obvious layering decision, or a meaningful consumer
contract with other parts of the system warrant an
`ARCHITECTURE.md`.

Single-file utilities, thin adapters, and pure data directories
do not warrant one. When in doubt, write a short version —
four sections plus an annotated file tree is a complete
`ARCHITECTURE.md`.

## Frontmatter fields

`ARCHITECTURE.md` files do not carry YAML frontmatter. The
template describes a plain Markdown file with a section
structure enforced by the per-genre validator in
`service-disclosure`. No citation-substrate fields are required
because the file is a project-root artefact, not a content-wiki
article.

## Structure

The template requires four sections in this order:

| Section | Purpose |
|---|---|
| **Position** | Where this project sits in the larger system — which ring, which service family, which consumer-producer relationships. One or two paragraphs. Reference siblings by canonical Nomenclature Matrix name. |
| **Public surface** | The API, interface, or contract this project exposes to the rest of the codebase. List types, functions, or endpoints the consumer depends on. |
| **Module layout** | Annotated directory tree of the project's internal organisation. ASCII-art suffices. One phrase per leaf explaining its responsibility. |
| **What this is not** | Explicit non-goals. Name the things a reader might reasonably expect this project to do but that it does not. This section limits readers' interpretation and prevents feature-creep. |

Sections are separated by `##` headings and appear in the order
above. Adding a fifth or sixth section is acceptable when the
project has meaningfully distinct concerns (for example, a
"Threading model" section for a concurrent service). Omitting
a required section is not.

## Register and tone

The register is technical. Assume domain familiarity; do not
explain the platform's general architecture in an
`ARCHITECTURE.md` for a specific project — that belongs in a
TOPIC in `content-wiki-documentation`.

Sentence-length budget: mean around eighteen words, maximum
around thirty. Active voice. Diagrams for cross-component
relationships are encouraged; ASCII-art trees suffice for module
layout. Every canonical project or service name is used exactly
as it appears in the Nomenclature Matrix — no paraphrases, no
abbreviations.

The banned-vocabulary list applies. Technical writing that says
"robust", "seamless", or "leverage" signals vagueness; an
`ARCHITECTURE.md` should name the specific invariant, the
specific interface, or the specific dependency.

## Example

```markdown
## Position

`service-disclosure` holds the schema substrate for Foundry
editorial work. It sits in Ring 2 alongside `service-content`
and is consumed at request time by `service-slm` (the Doorman)
to validate incoming protocol requests before routing.

## Public surface

- `Family` — four-variant enum identifying the adapter family.
- `GenreTemplate` — eighteen-variant enum; each maps to a
  `.toml` + `.md` pair under `templates/`.
- `validate_frontmatter(fm: &Frontmatter) -> Result<(), ValidationError>`

## Module layout

service-disclosure/
├── src/
│   ├── lib.rs          # crate root; re-exports; BANNED_VOCABULARY
│   ├── genre.rs        # Family + GenreTemplate
│   ├── frontmatter.rs  # Frontmatter struct
│   └── validate.rs     # validate_frontmatter + ValidationError
└── templates/          # 18 .toml + 18 .md pairs

## What this is not

- Not an inference engine. Prompt scaffolding lives in the
  template `.toml` files; the Doorman composes prompts at
  request time.
- Not a storage layer. Documents live in `service-content`.
```

## See also

- [[style-guide-readme|Style Guide — README]]
- [[style-guide-topic|Style Guide — TOPIC]]
- [[style-guide-guide|Style Guide — GUIDE]]
- [[language-protocol-substrate|Language Protocol Substrate]]

## References
