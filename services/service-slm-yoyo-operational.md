---
schema: foundry-doc-v1
title: "SLM and Yo-Yo operational state"
slug: service-slm-yoyo-operational
category: services
type: topic
content_type: topic
quality: complete
index_group: ring-3-ai-gateway
short_description: "How service-slm's three-tier inference router and the Yo-Yo GPU burst VM operate: the Doorman boundary, the local and burst tiers, the apprenticeship queue, and the idle-shutdown cost ceiling."
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-09-05
editor: pointsav-engineering
cites:
 - ni-51-102
 - np-51-201
 - olmo3-allenai
references:
  - id: 1
    text: "AllenAI OLMo 3 model family. Apache 2.0 (model weights); Open Data Commons (training data)."
    url: "https://huggingface.co/allenai"
  - id: 2
    text: "NI 51-102 Continuous Disclosure Obligations. British Columbia Securities Commission."
    url: "https://www.bcsc.bc.ca/securities-law/law-and-policy/instruments-and-policies/5-ongoing-requirements-for-issuers-insiders/current/51-102"
  - id: 3
    text: "CSA National Policy 51-201 Forward-Looking Information Disclosure. Ontario Securities Commission."
    url: "https://www.osc.ca/en/securities-law/instruments-rules-policies/5/51-721/osc-staff-notice-51-721-forward-looking-information-disclosure"
paired_with: service-slm-yoyo-operational.es.md
---

`service-slm` is the platform's [[three-ring-architecture|Ring 3]] component — the optional
intelligence layer. It is a tiered inference router that clusters and contributors use to
delegate routine work: editorial polish, mechanical schema-conforming edits, bilingual
translation drafts, and structured-output generation. Work is handled locally or on a
dedicated GPU burst VM, without routing to a third-party API by default. Rings 1 and 2
(boundary ingest and knowledge processing) function fully without it — Ring 3 is structurally
optional.

**Yo-Yo** is the platform's on-demand GPU burst instance — a GCE VM that runs a larger model
than the local tier can, starts on demand, and shuts down after a period of inactivity. A
third tier (external API) exists in the routing configuration but is unused in normal
operation, reserved for cases genuinely requiring it.

## The Doorman boundary

Every inference request crosses the [[doorman-protocol|Doorman]] before reaching a model
tier. The Doorman does not run as its own standalone process — it is bundled together with
service-content inside a single service (`local-totebox.service`). Its responsibilities cover
the full request lifecycle: holding every API key so no key is dispersed across call sites,
routing requests to the correct tier by complexity, appending every transit to a per-tenant
audit ledger, and draining the apprenticeship brief queue described below.

## Local tier — always available

The local tier runs `llama-server` (the C++ HTTP server from llama.cpp) on the workspace VM's
own CPU. The model loaded is a quantized OLMo 3 7B **Instruct** build[^1] — the instruction-tuned
variant, not the "Think" reasoning variant. Throughput on a CPU-only workspace VM is on the
order of a few tokens per second — sufficient for short briefs and trivial completions, not for
routine editorial work at scale. This latency ceiling is what motivated the burst tier below.

## Yo-Yo tier — burst GPU

The Yo-Yo instance runs `llama-server` with GPU support on a separate GCE instance in
`us-central1-a`, on hardware with one NVIDIA L4 GPU (24 GB VRAM), provisioned on-demand
rather than as a spot instance — spot capacity for this GPU class proved unreliable across
multiple US zones during initial bootstrapping. The model is a larger OLMo 3 model tuned for
deeper reasoning. Network access to the instance's inference port is restricted by firewall
rule to the workspace VM's internal address only, and every request is authenticated with a
bearer token the Doorman holds.

**Currently down.** As of this writing, the live Doorman health check reports the Yo-Yo
tier's circuit open on all three of its configured labels, due to sustained health-probe
failures — this tier has not been serving requests for an extended period. Requests that
would route here currently fall back or queue rather than complete on this tier; this is a
live operational fact, disclosed here on the same continuous-disclosure basis as any other
current-state claim on this wiki, not a design description.[^2][^3]

### Provisioning

A fresh Yo-Yo instance is built from a startup script covering package installation, a CUDA
toolkit and `llama-server` build from source, model download, bearer-token generation, and
systemd unit configuration — a documented, multi-step process whose iteration history
(driver/kernel version mismatches, compilation memory limits, download reliability) is
preserved in the script's own inline comments and the workspace changelog.

## The apprenticeship brief queue

Every commit triggers a capture hook that writes an engineering corpus tuple and a shadow
brief to a durable queue. The Doorman's drain worker polls this queue, dispatches each brief
to the local tier by default (or the burst tier above a size threshold), and on completion
writes a corpus tuple at the review stage. This mechanism is durable across Yo-Yo
idle-shutdown windows, Doorman restarts, and apprentice timeouts — the queue accumulates
while the burst tier is stopped, and the backlog drains without loss once it restarts. As of
this writing, the live queue reports several thousand pending entries and a large poisoned
(failed-and-quarantined) count relative to completions — worth a dedicated look by whoever
owns this pipeline, not something this article resolves.

## Cost ceiling — the idle-shutdown monitor

An idle-shutdown monitor polls the Yo-Yo VM for active inference activity on a regular
schedule and stops the instance after a sustained period with none, keeping always-on GPU
cost from applying to idle time. The monitor runs from the workspace VM rather than the Yo-Yo
VM itself, since the workspace VM's service account holds the cloud permissions needed to
stop an instance and the Yo-Yo VM's does not.

## What runs on the burst tier

The platform's engineering workflow routes routine work here: mechanical documentation
updates, schema-conforming edits, pattern-based refactors, bilingual translation drafts,
routine status reports, and boilerplate code. Architectural decisions, novel design, and
cross-layer coordination route to a frontier-model tier instead. `service-slm` is the
multiplier for routine work; the frontier model is reserved for judgment calls.

## See also

- [[compounding-substrate]] — the architectural pattern this implements
- [[service-slm]] — service-slm's tier-routing overview
- [[apprenticeship-substrate]] — how training signal accumulates from operational corpus tuples
- [[brief-queue-substrate]] — the durable queue connecting the brief queue to tier processing
- [[worm-ledger-architecture]] — the audit ledger that records every external call
