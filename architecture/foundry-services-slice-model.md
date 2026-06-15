---
schema: foundry-doc-v1
title: "Workspace services slice — cgroup partitioning for multi-developer environments"
slug: foundry-services-slice-model
language: en
category: architecture
type: topic
content_type: topic
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-25
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

The [[pointsav-overview|PointSav]] development environment runs production services and interactive engineering sessions on the same Linux host. Platform services (the local SLM, [[doorman-protocol|Doorman]], [[service-content|content graph]], ledger writer, and proofreader) share CPU and memory with multi-operator build sessions. Without resource isolation, a heavy `cargo build` in one operator's session can starve the inference service that another operator is relying on.

An initial hardening pass introduced `foundry-services.slice` — a systemd cgroup partition with `CPUWeight=200` and `MemoryHigh=11G` that holds every `local-*.service`. Default systemd user slices (`user-1001.slice`, `user-1002.slice`) sit at `CPUWeight=100`, so under CPU contention the service group receives 2× the scheduler weight relative to a single interactive shell. Memory ceilings prevent any one service from pinning more than approximately 11 GiB on a 16 GiB VM; with `OOMScoreAdjust` ordering (sshd −1000, local-fs −500, local-doorman −300, local-slm +500), the kernel's last-resort kill prefers cheap-to-restart services over the WORM ledger writer or the operator's SSH connection.

This is not orchestration in the Kubernetes sense — there is no scheduler, no replica controller, no service mesh. systemd is enough. The pattern scales to roughly a dozen services on a single GCE VM, the compact single-node configuration that characterises a minimal sovereign deployment. Beyond that scale, the architecture changes — but the cgroup discipline carries forward.

Where this lives on disk: `/etc/systemd/system/services.slice`, plus `Slice=` drop-ins under `/etc/systemd/system/local-*.service.d/slice.conf`. The version-controlled source mirrors live under the monorepo's `infrastructure/` directory.

## See also

- [[multi-engine-session-coordination]] — how concurrent AI-coding sessions coordinate access to the same workspace to prevent index corruption
- [[cargo-target-per-user-discipline]] — per-user build cache separation for the same multi-developer scenario
- [[totebox-session]] — the session model that individual developer workstreams follow within this environment
- [[totebox-orchestration-development]] — the orchestration pattern at the development-environment layer
