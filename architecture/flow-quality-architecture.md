---
schema: foundry-doc-v1
title: "The Knowledge Flow: Training Loop and Ontological DataGraph"
slug: flow-quality-architecture
category: architecture
type: concept
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: planned
language_protocol: PROSE-TOPIC
last_edited: 2026-06-28
editor: editorial
short_description: "The Totebox knowledge flow turns prose into two durable assets — an ontological DataGraph of entities and LoRA adapters that specialise a local language model. Two quality questions determine whether the flow is worth its cost: is the training loop producing adapters that measurably improve the model, and is the DataGraph an accurate, well-resolved ontology?"
paired_with: flow-quality-architecture.es.md
cites: []
---

The Totebox knowledge flow turns prose into two durable assets: an ontological DataGraph of entities, and LoRA adapters that specialise a local language model. Both are served by `service-slm` (the Doorman) and `service-content` (the DataGraph).

```
prose ─▶ service-extraction ─▶ CORPUS_*.json
      ─▶ service-content ──▶ GLiNER Tier 0 (~150ms) ─▶ entity spans
                         └──▶ OLMo Tier A (30–137s)  ─▶ fallback if Tier 0 empty
                         └──▶ GPU Tier B (enrichment) ─▶ role/location vectors
                         └──▶ LadybugDB graph
      ◀── Doorman queries the graph for context before each inference ◀──
training corpus (git-commit shadow tuples + Tier-A-vs-B enrichment pairs)
      ─▶ TRL SFT / DPO ─▶ PEFT adapter
```

Two quality questions decide whether the flow is worth its cost: is the **training loop** producing adapters that measurably improve the model, and is the **DataGraph** an accurate, well-resolved ontology rather than a pile of fragments?

## How the loop is intended to close

A healthy training loop is a closed circuit: corpus → SFT → on-policy DPO → an **eval gate** that compares the new adapter to the incumbent on a frozen, version-hashed gold set → promotion only on a measured improvement → the promoted adapter **served** on the inference path → its behaviour captured back into the corpus. The gold standard for each stage is well established: adapters attach to all linear projections of the base model and the attachment is asserted post-build; learning rates sit an order of magnitude above full fine-tuning; preference training runs only above a clean, diverse pair floor; and no adapter is promoted that a base-versus-adapter probe cannot distinguish from the base model.

## How the ontology is intended to be coherent

A coherent DataGraph resolves entities through four stages — blocking, similarity, clustering, and canonicalisation — backed by an alias table so that surface variants ("Woodfine Management Corp.", "Woodfine Capital Projects") collapse to a single canonical identity. Facts carry provenance (source document, extractor tier, confidence, timestamp); conflicting facts are reconciled rather than blindly overwritten; relationships are typed edges from a closed, directional ontology; and history is retained so any fact can be read "as of" a point in time.

## Target state (planned)

The intended target, adopted incrementally, is two co-evolving loops behind one Doorman boundary, sharing one pinned base model on sovereign hardware.

**The DataGraph loop** is intended to advance from a property graph to a sophisticated ontological one: a formal versioned ontology (OWL 2 RL) whose axioms let a reasoner *derive* edges the extractor never wrote; SHACL validation as a write gate; embedding-based and inductive link completion that proposes scored *candidate* edges for review (never auto-published); multi-hop logical query answering over the incomplete graph; a community tier for thematic retrieval; and a self-ontologising layer so the schema grows from the corpus — all behind a `GraphStore` trait, with bitemporal provenance so any fact is reproducible "as of" a date.

**The training loop** is intended to run continuously rather than as an occasional batch: the served model generates its own on-policy preference pairs, a reference-free objective keeps perpetual training affordable, an evaluation gate is the only path to promotion, and a promoted adapter hot-swaps onto the inference path while the old one waits in a rollback slot — with training scheduled into serving idle slack so it never starves interactive requests. A single base registry would pin one base-model lineage across training, the reference policy, and serving, so a trained adapter is always servable.

The two loops are intended to unify: the graph supplies training signal, and the trained model improves extraction — one self-feeding system. The phased path and the decisions it requires are tracked in the flow build-plan brief. This topic describes architecture; the operational procedure is covered in the companion guide.
