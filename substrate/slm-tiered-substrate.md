---
schema: foundry-doc-v1
title: "The tiered SLM substrate — local-first AI routing"
slug: slm-tiered-substrate
short_description: "How the platform routes language-model requests across three tiers of compute — local CPU, burst GPU, and external API — keeping routine work on customer-controlled hardware and structured records inside the operator boundary."
category: substrate
type: topic
status: active
bcsc_class: no-disclosure-implication
last_edited: 2026-06-01
editor: pointsav-engineering
paired_with: slm-tiered-substrate.es.md
---

# The tiered SLM substrate — local-first AI routing

The platform routes language-model work through a single gateway that decides, per request, which tier of compute should answer. The design goal is to keep routine work on hardware the operator already owns, reach for rented GPU only when a task genuinely needs it, and never let structured business data cross the AI boundary. This article describes the tiers, how a request is routed, and how the gateway constrains model output to a required shape.

## The tiers

The substrate distinguishes three tiers of inference, each suited to a different class of work.

*Tier A — the local model.* A small model (currently OLMo 2 7B, 4-bit quantised) runs on the operator's own machine and answers immediately for interactive work: code navigation, short drafting, quick questions. It is always available and costs nothing per request. It is the *student* of the learning loop, not the generator of training data — a distinction that matters because a small model asked to critique its own work produces little useful signal.

*Tier B — the burst GPU model.* A larger reasoning model (OLMo 3 32B-Think) runs on a preemptible cloud GPU that is started on demand and stopped when idle. It handles the heavy, structured work — entity extraction for the knowledge graph, and the training-data generation that improves Tier A. Because the GPU is rented by the minute, the gateway brings it up only when there is batch work to do and a dead-man's switch stops it automatically.

*Tier C — the external API.* A commercial model, deliberately left unconfigured. It exists in the design as a resilience option but is not enabled, because the substrate's value is that work stays on customer-controlled compute.

## How a request is routed

Every request carries a complexity hint and an optional tier preference. The gateway's default posture is *local-first*: a confident local primary answers unless the caller explicitly asks for the burst tier and that tier's health check is currently passing. A circuit breaker tracks the burst tier's availability — when the GPU is down, the breaker opens and dependent work *defers* rather than failing, so a capacity stockout or a stopped VM never produces an error, only a "try again later" that the caller retries with backoff.

One routing rule is absolute: entity extraction goes only to the burst tier. The small local model cannot reliably produce structured JSON arrays, so it is never used as a fallback for extraction. When the GPU is unavailable, extraction simply waits.

## The structured-data boundary

A hard architectural rule ([[architecture-decisions|SYS-ADR-07]]) governs what may cross the AI boundary: prose may go out as a prompt; structured business records may not. Entity extraction illustrates the discipline. The text to be analysed is prose. The *schema* that describes the desired output is sent as a constraint, not as data. The model returns a structured array that the gateway parses and writes to the graph — but no existing structured record was ever exposed to the model. The boundary is one-directional by design.

## Constraining output to a required shape

For extraction to be usable, the model's output must match a known JSON shape exactly. The gateway does this by sending the output schema as a *grammar constraint* alongside the prompt, so the inference server is forced to emit only conforming tokens. In live testing this turns a request that would otherwise ramble into prose into a tight, parseable result: a short business sentence returned four correctly classified entities — company, location, location, person — in about seven seconds.

*Engineering note — the constraint is engine-specific, and that is a maintenance hazard.* The mechanism for requesting a grammar constraint differs between inference engines. One family of servers reads the constraint from a nested request envelope; another reads it from top-level request fields and silently ignores the envelope. When the substrate's burst tier migrated from the first engine to the second, one client path was updated and another was not — so for a period the schema was sent in a form the running server ignored, and the model generated unconstrained prose that could not be parsed. The lesson is durable: when a structured-output constraint "isn't working," confirm empirically which request field the *deployed* engine actually honours before changing anything else, because the failure is silent — the server returns a valid response that simply ignores the constraint.

## The boundary between interactive and batch

A second durable lesson: a reasoning model is the wrong tool for a structured, mechanical task. The 32B reasoning model spends a large token budget "thinking" before answering, which is valuable for hard generation work but pure overhead for extracting named entities against a fixed schema. The substrate's design intent is therefore to reserve reasoning for the generative path and run the extraction path with reasoning suppressed — fast, cheap, and deterministic. Per-path reasoning control at the gateway is a planned capability; today the reasoning budget is a server-wide setting for the burst-tier inference server.

## Surviving an interrupted burst

The burst GPU runs on reclaimable (spot) capacity: the cloud provider can take the machine back at any moment, often with little or no warning. A substrate that lost or corrupted work every time this happened would be unusable, so the design treats interruption as a normal event rather than a failure.

Two paths carry in-flight work, and both are built to fail closed. On the batch side, each unit of work is leased from a durable queue before it is sent to the GPU; if the machine disappears mid-request, the lease simply expires and a reaper returns the unit to the queue, where the next worker picks it up. Nothing is marked done until the result is actually in hand. On the extraction side, the service that feeds documents to the gateway distinguishes a transient interruption from a genuine, permanent failure. A request cut off because the GPU vanished is treated as retryable, not as a processed document — so it is never silently dropped. While the GPU is unavailable, pending documents are held in a dormant state rather than retried in a tight loop, which would needlessly hammer the gateway. A single lightweight probe runs on a fixed interval; the moment it succeeds, the whole dormant backlog is promoted back into the active queue and extraction resumes on its own, without any operator action or service restart.

The result is a flow that degrades gracefully: an interrupted burst costs some latency while the system notices and falls back, but no document is lost, no record is half-written, and recovery is automatic when capacity returns.

## Why this matters

The tiered substrate is what lets a customer-controlled deployment behave like a managed AI service without surrendering control of its data or its compute. Routine work is instant and free on local hardware; heavy work bursts to a GPU only as needed and stops itself; structured records never leave the operator's boundary; and the model's output is constrained to a shape the system can trust. The architecture is deliberately unremarkable in operation — which, for infrastructure that sits between a private data vault and an external model, is the point.

## See also

- [[architecture-decisions|SYS-ADR-07]] — the architectural decision record that encodes the structured-data boundary
- [[service-slm]] — the service that implements the gateway and circuit-breaker logic
- [[service-content]] — the extraction client that feeds documents through the gateway
