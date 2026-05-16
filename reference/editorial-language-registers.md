---
schema: foundry-doc-v1
title: "Editorial Language Registers"
slug: editorial-language-registers
category: reference
status: stable
bcsc_class: no-disclosure-implication
last_edited: 2026-05-08
editor: pointsav-engineering
---

The three PointSav wikis address three distinct primary audiences. Each audience has different financial and technical literacy, different reasons for reading, and different vocabulary expectations. Writing in the wrong register produces content that fails to communicate — not because it is inaccurate, but because it addresses the wrong reader. This article defines the three registers, explains who each audience is, and provides the vocabulary rules that govern all three wikis.

## What a register is

A language register is the combination of sentence structure, vocabulary, depth, and tone appropriate for a specific audience in a specific context. A financial brief uses a different register than a technical specification. Bloomberg and the Financial Times use a different register than a building code. Stripe's developer documentation uses a different register than either. The PointSav wikis are written in three distinct registers — one per audience — applied consistently across every article.

Register is not style preference. It is the difference between a reader who understands what they came to learn and a reader who gives up and closes the tab.

## Audience map

| Wiki | Primary audience | Secondary audience | Register |
|---|---|---|---|
| `content-wiki-corporate` | Bankers, family offices, institutional investors | C-suite principals, corporate advisors | Bloomberg / FT / Economist |
| `content-wiki-projects` | Top-400 development firms, commercial architects, construction programme managers | Same institutional investors reading project subject matter | Bloomberg / FT / Economist |
| `content-wiki-documentation` | Software engineers, graphic designers, platform developers | Next-generation institutional readers evaluating technical credibility | Stripe / Cloudflare primary + Corporate accessibility layer |
| `bim.woodfinegroup.com` | Architects, engineers, building code officials | — | RIBA / IFC specification |
| `gis.woodfinegroup.com` | GIS analysts, co-location programme managers | — | Technical specification |
| `design.pointsav.com` | Design system contributors, component authors | — | Design specification (DTCG, component API) |

The corporate and projects wikis share a register because they share a primary audience. The subject matter shifts — corporate governance and capital structure versus real estate development programmes and co-location markets — but the reader's financial literacy and capital-allocation frame does not. A family office principal reading about direct-hold tax structures and then reading about co-location development sites is the same person applying the same evaluative frame to different subject matter.

## Register 1 — Bloomberg / FT / Economist

**Applies to:** `content-wiki-corporate` and `content-wiki-projects`

The reader is an institutional decision-maker. They have financial literacy and no obligation to understand software architecture or building codes. They are reading to make a capital allocation decision or to evaluate the platform's sponsors and structure.

**Rules:**
- Sentence length: 14–18 words target; 25-word hard limit
- Lead structure: consequence first — the most important fact for a capital allocator goes in sentence one
- Voice: active. Passive voice hides responsibility and reads as evasion.
- Numbers: always specific. "$7 per month" not "low cost." "Top-400 development markets" not "major markets."
- Jargon: translate everything on first use. Platform-internal terms do not appear without a plain-language equivalent immediately preceding them.
- Code blocks: never. The corporate and projects reader does not need to see terminal commands.
- Citations: financial research, regulatory filings, industry reports, market data
- Avoid: academic hedging, abstract nouns, dramatic marketing claims, platform-internal metaphors

**Consequence-first pattern:**

*"The Direct-Hold framework removes the pool. Each property is its own legal and financial unit."*

*"Each co-location development site is underwritten as an independent capital event. Woodfine does not pool site performance — convergence at a node is validated independently before capital is committed."*

Same reader, same register, different subject matter.

## Register 2 — Stripe / Cloudflare + Corporate accessibility layer

**Applies to:** `content-wiki-documentation`

The primary reader is a software engineer, designer, or developer. They have technical literacy and are reading to understand how the platform works, how to deploy it, or how to contribute to it. The secondary reader — increasingly important — is a next-generation institutional reader: a bank's technology committee, a family office's next-generation principal, a senior developer from a Top-400 firm who is evaluating whether the platform is credible enough to approve or fund. This reader is technically literate — they can read code — but does not know the platform's internal vocabulary.

**Rules:**
- Structure per section: Concept → Why it matters (one sentence, consequence-first, no jargon) → How it works → Code → Edge cases
- The "why it matters" sentence must stand alone for the institutional reader scanning section headers — it is the Corporate accessibility layer
- Code blocks: real and runnable. If abbreviated, mark with `# ...`
- Field jargon (gRPC, systemd, JSON, async): use freely — no need to explain
- Platform-specific terms: define once in plain language on first use, then use the term
- Tone: peer-level, confident, direct — engineer to engineer
- Avoid: over-explaining basics (HTTP, SSH, git), vague architecture descriptions, incomplete examples

**Accessibility layer pattern:**

*"**service-slm** routes every AI request to the cheapest compute tier that meets the deadline, without the caller specifying which tier. Local inference first (5 s), cloud burst second (10 s), external API last (30 s). A request that resolves locally never leaves the customer's infrastructure — and never appears on a cloud billing statement."*

The last sentence is the Corporate accessibility layer. An institutional reader scanning section headers gets: "it can run locally, and you pay nothing when it does."

## Register 3 — RIBA / IFC specification

**Applies to:** specialist deployment sites only — `bim.woodfinegroup.com`, `gis.woodfinegroup.com`, `design.pointsav.com`

Prescriptive specification language (shall / shall not for requirements, measurements with units, normative vs informative distinction, standards citations) is the correct register for the specialist sites. It does not appear in the three main wikis because the main wiki audience is the institutional decision-maker, not the compliance engineer. "Shall" language reads as aggressive to a capital allocator. Specification language signals "compliance document," not "credible platform."

**Specialist sites as cross-reference destinations:**

When a main wiki article references a topic requiring prescriptive specification, link to the relevant specialist site:

- *"For full climate zone token specifications and IFC mappings, see `bim.woodfinegroup.com`."*
- *"For co-location scoring methodology and zoning criteria, see `gis.woodfinegroup.com`."*
- *"For design token schemas and component specifications, see `design.pointsav.com`."*

These sites are canonical reference destinations, in the same way that Wikipedia articles link to technical standards — the main article is readable by a general audience; the specialist site is where you go to build or verify.

## Vocabulary retirement

These terms appear in current wiki articles written for an internal engineering audience. They must be translated for any externally-facing article.

| Retire | Replace with |
|---|---|
| Substrate | the data layer / the platform code / the security foundation |
| Doctrine | architectural principle / design decision / engineering policy |
| Compounding | training signal aggregation / model improvement over time |
| Leapfrog | designed to exceed / targeted to replace / planned for [date] |
| Doorman | access-control gateway / AI request router |
| Ring 1 / Ring 2 / Ring 3 | archive tier / data tier / inference gateway |
| Totebox | property archive / data vault |
| Yo-Yo pool | on-demand GPU instances / ephemeral inference nodes |
| Sovereign (adjective) | independently verifiable / operator-controlled |
| Compounding Substrate | the platform (first use); link to architecture article |
| Apprenticeship Substrate | the learning pipeline / the training system |
| LadybugDB | property graph database / the DataGraph store |

**Rule:** Retired terms may appear in architecture and services articles in the documentation wiki where they are being explicitly defined. They must not appear in corporate wiki, projects wiki, or GUIDE content without a plain-language translation immediately preceding them.

## See also

- [[editorial-philosophy]] — the Wikipedia learning environment model that defines the purpose all three registers serve
- [[style-guide-topic]] — article structure and Wikipedia-pattern conventions
- [[style-guide-guide]] — operational guide structure and code block conventions
- [[glossary-documentation]] — canonical term definitions
