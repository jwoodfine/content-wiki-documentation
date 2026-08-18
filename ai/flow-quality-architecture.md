---
schema: foundry-doc-v1
title: "Knowledge flow: training loop and ontological DataGraph"
slug: flow-quality-architecture
category: ai
type: concept
content_type: topic
quality: complete
index_group: entity-extraction-and-the-training-loop
status: active
audience: vendor-public
bcsc_class: planned
language_protocol: PROSE-TOPIC
last_edited: 2026-08-17
editor: editorial
short_description: "Quality framework for the Totebox knowledge flow, asking whether LoRA adapters measurably improve the model and whether the DataGraph is an accurate ontology."
paired_with: flow-quality-architecture.es.md
cites: []

---

The Totebox knowledge flow turns prose into two durable assets: an [[ontological-datagraph|ontological DataGraph]] of entities, and LoRA adapters that specialise a local language model. Both are served by `service-slm` (the [[doorman-protocol|Doorman]]) and `service-content` (the DataGraph).

```
prose ─▶ service-extraction ─▶ CORPUS_*.json
      ─▶ service-content ──▶ GLiNER Tier 0 (fast — no published figure; qualitatively "~150x faster than OLMo") ─▶ entity spans
                         └──▶ OLMo Tier A (fallback, latency not published) ─▶ extraction fallback (Tier 0 unreachable) + async training-pass job
                         └──▶ GPU Tier B (enrichment) ─▶ role/location vectors
                         └──▶ LadybugDB graph
      ◀── Doorman queries the graph for context before each inference ◀──
training corpus (git-commit shadow tuples + Tier-A-vs-B enrichment pairs)
      ─▶ TRL SFT / DPO ─▶ PEFT adapter
```

The Tier-0-success path enqueues a `TierAJob` for an asynchronous Tier A *training* pass. DPO pair generation happens later, downstream, not at this queue.

Two quality questions decide whether the flow is worth its cost: is the **training loop** producing adapters that measurably improve the model, and is the **DataGraph** an accurate, well-resolved ontology rather than a pile of fragments?

## How the loop is intended to close

A healthy training loop is a closed circuit: corpus → SFT → on-policy DPO → an eval gate → promotion only on a measured improvement → the promoted adapter **served** on the inference path → its behaviour captured back into the corpus. Several stages are real and confirmed: adapters attach to all linear projections of the base model and the attachment is asserted post-build (a fail-closed check on the exact target-module list, in both the SFT and DPO training scripts); learning rates sit an order of magnitude above full fine-tuning (2e-4 vs. a stated 2e-5 full-FT default); preference training runs only above a clean, diverse pair floor (a real `CLEAN_PAIR_FLOOR = 3000` constant, plus per-pair quality gates); and no adapter is promoted that a base-versus-adapter probe cannot distinguish from the base model (a real deploy-gate script implementing exactly this check).

The eval gate does not compare the new adapter to an incumbent on a frozen, version-hashed gold set — no incumbent comparison or version-hashed gold set exists. The gate scores an adapter's own completions against a static pass-rate threshold — diff-parse / git-apply / envelope-format correctness — over a randomly-shuffled 10% holdout, freshly split each run.

## How the ontology is intended to be coherent

A coherent DataGraph is intended to resolve entities through blocking, similarity, and canonicalisation stages, so that surface variants ("MCorp", "Woodfine Capital Projects") collapse to a single canonical identity. What's built today is narrower: entity resolution implements three stages, not four — blocking → similarity → decision bands (auto-merge / review / new) — with no clustering stage. The alias table that would back canonicalization is explicitly not yet implemented; the module's own comment describes it as "an additive migration applied separately." Entity resolution today is pure and side-effect-free, not yet backed by the alias mechanism this section describes.

Facts carry partial provenance: a real `confidence` field and a real `source_doc` field exist on every graph entity, with `source_doc` first-write-wins — but there is no `extractor_tier` field, so provenance does not yet capture which tier (GLiNER, OLMo, or GPU) produced a given fact. Conflict handling is mixed, not uniformly "reconciled rather than blindly overwritten": vector fields use a new-wins-if-present merge and `source_doc` is first-write-wins, but `confidence` is unconditionally overwritten on every write — the one field most directly meant to signal trust is the one field that isn't reconciled at all. Relationships genuinely are typed, directional edges from a closed ontology (a real relation-type vocabulary loaded from a CSV file) — this part is accurate as described.

Point-in-time history — reading any fact "as of" a date — is not built. It is planned; see Target state, below.

## Target state (planned)

The intended target, adopted incrementally, is two co-evolving loops behind one Doorman boundary, sharing one pinned base model on sovereign hardware.

**The DataGraph loop** is intended to advance from a property graph to a sophisticated ontological one: a formal versioned ontology (OWL 2 RL) whose axioms let a reasoner *derive* edges the extractor never wrote; SHACL validation as a write gate; embedding-based and inductive link completion that proposes scored *candidate* edges for review (never auto-published); multi-hop logical query answering over the incomplete graph; a community tier for thematic retrieval; and a self-ontologising layer so the schema grows from the corpus — all behind a `GraphStore` trait, with bitemporal provenance so any fact is reproducible "as of" a date.

**The training loop** is intended to run continuously rather than as an occasional batch: the served model generates its own on-policy preference pairs, a reference-free objective keeps perpetual training affordable, an evaluation gate is the only path to promotion, and a promoted adapter hot-swaps onto the inference path while the old one waits in a rollback slot — with training scheduled into serving idle slack so it never starves interactive requests. A single base registry would pin one base-model lineage across training, the reference policy, and serving, so a trained adapter is always servable.

The two loops are intended to unify: the graph supplies training signal, and the trained model improves extraction — one self-feeding system. The phased path and the decisions it requires are tracked in the flow build-plan brief. This topic describes architecture; the operational procedure is covered in the companion guide.
