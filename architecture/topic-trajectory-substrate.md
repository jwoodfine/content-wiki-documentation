---
schema: foundry-doc-v1
title: "The Trajectory Substrate"
slug: topic-trajectory-substrate
category: architecture
type: topic
quality: published
short_description: "The mechanism by which the PointSav platform captures its own production work as training material: three orthogonal corpus types, a versioned adapter library, and a composition algebra that allow the substrate to improve itself from real operational activity without mixing vendor data, customer data, or cross-tenant records."
status: pre-build
last_edited: 2026-05-01
editor: pointsav-engineering
cites: []
paired_with: topic-trajectory-substrate.es.md
---

Foundry captures the work it does as training material. Over time, the substrate shapes the substrate.

This is the Trajectory Substrate: a set of capture mechanics, corpus types, adapter types, and separation rules that allow the platform to improve its AI substrate from real production activity. The improvement happens without mixing vendor and customer data, without crossing tenant boundaries, and without requiring a separate annotation or data-labelling effort. The work itself is the training material.

## Three orthogonal corpora

The corpus is not a single file. It is three separate types, each producing a different adapter class, each living in a different location, and each enforcing different tenant-isolation rules. Mixing them is the failure mode.

**The constitutional corpus** captures the relationship between doctrine clauses, roles, and operational scope. Its scope is universal — it applies to every deployment. The adapter it produces is the constitutional adapter, loaded by the Doorman on every request regardless of other context.

**The engineering corpus** captures the platform builder's session trajectories, code commits, and doctrine amendments. Its scope is the vendor. The adapter it produces — the engineering adapter — reflects the accumulated judgment of the platform's development work. It is offered to customers as the "platform-builder personality" under the SMB Customer service tier, but the training records behind it are vendor-only.

**The tenant-runtime corpus** captures what actually flows through a customer's Ring 1 services: the records that arrive, the graph deltas that the knowledge pipeline produces, the usage patterns the operator establishes. Its scope is strictly per-customer. It lives inside the customer's ToteboxOS instance. The vendor workspace never receives tenant-runtime records unless the customer has explicitly opted into the federated marketplace. The adapter it produces lives on the customer's instance, not at the vendor.

The three corpora never cross at training time. This is structural privacy by infrastructure — the separation is enforced by where files are written, not by policy documents or contractual terms.

## Capture mechanics

Four capture operations run in the background during normal platform use.

Edit capture fires after every commit on active development branches. It records the diff, the session context, the cluster scope, and a redacted version of the changed content. The redaction pass strips private keys, authentication tokens, and identifying strings before the record is written — redaction happens at capture, not at consumption.

Session trajectory capture fires at the end of a working session. It records what the session was attempting, the sequence of actions taken, and the outcome. This is the session-level complement to edit capture: where edit capture records individual changes, trajectory capture records the arc of a session.

Doctrine capture fires on doctrine version bumps. It records the clause-by-clause changes to the platform's constitutional document as a set of structured training tuples that can be used to retrain the constitutional adapter when the doctrine advances.

Feedback capture fires when an operator rejects a result, requests a revision, or marks output as incorrect. It records the triple of the rejected output, the corrected output, and a tag identifying what doctrine rule the rejection corresponds to. These triples are the input to direct preference optimisation training on the engineering adapter.

## The adapter library

Training the captured corpora produces a library of LoRA adapters — lightweight weight modifications that shift a base model's behaviour in a specific direction. The adapters are versioned and signed; each version record embeds the doctrine version it was trained against, so an adapter trained on an earlier doctrine does not silently apply to requests under a newer doctrine.

The adapter composition at request time follows a fixed algebra: the base model plus a constitutional adapter (always loaded), plus an engineering adapter for platform-building work, plus a tenant adapter for customer-voice work, plus a role adapter matching the operational role of the requesting session, plus a cluster adapter for the specific project cluster in use. The maximum composition depth at any given request is bounded; the Doorman selects which adapters to compose based on the request's context.

## Per-cluster training and consumption

Each active development cluster declares which adapters its work feeds (the training side) and which adapters the Doorman composes when that cluster queries the model (the consumption side). A cluster doing platform engineering feeds the engineering adapter and consumes the engineering adapter. A cluster producing customer-voice content adds the tenant adapter on both sides. These declarations sit in each cluster's manifest and are read by both the capture pipeline (to tag records correctly) and the Doorman (to assemble the request-time composition).

The default rule is that every cluster always feeds the engineering adapter — every commit on any active cluster contributes to the platform-wide engineering corpus — and always consumes the constitutional and engineering adapters. Tenant-specific adapters are additive when the work scope calls for them.

## Negative trajectory distillation

When an operator rejects a result, the rejection is not just discarded. The capture-feedback script records the triple: the rejected output, the corrected output, and the doctrine violation tag that explains the rejection. These triples feed DPO training on the appropriate adapter. The model learns what not to do at per-cluster, per-role, per-contributor granularity — the inverse of the aggregate preference averaging that is the only option on platforms where all users' feedback is pooled.

## Provenance and re-derivability

Every corpus record carries a structured provenance header: tuple type, doctrine version at time of capture, tenant identifier, cluster identifier, role, scope, redaction class, evidence class, source commit, and session identifier. The combination makes every adapter version re-derivable from its source records. Any source record can answer the question: which adapter versions was this record used in training?

Evidence classes carry different lifecycles. Primary evidence — original observations — is immutable once captured. Derived evidence — versioned reasoning built on primary records — is supersedable, with the supersession tracked. Cited evidence — references to external authority — is verified against the source on a regular schedule.

## Implementation state

The first capture tier — edit corpus capture via a post-commit hook — is operational on all active development clusters. Every commit on a registered branch produces a structured JSONL record in the engineering corpus. Session trajectory capture and doctrine-grounded adapter training are in development; the adapter library and full training pipeline are planned for later platform milestones.

## See Also

- [[topic-apprenticeship-substrate]] — the fourth corpus type (apprenticeship) that the Trajectory Substrate works alongside
- [[compounding-doorman]] — the Doorman that reads the adapter library and applies the composition algebra at request time
- [[topic-llm-substrate-decision]] — the OLMo 3 base model that all adapters modify
- [[topic-four-tier-slm-substrate]] — the tier model that determines which compute handles requests at each stage of adapter progression

## References

1. Constitutional AI paper, arXiv 2212.08073 — foundational DPO and preference training work.
2. Federated LoRA paper, arXiv 2502.05087 — federated adapter exchange mechanics.
3. S-LoRA, 2024 — concurrent adapter serving infrastructure.
4. LoRAX (Predibase) — multi-LoRA serving.
5. `conventions/trajectory-substrate.md` — source convention for this article.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
