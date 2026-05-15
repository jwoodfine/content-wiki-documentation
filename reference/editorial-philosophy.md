---
schema: foundry-doc-v1
title: "Editorial Philosophy"
slug: editorial-philosophy
category: reference
status: stable
bcsc_class: no-disclosure-implication
last_edited: 2026-05-08
editor: pointsav-engineering
---

Every article in the Foundry wikis is a learning resource, not a reference lookup. A reader who finishes an article should understand the subject — not just have retrieved a fact. Wikipedia is the model: structured, internally linked, deep enough to build genuine understanding, and consistent enough that a reader who knows Wikipedia recognises the layout immediately and knows how to navigate it. This article explains what that means in practice and how it shapes every editorial decision.

## The Wikipedia model

Wikipedia succeeds at something that most documentation does not: it teaches. A reader who arrives looking up "direct-hold property structure" or "service-slm" or "co-location mandate" leaves with a mental model, not just a definition. That happens because Wikipedia articles are built around understanding, not retrieval.

Three structural choices produce this outcome:

**1. The encyclopedic lead.** The first paragraph of a Wikipedia article contains the most important facts about the subject — in plain language, at the right level of abstraction for a general reader. The lead does not assume prior knowledge. It does not start with a definition. It starts with consequence: why this thing matters, what it does, what the reader gains by understanding it.

**2. Internal linking that builds webs of understanding.** Articles link to each other using `[[slug]]` wikilinks. A reader who follows the links progressively builds richer knowledge of the subject. Red links — links to articles that do not yet exist — are features, not defects. They show the reader where the encyclopedia is incomplete and invite contribution.

**3. Consistent structure.** Lead paragraph → body sections → See also → References. This structure is Wikipedia's muscle memory. A reader who has used Wikipedia for ten minutes recognises it. The recognition is itself a form of trust — the reader knows how to use the article before they read it.

The Foundry wikis apply this model to three distinct audiences in three distinct language registers. The structure is the same. The register shifts to match the reader.

## The encyclopedic test

Every article should pass one test:

*Does a reader who finishes this article understand the subject, or have they only found a fact?*

A fact-retrieval article answers "what is X." An encyclopedic article answers "what is X, why does it matter, how does it work, and how does it connect to Y and Z." The second article is a learning resource. The first is a glossary entry.

This test applies to all three wikis:

- **Corporate:** After reading `direct-hold-structures`, a banker understands why Woodfine uses this structure, what it means for capital allocation, and how it differs from pooled structures — not just what the term means.
- **Projects:** After reading `co-location-mandate`, a developer or architect understands the logic behind the mandate, the capital framework that validates it, and the market conditions that make it viable.
- **Documentation:** After reading `service-slm`, an engineer understands the routing logic, why the tier thresholds are set the way they are, and what the consequence is for the operator — and an institutional reader scanning section headers understands that the platform manages AI costs automatically without sending requests off-premises.

If an article fails this test, the rewrite adds the relationships, context, and consequence framing that turn a fact into understanding.

## DataGraph-enriched content

The Foundry wikis are connected to a property graph database — the DataGraph — that accumulates knowledge about every entity in the platform: what each entity connects to, which domain it belongs to, which themes span it, and what the research corpus says about it.

The wiki articles were authored before the DataGraph was fully populated. The DataGraph now knows things that many articles do not yet express. A DataGraph-informed rewrite adds that knowledge to the article:

- **What connects to what.** An article about `service-slm` that does not mention the three compute tiers, the access-control gateway it transits, or the audit log it produces is incomplete — not because those facts are missing, but because the reader cannot build the mental model without them.
- **Why the institutional reader should care.** The consequence framing — the sentence that connects the technical mechanism to the business outcome — is often the piece that articles written for an engineering audience omit. "The routing logic is operator-controlled" is a fact. "A request that resolves locally never leaves the customer's infrastructure — and never appears on a cloud billing statement" is a consequence that builds understanding.
- **Domain and theme context.** An article that explains what a service does without explaining where it sits in the platform architecture leaves the reader with a fact and no map. Domain and theme connections are how the reader builds the map.

**The two inputs to every article:**

| Input | Source | What it provides |
|---|---|---|
| **How to write** | RESEARCH corpus → language tokens | Register, sentence structure, vocabulary, consequence-first lead |
| **What to say** | DataGraph — entities, relationships, domains, themes | Content the article was written before the DataGraph existed to supply |

The language tokens govern register. The DataGraph governs substance. An article that has correct register but thin substance fails the encyclopedic test. An article that has rich substance but wrong register fails to communicate. Both inputs are required.

## The monthly improvement cycle

The Foundry wikis improve continuously through a monthly content sweep. Each sweep runs against an updated DataGraph — refined by on-demand GPU inference passes that run daily and external API passes that run weekly or monthly as new source data accumulates. Each sweep takes every article one level higher in quality.

The mechanism: the inference system generates a new draft of each article against the current DataGraph. Editorial review produces a verdict — accept, refine, or reject. Each verdict is a training example that makes the next month's generated draft better. The language tokens score each generated draft for register correctness, so register drift is caught automatically.

The result is compounding improvement. Each monthly pass produces better training signal than the last because the DataGraph is richer, the system has been trained on prior editorial verdicts, and the articles being refined are themselves already better. The work required per article per month decreases as the system matures.

**The calibration rule:** The goal for each article in any given sweep is "draft 2 of 10" — good enough that the inference system produces a clearly better draft 3. Perfection in a single pass wastes effort better spent establishing the framework that makes every subsequent pass better.

## See also

- [[editorial-language-registers]] — the three registers and vocabulary rules that govern how each wiki is written
- [[style-guide-topic]] — article structure and Wikipedia-pattern conventions
- [[style-guide-guide]] — operational guide structure
- [[glossary-documentation]] — canonical term definitions
