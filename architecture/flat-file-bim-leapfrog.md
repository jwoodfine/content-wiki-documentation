---
schema: foundry-doc-v1
type: topic
slug: flat-file-bim-leapfrog
title: The Flat-File BIM Leapfrog
audience: vendor-public
bcsc_class: vendor-public
language: en
paired_with: flat-file-bim-leapfrog.es.md
status: active
last_edited: 2026-05-06
---

PointSav's Building Design System is built on five architectural constraints that, individually, are mild inconveniences for any single feature comparison and, together, define a product category that hyperscalers cannot occupy without cannibalising their own revenue model. The constraints are flat-file storage, open standards, Rust + Tauri, offline-first, and EUPL-licensed. The open BIM standards stack matured between 2023 and 2025 into the infrastructure that makes this strategy viable; the property-manager market gap is documented in peer-reviewed literature; and the open toolchain is commercial-grade today.

This document explains what flat-file BIM is, what it is not, and why five specific capabilities follow from the architecture rather than needing to be added on top.

## The standards stack reached production maturity in 2024

The foundation is that the standards exist, specify plain-text encodings, and sit inside ISO. IFC 4.3 was formally published as ISO 16739-1:2024 in April 2024, extending IFC from buildings to bridges, roads, rail, ports, and waterways. The canonical serialisation, IFC-SPF, is ISO 10303-21 clear-text — readable in any text editor. IDS 1.0 became the official buildingSMART standard on 1 June 2024. BCF 3.0 is a ZIP of XML markup files plus PNG snapshots — unzip it and the per-topic directory tree is git-friendly diff-able prose. CityJSON 2.0 is an OGC community standard, with CityJSONSeq used at national scale by TU Delft's 3DBAG dataset for 10M+ Dutch buildings.

What is not yet production-ready matters as much. ifcJSON remains a community draft. IFC 5 is alpha, with a JSON-based IFCX serialisation borrowing USD-like composition from Pixar's OpenUSD; breaking changes are expected. The pragmatic conclusion: canonicalise on IFC-SPF today, mirror to ifcJSON opportunistically, and architect the object model so that an IFC 5 / IFCX migration is intended to be a serialisation swap, not a rewrite.

## What "flat-file" means

A directory of plain-text and standardised-binary files that an ordinary text editor or SVG viewer can open without a proprietary SDK, decades after the software vendor that produced it is gone.

| Format | ISO / publisher | Role |
|---|---|---|
| IFC-SPF (`.ifc`) | ISO 16739-1:2024 | Authoritative geometry + semantics |
| IDS 1.0 | buildingSMART (June 2024) | Validation contract |
| BCF 3.0 | buildingSMART | Per-topic collaboration history |
| COBie via ifccsv | NIST | Asset handover |
| Per-element YAML sidecars | local convention | Pset_* + sensor + work-order data |
| Hash-addressed object store | local convention; Speckle-inspired | Versioned Merkle DAG |
| glTF 2.0 | ISO/IEC 12113:2022 | Visualisation cache (regenerable) |
| SVG | ISO/IEC 14496-22:2019 | 2D drawings (regenerable) |
| CityJSONSeq | OGC | Portfolio / urban context |

The `.ifc` file is the authoritative spatial and semantic state of the building. The sidecars carry non-geometric data (ratings, quantities, sensor readings, work orders, lease references). The object store layer gives the whole vault git-grade versioning semantics. Visualisation derivatives are caches that regenerate at will from the authoritative source. Any specific BIM viewer or authoring tool is replaceable. The archive is permanent.

## Five capabilities that follow from the architecture

### 1. Asset-anchored BIM

The digital twin is signed with the land title and travels with the property deed when ownership changes hands. Multi-tenant SaaS cannot offer this without breaking the tenancy model — a new owner would need to be onboarded to the vendor's tenant, the model migrated, permissions reconstructed, the subscription repriced. A flat-file twin is owned like the building itself: forever, transferrably, without vendor permission.

A major cloud BIM platform's subscription licence makes the risk explicit: a term lapse requires the owner to enter into a new subscription agreement for continued access to project data. The digital twin rents; it does not sell.

### 2. Offline-capable BIM for field use

Basements, rooftops, remote construction sites, air-gapped defence facilities, healthcare campuses with strict data-residency rules, developing-world connectivity — all are workflows where a cloud-authoritative twin is structurally impossible. Cloud-authoritative BIM platforms require live internet access by construction. The Tauri + Rust shell hosting an offline IFC archive on a laptop or tablet preserves full BIM functionality without any network dependency.

### 3. Vendor-obsolescence-survivable BIM

Buildings live 50+ years. Proprietary BIM authoring formats have compatibility windows of roughly three to five years. The flat-file substrate is readable for decades after any specific vendor disappears. This matters most for public-sector BIM (UK Government Level 2, US GSA, DoD, VA), cultural-heritage custodians, and long-horizon property owners — exactly the buyers most exposed to vendor-discontinuation risk.

### 4. IoT integration directly into the BIM archive

A flat-file archive with per-element YAML sidecars can ingest sensor readings via local MQTT broker, written as timestamped JSON records into the element's sidecar, without the data ever leaving the owner's premises. This matters economically (no sensor-count-based token charges), legally (GDPR data residency, HIPAA in healthcare, export control in defence), and architecturally (the sensor graph is versioned alongside the model).

### 5. BIM + lease register + financial ledger as one portable archive

For a property owner, the building, the lease, the rent, and the financing are the same asset. The building is where the lease applies; the lease is where the rent comes from; the rent services the loan; the loan justified the building. Multi-tenant cloud cannot commingle BIM, lease register, and rent roll in a single owner-controlled archive — commercial confidentiality, data residency, financial-audit trails, and multi-tenant isolation each prevent it on its own.

The Foundry workplace family — `app-workplace-memo`, `app-workplace-presentation`, `app-workplace-proforma`, and `app-workplace-bim` — is intended to converge these into one portable archive. The Totebox Archive is the first data architecture where a building's legal, financial, spatial, and operational identity are one artifact that travels with the asset.

## Government regulatory acceptance is structurally favourable

The format stack — IFC-SPF + IDS 1.0 + BCF 3.0 + COBie — fulfills mandatory open-standard delivery requirements across US federal (GSA, USACE, VA, NAVFAC), EU member states (Germany, Italy, Spain, Denmark, Norway, Netherlands, Poland), the UK BIM Framework, Singapore CORENET X (mandatory October 2026), Dubai (mandatory since January 2024), and the broader buildingSMART openBIM movement.

The offline-first, flat-file architecture is the only approach that natively satisfies ITAR air-gapped requirements for defence projects, EU Data Act data sovereignty for European projects, HIPAA technical safeguards for VA healthcare facilities, and GDPR data residency for EU government clients — without dependency on a cloud vendor's contractual assurances. The EUPL-1.2 licence is OSI-approved, FAR 12.212-compatible, and EU-procurement-preferred.

## What flat-file BIM does not do well — yet

Honest accounting:

- Real-time multi-user editing is slower than synchronous SaaS for charette-style design workshops. Cloud SaaS is genuinely better for synchronous design sessions.
- City-scale federation (1M+ buildings) needs a different streaming architecture than a single-property archive.
- Generative-AI BIM authoring tools from major vendors are proprietary today. The substrate is AI-ready (the Doorman dispatches generative requests through an audit ledger), but a generative BIM authoring tool is not planned for the v0.0.1 release.

These are deliberate trade-offs for the offline-first, vendor-obsolescence-survivable posture; not oversights to be patched in the next release.


---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*

*Woodfine Capital Projects™, Woodfine Management Corp™, PointSav Digital Systems™, Totebox Orchestration™, and Totebox Archive™ are trademarks of Woodfine Capital Projects Inc., used in Canada, the United States, Latin America, and Europe. All other trademarks are the property of their respective owners.*
