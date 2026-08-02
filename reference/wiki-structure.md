---
schema: foundry-doc-v1
title: "How this knowledge base is organized"
slug: wiki-structure
category: reference
type: topic
content_type: topic
quality: complete
short_description: "A reader's map of the platform knowledge base: fourteen areas covering what PointSav builds, how it's built, and why it can be trusted, for every reader."
status: active
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
paired_with: wiki-structure.es.md
---

[[pointsav-overview|PointSav]] builds operating systems and services for regulated businesses
that need to own their data, their AI, and their record-keeping
outright. The platform runs on customer hardware, is built to produce
continuous-disclosure-grade records by structure, and operates fully
without AI for buyers that require an air-gap. This knowledge base
documents that platform. The articles are technical — written for
developers first — but the map below is written for everyone, including
readers arriving from the corporate knowledge base with no engineering
background. Each area name says plainly what it holds.

## What it is and how it's built

- **How It's Built** — how the platform is put together: a three-part
  build that separates what comes in, the record-keeping core, and
  optional AI — and the principle behind it: customers own their
  running instance outright, on their own hardware. Start here for the
  big picture, including how the business model follows from the
  architecture.
- **Building Blocks** — the reusable pieces the platform is built from.
  If an article elsewhere names a mechanism you don't recognize, its
  definition lives here.
- **Design Patterns** — the named, repeatable shapes the platform
  reuses to solve coordination and ownership problems, written up once
  and referenced everywhere.

## Why it can be trusted

- **Security and Trust** — how the platform is protected and how its
  records are verified: identity and permissions, cryptographic
  verification, isolation boundaries, how data is handled and kept
  private, and the supply-chain controls designed to keep code honest
  from contributor to production.
- **How AI Is Used and Contained** — the platform's most distinctive
  design choice, stated plainly: the core data pipeline runs entirely
  without AI, and where AI is used it cannot write to the authoritative
  record. These articles explain the boundary that enforces that, how
  requests are routed between models, and the small, customer-side
  models designed to learn a customer's own environment.

## The platform, piece by piece

- **Operating Systems** — the operating systems PointSav ships, one
  article per system.
- **Platform Services** — the always-on background services, one
  article per service: what it does and what data it owns.
- **Applications** — the applications people actually use, from the
  public knowledge sites to the internal consoles.
- **Where It Runs** — where everything physically runs: customer
  hardware, deployment, storage, telemetry, and the shared compute
  network that pools hardware across sites.
- **Design and Brand** — how the platform looks and speaks: design
  philosophy, visual vocabulary, and brand surfaces.

## How decisions are made

- **Governance and Standards** — how engineering decisions are made and
  recorded: decision records, licensing and legal structure, and
  disclosure discipline. Readers from the financial community will find
  the compliance material here.

## Working with the platform

- **How You Run It** — step-by-step instructions for the hands-on work:
  installing, configuring, deploying, operating. Customers run their
  own instance, so these are written for a reader at a keyboard.
- **Glossary and Reference** — every term defined in plain words, plus
  the catalogues used across the knowledge base. The fastest route to
  an unfamiliar term.
- ~~**Research**~~ (Correction, 2026-08-02: the `research/` category was retired 2026-07-15, `naming-convention.md` Decision #13 — no `research/` directory exists on disk, and `categories.yaml` lists thirteen categories, not fourteen. JOURNAL papers now publish to each product site's own `/research` page under the sovereign-per-surface model, not to this wiki. This article's own headline "fourteen areas" claim needs correcting to thirteen. Flagged, not resolved.)

Every article is published in English and Spanish. Category pages list
their articles alphabetically; each opens with a curated guide to the
area before the full list.
