---
title: "The Language-Protocol Substrate"
slug: topic-language-protocol-substrate
category: architecture
status: pre-build
last_edited: 2026-04-27
editor: pointsav-engineering
cites:
  - ni-51-102
  - osc-sn-51-721
---

# The Language-Protocol Substrate

The substrate that makes editorial work in Foundry an audited,
per-tenant, forkable practice. It carries four families, eighteen
genre templates, and a four-service split that lets a customer
swap any single component without touching the rest. This article
explains what it does, why it exists, and how it composes with
the other Foundry substrates.

## What it does

The substrate provides four artefacts:

1. **A 4-family adapter taxonomy.** PROSE for long-form English,
   COMMS for short-form interpersonal, LEGAL for volume-gated
   formal documents, TRANSLATE as a meta-protocol layered on top
   of any other family.
2. **A genre-template registry.** Eighteen templates, each
   carrying its required sections, register parameters,
   bilingual-pair convention, frontmatter schema, and prompt
   scaffolding.
3. **A frontmatter validator.** Returns every per-genre rule
   violation in one pass rather than first-fail.
4. **A banned-vocabulary list.** Eight cross-genre prohibited
   terms that survive in marketing prose and have no place in
   precise writing.

These four artefacts ship as a Rust crate (`service-disclosure`)
that any Foundry component can consume. The Doorman composes the
templates into prompts at request time; the per-tenant
write-assistant validates inbound and outbound text against the
schema; the apprenticeship pipeline produces verdict-signed
training tuples on every editorial action.

## Why it exists

Hyperscaler writing assistants — Grammarly Business, Microsoft
365 Copilot, Google Workspace, Apple Intelligence Writing Tools
— share a posture: cloud-default, provider-rooted attestation,
customer text traverses the provider's network, and per-customer
voice profiles (when one exists) live with the provider. The
customer cannot fork the weights or run on owned metal.

The 80-95% wrapper-startup failure rate of 2023-2024 documents
what happens when the moat is a prompt on top of a frontier
model: there is no moat. Jasper raised at a $1.5 billion
valuation and faded once ChatGPT shipped equivalent capability
free; Foundry's posture rejects that path.

Foundry's leapfrog is composition, not invention. Existing
claims compose:

| Claim | What it adds |
|---|---|
| #15 | Continued-pretraining on a customer-owned base model |
| #21 | Role-conditioned cluster adapters |
| #22 | Adapter-composition algebra (`base ⊕ tenant ⊕ protocol`) |
| #25 | Citation graph as first-class substrate |
| #31 | Constrained-constitutional authoring (CFG decode-time) |
| #32 | Apprenticeship substrate (verdict-signed editorial training) |

Composed: **your data, your weights, your adapter, audited, on
your metal.** Hyperscalers structurally cannot offer this at SMB
economics because their unit economics require central training
and shared trust roots. SMB-scale per-tenant continued
pretraining + per-tenant adapter serving + per-tenant audit
ledger require sovereign substrate at the customer's end —
which is Foundry's three-tier flow.

## The four families

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

Five or more adapters per request crosses into multi-task
interference per the 2025 LoRA literature (LoRAX, S-LoRA,
TC-LoRA, LoRI). Foundry stays at three.

Register, brand voice, document sub-type, and target audience
live as prompt scaffolding rather than additional adapters. This
is the Writer Brand IQ pattern and the Jasper brand-voice
configuration — fewer adapters, richer scaffolding, retrieval
grounding, decode-time constraints. The 2026 industry consensus.

## The four-service split

The editorial-write path runs through four services. Each owns
one shape:

| Service | Shape | Owner cluster |
|---|---|---|
| `service-content` | Data — taxonomy ledger and knowledge graph | project-slm |
| `service-slm` | Inference — Doorman + tier routing + audit ledger | project-slm |
| `service-disclosure` | Schema — types, validators, CFG, templates | project-language |
| `service-proofreader` | Operational — request-shaped HTTP write-assistant | project-proofreader |

A customer can swap any one without touching the rest. Replace
`service-slm` with a customer-owned GPU host while keeping
`service-content` and `service-disclosure`. Replace
`service-content` with a Customer's existing knowledge graph
while keeping `service-slm`. The contract between services is
the only thing that needs to hold.

This matches Microsoft's synced-versus-federated-connector
framing, LangChain's swappable-retriever pattern, and
llama-agents' independently-deployable-microservice approach.
Foundry's contribution is the per-tenant audit ledger that
makes the substitution composable across regulatory contexts.

## Multi-tenant via moduleId namespacing

The standard 2024-2026 pattern, drawn from Pinecone, Microsoft
365 Copilot Semantic Index, and AWS Bedrock Knowledge Bases, is
namespace-per-tenant inside one service instance — not separate
per-tenant deployments.

For Foundry: ONE `service-content` instance per Foundry
deployment, with `moduleId` partitioning Woodfine + PointSav +
future tenants inside. Per-tenant siloed deployment is the
escalation path — when a customer needs key-management-per-
tenant or stronger isolation, they spin up their own Foundry
instance in their own substrate and get their own
`service-content` there.

This is the meaning of "tenant escalation happens at the
deployment boundary, not the service-naming boundary." The
service stays multi-tenant; the deployment topology grows
isolation when warranted.

## Forward-looking — the Apprenticeship pipeline

The substrate's day-1 training pipeline is described in `planned`
terms per `[ni-51-102]` continuous-disclosure language and the
forward-looking discipline of `[osc-sn-51-721]`. The shape is in
place; the operational throughput is what matures over time.

Eight editorial task-types are defined in the project-language
cluster manifest: `prose-edit`, `comms-edit`,
`frontmatter-normalize`, `citation-insert`, `register-tighten`,
`cross-link-verify`, `schema-validate`, `template-author`. Each
generates verdict-signed training tuples through the
apprenticeship-substrate pipeline (Doctrine claim #32). The
tuples feed continued pretraining on the customer's adapter
when corpus volume warrants.

The pipeline target: every editorial action a Foundry-shaped
deployment performs is one tuple of training data for the
customer's adapter. The customer's voice deepens over time
without their text ever leaving their substrate.

## See also

- [Style Guide — TOPIC](topic-style-guide-topic.md)
- [Style Guide — README](topic-style-guide-readme.md)
- [Customer Hostability](topic-customer-hostability.md)
- [Anti-Homogenization Discipline](topic-anti-homogenization-discipline.md)
- The convention this article reflects:
  `~/Foundry/conventions/language-protocol-substrate.md`
- The implementation:
  `pointsav-monorepo/service-disclosure/`
