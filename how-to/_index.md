---
schema: foundry-doc-v1
title: "Developer Guides"
slug: how-to
category: how-to
type: topic
content_type: topic
quality: complete
short_description: "Step-by-step developer guides covering toolchain setup, console TUI navigation, WORM ledger operations, and multi-entity scale for the PointSav platform. Device pairing and capability tokens now live in Machine Authorization; self-hosted deployment now lives in Self-Hosting."
status: active
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
index_type: thematic
index_scope: how-to
last_edited: 2026-08-24
editor: pointsav-engineering
paired_with: _index.es.md
---

Step-by-step developer guides for building with and on the PointSav platform. Each guide addresses a specific task — follow it start to finish, then refer back to the related architecture articles when you need the underlying theory.

For the concepts behind each guide, start in [[architecture]] or [[patterns-index|Patterns]]. For platform architecture overview, see [[totebox-orchestration-development]].

<!-- START-HERE-HIGHLIGHT: engine reads this block to render the single "start here" card
     (reuses the existing cluster-card--start-here component). Do not add more than one. -->

**Start here:** [[install-toolchain|Install the development toolchain]] — the first step for any new contributor, before opening a session or exploring the console.

<!-- END-START-HERE-HIGHLIGHT -->

## Getting started

The foundation: install the toolchain and open your first session.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: getting-started -->
- [[pair-a-new-device|Pair a new device]] — register a device with the pairing server and get it approved onto the network (now part of [Machine Authorization](/category/machine-authorization))
- [[install-toolchain|Install the development toolchain]] — set up Rust and the staging-tier commit helper on a workspace VM
- [[open-first-totebox-session|Open your first Totebox session]] — navigate to an archive, read your inbox, and start contributing
- [[explore-the-console|Explore the console]] — tour the three-zone TUI, the status bar, and the F-key slots
<!-- END AUTO-GENERATED -->

## Working in the console

Use the platform's terminal interface and its built-in Cartridges.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: working-in-the-console -->
- [[navigate-console-tui|Navigate the console TUI]] — the real screen layout and status bar fields
- [[use-f-key-model|Use the F-key model]] — what F3, F9, and F12 actually do
- [[read-the-command-ledger|Read the command ledger]] — page entries and fetch a signed checkpoint over service-fs's real HTTP API
- [[run-first-slm-query|Run your first SLM query]] — the real path to a first inference request
<!-- END AUTO-GENERATED -->

## Records & storage

Work with the WORM audit ledger and entity data.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: records-and-storage -->
- [[read-write-totebox-archives|Read and write Totebox archives]] — session start reading protocol, commit flow, draft staging, cross-archive mailbox
- [[verify-worm-ledger|Verify a WORM ledger entry]] — verify against a fetched checkpoint using only curl and SHA-256
- [[query-the-datagraph|Query the DataGraph]] — the real query_datagraph/get_entity_context tools
- [[export-structured-data|Export structured data]] — three real export paths: DataGraph, wiki Markdown, ledger entries
<!-- END AUTO-GENERATED -->

## Multi-entity scale

Manage multiple tenants, users, and fleet nodes.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: multi-entity-scale -->
- [[configure-tenant-namespace|Configure a tenant namespace]] — the real config-driven provisioning, since no registration API exists
- [[scale-user-tiers|Scale user access]] — grant role-scoped tokens as a team grows; there's no promote/revoke
- [[add-a-fleet-node|Add a node to a running fleet]] — enroll a second node without interrupting existing fleet operations
<!-- END AUTO-GENERATED -->

## Integration & data

Connect external data pipelines and build location-intelligence applications.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: integration-and-data -->
- [[build-a-colocation-map|Build a co-location map]] — load a PMTiles archive directly; no REST API or API key exists
- [[connect-osm-data-pipeline|Connect to the OSM data pipeline]] — the real ingest-osm.py script and taxonomy.py registration
- [[federate-archives-via-content-mounts|Federate archives via content mounts]] — mount a second repository's content into a running instance
- [[use-knowledge-mounts|Use declarative knowledge mounts]] — the real `[[mount]]` schema and its real, unmitigated slug-collision risk
<!-- END AUTO-GENERATED -->

Device pairing, capability tokens, and fleet enrollment now have their own category — see [Machine Authorization](/category/machine-authorization). Self-hosted deployment now has its own category — see [Self-Hosting](/category/self-hosting).

## Financial & construction tools

Run the platform's domain tools — the construction cost, schedule, and quality ledger and its accounting and payroll siblings. Each is a command-line tool; none has a console screen today.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: financial-construction-tools -->
- [[generate-a-construction-cost-estimate|Generate a construction cost estimate report]] — run the real reporting binary against a CSV data directory; there are no flags, since it parses no arguments at all
- [[generate-a-financial-statement-package|Generate a financial statement package]] — render a consolidated package for one fiscal year and period; the run refuses rather than publish a figure that does not tie
- [[generate-a-payroll-register|Generate a payroll register]] — aggregate budgeted labour hours by division; it computes no gross pay, no pay frequency, and no remittance
<!-- END AUTO-GENERATED -->

## See also

- [[architecture-index|Architecture]] — cross-cutting platform architecture
- [[patterns-index|Patterns]] — named design patterns used across the platform
- [[totebox-session]] — what a Totebox session is and what it can do
- [[machine-based-auth]] — how machine-based authorization works
- [Machine Authorization](/category/machine-authorization) — device pairing, capability tokens, fleet enrollment, and binary-download authentication
- [Self-Hosting](/category/self-hosting) — deploying platform components on your own infrastructure
