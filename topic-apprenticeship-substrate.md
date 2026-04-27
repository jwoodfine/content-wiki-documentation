---
title: "The Apprenticeship Substrate"
slug: topic-apprenticeship-substrate
category: architecture
status: pre-build
last_edited: 2026-04-27
editor: pointsav-engineering
cites:
  - ni-51-102
---

# The Apprenticeship Substrate

The Doorman flips polarity. The local SLM (`service-slm`) becomes
the **first responder** on code-shaped and editorial work; the
human operator with their senior reviewer assistant becomes the
**senior reviewer**. The disagreement between them — captured as
signed, append-only training tuples — is the highest-quality
continued-pretraining signal Foundry can produce.

This article describes the routing protocol, the brief / attempt
/ verdict format, the promotion ledger, and what makes this
posture structurally inaccessible to hyperscaler-managed AI.

## Why this exists

Captured observation trains a model on what the senior wrote.
Captured **interaction** — apprentice attempt plus signed senior
verdict — trains an order of magnitude more efficiently per
tuple. This is the core finding of the RLHF / DPO / RLAIF
literature 2024-2026: signed preference data is the most
valuable training input.

The Apprenticeship Substrate is the routing inversion that
produces those interaction tuples on real production work, not
synthetic benchmarks. Every Foundry session exercises the
apprentice; every signed verdict is a training tuple; every
graduated task-type eliminates Claude tokens monotonically.

Four preconditions make this work, and all four hold only inside
Foundry-shaped substrates:

1. Per-customer constitutional charter (the Doctrine).
2. Per-customer signing identities (`allowed_signers`).
3. Per-customer task-type granularity (the promotion ledger).
4. Per-customer continued pretraining.

Hyperscalers structurally lack all four.

## The three stages

Routing operates per task-type. Promotion is automatic on
threshold crossing; demotion is automatic on any post-commit
revert traced to an apprentice diff.

| Stage | Routing | Senior review |
|---|---|---|
| `review` | Apprentice attempts; senior reviews every diff before commit | Every diff |
| `spot-check` | Apprentice commits; senior reviews 1-in-N sampled + auto-flagged anomalies | Sampled + flagged |
| `autonomous` | Apprentice commits autonomously; monthly batch audit | Batch audit |

Initial promotion thresholds:

- `review → spot-check`: at least 50 verdicts AND accept-rate at
  least 0.85 over the rolling 50.
- `spot-check → autonomous`: at least 100 verdicts AND
  accept-rate at least 0.95 over the rolling 100 AND zero
  post-commit reverts traced to apprentice diffs.

Demotion: a single revert traced to an apprentice diff drops the
task-type one stage. Recorded as a signed event in the ledger.
New task-types start at `review`.

## The brief, the attempt, the verdict

A senior who would author a diff issues a **brief** instead. The
brief states what is being done, the invariants the diff must
preserve, the doctrine clauses cited, and the acceptance test the
apprentice should make pass.

The apprentice responds with an **attempt**: chain-of-thought
reasoning citing the brief invariants, a self-confidence value
calibrated against its prior ledger record on this task-type,
and a unified diff. If self-confidence falls below 0.5, the
apprentice escalates without diff — surfacing "this task-type is
harder than I can handle today" rather than producing a low-
confidence diff that wastes senior review.

The senior reads the attempt and signs a **verdict**: `accept`,
`refine`, `reject`, or `defer-tier-c`. Verdicts on `refine` and
`reject` carry one-sentence notes — these are the highest-signal
training data the corpus produces. The signature uses
`ssh-keygen -Y sign` with a namespace tag (`apprenticeship-
verdict-v1`) that binds the signature to this protocol; a
commit-signing signature cannot be repurposed as a verdict
signature.

## The promotion ledger

A single plain-text file tracks every task-type's stage and the
event log that drives promotion / demotion. Every event line
carries an embedded SSH signature block; the writer (the Doorman)
appends only after verifying the senior's signature on the
verdict batch. Single-writer concurrency via `flock(2)`;
acceptable latency at the expected verdict rate of tens per day.

Event types: `task-type-add`, `verdict-batch`, `promotion`,
`demotion`, `verdict-supersession`, `task-type-retire`. The
schema is closed; new event types require ledger discipline
because promotion threshold computations depend on them.

## Production routing vs shadow routing

Two paths run in parallel.

**Production routing** runs on graduated task-types. The senior
issues a brief before authoring the diff themselves; the
apprentice's attempt is the candidate diff; on `accept`, the
apprentice's diff lands in the commit. This eliminates senior
authoring tokens on graduated task-types.

**Shadow routing** runs on every other code-shaped commit across
every active cluster. After the diff is authored the existing
way, the session fires a brief to the apprentice; the apprentice
produces what it would have done; the (brief, attempt, actual-
diff) triple is captured to the corpus as a training tuple. No
verdict; no signing. The apprentice is exercised continuously;
the corpus grows on every cluster's work.

Production routing eliminates senior tokens on graduated types.
Shadow routing generates the training data that graduates the
next type. The two paths compound.

## Capture pipeline

The apprenticeship corpus is a fourth corpus alongside the
constitutional, engineering, and tenant-runtime corpora.
Per-tenant partitioning lives at the directory level:

```
~/Foundry/data/training-corpus/apprenticeship/<task-type>/<tenant>/<ulid>.jsonl
```

One file per (brief, attempt, verdict) triple. Tenant-private
records never leave the tenant's substrate per Doctrine §IV.b.

A `refine` or `reject` verdict additionally produces a Direct
Preference Optimisation triple: (rejected attempt, corrected
diff, doctrine-violation tag). DPO triples feed adapter training
on the apprentice's policy.

## Forward-looking — graduation eliminates tokens

Per `[ni-51-102]` continuous-disclosure language, the trajectory
toward token-elimination across graduated task-types is forward-
looking. The shape is in place; the operational throughput
matures as the corpus grows and task-types graduate.

The first registered task-type is narrow and high-volume:
`version-bump-manifest`. Every workspace MINOR / PATCH bump
touches `MANIFEST.md` and `CHANGELOG.md`. Well-shaped, no
architectural judgment required, easily verifiable. The
apprentice graduates this type first; senior tokens drop on this
class of work; the next task-type registers.

The end state is a continuum — code-shaped work the apprentice
handles autonomously, code-shaped work the apprentice handles
with spot-check, code-shaped work that still requires senior
review. The continuum shifts left as the corpus matures.

## See also

- [The Compounding Substrate](topic-compounding-substrate.md)
- [The Three-Tier Contributor Model](topic-contributor-model.md)
- [The Language-Protocol Substrate](topic-language-protocol-substrate.md)
- [Customer Hostability](topic-customer-hostability.md)
- The convention this article reflects:
  `~/Foundry/conventions/apprenticeship-substrate.md`
- The corpus schema:
  `pointsav-monorepo/service-disclosure/CORPUS-SCHEMA.md`
