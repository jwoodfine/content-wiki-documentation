---
schema: foundry-doc-v1
content_type: topic
index_group: compute-tiers
title: "Zero-container inference"
slug: zero-container-inference
short_description: "Tier B GPU deployment pattern using native Linux binaries under systemd on an L4 GPU, with idle detection run from the Doorman server process rather than a timer on the GPU VM itself."
category: ai
status: active
quality: complete
bcsc_class: forward-looking
last_edited: 2026-08-24
editor: pointsav-engineering
cites:
 - np-51-201

---

Zero-container inference is the deployment pattern for the platform's Tier B [[yoyo-compute-substrate|GPU compute]]: native Linux binaries under systemd on GCE virtual machine instances, with no container runtime or orchestrator.

The economics close because idle detection ensures GPU billing stops when inference is not running. The Tier B inference pool that embodies this pattern has real, deployed infrastructure code; it is not a from-scratch build.

## Why no containers

OCI container images imply a container registry: the registry becomes the durable artefact, and the operator must maintain image build chains, registry credentials, and CVE remediation for base images. For a one-shot inference VM that boots, runs for 30 minutes, and stops, the container layer adds operator surface without solving any problem the virtual machine approach does not address more directly. The single-binary, systemd-supervised approach is consistent with the [[zero-container-runtime]] structural commitment that governs all platform service deployments.

## What is used instead

A native binary in the `slm-yoyo` GCE image family. A systemd unit supervises the binary; both a llama.cpp service and a vLLM service ship in the image, and which one serves live Tier B traffic is not yet settled (see Operational artefacts, below). OpenTofu handles VM provisioning and lifecycle management. Model weights are cached in Cloud Storage, so the cold-start path fetches locally rather than downloading from the upstream registry on each boot. nginx handles TLS termination, with the firewall restricted to port 9443. CUDA drivers are baked into the GCE image at build time.

Authentication does not use Secret Manager. The mechanism is a static bearer token passed via GCE instance metadata.

## SMB economics

The GPU is an `nvidia-l4` on a `g2-standard-4` instance, running as a preemptible/spot instance. The economics close because idle detection is the load-bearing primitive: the instance stays up only while inference is running, not for operator convenience.

**How idle detection works.** A background task inside the Doorman server process polls the instance's health metrics every 5 minutes and deletes the instance — a real deletion, not a stop — once it has been idle past `SLM_YOYO_IDLE_MINUTES` (default 30). A separate, VM-local systemd unit is a dead-man's switch that powers the instance off at a metadata-set maximum lifetime — a different mechanism, for a different failure mode (a runaway or orphaned instance), not the routine idle-shutdown path.

## Cold start

Startup budgets configured on the systemd units run in the minutes, not under two — cold start from a stopped instance to inference-ready takes several minutes, not seconds. For latency-critical workloads where a fast response is required, the deployment should extend `SLM_YOYO_IDLE_MINUTES` to keep the instance warm rather than assume a fast cold start. For nightly batch workloads — the primary use case for continued pretraining and large-scale corpus extraction — the cold-start cost is the price of zero idle cost and is a reasonable trade.

## Operational artefacts

The deployment stack for a Tier B inference instance has four pieces. An OpenTofu module handles instance lifecycle management. The GCE image ships CUDA drivers, nginx, systemd units, and both a llama.cpp and a vLLM service — which one serves live traffic is not yet settled platform-wide. A bearer token in GCE instance metadata handles authentication. Cloud Logging points to the customer's own GCP project.

Defence-in-depth against runaway spend — a Cloud Billing budget with a kill-switch — is not yet built. The operator never interacts with the instance directly during inference; the systemd units and the Doorman-side idle monitor handle the lifecycle autonomously.

## What this rules out

Managed container orchestration platforms, container runtime systems, multi-cloud abstraction frameworks, OCI image registries, layered container image build caching, and container build pipelines. These categories are not excluded because they are inferior in general; they are excluded because they introduce operator surface that is inconsistent with the [[zero-container-runtime]] structural commitment and the SMB economics case described above.

## See also

- [[zero-container-runtime]] — the structural commitment underlying this deployment pattern; applies across all platform service rings
- [[doorman-protocol]] — the Tier B routing path that dispatches to the inference pool
- [[substrate-without-inference-base-case]] — the substrate functions fully without Tier B; inference is additive
