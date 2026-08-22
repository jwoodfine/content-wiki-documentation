---
schema: foundry-doc-v1
title: "service-slm graph store rebuild"
slug: service-slm-graph-store-migration
category: services
index_group: ring-3-ai-gateway
type: concept
content_type: topic
quality: pre-build
status: pre-build
audience: vendor-public
bcsc_class: current-fact
language_protocol: PROSE-TOPIC
last_edited: 2026-08-22
editor: pointsav-engineering
paired_with: service-slm-graph-store-migration.es.md
short_description: "service-slm's graph store runs a nightly rebuild — entity extraction via the Doorman writes directly to the graph on completion, with no human review step in the rebuild script itself."
cites: []
---

The [[service-slm]] graph store is a live property graph of named business entities
extracted nightly from an operator's data corpus — the entity layer [[service-content]] uses
to inject structured business context into inference requests without sending proprietary
data to an external model. The graph is stored in LadybugDB and rebuilt nightly by a script
that runs as Phase 1 of the Elastic Compute window, before the model-training phase claims
the GPU.

## What the graph contains

The graph holds five entity classifications: Person (staff, contacts, counterparties),
Company (vendors, customers, partner organisations), Project (active and historical
engagements), Account (financial accounts and ledger references), and Location (offices,
sites, and operational addresses). These entities are extracted from three document
streams: meeting-transcript files, research and background material, and contact source
records from [[service-people]].

## What the nightly rebuild does

For each unprocessed document, the rebuild script calls the [[doorman-protocol|Doorman]]'s
completion endpoint with a JSON Schema grammar constraint. The language model — running on
the burst GPU tier via vLLM — returns a structured array of entity objects, each carrying a
name, classification, confidence score, and optional role, location, and contact fields. The
script then writes those entities directly to the graph through service-content's mutate
endpoint. A health check at the end of each cycle records the current entity count.

The script processes the full backlog of unprocessed documents each run, with a randomised
delay between requests so the Doorman never receives a burst that could interfere with the
training phase's own startup.

## The write path has no review step of its own

This is the fact a reader evaluating the platform's data-governance posture needs: the
rebuild script's write to the graph is unconditioned. It calls the same mutate endpoint any
operator or community member could call from their own automation, and that endpoint writes
immediately — there is no proposal file, no pending queue, and no human sign-off anywhere in
this script's own flow. A separate write-governance checkpoint exists elsewhere in
service-content (a capture-then-verify path for a different automated call site, requiring a
signed human verdict before a write lands), but it does not cover this endpoint or this
script; the endpoint's own design instead assumes each caller provides its own gate, and this
script does not provide one.

## Idempotency

The script tracks processed documents in a local append-only ledger, identified by a hash of
each document's content. A document already in the ledger is skipped on future runs. The
ledger is not pruned automatically; clearing it forces a full re-extraction on the next run.

## Graph context injection

The graph is not a static reference store. service-content queries it before each inference
request, retrieves entities relevant to the request's context, and injects them into the
model's system message as structured business context — who the relevant people are, what
projects are active, which companies are counterparties — without that structured data
crossing the external model boundary. The graph itself stays within the deployment; only the
injected prose context leaves it.

## Current status

The graph is live today, with real extracted entities actively serving inference requests.
Whether this pattern is ready to extend to larger operational contexts is gated on a
consecutive-healthy-runs criterion that has not yet been met — the pipeline is still in its
initial operational period.

## See also

- [[elastic-compute-lora-training-pipeline]] — Phase 2 of the same nightly window (LoRA adapter training)
- [[service-slm]] — the service that orchestrates the full nightly pipeline
