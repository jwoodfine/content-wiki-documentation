---
schema: foundry-doc-v1
title: "Developer Guides"
slug: how-to
category: how-to
type: topic
content_type: topic
quality: complete
short_description: "Step-by-step developer guides covering device pairing, toolchain setup, console TUI navigation, WORM ledger operations, and self-hosted deployment of the PointSav platform."
status: active
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-06-14
editor: pointsav-engineering
paired_with: _index.es.md
---

Step-by-step developer guides for building with and on the PointSav platform. Each guide addresses a specific task — follow it start to finish, then refer back to the related architecture articles when you need the underlying theory.

For the concepts behind each guide, start in [[architecture]] or [[patterns-index|Patterns]]. For platform architecture overview, see [[totebox-orchestration-development]].

## Getting started

The foundation: authenticate your device, install the toolchain, and open your first session.

- [[pair-a-new-device|Pair a new device]] — register a device with the pairing server and get it approved onto the network (now part of [Machine Authorization](/category/machine-authorization))
- [[install-toolchain|Install the development toolchain]] — set up Rust and the staging-tier commit helper on a workspace VM
- [[open-first-totebox-session|Open your first Totebox session]] — navigate to an archive, read your inbox, and start contributing
- [[explore-the-console|Explore the console]] — tour the three-zone TUI, the status bar, and the F-key slots

## Working in the console

Use the platform's terminal interface and its built-in Cartridges.

- [[navigate-console-tui|Navigate the console TUI]] — the real screen layout and status bar fields
- [[use-f-key-model|Use the F-key model]] — what F3, F9, and F12 actually do
- [[read-the-command-ledger|Read the command ledger]] — page entries and fetch a signed checkpoint over service-fs's real HTTP API
- [[run-first-slm-query|Run your first SLM query]] — the real path to a first inference request

## Records & storage

Work with the WORM audit ledger and entity data.

- [[read-write-totebox-archives|Read and write Totebox archives]] — session start reading protocol, commit flow, draft staging, cross-archive mailbox
- [[verify-worm-ledger|Verify a WORM ledger entry]] — verify against a fetched checkpoint using only curl and SHA-256
- [[query-the-datagraph|Query the DataGraph]] — the real query_datagraph/get_entity_context tools
- [[export-structured-data|Export structured data]] — three real export paths: DataGraph, wiki Markdown, ledger entries

## Multi-entity scale

Manage multiple tenants, users, and fleet nodes.

- [[configure-tenant-namespace|Configure a tenant namespace]] — the real config-driven provisioning, since no registration API exists
- [[scale-user-tiers|Scale user access]] — grant role-scoped tokens as a team grows; there's no promote/revoke
- [[add-a-fleet-node|Add a node to a running fleet]] — enroll a second node without interrupting existing fleet operations

## Integration & data

Connect external data pipelines and build location-intelligence applications.

- [[build-a-colocation-map|Build a co-location map]] — load a PMTiles archive directly; no REST API or API key exists
- [[connect-osm-data-pipeline|Connect to the OSM data pipeline]] — the real ingest-osm.py script and taxonomy.py registration
- [[federate-archives-via-content-mounts|Federate archives via content mounts]] — mount a second repository's content into a running instance
- [[use-knowledge-mounts|Use declarative knowledge mounts]] — the real [[mount]] schema and its real, unmitigated slug-collision risk

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
- [Machine Authorization](/category/machine-authorization) — device pairing, capability tokens, fleet enrollment, and binary-download authentication
- [Self-Hosting](/category/self-hosting) — deploying platform components on your own infrastructure
