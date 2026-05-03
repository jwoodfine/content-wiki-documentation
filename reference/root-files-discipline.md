---
schema: foundry-doc-v1
title: "Root Files Discipline"
slug: root-files-discipline
category: reference
type: topic
quality: published
short_description: The convention that every repository and project sub-clone keeps a small, explicitly enumerated set of canonical companion files at its root — and nothing else.
status: pre-build
last_edited: 2026-05-01
editor: pointsav-engineering
cites: []
paired_with: root-files-discipline.es.md
---

Every repository in the PointSav engineering framework keeps a clean root directory. Clean means that a small, explicitly enumerated list of files is permitted at the root and every other file is a defect requiring relocation. The Root Files Discipline names this canonical companion set, organises files into tiers by when in a repository's lifecycle they become required, and specifies the bilingual posture and prohibition list that applies uniformly across the framework.

## The tiered model

Six tiers, ordered by when in a repository's lifecycle they become required. The first tier is always required; the sixth must never appear.

**Tier 1 — Always required.** Every repository and every cluster sub-clone carries three files from the day it is created: a `README.md` as the English entry point, a `README.es.md` as a Spanish strategic-adaptation overview, and a `LICENSE` file containing the full text of the repository's primary licence. A repository missing any of these three is structurally incomplete regardless of how much code it contains.

**Tier 2 — Required when work is active.** When a project or cluster is in the Active lifecycle state, three additional files must be present: a `CLAUDE.md` operational guide for sessions opened in that directory, an `AGENTS.md` vendor-neutral pointer file that lets non-Anthropic coding agents discover the project's operational guide, and a `NEXT.md` listing open items in priority order. These three files land together in the activation commit; writing feature code without completing them first is a process defect.

The `AGENTS.md` convention, published in December 2025 and maintained under the Linux Foundation, enables coding agents from any vendor to discover the project's operational guide from a standard filename without requiring knowledge of any particular vendor's preferred filename. The substantive content lives in `CLAUDE.md`; `AGENTS.md` is a thin pointer.

**Tier 3 — Required when meaningful work has happened.** `CHANGELOG.md`, following the keep-a-changelog format with one entry per accepted commit, becomes required once a repository has content worth recording. The versioning rule applies: one patch increment per accepted commit, one minor increment per feature milestone, one major increment per breaking change.

**Tier 4 — Optional when warranted.** A range of additional companion files are appropriate in specific circumstances: `ARCHITECTURE.md` for repositories whose design warrants a dedicated overview, `SECURITY.md` for threat model and disclosure path, `INVENTIONS.md` for novel claims surfaced from the repository, `CONTRIBUTING.md` for repositories expected to receive open-tier contributions, `CITATION.cff` for repositories expected to be cited externally, and several others. Each is optional; the decision to add one is made when the repository's scope warrants it, not by default.

**Tier 5 — Tooling files per repository type.** These appear when the repository type calls for them. Rust workspace repositories carry `Cargo.toml` and `Cargo.lock`; Python projects carry `pyproject.toml`; every tracked directory carries `.gitignore`. These are expected at root for their respective repository types but are not canonical companion files in the doctrinal sense.

**Tier 6 — Prohibited at root.** Scripts belong inside the project directory they operate on, not at the repository root. User-facing documentation belongs in the documentation wiki. Architecture topics and ADRs belong in the documentation wiki. Design-system material belongs in the design-system repository. Large binaries are fetched at build time and never checked in. Files with version-number suffixes in their names — `_V2`, `_V3`, and similar — represent edit-in-place violations and are moved to the proper single canonical file with history preserved in Git.

## Licence discipline

The `LICENSE` file in every repository is the single most consequential Tier-1 file. It determines what downstream consumers may do with the repository's content. The framework maintains a licence directory in the factory-release-engineering repository as the source of truth for every licence text used across the framework. Licence assignments are declared in a machine-readable map that names which licence applies to which repository, sometimes with per-path overrides for mixed-licence monorepos. A propagation script reads the map and copies the appropriate licence text into each target repository's `LICENSE` file when governance propagation runs.

Source files carry SPDX licence identifier headers using the standardised identifier vocabulary rather than embedding full licence text inline.

## Bilingual posture

The bilingual rule from the workspace-level operational guide applies uniformly. Public-facing material is bilingual: `README.md` with `README.es.md`, TOPIC files in the documentation wiki, and the constitutional doctrine with its Spanish overview. Internal operational documentation — `CLAUDE.md`, `NEXT.md`, `CHANGELOG.md`, runbooks — is English-only. The discriminator is whether a fresh reader outside the framework's English-speaking operators might encounter the file; if so, it carries a Spanish pair.

## Why this convention exists

The Root Files Discipline serves three structural purposes. It makes repositories immediately navigable for contributors arriving with any coding agent: both `AGENTS.md` and `CLAUDE.md` are present and pointing the same direction. It makes repositories citable through `CITATION.cff` at every repository expected to receive external citations, supporting the citation substrate that treats provenance as a first-class concern. And it ensures that licence boundaries are unambiguous at every repository root, which is the precondition for the three-tier contributor model — core, paid, and open contributors — to operate legally at scale.

Missing files surface at session start when any session in a repository observes that a required Tier-1 or Tier-2 file is absent. The session records the defect and proceeds with the actual task; it does not silently create the missing file or ignore the absence.

## See also

- [[project-tetrad-discipline]] — The project lifecycle that determines when Tier-2 files become required.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
