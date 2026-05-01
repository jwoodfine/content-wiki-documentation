---
schema: foundry-doc-v1
title: "The Language-Protocol Substrate"
slug: topic-language-protocol-substrate
category: architecture
type: topic
quality: published
short_description: The editorial infrastructure that makes writing in a PointSav deployment an audited, per-tenant, forkable practice — a four-family adapter taxonomy, genre templates, and a compounding training pipeline that compounds the per-tenant voice over time.
status: pre-build
last_edited: 2026-05-01
editor: pointsav-engineering
cites:
  - constitutional-ai-2212-08073
  - federated-lora-2502-05087
  - lorax-predibase
  - olmo3-allenai
  - s-lora-2024
paired_with: topic-language-protocol-substrate.es.md
---

The **Language-Protocol Substrate** is the architecture that makes editorial work in a PointSav deployment structured, per-tenant, and auditable. It defines a four-family adapter taxonomy for language generation, a set of genre templates delivered as prompt scaffolding at request time, a service split that keeps data, inference, and operational concerns in separate components, and a training pipeline whose output compounds with each editorial action the tenant takes.

## Why this exists

Cloud writing assistants typically route customer text through provider infrastructure, train on provider models, and store per-customer voice profiles at the provider. When a customer leaves, the model leaves with the provider. The per-customer voice evaporates. The audit trail of what the AI wrote on the customer's behalf is inaccessible.

The Language-Protocol Substrate inverts these properties. Per-tenant LoRA adapters are trained on the customer's own corpus, held on the customer's own hardware, and portable if the customer moves. The audit ledger of every editorial AI call is owned by the customer. The substrate ships as four composable services the customer can run independently, swap individually, or fork entirely.

## The four-family adapter taxonomy

Production multi-LoRA infrastructure supports up to three adapters per request before multi-task interference degrades quality. The substrate's taxonomy is designed around this constraint:

| Family | Generation responsibility |
|---|---|
| **PROSE** | Long-form English prose — READMEs, TOPICs, GUIDEs, memos, architecture documents, changelogs |
| **COMMS** | Short-form interpersonal — email, chat, ticket comments, meeting notes |
| **LEGAL** | Volume-gated; routes to Tier C (external API via Doorman) unless per-tenant legal corpus justifies a dedicated adapter |
| **TRANSLATE** | Meta-protocol; transforms the output of any other family across a language pair or register shift |

At request time the Doorman composes three adapter layers:

```
composed_weights =
    base_model[OLMo 1B or 32B]
    ⊕ tenant_adapter[<tenant_id>]
    ⊕ protocol_adapter[PROSE | COMMS | LEGAL | TRANSLATE]
```

Register, brand voice, document sub-type, channel formality, and target audience all live as **prompt scaffolding** — structured prompt fragments composed at request time — rather than as additional adapters.

## Genre templates

Each genre template is a structured prompt fragment that the Doorman composes at request time. Templates carry required sections, a banned-vocabulary list (terms such as "leverage," "seamless," "next-generation," "cutting-edge" are prohibited across all genres), register parameters (target reading level, sentence-length budget, active/passive preference), the bilingual-pair convention (English canonical plus Spanish overview), and frontmatter schema requirements (citations, license, forward-looking flag).

Templates are versioned. They live in `service-disclosure` and are served by the Doorman at request time so that every request automatically receives the current schema constraints.

## The service split

Four services compose the substrate. Each has a distinct contract and can be deployed, swapped, or replaced independently:

- **`service-content`** — data substrate; the per-tenant knowledge graph, taxonomy ledger, embeddings, and indexes. Multi-tenant via `moduleId` namespacing inside one instance per deployment.
- **`service-slm`** — inference router; the Doorman, Tier A local model, Tier B GPU burst, and Tier C external API allowlist. Enforces sanitise-outbound and audit-ledger discipline on every call.
- **`service-disclosure`** — schema and constraint substrate; TOPIC/GUIDE/README schemas as Rust types, banned-vocabulary context-free grammar, genre template registry, frontmatter validators. Library-shaped; consumed by `service-proofreader` as a Cargo dependency.
- **`service-proofreader`** — operational write-assistant; text in, improved text out, diff displayed. Consumes `service-slm`, `service-content`, and `service-disclosure` at request time.

A customer who wants to replace their inference backend replaces `service-slm` while keeping the other three unchanged. A customer who wants to extend the schema for a new document genre edits `service-disclosure` without touching inference or data.

## AI-garbage prevention

The substrate addresses four documented failure modes in AI writing systems:

**Register collapse.** AI suggestions can silently coerce writers toward a homogenised Western register. The substrate's default is flag-and-display rather than auto-rewrite. The per-tenant adapter preserves the customer's voice. Protocol selection is explicit, not auto-detected.

**Hallucinated legal citations.** The LEGAL protocol disables citation generation. Factual claims route to an explicit citation-check step drawing only from `citations.yaml`. The substrate never invents a citation.

**Customer-text training.** The deployment MANIFEST explicitly prohibits training on tenant text without opt-in. The Doorman's audit trail records every call. Constrained decoding prevents tenant-text leakage at generation time.

**Wrapper-startup failure.** The substrate's moat is per-tenant adapter plus customer-owned weights plus on-customer-substrate compute — the structural properties that prompt-only wrappers lack.

## The editorial gateway role

At workspace v0.1.31, the Language-Protocol Substrate's operational expression — `service-language` — became the editorial gateway for all of Foundry's wiki and documentation output. Drafts from Task, Root, and Master sessions stage to `drafts-outbound/` directories. `project-language` sweeps those drafts, applies the substrate's constraints (banned-vocabulary grammar, citation registry resolution, bilingual pair generation, BCSC forward-looking discipline), and hands refined output to the appropriate destination repository.

The two-stage DPO loop closes over time: Stage 1 captures structural correctness from the apprenticeship substrate; Stage 2 captures editorial craft from Creative Contributor edits at the end of the cycle. Quarterly OLMo continued pretraining on the combined corpus means the substrate-generated baseline converges toward the combined standard of structure and craft. Creative incremental load drops as the baseline improves; Creative leverage grows.

## Customer-hostability

Every component ships with a bootstrap script. The customer's per-tenant adapters live in `data/adapters/<tenant>.safetensors` on the customer's own hardware, trained on the customer's own corpus, never transmitted outside customer-controlled storage. The audit ledger is owned by the customer and anchored to the customer's signing key. The stack can be taken and operated independently of any vendor relationship.

## Implementation state

`service-disclosure` scaffold, genre template registry, and apprenticeship corpus directory tree are planned for initial phases of the `project-language` cluster. `service-proofreader` and `app-console-proofreader` are operational at `proofreader.woodfinegroup.com`. Yo-Yo training pipeline scripts are a longer-horizon item. The constrained-decoding upgrade that would allow the Doorman to enforce banned-vocabulary grammar at decode time (rather than post-hoc) depends on the AS-2 integration work in the `project-slm` cluster.

## See Also

- [[compounding-doorman]] — the inference boundary the substrate routes through
- [[apprenticeship-substrate]] — the training mechanism the substrate extends to editorial work
- [[topic-adapter-composition]] — the algebra that makes three-adapter composition work
- [[topic-disclosure-substrate]] — the wiki-as-disclosure-record framing that depends on this substrate's output quality

## References

1. Constitutional AI: Harmlessness from AI Feedback, Bai et al., arXiv 2212.08073.
2. Federated LoRA, arXiv 2502.05087.
3. LoRAX — Predibase multi-LoRA inference server.
4. OLMo 3 — Allen Institute for AI, Apache 2.0.
5. S-LoRA — scalable serving of thousands of concurrent LoRA adapters.

---

## Provenance

Source material: `conventions/language-protocol-substrate.md` (ratified 2026-04-27, doctrine v0.0.8). Disciplines applied: no body H1; structural positioning (competitor products removed by name; capability contrast retained structurally); BCSC forward-looking framing on constrained-decoding upgrade and training pipeline (planned/depends on); banned-vocabulary pass; workspace-internal operational details stripped.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
