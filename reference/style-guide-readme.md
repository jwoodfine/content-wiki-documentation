---
schema: foundry-doc-v1
title: "Style guide — README"
slug: style-guide-readme
category: reference
type: topic
quality: complete
short_description: "Editorial standards for README.md files at repo roots and project roots in the platform, covering required sections, reader orientation, and the bilingual pair discipline."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-24
editor: pointsav-engineering
cites: []
paired_with: style-guide-readme.es.md
---

> A `README.md` is the first thing a collaborator or automated system reads when it enters a repository. It answers three questions in order: what is this, what do I need to know to use it, and where do I look next.

A **README** is the entry point for a repository or project directory. It is addressed to a reader who has no prior context — a new contributor, a review system, or an external collaborator encountering the repo for the first time. This article covers the human-facing standard; the machine-readable counterpart lives in `service-disclosure/templates/readme.toml`. The [[root-files-discipline|root files discipline]] governs which companion files may appear alongside the README at a repository root.

## When to use this template

Every repository root must carry a `README.md`. Projects inside a monorepo (`pointsav-monorepo/<prefix>-<name>/`) carry their own `README.md` at project root when the project is significant enough to be addressed independently. Thin adapters and single-file utilities do not require a separate project README — the repo-root README covers them.

Repositories with bilingual content (per workspace §6) also carry a `README.es.md` at the same level. Operational repos (internal tooling, deployment scaffolds) may defer the Spanish pair until a public-facing milestone.

## Structure

The template requires five sections in this order:

| Section | Purpose |
|---|---|
| **Opening** | One paragraph: what this repository or project is and who it is for. No headings before this paragraph — it appears immediately after any repo metadata. |
| **What this is** | What the repo contains or what the project does. Scope, not features. Two to four sentences. |
| **Layout** | An annotated directory tree or section listing. One phrase per entry. Describes structure, not behaviour. |
| **Using it** | The minimal sequence a new contributor needs to read, run, or build this repo's content. Prerequisites, then commands, then expected output. |
| **Where to look next** | A curated list of pointers to deeper documentation — ARCHITECTURE.md, CLAUDE.md, the relevant content-wiki TOPIC, the deployment guide. |

Optional sections (permitted at the end, after the required five): Contributing, Licence, Contact.

## Frontmatter fields

Repo-root `README.md` files carry no YAML frontmatter — they are plain Markdown for GitHub rendering. Project-root `README.md` files inside `pointsav-monorepo` also carry no frontmatter.

Content-wiki README-style articles (when a wiki article explains a README's design) use the standard `foundry-doc-v1` schema with `type: reference`.

## Register and tone

Plain English. Address the reader directly where helpful ("To build the crate, run…"). Avoid jargon that is not defined in the same document or available from a linked TOPIC. Mean sentence length around twenty words; nothing over forty.

The banned-vocabulary list applies. Do not use `"utilize"`, `"leverage"`, `"seamless"`, or `"robust"` in a README. State the actual behaviour, not the aspiration.

Bilingual pairs (`README.md` + `README.es.md`) are strategic adaptations, not translations. The Spanish version may restructure, shorten, or reframe for a different reader's context while carrying the same factual content.

## See also

- [[style-guide-topic|Style Guide — TOPIC]]
- [[style-guide-guide|Style Guide — GUIDE]]
- [[language-protocol-substrate|Language Protocol Substrate]]
- [[root-files-discipline]] — allowed companion files at a repository root
