---
schema: foundry-doc-v1
title: "Zero-container inference"
slug: zero-container-inference
short_description: "Zero-container inference is the planned deployment pattern for Tier B GPU compute using native Linux binaries under systemd on cloud virtual machines with no container runtime, achieving viable SMB economics through idle-shutdown timers that halt GPU billing when inference queues are empty."
category: architecture
status: stub
bcsc_class: forward-looking
last_edited: 2026-04-28
editor: pointsav-engineering
cites:
 - osc-sn-51-721
---

Zero-container inference is the planned deployment pattern for the platform's Tier B GPU compute: native Linux binaries under systemd on GCE virtual machine instances, with no container runtime or orchestrator. The economics close because idle-shutdown timers ensure GPU billing stops precisely when inference is not running — a 30-minute daily window on a preemptible A100 costs approximately $7–8 per month. The Yo-Yo compute pool that embodies this pattern is planned; it is not yet in production.

## Why no containers

OCI container images imply a container registry: the registry becomes the durable artefact, and the operator must maintain image build chains, registry credentials, and CVE remediation for base images. For a one-shot inference VM that boots, runs for 30 minutes, and stops, the container layer adds operator surface without solving any problem the virtual machine approach does not address more directly. The single-binary, systemd-supervised approach is consistent with the [[zero-container-runtime]] structural commitment that governs all platform service deployments.

## What is used instead

A native binary in a `pointsav-public` GCE image family, versioned and promoted through the standard release process. A systemd unit with an `ExecStart` pointing to the binary. OpenTofu for VM provisioning and lifecycle management. An idle-shutdown timer that stops the instance when the inference queue is empty. GCS-cached model weights so the cold-start path fetches from Cloud Storage rather than downloading from the upstream registry on each boot. Secret Manager for API keys. nginx for TLS termination. CUDA drivers baked into the GCE image at build time.

## SMB economics

A preemptible A100 80 GB instance costs approximately $0.50–0.70 per hour on Google Cloud. A daily 30-minute active window costs approximately $0.25–0.35 per day, or roughly $7–10 per month. The economics close because idle-shutdown is the load-bearing primitive: the instance is on for exactly the moments inference is running, not for operator convenience. For an SMB running nightly continued-pretraining cycles, zero-idle-cost GPU is the only structure that makes the economics viable at that scale.

## Cold-start: the one honest concern

A GCE GPU instance from stopped state takes approximately 60–120 seconds to reach inference-ready state. For latency-critical workloads where a sub-minute response is required, the deployment should extend `idle_shutdown_minutes` to keep the instance warm. For nightly batch workloads — the primary use case for continued pretraining and large-scale corpus extraction — the cold-start cost is the price of zero idle cost and is a reasonable trade.

## Operational artefacts

The full deployment stack for a Yo-Yo inference instance consists of: an OpenTofu module for instance lifecycle management; the GCE image (CUDA driver + vLLM + nginx + idle-shutdown timer + systemd unit); Secret Manager entries for the bearer token and provider API keys; Cloud Logging configuration pointing to the customer's own GCP project; and a Cloud Billing budget with a Pub/Sub kill-switch as defence-in-depth against runaway spend. The operator never interacts with the instance directly during inference; the systemd unit and idle-shutdown timer handle the lifecycle autonomously.

## What this rules out

Managed container orchestration platforms, container runtime systems, multi-cloud abstraction frameworks, OCI image registries, layered Docker build caching, and container build pipelines. These categories are not excluded because they are inferior in general; they are excluded because they introduce operator surface that is inconsistent with the [[zero-container-runtime]] structural commitment and the SMB economics case described above.

## See also

- [[zero-container-runtime]] — the structural commitment underlying this deployment pattern; applies across all platform service rings
- [[doorman-protocol]] — the Tier B routing path that dispatches to Yo-Yo pool instances
- [[substrate-without-inference-base-case]] — the substrate functions fully without Tier B; inference is additive
