---
schema: foundry-doc-v1
title: "Architecture Overview — PointSav Platform"
slug: architecture-overview
category: architecture
type: concept
content_type: topic
quality: stub
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-06-15
editor: pointsav-engineering
paired_with: architecture-overview.es.md
short_description: "A map of the PointSav platform's major architectural surfaces: compute substrate, software distribution, GIS intelligence, and the editorial pipeline."
cites: []
---

The PointSav platform is composed of several architectural surfaces that operate independently but share a common substrate. This article serves as a map to the detailed architecture articles.

## Compute substrate — PointSav Private Network (PPN)

The PPN is the multi-tenant VM resource pool that forms the runtime floor of the platform. It is a three-service stack (fleet controller, host agent, tenant proxy) sitting over a WireGuard mesh.

- [[ppn-small-business-compute|PPN Small-Business Compute]] — product overview and three-node stack
- [[ppn-vm-resource-pool|PPN VM Resource Pool Architecture]] — placement algorithm, host agent, inference broker
- [[ppn-tenant-vm-isolation|PPN Tenant VM Isolation]] — namespace isolation, bearer tokens, WORM audit

## Software distribution

Commercial software built on the platform is distributed through a signed binary pipeline with license verification at install and at runtime.

- [[software-distribution-substrate|Software Distribution Substrate]] — binary signing, Ed25519 license tokens, private Git server

## Location intelligence and GIS

The GIS orchestration platform produces commercial co-location cluster data covering the PRO, VWH, and PKS archetypes.

- Data Overview — data layers and GIS tile pipeline
- [[ppn-small-business-compute|Location Intelligence Co-location Archetypes]] — PRO/VWH/PKS overview
- Co-location Tier Nomenclature — T1/T2/T3 vocabulary

## OS Console and desktop surfaces

The OS Console is the terminal-based interface for platform management. Workplace-surface applications target AEC professionals.

- [[os-console-architecture|OS Console Architecture]] — cartridge model, Ratatui surface, Doorman health dashboard

*This article is a stub. Full content is planned for a future session.*
