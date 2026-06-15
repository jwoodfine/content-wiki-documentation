---
schema: foundry-doc-v1
title: "Developer Guide Index"
slug: guide-catalog
category: reference
type: topic
content_type: topic
status: stable
last_edited: 2026-06-15
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

- [[pair-a-new-device]] — register a new device and assign it a pairing tier (INPUT, USER, or INTERFACE)
- [[install-toolchain]] — install the Rust compiler and the workspace commit helper on a workspace VM
- [[open-first-totebox-session]] — open a scoped working session in a Totebox Archive and navigate the session lifecycle
- [[explore-the-console]] — tour the three-zone TUI, read the status bar, and navigate F-key slots for the first time

## Working in the console

These guides cover the platform's terminal interface and its F-key Cartridge slots.

- [[navigate-console-tui]] — status bar field definitions, F-key switching, and universal key bindings
- [[use-f-key-model]] — default slot assignments, the Cartridge compilation model, Email / SLM / Input Machine slots
- [[read-the-command-ledger]] — view WORM ledger entries from the F12 LEDGER tab, understand entry types, export to C2SP format
- [[run-first-slm-query]] — submit an inference prompt in F9 and read the Doorman health dashboard

## Records & storage

These guides cover the WORM audit ledger and entity data operations.

- [[read-write-totebox-archives]] — the five-step session start reading protocol, commit flow, draft staging, cross-archive mailbox
- [[verify-worm-ledger]] — confirm hash-chain integrity using SHA-256 and validate against a signed Sigstore checkpoint
- [[query-the-datagraph]] — search named entities by plain-text query, navigate relationships, handle Tier A circuit outages
- [[export-structured-data]] — four export paths by use case: DataGraph, wiki Markdown, GeoJSON, ledger tiles

## Machine authorization

These guides cover the cryptographic device pairing that controls platform access.

- [[pair-a-new-device]] — the core pairing workflow; all four pairing types (ADMIN, INPUT, USER, INTERFACE)
- [[enroll-ppn-node]] — register a PPN compute node with the fleet controller and verify the first heartbeat
- [[issue-capability-token]] — generate a scoped Ed25519 capability token for a device or service
- [[rotate-keys]] — replace a keypair and its token using the three-phase transition sequence
- [[authenticate-binary-downloads]] — verify Ed25519-signed binary releases from the private distribution endpoint

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
