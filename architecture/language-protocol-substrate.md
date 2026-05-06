---
schema: foundry-doc-v1
title: "The Language-Protocol Substrate"
slug: language-protocol-substrate
category: architecture
type: topic
quality: complete
short_description: "The Language-Protocol Substrate is the Foundry editorial infrastructure that provides four adapter families, eighteen genre templates, a frontmatter validator, and a banned-vocabulary list, making editorial work a per-tenant, audited, and forkable practice."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-04-30
editor: pointsav-engineering
cites:
  - ni-51-102
  - osc-sn-51-721
paired_with: language-protocol-substrate.es.md
---

# The Language-Protocol Substrate

> The Language-Protocol Substrate is the Foundry editorial infrastructure that provides four adapter families, eighteen genre templates, a frontmatter validator, and a banned-vocabulary list, making editorial work a per-tenant, audited, and forkable practice.

**The Language-Protocol Substrate** is a cross-cutting architecture pattern in the Foundry platform. It carries four families, eighteen genre templates, and a four-service split that lets a customer replace any single component without touching the rest. The substrate makes editorial work in Foundry an audited, per-tenant, forkable practice by encoding register, brand voice, document sub-type, and target audience as reusable prompt scaffolding rather than ad-hoc instruction. This article explains what it does, why it exists, and how it composes with the other Foundry substrates.

## Overview

The substrate provides four artefacts:

1. **A 4-family adapter taxonomy.** PROSE for long-form English, COMMS for short-form interpersonal, LEGAL for volume-gated formal documents, TRANSLATE as a meta-protocol layered on top of any other family.
2. **A genre-template registry.** Eighteen templates, each carrying its required sections, register parameters, bilingual-pair convention, frontmatter schema, and prompt scaffolding.
3. **A frontmatter validator.** Returns every per-genre rule violation in one pass rather than first-fail.
4. **A banned-vocabulary list.** Eight cross-genre prohibited terms that survive in marketing prose and have no place in precise writing.

These four artefacts ship as a Rust crate (`service-disclosure`) that any Foundry component can consume. The Doorman composes the templates into prompts at request time; the per-tenant write-assistant validates inbound and outbound text against the schema; the apprenticeship pipeline produces verdict-signed training tuples on every editorial action.

## Ring and Role

The Language-Protocol Substrate spans Ring 3 — Optional Intelligence (inference via the Doorman) and Ring 2 — Knowledge and Processing (schema validation and template management via `service-content` and `service-disclosure`). It has no Ring 1 component: editorial work begins after boundary ingest completes. The substrate is activated on every editorial action that passes through the Doorman, whether that action is a document generation request, a validation pass, or a training-tuple capture.

## Architecture

### The four families

| Family | Generation responsibility | Templates |
|---|---|---|
| **PROSE** | Long-form English prose | README (workspace / repo / project), TOPIC, GUIDE, MEMO, ARCHITECTURE, INVENTORY, license-explainer, CHANGELOG |
| **COMMS** | Short-form interpersonal | email, chat, ticket comment, meeting notes |
| **LEGAL** | Volume-gated formal | contract, CLA, policy, terms (default-routes to Tier C) |
| **TRANSLATE** | Meta-protocol | Operates over the other families; not a separate generation track |

Three adapters compose at request time:

```
composed_weights =
    base_model
    ⊕ tenant_adapter[<tenant_id>]      // brand voice
    ⊕ protocol_adapter[PROSE | COMMS | LEGAL | TRANSLATE]
```

Five or more adapters per request crosses into multi-task interference per the 2025 LoRA literature (LoRAX, S-LoRA, TC-LoRA, LoRI). Foundry stays at three.

Register, brand voice, document sub-type, and target audience live as prompt scaffolding rather than additional adapters. This is the Writer Brand IQ pattern and the Jasper brand-voice configuration — fewer adapters, richer scaffolding, retrieval grounding, decode-time constraints. The 2026 industry consensus.

### The four-service split

The editorial-write path runs through four services. Each owns one shape:

| Service | Shape | Owner cluster |
|---|---|---|
| `service-content` | Data — taxonomy ledger and knowledge graph | project-slm |
| `service-slm` | Inference — Doorman, tier routing, audit ledger | project-slm |
| `service-disclosure` | Schema — types, validators, CFG, templates | project-language |
| `service-proofreader` | Operational — request-shaped HTTP write-assistant | project-proofreader |

A customer can replace any one without touching the rest. Replace `service-slm` with a customer-owned GPU host while keeping `service-content` and `service-disclosure`. Replace `service-content` with a customer's existing knowledge graph while keeping `service-slm`. The contract between services is the only thing that needs to hold.

This matches Microsoft's synced-versus-federated-connector framing, LangChain's swappable-retriever pattern, and llama-agents' independently-deployable-microservice approach. Foundry's contribution is the per-tenant audit ledger that makes the substitution composable across regulatory contexts.

### Multi-tenant via moduleId namespacing

The standard 2024–2026 pattern, drawn from Pinecone, Microsoft 365 Copilot Semantic Index, and AWS Bedrock Knowledge Bases, is namespace-per-tenant inside one service instance — not separate per-tenant deployments.

For Foundry: one `service-content` instance per Foundry deployment, with `moduleId` partitioning Woodfine, PointSav, and future tenants inside. Per-tenant isolated deployment is the escalation path — when a customer needs key-management-per-tenant or stronger isolation, they spin up their own Foundry instance in their own substrate and get their own `service-content` there.

This is the meaning of "tenant escalation happens at the deployment boundary, not the service-naming boundary." The service stays multi-tenant; the deployment topology grows isolation when warranted.

## Configuration

Eight editorial task-types are defined in the project-language cluster manifest: `prose-edit`, `comms-edit`, `frontmatter-normalize`, `citation-insert`, `register-tighten`, `cross-link-verify`, `schema-validate`, `template-author`. Each generates verdict-signed training tuples through the apprenticeship-substrate pipeline (Doctrine claim #32). The tuples feed continued pretraining on the customer's adapter when corpus volume warrants.

Per `[ni-51-102]` continuous-disclosure language and in accordance with the forward-looking information principles of `[osc-sn-51-721]`, the substrate's training pipeline is described in planned terms. The shape is in place; the operational throughput is what matures over time. The pipeline target: every editorial action a Foundry-shaped deployment performs is one tuple of training data for the customer's adapter. The customer's voice deepens over time without their text leaving their substrate.

## See Also

- [[style-guide-topic]]
- [[style-guide-readme]]
- [[customer-hostability]]
- [[anti-homogenization-discipline]]
- [[apprenticeship-substrate]]

## References

- `~/Foundry/conventions/language-protocol-substrate.md` — the convention this article reflects
- `pointsav-monorepo/service-disclosure/` — the implementation crate
- DOCTRINE.md Claims #21, #22, #25, #31, #32 — the composition claims this substrate realises
- `[ni-51-102]` — NI 51-102 Continuous Disclosure Obligations
- `[osc-sn-51-721]` — OSC Staff Notice 51-721 Forward-Looking Information Disclosure


---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*

*Woodfine Capital Projects™, Woodfine Management Corp™, PointSav Digital Systems™, Totebox Orchestration™, and Totebox Archive™ are trademarks of Woodfine Capital Projects Inc., used in Canada, the United States, Latin America, and Europe. All other trademarks are the property of their respective owners.*
