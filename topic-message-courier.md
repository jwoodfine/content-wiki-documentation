---
schema: foundry-doc-v1
title: "Message Courier Service"
slug: topic-message-courier
category: services
type: topic
quality: stub
short_description: "The message courier service is a headless web-automation engine that bridges internal identity ledgers with external web portals using runtime-injected adapters, keeping proprietary operational logic out of the open-source monorepo."
status: pre-build
last_edited: 2026-04-30
editor: pointsav-engineering
cites: []
paired_with: topic-message-courier.es.md
---

# Message Courier Service

> The message courier service is a headless automation engine that reads pending dispatch records from an internal ledger, executes portal interactions via private runtime adapters, and writes completion timestamps back without embedding any client-specific logic in the open-source codebase.

**`service-message-courier`** is a headless web-automation and
messaging component designed to bridge `service-people`, the
internal identity ledger, with external web portals. The service
operates as a generic execution engine: all portal-specific logic
is supplied at runtime through the adapter pattern, so the core
engine remains free of hard-coded selectors, credentials, or
target URLs. The adapter directory (`private-adapters/`) is
excluded from version control so proprietary client operational
data never enters the public Git history.

## Adapter pattern

The core engine contains no knowledge of any specific portal or
site. Operational logic — CSS selectors, URL shapes, authentication
flows — is injected at runtime via scripts placed in
`private-adapters/`. This directory is explicitly excluded by
`.gitignore`. The separation means the open-source monorepo
remains tenant-agnostic while each deployment instance carries its
own private adapter set.

## Operational flow

The courier follows a three-step cycle per dispatch:

1. **Query.** The engine polls the local ledger for pending
   dispatch records.
2. **Execution.** It mounts the specified private adapter and runs
   the headless browser routine against the target portal.
3. **Write-back.** On success, the engine logs the completion
   timestamp to the ledger and unloads the adapter.

Each step is isolated. A failure at execution does not corrupt the
ledger record; the dispatch remains pending until a successful
write-back closes it.

## See Also

- [[topic-ontological-governance|Ontological Governance]]
- [[topic-verification-surveyor|Verification Surveyor]]
- [[topic-sovereign-telemetry|Zero-State Telemetry Architecture]]

## References
