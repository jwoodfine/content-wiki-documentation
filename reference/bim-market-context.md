---
schema: foundry-doc-v1
type: topic
content_type: topic
slug: bim-market-context
short_description: "Building Information Modelling is now a government mandate across the jurisdictions that matter most to institutional real estate, with ISO 19650 and IFC as global defaults, and the UK Golden Thread creating legal market demand for portable, continuously maintained digital building records."
title: "BIM market context and regulatory landscape"
category: reference
language: en
paired_with: bim-market-context.es.md
bcsc_class: public-disclosure-safe
status: stable
last_edited: 2026-05-07
editor: pointsav-engineering
cites: [ifc-4-3, uniclass-2015, bsdd-v1, ids-1-0, iso-19650]
---

The architecture of the building industry's digital transformation is settled. The standards are ISO. The formats are open. The regulatory mandates are published. What remains unsettled is who will build the infrastructure layer that connects geometry, records, sensors, and legal title into a single portable archive — one that survives every software vendor that touches it. The [[totebox-archive|Totebox Archive]] is that infrastructure layer: a portable, [[worm-ledger-architecture|append-only ledger]] of every building record, transferable at sale and independently verifiable.

## The Global BIM Mandate

Building Information Modelling is no longer an industry preference. It is a government mandate across the jurisdictions that matter most to institutional real estate.

### United Kingdom — The Pioneer

The UK mandated BIM Level 2 for all centrally procured public projects in April 2016, becoming the first country to require collaborative 3D BIM across an entire public construction programme. The mandate requires IFC-compatible data delivery and adoption of ISO 19650 information management standards. As of 2026, the country is advancing toward a more integrated lifecycle standard, with the Building Safety Act 2022 adding a legal obligation for continuous digital records on higher-risk buildings.

### European Union — The Regulatory Framework

EU Directive 2014/24/EU on public procurement explicitly encourages member states to require BIM for publicly funded construction. The EU BIM Task Group, supported by the European Commission's DG GROW, published its Position Paper on BIM for Public Procurement in November 2025, describing BIM under ISO 19650 as "not simply a technology but a structured approach to managing information throughout the lifecycle of a public asset." The European Committee for Standardization (CEN/TC 442) has adopted all major ISO BIM standards as European Norms, including EN ISO 16739-1 (IFC), EN ISO 19650, and EN ISO 29481.

**Country-level mandates across Europe:**

| Country | Mandate | Format Required | Year |
|---|---|---|---|
| Denmark | All public projects over €677K | IFC | 2007 (first in world) |
| Norway | All public projects (Statsbygg) | IFC | 2010 |
| Finland | Senate Properties — all major projects | IFC | 2012 |
| Netherlands | Rijkswaterstaat infrastructure | IFC | 2012 |
| UK | All centrally procured public projects | IFC / ISO 19650 | 2016 |
| Germany | Federal Stufenplan — phased mandate | IFC | 2017 onwards |
| Spain | BIM Commission — large infrastructure | IFC | 2018+ |
| Italy | D.Lgs. 36/2023 — all public works phased | IFC | 2023+ |
| France | Encouraged across public works | IFC | Active |
| Poland | €10M+ projects by 2025, all by 2030 | IFC | Phased |
| Singapore | All new building applications (CORENET X) | IFC | 2025 |

The convergence is clear: ISO 19650 as the process standard and IFC as the data format are the global government default for building information. No country mandating BIM has mandated any proprietary format. The mandates are written around open standards.

### ISO 19650 — The Process Standard, Under Active Revision

ISO 19650 defines how information is managed throughout the lifecycle of a built asset using BIM. Part 6, focused on health and safety data, was released in 2025. The standard is currently under revision — proposed changes include clearer terminology, removal of repetitive content, a more logical workflow, and expanded focus on whole-lifecycle information covering operations, maintenance, and decommissioning.

**What this means for PointSav:** Every government-funded project in Europe and most major markets outside the US now legally requires IFC-format deliverables and ISO 19650-aligned information management. PointSav's flat-file archive, canonicalised on IFC-SPF, is the infrastructure that makes those mandates survivable beyond the construction phase. The [[sel4-microkernel-substrate|seL4 microkernel]] addresses the data-sovereignty requirement that cloud BIM platforms cannot meet structurally.

---

## The UK Golden Thread

The UK's Building Safety Act 2022 is the most commercially significant piece of building legislation in a generation. It emerged directly from the Grenfell Tower fire of 2017, in which 72 people died, and the subsequent Hackitt Review, which identified systemic failures in how building information was created, managed, and handed over.

### What the Golden Thread Requires

Section 88 of the Building Safety Act 2022 establishes the Golden Thread of information as a legal requirement for Higher-Risk Buildings (HRBs) — buildings of at least 7 storeys or 18 metres with at least 2 residential units. The requirement: a comprehensive, electronic, continuously maintained record of all safety-critical information about a building, from first design through occupation, including all design decisions and materials, all changes made during construction and occupation, inspection reports and maintenance records, fire safety strategy and structural safety data, and records from previous owners.

The Building Safety Alliance published detailed Golden Thread guidance in May 2025, coordinated with ISO and European data standards experts.

### The Digital Twin Connection

The Golden Thread has created, by statute, a legal market for exactly what a PointSav PropertyArchive delivers: a portable, version-controlled, continuously maintained digital record of a building, transferable at handover, independently verifiable, with no ongoing dependency on any vendor's continued existence. This is a procurement argument, not a technology argument.

---

## The Open BIM Standards Stack

The open BIM standards ecosystem reached production maturity between 2023 and 2025. Every component described below is either an ISO standard, an official buildingSMART standard, or an OGC community standard.

### buildingSMART International

buildingSMART International (bSI) is the non-profit standards body responsible for IFC, BCF, IDS, and the buildingSMART Data Dictionary. Its standards are developed openly and published under terms that permit free implementation.

### IFC — The Canonical Standard

IFC (Industry Foundation Classes) is published as **ISO 16739-1:2024**. It defines a comprehensive schema for representing buildings, bridges, roads, rail, ports, and waterways. It covers geometry, spatial structure, element properties, quantities, classifications, relationships, and process information.

IFC has three stable serialisation formats:
- **IFC-SPF** (`.ifc`) — ISO 10303-21 STEP Physical File, clear-text ASCII. The canonical archival format.
- **ifcXML** (`.ifcXML`) — XML serialisation of the same schema.
- **IFCZIP** (`.ifczip`) — ZIP compression of IFC-SPF. Useful for transmission.

### IFC 5 — The Next Generation

IFC 5 is under active development at buildingSMART. Its defining change is the introduction of **IFCX**, a new JSON-based serialisation inspired by Pixar's OpenUSD and using entity-component-system (ECS) decomposition. Key principles: multi-file composition, USD-style layering and overriding, and native JSON encoding with proper UTF-8. PointSav's object model is designed for IFC 5 / IFCX compatibility as a forward migration.

### BCF — BIM Collaboration Format

BCF 3.0 is the buildingSMART standard for communicating issues, clash reports, and design queries between BIM tools. Unzipped, it is a plain-text, git-friendly directory structure.

### IDS — Information Delivery Specification

IDS 1.0 became the official buildingSMART standard on 1 June 2024. An `.ids` file is an XML document that machine-validates whether an IFC model contains the required properties for a specific use case. IfcOpenShell's `ifctester` module validates any IFC file against any IDS file.

### bSDD — buildingSMART Data Dictionary

bSDD publishes building element classifications and property definitions as dereferenceable URLs returning JSON-LD. A bSDD URI is a stable, globally unique identifier for a building element type that any tool can look up and retrieve a machine-readable definition.

### CityJSON and CityJSONSeq

CityJSON 2.0 is an OGC Community Standard — a JSON encoding of the CityGML urban model standard. **CityJSONSeq** is its streaming variant: one JSON feature per line. TU Delft uses CityJSONSeq to serve the entire Netherlands building stock (~10 million records) via the 3DBAG dataset. For multi-building portfolio views, CityJSONSeq is the natural format for the `app-orchestration-bim` aggregation layer.

---

## File Formats

### Import Formats — Not Archive Formats

**RVT** is a closed binary format. For ISO 19650-compliant projects, the architect exports IFC at each project milestone. PointSav ingests IFC. The RVT file remains in the architect's authoring environment. This is the correct information architecture under every government BIM mandate — not a compromise.

The Open Design Alliance (ODA) provides a legally clean-room implementation for reading DWG/DXF formats. **DXF** is fully open (published specification); **DWG** is readable through ODA membership.

### The Open Archive Stack

Every format below is an ISO standard, a W3C standard, or a published open specification. Every one will be readable in 2076 by tools that do not yet exist.

| Format | Standard | Role |
|---|---|---|
| IFC-SPF (`.ifc`) | ISO 16739-1:2024 | Canonical archival format. Complete building model. |
| SVG (`.svg`) | W3C | 2D floor plans. IFC GUIDs embedded as element IDs. |
| glTF 2.0 (`.glb`) | ISO/IEC 12113:2022 | 3D viewer cache. Regenerated from canonical IFC on demand. |
| BCF 3.0 (`.bcf` decomposed) | buildingSMART | Per-issue XML + PNG snapshots. Git-native. |
| IDS 1.0 (`.ids`) | buildingSMART (June 2024) | Compliance validation schema. |
| YAML sidecars | PointSav-native | Per-element operational metadata keyed by IFC GUID. |
| CityJSONSeq | OGC Community | Portfolio and urban context. One building per line. |

**The 50-year readability test:** IFC-SPF, SVG, glTF, YAML, and BCF XML each pass — ISO standards with published specifications, readable by any conformant tool. Closed binary formats do not pass: they are version-locked to the vendor's continued existence.

---

## Cyber-Physical Connectivity — The Digital Twin Gap

### What a Digital Twin Requires

The UK National Digital Twin Programme and ISO 23247 converge on a definition requiring three components simultaneously present:

1. **Geometric representation** — a spatially accurate model of the physical asset
2. **Real-time sensor data** — live operational readings from the physical asset
3. **Operational and legal context** — the records that give sensor data its meaning

A 3D BIM model without sensors is a geometric record, not a digital twin. A sensor network without geometry is a data stream. A digital twin requires all three — linked with sufficient semantic precision that querying one dimension retrieves correlated data from the others.

### The Structural Gap

No current commercial platform delivers simultaneous, owner-controlled access to a building's geometric record, sensor data, lease register, financial ledger, and maintenance history in a single portable, offline-capable archive. This is not an oversight. It is a consequence of multi-tenant cloud architecture: co-mingling a tenant's BIM geometry with their financial ledger in a single owner-controlled record is architecturally incompatible with the data residency, access control, and revenue models of any shared-cloud platform.

---

## The IoT-BIM Integration Layer

The semantic web layer connecting sensor data to building geometry has converged on three complementary standards.

### Brick Schema

Brick (brickschema.org) is an RDF-based ontology for building metadata, focused on HVAC, electrical, plumbing, and sensing systems. Brick 1.3 (2023) includes alignment with IFC 4.3. Each HVAC element in the IFC model holds a Brick Schema URI in its YAML sidecar; each sensor's sidecar references the IFC GUID of the element it is attached to.

### SAREF — Smart Applications REFerence Ontology

SAREF is an ETSI IoT standard (SAREF4BLDG for the buildings extension). It aligns with IFC at the element level, enabling information reuse between design-phase BIM and operations-phase IoT data.

### Project Haystack

Project Haystack is an open-source tagging taxonomy for building equipment data, particularly BMS points. Where Brick provides a graph-based ontology, Haystack provides flat tagging that many BMS vendors support natively. The two are complementary.

### The PointSav IoT Integration Pattern

```
Physical sensor (BACnet / KNX / MQTT)
 ↓ local MQTT broker on ToteboxOS node
service-bim ingestion
 ↓ writes to element YAML sidecar
elements/{IFC-GUID}/sensors.yaml
```

Sensor readings are appended to a JSONL time-series file. The file grows append-only. No database engine is required. The entire sensor history is readable by any JSONL-capable tool.

---

## The Interoperability Argument

The ISO 19650-compliant project delivery workflow that every government-mandated project already uses is:

```
Architect authors in BIM authoring tool
 ↓ IFC export (at each project milestone)
Coordination platform
 ↓ IFC as exchange format
FM platform / archive (PointSav PropertyArchive)
 ↓ IFC as permanent record
```

PointSav sits at the end of this workflow as the permanent archive — the ISO 19650 "Asset Information Model" that ISO 19650 Part 3 requires to be handed over and maintained. The architect never opens PointSav. The contractor never opens PointSav. They deliver IFC at handover, which is what the law already requires on any mandated project.

PointSav produces DXF as a coordination output — readable in every drafting tool. SVG floor plans are readable in every browser and vector graphics editor. glTF is viewable in every major 3D application. The archive produces derivatives for any workflow without compromising the canonical IFC.

---

## The Leapfrog Thesis

Five capabilities are absent from every currently shipping commercial BIM platform — not through oversight, but through structural incompatibility with the subscription cloud model:

1. **Asset-anchored BIM.** A PointSav PropertyArchive, exported as a bootable disk image, transfers with the deed. The buyer receives the building's complete institutional memory. No current platform can offer this credibly because it undermines subscription renewal.

2. **Offline-capable BIM.** Basements, rooftops, rural construction sites, air-gapped defence facilities, healthcare campuses with strict data residency requirements, and lower-connectivity regions are structurally inaccessible to cloud-first BIM platforms.

3. **Vendor-obsolescence-survivable BIM.** A building lives 50–100 years. A software subscription lives until the vendor changes its pricing model. The PointSav archive, written in IFC-SPF + YAML + SVG + glTF, will be readable in 2076 by tools that do not yet exist.

4. **IoT integration without cloud intermediary.** A PointSav [[totebox-os|ToteboxOS]] node ingests BACnet / KNX / MQTT sensor data directly into the archive via a local broker — the data never leaves the owner's premises unless the owner chooses to send it.

5. **BIM + lease + financial ledger in one portable archive.** A PropertyArchive holding a building's geometry, lease register, financial ledger, and maintenance history in a single owner-controlled archive is architecturally impossible for any multi-tenant shared platform. For a property owner, these are not four datasets — they are one record about one asset. The [[customer-owned-graph-ip|customer-owned graph]] principle means the record belongs to the property owner, not to any platform vendor.

### The 2030 Horizon

The convergence of three independent forces by 2030 creates the market PointSav is architecting toward:

- **The tokenisation market.** The tokenised real estate market is projected toward $30 trillion by 2034. Every tokenised property currently lacks an operational record. A PointSav PropertyArchive, attached to a land title and delivered with the building at sale, is the operational record the tokenisation market is missing.
- **The Golden Thread mandate.** The UK Building Safety Act's Golden Thread requirement (in force April 2024) creates a legal obligation for exactly the continuous, transferable, digitally maintained building record that a PropertyArchive delivers.
- **The seL4 security position.** The seL4 microkernel's formally verified security properties address the one concern that prevents classified, healthcare, and defence clients from adopting cloud BIM: data sovereignty.

---

## Bibliography

1. buildingSMART International. *IFC 4.3 Formally Approved and Published as an ISO Standard.* April 2024.
2. ISO. *ISO 16739-1:2024 — Industry Foundation Classes (IFC).* 2024.
3. buildingSMART International. *IFC5 Development Repository.* github.com/buildingSMART/IFC5-development
4. buildingSMART International. *IDS 1.0 — Information Delivery Specification.* 1 June 2024.
5. EU BIM Task Group. *Position Paper on BIM for Public Procurement.* November 2025.
6. European Commission. *EU Directive 2014/24/EU on Public Procurement.* 2014.
7. ISO. *ISO 19650 — Information Management Using Building Information Modelling.* Parts 1–6. 2018–2025.
8. UK Government / HSE. *Keeping Information About a Higher-Risk Building: The Golden Thread.* GOV.UK. September 2024.
9. UK Parliament. *Building Safety Act 2022.* Section 88 — Golden Thread.
10. Building Safety Alliance. *Golden Thread Guidance Documents.* May 2025.
11. IfcOpenShell. *The Open Source IFC Toolkit and Geometry Engine.* ifcopenshell.org
12. ThatOpen Company. *web-ifc Documentation.*
13. Khronos Group. *glTF — Runtime 3D Asset Delivery.*
14. CDBB. *The Gemini Principles.* Centre for Digital Built Britain. 2018.
15. TU Delft. *3DBAG — CityJSONSeq Dataset of Dutch Building Stock.* 3dbag.nl
16. brickschema.org. *Brick Schema 1.3.*
17. ETSI. *SAREF — Smart Applications REFerence Ontology.* ETSI TS 103 264.
18. Chung, J. & Shelden, D. *A Framework of ifcJSON-Based Digital Twin Platform.* ICCCBE 2024. Springer, 2025.
19. Tandfonline. *Development and Demonstration of a Digital Twin Platform Leveraging Ontologies.* DOI: 10.1080/19401493.2025.2504005
