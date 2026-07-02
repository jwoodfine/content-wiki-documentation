---
schema: foundry-doc-v1
title: "Placement — which wiki, which category"
slug: placement
category: internal
type: reference
content_type: reference
quality: complete
status: active
audience: contributor
bcsc_class: public-disclosure-safe
last_edited: 2026-07-02
editor: pointsav-engineering
---

> The routing half of the writing system. The register guides ([[house-core]] + the
> guide-* set, mapped in [[coverage-matrix]]) say **how** to write an artifact. This file
> says **where** it goes: which wiki, then which category. Every TOPIC, GUIDE, and JOURNAL
> is placed with these two decisions. The authoritative category list for each wiki is that
> wiki's root `categories.yaml` — this file is the decision aid that sits on top of it.

## Step 1 — which wiki

Three public wikis, one question each. Decide by subject, not by author or by artifact type.

| Wiki | It answers | Belongs here |
|---|---|---|
| **corporate** (`corporate.woodfinegroup.com`) | *Who is the company and what is the capital?* | The company, the investment vehicles, the financial model, distributions and transfers, governance and legal, risks, per-entity reports. Reader: investor, banker, auditor, lawyer. |
| **projects** (`projects.woodfinegroup.com`) | *What are the buildings and where do they go?* | The buildings and development classes, how they are built, how sites are chosen, the markets, the rollout programme, commercial-real-estate market context, urban context, architecture, and the maps and data behind it. Reader: architect/AEC, development-market firm, investor. |
| **documentation** (`documentation.pointsav.com`) | *How does the PointSav platform work?* | How the platform is built, its building blocks and patterns, security, AI, operating systems, services, applications, where it runs, the design system, governance and standards, how-to guides, reference. Reader: engineer, plus a finance reader arriving from corporate. |

If a subject seems to fit two wikis, place it by its **primary reason for existing**: a building's
*investment* framing → corporate links across to the building on projects; the building itself →
projects. Corporate and projects are deliberately two halves of one company story — corporate keeps
capital/legal/reporting; projects keeps buildings/markets. The market evidence that a corporate risk
factor cites lives on projects and is linked, never duplicated.

## Step 2 — which category

Open that wiki's root `categories.yaml` and match the artifact's subject to a category `scope`. Each
category's `scope` line is written to make this unambiguous; the `_index.md` landing confirms it. Known
placement facts, so they are never re-litigated:

- **JOURNAL → the `research` category** of its mapped wiki (per `.agent/rules/journal-registry.md`):
  corporate, projects, or documentation. Specialist GIS/BIM papers route to their specialist surfaces,
  not these three wikis.
- **GUIDE (operational how-to) → documentation `how-to`.** The canonical GUIDE source of record is the
  `woodfine-fleet-deployment` repository (Woodfine GitHub); the documentation wiki `how-to/` category is
  the publication surface. Both are true — source and surface are different things.
- **Buildings / development classes / sites / development markets / regions → projects** (never
  corporate — the prospectus's "Description of the Business" and "Development Markets" live here).
- **Prospectus / financial / securities / governance / reporting subjects → corporate.**
- **Platform / engineering / OS / service / app subjects → documentation.**

Within a growing per-place category (projects `markets`, `rollout`), follow the slug-band grammar in the
projects taxonomy (`about-*` framework < `atlas-*` index pages < `<country>-<subdivision>-<place>`), not
a new category — the flat category absorbs unbounded places by slug.

## Step 3 — sanity checks

- The category `id` you chose is a real entry in that wiki's `categories.yaml`. If nothing fits, the
  artifact is either mis-scoped or the taxonomy has a gap — raise it, do not invent a category.
- The register guide for the artifact type (from [[coverage-matrix]]) governs the writing; this file only
  governs placement. The two are independent: a TOPIC on any wiki still obeys the reference guide; a
  JOURNAL on any wiki still obeys the journal guide.
- On the corporate wiki, the conservative BCSC posture binds: nothing in a title, category, or lede reads
  as an offer, a solicitation, or a promise of a return. See the corporate `categories.yaml` design record
  (`.agent/audit/2026-07-02-category-redesign/proposal-corporate.md` §BCSC disclosure posture).

## Authority

- Each wiki's **root `categories.yaml`** — the machine-readable, canonical category list (id, name, scope,
  audience). The single source of truth for *where*.
- **`.agent/rules/journal-registry.md`** — which JOURNALs exist per surface, against the ~3–5 cap.
- The **register guides** ([[house-core]], [[coverage-matrix]], guide-*) — the single source of truth for
  *how*. This file defers to all of the above; it adds only the wiki-and-category decision that sits between
  them.
