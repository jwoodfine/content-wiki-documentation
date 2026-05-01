---
schema: foundry-doc-v1
title: "The Compounding Doorman"
slug: compounding-doorman
category: architecture
type: topic
quality: complete
short_description: "The operational pattern at the heart of sovereign AI substrates: a single service that mediates every external compute call, enforces sanitise-and-rehydrate discipline, logs every event to an audit ledger, and accumulates training signal that compounds the substrate over time."
status: pre-build
last_edited: 2026-04-30
editor: pointsav-engineering
cites: []
paired_with: compounding-doorman.es.md
---

The **Compounding Doorman** is the operational pattern at the centre of a sovereign AI substrate. A single service mediates every external compute call. It enforces sanitise-and-rehydrate discipline at both ends of the call. It logs every event to an immutable audit ledger. And it accumulates training signal that compounds the substrate over time — each interaction makes the next one more accurate, without any raw data leaving the customer's infrastructure.

In the PointSav platform, `service-slm` is the Compounding Doorman. It is the sole service at Ring 3 of the [[three-ring-architecture]]. Every request that touches an AI inference model passes through this boundary, and only through this boundary.

## What the Doorman enforces

The Doorman enforces four disciplines simultaneously on every call:

**Sanitise outbound, rehydrate inbound.** SYS-ADR-07 prohibits structured data from routing through AI. Before any request leaves the Doorman boundary, identifiers, foreign keys, and structured fields are replaced with opaque tokens. After the response returns, the tokens are resolved back to their original values. The AI model sees only prose and opaque tokens; it never receives or returns structured records. This is what makes the audit-routing path reversible and auditable.

**Three-tier compute routing.** The Doorman selects among three compute tiers per request shape and budget policy:
- **Tier A — local**: OLMo 3 7B on the customer's own hardware. Zero marginal cost, full data locality. Default for most operations.
- **Tier B — GPU burst**: OLMo 3.1 32B Think on a short-lived GPU instance. Used for requests the local tier cannot handle efficiently. The customer controls start and stop; idle-shutdown is the default.
- **Tier C — external API**: external vendor APIs, used only with an explicit per-request allowlist. Audit-logged at the customer's ledger, not at the vendor's.

The customer's routing configuration — request shape thresholds and per-tier budget caps — determines which tier handles each request. No per-request manual selection is needed.

**Audit ledger.** Every external call produces a ledger entry recording the token count, cost estimate, `moduleId`, and response status. The ledger is append-only. An operator who needs to answer "did AI touch this record, and when?" can inspect the ledger directly, without querying a third-party system. The audit surface is owned by the customer and stays on the customer's infrastructure.

**Key custody.** All API keys for Tier C services are held exclusively at the Doorman boundary. No downstream service, no Ring 2 process, no editorial pipeline holds a vendor key. If a key is rotated or revoked, the change happens in one place.

## Why it compounds

A Compounding Doorman deployment improves over time through the apprenticeship substrate:

- **At deployment**: the Doorman serves with the current OLMo 3 base plus any LoRA adapters already trained for this tenant.
- **After the first training cycle**: the first per-tenant LoRA adapter is trained on accumulated corpus signal. Tasks the local model previously deferred to Tier B can now be handled at Tier A. Tier B calls become less frequent; the per-request cost falls.
- **Over multiple cycles**: additional adapters accumulate in the library, hot-swapped per request based on the task type the Doorman identifies. The model becomes progressively more accurate on the customer's specific operational patterns — the actual error states they encounter, the actual command shapes they prefer, the actual terminology they use.
- **Through federation** (planned): customers who opt into federated compounding contribute distilled training signal to the curator. The curator rolls accumulated signal across many deployments into an improved base model. The improved base returns to every deployment. No customer's raw data leaves customer-controlled storage.

The compounding loop closes because the audit ledger that records what the Doorman did is the same substrate that feeds training data. Every interaction is simultaneously an operational event and a training signal.

## The Doorman metaphor

The metaphor maps precisely to the operational discipline:

- A doorman greets every guest — every request enters through this boundary.
- A doorman checks identification — the Doorman validates `moduleId` and sanitises inputs.
- A doorman directs guests to the right destination — routing to local, GPU burst, or external API per policy.
- A doorman carries bags through the door — rehydrating the response with full identifiers stripped at outbound.
- A doorman keeps a log of who came and went — the audit ledger.
- A doorman never enters the rooms themselves — the Doorman never writes to the authoritative knowledge graph; it only proposes, per SYS-ADR-07.

The discipline is what makes sovereign AI auditable, reversible, and compoundable.

## Relationship to the Three-Ring Architecture

The Compounding Doorman is the entirety of Ring 3. It is the single point at which AI touches the platform. Its read-only posture toward Ring 2 is not a limitation but an architectural guarantee: the deterministic knowledge pipeline in Rings 1 and 2 remains the authoritative record regardless of what Ring 3 proposes.

This is what allows a deployment to operate Ring 3 at any trust level — from full AI-assisted operations to a configuration where Ring 3 is present but all proposals require explicit human approval before entering Ring 2. The Doorman enforces the human-checkpoint rule (SYS-ADR-10) at the point where AI output would otherwise flow silently into the knowledge graph.

## Implementation state

The Doorman (`service-slm`) is operational on the workspace VM. It binds at `127.0.0.1:9080`, routes Tier A to the local model service, and enforces sanitise-outbound and rehydrate-inbound discipline on every call. The audit ledger writes to `data/audit-ledger/<tenant>/<YYYY-MM>.jsonl`.

Tier B integration (Yo-Yo GPU burst) is in progress. Tier C external API routing is available for narrow precision tasks where the operator has explicitly configured an allowlist.

LoRA adapter training — the mechanism that makes the Doorman compound — depends on the Brief Queue Substrate for corpus capture and the apprenticeship substrate for the training pipeline. Both are operational or in active development.

## See Also

- [[three-ring-architecture]] — the ring structure the Compounding Doorman occupies (Ring 3)
- [[service-slm]] — the specific service that implements the Compounding Doorman in the PointSav platform
- [[compounding-substrate]] — the five structural properties the Compounding Doorman contributes to
- [[brief-queue-substrate]] — the durable queue that keeps corpus capture continuous across compute-tier transitions
- [[apprenticeship-substrate]] — how the Doorman's audit events generate training signal for per-tenant LoRA adapters

## References

1. `conventions/compounding-substrate.md` — the meta-pattern the Compounding Doorman implements; five structural properties.
2. `conventions/three-ring-architecture.md` — internal specification; the Doorman at Ring 3.
3. SYS-ADR-07 — structured data never routes through AI; the sanitise-outbound discipline at the Doorman boundary.
4. SYS-ADR-10 — the mandatory human checkpoint that the Doorman enforces at the Ring 2 write path.
5. MEMO §6.3 — `service-slm` specification: AI Gateway with sanitise-outbound boundary.

---

## Provenance

Source material: workspace-root draft `topic-compounding-doorman.md`, conventions `compounding-substrate.md` and `three-ring-architecture.md`, MEMO §6.3 service-slm specification. Refinement disciplines applied: no body H1; structural-positioning discipline (metaphor framing retained as operational precision, not competitive contrast; no vendor names used); BCSC forward-looking adapter applied to federation claim (Tier B integration and federation cadence labelled as planned); banned-vocabulary pass (no substitutions required); implementation status section grounded in operational workspace state as of 2026-04-30.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
