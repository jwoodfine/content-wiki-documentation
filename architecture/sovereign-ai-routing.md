---
schema: foundry-doc-v1
title: "AI routing and the linguistic air-lock"
slug: sovereign-ai-routing
category: architecture
type: topic
content_type: topic
quality: complete
short_description: "AI routing in the PointSav platform processes language model requests through a local sanitization step before any data reaches external models, ensuring that internal structured data never travels to third-party servers in identifiable form."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-04-30
editor: pointsav-engineering
cites: []
paired_with: sovereign-ai-routing.es.md
---


> AI routing in the PointSav platform processes language model requests through a local sanitization step before any data reaches external models, ensuring that internal structured data never travels to third-party servers in identifiable form.

**AI routing** in the [[pointsav-overview|PointSav]] platform is the mechanism by which [[service-slm|`service-slm`]] — the [[doorman-protocol|Doorman]] — mediates every request that involves a language model, whether the model runs locally on the customer's hardware, on a burst compute provider, or on an external API. The routing design treats the boundary between customer-controlled infrastructure and external compute as a one-directional filter: before any text leaves the customer's private network, the payload passes through a local Small Language Model that sanitizes sensitive information, strips location identifiers, and masks Personally Identifiable Information (PII). Only the sanitized prompt — containing the mathematical structure of the request but not the customer's private data — routes to external compute. When the external model returns a result, the router re-hydrates the response with the correct internal context before delivering it to the operator. The external model never holds the actual structured records from the customer's ledger.

## Overview

Commercial language models operate as external services. When an operator sends raw internal documents, ledger records, or operational questions to a centralized AI provider, that data enters third-party servers. For regulated industries — real estate, financial advisory, small clinics, law firms — this creates a compliance problem that cannot be solved by contractual agreements alone, because the data has physically left the customer's infrastructure.

The [[pointsav-overview|PointSav]] routing design solves this at the architecture layer. [[service-slm|`service-slm`]] acts as the sole boundary that holds API keys, logs every external call to the per-tenant audit ledger, and applies the sanitize-outbound / rehydrate-inbound discipline on every request. No other component in the system holds external AI credentials or makes direct outbound calls to external language models. See [[single-boundary-compute-discipline|the single-boundary compute discipline]].

## How It Works

The routing flow for a request that reaches Tier C (external API):

1. Operator or service sends request to [[service-slm|`service-slm`]] [[doorman-protocol|Doorman]].
2. Doorman identifies the tenant (`moduleId`) and the request tier.
3. Local SLM (Tier A, OLMo 3 7B) runs the sanitization pass: identifies PII patterns, strips physical coordinates, replaces identifiable references with pseudonymous tokens, and records the token-to-original mapping in a per-request rehydration table held in local memory.
4. Sanitized prompt routes outbound to the external model endpoint.
5. External model returns response.
6. Doorman applies the rehydration pass: replaces pseudonymous tokens with the correct internal context before returning the response to the caller.
7. Doorman appends the full request record — original (local), sanitized version, response, grammar version, [[adapter-composition|adapter composition]] — to the per-tenant audit ledger ([[service-fs-architecture|`service-fs`]]).

For Tier A (local) and Tier B (burst) requests, steps 3–6 simplify: the sanitization pass still runs for consistency of audit records, but the data does not leave the customer's infrastructure.

## Architecture

[[service-slm|`service-slm`]] is the single [[doorman-protocol|Doorman]] boundary across all three compute tiers:

- **Tier A — Local:** OLMo 3 7B Q4 on the customer's machine (CPU). Zero data leaves the customer's hardware.
- **Tier B — [[yoyo-compute-substrate|Yo-Yo burst]]:** OLMo 3.1 32B Think on multi-cloud GPU burst (GCP Cloud Run / RunPod / Modal / customer GPU). Sanitized prompt only.
- **Tier C — External API:** Anthropic Claude / Google Gemini / OpenAI for narrow precision tasks. Sanitized prompt only; API keys held exclusively by Doorman.

The customer does not select the tier. Request shape, prompt length, and the tenant's configured budget caps determine routing. The Doorman's routing decision is logged to the audit ledger alongside the request record.

## Applications

- **Editorial workflow:** TOPIC and GUIDE drafts routed through external models carry only the sanitized editorial prompt; customer-specific terminology maps are applied locally.
- **Financial advisory firms:** ledger summaries routed for analysis strip account numbers, client names, and jurisdiction identifiers before leaving the office network.
- **Real estate operations:** property records routed for description generation replace addresses and owner names with pseudonymous tokens for the external call.

## See also

- [[compounding-substrate]]
- [[worm-ledger-architecture]]
- [[decode-time-constraints]]
- [[machine-based-auth]]
- [[3-layer-stack]]
