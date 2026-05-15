---
schema: foundry-doc-v1
title: "service-slm — The Institutional Small Language Model"
slug: service-slm
category: services
type: concept
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-15
editor: pointsav-engineering
paired_with: service-slm.es.md
short_description: "service-slm is the language-model service of the PointSav family — a quantised, narrow Small Language Model that translates institutional intent into deterministic outputs and routes every AI inference call through the Doorman audit boundary."
cites: []
---

`service-slm` is the language-model service of the PointSav family. It is intentionally a Small Language Model — quantised, narrow, fast — rather than a frontier-scale model. Its job is not conversation. Its job is semantic translation: turning institutional intent (English commands, document content, taxonomy queries) into deterministic outputs (binary commands, `VALID`/`REJECT` decisions, Chart-of-Accounts socket assignments). It is invisible — there is no chat window, and the operator never types into `service-slm` directly. The surface above it presents a structured workflow; `service-slm` is the silent intermediary. This article covers the four operations, the three compute tiers, the Doorman audit boundary, and why a small model is a structural choice, not a cost compromise.

## What service-slm does

The service performs four operations in order of increasing institutional weight:

| Operation | Inputs | Output |
|---|---|---|
| Semantic command parsing | English intent from the F8 Terminal | Binary UDP command for `service-udp` |
| Gravity verification | 50-word Gravity Vector from `service-content` | `VALID` or `REJECT` single token |
| Socket assignment | Entity bundle from `service-extraction` + Chart of Accounts | Sovereign-ID with Chart-of-Accounts socket |
| Theme suggestion | Recurring patterns the Gravity Engine flags | Proposed new entries to the Themes Seed Vault (for operator approval) |

The model never publishes structured data autonomously. Every output transits a human-in-the-loop verification step before it can be written to a verified ledger.

## The three compute tiers

The same `service-slm` interface adapts to the host hardware through three execution modes:

| Tier | Where it runs | Model size | Use case |
|---|---|---|---|
| Local | Operator's workstation or `os-totebox` with ≥16 GB RAM | 1B–7B parameter quantised model loaded locally | Sovereign Iron Vault — institutional customers; no cloud egress |
| Yo-Yo | Operator-provisioned elastic GPU node | Larger model on rented hardware; data tunnelled via WireGuard | Cost-optimised heavy batch processing; node is torn down after the run |
| External API | Licensed third-party API endpoint | Frontier model | Last-resort routing for tasks where local capacity is insufficient |

All three tiers transit the Doorman audit boundary. No tier bypasses it.

## The Doorman boundary

The Doorman is the audit-routing checkpoint between `service-slm` and the rest of the system. Every prompt and every completion is captured before the response returns to the caller. The audit trail lives in the local per-tenant ledger and forms the institutional record of every AI decision.

The Doorman exists for three reasons:

1. **Regulatory.** ISO/IEC 42001 (AI Management System) requires an immutable log of AI-assisted decisions.
2. **Operational.** A self-healing system needs a corpus of its own past behaviour. The Doorman captures it.
3. **Sovereign.** No request reaches a third-party API without passing through a local boundary the operator controls.

## Model selection

The canonical local model is from the OLMo family (Apache 2.0 + Open Data Commons). Two profiles are available:

| Profile | Model | RAM target |
|---|---|---|
| Edge | OLMo-2-0425-1B-Instruct | ~2 GB |
| Standard | OLMo-3-1125-7B-Think-Q4_K_M | ~6 GB |

OLMo is preferred because it ships with fully-open weights and training-data documentation — a prerequisite for continued pre-training on an operator's own corpus, which is the long-term path to a domain-specialised institutional model.

## Why a small model

Frontier-scale models impose three costs `service-slm` cannot accept: they require cloud egress, they consume tens of gigabytes of RAM, and they cannot be audited in any meaningful sense. A 1B-parameter quantised model is sufficient for its one narrow task — translating institutional English into deterministic outputs — and fits inside the cost envelope of a $7 cloud node alongside a Totebox.

Specialisation, not scale, is the design principle.

## See also

- [[service-content]] — the upstream Gravity Engine; primary caller of service-slm for gravity verification
- [[os-network-admin]] — the F8 Terminal where semantic command parsing originates
- [[totebox-os]] — the Totebox that hosts service-slm in Sovereign Iron mode
- [[sys-adr-07]] — structured data never routes through AI; service-slm is the implementation of this boundary
- [[doorman-protocol]] — the Doorman audit-routing protocol in detail
