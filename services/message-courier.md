---
schema: foundry-doc-v1
title: "Message courier service"
slug: message-courier
category: services
type: topic
quality: stub
short_description: "The message courier service is a headless web-automation engine that bridges internal identity ledgers with external web portals using runtime-injected adapters, keeping proprietary operational logic out of the open-source monorepo."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-08
editor: pointsav-engineering
cites: []
paired_with: message-courier.es.md
---

**`service-message-courier`** is the headless web-automation engine that bridges the platform's internal [[service-people|identity ledger]] with external web portals — without embedding any client-specific logic in the open-source codebase. The core engine reads pending dispatch records from the [[worm-ledger-design|WORM ledger]], executes portal interactions through privately distributed runtime adapters, and writes completion timestamps back; the engine itself remains free of hard-coded selectors, credentials, or target URLs. The adapter directory (`private-adapters/`) is excluded from version control so proprietary client operational data never enters the public Git history.

## Adapter pattern

The core engine contains no knowledge of any specific portal or site. Operational logic — CSS selectors, URL shapes, authentication flows — is injected at runtime via scripts placed in `private-adapters/`. This directory is explicitly excluded by `.gitignore`. The separation means the open-source monorepo remains tenant-agnostic while each deployment instance carries its own private adapter set. This runtime-injection architecture is consistent with the [[sovereign-airlock-doctrine|sovereign airlock]] principle — proprietary client logic never crosses into the open codebase.

## Operational flow

The courier follows a three-step cycle per dispatch:

1. **Query.** The engine polls the local [[service-fs-architecture|WORM ledger]] for pending dispatch records.
2. **Execution.** It mounts the specified private adapter and runs the headless browser routine against the target portal.
3. **Write-back.** On success, the engine logs the completion timestamp to the ledger and unloads the adapter.

Each step is isolated. A failure at execution does not corrupt the ledger record; the dispatch remains pending until a successful write-back closes it. Completed write-backs are logged by [[sovereign-telemetry|zero-state telemetry]] for audit purposes.

## See also

- [[ontological-governance|Ontological Governance]] — the governance framework governing adapter permissions
- [[verification-surveyor|Verification Surveyor]] — the service that monitors daily dispatch volumes
- [[sovereign-telemetry|Zero-State Telemetry Architecture]] — telemetry layer consuming write-back events
- [[service-people]] — the identity ledger the courier bridges to external portals
