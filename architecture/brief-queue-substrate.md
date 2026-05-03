---
schema: foundry-doc-v1
title: "The Brief Queue Substrate"
slug: brief-queue-substrate
category: architecture
type: topic
quality: core
short_description: "A durable file-backed queue that makes idle-shutdown Yo-Yo compute viable without losing apprenticeship corpus capture data — the durability layer of the three-tier SLM substrate."
status: pre-build
last_edited: 2026-04-30
editor: pointsav-engineering
cites:
  - ni-51-102
  - osc-sn-51-721
paired_with: brief-queue-substrate.es.md
---

The **Brief Queue Substrate** is a durable, file-backed queue that sits between the editorial pipeline and the apprenticeship corpus capture system inside the PointSav platform. Its primary function is to accept brief-execution records — JSON Lines events describing an editorial operation — and hold them reliably until the drain worker can write them to the long-term corpus. This decoupling is what makes Yo-Yo idle-shutdown viable: when the GPU instance shuts down mid-session to avoid idle billing, no in-flight corpus event is lost. The queue itself persists on disk; the drain worker picks up where it left off when the next session begins. The substrate also absorbs spot preemption events from cloud providers, simplifies the capture-edit pipeline by removing inline write dependencies, and positions the platform for the eventual PointSav-LLM continued-pretraining path. It is a deliberate structural choice that keeps the apprenticeship corpus growing continuously regardless of compute-tier availability.

## What the queue is

The queue is four directories arranged as a state machine for JSONL event files:

- **`queue/`** — incoming events land here. Any process that generates a brief-execution record writes an atomic file into this directory. No lock is required at write time.
- **`queue-in-flight/`** — the drain worker atomically renames a file from `queue/` into `queue-in-flight/` when it begins processing. The rename is the lease acquisition. If the drain worker crashes mid-write, the file remains in `queue-in-flight/` and is recoverable on restart.
- **`queue-done/`** — after the drain worker successfully appends the event to the corpus JSONL file, it moves the file here. Files in `queue-done/` are safe to archive or delete on a scheduled basis.
- **`queue-poison/`** — files that cannot be parsed, fail schema validation, or exhaust a configurable retry limit are moved here for human inspection. Poison files do not block the rest of the queue.

Each file in the queue is a single JSONL event serialized to disk. File names are constructed from a timestamp plus a random suffix to ensure uniqueness across concurrent writers without requiring coordination. The four-directory structure makes queue state visible at a glance using standard filesystem tools — no daemon is required to inspect it.

## What the queue enables

The Brief Queue Substrate delivers five operational properties that the platform depends on:

**Yo-Yo idle-shutdown tolerance.** The Yo-Yo compute tier (OLMo 3.1 32B Think on GPU burst) shuts down after a configurable idle period to avoid unnecessary billing. Without the queue, any brief-execution event generated during a Yo-Yo session would need to be written to the corpus synchronously before shutdown — coupling the SLM's inference loop to disk I/O and adding latency to every inference call. With the queue, the inference loop writes to `queue/` (a fast local write) and the drain worker handles corpus persistence independently. Shutdown can proceed as soon as the inference completes; no corpus writes are in progress.

**Spot preemption tolerance.** Cloud spot and preemptible instances can be reclaimed with minimal notice. Events sitting in `queue/` or `queue-in-flight/` survive preemption because the queue directory is on persistent storage, not instance-local ephemeral storage. When a replacement instance starts, the drain worker resumes from the last committed position.

**Capture-edit pipeline simplification.** The previous pattern required the capture pipeline to write directly to corpus JSONL files during the editorial session, which created ordering dependencies between the Doorman's audit-routing logic and the corpus file's append position. The queue removes that dependency: the Doorman writes an event record to `queue/` and returns immediately; the drain worker serializes corpus appends in arrival order without blocking the inference path.

**Customer Tier 1 alignment.** The queue architecture matches the pattern that Ring 1 ingest services (service-fs, service-people, service-email, service-input) already use for durable event capture at the tenant boundary. A customer extending the platform with an additional MCP server can use the same four-directory queue pattern for their ingest events. Consistency across tiers reduces the surface area a contributor needs to understand.

**Future PointSav-LLM readiness.** The apprenticeship corpus — the accumulation of draft-created, draft-refined, and creative-edited JSONL events — is the intended training signal for a future PointSav-LLM continued-pretraining run [1]. The Brief Queue Substrate ensures that corpus growth is uninterrupted by compute-tier transitions, idle shutdowns, or preemption events. Every editorial session contributes to the corpus regardless of which compute tier handled the inference.

## Lease mechanics

The queue preserves correctness under concurrent drain workers and process crashes through an atomic rename lease pattern. The sequence is:

1. The drain worker scans `queue/` for candidate files.
2. For each candidate, it attempts `rename(queue/<file>, queue-in-flight/<file>)`. This is an atomic filesystem operation on POSIX-compliant filesystems: exactly one worker succeeds; all others see a "no such file" error and move on.
3. The winning worker reads the event, validates the schema, and appends to the corpus JSONL file.
4. On success, it renames from `queue-in-flight/<file>` to `queue-done/<file>`.
5. On failure (parse error, schema validation failure, or retry exhaustion), it renames to `queue-poison/<file>`.

At startup, the drain worker scans `queue-in-flight/` for files left by a previous crashed instance. It reprocesses those files before picking up new ones from `queue/`. This guarantees at-least-once delivery: an event may be appended to the corpus more than once if the drain worker crashes between the corpus append and the rename to `queue-done/`. Consumers of the corpus deduplicate by event ID where idempotency matters.

The lease pattern does not require a network round-trip, a lock daemon, or a message broker. It requires only that the four directories share a filesystem where `rename()` is atomic — a property guaranteed by every POSIX-compliant local filesystem and by most network filesystems when source and destination are on the same mount.

## File-JSONL compared to message brokers

The Brief Queue Substrate stores events as JSONL files on a local filesystem rather than routing them through a hosted message broker. This is an intentional architectural choice grounded in the platform's sovereignty posture and operational constraints, not a limitation to be remedied later.

Message brokers such as NATS JetStream or Redis Streams offer strong durability guarantees and rich consumer-group semantics. They also introduce a persistent network dependency: the producer cannot write if the broker is unreachable, and the consumer cannot read if the broker has lost its state. For a single-tenant workspace where the queue producer, queue consumer, and corpus storage are all on the same machine or the same cloud-persistent volume, the network round-trip adds latency and a failure mode without adding a capability the platform needs at this scale.

JSONL files have a further advantage for this use case: they are directly inspectable. An operator investigating a corpus anomaly can read a file in `queue-poison/` with any text editor. A message broker entry requires the broker's own query interface. The four-directory layout makes queue depth, in-flight count, and poison-file count observable with a single `find` or `ls -l` invocation — no broker dashboard required.

The file-JSONL choice also aligns with DOCTRINE Pillar 1: plain text only. The corpus itself is JSONL; the queue payload format matches the corpus format; the drain worker's only job is to move events from one JSONL context (queue file) to another (corpus file). The entire path is auditable as plain text with no binary state.

When the platform scales to multi-node corpus producers — a planned future state — the queue directory can be placed on a shared network filesystem (NFS, Cloud Filestore, or an equivalent) and the lease mechanics continue to hold on POSIX-compliant mounts. Alternatively, that future state may introduce a message broker as a speed layer while retaining the JSONL corpus format. The choice remains open and is not foreclosed by the current design.

## Implementation status

The Brief Queue Substrate convention was ratified at workspace v0.1.78 / Doctrine v0.0.14. Implementation is in progress under the project-slm cluster scope.

The functional components being built are:

- **Queue API** — four operations exposed to producers: `enqueue` (write an event file to `queue/`), `dequeue` (atomically lease a file from `queue/`), `release` (move from `queue-in-flight/` back to `queue/` on non-fatal error), and `poison` (move to `queue-poison/` on fatal error).
- **Background drain worker** — a long-running process inside the Doorman that polls `queue/` at a configurable interval, processes leased files, and appends to the corpus JSONL. The drain worker also performs startup recovery of any files stranded in `queue-in-flight/`.
- **Post-commit hook graduation** — the current capture-edit pipeline writes corpus events inline during the editorial session. Once the queue API is available, the post-commit hook is updated to write to `queue/` instead of directly to the corpus file. The corpus write path is then exclusively the drain worker's responsibility.

The implementation does not change the corpus JSONL schema. Consumers of the apprenticeship corpus — including the future PointSav-LLM pretraining pipeline — observe no change in corpus format; only the write path changes.

## See Also

- [[apprenticeship-substrate]] — the apprenticeship corpus the Brief Queue Substrate feeds into; Doctrine claim #32
- [[service-slm-yoyo-operational]] — the Yo-Yo operational state that motivated the queue's idle-shutdown tolerance requirement
- [[service-slm]] — the Doorman service that hosts the drain worker and enforces audit-routing discipline

## References

1. PointSav Doctrine claim #32 — Apprenticeship Substrate: every editorial Task session generates signed draft-created / draft-refined / creative-edited JSONL events that form the continued-pretraining corpus for a future PointSav-LLM.
2. `conventions/apprenticeship-substrate.md` §7C — the signal-complete acknowledgment that established the queue as a required durability layer for corpus capture.
3. PointSav Doctrine Pillar 1 — Plain text only: structured state is stored as version-controllable plain text; binary state and daemon-held state are avoided where the operational requirement can be met by a text-based alternative.
4. DOCTRINE.md §XIV — Compounding Substrate: the three-tier compute routing pattern (Local / Yo-Yo / External API) that the Brief Queue Substrate makes operationally continuous across tier transitions.

---

## Provenance

This article was drafted based on architectural documentation describing the four-directory queue design, the Yo-Yo idle-shutdown operational requirement, and the apprenticeship corpus capture pipeline. Source materials consulted include the apprenticeship substrate convention, the Yo-Yo operational runbook and its associated startup procedure, the Foundry Doctrine's treatment of the Compounding Substrate, and session trajectory logs from the project-slm cluster documenting the rationale for the file-JSONL approach. The §7C signal-complete acknowledgment from the apprenticeship substrate convention was the proximate event that established the queue as a required structural component.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
