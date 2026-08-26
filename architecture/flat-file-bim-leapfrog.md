---
schema: foundry-doc-v1
title: "Flat-file BIM leapfrog"
slug: flat-file-bim-leapfrog
language: en
category: architecture
index_group: location-intelligence-and-domain
type: topic
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-08-26
editor: pointsav-engineering
short_description: "The Building Design System is built on five architectural constraints — flat-file storage, open standards, Rust and Tauri, offline-first operation, and Apache 2.0 licensing. Asset-anchored ownership, offline field use, IoT ingestion, and convergence of the model with lease and financial records follow from the architecture rather than being added on top."
cites: [ifc-4-3, iso-19650]
paired_with: flat-file-bim-leapfrog.es.md
---

PointSav's Building Design System is built on five architectural constraints that, taken individually, are mild inconveniences in any single feature comparison and, taken together, define a product category a hyperscaler cannot occupy without cannibalising its own revenue model. The constraints are flat-file storage, open standards, Rust and Tauri, offline-first operation, and Apache 2.0 licensing.

**Why it matters:** a building's digital record built this way is owned the way the building itself is owned — permanently, transferably, and without paying a vendor for continued access to it.

This article explains what flat-file BIM is, what it is not, and why five specific capabilities follow from the architecture rather than needing to be bolted on.

## The standards stack reached production maturity in 2024

The premise the architecture rests on is that the standards already exist, specify plain-text encodings, and sit inside ISO. IFC 4.3 was formally published as ISO 16739-1:2024 in April 2024, extending IFC from buildings to bridges, roads, rail, ports, and waterways. Its canonical serialisation, IFC-SPF, is ISO 10303-21 clear text — readable in any text editor. IDS 1.0 became the official buildingSMART standard on 1 June 2024. BCF 3.0 is a ZIP of XML markup plus PNG snapshots; unzipped, the per-topic directory tree is diff-able prose. CityJSON 2.0 is an OGC community standard, with CityJSONSeq used at national scale by TU Delft's 3DBAG dataset for over ten million Dutch buildings.

What is *not* yet production-ready matters as much. ifcJSON remains a community draft. IFC 5 is alpha, with a JSON-based IFCX serialisation borrowing USD-like composition from Pixar's OpenUSD; breaking changes are expected. The pragmatic conclusion: canonicalise on IFC-SPF today, mirror to ifcJSON opportunistically, and shape the object model so that an IFC 5 / IFCX migration is intended to be a serialisation swap rather than a rewrite.

**Why it matters:** nothing here depends on a standard PointSav authored or controls. The durability claim is a claim about ISO, not about PointSav.

## What "flat-file" means

A directory of plain-text and standardised-binary files that an ordinary text editor or SVG viewer can open without a proprietary SDK, decades after the software vendor that produced them is gone.

| Format | ISO / publisher | Role |
|---|---|---|
| IFC-SPF (`.ifc`) | ISO 16739-1:2024 | Authoritative geometry + semantics |
| IDS 1.0 | buildingSMART (June 2024) | Validation contract |
| BCF 3.0 | buildingSMART | Per-topic collaboration history |
| COBie via ifccsv | NIST | Asset handover |
| Per-element YAML sidecars | local convention | `Pset_*` + sensor + work-order data |
| Hash-addressed object store | local convention; Speckle-inspired | Versioned Merkle DAG |
| glTF 2.0 | ISO/IEC 12113:2022 | Visualisation cache (regenerable) |
| SVG | W3C Recommendation (no ISO/IEC number) | 2D drawings (regenerable) |
| CityJSONSeq | OGC | Portfolio / urban context |

The `.ifc` file is the authoritative spatial and semantic state of the building. Sidecars carry non-geometric data — ratings, quantities, sensor readings, work orders, lease references. The object-store layer gives the whole vault git-grade versioning semantics. Visualisation derivatives are caches that regenerate at will from the authoritative source. Any specific BIM viewer or authoring tool is replaceable; the archive is not.

**Why it matters:** replaceability is the whole design. A tool that disappears costs a re-render, not a re-survey.

## Five capabilities that follow from the architecture

### 1. Asset-anchored BIM

The digital record is signed with the land title and travels with the property deed when ownership changes hands. A multi-tenant SaaS platform cannot offer this without breaking its tenancy model: a new owner must be onboarded to the vendor's tenant, the model migrated, permissions reconstructed, the subscription repriced. A flat-file record is owned the way the building is owned — indefinitely, transferably, without vendor permission.

Cloud BIM subscription terms make the exposure explicit: a lapsed term requires the owner to enter a new subscription agreement for continued access to project data. The digital record is rented, not sold.

### 2. Offline-capable BIM for field use

Basements, rooftops, remote construction sites, air-gapped defence facilities, healthcare campuses under strict data-residency rules, low-connectivity regions — each is a workflow where a cloud-authoritative model is structurally impossible, because cloud-authoritative BIM requires live network access by construction. A Tauri and Rust shell hosting an offline IFC archive on a laptop or tablet preserves full functionality with no network dependency at all.

### 3. Vendor-obsolescence-survivable BIM

Buildings stand for fifty years and longer. Proprietary BIM authoring formats have compatibility windows of roughly three to five years. A flat-file substrate stays readable for decades after any particular vendor disappears. This matters most to public-sector BIM programmes (UK Government Level 2, US GSA, DoD, VA), cultural-heritage custodians, and long-horizon property owners — the buyers most exposed to vendor-discontinuation risk.

### 4. IoT ingestion directly into the archive

A flat-file archive with per-element YAML sidecars ingests sensor readings from a local MQTT broker, written as timestamped JSON records into the element's own sidecar, without the data leaving the owner's premises. That matters economically (no per-sensor metering), legally (GDPR residency, HIPAA in healthcare, export control in defence), and architecturally — the sensor history is versioned alongside the geometry rather than in a separate system that drifts.

### 5. Model, lease register, and financial ledger as one portable archive

To a property owner the building, the lease, the rent, and the financing are one asset: the building is where the lease applies, the lease is where the rent comes from, the rent services the loan, and the loan justified the building. Multi-tenant cloud cannot commingle model, lease register, and rent roll in a single owner-controlled archive — commercial confidentiality, data residency, financial-audit trails, and tenant isolation each prevent it independently.

The workplace application family — `app-workplace-memo`, `app-workplace-presentation`, `app-workplace-proforma`, and `app-workplace-bim` — is intended to converge these into one portable archive, so that a building's legal, financial, spatial, and operational identity is a single artifact that travels with the asset.

**Why it matters:** none of these five are features on a roadmap that could be dropped. Each is a direct consequence of choosing flat files, open standards, and offline-first — which is also why a cloud-native competitor cannot ship them without changing what it sells.

## Government regulatory acceptance is structurally favourable

The format stack — IFC-SPF, IDS 1.0, BCF 3.0, COBie — satisfies mandatory open-standard delivery requirements across US federal agencies (GSA, USACE, VA, NAVFAC), EU member states (Germany, Italy, Spain, Denmark, Norway, the Netherlands, Poland), the UK BIM Framework, Singapore's CORENET X (mandatory October 2026), Dubai (mandatory since January 2024), and the wider buildingSMART openBIM programme.

An offline-first, flat-file architecture is the only approach that natively satisfies ITAR air-gap requirements for defence work, EU Data Act sovereignty for European projects, HIPAA technical safeguards for VA healthcare facilities, and GDPR residency for EU government clients — without depending on a cloud vendor's contractual assurances. The Apache 2.0 licence governing the BIM Object data files is OSI-approved, FAR 12.212-compatible, and compatible with both public-sector procurement and commercial derivative use.

**Why it matters:** the compliance posture is a property of the file formats, not of a certification PointSav has to maintain.

## What flat-file BIM does not do well — yet

An honest accounting of the trade-offs:

- Real-time multi-user editing is slower than synchronous SaaS for charette-style design workshops. Cloud SaaS is genuinely better for synchronous design sessions.
- City-scale federation across a million or more buildings needs a different streaming architecture than a single-property archive provides.
- Generative BIM authoring tools from the major vendors are proprietary today. The substrate is ready for AI participation — the [[compounding-doorman|Doorman]] dispatches generative requests through an audit ledger — but a generative authoring tool is not planned for the v0.0.1 release.

These are deliberate trade-offs of the offline-first, vendor-obsolescence-survivable posture, not oversights awaiting a patch.

## See also

- [[city-code-as-composable-geometry]] — encoding regulatory requirements into the element specification itself
- [[worm-ledger-design]] — the append-only ledger pattern the archive versioning follows
- [[sel4-microkernel-substrate]] — the isolation substrate underneath offline deployments
