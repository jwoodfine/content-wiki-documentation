---
schema: foundry-doc-v1
title: "Model Tier Discipline"
slug: model-tier-discipline
category: reference
type: topic
quality: published
short_description: The discipline for routing work to the appropriate AI model tier — deep-think, implementation, or mechanical — to match model capability to work shape and control inference cost.
status: pre-build
last_edited: 2026-05-01
editor: pointsav-engineering
cites: []
paired_with: model-tier-discipline.es.md
---

A platform that routes all inference work through the highest-capability model available regardless of work shape spends significantly more per output than necessary. A platform with no guidance on model selection leaves each contributor to make independent choices that may be inconsistent, cost-inefficient, or both. Model tier discipline is the structured approach that matches work shape to model capability, routes appropriate work to lower-cost tiers, and makes the routing decision explicit and reviewable.

## Three abstract tiers

Work shapes fall into three categories that map to three model tiers:

**Deep-think.** Architectural decisions, doctrine authoring, cross-cutting analysis, novel problem framing, multi-source synthesis. These are the tasks where a more capable model's additional reasoning ability produces materially better outputs. Examples: authoring a new convention, debugging a problem whose root cause is not yet identified, coordinating decisions across multiple workstreams.

**Implementation.** Following an established plan, single-component scoped work, well-specified feature implementation, code review against ratified conventions. A model at this tier can produce correct output on an established specification without needing the full reasoning capacity required for deep-think work. Examples: scaffolding a new module from a documented spec, drafting a runbook from a known template, writing unit tests for a defined interface.

**Mechanical.** Pattern-matching work with clear inputs and outputs, no architectural judgment, repeatable structure. The work is correct or incorrect in an unambiguous way. Examples: file moves, version number bumps, registry row updates, formatting normalization.

## The preferred in-seat routing mechanism

When a work session reaches a natural pause and the next bounded chunk of work fits a lower tier, the session dispatches a foreground sub-agent at the appropriate tier rather than continuing to perform that work at the current tier. The parent session retains its context and waits for the sub-agent to complete, then reviews the result and either commits it or queues the next chunk.

This approach preserves session context while routing volume work through lower-cost tiers. The parent pays parent-tier rates only for orchestration — reviewing results, authoring commit messages, making the next structural decision. The sub-agent does the volume work at a lower rate.

Four properties govern how sub-agent dispatch works in practice:

**Bounded brief.** One task, one result, self-contained. The brief includes file paths, names the desired output shape, and caps response length. Open-ended exploration is not a sub-agent task.

**Foreground and serial when writing.** A sub-agent writing to files runs to completion before the next one starts. Parallel dispatch is appropriate for read-only work — research, scanning, triage — but not for write operations that share a file index.

**Confidence gate.** Dispatch only when there is high confidence the sub-agent will produce output matching or exceeding what the current tier would produce on the same bounded task. Mechanical edits, well-specified implementations, read-only research, and scoped refactors against a clear spec pass this gate. Architectural decisions, doctrine drafting, cross-layer coordination, and anything requiring novel framing do not.

**Layer scope preserved.** A sub-agent dispatched from one layer operates within that layer's scope. Cross-layer work travels through the established coordination mechanism rather than through sub-agent dispatch.

## The cost framing

The three-tier structure produces a significant effective multiplier at fixed daily token budgets. Using the same daily token cap, running mechanical work at the mechanical tier instead of the deep-think tier extends the budget by approximately a factor of fifteen. A contributor pool operating at tier discipline can sustain a substantially larger volume of committed output within the same infrastructure cost as a smaller pool operating without tier discipline.

This multiplier is the structural reason why a contributor model that includes a larger pool of paid contributors is operationally viable. Without tier discipline, that model is expensive enough to be impractical. With it, the cost structure works.

## What the discipline is not

Model tier discipline does not refuse work at the current tier. Sessions write a dispatch recommendation or proposal; a human principal decides whether to act on it. The discipline is a cost-optimization recommendation mechanism, not a gate.

It is also not a constant check. Recommendations fire only at substantive work-shape pivots. Constant suggestions create overhead that erodes the cost savings they are intended to produce. The trigger is a genuine pivot, not a micro-pause.

Tier discipline and model version progression are orthogonal axes. A new model version earning a role through a supervised period of demonstrated correctness is a different question from which tier of the current model family to use for a specific bounded task. Both apply simultaneously.

## See also

- [[compounding-substrate]] — the contributor model this discipline makes economically viable
- [[cluster-wiki-draft-pipeline]] — a concrete application of sub-agent dispatch in the editorial pipeline

## Provenance

Authored 2026-05-01 by project-language Task Claude. Source: `conventions/model-tier-discipline.md` (ratified 2026-04-26). Version note: the v0.1.30 amendment replaced the prior exit-and-re-enter recommendation mechanism with in-seat sub-agent dispatch as the preferred path; the earlier mechanism remains available for operator-elective session restarts.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
