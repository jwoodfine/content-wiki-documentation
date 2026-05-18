---
schema: foundry-doc-v1
title: "Multi-Engine Session Coordination — Session Locks, boot_id, and Role Guards"
slug: multi-engine-session-coordination
language: en
category: architecture
type: topic
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-18
editor: pointsav-engineering
cites: []
paired_with: multi-engine-session-coordination.es.md
---

The development workspace supports two AI engines (Claude Code and Gemini CLI) and two human operators on the same Linux box. The coordination problem is not theoretical — when two sessions touch the same `.git/index`, the working tree corrupts in ways that are expensive to diagnose.

The protocol is intentionally minimal: each engine writes `.agent/engines/<engine-id>/session.lock` at startup. The lock carries the engine identifier, role (Command or Totebox), parent PID, ISO-8601 start time, and the boot ID from `/proc/sys/kernel/random/boot_id`. The boot ID is the key — it lets a future session decide whether a lock is stale (a different boot ID means the VM rebooted between sessions, making the lock definitively dead) or potentially live (same boot ID, check `kill -0 <pid>` for process liveness).

The [[totebox-session]] model assigns exactly one Command Session to the workspace root. That Command Session writes `role.lock` at `.agent/role.lock`; a second attempt errors out unless the operator manually clears the lock. Totebox Sessions are scoped to individual archives and write their locks under `clones/<archive>/.agent/engines/<engine-id>/session.lock`.

What this does not solve: two engines opened in the same clone. The session-lock protocol detects the conflict and warns, but does not physically prevent it — `flock` on `.git/index` does that. A planned PreToolUse hook adds a check that refuses any Bash or Write tool call in a clone whose `session.lock` shows a different live engine. `bin/foundry-health.sh` includes a cross-user `index.lock` detector that surfaces same-repo locks held by different UIDs.

Stale-lock cleanup is automatic when boot IDs disagree, manual otherwise. A cleanup pass on 2026-05-18 removed 8 such locks — 3 from a previous boot, 5 from dead PIDs in the current boot. Command Sessions should run `foundry-health.sh` early and clear stale locks before opening any archive.

## See also

- [[totebox-session]] — the session model whose concurrency guarantees this protocol protects
- [[mailbox-atomicity]] — the complementary atomic-write discipline for cross-session communication
- [[foundry-services-slice-model]] — the cgroup partition that isolates resource consumption in the same multi-developer environment
- [[totebox-orchestration-development]] — the orchestration layer these sessions operate within
