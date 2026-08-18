---
schema: foundry-doc-v1
title: "Doorman protocol"
slug: doorman-protocol
short_description: "The Doorman is the sole AI request boundary through which every inference call routes, holding every external-model credential and logging every call to an immutable audit ledger."
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

Every service that can call an external AI model is its own hole in the wall. Ten services with ten egress paths means ten audit surfaces, and ten places credential handling and logging can drift out of sync.

The Doorman closes the wall to a single door. [[service-slm|`service-slm`]] is the platform's sole AI request boundary; every inference call routes through one access-control gateway, and no inference call leaves the customer data vault without passing through it.

At that one boundary the Doorman holds every external-model credential, routes the call to the appropriate compute tier, logs every event to an immutable audit ledger, and captures the training signal that improves the platform over time.

For a regulated buyer the consequence is concrete. No inference call leaves the data vault unlogged or with a credential the Doorman doesn't control, because the boundary is a structural guarantee rather than a per-service configuration. This article defines the routing rules, the audit schema, the `moduleId` discipline, and the training-signal capture.

## Why a Doorman

A customer data vault holds the customer's authoritative structured data. Without a single boundary, every service in the [[totebox-os|Totebox]] grows its own egress path, every egress path needs its own audit, and credential and audit discipline becomes per-service rather than platform-wide. The Doorman centralises the boundary so the discipline is enforced once.

**What the Doorman does not yet do**: it does not scrub personally identifiable information or location data from a prompt before an external call. The only sanitisation code on the platform today redacts credentials — API keys, tokens, private keys — and runs solely on the path that writes training examples into the learning corpus, never on the path to an external model. See [[sovereign-ai-routing]] for the full picture of what reaches Tier C today and what does not.

## Three-tier compute routing

The Doorman routes inference calls across three compute tiers.

**Tier A — local.** Executes on the host VM using CPU and RAM, for fast, low-latency, low-cost inference on a locally hosted model. Tier A handles the majority of routing volume with no cloud spend.

**Tier B — on-demand GPU pool.** Tier B routes workloads to ephemeral GPU instances ([[yoyo-compute-substrate|the Yo-Yo compute substrate]]), spun up on demand and shut down on idle — a 30-minute default idle window before deprovisioning — with two profiles: a **trainer** instance for continued training cycles on accumulated tuples, and a **graph** instance for property-graph workloads. Whether a given profile is reachable at any moment depends on its own health probe and circuit-breaker state, which the Doorman's health endpoint reports per profile.

**Tier C — external API proxy.** Tier C's allowlist and cost-guardrail scaffolding cover narrow-precision tasks — citation grounding, graph-build assistance, entity disambiguation. Activating live external calls is a deliberate, separate operator decision, not an in-progress build.

## The audit ledger

Every inference call produces a JSONL audit-ledger entry appended to a daily file. Fields: timestamp, request ID, module ID, tier, model, inference duration, cost estimate, sanitised-outbound flag, completion status, entry type, and (when applicable) an error message and an archive name. Each entry also carries a hash computed at write time for tamper detection. The ledger is append-only; no entry is modified or deleted after write.

## The moduleId discipline

`moduleId` serves two roles: it tags audit-ledger entries for per-project cost accounting, and it strictly scopes property-graph reads and writes to the caller's own module, with no cross-tenant merge.

Enforcement differs by endpoint. The graph endpoints reject a missing or malformed `moduleId` outright. The primary inference endpoint rejects a malformed `moduleId`, but falls back to a default when the header is simply absent, logging only a warning — a narrower guarantee on that path than on the graph endpoints.

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
