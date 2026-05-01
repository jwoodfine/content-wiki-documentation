---
schema: foundry-doc-v1
title: "The Apprenticeship Substrate"
slug: topic-apprenticeship-substrate
category: architecture
type: topic
quality: published
short_description: "A production routing protocol that inverts the usual AI-to-human workflow: a local model attempts a task first, a senior reviewer signs a verdict, and the disagreement between them — captured as signed training tuples — generates the highest-quality continued-pretraining signal the platform can produce."
status: pre-build
last_edited: 2026-05-01
editor: pointsav-engineering
cites: []
paired_with: topic-apprenticeship-substrate.es.md
---

The Apprenticeship Substrate inverts the usual order of AI-assisted work. Rather than a senior session authoring a result and optionally asking an AI to verify it, the local model — the apprentice — attempts the task first. The senior reviewer reviews the attempt and signs a verdict. The disagreement between attempt and verdict is captured as a signed training tuple and fed into the platform's continued-pretraining pipeline.

Every production session exercises the apprentice. Every signed verdict is a training tuple. Every task type that accumulates enough accepted verdicts graduates toward autonomous operation, eliminating the token cost of senior review for that type. The two effects — production value now, training signal for the future — compound with each other.

## Why interaction data is the most valuable training signal

Training a language model on observations of what a senior reviewer wrote produces one kind of improvement. Training on the interaction between an apprentice's attempt and the senior's correction produces an order-of-magnitude more efficient improvement per training example. This is the core finding from direct preference optimisation and related alignment training research.

The Apprenticeship Substrate is designed to produce interaction data on real production work, not synthetic benchmarks. Every task the platform performs in production is a candidate for apprenticeship capture. The quality of the signal is higher because the tasks are real, the stakes are real, and the senior's corrections reflect genuine judgment about what the correct result is.

This training signal is structurally inaccessible to platforms whose preference signal is averaged across all users — they cannot produce per-customer, per-task-type, per-contributor interaction data at the granularity the Apprenticeship Substrate generates.

## Three stages of progression

Every registered task type progresses through three stages based on accumulated verdict history.

**Review.** The apprentice attempts the task; the senior reviews every result before it is committed. The attempt and the verdict are captured as a training tuple regardless of outcome. New task types start here.

**Spot-check.** The apprentice's results are committed without per-result review; the senior reviews a sampled fraction and any results flagged by an anomaly detector. The sampling and flagging criteria are defined by the accumulated ledger evidence for that task type.

**Autonomous.** The apprentice operates without active review. Periodic batch audits provide the assurance layer. Post-commit reverts traced to apprentice results trigger an automatic demotion to the preceding stage.

The thresholds for promotion — 50 verdicts with an acceptance rate above 85% for the first promotion, 100 verdicts with an acceptance rate above 95% and no traced reverts for the second — are the initial values. They are tunable per-task-type based on what the ledger evidence shows.

## The brief, attempt, and verdict format

Each interaction has a structured format at all three stages.

A **brief** names the task type, the files in scope, the acceptance test the apprentice should make pass, and the doctrine citations that bound the work. The senior writes the brief before authoring the result themselves.

An **attempt** is the apprentice's proposed result: a chain of reasoning, a diff, a self-assessed confidence score, and a flag indicating whether the apprentice is requesting escalation to a more capable model.

A **verdict** is the senior's assessment: accept, refine, reject, or defer to a higher compute tier. For refine and reject verdicts, a one-sentence explanation is required. The verdict is signed with the same cryptographic signing primitive used for all platform commits, binding the senior's identity to their review. The signature cannot be repurposed — a namespace tag in the signing protocol ties each signature specifically to the apprenticeship-verdict context.

Verdicts are append-only once signed. Corrections require a new superseding verdict, recorded in the promotion ledger as a separate event.

## Shadow routing and continuous corpus growth

For task types not yet registered for production routing, the platform operates a shadow path: after every commit, a brief describing that commit is submitted and the apprentice produces what it would have done. The triple of brief, apprentice attempt, and actual result that landed is captured as a training tuple without a senior verdict.

Shadow-route tuples land in the corpus immediately at capture — they do not wait for a verdict to be written. This addresses a failure mode in naive apprenticeship systems where tuples accumulate in memory and are lost when a process restarts. The captured tuple carries a null verdict field that is filled in when a verdict is eventually signed; the corpus entry is updated in place rather than duplicated.

Training paths consume different subsets of the corpus: supervised fine-tuning uses the full corpus; direct preference optimisation uses only the verdict-signed subset, where the senior's correction is the preferred output and the apprentice's rejected attempt is the dispreferred output; continued pretraining uses the full corpus weighted by stage, with autonomous-stage tuples weighted most heavily.

## The durable brief queue

When the GPU burst model is used for apprentice inference and the burst instance is idle, a naive implementation would lose the brief when the HTTP call times out. The platform addresses this with a file-backed queue: the post-commit hook writes the brief as a file rather than making an HTTP call, and a background process drains the queue as inference capacity becomes available. Briefs queued while the burst instance is asleep are processed when it wakes.

The queue uses rename-based atomic state transitions and file-lock-based lease semantics, so a crashed worker does not leave briefs permanently in-flight — leases expire and return the brief to the queue. The corpus tuple lands after the apprentice completes, not at queue time.

## The editorial task type

The platform's editorial pipeline — where bulk draft content is refined through a structured register-alignment process — generates its own apprenticeship corpus. Every draft that enters the pipeline produces a creation event; every refinement produces a refinement event. Drafts that receive a subsequent creative-contributor edit produce a third event capturing the before and after of the creative pass.

Two distinct preference pairs emerge from the editorial lifecycle: one capturing the transformation from raw draft to register-aligned output, and one capturing the transformation from aligned output to creatively polished output. These pairs operate at different levels of the writing craft and do not conflict when used together in continued pretraining.

The editorial task type generates more tuples per unit time than code-oriented task types, because editorial output is produced at higher volume and more frequently than code changes. It is the primary source of domain-voice training signal for the platform's AI substrate.

## See Also

- [[topic-trajectory-substrate]] — the broader corpus typology of which the apprenticeship corpus is one component
- [[compounding-doorman]] — the Doorman that routes briefs to the local model and manages key custody for higher-tier inference
- [[topic-llm-substrate-decision]] — why OLMo 3's fully open structure makes the intended continued-pretraining outcome possible
- [[topic-four-tier-slm-substrate]] — the tier model that determines which compute handles apprentice inference at each stage

## References

1. Constitutional AI paper, arXiv 2212.08073 — foundational work on preference learning and verdict-based training.
2. Federated LoRA paper, arXiv 2502.05087 — federated adapter training mechanics.
3. S-LoRA, 2024 — concurrent adapter serving.
4. `conventions/apprenticeship-substrate.md` — source convention for this article.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
