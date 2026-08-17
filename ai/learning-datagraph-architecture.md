---
schema: foundry-doc-v1
title: "Learning Datagraph — SLM trajectory loop and apprenticeship queue"
slug: learning-datagraph-architecture
short_description: "Training loop turning operator interactions into training signal — trajectory capture, apprenticeship queue, and a real GLiNER→OLMo distillation pipeline (not the editorial DPO leg earlier versions of this article described)."
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

- The substrate accumulates training signal through several distinct mechanisms: trajectory capture at session end, an apprenticeship queue that fires on every commit, and a real GLiNER→OLMo distillation pipeline — not the "editorial reverse-funnel DPO" leg earlier versions of this article described, which has no support in the codebase.
- All training signal passes through the same auditable boundary — [[doorman-protocol|Doorman]] — and lands in the append-only audit ledger. The graph-tenant-scoping behavior described below is a real example of that boundary being enforced, not just described.
- Specific corpus-size figures (tuple counts, pair counts) are not repeated here — the only figures verified against real code are dated 2026-04-29 and already stale (14 apprenticeship files, an empty feedback corpus); a fresher-sounding but unverified number would be worse than none.
- `POST /v1/draft/generate` is real, built, and live — `service-content/src/http.rs:352-479` (not the previously-cited `176-280`), confirmed by direct read, not a live probe's status code alone. Its own doc comment calls it the "Tier C Drafting Pipeline" and proxies to **Claude Haiku 4.5** (`anthropic:claude-haiku-4-5-20251001`) — not Claude 3.5 Sonnet as an earlier correction claimed. No `service-content/CLAUDE.md` exists anywhere in the monorepo; that citation and the model-version claim do not correspond to anything in the codebase.

## Training signal mechanisms

**Trajectory capture.** A session-end hook fires at session close. The real `capture-trajectory.sh` posts a free-text session summary wrapped in an apprenticeship-brief JSON schema (`brief_id`/`senior_role`/`task_type`/`body`) — not a fixed field set of branch-state/uncommitted-file-count/head-SHA as earlier text claimed.

**Apprenticeship queue.** A post-commit hook fires a shadow brief via `POST /v1/shadow` for commits across 8 clusters — the specific "15-minute drainer" interval in earlier text has no support in the code or in `service-slm/docs/trainer-scoping.md`, the closest real documentation of this mechanism. The local model in this loop is **OLMo 3** (`OLMo-3-7B-Q4_K_M.gguf`, `slm-doorman/src/tier/local.rs`; also `olmo-3-1125-7b-q4` in `slm-core/src/apprenticeship.rs`) — not "OLMo-2 7B Q4"; no reference to an OLMo-2 model exists anywhere in the codebase.

**The real DPO mechanism is GLiNER→OLMo distillation, not editorial reverse-funnel pairs.** `service-content/src/lib.rs` (`write_gliner_olmo_dpo_pair`, around lines 279–282 and 659–690) shows the actual DPO pipeline: GLiNER (Tier 0 extraction, `:9085`) proposes entities, OLMo 7B (Tier A) is asked to reproduce or improve on the extraction, and the delta becomes a DPO pair — an entity-extraction-quality signal, not an editorial-voice signal from a "raw → refined → creative-edited" pipeline. No such reverse-funnel-to-DPO-pair mechanism exists in the code; earlier text describing one was not grounded in the codebase.

**Negative-trajectory distillation.** An inbox-scanner script reads operator corrections from archived messages and emits negative-trajectory signals to the feedback corpus. Carried forward as previously described; unlike the other three mechanisms above, this one has not been independently checked against the current codebase.

## The structured-entity loop, and the tenant-scoping behavior it actually has

`POST /v1/draft/generate` genuinely grounds generation in graph entities — it queries `state.graph.query_context` and an induced edge subgraph before calling out, matching the "grounds generation in graph entities" description. What it does **not** do: call a LoRA scheduler or wake Tier B GPU compute. Earlier text claimed "a LoRA scheduler then wakes Tier B GPU compute for nightly adapter training" downstream of this endpoint — no such wiring exists in `draft_generate`; it is a synchronous Doorman `/v1/audit/proxy` call to a cloud model (Claude Haiku 4.5, see above), full stop.

**Not previously documented at all, despite being load-bearing:** every graph query this endpoint makes is subject to the same tenant-isolation enforcement described in [[doorman-protocol]] — `graph_query`/`graph_mutate` scope strictly to the caller's own module, no cross-tenant merge, since the fix confirmed live 2026-07-28. A structured-entity draft for one tenant cannot ground itself in another tenant's graph entities. This matters for exactly the DOCTRINE claim #48 reason [[doorman-protocol]] covers in more depth — customer-owned graph IP never aggregates across tenants without opt-in — and applies here even though nothing in this article's earlier text ever mentioned it.

The substrate compounds in two directions in principle. Structurally, citation density and supersedence chains thicken with each draft. Generatively, each adapter raises the floor of "raw" so refinement starts closer to publish-ready — but that generative half depends on the LoRA training pipeline described in [[elastic-compute-lora-training-pipeline]], which this article does not itself verify.

## See also

- [[compounding-substrate]] — the substrate discipline this architecture instantiates
- [[service-slm]] — the local SLM service that executes model inference in the loop
- [[totebox-session]] — the session model that trajectory capture instruments at session end
- [[mailbox-atomicity]] — the atomic prepend discipline that protects the audit ledger from concurrent write races
