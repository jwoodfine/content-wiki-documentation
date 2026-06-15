---
schema: foundry-doc-v1
title: "Developer Guides"
slug: how-to
category: how-to
content_type: how-to
type: topic
status: active
last_edited: 2026-06-14
editor: pointsav-engineering
paired_with: _index.es.md
---

Step-by-step developer guides for building with and on the PointSav platform. Each guide addresses a specific task — follow it start to finish, then refer back to the related architecture articles when you need the underlying theory.

For the concepts behind each guide, start in [[architecture]] or [[patterns]]. For platform architecture overview, see [[totebox-orchestration-development]].

## Getting started

The foundation: authenticate your device, install the toolchain, and open your first session.

- [[pair-a-new-device|Pair a new device]] — enroll a machine using machine-based authorization; no username or password required
- [[install-toolchain|Install the development toolchain]] — set up Rust and the staging-tier commit helper on a workspace VM
- [[open-first-totebox-session|Open your first Totebox session]] — navigate to an archive, read your inbox, and start contributing
- [[explore-the-console|Explore the console]] — tour the three-zone TUI, the status bar, and the F-key slots

## Working in the console

Use the platform's terminal interface and its built-in Cartridges.

- [[navigate-console-tui|Navigate the console TUI]] — status bar fields, F-key switching, universal key bindings
- [[use-f-key-model|Use the F-key model]] — default slot assignments, Cartridge architecture, Email / SLM / Input Machine
- [[read-the-command-ledger|Read the command ledger]] — view WORM ledger entries from the F12 LEDGER tab and export to C2SP format
- [[run-first-slm-query|Run your first SLM query]] — submit an inference prompt in F9 and read the Doorman health dashboard

## Records & storage

Work with the WORM audit ledger and entity data.

- [[read-write-totebox-archives|Read and write Totebox archives]] — session start reading protocol, commit flow, draft staging, cross-archive mailbox
- [[verify-worm-ledger|Verify a WORM ledger entry]] — confirm hash-chain integrity and validate against a signed Sigstore checkpoint
- [[query-the-datagraph|Query the DataGraph]] — search named entities, navigate relationships, handle Tier A outages
- [[export-structured-data|Export structured data]] — four export paths: DataGraph, wiki Markdown, GeoJSON, ledger tiles

## Machine authorization

Credential and access control operations.

- [[pair-a-new-device|Pair a new device]] — the core enrollment flow; all four pairing types (ADMIN, INPUT, USER, INTERFACE)
- [[enroll-ppn-node|Enroll a PPN node]] — register a compute node with the fleet controller and verify heartbeat enrollment
- [[issue-capability-token|Issue a capability token]] — generate an Ed25519 token for a device or service at a specific scope
- [[rotate-keys|Rotate keys and tokens]] — replace a keypair and its token with a new one through the three-phase rotation sequence
- [[authenticate-binary-downloads|Authenticate binary downloads]] — verify and fetch signed binaries from the private distribution endpoint

## Multi-entity scale

Manage multiple tenants, users, and fleet nodes.

- [[configure-tenant-namespace|Configure a tenant namespace]] — register a tenant, set quotas, verify isolation, issue the root credential
- [[scale-user-tiers|Scale user access tiers]] — promote users between READ / USER / INPUT tiers and bulk-update a team
- [[add-a-fleet-node|Add a node to a running fleet]] — enroll a second node without interrupting existing fleet operations

## Integration & data

Connect external data pipelines and build location-intelligence applications.

- [[build-a-colocation-map|Build a co-location map]] — query the GIS engine API and render a MapLibre cluster layer
- [[connect-osm-data-pipeline|Connect to the OSM data pipeline]] — write a chain ingest YAML, run the ingest script, and rebuild the cluster layer
- [[federate-archives-via-content-mounts|Federate archives via content mounts]] — mount wiki content from one archive into a second instance using declarative TOML mounts
- [[use-knowledge-mounts|Use declarative knowledge mounts]] — add a secondary content repository to a running wiki instance via knowledge.toml

## Self-hosting

Deploy the platform on your own infrastructure.

- [[self-host-a-deployment|Self-host a deployment]] — provision a Totebox Archive on a supported compute node
- [[configure-doorman|Configure the Doorman gateway]] — set tier upstream addresses, circuit-breaker thresholds, and verify the health endpoint
- [[deploy-knowledge-instance|Deploy a knowledge instance]] — build and start app-mediakit-knowledge pointed at a local content repository
- [[run-local-slm-inference|Run local SLM inference]] — start the SLM service, verify Doorman Tier B, and submit inference requests from the console or API

## See also

- [[architecture/_index|Architecture]] — cross-cutting platform architecture
- [[patterns/_index|Patterns]] — named design patterns used across the platform
- [[totebox-session]] — what a Totebox session is and what it can do
- [[machine-based-auth]] — how machine-based authorization works
