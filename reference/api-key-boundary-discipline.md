---
schema: foundry-doc-v1
title: "API Key Boundary Discipline"
slug: api-key-boundary-discipline
category: reference
type: topic
quality: published
short_description: The rule that all external LLM API credentials belong exclusively at the gateway service and never at inference engines.
status: pre-build
last_edited: 2026-05-01
editor: pointsav-engineering
cites:
  - ni-51-102
paired_with: api-key-boundary-discipline.es.md
---

In a platform that routes inference requests through multiple compute tiers, the single most consequential security discipline is also one of the simplest to state: API keys belong at the gateway, never at the inference engine. This TOPIC explains the rule, its structural rationale, and how it applies across every deployment tier in the PointSav substrate.

## The rule

Any process that runs model inference — whether a local quantized model on a Totebox appliance, a cloud-burst GPU worker, or any future compute node — must not read or hold credentials for external LLM providers. Credentials flow only between the Doorman gateway and the external API endpoint. There are no exceptions.

The corollary: if a use case appears to require an exception, the correct response is to route the request through the gateway, adding a new endpoint or purpose if needed, rather than passing the key to the inference process.

## Why a single boundary

Three structural properties follow from holding this discipline:

**Audit completeness.** Every API call passes through the gateway boundary. A per-tenant audit ledger can capture provider, purpose, token volume, and cost at one chokepoint. Shadow paths that bypass the gateway produce shadow spend that cannot be attributed or audited.

**Allowlist enforcement.** Restricting inference calls to a defined set of permitted purposes requires a single enforcement point. A gateway that receives all requests can enforce the allowlist; inference engines scattered across compute nodes cannot.

**Stateless inference scaling.** Inference processes that hold no secrets can be started, stopped, replaced, and scaled without credential rotation. Cold-starting a new inference node means loading model weights and accepting requests — nothing more.

## Key placement by tier

The discipline applies consistently across every deployment shape:

**Self-hosted Totebox (customer deployment).** The customer's local Doorman holds external LLM keys and, optionally, a subscription key for cloud-hosted model tiers. The local inference engine holds nothing. Customer keys never travel to the vendor.

**Cloud-burst workers.** When a request routes to a GPU worker in a cloud provider's infrastructure, the worker holds no external API credentials. Authentication between the cloud-burst tier and any external provider is handled by the gateway that dispatched the request.

**Vendor gateway (vendor-side deployments).** The vendor's Doorman holds vendor-side credentials. The vendor never holds, stores, or accesses customer external LLM keys. Federated marketplace contributions exchange adapters, not credentials.

## Forbidden patterns

The following patterns violate the discipline regardless of context:

- An inference process reading keys from environment variables, even if it does not make external calls at that moment.
- An inference process fetching keys from a secrets manager at boot.
- Ad-hoc scripts reading external API keys from any source other than the gateway.
- Vendor-side storage of customer-owned external LLM credentials.

## Relationship to identity credentials

API keys for LLM providers are runtime credentials — they change on rotation, they belong to the Doorman, they are never embedded in code. They are distinct from identity signing keys, which are authorship credentials used at commit time. The two classes of credential have separate storage locations and separate lifecycle rules; neither crosses the other's boundary.

## Audit and compliance

The gateway boundary, combined with a per-tenant audit ledger and a purpose allowlist, produces a cryptographic audit trail over every external inference call. This structure satisfies SOC 2 Processing Integrity requirements and ISAE 3402 chain-of-custody principles by construction rather than by periodic attestation. The customer's own per-tenant ledger covers the customer's calls; the vendor's ledger covers the vendor's calls; the two never intermingle.

## See also

- [[compounding-substrate]] — the three-ring architecture this discipline is embedded in
- [[design-system-substrate]] — the design system substrate, which routes AI-readable research through the same gateway boundary
- [[cluster-wiki-draft-pipeline]] — the editorial pipeline, whose inference calls route through the gateway

## Provenance

Authored 2026-05-01 by project-language Task Claude. Source: `conventions/api-key-boundary-discipline.md` (ratified 2026-04-29). Research basis: 2026 LLM gateway industry consensus; cross-checked against Foundry gateway implementation. Forward-looking statements (planned federation marketplace) carry intended/planned framing per [ni-51-102].

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
