---
schema: foundry-doc-v1
title: "Doorman protocol"
slug: doorman-protocol
short_description: "The Doorman is the sole AI request boundary through which every inference call routes — enforcing sanitise-and-rehydrate discipline once, logging every call to an immutable audit ledger, and capturing the training signal that compounds the platform over time."
category: architecture
type: concept
status: active
bcsc_class: current-fact
forward_looking: true
last_edited: 2026-05-22
editor: pointsav-engineering
cites: []
paired_with: doorman-protocol.es.md
---

Every service that can call an external AI model is its own hole in the wall. Ten services with ten egress paths means ten audit surfaces, and ten places the sanitise discipline can be forgotten.

The Doorman closes the wall to a single door. <!--claim id=sole-boundary confidence=structural cites=[]-->`service-slm` is the platform's sole AI request boundary; every inference call routes through one access-control gateway, and no inference call leaves the customer data vault without passing through it.<!--/claim-->

<!--claim id=doorman-functions confidence=structural cites=[]-->At that one boundary the Doorman enforces sanitise-and-rehydrate discipline, routes the call to the appropriate compute tier, logs every event to an immutable audit ledger, and captures the training signal that compounds the platform over time.<!--/claim-->

For a regulated buyer the consequence is concrete. No inference call leaves the data vault unlogged or unsanitised, because the discipline is a structural guarantee rather than a per-service configuration. This article defines the routing rules, the audit schema, the `moduleId` discipline, and the training-signal capture.

## Why a Doorman

A customer data vault holds the customer's authoritative structured data, and external compute — large language models — cannot be trusted with raw structured facts. <!--claim id=centralised-discipline confidence=structural cites=[]-->Without a single boundary, every service in the Totebox grows its own egress path, every egress path needs its own audit, and the sanitise-and-rehydrate discipline (SYS-ADR-07) becomes per-service discipline rather than substrate discipline.<!--/claim--> The Doorman centralises the boundary so the discipline is enforced once.

## Three-tier compute routing

The Doorman routes inference calls across three compute tiers.

**Tier A — local.** Executes on the host VM using CPU and RAM, for fast, low-latency, low-cost inference on a locally hosted model. <!--claim id=tier-a-verified confidence=established cites=[]-->Tier A handles the majority of routing volume with no cloud spend, and is operationally verified.<!--/claim-->

**Tier B — on-demand GPU pool.** <!--claim id=tier-b-planned confidence=projected cites=[] valid_at=2026-->Tier B is planned to route workloads to ephemeral GPU instances, spun up on demand and shut down on idle, with two profiles: a trainer instance for continued training cycles on accumulated tuples, and an extractor instance for large-scale corpus ingestion.<!--/claim--> Both profiles use idle-shutdown timers so billing stops when the queue is empty.

**Tier C — external API proxy.** Tier C is planned to route specialised linguistic refinement and formatting tasks to external frontier models. The Doorman enforces cost guardrails and injects predefined `service-content` ontologies to constrain output to canonical platform vocabulary.

## The audit ledger

<!--claim id=audit-ledger confidence=structural cites=[]-->Every inference call produces a JSONL audit-ledger entry appended to a daily file. The required fields are timestamp, request ID, module ID, tier, model, inference duration, cost estimate, sanitised-outbound flag, and completion status. The ledger is append-only; no entry is modified or deleted after write.<!--/claim-->

## The moduleId discipline

<!--claim id=moduleid-five-roles confidence=structural cites=[]-->A single `moduleId` field serves five roles at once: it selects the systemd unit that handles the request, namespaces the key-value cache blocks, scopes the property-graph database traversals to the correct tenant, selects the adapter stack, and tags audit-ledger entries for per-project cost accounting. A request without a valid `moduleId` is rejected at the Doorman boundary.<!--/claim-->

## Learning-pipeline routing

<!--claim id=learning-routing confidence=structural cites=[]-->The Doorman implements the [[apprenticeship-substrate]] routing inversion for code-shaped and editorial work: `service-slm` attempts first, and the senior session reviews. Every signed verdict — `Accept`, `Refine`, `Reject`, `DeferTierC` — is captured to the apprenticeship corpus as a training tuple.<!--/claim-->

The Doorman's routing logic and the apprenticeship substrate's promotion ledger are two surfaces of the same mechanism.

## See also

- [[compounding-doorman]] — conceptual overview of the Doorman as a sovereign AI substrate pattern
- [[apprenticeship-substrate]] — the routing inversion and verdict-signing protocol that compounds the substrate
- [[three-ring-architecture]] — Ring 3 framing; the Doorman is the sole Ring 3 service
- [[service-slm]] — the service-slm crate that implements the Doorman
