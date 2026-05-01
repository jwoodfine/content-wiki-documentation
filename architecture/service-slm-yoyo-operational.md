---
schema: foundry-doc-v1
title: "service-SLM and Yo-Yo — Operational State"
slug: service-slm-yoyo-operational
category: architecture
type: topic
quality: complete
short_description: "How service-SLM's three-tier inference router and the Yo-Yo GPU burst VM operate at workspace v0.1.91, including the Doorman boundary, Tier A/B configuration, apprenticeship brief queue, and idle-shutdown cost ceiling."
status: pre-build
last_edited: 2026-04-30
editor: pointsav-engineering
cites:
  - ni-51-102
  - osc-sn-51-721
  - olmo3-allenai
paired_with: service-slm-yoyo-operational.es.md
---

**service-SLM** is Foundry's Ring 3 component — the Optional Intelligence layer (Doctrine claim #16). It is a three-tier inference router that clusters and contributors use to delegate routine work: editorial polish, mechanical schema-conforming edits, bilingual translation drafts, and structured-output generation. The work is handled locally or on a dedicated GPU burst VM, without routing to a third-party API. Rings 1 and 2 (boundary ingest and knowledge processing) function fully without it; Ring 3 is structurally optional.

The **Yo-Yo** is the name for Foundry's on-demand GPU burst instance — a GCE VM that runs a 32-billion-parameter instruction-tuned model at approximately 50-100 tokens per second. It starts on demand, shuts down after 30 minutes of inactivity, and accumulates a brief queue through its idle windows. The combination — a lightweight always-available local model on the workspace VM and a capable on-demand burst VM — defines the two active inference tiers. A third tier (external API) is configured for future use; Tier C has no active keys in workspace v0.1.91.

This document describes how service-SLM and the Yo-Yo operate as of workspace v0.1.91, when the substrate-arc was marked complete.

## The Doorman boundary

Every inference request crosses the Doorman before reaching a model tier. The Doorman is a Rust binary running as systemd unit `local-doorman.service`, binding `127.0.0.1:9080`. Its responsibilities cover the full request lifecycle:

- Hold all API keys — Tier C provider tokens and the Tier B bearer token. Keys exist nowhere else in the request path. This is the API-key boundary discipline: no key dispersal across call sites.
- Route requests to the correct tier based on complexity heuristics: request size, structured-output requirements, and audit-ledger semantics.
- Sanitise outbound requests before they reach any external API (strip workspace identifiers; rehydrate on inbound).
- Append every transit to a per-tenant audit ledger at `/var/lib/local-doorman/audit/<tenant>/<YYYY-MM>.jsonl`.
- Drain the §7C apprenticeship brief queue (described below).

The `/readyz` endpoint returns live tier-availability flags. As of workspace v0.1.91:

```json
{
  "ready": true,
  "has_local": true,
  "has_yoyo": true,
  "has_external": false,
  "apprenticeship_enabled": true
}
```

## Tier A — workspace VM (always available)

Tier A runs `llama-server` — the C++ HTTP server from llama.cpp — on the workspace VM CPU. The model is `OLMo-3-1125-7B-Think-Q4_K_M.gguf`, self-quantized from AllenAI's published safetensors release (Apache 2.0; sovereign supply chain). It binds `127.0.0.1:8080` as `local-slm.service`.

Throughput on the workspace VM (an `e2-standard-4` GCE instance, CPU only) is approximately 2-3 tokens per second. This is sufficient for short briefs and trivial completions. It is not sufficient for routine editorial work at scale. The Tier A latency constraint was documented operationally at workspace v0.1.77 and motivated the v0.1.78 ratification of the four-tier substrate ladder (Doctrine claim #40).

## Tier B — Yo-Yo on L4 GPU

Tier B runs `llama-server` with CUDA support on a separate GCE instance (`yoyo-tier-b-1`) in `us-west1-a`. The hardware is `g2-standard-4`: 4 vCPU, 16 GB RAM, and one NVIDIA L4 GPU with 24 GB VRAM. The model is AllenAI's published `OLMo-2-0325-32B-Instruct-Q4_K_S.gguf` (Apache 2.0). The instance is provisioned on-demand rather than as a spot instance — L4 spot capacity proved unreliable across multiple US zones during the workspace v0.1.81 through v0.1.88 bootstrap.

Port 8080 on the Yo-Yo VM is restricted by GCE firewall rule `yoyo-tier-b-from-workspace` to the workspace VM's internal IP (`10.138.0.4/32`) only. The Doorman holds the bearer token (`SLM_YOYO_BEARER`, configured in `/etc/local-doorman/local-doorman.env`) and authenticates every request.

Measured throughput (smoke test at workspace v0.1.88): approximately 50-100 tokens per second generation; 100 tokens per second prompt processing. A typical 500-token instruction task completes in 5-15 seconds wall-clock. Cold-start — loading the model into GPU memory — takes 60-180 seconds and is amortised across subsequent requests in the same session.

### Provisioning

The Yo-Yo VM is configured from the startup provisioning script at `infrastructure/yoyo-manual/startup.sh`. A fresh provision reproduces the live state in approximately 30-40 minutes wall-time, across eight steps:

1. Wait for cloud-init and unattended-upgrades to release the dpkg lock (up to 5 minutes on first boot).
2. Install common dependencies (`curl`, `wget`, `jq`, `aria2`, `python3.12-venv`).
3. Install CUDA toolkit, cmake, and build-essential.
4. Clone llama.cpp and build `llama-server` with `-DGGML_CUDA=ON` and `-j 2`. The `-j 2` constraint is intentional: unrestricted parallelism triggers `cc1plus` out-of-memory failures on 16 GB RAM during compilation.
5. Download the OLMo 2 GGUF via `aria2c` with four parallel segments and resume support. Single-stream wget proved unreliable against HuggingFace unauthenticated CDN rate-limiting; `aria2c -x 4 -s 4` is the documented 2026 community practice.
6. Generate a 64-character bearer token and write it to `/etc/yoyo-bearer` with mode 0640.
7. Configure the `yoyo-llama-server.service` systemd unit.
8. Start the service and wait for `/health` to return `{"status":"ok"}`.

The bootstrap pipeline incorporates 14 distinct fixes for failure modes encountered during the v0.1.81 through v0.1.88 iteration: spot capacity stockouts, networking edge cases, NVIDIA driver and kernel version mismatches (driver 550 does not support kernel 6.17; the solution is a DL VM image with NVIDIA 580 and a matched kernel), 16 GB RAM compilation OOM, dpkg lock races, model hosting changes, HuggingFace CDN rate-limiting, and llama-server architecture support gaps. Each fix is documented inline in `infrastructure/yoyo-manual/startup.sh`. The iteration history is preserved in the workspace CHANGELOG.

## §7C — the apprenticeship brief queue

Every commit on the workspace and on every active cluster triggers the `bin/capture-edit.py` post-commit hook. The hook writes two records:

- An engineering corpus tuple at `data/training-corpus/engineering/<scope>/<commit_sha>.jsonl` (accumulating since workspace v0.1.x).
- A shadow brief at `data/apprenticeship/queue/<brief_id>.brief.jsonl` (workspace v0.1.85 onwards; replaces an earlier HTTP fire-and-forget path that proved unreliable under network interruptions).

The Doorman runs a drain worker that polls the queue directory every 30 seconds. When a brief appears, the worker performs an atomic rename to `queue-in-flight/` (dequeue), dispatches to the apprentice tier — Tier A by default, Tier B when the brief size exceeds `SLM_BRIEF_TIER_B_THRESHOLD_CHARS=500` — and on completion writes a corpus tuple at `data/training-corpus/apprenticeship/<task-type>/<tenant>/<brief_id>.jsonl` at stage `review`. A reaper task reclaims expired leases (5-minute timeout) and returns briefs to the queue for retry.

This mechanism is durable across Yo-Yo idle-shutdown windows, Doorman restarts, and apprentice timeouts. The queue accumulates while the Yo-Yo VM is stopped; on restart, the drain worker processes the backlog without loss.

## Cost ceiling — the idle-shutdown monitor

The Yo-Yo VM costs approximately $0.71 USD per hour while running. Always-on operation is approximately $540 USD per month. The idle-shutdown monitor at `bin/yoyo-idle-monitor.sh`, scheduled by `yoyo-idle-monitor.timer` every five minutes, keeps the monthly cost within a practical ceiling.

The monitor polls the Yo-Yo VM's `/slots` endpoint for active inferences. After 30 consecutive minutes of zero active inference slots, the monitor calls `gcloud compute instances stop yoyo-tier-b-1`. The brief queue continues to accumulate during stopped windows; the next operator-triggered start drains the backlog.

The monitor runs from the workspace VM rather than the Yo-Yo VM. The workspace VM's Compute Engine service account holds `cloud-platform` scope; the Yo-Yo VM's default service account does not. Running the monitor workspace-side is the simpler design given this scope difference.

At a typical development utilisation of approximately 25 percent, the idle-shutdown ceiling brings monthly spend to approximately $130-150 USD. Customers replicating this pattern operate under the same economics; the cost ceiling is a structural property of the on-demand provisioning model, not a vendor-specific optimisation.

## What runs on Tier B today

The v0.1.86 cluster broadcast established the `SERVICE-SLM-PROPOSAL` convention: cluster Tasks identify routine work that service-SLM can handle and propose it via outbox. Master batches the proposals into the apprenticeship queue; service-SLM produces attempts; senior verdicts sign quality outputs into the DPO corpus.

Examples of routine work routed to Tier B: mechanical documentation updates, schema-conforming edits, pattern-based refactors, bilingual translation drafts, routine status reports, and boilerplate code. Architectural decisions, novel design, and cross-layer coordination remain on Claude per the broadcast's discipline rules. service-SLM is the multiplier for routine work; Claude is the engine for judgment.

## What is next

*Forward-looking statement: the targets in this section are planned, not committed outcomes. Actual timelines depend on apprenticeship corpus growth rate, operator availability, and model performance characteristics. [ni-51-102] [osc-sn-51-721]*

Per the workspace v0.1.86 first-week target, it is currently planned for the apprenticeship corpus to reach 100 verdict-signed tuples by 2026-05-06, subject to commit cadence and senior-verdict throughput. It is intended that 50 percent of routine Task work routes through service-SLM within 30 days of the v0.1.86 broadcast, as clusters adopt the `SERVICE-SLM-PROPOSAL` convention and the drain worker accumulates a sufficient backlog of reviewed corpus tuples. The first per-cluster LoRA training cycle is planned for Week 4, targeting the densest existing corpus — the project-language Stage-1 `prose-edit/pointsav` collection.

When AllenAI publishes OLMo 3 32B Think or Instruct in a Q4 GGUF format, the Yo-Yo deployment is designed to swap to it via a single configuration line. Per-cluster LoRA adapters compose on top of whatever base model is current; the substrate is base-model-agnostic by design.

## See Also

- [[compounding-substrate]] — the five-property architectural pattern this implements
- [[service-slm]] — service-SLM service overview
- [[apprenticeship-substrate]] — how training signal accumulates from operational corpus tuples
- [[brief-queue-substrate]] — the durable queue that connects §7C to Tier A/B processing
- [[worm-ledger-architecture]] — the audit ledger that records every external call

## References

1. PointSav Doctrine claim #16 — Optional Intelligence Layer. Defines Ring 3 as structurally optional; Rings 1 and 2 function without it.
2. PointSav Doctrine claim #40 — Four-Tier SLM Substrate Ladder. Ratified workspace v0.1.78; defines Tier 0 (none) / Tier 1 (local 7B) / Tier 2 (Yo-Yo 32B vendor-hosted) / Tier 3 (PointSav-LLM, planned).
3. AllenAI OLMo 3 model family. Apache 2.0 (model weights); Open Data Commons (training data). [olmo3-allenai] https://huggingface.co/allenai
4. `conventions/four-tier-slm-substrate.md` — workspace convention defining the four-tier ladder and routing heuristics.
5. `conventions/apprenticeship-substrate.md` §7B, §7C — drain worker protocol, corpus schema, and brief-queue mechanics.
6. NI 51-102 Continuous Disclosure Obligations. British Columbia Securities Commission. [ni-51-102] https://www.bcsc.bc.ca/securities-law/law-and-policy/instruments-and-policies/5-ongoing-requirements-for-issuers-insiders/current/51-102
7. OSC Staff Notice 51-721 Forward-Looking Information Disclosure. Ontario Securities Commission. [osc-sn-51-721] https://www.osc.ca/en/securities-law/instruments-rules-policies/5/51-721/osc-staff-notice-51-721-forward-looking-information-disclosure

## Provenance

This article draws on direct observation of workspace substrate state at v0.1.91: the Doorman `/readyz` endpoint was queried to confirm tier-availability flags; the Yo-Yo `/health` endpoint was queried to confirm model service; the cost estimate was calculated from Doorman audit ledger entries and GCP billing data. AllenAI's HuggingFace model pages were consulted to confirm OLMo 2 and OLMo 3 model availability, quantization levels, and licensing. The llama.cpp project's GitHub releases and documentation were consulted to confirm OLMo 2 architecture support and build flags. GCP Compute Engine API and Cloud NAT documentation were consulted to confirm service-account scope inheritance and external-IP requirements. HuggingFace rate-limit documentation was consulted to confirm CDN bandwidth shaping behaviour and the `aria2c -x 4` community practice.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
