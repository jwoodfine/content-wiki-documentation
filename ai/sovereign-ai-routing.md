---
schema: foundry-doc-v1
title: "AI routing and the linguistic air-lock"
slug: sovereign-ai-routing
category: ai
type: topic
content_type: topic
quality: complete
index_group: the-doorman-boundary
short_description: "AI routing holds every external-model credential and audit-logs every request at a single boundary — but the sanitize-outbound/rehydrate-inbound PII mechanism earlier versions of this article described does not exist in code, and Tier C external routing itself is not live yet."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-08-17
editor: pointsav-engineering
cites: []
paired_with: sovereign-ai-routing.es.md

---


**What this article used to claim, and what's actually true.** Earlier versions described a "sanitize-outbound / rehydrate-inbound" mechanism: a local pass that would strip PII and location identifiers before any text left the customer's network, replace them with pseudonymous tokens, and reverse the substitution when the external model's response came back — a "linguistic air-lock." **No part of that mechanism exists.** The only real sanitization code, `service-slm/crates/slm-doorman/src/redact.rs`, is a plain regex-based **secret/credential redactor** — PEM private keys, AWS/GitHub/Slack tokens, generic bearer/API-key/secret/password patterns — and its own doc comment states it is "the only redaction surface in the apprenticeship pipeline," called exclusively when writing training-corpus tuples. It never runs on the path to an external model. A corpus-wide search for "PII," "pseudonym," "location identif," or any rehydration-table code returns zero hits anywhere in `service-slm`. Separately, the real Tier C client (`crates/slm-doorman/src/tier/external.rs`) documents "no live API calls in v0.1.x" and gates every call behind a compile-time allowlist that cannot be extended at runtime — so the routing this article describes as live today is not live at all yet, on top of never having had the sanitization step it claimed.

This is a compliance-relevant gap, not a cosmetic one. This article explicitly targets regulated-industry readers — real estate, financial advisory, clinics, law firms — evaluating the platform's actual privacy protections. The honest current answer: **when Tier C does go live, raw customer text will reach an external model unless a real PII-scrubbing mechanism is built first** — the credential redactor protects secrets, not customer data. What follows describes what's real today, not the retracted mechanism.

**AI routing**, as it actually exists, is the mechanism by which [[service-slm|`service-slm`]] — the [[doorman-protocol|Doorman]] — mediates every request that involves a language model, across three real compute tiers. [[service-slm|`service-slm`]] is confirmed as the sole boundary that holds external-model credentials and logs every call to the per-tenant audit ledger; no other component in the system holds external AI credentials or makes direct outbound calls to external language models. This part of the architecture is real and does what it claims — the gap is specifically the sanitization/rehydration layer, not the single-boundary design.

## What's real today

- **Three compute tiers, confirmed in `crates/slm-doorman/src/flow_policy.rs` and `lib.rs`**: Tier A (local), Tier B (Yo-Yo burst/GPU), Tier C (external API) as real routing targets (`RouteTarget::TierALocal`/`TierBNode`).
- **Model names**: Tier A runs `olmo-3-7b-instruct` locally; Tier B (Yo-Yo) defaults to `Olmo-3-1125-32B-Think`.
- **Tier C is not live.** `tier/external.rs` documents no live external API calls in this version; the client is wired only against a test mock, and every call is gated behind a fixed, compile-time allowlist.
- **Every proxied call is audit-logged** — confirmed in `audit_proxy.rs`, `lib.rs`, and `cost_ledger.rs` — with cost and response recorded to a real audit ledger.
- **Every request carries a mandatory tenant tag** (`ModuleId` in `slm-core`), confirmed real.
- **Not found in code**: a "tenant's configured budget cap" determining routing decisions — cost tracking and pricing config exist, but no explicit per-tenant budget gate on the routing decision itself was located.

## What is not real (retracted, not softened)

The sanitize-outbound / rehydrate-inbound pass; PII detection; location-identifier stripping; pseudonymous token substitution; a rehydration table of any kind. None of it exists in `service-slm`. Any future version of this article that reinstates language like "sanitizes sensitive information" or "masks PII" for the Tier C routing path needs a fresh code citation, not a restoration of this text.

## Applications — reframed as what the platform can honestly promise today

- **Editorial workflow**: TOPIC and GUIDE drafts that reach Tier C today do so through the fixed allowlist's narrow-precision tasks (see [[learning-datagraph-architecture]] for `draft_generate`'s real behavior) — not through any sanitization step, because none exists for this path.
- **Financial advisory / real estate / clinic / law-firm use** of Tier C: not yet a safe claim to make in this article's own terms, given the retraction above. Any of these use cases sending ledger records, client names, or property/owner records through Tier C today would reach the external model unredacted for PII. This should stay flagged until a real mechanism is built and independently verified, not implied as already solved.

## See also

- [[compounding-substrate]]
- [[worm-ledger-architecture]]
- [[decode-time-constraints]]
- [[machine-based-auth]]
- [[3-layer-stack]]
