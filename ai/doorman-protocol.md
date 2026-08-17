---
schema: foundry-doc-v1
title: "Doorman protocol"
slug: doorman-protocol
short_description: "The Doorman is the sole AI request boundary through which every inference call routes, enforcing sanitise-and-rehydrate once and logging every call to an immutable audit ledger."
category: ai
type: concept
content_type: topic
index_group: the-doorman-boundary
status: active
bcsc_class: current-fact
forward_looking: true
last_edited: 2026-08-17
editor: pointsav-engineering
cites: []
paired_with: doorman-protocol.es.md

---

Every service that can call an external AI model is its own hole in the wall. Ten services with ten egress paths means ten audit surfaces, and ten places the sanitise discipline can be forgotten.

The Doorman closes the wall to a single door. [[service-slm|`service-slm`]] is the platform's sole AI request boundary; every inference call routes through one access-control gateway, and no inference call leaves the customer data vault without passing through it.

At that one boundary the Doorman enforces sanitise-and-rehydrate discipline, routes the call to the appropriate compute tier, logs every event to an immutable audit ledger, and captures the training signal that compounds the platform over time.

For a regulated buyer the consequence is concrete. No inference call leaves the data vault unlogged or unsanitised, because the discipline is a structural guarantee rather than a per-service configuration. This article defines the routing rules, the audit schema, the `moduleId` discipline, and the training-signal capture.

## Why a Doorman

A customer data vault holds the customer's authoritative structured data, and external compute — large language models — cannot be trusted with raw structured facts. Without a single boundary, every service in the [[totebox-os|Totebox]] grows its own egress path, every egress path needs its own audit, and the sanitise-and-rehydrate discipline (SYS-ADR-07) becomes per-service discipline rather than substrate discipline. The Doorman centralises the boundary so the discipline is enforced once.

## Three-tier compute routing

The Doorman routes inference calls across three compute tiers. All three are implemented in the routing code — "planned" describes activation state, not code that doesn't exist yet.

**Tier A — local.** Executes on the host VM using CPU and RAM, for fast, low-latency, low-cost inference on a locally hosted model. Tier A handles the majority of routing volume with no cloud spend, and is operationally verified.

**Tier B — on-demand GPU pool.** Tier B routes workloads to ephemeral GPU instances ([[yoyo-compute-substrate|the Yo-Yo compute substrate]]), spun up on demand and shut down on idle (a 30-minute default idle-shutdown monitor issues the real deprovision call), with two profiles: a **trainer** instance for continued training cycles on accumulated tuples, and a **graph** instance for property-graph workloads — not an "extractor" instance as earlier documentation described. The routing logic and idle-shutdown monitor are fully wired; whether a given profile is reachable at any moment depends on its own health probe and circuit-breaker state, which the Doorman's `/readyz` endpoint reports per profile.

**Tier C — external API proxy.** Tier C's allowlist and cost-guardrail scaffolding are implemented for narrow-precision tasks — citation grounding, graph-build assistance, entity disambiguation — but the crate's own source comments state live external API calls are not yet enabled in this version; activating them is a separate operator decision, not a missing feature. Earlier documentation claimed Tier C "injects predefined `service-content` ontologies to constrain output to canonical platform vocabulary" — no such mechanism exists in the Tier C code path; that claim is retracted here, not merely softened.

## The audit ledger

Every inference call produces a JSONL audit-ledger entry appended to a daily file. Fields: timestamp, request ID, module ID, tier, model, inference duration, cost estimate, sanitised-outbound flag, completion status, entry type, and (when applicable) an error message and an archive name. Each entry also carries a hash computed at write time for tamper detection. The ledger is append-only; no entry is modified or deleted after write.

## The moduleId discipline

`moduleId` is confirmed to serve two roles, not five: it tags audit-ledger entries for per-project cost accounting, and — since the tenant-isolation fix landed — it strictly scopes property-graph reads and writes to the caller's own module, with no cross-tenant merge. Earlier documentation additionally claimed `moduleId` selects the systemd unit handling a request, namespaces the key-value cache, and selects the adapter stack. None of those three roles has support in the current routing, caching, or adapter-hub code, so the claim is retracted here rather than carried forward unverified.

Enforcement is real but narrower than "every request needs a valid `moduleId`": the graph endpoints (`graph_query`, `graph_mutate`) reject a missing or malformed `moduleId` outright. The primary inference endpoint (`chat_completions`) rejects a malformed `moduleId`, but silently falls back to a default when the header is simply absent, logging only a warning — a real gap between the two endpoint families, not a uniform boundary.

## Learning-pipeline routing

The Doorman implements the [[apprenticeship-substrate]] routing inversion for code-shaped and editorial work: `service-slm` attempts first, and the senior session reviews. Every signed verdict — `Accept`, `Refine`, `Reject`, `DeferTierC` — is captured to the apprenticeship corpus as a training tuple.

The Doorman's routing logic and the apprenticeship substrate's promotion ledger are two surfaces of the same mechanism.

## See also

- [[compounding-doorman]] — conceptual overview of the Doorman as a sovereign AI substrate pattern
- [[apprenticeship-substrate]] — the routing inversion and verdict-signing protocol that compounds the substrate
- [[three-ring-architecture]] — Ring 3 framing; the Doorman is the sole Ring 3 service
- [[service-slm]] — the service-slm crate that implements the Doorman
- [[configure-doorman]] — step-by-step guide: set Tier A/B/C addresses, circuit-breaker thresholds, and verify the health endpoint
- [[run-first-slm-query]] — step-by-step guide: submit an inference prompt and read the Doorman health dashboard
