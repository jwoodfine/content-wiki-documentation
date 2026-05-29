---
schema: foundry-doc-v1
title: "The apprenticeship substrate"
slug: apprenticeship-substrate
category: substrate
type: topic
quality: complete
short_description: "The platform mechanism that routes code-shaped and editorial work first through a local Small Language Model, captures a signed senior verdict on every attempt, and uses the resulting preference pairs as continued-pretraining signal — compounding toward task types that need no senior authoring."
status: active
bcsc_class: public-disclosure-safe
forward_looking: true
last_edited: 2026-05-22
editor: pointsav-engineering
cites:
 - ni-51-102
paired_with: apprenticeship-substrate.es.md
---

When a senior engineer reviews a junior's work, the correction is the most valuable artifact in the room — and almost every organization discards it. The reasoning behind a fix is spoken once, applied once, and never captured. The next junior, and the next model, start from zero.

The apprenticeship substrate captures it. <!--claim id=route-and-capture confidence=structural cites=[]-->Every code-shaped and editorial task is routed first through a local [[service-slm|Small Language Model]]; a senior reviewer then signs a verdict on the attempt. The signed disagreement between apprentice attempt and senior verdict becomes preference-pair training data.<!--/claim-->

<!--claim id=three-stage-routing confidence=structural cites=[]-->Routing runs in three stages per task type — `review`, `spot-check`, and `autonomous` — with quantified promotion thresholds. A graduated task type eliminates senior-author tokens on that class of work, and shadow routing harvests training data from every other code-shaped commit across the fleet.<!--/claim-->

For a regulated buyer the consequence is concrete. The AI improves on the organization's own work, and that work never leaves the deployment. Per `[ni-51-102]` [[disclosure-substrate|continuous-disclosure]] language, the trajectory toward token elimination across graduated task types is forward-looking; the routing structure is operational today.

## Overview

Captured observation trains a model on what the senior wrote. Captured interaction — an apprentice attempt plus a signed senior verdict — trains an order of magnitude more efficiently per tuple. Signed preference data is the most valuable training input, a finding established across the 2024–2026 reinforcement-learning-from-feedback literature.

This routing pattern produces those interaction tuples on real production work, not synthetic benchmarks. Every session exercises the apprentice; every signed verdict is a training tuple; every graduated task type eliminates external AI tokens monotonically.

## Ring and role

The apprenticeship substrate spans Ring 3 — Optional Intelligence — and the training-corpus infrastructure. [[service-slm]], the [[compounding-doorman|Doorman]], is the Ring 3 service that executes apprentice routing. The promotion ledger and the corpus-capture scripts live inside the customer's own deployment. The substrate is active whenever a session issues a brief rather than authoring directly.

## The three stages

Routing operates per task type. Promotion is automatic on a threshold crossing; demotion is automatic on any post-commit revert traced to an apprentice diff.

| Stage | Routing | Senior review |
|---|---|---|
| `review` | Apprentice attempts; senior reviews every diff before commit | Every diff |
| `spot-check` | Apprentice commits; senior reviews a 1-in-N sample and auto-flagged anomalies | Sampled and flagged |
| `autonomous` | Apprentice commits autonomously; monthly batch audit | Batch audit |

<!--claim id=promotion-thresholds confidence=structural cites=[]-->Promotion from `review` to `spot-check` requires at least 50 verdicts at a 0.85 acceptance rate over the rolling 50. Promotion to `autonomous` requires at least 100 verdicts at a 0.95 acceptance rate over the rolling 100, with zero post-commit reverts traced to apprentice diffs.<!--/claim--> A single revert traced to an apprentice diff drops the task type one stage, recorded as a signed ledger event. New task types start at `review`.

## The brief, the attempt, the verdict

A senior who would author a diff issues a **brief** instead. The brief states what is being done, the invariants the diff must preserve, the constraints cited, and the acceptance test the apprentice must make pass.

The apprentice responds with an **attempt**: reasoning that cites the brief's invariants, a self-confidence value calibrated against its prior ledger record on this task type, and a unified diff. If self-confidence falls below 0.5, the apprentice escalates without a diff — surfacing that the task type is harder than it can handle today, rather than wasting senior review on a low-confidence diff.

The senior reads the attempt and signs a **verdict**: `accept`, `refine`, `reject`, or `defer-tier-c`. <!--claim id=verdict-signature confidence=structural cites=[]-->Verdicts of `refine` and `reject` carry a one-sentence note — the highest-signal training data the corpus produces. The signature uses `ssh-keygen -Y sign` with a namespace tag that binds it to this protocol, so a commit-signing signature cannot be repurposed as a verdict.<!--/claim-->

## The promotion ledger

A single plain-text file tracks every task type's stage and the event log that drives promotion and demotion. Every event line carries an embedded SSH signature block; the writer — the Doorman — appends only after verifying the senior's signature on the verdict batch. Single-writer concurrency is held by `flock(2)`, with acceptable latency at the expected rate of tens of verdicts per day.

The event schema is closed — `task-type-add`, `verdict-batch`, `promotion`, `demotion`, `verdict-supersession`, `task-type-retire` — because the promotion-threshold computations depend on it.

## Production routing and shadow routing

Two paths run in parallel.

<!--claim id=production-routing confidence=structural cites=[]-->Production routing runs on graduated task types: the senior issues a brief before authoring a diff, the apprentice's attempt is the candidate diff, and on `accept` that diff lands in the commit. This eliminates senior authoring tokens on graduated task types.<!--/claim-->

<!--claim id=shadow-routing confidence=structural cites=[]-->Shadow routing runs on every other code-shaped commit across every active cluster. After the diff is authored the usual way, the session fires a brief to the apprentice; the (brief, attempt, actual-diff) triple is captured to the corpus with no verdict and no signing.<!--/claim-->

Production routing eliminates senior tokens on graduated types. Shadow routing generates the training data that graduates the next type. The two paths compound.

## Capture pipeline

The apprenticeship corpus is a fourth corpus alongside the constitutional, engineering, and tenant-runtime corpora. Per-tenant partitioning lives at the directory level (see [[totebox-archive|Totebox]] storage layout):

```
data/training-corpus/apprenticeship/<task-type>/<tenant>/<ulid>.jsonl
```

One file holds one (brief, attempt, verdict) triple. <!--claim id=tenant-private-corpus confidence=structural cites=[]-->Tenant-private records never leave the tenant's infrastructure.<!--/claim--> A `refine` or `reject` verdict additionally produces a Direct Preference Optimisation triple — rejected attempt, corrected diff, constraint-violation tag — which feeds adapter training on the apprentice's policy.

## Configuration

The first registered task type is `version-bump-manifest`. Every platform MINOR and PATCH bump touches `MANIFEST.md` and `CHANGELOG.md`: well-shaped work, no architectural judgment, easily verifiable. The apprentice graduates this type first; senior tokens drop on this class of work; the next task type registers.

<!--claim id=four-conditions confidence=structural cites=[]-->Four conditions make the substrate work, and all four are structural properties of a [[customer-hostability|customer-owned deployment]]: a per-customer governance charter, per-customer signing identities, per-customer task-type granularity in the promotion ledger, and per-customer continued pretraining.<!--/claim--> A cloud-managed AI platform lacks all four — training on customer interaction data requires pooling it, which eliminates the per-customer isolation guarantee.

The end state is a continuum: code-shaped work the apprentice handles autonomously, work it handles under spot-check, and work that still requires senior review. The continuum shifts as the corpus matures. Per `[ni-51-102]`, the trajectory toward token elimination is forward-looking; the [[adapter-composition|routing shape]] is in place today.

## See also

- [[compounding-substrate]]
- [[contributor-model]]
- [[language-protocol-substrate]]
- [[trajectory-substrate]]
- [[customer-hostability]]
