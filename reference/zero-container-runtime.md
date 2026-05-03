---
schema: foundry-doc-v1
title: "Zero-Container Runtime"
slug: zero-container-runtime
category: reference
type: topic
quality: published
short_description: The structural commitment that every PointSav deployment runs as a Linux binary under systemd on a plain virtual machine or bare-metal host, with no container runtime, container orchestrator, or managed-runtime platform.
status: pre-build
last_edited: 2026-05-01
editor: pointsav-engineering
cites: []
paired_with: zero-container-runtime.es.md
---

Every PointSav deployment — across all service rings, all compute tiers, and all deployment contexts from the reference implementation to a future appliance deployment — runs as a Linux ELF binary supervised by systemd on a plain virtual machine or bare-metal host. No container runtime. No orchestrator. No managed-runtime platform.

This is a structural commitment, not a phase-one pragmatic choice. It does not relax in later versions, and the burden of proof for revisiting it falls on a proposal demonstrating that the principle has produced a material disadvantage that cannot be addressed within the principle.

## Why this is structural, not pragmatic

**Plain-text inspectability.** Container images are binary artefacts processed by container runtimes. Both add opacity over the filesystem. A systemd unit file and a Linux binary on a filesystem are fully inspectable with standard tools: the process table shows what is running, the journal shows what happened, the unit file shows how the process is configured. The filesystem is the truth.

**Customer sovereignty.** A customer running software inside a container they did not build, on a runtime they do not control, is one platform decision away from disruption. Container runtime platforms can change pricing, policy, or availability without the customer's input. A systemd-managed binary on a Linux virtual machine is portable to any Linux host — any cloud provider, customer on-premise infrastructure, or appliance — without modification. The customer controls the substrate.

**Long-horizon readability.** ELF binaries and systemd unit files have been the standard on Linux since the 1990s and 2010s respectively. Container runtime ecosystems depend on image format specifications and registry infrastructure that has undergone substantial change even within a decade. The surface area that must remain stable for a binary to run in twenty years is far smaller than the surface area that must remain stable for a containerised application to run in twenty years.

**SMB economics.** Small and medium-sized businesses — the target customer for PointSav deployments — cannot reasonably maintain container infrastructure. An operator at a small clinic can run `systemctl status` and read the answer in plain text. Debugging container orchestration requires specialist knowledge that most SMB operators do not have and should not need.

**Compounding loop integrity.** The substrate that generates training signal from customer interactions must traverse the full path from edge to centre and back without crossing platform boundaries that obscure provenance. Container layers introduce provenance opacity that is incompatible with the audit discipline the substrate requires.

## What this rules out

The following are not used in any PointSav deployment path: Docker and Docker Compose in any form, including for local development; Podman; Cloud Run in either the standard or GPU variant; AWS ECS and Fargate; Kubernetes in any flavour including managed variants; Modal; container registries; and OCI image formats whether built or consumed.

## What is used instead

Process supervision is handled by systemd units. Linux ELF binaries are packaged for distribution as native binaries, optionally installed via Debian packages or the language-native package manager where appropriate. Service discovery uses DNS and static addressing with systemd target dependencies. Configuration lives in plain text files under `/etc/` or in systemd environment files. Secrets are fetched from the cloud secret manager at boot and held in a memory-backed filesystem rather than written to disk. Logging routes through journald and optionally to cloud log collection. GPU acceleration uses the CUDA driver installed via the system package manager; the inference binary communicates with the driver directly.

For Tier B burst compute — the preemptible GPU instances used for large model inference — the Doorman service starts the virtual machine ahead of an anticipated workload and shuts it down after an inactivity window. The startup-to-first-inference latency for this path is sixty to one hundred twenty seconds, which is longer than a managed container platform's cold-start time. This latency is acceptable for asynchronous ingest pipelines; for synchronous workflows, a warm-VM mode holds the instance running between requests within a configurable window.

## The trade-off, stated plainly

The commitment accepts a longer cold-start time for burst compute compared to managed container platforms, and accepts that declarative cluster orchestration with rolling updates requires OpenTofu applied to systemd units rather than a purpose-built orchestration control plane.

In exchange: every running process on every deployment is visible to the customer with standard system administration tools. The same binary and unit file runs on any Linux host without modification. There is no container layer to peel back when answering questions about what was running at a specific moment. Billing is straightforward: virtual machine pricing is per-second, and the instance costs nothing beyond disk and reserved IP when it is stopped.

## Future-proofing

The principle applies without time limit. If a future technical review under the framework's constitutional amendment process demonstrates that the principle has produced a material disadvantage that cannot be addressed within the principle's constraints, a formal proposal may be brought. Until such a proposal is made and ratified, the principle is the operative rule.

## See also

- [[service-slm-operationalization-plan]] — The compute routing architecture that applies this principle across Tier A, B, and C.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
