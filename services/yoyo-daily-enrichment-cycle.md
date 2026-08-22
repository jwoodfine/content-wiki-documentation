---
schema: foundry-doc-v1
title: "Yo-Yo daily enrichment cycle"
slug: yoyo-daily-enrichment-cycle
short_description: "The nightly two-phase GPU batch window that rebuilds the DataGraph and, once fully enabled, trains adapter weights for the local language model — currently running in DataGraph-only mode."
category: services
index_group: ring-3-ai-gateway
type: topic
content_type: topic
status: stable
bcsc_class: current-fact
last_edited: 2026-08-22
editor: pointsav-engineering
paired_with: yoyo-daily-enrichment-cycle.es.md
---

The Yo-Yo daily enrichment cycle is the nightly batch window on the [[yoyo-compute-substrate|
burst GPU node]] that rebuilds the [[ontological-datagraph|DataGraph]] and, once fully
enabled, trains updated adapter weights for the workspace language model. The cycle runs on
a fixed schedule and always releases the GPU at the end, whether or not both phases complete.

## Two phases, not eight

The cycle is one script running two sequential phases, each with its own
configurable time budget defaulting to two hours — roughly four hours total, not a
forty-five-minute window. The two phases cannot overlap: they need exclusive access to the
same GPU, and the script stops the inference server before the training phase begins.

**Phase 1 — DataGraph rebuild.** The batch VM boots, waits for its inference server to
become healthy, then processes the day's accumulated documents through the Doorman, writing
extracted entities directly to the DataGraph. Full detail: [[service-slm-graph-store-
migration]].

**Phase 2 — Adapter training.** A threshold check counts accumulated training tuples across
two corpus buckets. Once a bucket crosses its clean-pair floor, a training-pending marker
is written and, if configured, the relevant corpus syncs to cloud storage. On the batch VM, a
training script polls for that marker and runs a parameter-efficient fine-tune (QLoRA)
against the base model when one appears.

## Current status: training is not yet active

As of this writing, the training half of the cycle runs in marker-only mode: the threshold
check writes and dispatches the marker, but the training script itself is not yet enabled on
the batch VM's running image — a pending image rebuild is the next step before it goes live.
Every night's cycle today does real DataGraph enrichment; no adapter has yet been produced by
this pipeline running end to end on its own schedule.

## Cost and the hard stop

The VM is stopped unconditionally at the end of the cycle regardless of how far the phases
got, and a kill-switch file can suppress the whole cycle immediately if set. An idle monitor
provides a backstop: if the cycle ever fails to stop the VM itself, the monitor stops it after
a sustained idle period, bounding the worst case. At the real multi-hour cycle length — not
the forty-five-minute figure a stale version of this article assumed — the per-cycle cost is
several times higher than that shorter window would suggest; an exact current figure isn't
republished here since it would need to be re-measured against the real Phase 1/Phase 2
budgets and current cloud pricing, not carried forward from a since-corrected assumption.

## See also

- [[service-slm-graph-store-migration]] — the DataGraph rebuild that is Phase 1 of this cycle
- [[elastic-compute-lora-training-pipeline]] — the fuller two-phase pipeline description, including the training phase's real QLoRA configuration
- [[service-slm]] — the service that orchestrates the pipeline
