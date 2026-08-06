---
schema: foundry-doc-v1
title: "Developer guide index"
slug: guide-catalog
short_description: "Developer guide index for the PointSav platform — task-oriented how-to guides organised by concern, from toolchain setup to session lifecycle."
category: reference
index_group: platform-orientation
type: topic
content_type: topic
status: stable
last_edited: 2026-07-11
editor: pointsav-engineering
paired_with: guide-catalog.es.md
aliases:
  - developer-guide-index
---

> **Operator guides** for platform deployments are maintained separately in the Woodfine fleet deployment catalog. Those are operational documents for system operators and are not listed here.

The Developer Guide Index lists the task-oriented how-to guides for the PointSav platform, organised by developer concern. Each guide covers a specific task a developer performs when building with or deploying the platform. For the underlying architecture that each guide draws on, follow the article wikilinks within each guide.

Internal operator runbooks for the Woodfine fleet deployment are not listed here — they are operational documents for provisioning and maintenance, not public developer guides.

## Getting started

These guides cover the first steps for a developer new to the platform — setting up the toolchain, authenticating a device, and opening a working session.

- [[pair-a-new-device]] — register a new device with the pairing server and get it approved onto the network
- [[install-toolchain]] — install the Rust compiler and the workspace commit helper on a workspace VM
- [[open-first-totebox-session]] — open a scoped working session in a Totebox Archive and navigate the session lifecycle
- [[explore-the-console]] — tour the three-zone TUI, read the status bar, and navigate F-key slots for the first time

## Working in the console

These guides cover the platform's terminal interface and its F-key Cartridge slots.

- [[navigate-console-tui]] — the real screen layout and status bar fields, and switching slots without losing state
- [[use-f-key-model]] — what F3, F9, and F12 actually do, correcting two invented behaviors
- [[read-the-command-ledger]] — page ledger entries and fetch a signed checkpoint over service-fs's real HTTP API
- [[run-first-slm-query]] — the real path to a first inference request, since F9 has no query interface at all

## Records & storage

These guides cover the WORM audit ledger and entity data operations.

- [[read-write-totebox-archives]] — the five-step session start reading protocol, commit flow, draft staging, cross-archive mailbox
- [[verify-worm-ledger]] — verify a ledger entry against a fetched checkpoint using only curl and SHA-256
- [[query-the-datagraph]] — the real query_datagraph/get_entity_context tools, and why DataGraph availability isn't a Doorman tier
- [[export-structured-data]] — the three real export paths, since a fourth in an earlier version of this guide didn't exist

## Machine authorization

These guides cover the credential and admission mechanisms that gate who and what can act
on the platform — device pairing, service-to-service capability tokens, fleet node
enrollment, and signed binary downloads. These are separate mechanisms, not one system
under different names.

- [[pair-a-new-device]] — register a device with the pairing server and get it approved onto the WireGuard mesh
- [[issue-capability-token]] — mint an Ed25519-signed capability token and register it with a peer service
- [[rotate-keys]] — replace a credential within the system's real 24-hour expiry limits; there is no revocation mechanism
- [[enroll-ppn-node]] — start the per-node heartbeat agent and confirm it in the fleet controller
- [[authenticate-binary-downloads]] — confirm an order and follow the signed download path for a release

For the authorization model that underpins all these operations, see [[machine-based-auth]] and [[pairing-as-permission]].

## Multi-entity scale

These guides cover operating the platform across multiple tenants, users, and fleet nodes.

- [[configure-tenant-namespace]] — register a tenant namespace, set quota limits, verify isolation, and issue the root credential
- [[scale-user-tiers]] — promote users between READ / USER / INPUT tiers; bulk-update a team at scale
- [[add-a-fleet-node]] — enroll a second PPN node into a running fleet without interrupting existing nodes

## Integration & data

These guides cover consuming platform data and connecting external applications.

- [[build-a-colocation-map]] — authenticate against the GIS tile API and render tier-coloured cluster markers in MapLibre
- [[connect-osm-data-pipeline]] — write a chain ingest YAML, run the ingest script against the Overpass API, and rebuild the cluster layer
- [[federate-archives-via-content-mounts]] — declare a secondary content mount in `knowledge.toml` and access federated articles across instances
- [[use-knowledge-mounts]] — add a secondary content repository to a running wiki instance and verify slug isolation

## Self-hosting

These guides cover deploying and running platform components on operator-controlled infrastructure.

- [[self-host-a-deployment]] — provision a named deployment instance, start the gateway, and connect it to the upstream platform
- [[configure-doorman]] — configure Tier A/B/C upstream addresses, circuit-breaker thresholds, and verify the health endpoint
- [[deploy-knowledge-instance]] — build and start `app-mediakit-knowledge` pointed at a local content repository path
- [[run-local-slm-inference]] — start the local SLM service, verify Doorman Tier B, and submit inference requests from the console or API

## See also

- [[machine-based-auth]] — the machine-based authorization model underlying all platform access
- [[totebox-orchestration-development]] — the session orchestration model that governs how Totebox Archives are used
- [[app-mediakit-knowledge]] — the wiki engine serving this documentation instance
