---
schema: foundry-doc-v1
title: "Workspace services slice — cgroup partitioning for multi-developer environments"
slug: foundry-services-slice-model
short_description: "A systemd cgroup memory reservation that protects production services from being evicted by heavy build or research processes on the same host — single-node isolation without Kubernetes."
language: en
category: architecture
index_group: customer-ownership-and-deployment
type: topic
content_type: topic
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-07-18
editor: pointsav-engineering
cites: []
paired_with: foundry-services-slice-model.es.md
---

The [[pointsav-overview|PointSav]] development environment runs production services and interactive engineering sessions on the same Linux host. The workspace services slice pattern ensures that build-session resource bursts do not starve the inference and ledger services that other operators depend on during the same session.

## Key Takeaways

- `foundry-services.slice` reserves 12G of RAM (`MemoryMin=12G`, on a 31G host) that the kernel will not reclaim from the platform's services even under severe host memory pressure — a guarantee, not a ceiling.
- One service, `local-content` (the entity graph), carries additional protection: a 2G `MemoryMin` of its own plus `OOMScoreAdjust=-200`, making it a late candidate for the kernel's last-resort kill. No other service currently carries this protection.
- This is not Kubernetes. No scheduler, no replica controller, no service mesh, and no CPU-weight scheduling — just a memory reservation plus one service's OOM protection. Appropriate for a single-node deployment of up to roughly 12 services.
- The cgroup discipline carries forward when scale increases. The per-service `Slice=` drop-in pattern is compatible with more complex multi-node orchestration.

## Resource contention on a shared host

The [[pointsav-overview|PointSav]] development environment runs production services and interactive engineering sessions on the same Linux host. Platform services (the local SLM, [[doorman-protocol|Doorman]], [[service-content|content graph]], ledger writer, and proofreader) share memory with multi-operator build sessions and research/GIS batch processes. Without protection, a memory-heavy process outside the slice can evict a platform service's working set under host pressure — service-content was observed hitting this exactly, going unresponsive when an external Python process exhausted host RAM.

## A memory reservation, not a CPU or OOM-ordering scheme

`foundry-services.slice` sets `MemoryMin=12G` on a 31G host: a floor the kernel will not reclaim below for any service in the slice, even under severe pressure — sized as the local SLM's ~7G working set, `local-content`'s own 2G reservation, and a 3G buffer for the rest. There is no `CPUWeight` setting anywhere in this slice or anywhere else in the monorepo; CPU scheduling is not part of this mechanism.

Only `local-content` carries additional protection beyond the slice-wide floor: its own `MemoryMin=2G` (plus `MemoryHigh=5500M`, `MemoryMax=6G`, and `MemorySwapMax=0` — it is never swapped, since a partially-swapped entity graph can't serve real-time queries), and `OOMScoreAdjust=-200`. That negative score tells the kernel's OOM killer to treat `local-content` as a late candidate — the graph takes minutes to rebuild if killed. No other platform service (`local-doorman`, the local SLM) carries its own `OOMScoreAdjust` setting today; a three-tier hierarchy is described in `local-content`'s own configuration comments as the rationale for its value, but only `local-content`'s own score is actually applied.

## Single-node scope without Kubernetes

This is not orchestration in the Kubernetes sense — there is no scheduler, no replica controller, no service mesh. systemd is enough. The pattern scales to roughly a dozen services on a single GCE VM, the compact single-node configuration that characterises a minimal sovereign deployment. Beyond that scale, the architecture changes — but the cgroup discipline carries forward.

Installed as `/etc/systemd/system/foundry-services.slice`, plus per-service memory and OOM-protection drop-ins under each protected service's own `.service.d/` directory.

## See also

- [[multi-engine-session-coordination]] — how concurrent AI-coding sessions coordinate access to the same workspace to prevent index corruption
- [[cargo-target-per-user-discipline]] — per-user build cache separation for the same multi-developer scenario
- [[totebox-session]] — the session model that individual developer workstreams follow within this environment
- [[totebox-orchestration-development]] — the orchestration pattern at the development-environment layer
