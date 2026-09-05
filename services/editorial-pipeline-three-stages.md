---
schema: foundry-doc-v1
title: "The proofreading pipeline's wire contract"
slug: editorial-pipeline-three-stages
aliases:
  - editorial-pipeline-three-stages
short_description: "The real client-confirmed contract for the platform's proofreading pipeline: a fixed set of language protocols, a response that reports which compute tier ran and what degraded, and a binary human verdict that feeds the training corpus."
category: services
index_group: specialist-and-domain-services
type: topic
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-09-05
editor: pointsav-engineering
paired_with: editorial-pipeline-three-stages.es.md
---

The [[radical-proofreader-ui|proofreader console]] — the F4 content cartridge in `app-console-content` — submits text for editorial review and gets back a rewrite. What follows describes only what's confirmed by the client's own request and response types: the language-protocol vocabulary, the shape of a proofread response, and the verdict step that closes the loop.

## Protocol selection is a fixed, real list

Every submission names a `protocol` from a fixed set of nine, defaulting to `prose-topic`:

| Protocol | Genre |
|---|---|
| `prose-architecture` | Architecture documentation |
| `prose-guide` | Operational runbook |
| `prose-memo` | Memo |
| `prose-readme` | README |
| `prose-topic` | Content-wiki TOPIC (default) |
| `comms-chat` | Chat message |
| `comms-email` | Email |
| `comms-ticket-comment` | Ticket comment |
| `translate-en-es` | English-to-Spanish translation |

The request also carries a `tenant`, scoping the submission to the caller's own organisation.

## The response reports what actually ran

A successful response carries `improved_text` (the rewrite) alongside fields that describe how it was produced. `tier_used` names which compute tier handled the request. `degraded` lists anything that didn't run at full capability — real evidence that the pipeline has more than one internal component capable of failing independently, though this contract doesn't name those components or their order. `audit_ledger_id` references the audit trail, and `request_id` is used to record the verdict afterward. A caller can tell from the response alone whether the full pipeline ran or something degraded along the way, without needing separate status calls.

## The verdict is binary, and it trains the model

After reviewing the rewrite, the operator posts a verdict tied to the original `request_id`. The verdict is binary — accept or reject — and it's SSH-signed the same way the platform's other human-review checkpoints are: a reviewer's signature is checked against the workspace's `allowed_signers` file before the verdict is recorded. An accepted verdict marks the rewrite as a positive training example; a rejected one keeps the original. This is the same apprenticeship-style verdict mechanism used elsewhere in the platform for supervised model improvement — a human decision converted directly into training signal, never an automated accept.

## See also

- [[radical-proofreader-ui]] — the terminal console that submits text through this pipeline
- [[language-protocol-substrate]] — the genre family definitions the protocol list is drawn from
- [[customer-tier-catalog-pattern]] — the deployment model for a proofreading pipeline instance
