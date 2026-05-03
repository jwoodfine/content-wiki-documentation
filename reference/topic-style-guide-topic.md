---
schema: foundry-doc-v1
title: "Style Guide — TOPIC"
slug: topic-style-guide-topic
category: reference
type: topic
quality: core
short_description: "Editorial standards for TOPIC files in Foundry content wikis, covering where TOPICs live, the bilingual pair requirement, frontmatter citation discipline, voice, forward-looking statement treatment, and the distinction from GUIDE files."
status: pre-build
last_edited: 2026-04-30
editor: pointsav-engineering
cites:
  - ni-51-102
  - osc-sn-51-721
paired_with: topic-style-guide-topic.es.md
---

# Style Guide — TOPIC

> A TOPIC file explains what something is — doctrine, architecture, or background that a fresh reader needs to understand the platform — and is the counterpart of a GUIDE, which explains how to operate it.

A **TOPIC** file (`topic-<subject>.md`) in a Foundry content wiki
explains what something *is*. It is doctrine, architecture, or
background — material a fresh reader needs to understand the
platform. It is not how to operate something; that is a GUIDE
file, covered in [[topic-style-guide-guide|Style Guide — GUIDE]].
This article is itself a TOPIC, and the structure it follows is
the structure it documents.

## Where TOPICs live

| Wiki | Subject | License |
|---|---|---|
| `content-wiki-documentation` | Vendor platform documentation | CC BY 4.0 (public) |
| `content-wiki-corporate` | Customer corporate doctrine | CC BY-ND 4.0 |
| `content-wiki-projects` | Customer project narratives | CC BY-ND 4.0 |

A TOPIC's home is the wiki whose subject matter it covers. A
TOPIC about service architecture lives in
`content-wiki-documentation`. A TOPIC about a Customer's
corporate doctrine lives in `content-wiki-corporate`. Crossing
these boundaries silently is drift; surface the question rather
than choosing arbitrarily.

## Bilingual pair required

Every TOPIC ships as a pair: `topic-<subject>.md` (English) and
`topic-<subject>.es.md` (Spanish overview). The Spanish file is
strategic adaptation, not 1:1 translation — translate the
orientation a Spanish-reading audience needs, drop the deeper
implementation detail.

The pattern matches the README rule. The reason is the same: a
non-English-speaking contributor or reader should be able to
locate themselves in the system without first decoding English-
only material.

## Frontmatter is required

Per `~/Foundry/CLAUDE.md` §16 citation discipline, every TOPIC
declares its citation dependencies in YAML frontmatter:

```yaml
---
title: "Style Guide — TOPIC"
slug: topic-style-guide-topic
category: reference
status: pre-build
last_edited: 2026-04-27
editor: pointsav-engineering
cites:
  - ni-51-102
  - osc-sn-51-721
---
```

The required fields are `title`, `slug`, and `category`. The
`cites` list is required when the article makes claims that
resolve to external regulatory instruments, research papers, or
technical specifications. Citation IDs resolve against
`~/Foundry/citations.yaml`. Inline references in body prose use
`[citation-id]` syntax (e.g., `[ni-51-102]`) and may carry
clause references (`[ni-51-102 §4A.2]`).

The renderer accepts unknown citation IDs but renders them as
broken citations. A new external reference is added to
`citations.yaml` first, then cited in the article. The
registry-update commit and the article commit may land
separately if the registry edit happens at workspace tier and
the article edit is at content-wiki tier.

## Show before telling

A TOPIC opens with the artefact a reader can hold in their head.
For a service description, that is a one-paragraph summary
saying what the service does and where it sits in the platform.
For an architecture description, that is a diagram or an
annotated tree of the relevant components. For a doctrine
explainer, that is the core claim in one sentence.

The reasoning, the supporting citations, and the trade-off
discussion follow. Inverting that order — opening with reasoning
and arriving at the artefact at the end — is academic-paper
shape, not Bloomberg shape. A reader who stops after the first
two paragraphs of a Bloomberg article still leaves with the
news; the same standard applies here.

## Voice — Bloomberg, not marketing

The standard is precise, professional prose understandable to a
financially literate reader without a technical background.
Active voice unless passive carries specific meaning. Sentence-
length budget: mean around eighteen words, maximum around
thirty.

The banned-vocabulary list applies in full: `leverage`,
`empower`, `next-generation`, `industry-leading`, `seamless`,
`robust`, `cutting-edge`, `world-class`. None of these words
carry information. Their absence sharpens the prose; their
presence dilutes it.

## Forward-looking statements carry cautionary language

A TOPIC that describes future capability, timeline, customer
outcome, or governance arrangement uses `planned`, `intended`,
`may`, or `target` — never declarative-future. This is the BCSC
continuous-disclosure posture per `[ni-51-102]` and the
forward-looking discipline of `[osc-sn-51-721]`.

The Sovereign Data Foundation specifically is referenced in
planned / intended terms only. Treating it as a current equity
holder or active governance body is a posture violation; future
state is described as future state.

## Cite every non-obvious claim

A TOPIC that says "compose service-disclosure with
service-content" cites neither — those are platform components
and the reader can find them in the monorepo. A TOPIC that says
"per the production AI literature, multi-LoRA composition above
three adapters per request hits multi-task interference" needs
a citation; the claim is non-obvious, the reader cannot verify
it from the platform alone.

The discipline is not academic exhaustiveness. It is
auditability. A reviewer reading the TOPIC five years from now
should be able to follow each non-obvious claim back to its
source.

## Edit in place

A TOPIC does not get a `_V2` or `_V3` suffix when revised. Edit
the existing file; rely on Git history for prior versions. This
is workspace policy per `~/Foundry/CLAUDE.md` §6, and it applies
with full weight to TOPIC files because the wiki renderer
serves the latest committed version.

A TOPIC that has been substantially rewritten — new structural
sections, removed claims, new citations — bumps `last_edited`
in frontmatter and may add a brief note at the bottom of the
article describing what changed. Routine wording polish does
not warrant the note.

## What a TOPIC is not

A TOPIC is not a runbook. Operational instructions — "run this
command, configure this setting, recover from this failure" —
belong in GUIDE files inside the deployment subfolder they
operate. A file that describes both is split.

A TOPIC is not a marketing piece. Foundry's wikis are public-
facing in the sense that they are served at
`documentation.pointsav.com`, but the audience is contributors,
customers, regulators, and engineers — not buyers being
persuaded.

A TOPIC is not internal-only material. Anything internal-only
(in-flight cleanup, mailbox correspondence, deployment-specific
notes) lives in the workspace `.claude/` directories or
deployment instances, not in a content wiki.

## See Also

- [[topic-style-guide-readme|Style Guide — README]]
- [[topic-style-guide-guide|Style Guide — GUIDE]]
- [[topic-language-protocol-substrate|Language Protocol Substrate]]
- [[topic-citation-substrate|Citation Substrate]]
- [[topic-anti-homogenization-discipline|Anti-Homogenization Discipline]]

## References
