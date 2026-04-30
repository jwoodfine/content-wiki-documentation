---
schema: foundry-doc-v1
title: "Style Guide — README"
slug: topic-style-guide-readme
category: reference
type: topic
quality: core
short_description: "Editorial standards for README files in Foundry repositories, covering the three README sub-types, the bilingual pair requirement, voice discipline, forward-looking statement treatment, and the Standard Readme structure."
status: pre-build
last_edited: 2026-04-30
editor: pointsav-engineering
cites:
  - ni-51-102
  - osc-sn-51-721
paired_with: topic-style-guide-readme.es.md
---

# Style Guide — README

> A Foundry README is the first file a cold reader encounters in any repository and must orient them in three elements — identity, scope, and where to look next — before supplying any further detail.

The **README** is the most-read file in any repository. It is the
first artefact a cold reader, contributor, or evaluator sees, and
it sets the tone for everything else they read in the project.
Foundry has three README sub-types — workspace, repository, and
project — each with its own scope but a shared editorial
discipline. This style guide is the public-facing operational
document for contributors; the machine-readable counterpart lives
in `service-disclosure/templates/readme-*.toml`.

## What "README" means here

| Sub-type | Where it lives | What it does |
|---|---|---|
| **Workspace** | `~/Foundry/README.md` | Identifies the workspace, names the deployment it represents, points cold readers at `DOCTRINE.md`, `CLAUDE.md`, `NEXT.md`, `MANIFEST.md`. |
| **Repository** | `<repo>/README.md` | Standard Readme structure — Background, Install, Usage, Contributing, License. |
| **Project** | `<repo>/<project>/README.md` | Narrower than repo-level — what one project does, how to build and test it, license note pointing at the repo `LICENSE`. |

## The first 30 lines must work in plain editors

Foundry READMEs read cleanly in `nano`, `vim`, and `less` for the
first 30 lines. No centred hero blocks, no Mermaid diagrams, no
HTML, no badge clusters in the opening. After line 30, GitHub-
flavoured Markdown richness is fine — tables, code blocks, link
formatting, hierarchical lists.

The reason is concrete: many contributors first see a README
through a terminal, an SSH session, or a bare git client. A
README that opens with twenty lines of HTML reduces to a wall of
tag soup in those environments. Bloomberg articles do not lead
with a logo; READMEs need not either.

## Bilingual pair required

Every README ships as a pair: `README.md` (English) and
`README.es.md` (Spanish overview). The Spanish file is strategic
adaptation, not 1:1 translation. Translate the orientation a
non-English-speaking reader needs, drop the implementation
detail that the English text already covers in depth.

This rule applies to README files specifically. Operational
documents (CLAUDE.md, NEXT.md, CHANGELOG.md, ARCHITECTURE.md)
remain English-only.

## Voice — Bloomberg, not marketing

The standard is "Bloomberg article standard": precise,
professional, and understandable to a financially literate reader
without a technical background. Active voice unless passive
carries specific meaning. Sentence-length budget: mean around
eighteen words, maximum around thirty.

The banned-vocabulary list applies. The terms `leverage`,
`empower`, `next-generation`, `industry-leading`, `seamless`,
`robust`, `cutting-edge`, and `world-class` carry no information;
they are the verbal tics of marketing copy and they signal to
informed readers that the writer has nothing specific to say.

## Forward-looking statements carry cautionary language

Where a README describes future capability, timeline, customer
outcome, or governance arrangement, the language is `planned`,
`intended`, `may`, or `target` — never declarative-future. This is
the BCSC continuous-disclosure posture per `[ni-51-102]`, with
the additional discipline from `[osc-sn-51-721]` that
forward-looking statements carry a stated reasonable basis,
cautionary language, and material assumptions.

The discipline applies whether or not the relevant entity is
currently a reporting issuer. The cost of treating every
artefact as potentially reviewable is small; the cost of
retrofitting compliance after the fact is significant.

## What every README has

A Foundry README opens with three things:

1. **Identity** — the canonical name from the Nomenclature
   Matrix, in one sentence. No tagline.
2. **Scope** — what the project does and what it does not do, in
   one short paragraph.
3. **Where to look next** — links to the constitutional charter
   (`DOCTRINE.md` at workspace), operational guide (`CLAUDE.md`
   at this directory), open work queue (`NEXT.md`), and the
   relevant content wiki for deeper background.

Beyond those three, the Standard Readme structure (Background,
Install, Usage, Contributing, License) carries the rest. Sections
that do not apply are omitted rather than padded — a project
without an install step does not need an Install section that
says "no installation required".

## Canonical names matter

Names from the Nomenclature Matrix are not substituted with
synonyms. ToteboxOS is not "ArchiveOS"; ConsoleOS is not
"Frontend"; service-slm is not "the AI service". Substitution
breaks discoverability and signals to readers that the writer
has not internalised the platform's vocabulary.

Reference sibling projects by canonical name when the
architecture is related. A reader skimming a project README who
sees a canonical sibling name knows where to look next; a reader
who sees a paraphrase has to decode it.

## What this style guide is not

It is not a copy template. The `service-disclosure` machine-
readable templates are the structured form that the per-tenant
adapter pipeline consumes; this article is the human form that
contributors read once and internalise. Both must agree.

It is not a substitute for editorial review. The
apprenticeship-substrate produces verdict-signed training tuples
on every editorial action so the per-tenant adapter learns the
voice over time. This article tells contributors and the
apprentice what voice they are aiming for.

## See Also

- [[topic-style-guide-topic|Style Guide — TOPIC]]
- [[topic-style-guide-guide|Style Guide — GUIDE]]
- [[topic-language-protocol-substrate|Language Protocol Substrate]]
- [[topic-anti-homogenization-discipline|Anti-Homogenization Discipline]]

## References
