---
schema: foundry-doc-v1
title: "Workspace services slice — cgroup partitioning for multi-developer environments"
slug: foundry-services-slice-model
short_description: "systemd cgroup partitioning that gives production services twice the CPU weight of interactive build sessions — single-node isolation without Kubernetes."
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

- `foundry-services.slice` gives production services 2× CPU scheduler weight vs. a single interactive user shell. Under contention, services win over build jobs.
- Memory ceilings (`MemoryHigh=11G`) prevent any one service from pinning the full 16 GiB VM memory. The OOMScoreAdjust ordering — sshd at −1000, local-fs at −500, local-doorman at −300, local-slm at +500 — means the kernel kills cheap-to-restart services first.
- This is not Kubernetes. No scheduler, no replica controller, no service mesh — just systemd cgroup partitioning. Appropriate for a single-node deployment of up to roughly 12 services.
- The cgroup discipline carries forward when scale increases. The per-service `Slice=` drop-in pattern is compatible with more complex multi-node orchestration.

## Resource contention on a shared host

The [[pointsav-overview|PointSav]] development environment runs production services and interactive engineering sessions on the same Linux host. Platform services (the local SLM, [[doorman-protocol|Doorman]], [[service-content|content graph]], ledger writer, and proofreader) share CPU and memory with multi-operator build sessions. Without resource isolation, a heavy `cargo build` in one operator's session can starve the inference service that another operator is relying on.

## CPU weights, memory ceilings, and OOM ordering

An initial hardening pass introduced `foundry-services.slice` — a systemd cgroup partition with `CPUWeight=200` and `MemoryHigh=11G` that holds every `local-*.service`. Default systemd user slices (`user-1001.slice`, `user-1002.slice`) sit at `CPUWeight=100`, so under CPU contention the service group receives 2× the scheduler weight relative to a single interactive shell. Memory ceilings prevent any one service from pinning more than approximately 11 GiB on a 16 GiB VM; with `OOMScoreAdjust` ordering (sshd −1000, local-fs −500, local-doorman −300, local-slm +500), the kernel's last-resort kill prefers cheap-to-restart services over the WORM ledger writer or the operator's SSH connection.

**Correction (2026-07-18):** the live `foundry-services.slice` in the monorepo
(`infrastructure/systemd/foundry-services.slice`) does not match this description. It sets
`MemoryMin=12G` (a memory-reservation guarantee against eviction under host pressure, sized
against a 31G host, not an 11G ceiling on a 16G VM) — no `CPUWeight` setting appears anywhere
in the slice file, and a repo-wide search finds `CPUWeight` nowhere in the monorepo at all.
The mechanism described in the file's own comments is different in kind: per-service
`MemoryMin` budgeting (local-content/LadybugDB gets a 2G guarantee; local-slm and
local-doorman have none set) rather than a CPU-weight/OOMScoreAdjust scheme. The only
`OOMScoreAdjust` setting found anywhere in the monorepo is on `local-content` (`-200`,
"moderately protected") — not the four-service sshd/local-fs/local-doorman/local-slm
ordering this article describes. **Flagged, not silently rewritten** — this reads as an
earlier design superseded by a simpler memory-reservation-only mechanism, but needs
project-totebox confirmation before the CPU-weight and OOM-ordering claims are corrected
or removed.

## Single-node scope without Kubernetes

This is not orchestration in the Kubernetes sense — there is no scheduler, no replica controller, no service mesh. systemd is enough. The pattern scales to roughly a dozen services on a single GCE VM, the compact single-node configuration that characterises a minimal sovereign deployment. Beyond that scale, the architecture changes — but the cgroup discipline carries forward.

Where this lives on disk: `/etc/systemd/system/services.slice`, plus `Slice=` drop-ins under `/etc/systemd/system/local-*.service.d/slice.conf`. The version-controlled source mirrors live under the monorepo's `infrastructure/` directory.

**Correction (2026-07-18):** the version-controlled source names do not match those paths.
The slice file is `infrastructure/systemd/foundry-services.slice` (not `services.slice`),
and the only matching drop-ins found are `local-content-memory.conf` and
`local-content-oom.conf` (not a generic `slice.conf` per service). Flagged alongside the
CPU-weight/OOM-ordering correction above — same underlying staleness.

## See also

- [[multi-engine-session-coordination]] — how concurrent AI-coding sessions coordinate access to the same workspace to prevent index corruption
- [[cargo-target-per-user-discipline]] — per-user build cache separation for the same multi-developer scenario
- [[totebox-session]] — the session model that individual developer workstreams follow within this environment
- [[totebox-orchestration-development]] — the orchestration pattern at the development-environment layer
