---
schema: foundry-doc-v1
title: "The Trajectory Substrate"
slug: trajectory-substrate
category: architecture
type: topic
quality: complete
short_description: "The Trajectory Substrate is the Foundry mechanism that converts operational work — commits, sessions, operator feedback — into structured JSONL training tuples, routing them into a continued-pretraining corpus that improves the OLMo base model over time."
status: pre-build
last_edited: 2026-04-30
editor: pointsav-engineering
cites:
  - ni-51-102
  - osc-sn-51-721
  - constitutional-ai-2212-08073
  - federated-lora-2502-05087
  - s-lora-2024
  - lorax-predibase
  - olmo3-allenai
paired_with: trajectory-substrate.es.md
---

# The Trajectory Substrate

> The Trajectory Substrate is the Foundry mechanism that converts operational work — commits, sessions, operator feedback — into structured JSONL training tuples, routing them into a continued-pretraining corpus that improves the OLMo base model over time.

Every commit Foundry makes, every session a Task Claude runs, every time an operator marks a suggestion as wrong — these interactions are not discarded. They are captured as structured JSONL tuples, tagged with provenance metadata, and routed into a training corpus whose accumulated signal shapes the OLMo base model each time a continued-pretraining run closes. The substrate trains itself on the work it performs. That loop — operational interaction to training signal to improved model to better operational output — is **The Trajectory Substrate**.

## Overview

The Trajectory Substrate is the Foundry mechanism that converts operational work into continued-pretraining signal without interrupting that work. It operates in the background of every commit, every session, and every operator feedback exchange.

Three properties distinguish a trajectory substrate from a generic fine-tuning pipeline:

1. **Capture is automatic.** No operator decision is required to generate a training tuple. The `git post-commit` hook fires; the session-end script fires; the rejected-suggestion script fires. Work produces signal by existing.
2. **Provenance is structural.** Every JSONL record carries the doctrine version it was produced under, the tenant it belongs to, the role of the session, the cluster, and its redaction class. The training pipeline does not trust prose; it filters on these fields.
3. **Corpus boundaries are enforced by infrastructure.** Vendor data never co-mingles with Customer data at training time. Tenant data never crosses tenants. The separation is directory-level and pipeline-level — not policy-level.

## Ring and Role

The Trajectory Substrate does not map to a single ring. Capture happens at every layer — Ring 1 runtime events, Ring 2 processing events, Ring 3 inference interactions, and workspace-level commit hooks. The substrate is the infrastructure that runs beneath all three rings, converting their operational outputs into training material. `service-slm` (Ring 3) is the primary consumer of the resulting adapters at inference time.

## Architecture

### Three corpora, three adapter families

The convention behind this article (`~/Foundry/conventions/trajectory-substrate.md`) defines three orthogonal corpus types. Each produces a different adapter class. Mixing them is the failure mode.

**Constitutional corpus**

Captures doctrine clauses crossed with role and scope: what the Foundry constitutional charter says a Master / Root / Task session may and may not do. Lives at `~/Foundry/data/training-corpus/doctrine/<doctrine-version>/`. Produces the constitutional adapter (`constitutional-doctrine-vM.m.p.lora`). Retrains on every Doctrine MINOR version bump. Universal — loaded by every Foundry deployment, regardless of tenant.

The doctrinal basis is `[constitutional-ai-2212-08073]`: a model whose behaviour is governed by a written charter, not only by aggregate preference signal.

**Engineering corpus (Vendor side)**

Captures Master, Root, and Task session trajectories on Vendor repos: commit diffs, session logs, and Doctrine amendments in flight. Lives at `~/Foundry/data/training-corpus/engineering/`. Tenant scope: PointSav only. Produces the engineering adapter (`engineering-pointsav-vN.lora`), which PointSav may offer as a "platform-builder personality" to Customers via service contract.

**Tenant-runtime corpus (per Customer)**

Captures what flows through Ring 1 inside each Customer deployment: `service-fs`, `service-people`, `service-email`, `service-input` events; curated graph deltas from `service-content`; operator usage trajectories. Lives inside the Customer deployment instance at `<deployment-instance>/training-corpus/<tenant>/`. Never in the Vendor workspace. Produces the tenant adapter (`tenant-<tenant>-vK.lora`) inside and held by the Customer deployment.

Tenant adapters do not leave the customer's deployment unless that customer explicitly opts into the federated marketplace (Doctrine claim #14, a forward-looking feature). This is structural privacy by infrastructure.

### Capture mechanics

Five scripts in `~/Foundry/bin/` handle capture:

| Script | Trigger | Writes |
|---|---|---|
| `capture-edit.py` | `git post-commit` hook on `cluster/*` branches and workspace `main` | `engineering/<cluster>/<sha>.jsonl` |
| `capture-trajectory.sh` | Session end via `bin/claude-role.sh` | `engineering/sessions/<id>.jsonl` |
| `capture-doctrine.sh` | Per Doctrine MINOR bump | `doctrine/<version>/<tuple>.jsonl` |
| `capture-feedback.sh` | Inbox-archive of rejected or redo messages | `engineering/feedback/<record>.jsonl` |
| `capture-tenant-runtime.sh` | Scheduled inside deployment instance | `<instance>/training-corpus/<tenant>/<shard>.jsonl` |

Sanitize-outbound discipline applies at every capture point: private keys, PII, and customer-identifying details are redacted before write. Redaction runs at the capture script, not at the downstream consumer. Diff output is truncated at 1,000 lines.

Every JSONL record carries a provenance header with fields `tuple_type`, `doctrine_version`, `tenant`, `moduleId`, `cluster`, `role`, `scope`, `redaction_class`, `evidence_class`, `source_commit`, `session_id`, and `created`. The training pipeline filters on `(tenant, redaction_class, evidence_class)` to assemble each corpus. Any adapter version is re-derivable from its source records; any record can answer which adapter versions it trained.

### Adapter composition at request time

At inference time the Doorman (`service-slm`) composes adapters per request:

```
composed_weights =
    base_model[OLMo-3-1125-7B-Q4]
    ⊕ constitutional[doctrine_v0.0.x]   ← always
    ⊕ engineering[pointsav_vN]?          ← if request is platform-build context
    ⊕ tenant[<tenant>_vK]?               ← if request is tenant-data context
    ⊕ role[<role>]                        ← what role is asking
    ⊕ cluster[<cluster>_vJ]?             ← if cluster scope applies
```

Multi-LoRA serving infrastructure — `[s-lora-2024]`, `[lorax-predibase]` — serves thousands of concurrent adapters with hot-swap per request. The composition algebra is specified at `conventions/adapter-composition.md`.

Each cluster manifest declares `adapter_routing.trains:` (which adapters this cluster's commits and sessions feed) and `adapter_routing.consumes:` (which adapters the Doorman composes when this cluster's sessions query the SLM). Every cluster defaults to training the engineering-pointsav adapter — the substrate is always improving from every cluster's work.

### Negative-trajectory distillation

When an operator rejects a suggestion, asks for a revision, or marks a result as wrong, that exchange is a training signal of the highest quality. The `capture-feedback.sh` script records the triple:

```
(rejected_trajectory, corrected_trajectory, doctrine_violation_tag)
```

These pairs feed Direct Preference Optimisation (DPO) training, per the RLAIF literature lineage `[constitutional-ai-2212-08073]`. The adapter family learns, per cluster and per role, which outputs to avoid and which corrections to prefer.

This per-contributor inverse of aggregate preference learning is structurally inaccessible to platforms whose preference signal is averaged across all users. An operator's specific correction pattern shapes their own cluster's adapter — no other tenant benefits or is burdened by it.

## Configuration

The Trajectory Substrate currently operates at L1 (edit-corpus capture, live since v0.1.1). Per `[ni-51-102]` continuous-disclosure language, and in accordance with the forward-looking information principles of `[osc-sn-51-721]`, the statements below describe planned and intended development. Material assumptions: continued-pretraining technology matures on the current trajectory; OLMo 3 base model `[olmo3-allenai]` remains openly licensed; engineering corpus accumulates at the current Foundry development cadence. Actual outcomes may differ.

Planned subsequent tiers:

- **L2 — Trajectory capture** (`bin/capture-trajectory.sh` + sanitize-outbound): intended for the v0.2.x release window; adds full session-log tuples to the corpus.
- **L3 — Fine-tuning prototype**: intended for the v0.5.0 target; the `router-trainer` service reads the accumulated corpus and produces the first trained adapter against the OLMo 3 base.
- **L4 — Federated marketplace**: long-horizon; depends on L3 operational maturity and the federated-LoRA research lineage `[federated-lora-2502-05087]` proving out in production at scale.

The quarterly pretraining cadence is intended once L3 is operational. Substrate baselines are designed to improve monotonically as the corpus accumulates; the mechanism is in place and the signal is accumulating.

## See Also

- [[compounding-substrate]]
- [[apprenticeship-substrate]]
- [[decode-time-constraints]]
- [[language-protocol-substrate]]
- [[citation-substrate]]

## References

- `~/Foundry/conventions/trajectory-substrate.md` — the convention this article reflects
- `pointsav-monorepo/service-disclosure/CORPUS-SCHEMA.md` — the corpus schema
- `~/Foundry/bin/install-capture-hook.sh` — the capture hook installer
- `[constitutional-ai-2212-08073]` — Constitutional AI: Harmlessness from AI Feedback (Bai et al., 2022)
- `[federated-lora-2502-05087]` — Federated LoRA research lineage
- `[s-lora-2024]` — S-LoRA: Serving Thousands of Concurrent LoRA Adapters
- `[lorax-predibase]` — LoRAX multi-LoRA serving
- `[olmo3-allenai]` — OLMo 3 base model (Allen Institute for AI)
- `[ni-51-102]` — NI 51-102 Continuous Disclosure Obligations
- `[osc-sn-51-721]` — OSC Staff Notice 51-721 Forward-Looking Information Disclosure
