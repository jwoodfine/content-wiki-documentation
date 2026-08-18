---
schema: foundry-doc-v1
title: "Learning Datagraph — SLM trajectory loop and apprenticeship queue"
slug: learning-datagraph-architecture
short_description: "Training loop turning operator interactions into training signal — trajectory capture, an apprenticeship queue, and a GLiNER→OLMo distillation pipeline that generates entity-extraction DPO pairs."
language: en
category: ai
type: topic
content_type: topic
index_group: entity-extraction-and-the-training-loop
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-08-17
editor: pointsav-engineering
cites: []
paired_with: learning-datagraph-architecture.es.md

---

The platform builds a [[compounding-substrate|compounding substrate]]: every operator interaction with an AI session becomes a structured training tuple, routed through a single auditable boundary ([[doorman-protocol|Doorman]]), captured to an [[worm-ledger-architecture|append-only ledger]], and folded back into the local SLM via periodic fine-tuning. The result is a development environment that learns from how it gets used — code completions improve toward the patterns this operator writes, draft suggestions align closer to the editorial voice this house produces, entity extractions tighten as the graph thickens.

## Key Takeaways

- The substrate accumulates training signal through several distinct mechanisms: trajectory capture at session end, an apprenticeship queue that fires on every commit, and a GLiNER→OLMo distillation pipeline that produces entity-extraction DPO pairs.
- All training signal passes through the same auditable boundary — [[doorman-protocol|Doorman]] — and lands in the append-only audit ledger. Graph queries made in this loop are tenant-scoped at that same boundary.
- Corpus-size figures (tuple counts, pair counts) change too often to publish a reliable number here.
- `POST /v1/draft/generate` is real, built, and live. Its own doc comment calls it the "Tier C Drafting Pipeline" and it proxies to **Claude Haiku 4.5**.

## Training signal mechanisms

**Trajectory capture.** A session-end hook fires at session close and posts a free-text session summary wrapped in an apprenticeship-brief JSON schema (`brief_id`/`senior_role`/`task_type`/`body`).

**Apprenticeship queue.** A post-commit hook fires a shadow brief for commits across 8 clusters. The local model in this loop is **OLMo 3**.

**The DPO mechanism is GLiNER→OLMo distillation.** GLiNER (Tier 0 extraction) proposes entities, OLMo 7B (Tier A) is asked to reproduce or improve on the extraction, and the delta becomes a DPO pair — an entity-extraction-quality signal, distinct from editorial-voice training.

**Negative-trajectory distillation.** An inbox-scanner script reads operator corrections from archived messages and emits negative-trajectory signals to the feedback corpus.

## The structured-entity loop, and its tenant-scoping behavior

`POST /v1/draft/generate` grounds generation in graph entities — it queries the graph and an induced edge subgraph before calling out. What it does **not** do: call a LoRA scheduler or wake Tier B GPU compute. It is a synchronous Doorman audit-proxy call to a cloud model (Claude Haiku 4.5, see above), full stop.

Every graph query this endpoint makes is subject to the same tenant-isolation enforcement described in [[doorman-protocol]] — `graph_query`/`graph_mutate` scope strictly to the caller's own module, with no cross-tenant merge. A structured-entity draft for one tenant cannot ground itself in another tenant's graph entities, so a customer's graph IP never aggregates across tenants without opt-in.

The substrate compounds in two directions in principle. Structurally, citation density and supersedence chains thicken with each draft. Generatively, each adapter raises the floor of "raw" so refinement starts closer to publish-ready — that generative half depends on the LoRA training pipeline described in [[elastic-compute-lora-training-pipeline]].

## See also

- [[compounding-substrate]] — the substrate discipline this architecture instantiates
- [[service-slm]] — the local SLM service that executes model inference in the loop
- [[totebox-session]] — the session model that trajectory capture instruments at session end
- [[mailbox-atomicity]] — the atomic prepend discipline that protects the audit ledger from concurrent write races
