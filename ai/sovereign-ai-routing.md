---
schema: foundry-doc-v1
title: "AI routing and the linguistic air-lock"
slug: sovereign-ai-routing
category: ai
type: topic
content_type: topic
quality: complete
index_group: the-doorman-boundary
short_description: "AI routing holds every external-model credential and audit-logs every request at a single boundary. It does not scrub PII from prompts, and Tier C external routing is not live yet."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-08-17
editor: pointsav-engineering
cites: []
paired_with: sovereign-ai-routing.es.md

---


**AI routing**, as it exists today, is the mechanism by which [[service-slm|`service-slm`]] — the [[doorman-protocol|Doorman]] — mediates every request that involves a language model, across three compute tiers. `service-slm` is the sole boundary that holds external-model credentials and logs every call to the per-tenant audit ledger; no other component in the system holds external AI credentials or makes direct outbound calls to external language models.

This platform does not scrub personally identifiable information or location data from a prompt before an external call. The only sanitization code on the platform today is a credential redactor: it removes secrets — private keys, API tokens, generic bearer/secret/password patterns — and it runs solely on the path that writes training examples into the learning corpus, never on the path to an external model.

This is a compliance-relevant gap, not a cosmetic one, for regulated-industry readers — real estate, financial advisory, clinics, law firms — evaluating the platform's privacy protections. The honest current answer: when Tier C goes live, raw customer text will reach an external model unless a PII-scrubbing mechanism is built first. The credential redactor protects secrets, not customer data.

## What's real today

- **Three compute tiers**: Tier A (local), Tier B (Yo-Yo burst/GPU), Tier C (external API).
- **Model names**: Tier A runs `olmo-3-7b-instruct` locally; Tier B (Yo-Yo) defaults to `Olmo-3-1125-32B-Think`.
- **Tier C is not live.** The client is wired only against a test mock, and every call is gated behind a fixed, compile-time allowlist.
- **Every proxied call is audit-logged**, with cost and response recorded to the audit ledger.
- **Every request carries a mandatory tenant tag.**
- **No per-tenant budget cap gates routing decisions yet.** Cost tracking and pricing configuration exist, but nothing currently ties a tenant's spend to a routing decision.

## What is not built

PII scrubbing, location-identifier stripping, pseudonymous token substitution, and any form of rehydration mechanism are not built.

## Applications — what the platform can honestly promise today

- **Editorial workflow**: TOPIC and GUIDE drafts that reach Tier C today do so through the fixed allowlist's narrow-precision tasks (see [[learning-datagraph-architecture]] for `draft_generate`'s behavior) — not through any sanitization step, because none exists for this path.
- **Financial advisory / real estate / clinic / law-firm use** of Tier C is not yet a safe claim to make. Any of these use cases sending ledger records, client names, or property/owner records through Tier C today would reach the external model with PII unredacted. A real PII-scrubbing mechanism, independently verified, must exist before that changes.

## See also

- [[compounding-substrate]]
- [[worm-ledger-architecture]]
- [[decode-time-constraints]]
- [[machine-based-auth]]
- [[3-layer-stack]]
