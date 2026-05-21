---
schema: foundry-doc-v1
title: "Style guide — topic"
slug: style-guide-topic
category: reference
type: topic
quality: complete
short_description: "Editorial standards for TOPIC files in content wikis: the Bloomberg four-paragraph lede, 75/25 institutional register, CFO sentence test, named actors rule, voice, forward-looking language, citation discipline, and the distinction from GUIDE files."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-21
editor: pointsav-engineering
cites:
 - ni-51-102
 - osc-sn-51-721
paired_with: style-guide-topic.es.md
---

> A TOPIC file explains what something is — architecture, background, or platform context that a fresh reader needs to understand the platform — and is the counterpart of a GUIDE, which explains how to operate it.

A **TOPIC** file explains what something *is*. It is architecture, background — material a fresh reader needs to understand the platform. It is not how to operate something; that is a GUIDE file, covered in [[style-guide-guide|Style Guide — GUIDE]]. This article is itself a TOPIC, and the structure it follows is the structure it documents.

## The editorial standard

These five rules are the ratified editorial standard for every TOPIC. They were reconciled and operator-ratified on 2026-05-21. Where any other guidance in this document — or in [[editorial-language-registers]] — conflicts with a rule below, the rule below governs.

1. **Sentence length is budgeted by sentence role.** An expansion sentence — one that develops a mechanism or an argument inside a body section — runs to about 45 words at most. A disclosure sentence — the lede, a compliance claim, a regulatory statement — runs to 25 words at most. Vary the rhythm: every paragraph carries at least one short declarative sentence, so the prose reads as an accordion rather than a monotone.
2. **Active verbs describe present-fact mechanism.** Use the active voice to describe how something works now. Do not use it to assert a forward-looking claim as accomplished fact — capability, timeline, or outcome that is not yet true keeps `planned`, `intended`, `may`, or `target` (see "Forward-looking statements" below). Do not give a system human intent or feeling. There is no ban on `is`, `are`, or `was`: a plain copula is correct when the sentence states a fact.
3. **Analogy is a ceiling, not a quota.** An analogy is optional. Where one is used, hold to at most one per 300 words. A TOPIC with no analogy is fully compliant; a TOPIC that reaches for an analogy in every paragraph is not.
4. **The lede is the nut graf; the Franklin arc orders the body.** The Bloomberg four-paragraph lede carries the news in roughly the first 10% of the article. The Franklin arc — Crisis, then Quest, then Breakthrough — governs the order of body sections only. It never displaces the lede or delays the news.
5. **The SaaS-marketing register is rejected.** Public content does not adopt the promotional voice of a software-product landing page. Internal codenames — "Liquid Glass" among them — stay internal; they do not appear in public TOPIC text.

## Where TOPICs live

| Wiki | Subject | License |
|---|---|---|
| `content-wiki-documentation` | Vendor platform documentation | CC BY 4.0 (public) |
| `content-wiki-corporate` | Customer corporate principles | CC BY-ND 4.0 |
| `content-wiki-projects` | Customer project narratives | CC BY-ND 4.0 |

A TOPIC's home is the wiki whose subject matter it covers. A TOPIC about service architecture lives in `content-wiki-documentation`. A TOPIC about a customer's corporate principles lives in `content-wiki-corporate`. Crossing these boundaries silently is drift; surface the question rather than choosing arbitrarily.

## Bilingual pair required

Every TOPIC ships as a pair: the English file and a Spanish strategic adaptation (`.es.md`). The Spanish file is strategic adaptation, not 1:1 translation — translate the orientation a Spanish-reading audience needs; drop the deeper implementation detail.

A non-English-speaking contributor or reader should be able to locate themselves in the system without first decoding English-only material.

## Frontmatter is required

Every TOPIC declares its metadata in YAML frontmatter. The `cites` list is required when the article makes claims that resolve to external regulatory instruments, research papers, or technical specifications.

```yaml
---
schema: foundry-doc-v1
title: "Style Guide — TOPIC"
slug: style-guide-topic
category: reference
type: topic
quality: complete
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-15
editor: pointsav-engineering
cites:
 - ni-51-102
 - osc-sn-51-721
paired_with: style-guide-topic.es.md
---
```

Citation IDs resolve against the platform citation registry. Inline references in body prose use `[citation-id]` syntax. A new external reference is added to the registry first, then cited in the article.

## Bloomberg lede structure

A TOPIC opens with a Bloomberg-shaped lede of four paragraphs. The model: the first paragraph states the structural property in one sentence that satisfies a Goldman Sachs analyst reading on their phone. The second paragraph supplies one concrete fact or number that makes the first paragraph verifiable. The third explains the mechanism. The fourth states why it matters for a regulated buyer, an auditor, or a risk manager.

| Paragraph | Content | Test |
|---|---|---|
| 1 — What + so-what | The structural property and its compliance or risk consequence | Can a Goldman Sachs analyst read this on their phone and understand the point? |
| 2 — Concrete fact | A specific datum: metric, date, binary decision | Is this verifiable? Does it make paragraph 1 falsifiable? |
| 3 — Mechanism | How it works | Is this the simplest accurate description of the mechanism? |
| 4 — Why it matters | Consequence for compliance, custody, or risk | Does a regulated buyer or auditor know what action to take from this? |

**Stand-alone PDF test.** Print paragraphs 1–4 in isolation and hand them to a reader who will see nothing else. The essential compliance or risk message must survive. If it does not, revise the lede before any other edit.

A reader who stops after the lede should leave with the news. This is Bloomberg shape. The reasoning, supporting citations, and trade-off discussion follow the lede; they do not precede it. Opening with mechanism and arriving at the consequence at the end is academic-paper shape — the wrong shape for a public platform wiki.

## Voice — Bloomberg, not marketing

The standard is precise, professional prose understandable to a financially literate reader without a technical background. Active voice unless passive carries specific technical meaning. Sentence length follows the budgeted standard above — expansion sentences to about 45 words, disclosure prose to 25 — and every paragraph carries at least one short declarative sentence.

The banned-vocabulary list applies in full: `leverage`, `empower`, `next-generation`, `industry-leading`, `seamless`, `robust`, `cutting-edge`, `world-class`. These words carry no information. Their absence sharpens the prose; their presence dilutes it.

**Named actors and consequences.** Every active sentence names who does what and what the consequence is if they do not. "The Doorman holds every API key" names the actor. "API keys are managed centrally" hides who holds them and what happens if they are not held there. The passive construction is useful only when the actor genuinely does not matter; in most governance sentences, the actor is the point.

**CFO sentence test.** Every sentence must be useful to a chief financial officer — someone who understands contracts, risk, and regulation but does not read source code. Pure engineering detail without a business consequence belongs deeper in the article or in a footnote. "The storage engine appends to an immutable tile format" fails the test. "A record cannot be deleted or modified after it is written — the storage engine makes modification structurally impossible rather than policy-prohibited" passes it.

**"So what" discipline.** Every body paragraph answers the question: *so what for a regulated buyer or a risk-aware engineer?* A paragraph that describes a mechanism without stating its consequence for compliance, custody, cost, or risk should either have that consequence added or be collapsed into the paragraph that does.

## 75/25 institutional and developer register

A TOPIC in `content-wiki-documentation` is addressed to two audiences simultaneously: institutional readers (financial community, regulated buyers, compliance officers, auditors) and developer readers (engineers, architects, integrators). The target register is 75% institutional, 25% developer.

Institutional prose answers questions of the form: *does this satisfy my regulatory requirement? who owns this data? what happens if the vendor fails? what does the audit log look like?* Developer prose answers: *how does this work? what does the API look like? what are the edge cases?*

In practice: write the structural claim and its compliance consequence before the implementation detail. An article about the WORM ledger leads with "a record cannot be deleted or modified after it is written, satisfying SEC 17a-4(f) by structure" before it describes the tile format. An article about the Doorman leads with "no API key lives outside this boundary; every call is logged to the per-tenant audit ledger" before it describes the routing code.

## Internal governance vocabulary

The words **Doctrine** and **Convention** as internal governance vocabulary never appear in TOPIC body text or section headings. A Goldman Sachs analyst reading this wiki should encounter the underlying idea in institutional prose, not the internal name for the governance machinery.

Write the principle, not the label:

- Instead of "per Doctrine claim #7, no AI may write to the knowledge graph" → "no AI component writes to the knowledge graph; that path is exclusively deterministic"
- Instead of "this Convention establishes the commit-signing requirement" → "every commit must be signed with an SSH key verified against the platform's identity store"

Where the term is being defined as a first-class concept within the article — a TOPIC about constitutional amendment process, for example — use the term but immediately follow it with a plain-language translation.

## Forward-looking statements carry cautionary language

A TOPIC that describes future capability, timeline, customer outcome, or governance arrangement uses `planned`, `intended`, `may`, or `target` — never declarative-future. This is the BCSC continuous-disclosure posture per `[ni-51-102]` and the forward-looking discipline of `[osc-sn-51-721]`.

The Sovereign Data Foundation is referenced in planned and intended terms only. Treating it as a current equity holder or active governance body is a posture violation; future state is described as future state.

## Cite every non-obvious claim

A TOPIC that says "compose service-disclosure with service-content" cites neither — those are platform components and the reader can find them in the monorepo. A TOPIC that says "per the production AI literature, multi-LoRA composition above three adapters per request hits multi-task interference" needs a citation; the claim is non-obvious, the reader cannot verify it from the platform alone.

The discipline is not academic exhaustiveness. It is auditability. A reviewer reading the TOPIC five years from now should be able to follow each non-obvious claim back to its source.

## Edit in place

A TOPIC does not get a `_V2` or `_V3` suffix when revised. Edit the existing file; rely on Git history for prior versions. This applies with full weight to TOPIC files because the wiki renderer serves the latest committed version.

A TOPIC that has been substantially rewritten — new structural sections, removed claims, new citations — bumps `last_edited` in frontmatter. Routine wording polish does not require a frontmatter bump.

## What a TOPIC is not

A TOPIC is not a runbook. Operational instructions — "run this command, configure this setting, recover from this failure" — belong in GUIDE files inside the deployment subfolder they operate. A file that describes both is split.

A TOPIC is not a marketing piece. These wikis are public-facing in the sense that they are served at `documentation.pointsav.com`, but the audience is contributors, customers, regulators, and engineers — not buyers being persuaded.

A TOPIC is not internal-only material. Anything internal-only (in-flight cleanup, mailbox correspondence, deployment-specific notes) lives in the workspace's `.agent/` directories or deployment instances, not in a content wiki.

## See also

- [[style-guide-guide|Style Guide — GUIDE]]
- [[language-protocol-substrate|Language Protocol Substrate]]
- [[citation-substrate|Citation Substrate]]
- [[anti-homogenization-discipline|Anti-Homogenization Discipline]]
