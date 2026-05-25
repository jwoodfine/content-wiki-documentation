---
schema: foundry-doc-v1
title: "Operational Guide Catalog"
slug: guide-catalog
category: reference
type: topic
status: stable
last_edited: 2026-05-25
editor: pointsav-engineering
paired_with: guide-catalog.es.md
---

The Operational Guide Catalog lists every operational guide in the Woodfine fleet deployment, organized by purpose. Each guide covers a specific operational task on a named deployment node. Use this catalog to locate the right guide when you know what you need to do but not which system owns the task.

## Provisioning & Deployment

This section covers guides for provisioning new nodes and deploying services across the fleet. Use these guides when standing up a new node, performing a fresh deployment, or recovering a deployment to a known-good state.

- **guide-deployment** (cluster-totebox-corporate) — deploys the corporate archive Totebox node
- **guide-provision-node** (cluster-totebox-corporate) — provisions a new corporate archive node
- **guide-deployment** (cluster-totebox-property) — deploys the property archive Totebox node
- **guide-provision-node** (cluster-totebox-property) — provisions a new property archive node
- **guide-deployment** (fleet-infrastructure-cloud) — deploys a GCP cloud relay node
- **guide-provision-node** (fleet-infrastructure-cloud) — provisions a cloud relay node
- **guide-deployment** (fleet-infrastructure-onprem) — deploys an on-premises hardware node
- **guide-provision-node** (fleet-infrastructure-onprem) — provisions an on-premises node
- **guide-deployment** (gateway-interface-command) — deploys the command interface gateway
- **guide-provision-node** (gateway-interface-command) — provisions a command interface node
- **guide-deployment** (cluster-totebox-personnel) — deploys the personnel archive node
- **guide-provision-node** (cluster-totebox-personnel) — provisions a personnel archive node
- **guide-provision-standalone** (fleet-infrastructure-leased) — provisions a dedicated leased server node
- **guide-provision-relay** (fleet-infrastructure-cloud) — provisions the cloud PPN relay
- **guide-provision-onprem** (fleet-infrastructure-onprem) — provisions the on-premises hardware stack
- **guide-deployment** (route-network-admin) — deploys the network admin routing node
- **guide-provision-node** (route-network-admin) — provisions the network admin routing node
- **guide-provision-node** (vault-privategit-source) — provisions the private git vault node

## BIM & Property

This section covers guides for operating the BIM orchestration gateway and the property archive. Use these guides when authoring or managing BIM objects, publishing regulatory overlays, or performing day-to-day operations on the property archive.

- **guide-bim-object-authoring** (gateway-orchestration-bim) — creates and modifies BIM objects within the IFC archive
- **guide-bim-token-authoring** (gateway-orchestration-bim) — authors BIM tokens for the Woodfine BIM token registry
- **guide-climate-zone-objects** (gateway-orchestration-bim) — assigns and manages climate zone classifications on BIM objects
- **guide-climate-zone-tokens** (gateway-orchestration-bim) — publishes climate zone token sets to the BIM token registry
- **guide-deploy-bim-substrate** (gateway-orchestration-bim) — deploys the BIM substrate on a gateway-orchestration-bim node
- **guide-deployment** (gateway-orchestration-bim) — deploys the BIM orchestration gateway
- **guide-provision-node** (gateway-orchestration-bim) — provisions a BIM orchestration gateway node
- **guide-regulation-overlay-publishing** (gateway-orchestration-bim) — publishes regulatory overlays (zoning, building code) onto BIM model layers
- **guide-bim-archive-operations** (cluster-totebox-property) — day-to-day operations of the property BIM archive (IFC ingestion, validation, maintenance)

## GIS & Geospatial

This section covers guides for operating the GIS co-location pipeline and orchestration gateway. Use these guides when ingesting new retail chains, expanding coverage to new countries, rebuilding the GIS pipeline, or deploying the GIS gateway.

- **guide-gis-adding-a-chain** (gateway-orchestration-gis) — ingests a new retail chain into the GIS co-location pipeline
- **guide-gis-adding-a-country** (gateway-orchestration-gis) — adds a new country to the GIS coverage area and rebuilds affected data layers
- **guide-gis-pipeline-rebuild** (gateway-orchestration-gis) — performs a full rebuild of the GIS pipeline from source data
- **guide-totebox-orchestration-gis** (gateway-orchestration-gis) — runs the GIS Totebox orchestration workflow end-to-end
- **guide-deployment** (gateway-orchestration-gis) — deploys the GIS orchestration gateway
- **guide-provision-node** (gateway-orchestration-gis) — provisions a GIS orchestration gateway node

## Personnel & Identity

This section covers guides for operating the personnel archive. Use these guides when managing personnel records, running identity integrations, operating the sovereign search surface, or executing SLM inference within the personnel cluster.

- **guide-cold-storage-sync** (cluster-totebox-personnel) — syncs personnel records to encrypted cold storage
- **guide-ingress-operations** (cluster-totebox-personnel) — manages incoming personnel data ingestion and verification
- **guide-linkedin-adapter** (cluster-totebox-personnel) — operates the LinkedIn professional-data adapter
- **guide-msft-entra-id** (cluster-totebox-personnel) — configures and operates the Microsoft Entra ID identity integration
- **guide-personnel-ledger** (cluster-totebox-personnel) — manages the personnel ledger — create, update, and audit personnel records
- **guide-slm-execution** (cluster-totebox-personnel) — runs the SLM inference layer within the personnel cluster
- **guide-sovereign-search** (cluster-totebox-personnel) — operates the sovereign full-text search surface for personnel data
- **guide-totebox-orchestration** (cluster-totebox-personnel) — runs the personnel archive Totebox orchestration workflow

## Network & Infrastructure

This section covers guides for operating fleet network overlays, endpoint enrollment, and the Private Pointsav Network mesh routing layer. Use these guides when deploying VPN overlays, configuring macOS endpoints, administering container networking, or orchestrating the PPN mesh.

- **guide-deploy-vpn** (fleet-infrastructure-leased) — deploys the WireGuard VPN overlay on leased server nodes
- **guide-endpoint-macbook** (fleet-infrastructure-leased) — provisions a macOS endpoint on the leased infrastructure tier
- **guide-macos-endpoints** (fleet-infrastructure-leased) — manages macOS endpoint configuration and enrollment
- **guide-lxc-network-admin** (fleet-infrastructure-onprem) — administers LXC container networking on on-premises hardware
- **guide-mesh-orchestration** (route-network-admin) — orchestrates the Private Pointsav Network mesh routing layer
- **guide-mesh-execution** (root) — executes a PPN mesh operation from the F8 terminal
- **guide-physical-egress** (root) — manages physical egress and regulatory printing workflows

## Console & Operations

This section covers guides for operating the unified asset-manager console. Use these guides when performing daily console operations, managing the command ledger, pairing devices, or monitoring fleet telemetry.

- **guide-console-operations** (node-console-operator) — daily operations of the unified asset-manager console
- **guide-command-ledger** (node-console-operator) — manages the command ledger — logging, replay, and audit of console commands
- **guide-mba-pairing-ceremony** (node-console-operator) — performs the MBA device pairing ceremony for console authentication
- **guide-os-console-operator** (node-console-operator) — installs and operates the os-console platform for the Woodfine console node
- **guide-telemetry-operations** (root) — monitors and manages operational telemetry across the Woodfine fleet

## Content & Media

This section covers guides for operating the documentation wiki, corporate wiki, projects wiki, and marketing site. Use these guides when running editorial sweeps, managing sprint roadmaps, configuring design tokens, or operating media node deployments.

- **guide-editorial-content-sweep** (media-knowledge-documentation) — runs an editorial content sweep pass on the documentation wiki
- **guide-knowledge-wiki-sprint-roadmap** (media-knowledge-documentation) — manages the knowledge wiki sprint planning and roadmap
- **guide-wiki-dark-mode-toggle** (media-knowledge-documentation) — configures and tests the wiki dark-mode toggle
- **guide-wiki-design-tokens** (media-knowledge-documentation) — applies and audits design token updates on the wiki surface
- **guide-deployment** (media-knowledge-corporate) — deploys the corporate wiki media node
- **guide-provision-node** (media-knowledge-corporate) — provisions a corporate wiki node
- **guide-deployment** (media-knowledge-projects) — deploys the projects wiki media node
- **guide-provision-node** (media-knowledge-projects) — provisions a projects wiki node
- **guide-deployment-marketing-site** (media-marketing-landing) — deploys the Woodfine marketing and landing page site
- **guide-operate-marketing-landing** (media-marketing-landing) — daily operations of the marketing landing page
- **guide-provision-marketing-site** (media-marketing-landing) — provisions the marketing site infrastructure
- **guide-telemetry-governance** (media-marketing-landing) — manages telemetry governance policy for the marketing site
- **guide-telemetry-operations** (media-marketing-landing) — operates the marketing site telemetry stack

## Source Control & Distribution

This section covers guides for operating the private git vault. Use these guides when managing software distribution, opening development sessions, operating the Doorman access-control service, administering the vault node, or setting up a developer workbench.

- **guide-command-session** (vault-privategit-source) — opens and operates a Command Session against the private git vault
- **guide-deployment** (vault-privategit-source) — deploys the vault-privategit-source node
- **guide-doorman-deployment** (vault-privategit-source) — deploys the Doorman access-control service on the vault node
- **guide-doorman** (vault-privategit-source) — operates the service-slm Doorman — access control, authentication logging, session management
- **guide-open-archive** (vault-privategit-source) — opens a Totebox Archive for a new development session
- **guide-operating-yoyo** (vault-privategit-source) — operates the Elastic Compute (Yo-Yo) scheduling layer within the vault environment
- **guide-software-distribution-operations** (vault-privategit-source) — manages software distribution operations — release packages, binaries, and artifact publishing
- **guide-tier-a-sysadmin-tui** (vault-privategit-source) — operates the Tier A sysadmin TUI for vault-level system administration
- **guide-workbench-setup** (vault-privategit-source) — sets up the developer workbench environment on the vault node

## AI & Intelligence

This section covers guides for operating the intelligence cluster and the SLM inference service. Use these guides when running the nightly elastic compute pipeline or deploying the SLM inference service within the personnel cluster.

- **guide-elastic-compute-nightly-pipeline** (cluster-intelligence) — runs the nightly elastic compute (LoRA fine-tuning) pipeline
- **guide-01-deployment** (cluster-totebox-personnel/service-slm) — deploys the SLM inference service within the personnel cluster

## Workspace & Development

This section covers guides for operating the Foundry workspace itself. Use these guides when provisioning new Totebox Archives, managing pre-commit hooks, recovering VM resources, or verifying Claude Code tooling.

- **guide-claude-code-hooks-installed** (foundry-workspace) — verifies and operates the Claude Code pre-tool hooks in the Foundry workspace
- **guide-foundry-vm-resource-recovery** (foundry-workspace) — recovers disk and memory resources on the Foundry GCE VM
- **guide-onboarding-new-archive** (foundry-workspace) — provisions a new Totebox Archive from scratch within the Foundry workspace
- **guide-pre-commit-gate-operator-flow** (foundry-workspace) — operates the pre-commit gate — how to handle hook failures, bypass procedures, and gate audits

## See Also

- architecture/totebox-orchestration-development — the Totebox orchestration development model that underpins how deployment nodes are provisioned and operated
- systems/totebox-archive — the Totebox Archive pattern that organises session-scoped work across all fleet deployment clusters
