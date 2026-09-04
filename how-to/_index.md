---
schema: foundry-doc-v1
title: "How You Run It"
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
last_edited: 2026-09-04
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
- [[install-toolchain|Install the development toolchain]] — Installs the pinned Rust toolchain with rustup, runs a baseline build and tests, and verifies the commit helper and SSH signing key needed before working in a monorepo archive.
- [[open-first-totebox-session|Open your first Totebox session]] — Opens a first Totebox session in a single archive: read the manifest, check your inbox, understand what the session can and can't write, and complete the shutdown sweep before closing.
- [[explore-the-console|Explore the console]] — Orients a first-time operator to os-console — the status bar, the F9 inference-gateway dashboard, and the mandatory F12 input checkpoint that writes to the WORM ledger.
<!-- END AUTO-GENERATED -->

## Working in the console

Use the platform's terminal interface and its built-in Cartridges.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: working-in-the-console -->
- [[navigate-console-tui|Navigate the console TUI]] — Navigates os-console by keyboard — the F-key strip at the top, the status bar's real fields at the bottom, and switching slots without losing state.
- [[use-f-key-model|Use the F-key model]] — Works the os-console F-key cartridge model — F3 email, F9's monitoring-only SLM dashboard, F12's file-based Input Machine — where each compiled-in cartridge owns its slot's rendering and input.
- [[read-the-command-ledger|Read the command ledger]] — Reads the append-only WORM ledger over service-fs's real HTTP API — paging entries with a cursor and fetching a signed checkpoint — since no ledger-browsing UI exists in the console.
- [[run-first-slm-query|Run your first SLM query]] — Submits a first inference request to Doorman directly over HTTP — the real path, since the console's F9 slot is a monitoring dashboard with no query interface at all.
<!-- END AUTO-GENERATED -->

## Records & storage

Work with the WORM audit ledger and entity data.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: records-and-storage -->
- [[read-write-totebox-archives|Read and write Totebox archives]] — Reads a Totebox archive's state at session start — inbox, session context, git status, NEXT.md — and writes changes through the staging-tier commit flow.
- [[verify-worm-ledger|Verify a WORM ledger entry]] — Verifies WORM ledger entries against a fetched checkpoint over service-fs's real HTTP API, using a standard SHA-256 toolchain — no CLI or proprietary tooling exists or is required.
- [[query-the-datagraph|Query the DataGraph]] — Queries the DataGraph for current entity state with the real query_datagraph and get_entity_context MCP tools, and handles DataGraph unavailability as its own signal, separate from Doorman's inference tiers.
- [[export-structured-data|Export structured data]] — Exports platform data through three real paths — DataGraph entity records via MCP tools, wiki Markdown read directly from git, and paginated ledger entries over service-fs's HTTP API.
<!-- END AUTO-GENERATED -->

## Multi-entity scale

Manage multiple tenants, users, and fleet nodes.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: multi-entity-scale -->
- [[configure-tenant-namespace|Configure a tenant namespace]] — Configures a tenant namespace on service-vm-tenant via environment variables and a restart — the real config-driven mechanism, since no runtime tenant-registration API exists.
- [[scale-user-tiers|Scale user access]] — Grants role-scoped capability tokens to new users as a team scales, using service-content's real pairing API — there is no promote/demote or bulk-revoke operation, since no revocation mechanism exists at all.
- [[add-a-fleet-node|Add a node to a running fleet]] — Adds a second node to an already-running PPN fleet using service-vm-host's real env-var configuration — the same mechanism as the first node, since nothing about enrollment changes once a fleet exists.
<!-- END AUTO-GENERATED -->

## Integration & data

Connect external data pipelines and build location-intelligence applications.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: integration-and-data -->
- [[build-a-colocation-map|Build a co-location map]] — Renders tier-coloured co-location cluster markers in MapLibre GL by loading a PMTiles archive directly — the real flat-file architecture, since no bearer-token REST cluster API exists.
- [[connect-osm-data-pipeline|Connect to the OSM data pipeline]] — Ingests a new retail or service chain from OpenStreetMap using the real ingest-osm.py script and taxonomy.py's CATEGORIES/BRAND_FILL dicts, then rebuilds the servable cluster tiles.
- [[federate-archives-via-content-mounts|Federate archives via content mounts]] — Federates a second knowledge instance's articles into a running instance through a knowledge.toml [[mount]] entry — a flat, merged namespace with no isolation, not a URL-prefixed federation scheme.
- [[use-knowledge-mounts|Use declarative knowledge mounts]] — Adds a secondary content repository to a running knowledge instance via a knowledge.toml [[mount]] entry — into the same flat slug namespace as the primary, since no URL-prefix isolation exists.
<!-- END AUTO-GENERATED -->

Device pairing, capability tokens, and fleet enrollment now have their own category — see [Machine Authorization](/category/machine-authorization). Self-hosted deployment now has its own category — see [Self-Hosting](/category/self-hosting).

## Financial & construction tools

Run the platform's domain tools — the construction cost, schedule, and quality ledger and its accounting and payroll siblings. Each is a command-line tool; none has a console screen today.

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: financial-construction-tools -->
- [[generate-a-construction-cost-estimate|Generate a construction cost estimate report]] — Runs the construction reporting binary against a CSV data directory to produce costing and schedule reports as HTML and PDF, with reconciliation and validation logs — the only interface that exists, since the tool has no console screen and parses no command-line arguments at all.
- [[generate-a-financial-statement-package|Generate a financial statement package]] — Runs the statements binary for one fiscal year and one period to render a consolidated statement package as HTML and PDF, recomputed from journal CSVs on every run — the tool refuses to render rather than publish a figure that does not tie.
- [[generate-a-payroll-register|Generate a payroll register]] — Runs the payroll binary to aggregate budgeted labour hours by division into an HTML and PDF register — a narrow report that computes no gross pay, no pay frequency, and no remittance, and prints an em dash rather than a number wherever it has none.
<!-- END AUTO-GENERATED -->

## See also

- [[architecture-index|Architecture]] — cross-cutting platform architecture
- [[patterns-index|Patterns]] — named design patterns used across the platform
- [[totebox-session]] — what a Totebox session is and what it can do
- [[machine-based-auth]] — how machine-based authorization works
- [Machine Authorization](/category/machine-authorization) — device pairing, capability tokens, fleet enrollment, and binary-download authentication
- [Self-Hosting](/category/self-hosting) — deploying platform components on your own infrastructure
