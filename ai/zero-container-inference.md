---
schema: foundry-doc-v1
content_type: topic
index_group: compute-tiers
title: "Zero-container inference"
slug: zero-container-inference
short_description: "Tier B GPU deployment pattern using native Linux binaries under systemd on an L4 GPU (not the A100 earlier text claimed), with idle detection run from the Doorman server process, not a timer on the GPU VM itself."
category: ai
status: stub
bcsc_class: forward-looking
last_edited: 2026-08-17
editor: pointsav-engineering
cites:
 - osc-sn-51-721

---

Zero-container inference is the deployment pattern for the platform's Tier B [[yoyo-compute-substrate|GPU compute]]: native Linux binaries under systemd on GCE virtual machine instances, with no container runtime or orchestrator. This is confirmed in the real Packer/OpenTofu build (`service-slm/compute/`), which ships systemd `.service` units and no Docker or OCI tooling anywhere in the pipeline.

The economics close because idle detection ensures GPU billing stops when inference is not running. The specific GPU and pricing claims in earlier versions of this article were wrong, not just imprecise — corrected below rather than repeated here, since no single cost figure has been recomputed yet against the real instance shape. The Tier B inference pool that embodies this pattern has real, deployed infrastructure code; it is not a from-scratch build. Its production-traffic status was not independently confirmed here.

## Why no containers

OCI container images imply a container registry: the registry becomes the durable artefact, and the operator must maintain image build chains, registry credentials, and CVE remediation for base images. For a one-shot inference VM that boots, runs for 30 minutes, and stops, the container layer adds operator surface without solving any problem the virtual machine approach does not address more directly. The single-binary, systemd-supervised approach is consistent with the [[zero-container-runtime]] structural commitment that governs all platform service deployments.

## What is used instead

A native binary in the `slm-yoyo` GCE image family (`image_family = "slm-yoyo"` in the real Packer config; `pointsav-public` is the example GCP project id, not an image family — a distinction earlier text got right). A systemd unit with an `ExecStart` pointing to the binary — both `llama-server.service` and `vllm.service` ship in the image, and the codebase does not agree with itself about which one is actually the deployed engine (see Operational artefacts, below). OpenTofu for VM provisioning and lifecycle management. GCS-cached model weights so the cold-start path fetches from Cloud Storage rather than downloading from the upstream registry on each boot — confirmed in `vllm-weights-prep.sh`. nginx for TLS termination, with the firewall restricted to port 9443. CUDA drivers baked into the GCE image at build time (`provision.sh` installs the CUDA 12 toolkit during the Packer build).

**Not Secret Manager for API keys** — no GCP Secret Manager usage exists anywhere in `service-slm`. The real mechanism is a static bearer token passed via GCE instance metadata (`opentofu/variables.tf`).

## SMB economics

The GPU is an `nvidia-l4` on a `g2-standard-4` instance, confirmed in `opentofu/main.tf` — not an A100 80 GB as earlier text claimed; the specific per-hour and per-month cost figures that followed from the A100 assumption are wrong along with it and are not replaced with a new number here until they're recomputed against the real instance shape. The instance is preemptible/spot, which earlier text also got right. The economics close because idle detection is the load-bearing primitive: the instance stays up only while inference is running, not for operator convenience.

**How idle detection actually works — not a timer on the GPU VM.** It's a background task inside the Doorman server process (`idle_monitor.rs`) that polls the instance's `/metrics` every 5 minutes and issues a real `instances.delete` call — deletion, not a "stop" — once the instance has been idle past `SLM_YOYO_IDLE_MINUTES` (default 30). A separate, genuinely VM-local systemd unit, `yoyo-deadman.service`, is a real dead-man's-switch that powers the instance off at a metadata-set maximum lifetime — a different mechanism, for a different failure mode (a runaway or orphaned instance), not the routine idle-shutdown path.

## Cold-start: the one honest concern

Earlier text estimated 60–120 seconds from stopped state to inference-ready. The systemd units' own configured startup budgets suggest this was optimistic: `llama-server.service` sets `TimeoutStartSec=300`, `vllm.service` sets `TimeoutStartSec=600` — real cold-start budgets in the minutes, not under two. For latency-critical workloads where a fast response is required, the deployment should extend `SLM_YOYO_IDLE_MINUTES` to keep the instance warm rather than assume a sub-two-minute cold start. For nightly batch workloads — the primary use case for continued pretraining and large-scale corpus extraction — the cold-start cost is the price of zero idle cost and is a reasonable trade regardless of the exact number.

## Operational artefacts

The deployment stack for a Tier B inference instance has four real pieces. An OpenTofu module handles instance lifecycle management. The GCE image ships CUDA drivers, nginx, systemd units, and — this is where the codebase contradicts itself — **both** `llama-server` and `vllm` services: `slm-doorman/src/tier/yoyo.rs` states the deployed Tier B server is llama.cpp, "NOT vLLM," while `tier/local.rs` separately claims Tier B is "vLLM ≥0.12." That contradiction is not resolved here — it's flagged rather than silently picking a side. A bearer token in GCE instance metadata handles authentication (not Secret Manager, see above). Cloud Logging points to the customer's own GCP project.

**Not confirmed, despite earlier text's claim**: a Cloud Billing budget with a Pub/Sub kill-switch as defence-in-depth against runaway spend. No Pub/Sub or Cloud Billing budget code exists in `opentofu/` or `slm-doorman` — the only trace is an unimplemented `monthly_cap_usd` mention in prose documentation. The operator never interacts with the instance directly during inference; the systemd units and the Doorman-side idle monitor handle the lifecycle autonomously.

## What this rules out

Managed container orchestration platforms, container runtime systems, multi-cloud abstraction frameworks, OCI image registries, layered container image build caching, and container build pipelines. These categories are not excluded because they are inferior in general; they are excluded because they introduce operator surface that is inconsistent with the [[zero-container-runtime]] structural commitment and the SMB economics case described above.

## See also

- [[zero-container-runtime]] — the structural commitment underlying this deployment pattern; applies across all platform service rings
- [[doorman-protocol]] — the Tier B routing path that dispatches to the inference pool
- [[substrate-without-inference-base-case]] — the substrate functions fully without Tier B; inference is additive
