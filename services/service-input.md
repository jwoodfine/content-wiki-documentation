---
schema: foundry-doc-v1
type: topic
content_type: topic
slug: service-input
title: "service-input — reference-archive migration and calibration"
short_description: "service-input batch-migrates markdown reference material from a source archive into the platform's ingest pipeline, deduplicating by content hash and validating against each file's own ledger record — with a companion tool that scores how well downstream extraction matches that ledger."
audience: vendor-public
bcsc_class: current-fact
language_protocol: PROSE-TOPIC
paired_with: service-input.es.md
category: services
index_group: ring-1-boundary-ingest
status: active
quality: complete
last_edited: 2026-09-05
editor: pointsav-engineering
---

`service-input` is the backend behind a specific, named job: migrating a reference archive's markdown material into the platform in controlled batches, and evaluating how well the platform's own extraction later matches what that archive's ledger already said about each file. It is not a general-purpose multi-format document parser — its own package description calls it "file ingest, batch migration, and calibration evaluation."

## What it does

**Single-file ingest.** `POST /v1/append` reads one file from disk, hashes it with SHA-256, and skips it if that hash has already been processed this run — a simple, direct dedup gate before anything is forwarded onward.

**Batch migration.** `POST /v1/migrate` walks a source reference archive's markdown assets in sorted, offset-and-batch-size slices (capped at 50 files per call), checking each file against a YAML ledger record before including it. Two delivery modes exist: the default path routes files onward through the platform's normal ingest chain, while an optional direct mode — when a corpus-emission directory is configured — writes a `CORPUS_<stem>.json` bridge file straight to a directory [[service-content]] watches, the same bridge pattern [[service-extraction]] uses. In direct mode, ledger validation is relaxed and every markdown file in the batch is included rather than only ledger-matched ones.

**Calibration evaluation.** `GET /v1/eval/:stem` and `GET /v1/calibration-report` compare what extraction actually produced for a given file against a canonical, normalized form of that file's own reference ledger entry — entities, metrics, and themes — to measure how closely automated extraction tracks a known-good record.

## Configuration

The service reads its tenant scope from `SERVICE_INPUT_MODULE_ID` (defaulting to `jennifer`), and its remaining configuration — the source reference archive's root path, the destination archive, request-rate and batch-size limits, and the downstream `service-fs`/content endpoints it forwards to — is set at startup rather than negotiated per request.

## See also

- [[service-content]] — one of the two consumers of this service's output, either via the normal ingest chain or the direct CORPUS bridge
- [[service-extraction]] — uses the same CORPUS-bridge delivery pattern for its own output
- [[service-fs]] — the ledger this service's normal (non-direct) delivery path writes into
