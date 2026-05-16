---
schema: foundry-doc-v1
title: "Doorman Protocol"
slug: doorman-protocol
category: architecture
status: stub
bcsc_class: current-fact
last_edited: 2026-04-28
editor: pointsav-engineering
cites:
 - doctrine-claim-1
---

`service-slm` is the platform's sole AI request boundary — every inference call routes through a single access-control gateway (the Doorman) — which enforces sanitise-and-rehydrate discipline, routes to the appropriate compute tier, logs every event to an immutable audit ledger, and accumulates the training signal that compounds the platform over time. No inference call exits the customer data vault without passing through this single boundary. The Doorman Protocol defines the routing rules, audit schema, and training-signal capture that make this boundary work as a structural guarantee, not a configuration option.

## Why a Doorman

The boundary problem: a customer data vault holds the customer's authoritative structured data; external compute (large language models) cannot be trusted with raw structured facts. Without a single boundary, every service in the Totebox grows its own egress path, every egress path needs its own audit, and the sanitise-and-rehydrate discipline ([[architecture-decisions|SYS-ADR-07]]) becomes per-service discipline rather than substrate discipline. The Doorman centralises the boundary so the discipline is enforced once.

## Three-tier compute routing

The Doorman routes inference calls across three compute tiers:

**Tier A — Local.** Executes on the host VM using CPU and RAM. For fast, low-latency, low-cost inference on a locally hosted model (`OLMo-2-0425-1B-Instruct` in the reference deployment). Tier A handles the majority of routing volume; no cloud spend.

**Tier B — On-demand GPU pool (planned).** Routes workloads to dedicated GPU instances (the Yo-Yo pool — ephemeral inference nodes) on Google Cloud Platform, spun up on demand and shut down on idle. Two instance profiles are planned: a trainer instance for continued SFT and LoRA training cycles on accumulated engineering tuples, and an extractor instance for large-scale corpus ingestion requiring frontier-scale reasoning. Both profiles use idle-shutdown timers so billing stops when the queue is empty. Tier B routing is planned; Tier A is operationally verified (commit `cf4f6ee`, 2026-04-26).

**Tier C — External API proxy.** Routes specialised linguistic refinement and formatting tasks to external frontier models. The Doorman enforces cost guardrails and injects predefined service-content ontologies to constrain output to canonical platform vocabulary. Tier C routing is planned.

## The audit ledger

Every inference call produces a JSONL audit-ledger entry appended to a daily file. Required fields: timestamp, request ID, module ID, tier, model, inference duration (ms), cost estimate (USD), sanitised-outbound flag, and completion status. The ledger is append-only; no entry is modified or deleted after write.

## The moduleId discipline

A single `moduleId` field serves five roles in one: it selects the systemd unit that handles the request; namespaces KV cache blocks; scopes the property graph database (LadybugDB) traversals to the correct tenant; selects the LoRA adapter stack; and tags audit-ledger entries for per-project cost accounting. A request without a valid `moduleId` is rejected at the Doorman boundary.

## Learning pipeline routing

The Doorman implements the [[apprenticeship-substrate]] (the learning pipeline) polarity flip for code-shaped and editorial work: `service-slm` attempts first; the senior session reviews. Every signed verdict (`Accept` / `Refine` / `Reject` / `DeferTierC`) is captured to the apprenticeship corpus as a training tuple. The Doorman's routing logic and the Apprenticeship Substrate's promotion ledger are two surfaces of the same mechanism.

## See also

- [[compounding-doorman]] — conceptual overview of the Doorman as a sovereign AI substrate pattern
- [[apprenticeship-substrate]] — the routing inversion and verdict-signing protocol that compounds the substrate
- [[three-ring-architecture]] — Ring 3 framing; the Doorman is the sole Ring 3 service
- [[service-slm]] — implementation detail of the service-slm crate
