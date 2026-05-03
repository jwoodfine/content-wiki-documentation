---
schema: foundry-doc-v1
title: "Service-SLM Operationalization Plan"
slug: service-slm-operationalization-plan
category: reference
type: topic
quality: published
short_description: The strategic and operational plan for transitioning from externally hosted language model calls toward a per-tenant small language model substrate that heals through a compounding feedback loop.
status: pre-build
last_edited: 2026-05-01
editor: pointsav-engineering
cites: []
paired_with: service-slm-operationalization-plan.es.md
---

The service-slm operationalization plan describes the intended path from an initial state — in which external large language model calls handle substantially all AI-assisted work — to a target state in which a per-tenant small language model substrate contributes in parallel with external calls, accumulates a training corpus from its own outputs and corrections, and progressively displaces the higher-cost external tier across task types that the substrate has mastered.

This is a multi-year trajectory, not a single deployment event. The plan is ratified as operational guidance directing cross-cluster work across multiple engineering milestones.

## The target state

The strategic goal is a per-tenant editorial and apprenticeship substrate where every commit becomes training corpus material, per-tenant adapter weights compose with the open base model at inference time, and the substrate sharpens monotonically because two feedback loops both close simultaneously. The first loop captures the structural correctness signal — did the substrate produce output that the editorial gateway accepted — and feeds it into continued training. The second loop captures the craft signal — did a creative contributor edit the published output, and how — and feeds that into a preference training layer on top of the structural layer.

When both loops are operating, each task type the substrate handles with high enough acceptance rate is a candidate for promotion: from requiring senior review on every output, to requiring only spot-checks, to operating autonomously within its task boundary. Each promotion step reduces the per-task cost in external model calls. The per-week external model cost trends toward a floor comprising only the coordination and ratification work that irreducibly requires the highest-capability model.

The structural reason this path is not replicable by multi-tenant general-purpose deployments is that the feedback loops close per-tenant. A creative contributor editing content for one customer's deployment produces preference pairs that train an adapter specific to that customer's voice. Multi-tenant deployments produce feedback that averages across all customers and improves no customer's substrate specifically.

## The three compute tiers

The substrate routes AI-assisted work across three compute tiers based on task shape, latency requirements, and cost budget.

**Tier A — Local.** A smaller open-weight model running on the workspace virtual machine under CPU inference. This is the always-available fallback: no external dependency, no per-call cost, predictable latency. Appropriate for tasks where quality requirements are modest or where the task shape has already been mastered by the substrate through continued training.

**Tier B — Burst.** A larger open-weight model, specifically OLMo 3.1 32B Think, on preemptible GPU compute provisioned on demand. This tier is cost-efficient for workloads that tolerate sixty-to-one-hundred-twenty-second cold-start times, which is acceptable for asynchronous editorial pipelines but not for synchronous interactive workflows. The preemptible pricing model reduces cost by approximately sixty percent compared to on-demand compute for the same hardware.

**Tier C — External API.** External language model providers reached via HTTPS. This tier is reserved for narrow precision tasks — citation grounding, initial knowledge graph construction from a corpus, structured output generation when the local model cannot meet the schema conformance bar, and entity disambiguation in high-ambiguity cases. The Doorman service is the only component that holds external API keys; all Tier C calls route through it and are logged to the per-tenant audit ledger.

The routing decision is made by the Doorman based on request shape and per-tenant budget caps. Callers do not select a tier; they describe what they need, and the Doorman routes accordingly.

## The healing mechanism

The term "healing" describes a property of the feedback loop rather than a corrective process applied to specific errors. When the substrate produces output that the editorial gateway accepts, the acceptance is recorded. When the gateway rejects output, the rejection and the corrected version are also recorded. Both signals feed the training corpus. A task type that starts with a low acceptance rate improves over successive training cycles as the substrate learns from its rejections. The system is self-correcting at the corpus level, not at the individual output level.

This property has a practical implication for quality management: a somewhat lower per-output quality from a less capable model today is acceptable if the rejection signal feeds a training corpus that produces a better model tomorrow. The cost of imperfect output at acceptable rates is the training investment; the return is a substrate that requires progressively less correction.

## LoRA training framework

Adapter training uses the Axolotl framework, which supports the OLMo 3.1 32B Think model via the standard Hugging Face `AutoModel` interface. A per-tenant adapter trains with low-rank adaptation at rank 16, using the full-precision training path on an A100 GPU with 80 gigabytes of memory. The Axolotl configuration is parameterised by tenant-specific corpus path and output adapter path, so the same training driver handles all tenants by providing different input and output paths.

The intended training cadence is quarterly, timed to when each tenant's corpus has accumulated sufficient volume to produce a meaningful signal. An initial training run costs approximately ten to twenty USD in GPU compute at the planned instance class and window length.

## Corpus deployment

Per-tenant training data lives in deployment instances rather than at workspace tier. This keeps tenant data structurally separated: one deployment instance holds the PointSav tenant's corpus, adapter weights, and audit ledger; a second instance holds the same for the Woodfine tenant. The catalog entry in the fleet-deployment repository describes what a training-pipeline instance is for; the numbered instance carries the actual per-tenant state.

## See also

- [[reverse-funnel-editorial-pattern]] — The editorial pipeline that generates the craft preference pairs consumed by Stage-2 training.
- [[tier-c-key-wiring]] — The operational form of Tier C external API key management.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
