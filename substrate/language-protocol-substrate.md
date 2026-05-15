---
schema: foundry-doc-v1
title: "The Language-Protocol Substrate"
slug: language-protocol-substrate
category: substrate
type: topic
quality: complete
short_description: "The editorial infrastructure that encodes register, brand voice, document sub-type, and target audience as reusable prompt scaffolding — four adapter families, eighteen genre templates, a frontmatter validator, and a four-service split that lets a customer replace any single component without touching the rest."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-15
editor: pointsav-engineering
cites:
 - ni-51-102
 - osc-sn-51-721
paired_with: language-protocol-substrate.es.md
---

Every editorial action that passes through the PointSav platform — document generation, schema validation, training-tuple capture — is shaped by a substrate that encodes register, brand voice, document sub-type, and target audience as reusable prompt scaffolding rather than ad-hoc instruction. The result is editorial work that is audited, per-tenant, and replaceable at any layer without rebuilding the rest.

The substrate provides four artefact families, eighteen genre templates, a frontmatter validator that returns all schema violations in a single pass, and a banned-vocabulary list of eight cross-genre prohibited terms. These ship as a Rust crate (`service-disclosure`) split across four services — `service-content` (knowledge graph), `service-slm` (Doorman and inference), `service-disclosure` (schema and templates), `service-proofreader` (HTTP write-assistant) — where any single service can be replaced by a customer-owned equivalent while the rest hold.

Three adapters compose at request time: base model, tenant adapter (brand voice), and protocol adapter (PROSE | COMMS | LEGAL | TRANSLATE). Register, brand voice, and target audience live as prompt scaffolding rather than additional adapters — five or more adapters per request crosses into multi-task interference per the 2025 LoRA literature; the platform stays at three. Every editorial action produces a verdict-signed training tuple through the [[apprenticeship-substrate]] pipeline, feeding continued pretraining on the customer's adapter without the customer's text leaving their infrastructure.

For regulated buyers, the four-service split matters because every editorial action is audited in the per-tenant ledger before it exits the customer's network. The customer can fork any adapter, inspect the prompt scaffolding, and verify that their brand voice is not pooled with another tenant's training data. Per `[ni-51-102]` and `[osc-sn-51-721]`, the training pipeline is described in planned terms; the substrate architecture is operational today.

## Overview

The substrate provides four artefacts:

1. **A 4-family adapter taxonomy.** PROSE for long-form English, COMMS for short-form interpersonal, LEGAL for volume-gated formal documents, TRANSLATE as a meta-protocol layered on top of any other family.
2. **A genre-template registry.** Eighteen templates, each carrying its required sections, register parameters, bilingual-pair convention, frontmatter schema, and prompt scaffolding.
3. **A frontmatter validator.** Returns every per-genre rule violation in one pass rather than first-fail.
4. **A banned-vocabulary list.** Eight cross-genre prohibited terms that survive in marketing prose and have no place in precise writing.

These four artefacts ship as a Rust crate (`service-disclosure`) that any platform component can consume. The Doorman composes the templates into prompts at request time; the per-tenant write-assistant validates inbound and outbound text against the schema; the apprenticeship pipeline produces verdict-signed training tuples on every editorial action.

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
  ⊕ tenant_adapter[<tenant_id>] // brand voice
  ⊕ protocol_adapter[PROSE | COMMS | LEGAL | TRANSLATE]
```

Five or more adapters per request crosses into multi-task interference per the 2025 LoRA literature (LoRAX, S-LoRA, TC-LoRA, LoRI). The platform stays at three.

Register, brand voice, document sub-type, and target audience live as prompt scaffolding rather than additional adapters. Fewer adapters, richer scaffolding, retrieval grounding, decode-time constraints — this is the 2026 industry consensus for production editorial systems.

### The four-service split

The editorial-write path runs through four services. Each owns one shape:

| Service | Shape | Owner cluster |
|---|---|---|
| `service-content` | Data — taxonomy ledger and knowledge graph | project-slm |
| `service-slm` | Inference — Doorman, tier routing, audit ledger | project-slm |
| `service-disclosure` | Schema — types, validators, CFG, templates | project-language |
| `service-proofreader` | Operational — request-shaped HTTP write-assistant | project-proofreader |

A customer can replace any one without touching the rest. Replace `service-slm` with a customer-owned GPU host while keeping `service-content` and `service-disclosure`. Replace `service-content` with a customer's existing knowledge graph while keeping `service-slm`. The contract between services is the only thing that needs to hold.

The platform's contribution to this pattern is the per-tenant audit ledger that makes each substitution composable across regulatory contexts — a replacement service produces the same audit trail the original produced.

### Multi-tenant via moduleId namespacing

One `service-content` instance per platform deployment, with `moduleId` partitioning tenants inside. Per-tenant isolated deployment is the escalation path — when a customer needs key-management-per-tenant or stronger isolation, they spin up their own platform instance in their own infrastructure and get their own `service-content` there.

This is the meaning of "tenant escalation happens at the deployment boundary, not the service-naming boundary." The service stays multi-tenant; the deployment topology grows isolation when warranted.

## Configuration

Eight editorial task-types are defined in the platform's editorial cluster manifest: `prose-edit`, `comms-edit`, `frontmatter-normalize`, `citation-insert`, `register-tighten`, `cross-link-verify`, `schema-validate`, `template-author`. Each generates verdict-signed training tuples through the [[apprenticeship-substrate]] pipeline. The tuples feed continued pretraining on the customer's adapter when corpus volume warrants.

Per `[ni-51-102]` continuous-disclosure language and in accordance with the forward-looking information principles of `[osc-sn-51-721]`, the substrate's training pipeline is described in planned terms. The shape is in place; the operational throughput is what matures over time. The pipeline target: every editorial action a customer deployment performs is one tuple of training data for the customer's adapter. The customer's voice deepens over time without their text leaving their infrastructure.

## See also

- [[style-guide-topic]]
- [[customer-hostability]]
- [[anti-homogenization-discipline]]
- [[apprenticeship-substrate]]
- [[citation-substrate]]
