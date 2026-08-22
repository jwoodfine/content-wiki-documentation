---
schema: foundry-doc-v1
title: "AI inference service"
slug: service-slm
category: services
type: concept
content_type: topic
quality: complete
index_group: ring-3-ai-gateway
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-08-22
editor: pointsav-engineering
paired_with: service-slm.es.md
short_description: "service-slm is the platform's AI inference gateway — every request, local or remote, transits the Doorman's audit boundary and one of three compute tiers before a response returns."
cites:
 - olmo3-allenai
references:
  - id: 1
    text: "ISO/IEC 42001:2023 — Information technology — Artificial intelligence — Management system."
    url: "https://www.iso.org/standard/81230.html"
  - id: 2
    text: "Groeneveld, D. et al. 'OLMo: Accelerating the Science of Language Models.' arXiv:2402.00838, 2024."
    url: "https://arxiv.org/abs/2402.00838"
---

An AI request that leaves the building cannot be audited and cannot be recalled. `service-slm`
is the platform's AI inference gateway — the workspace that houses the [[doorman-protocol|
Doorman]] router and its supporting crates — and its central property is that every inference
call, whatever tier ultimately serves it, crosses the Doorman's audit boundary first.

## The Doorman routes, callers hint

`service-slm` implements [[model-tier-discipline|the platform's tier-routing discipline]]:
a caller submits a complexity hint, not a tier choice, and the Doorman picks one of three
routes based on that hint plus live budget state.

| Route | Where it runs | Model |
|---|---|---|
| Local | On the same host as the Doorman | Quantized OLMo 3 7B, served over HTTP |
| Yoyo | A preemptible multi-cloud GPU burst instance | A larger OLMo 3 model tuned for deeper reasoning |
| External | A licensed third-party API, allowlist-gated | A frontier model, for narrow precision-critical tasks only |

These three internal routing tiers are a distinct system from the customer-facing commercial
subscription ladder described in [[pointsav-llm]] — the source code itself names the routing
enum deliberately to avoid the two colliding.

## The Doorman audit boundary

Every prompt and completion captured by the Doorman is written to an audit path before the
response returns to the caller, forming the institutional record of every AI decision. The
Doorman exists for three reasons:

1. **Regulatory.** ISO/IEC 42001, the AI management-system standard [^1], calls for an
   immutable log of AI-assisted decisions.
2. **Operational.** A self-healing system needs a corpus of its own past behaviour to improve
   against; the audit capture provides it.
3. **Sovereign.** No request reaches a third-party API without first passing through a
   boundary the operator controls.

Full detail on the Doorman's own routing and audit mechanics: [[doorman-protocol]].

## Model selection

The canonical local model is from the OLMo family, which ships with fully open weights and
training-data documentation [^2] — a prerequisite for continued pre-training on an operator's
own corpus, the long-term path to a domain-specialised model.

## Why a small model, by default

A frontier-scale model imposes costs the Local tier is built to avoid: cloud egress, tens of
gigabytes of RAM, and a request that cannot be meaningfully audited. A quantized 7B model is
sufficient for most requests and fits inside the cost envelope of a low-cost node running
alongside the rest of the platform. Specialisation and tiering, not scale by default, is the
design principle — the Yoyo and External tiers exist precisely for the requests where more
capability is genuinely needed.

## See also

- [[doorman-protocol]] — the Doorman's routing and audit mechanics in detail
- [[model-tier-discipline]] — the tier-routing discipline this service implements
- [[pointsav-llm]] — the distinct, customer-facing commercial tier ladder
- [[architecture-decisions|SYS-ADR-07]] — structured data never routes through AI; the Doorman implements this boundary
- [[run-local-slm-inference]] — step-by-step guide: start the SLM service and submit inference requests from the console or API
- [[run-first-slm-query]] — step-by-step guide: read the Doorman health dashboard and submit your first prompt
