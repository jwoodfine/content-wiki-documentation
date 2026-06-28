---
artifact: topic
schema: foundry-draft-v1
status: draft
language_protocol: TOPIC
route: project-editorial
target_wiki: documentation.pointsav.com
created: 2026-06-20
session: Session 111 (Command@claude-code)
research_trail:
  source_briefs: [command-10x-dev-environment]
  cross_checks: [BRIEF-10x-dev-environment.md, pairings.yaml, AGENT.md]
  forbidden_terms_cleared: false
---

# Scaling Coordinated Development Across Many Sovereign Archives

The `app-orchestration-command` topology is designed to accommodate growth. This article describes the coordination challenges that appear as the number of Totebox Archives increases, the mechanisms introduced to address them, and the planned trajectory toward per-archive process isolation.

## The Coordination Challenge

When a small number of archives share a central coordinator, the coordinator's overhead is manageable — a human operator can relay inter-archive messages, review publication requests one by one, and maintain the queue manually. As the archive count grows past ten or twenty, three bottlenecks emerge:

1. **Publication serialization.** Each archive that wants its code in canonical history must wait for the coordinator to run the publication sequence. If the coordinator is occupied with another archive — or simply not running — the queue grows.
2. **Message relay latency.** Archives communicate through a file-based message system. Without automation, messages sit in an archive's outgoing queue until a coordinator operator manually delivers them to the destination. With 21 archives, this becomes a recurring manual task.
3. **Operator cognitive load.** The coordinator operator must track the state of every archive simultaneously: pending publication requests, outstanding messages, blocked work items, and operational alerts. At scale, this is unsustainable.

## The Decentralized Publication Path

The first mitigation is a tiered eligibility model. Archives that have demonstrated operational maturity — consistently passing their build and test suites, maintaining clean histories, and operating without frequent interventions — may be granted a higher self-service level.

At the highest self-service level *(planned/intended)*, an archive may initiate canonical publication directly, without waiting for the coordinator operator to act. The prerequisite is that the administrator key is accessible from the archive's environment. The coordinator validates the result after the fact and records the publication event in the audit ledger.

This does not eliminate the coordinator's role; it offloads routine, low-risk publication to the archives that have earned that trust, reserving coordinator attention for higher-stakes decisions.

## The Messaging Substrate

Inter-archive messages are written to a structured, git-tracked file format — one per archive, prepend-only, with schema-validated frontmatter. This format is auditable, diff-able, and recoverable from the archive's git history.

A relay service *(planned/intended)* will automate message delivery: on a regular cadence, it will scan each archive's outgoing message queue, read the declared destination, and write each message to the destination archive's incoming queue using the canonical write path. The coordinator operator's manual relay step will be replaced by a background timer.

### Why Not a Message Broker

Alternatives such as NATS or RabbitMQ were evaluated and declined for this use case:

- **Message rate mismatch.** Inter-archive messages arrive over hours and days, not milliseconds. A broker optimised for high-throughput, low-latency messaging introduces infrastructure complexity that the actual message rate does not justify.
- **Duplicate source of truth.** The file-based message format is already git-tracked and versioned. Introducing a broker would create a second authoritative record of message state, with no clear rule for which to trust when they diverge.
- **Dependency surface.** A broker is an additional long-running service that must be installed, monitored, and kept consistent with the git record. The file-based system runs without any external runtime.

The relay service adds automation without adding a broker: it reads and writes the same file format that already exists.

## Per-Operator Isolation

The current model runs all Totebox Archives under a shared system user. Each archive can read and write any other archive's files, limited only by filesystem group permissions.

A planned trajectory *(planned/intended)* assigns each Totebox Archive to a specific operator (Linux user). That operator owns the archive's filesystem and is the exclusive holder of its commit identity. Archives owned by different operators cannot write to each other's state files without explicit escalation. This mirrors the intended production topology, in which each archive runs as a dedicated `os-totebox` instance with full process isolation.

The transition from shared-user to per-operator isolation is incremental. The first step is provisioning key material for each operator so they can commit from their own shell sessions. Subsequent steps assign archive directory ownership and restrict cross-archive filesystem access.

## Trajectory

The current `app-orchestration-command` installation operates 21 archives in a shared-user environment on a single `os-orchestration` host. It is a working prototype of the target architecture.

The planned production topology maps each archive to a dedicated `os-totebox` instance — a single-purpose compute node running the archive's services, with its own operator user, commit identity, and network boundary. `app-orchestration-command` on `os-orchestration` remains the publication coordinator and audit authority; it does not disappear, but its role becomes coordination rather than execution.

This topology is the subject of ongoing architecture work. Current documentation on the `os-orchestration` and `os-totebox` models is maintained separately; see the related topics below.

## Related Topics

- [How app-orchestration-command Publishes Archive Changes](TOPIC-app-orchestration-command-publication-flow.draft.md) — the publication flow and eligibility model
- [The Per-Archive Branch Model in app-orchestration-command](TOPIC-app-orchestration-command-branch-model.draft.md) — isolation and filtering
- *os-orchestration architecture* — maintained in the project-data TOPIC series
- *os-totebox sovereign archive model* — maintained in the project-data TOPIC series
