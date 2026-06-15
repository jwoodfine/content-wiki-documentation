---
schema: foundry-doc-v1
title: "Institutional small language model"
slug: service-slm
category: services
type: concept
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-22
editor: pointsav-engineering
paired_with: service-slm.es.md
short_description: "service-slm is the language-model service of the PointSav family — a quantised, narrow Small Language Model that translates institutional intent into deterministic outputs and routes every AI inference call through the Doorman audit boundary."
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

An AI request that leaves the building cannot be audited and cannot be recalled. The moment institutional intent reaches a frontier model in another company's cloud, the organization has surrendered both the record of the decision and control over it.

<!--claim id=small-by-design confidence=structural cites=[]-->`service-slm` is the language-model service of the PointSav family. It is deliberately a Small Language Model — quantised, narrow, fast — and its job is not conversation but semantic translation: turning institutional intent into deterministic outputs.<!--/claim-->

<!--claim id=doorman-transit confidence=structural cites=[]-->The service runs in three compute tiers, and every inference call — local, burst, or external — transits the [[doorman-protocol|Doorman]] audit boundary, where each prompt and completion is captured to the per-tenant [[worm-ledger-design|ledger]] before the response returns.<!--/claim-->

For a regulated buyer the consequence is concrete. No AI decision is unlogged, and no request reaches a third-party API without crossing a boundary the operator controls. This article covers the four operations, the three compute tiers, the Doorman boundary, and why a small model is a structural choice rather than a cost compromise.

## What service-slm does

The service is invisible — there is no chat window, and the operator never types into `service-slm` directly. The surface above it presents a structured workflow; `service-slm` is the silent intermediary. It performs four operations, in order of increasing institutional weight.

| Operation | Inputs | Output |
|---|---|---|
| Semantic command parsing | English intent from the F8 Terminal | Binary UDP command for `service-udp` |
| Gravity verification | 50-word Gravity Vector from [[service-content]] | `VALID` or `REJECT` single token |
| Socket assignment | Entity bundle from [[service-extraction]] + [[archetypes-and-chart-of-accounts|Chart of Accounts]] | Sovereign-ID with Chart-of-Accounts socket |
| Theme suggestion | Recurring patterns the Gravity Engine flags | Proposed new entries to the Themes Seed Vault, for operator approval |

<!--claim id=no-autonomous-publish confidence=structural cites=[]-->The model never publishes structured data autonomously. Every output transits a human-in-the-loop verification step before it can be written to a verified ledger.<!--/claim-->

## The three compute tiers

The same `service-slm` interface adapts to the host hardware through three execution modes.

| Tier | Where it runs | Model size | Use case |
|---|---|---|---|
| Local | Operator workstation or [[totebox-os|`os-totebox`]] with at least 16 GB RAM | 1B–7B-parameter quantised model loaded locally | Sovereign Iron Vault — institutional customers; no cloud egress |
| Elastic burst | Operator-provisioned ephemeral GPU node | Larger model on rented hardware; data tunnelled over an encrypted link | Cost-optimised heavy batch processing; the node is torn down after the run |
| External API | Licensed third-party API endpoint | Frontier model | Last-resort routing for tasks where local capacity is insufficient |

<!--claim id=no-tier-bypass confidence=structural cites=[]-->All three tiers transit the Doorman audit boundary. No tier bypasses it.<!--/claim-->

## The Doorman boundary

The Doorman is the audit-routing checkpoint between `service-slm` and the rest of the system. Every prompt and every completion is captured before the response returns to the caller. The audit trail lives in the local per-tenant ledger and forms the institutional record of every AI decision.

The Doorman exists for three reasons.

1. **Regulatory.** ISO/IEC 42001, the AI management-system standard [^1], requires an immutable log of AI-assisted decisions.
2. **Operational.** A self-healing system needs a corpus of its own past behaviour; the Doorman captures it.
3. **Sovereign.** No request reaches a third-party API without passing through a local boundary the operator controls.

## Model selection

<!--claim id=olmo-canonical cites=[olmo3-allenai] confidence=established-->The canonical local model is from the OLMo family, which ships with fully open weights and training-data documentation [^2].<!--/claim--> Open weights and documented training data are a prerequisite for continued pre-training on an operator's own corpus — the long-term path to a domain-specialised institutional model.

| Profile | Model | RAM target |
|---|---|---|
| Edge | OLMo-2-0425-1B-Instruct | ~2 GB |
| Standard | OLMo-3-1125-7B-Think-Q4_K_M | ~6 GB |

## Why a small model

<!--claim id=small-model-rationale confidence=structural cites=[]-->A frontier-scale model imposes three costs `service-slm` cannot accept: it requires cloud egress, it consumes tens of gigabytes of RAM, and it cannot be audited in any meaningful sense. A 1B-parameter quantised model is sufficient for the one narrow task — translating institutional English into deterministic outputs — and fits inside the cost envelope of a low-cost cloud node alongside a Totebox.<!--/claim-->

Specialisation, not scale, is the design principle.

## See also

- [[service-content]] — the upstream Gravity Engine; primary caller of service-slm for gravity verification
- [[os-network-admin]] — the F8 Terminal where semantic command parsing originates
- [[totebox-os]] — the Totebox that hosts service-slm in Sovereign Iron mode
- [[architecture-decisions|SYS-ADR-07]] — structured data never routes through AI; service-slm implements this boundary
- [[doorman-protocol]] — the Doorman audit-routing protocol in detail
- [[run-local-slm-inference]] — step-by-step guide: start the SLM service and submit inference requests from the console or API
- [[run-first-slm-query]] — step-by-step guide: read the Doorman health dashboard and submit your first prompt
