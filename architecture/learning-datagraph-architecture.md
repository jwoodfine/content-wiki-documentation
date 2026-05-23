---
schema: foundry-doc-v1
title: "Learning Datagraph — SLM trajectory loop and apprenticeship queue"
slug: learning-datagraph-architecture
language: en
category: architecture
type: topic
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-18
editor: pointsav-engineering
cites: []
paired_with: learning-datagraph-architecture.es.md
---

The platform builds a compounding substrate: every operator interaction with an AI session becomes a structured training tuple, routed through a single auditable boundary (Doorman), captured to an append-only ledger, and folded back into the local SLM via periodic fine-tuning. The result is a development environment that learns from how it gets used — code completions improve toward the patterns this operator writes, draft suggestions align closer to the editorial voice this house produces, entity extractions tighten as the graph thickens.

The substrate has four legs.

**Trajectory capture.** A Claude Code Stop hook fires at session end, writing a `foundry-trajectory-v1` JSONL entry to `data/audit-ledger/<archive>/<YYYY-MM>.jsonl`: branch state, uncommitted-file count, head SHA, and a Stage 6 pending flag. A nightly transcript harvest copies the day's Claude Code transcripts into the same ledger, tagged by operator and archive.

**Apprenticeship queue.** A `bin/capture-edit.py` post-commit hook emits a brief for every workspace commit. A 15-minute queue drainer calls local-slm (OLMo-2 7B Q4 via llama-server) against each brief, captures the model's attempt, and writes the `(brief, attempt, actual_diff)` tuple to `data/training-corpus/apprenticeship/<task-type>/<tenant>/`. 502 tuples had accumulated as of 2026-05-18.

**Editorial DPO pairs.** Every draft that passes through the reverse-funnel editorial pattern — raw to refined to creative-edited — emits two DPO pairs to `data/training-corpus/apprenticeship/prose-edit/<tenant>/`. The pair captures the editorial improvement deltas. 34 pairs had accumulated to that date.

**Negative-trajectory distillation.** `bin/capture-feedback.sh` scans inbox archives for operator corrections and emits negative-trajectory signals to `data/training-corpus/feedback/`. This fourth leg captures what the model should not do.

What remains to wire — multi-week Rust engineering effort: the structured-entity loop. [[service-content]] (LadybugDB-backed graph) needs a `POST /v1/draft/generate` endpoint that queries the graph for relevant entities, assembles a 2K-token grounded prompt, calls Doorman, and writes the response as a graph-grounded corpus tuple. A LoRA scheduler then wakes Yo-Yo Tier B for nightly adapter training. The supporting infrastructure — queue, ledger, hooks, audit-routing — is already in place.

The substrate compounds in two directions: structurally (citation density and supersedence chains thicken with each draft) and generatively (each adapter raises the floor of "raw" so each refinement cycle starts closer to publish-ready).

## See also

- [[compounding-substrate]] — the substrate discipline this architecture instantiates
- [[service-slm]] — the local SLM service that executes model inference in the loop
- [[totebox-session]] — the session model that trajectory capture instruments at session end
- [[mailbox-atomicity]] — the atomic prepend discipline that protects the audit ledger from concurrent write races
