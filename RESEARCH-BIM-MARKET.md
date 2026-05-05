# Building Information Modelling — Market Research & Strategic Context

**Document:** `RESEARCH-BIM-MARKET.md`
**Repository:** `content-wiki-documentation/research/`
**Version:** 1.0 — April 2026
**Status:** Living document — updated as the market evolves
**Audience:** Developers joining the project · Investment community · Procurement officers
**Maintained by:** PointSav Digital Systems

---

*The architecture of the building industry's digital transformation is now settled. The standards are ISO. The formats are open. The regulatory mandates are published. What remains unsettled is who will build the infrastructure layer that connects geometry, records, sensors, and legal title into a single portable archive — one that survives every software vendor that touches it. This document explains the landscape that makes that question commercially significant, and the architectural position PointSav occupies within it.*

---

## Table of Contents

1. [The Global BIM Mandate — A Regulatory Tailwind](#1-the-global-bim-mandate)
2. [The UK Golden Thread — The Clearest Institutional Signal](#2-the-uk-golden-thread)
3. [The Competitive Landscape — Who Builds What](#3-the-competitive-landscape)
4. [The Open BIM Standards Stack — The Technical Foundation](#4-the-open-bim-standards-stack)
5. [File Formats — The Definitive Briefing](#5-file-formats)
6. [Cyber-Physical Connectivity — The Digital Twin Gap](#6-cyber-physical-connectivity)
7. [The IoT-BIM Integration Layer — What the Standards Say](#7-the-iot-bim-integration-layer)
8. [The Interoperability Argument — Working With, Not Against](#8-the-interoperability-argument)
9. [The Leapfrog Thesis — What the 2030 Horizon Looks Like](#9-the-leapfrog-thesis)
10. [Bibliography](#10-bibliography)

---

## 1. The Global BIM Mandate

Building Information Modelling is no longer an industry preference. It is a government mandate across the jurisdictions that matter most to institutional real estate.

### United Kingdom — The Pioneer

The UK mandated BIM Level 2 for all centrally procured public projects in April 2016, becoming the first country to require collaborative 3D BIM across an entire public construction programme. The mandate requires IFC-compatible data delivery and adoption of ISO 19650 information management standards. As of 2026, the country is advancing toward a more integrated lifecycle standard, with the Building Safety Act 2022 adding a legal obligation for continuous digital records on higher-risk buildings (see Section 2).

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

The convergence is unmistakable: ISO 19650 as the process standard and IFC as the data format are the global government default for building information. No country mandating BIM has mandated Revit. No country mandating BIM has mandated any proprietary format. The mandates are written around open standards.

### ISO 19650 — The Process Standard, Under Active Revision

ISO 19650 defines how information is managed throughout the lifecycle of a built asset using BIM. Part 6, focused on health and safety data, was released in 2025. The standard is currently under revision — proposed changes include clearer terminology, removal of repetitive content, a more logical workflow, and expanded focus on whole-lifecycle information covering operations, maintenance, and decommissioning. More governments are adopting it: the UK, UAE, Singapore, Germany, and India are all applying ISO 19650 on major public infrastructure.

**What this means for PointSav:** Every government-funded project in Europe and most major markets outside the US now legally requires IFC-format deliverables and ISO 19650-aligned information management. PointSav's flat-file archive, canonicalised on IFC-SPF, is not an alternative to these mandates — it is the infrastructure that makes those mandates survivable beyond the construction phase.

---

## 2. The UK Golden Thread

The UK's Building Safety Act 2022 is the most commercially significant piece of building legislation in a generation. It emerged directly from the Grenfell Tower fire of 2017, in which 72 people died, and the subsequent Hackitt Review, which identified systemic failures in how building information was created, managed, and handed over.

### What the Golden Thread Requires

Section 88 of the Building Safety Act 2022 establishes the Golden Thread of information as a legal requirement for Higher-Risk Buildings (HRBs) — buildings of at least 7 storeys or 18 metres with at least 2 residential units. The requirement: a comprehensive, electronic, continuously maintained record of all safety-critical information about a building, from first design through occupation, including:

- All design decisions and the materials and methods used
- All changes made during construction and occupation
- Inspection reports and maintenance records
- Fire safety strategy and structural safety data
- Records from previous owners

The Building Safety Alliance published detailed Golden Thread guidance in May 2025, coordinated with ISO and European data standards experts.

### The Digital Twin Connection

The ICE (Institution of Civil Engineers) has described the Golden Thread as having "many of the same goals that BIM has been trying to achieve for years." The GOV.UK guidance specifies that the record-keeping system must have version control. It must be accessible in a simple format. It must be continuously updated. It must transfer with the building at handover.

The Building Safety Act has created, by statute, a legal market for exactly what a PointSav PropertyArchive delivers: a portable, version-controlled, continuously maintained digital record of a building, transferable at handover, independently verifiable, with no ongoing dependency on any vendor's continued existence.

**What this means for PointSav:** The Golden Thread is not a compliance checkbox for architects. It is a permanent record-keeping obligation for building owners and operators — the accountable persons. The Woodfine showcase directly demonstrates Golden Thread compliance on a real property portfolio. This is a procurement argument, not a technology argument.

---

## 3. The Competitive Landscape

The BIM software market is organised around five major vendor ecosystems and a growing open-source layer. Each ecosystem has a coherent commercial logic, and each has structural constraints that follow from that logic.

### Autodesk — The Dominant Platform

Autodesk holds the largest share of the global BIM authoring market through Revit (architectural and structural BIM), AutoCAD (2D drafting), Navisworks (coordination and clash detection), and the Autodesk Construction Cloud (ACC) platform. The Autodesk Platform Services (APS), formerly Forge, provides API access to Autodesk's cloud infrastructure.

**2025–2026 pricing and commercial trajectory:** Revit list price is approximately $3,000 per seat per year. The AEC Collection is approximately $3,300. APS moved to a token-based pricing model with a migration deadline of February 2026; enterprise Token Flex commitments begin at roughly $120,000 annual floor. An EMEA subscription pilot announced in May 2025 adds approximately €3,725 per month per region for heavy Data Management API consumers. Annual renewal discounts and multi-year discounts have been reduced or eliminated.

**Autodesk Tandem** is Autodesk's digital twin product, introduced to capture the operations and maintenance market. Its contract terms state explicitly that when a Token Flex term lapses, customers "will need to enter into a new Token Flex Term for continued access to Your Project data." The twin rents. It does not sell.

**AI direction:** Project Bernini (a 3-billion-parameter generative 3D foundation model announced May 2024) remains research-only. Neural CAD, announced at AU 2025, is a category label, not a shipped product. Forma's Building Layout Explorer for parametric massing is the only production AI feature with narrow scope. Customer project data feeds vendor model training under vendor terms.

**Structural constraint:** Autodesk's revenue model depends on per-seat recurring subscriptions and usage-based cloud tokens. A product that allows customers to own their data permanently and export it completely would cannibalize both streams. This is not a strategic choice Autodesk can make.

### Nemetschek Group — The European Ecosystem

The Nemetschek Group (Frankfurt: NEM) is Germany's largest AEC software company, founded in 1963, publicly listed since 1999. Its brands span the full building lifecycle:

| Brand | Category | Notes |
|---|---|---|
| **Graphisoft / ArchiCAD** | BIM authoring | Founded Budapest 1982; acquired 2006 |
| **Allplan** | Engineering BIM | German-origin CAD/BIM |
| **Vectorworks** | Design / landscape | US-origin (formerly Diehl Graphsoft, acquired 2000) |
| **Bluebeam** | PDF markup / review | US; acquired 2014 |
| **Solibri** | Model checking / QA | Finnish; acquired 2015 |
| **Spacewell** | IWMS / FM | Belgian (MCS Solutions); acquired 2018 |
| **GoCanvas** | Field data capture | US; acquired 2024 |
| **HCSS** | Heavy civil construction | Texas; acquisition agreed April 2026, closes H2 2026 |

**Graphisoft specifically:** ArchiCAD 29 shipped October 2025 with IFC 4.3 implementation, MEP Designer (a new product), and AI Assistant (beta, full commercial release planned 2026). Customer data is stated not to be used for AI training, consistent with Nemetschek Group privacy standards. From 2026, ArchiCAD is available only by subscription — perpetual licences ended December 2024 for new customers. BIMcloud is Graphisoft's team collaboration platform.

**Nemetschek's openBIM position:** Nemetschek is a buildingSMART member and OpenBIM Charter signatory. The group publicly advocates for IFC and open standards. An April 2024 mutual API agreement with Autodesk enabled improved interoperability between Revit and ArchiCAD workflows. Solibri's deprecation of Solibri Anywhere (the free IFC viewer) in April 2026 signals that standalone viewing is being consolidated into paid platforms. In April 2026, Nemetschek agreed to acquire HCSS, a US heavy civil construction software company generating USD 215 million revenue at 40% EBITDA margins — a clear expansion into North American infrastructure.

**Structural position:** Nemetschek's openBIM advocacy is genuine at the format level and commercially strategic at the platform level. IFC compatibility is a competitive advantage against Autodesk (whose IFC export quality has been a documented criticism from the AEC industry). But Nemetschek's collaboration and FM products (BIMcloud, Spacewell) remain cloud-dependent, proprietary SaaS.

### Bentley Systems — Infrastructure and Engineering

Bentley (private, backed by Siemens AG as a minority investor) addresses infrastructure — bridges, roads, rail, utilities — as much as buildings. Its iTwin Platform provides digital twin infrastructure; iTwin.js is MIT-licensed on GitHub, but non-Snapshot (production) iModels require runtime authentication against Bentley's Azure-hosted services. OpenBuildings and MicroStation serve the authoring market. AssetWise handles asset operations. SYNCHRO provides 4D construction scheduling.

**Structural constraint:** Bentley's "open" positioning (iTwin.js MIT licence) is architecturally genuine for the SDK and commercially constrained at the data layer. The production data model requires Bentley's cloud. An application can be freely distributed; the data cannot be freely portable.

### Trimble — The Trades and Field Layer

Trimble serves contractors and trades as much as architects and engineers. Tekla Structures is the dominant reinforced concrete and structural steel authoring platform. Trimble Connect is a cloud-based BIM collaboration platform supporting 45+ file formats including IFC, DWG, and RVT. SketchUp remains widely used for early-stage design. Nova is Trimble's emerging unified platform strategy.

**Pricing:** Trimble Connect is approximately $12–$13 per user per month at standard tiers. The freemium entry point is more accessible than Autodesk or Bentley, but collaboration history, issue tracking, and version control all live in Trimble's cloud database.

### The Open-Source Layer — The Foundation PointSav Builds On

| Project | Licence | Maintained by | Role |
|---|---|---|---|
| **IfcOpenShell 0.8.5** | LGPL-3.0 | Open-source community | IFC parsing, geometry, conversion, validation |
| **Bonsai (BlenderBIM)** | GPL-3.0 | Dion Moult et al. | Full IFC authoring in Blender |
| **FreeCAD BIM** | LGPL-2.1 | FreeCAD community | IFC-native BIM workbench |
| **web-ifc 0.77** | MPL-2.0 | ThatOpen Company | WASM IFC parser for browser |
| **@thatopen/components** | MIT | ThatOpen Company | Web BIM viewer toolkit |
| **xeokit-sdk** | AGPL-3.0 | xeolabs / Creoox | High-performance WebGL BIM viewer |
| **Speckle** | Apache-2.0 | Speckle Systems | BIM data platform, object graph |
| **OpenCascade** | LGPL-2.1 | Open CASCADE SAS | 3D geometry kernel (C++) |

IfcOpenShell 0.8.5, released April 2026, is the most complete open-source IFC toolkit available. It parses, writes, validates, converts, and extracts geometry from IFC files. Its `IfcConvert` tool converts IFC to SVG, OBJ, Collada, and glTF. The `ifctester` module validates against IDS 1.0. The `ifcdiff` module computes semantic differences between IFC versions.

---

## 4. The Open BIM Standards Stack

The open BIM standards ecosystem reached production maturity between 2023 and 2025. Every component described below is either an ISO standard, an official buildingSMART standard, or an OGC community standard. None requires a proprietary SDK to read or write.

### buildingSMART International

buildingSMART International (bSI) is the non-profit standards body responsible for IFC, BCF, IDS, and the buildingSMART Data Dictionary. It operates as a neutral, multi-stakeholder organisation with members including vendors (including Autodesk and Nemetschek), governments, and research institutions. Its standards are developed openly and published under terms that permit free implementation.

### IFC — The Canonical Standard

IFC (Industry Foundation Classes) is the lingua franca of open BIM. Published as **ISO 16739-1:2024**, it defines a comprehensive schema for representing buildings, bridges, roads, rail, ports, and waterways — every physical asset type relevant to the built environment. It covers geometry, spatial structure, element properties, quantities, classifications, relationships, and process information.

IFC has three stable serialisation formats:
- **IFC-SPF** (`.ifc`) — ISO 10303-21 STEP Physical File, clear-text ASCII. The canonical archival format.
- **ifcXML** (`.ifcXML`) — XML serialisation of the same schema. Larger files, more developer-friendly for certain toolchains.
- **IFCZIP** (`.ifczip`) — ZIP compression of IFC-SPF. Useful for transmission; not ideal for version control.

IFC 4.3 (the current ISO version) introduced extended support for infrastructure assets and improved IFC-SPF encoding with explicit UTF-8 support as a migration path. The installed base remains split between IFC 2x3 (legacy projects) and IFC 4.x (modern workflows) — IFC 2x3 remains widely supported for import/export compatibility.

### IFC 5 — The Next Generation

IFC 5 is under active development at buildingSMART. Its defining change is the introduction of **IFCX**, a new JSON-based serialisation inspired by Pixar's OpenUSD and using entity-component-system (ECS) decomposition. The alpha is available at `github.com/buildingSMART/IFC5-development`. The schema is defined in TypeSpec. Key architectural principles: multi-file composition (no more monolithic blobs), USD-style layering and overriding, and native JSON encoding with proper UTF-8. Breaking changes are expected; no release date has been announced. **PointSav's object model should be designed for IFC 5 / IFCX compatibility as a forward migration, not as a current dependency.**

### BCF — BIM Collaboration Format

BCF 3.0 is the buildingSMART standard for communicating issues, clash reports, and design queries between BIM tools. A `.bcf` file is a ZIP archive containing per-topic directories of XML markup files and PNG snapshots. Unzipped, it is a plain-text, git-friendly directory structure — exactly the structure PointSav uses in the `service-BIM/issues/` directory layout.

### IDS — Information Delivery Specification

IDS 1.0 became the official buildingSMART standard on 1 June 2024. An `.ids` file is an XML document that machine-validates whether an IFC model contains the required properties, classifications, and information for a specific use case. IfcOpenShell's `ifctester` module validates any IFC file against any IDS file. This is the automated compliance check that fires when a new IFC model arrives in the `service-BIM/ingestion/queue/`.

### bSDD — buildingSMART Data Dictionary

bSDD publishes building element classifications and property definitions as dereferenceable URLs returning JSON-LD. A bSDD URI is a stable, globally unique identifier for a building element type — a door, an HVAC unit, a structural column — that any tool can look up and retrieve a machine-readable definition. The per-element YAML sidecars in the PointSav archive reference bSDD URIs as the canonical classification for each element.

### CityJSON and CityJSONSeq

CityJSON 2.0 is an OGC Community Standard — a JSON encoding of the CityGML urban model standard. **CityJSONSeq** is its streaming variant: one JSON feature per line, one file per city object. TU Delft uses CityJSONSeq to serve the entire Netherlands building stock (~10 million records) via the 3DBAG dataset, demonstrating production-scale performance at the portfolio level. For multi-building portfolio views, CityJSONSeq is the natural format for the `app-orchestration-BIM` aggregation layer.

---

## 5. File Formats

This is the section that matters most for developers evaluating the architecture and investors evaluating the durability of the data model. The central question: what file format should PointSav use as the canonical archive format, and how does that choice interact with the industry's dominant proprietary formats?

### The Proprietary Formats — Import Paths, Not Archive Formats

**RVT (Revit)** is a closed binary format owned by Autodesk. Autodesk has maintained this closure deliberately for twenty-five years. There are exactly two practical paths to reading an RVT file without Autodesk software:

1. **Open Design Alliance (ODA) BimRv library** — the ODA has reverse-engineered RVT through legal clean-room analysis. Their SDK reads RVT R2015 through current versions. ODA membership costs approximately $4,000 per year plus per-product royalties. This is the production path for Phase 2 RVT ingestion.

2. **Autodesk APS (Platform Services)** — Autodesk's own cloud API converts RVT to derivative formats including IFC. This reintroduces a cloud dependency and per-translation costs. Appropriate only as an optional first-ingestion step, not as a runtime dependency.

**The practical Phase 1 position:** IFC export from Revit has existed since 2012 and is the ISO 19650-compliant handover deliverable on any mandate-governed project. For the Woodfine showcase and any ISO 19650-compliant customer, the architect exports IFC at handover. PointSav ingests IFC. The RVT file remains in the architect's authoring environment. This is not a compromise — it is the correct information architecture under every government BIM mandate.

**DWG** is in a different legal position than RVT. The Open Design Alliance was founded specifically to provide legal DWG compatibility, and the `dxf` crate in Rust provides read/write access to DXF (the published ASCII version of AutoCAD's format). DWG read/write is achievable through ODA membership without requiring Autodesk involvement.

**DXF** is fully open. Autodesk published the DXF specification and it is freely implementable. Rust's `dxf` crate provides DXF r12 through current read/write. DXF is the coordination export format — what PointSav can produce for architects and contractors who need to take geometry back into AutoCAD workflows.

### The Open Formats — The Archive Stack

The following formats constitute the complete flat-file BIM archive. Every one is an ISO standard, a W3C standard, or a published open specification. Every one is readable by any text editor or standards-compliant tool in 2026 — or 2076.

**IFC-SPF (`.ifc`)** — The canonical archival format. ISO 16739-1:2024. Plain ASCII text. The complete building model: geometry, spatial structure, elements, properties, quantities, relationships, classifications. Readable by IfcOpenShell, xBIM, FreeCAD, ArchiCAD, Revit (import), Navisworks, Solibri, BIMvision, and every other serious BIM tool. SHA-256 sealed. The system of record.

**SVG (`.svg`)** — W3C standard. The 2D floor plan format. IfcOpenShell generates SVG floor plans directly from IFC files. IFC GUIDs are embedded as SVG element IDs, enabling click-to-select spatial queries from a 2D drawing. Human-readable in any text editor, renderable in any browser, printable at any scale. One SVG file per building level.

**glTF 2.0 (`.glb`)** — ISO/IEC 12113:2022. The 3D viewer cache. Not archival — geometry only, no BIM semantics survive the export. Regenerated on demand from the canonical IFC. Served to `app-console-BIM` and `app-workplace-BIM` for visual inspection. IfcOpenShell's `IfcConvert` generates glTF from IFC.

**BCF 3.0 (`.bcf` decomposed)** — buildingSMART standard. Per-issue directories of XML markup and PNG snapshots. Diff-friendly, git-native, human-readable.

**IDS 1.0 (`.ids`)** — buildingSMART standard (June 2024). XML. Defines what properties the IFC model must contain. Validated automatically at ingestion.

**YAML sidecars** — PointSav-native. One YAML file per IFC element, keyed by IFC GUID. Holds operational metadata: work order history, IoT sensor assignments, lease linkages, document references. Not part of the IFC standard — this is the PointSav operational layer.

**CityJSONSeq** — OGC Community Standard. Portfolio and urban context. One building per line. Used at the `app-orchestration-BIM` aggregation level for multi-property queries.

**ifcJSON** — buildingSMART community draft (not yet ISO). JSON representation of IFC. Useful for API consumption and developer tooling. Generated as a derivative of IFC-SPF; never the source of record until the spec reaches ISO stability.

### The 50-Year Readability Test

Every format in the PointSav archive stack passes the following test: *Can this file be read in 2076 without any software that exists today?*

| Format | 50-year verdict | Reason |
|---|---|---|
| IFC-SPF | **Yes** | ISO standard, plain ASCII text, self-describing schema header |
| SVG | **Yes** | W3C standard, XML, rendered by every browser since 2001 |
| glTF | **Yes** | ISO standard, JSON + binary buffers, open specification |
| YAML | **Yes** | Human-readable, widely implemented, no proprietary dependency |
| BCF XML | **Yes** | Standard XML, self-describing |
| RVT | **No** | Closed binary, Autodesk-controlled, version-locked |
| DWG | **Partial** | ODA-maintained compatibility; non-zero obsolescence risk |
| Autodesk Tandem data | **No** | Lives in Autodesk's tenancy; evaporates when subscription lapses |

This is not a theoretical argument. Revit 2005 files cannot be opened in Revit 2026 without a conversion process managed by Autodesk. Early ArchiCAD files from the 1980s are unrecoverable without obsolete hardware. IFC files from 2001 open in every current IFC viewer. The format choice is an insurance decision as much as a technology decision.

---

## 6. Cyber-Physical Connectivity — The Digital Twin Gap

### What a Digital Twin Actually Is

The term "digital twin" is used broadly enough to cover everything from a 3D model to a live sensor network. The canonical definition comes from the Gemini Principles (CDBB, 2018), which established three requirements for a national digital twin: it must have **purpose** (serve identifiable needs), it must be **trustworthy** (secure, accurate, and accessible), and it must **function as a platform** (enabling data to be combined with other data).

The UK National Digital Twin Programme and ISO 23247 (Digital Twin framework for manufacturing, applicable to buildings by extension) converge on a definition that requires three components to be simultaneously present:

1. **Geometric representation** — a spatially accurate model of the physical asset
2. **Real-time sensor data** — live operational readings from the physical asset
3. **Operational and legal context** — the records that give sensor data its meaning

A 3D BIM model without sensors is a geometric record, not a digital twin. A sensor network without geometry is a data stream, not a digital twin. A digital twin requires all three — and it requires them linked to each other with enough semantic precision that querying one dimension retrieves correlated data from the others.

### What Hyperscalers Actually Deliver

**Autodesk Tandem** connects to live data sources via an API and overlays sensor readings on a 3D model. It is the closest thing Autodesk offers to a building digital twin. Its structural limitations: data lives in Autodesk's Azure tenancy; sensor integrations are available for a limited set of data providers; the twin disappears when billing lapses. The operational and legal context layer — the lease register, the financial ledger, the maintenance history, the regulatory compliance record — is not part of Tandem's data model. Tandem is a geometry + sensor overlay, not a complete digital twin.

**Bentley iTwin Experience** provides 4D (time) and 5D (cost) extensions to the geometric model, plus IoT connectivity via the iTwin IoT module. The architecture is more open than Autodesk's — iTwin.js is MIT-licensed and the platform supports self-hosting of some components. But production iModels still require Bentley's cloud authentication. The legal and financial record layer is not native.

**Siemens Xcelerator Buildings** addresses building automation at the BMS level, connecting to BACnet/KNX/Modbus building systems. It is the most capable platform for operational technology (OT) integration. But it targets enterprise facilities management at enterprise pricing, and the data model is Siemens-proprietary.

**The structural gap:** No hyperscaler product in 2026 delivers simultaneous, owner-controlled access to a building's geometric record, sensor data, lease register, financial ledger, and maintenance history in a single portable, offline-capable archive. This is not an oversight. It is a consequence of multi-tenant cloud architecture: co-mingling a tenant's BIM geometry with their financial ledger in a single owner-controlled record is incompatible with the data residency, access control, and revenue models of any SaaS platform.

### What the Research Literature Shows

The gap between BIM-as-built and BIM-in-operation is one of the most active research areas in AEC informatics. Three findings from the 2024–2025 literature are directly relevant:

A 2025 paper in *Tandfonline* (DOI 10.1080/19401493.2025.2504005) found: "status quo BIMs are not easily compatible with IoT integration due to their legacy data standards and originally intended use as a static information exchange platform." The paper recommended SAREF4BLDG alignment over ifcOWL for IoT integration, citing "unnecessary complexity" in ifcOWL's backward-compatible design.

Researchers at Eindhoven University of Technology (cited in AlterSquare, July 2025) successfully integrated IFC building models with time-series data from a Honeywell BMS in TU/e's Atlas building. Their approach used an IFC file to create a building structure graph and a Brick Ontology graph for BMS sensor semantics — enabling users to query building data and visualize sensor readings against the spatial model. The BMS produced over 1.3 million data points monthly.

A 2025 ICCCBE paper (Oak Ridge National Laboratory, published Springer 2025) demonstrated an ifcJSON-based digital twin platform that "effectively federates building information with IoT sensor data and ontologies, such as Brick ontology and ifcOWL" — specifically using a linked-data version of ifcJSON rather than IFC-SPF, enabling SPARQL queries across the federated graph.

---

## 7. The IoT-BIM Integration Layer

The semantic web layer connecting sensor data to building geometry has converged on three complementary standards. PointSav's per-element YAML sidecar architecture maps directly to each.

### Brick Schema

Brick (brickschema.org) is an RDF-based ontology for building metadata, focused on HVAC, electrical, plumbing, and sensing systems. It provides a controlled vocabulary for describing sensors, actuators, equipment, locations, and the relationships between them. Brick 1.3 (2023) includes alignment with IFC 4.3 schema expansions and is specifically designed to answer queries like "which sensors measure temperature in zones served by AHU-3?" — the spatial-operational query that is the fundamental digital twin use case.

**PointSav mapping:** Each HVAC element in the IFC model has a Brick Schema URI in its YAML sidecar. Each IoT sensor's YAML sidecar references the IFC GUID of the element it is physically attached to and the Brick Schema class of what it measures. The YAML structure bridges IFC geometry and Brick semantics without requiring a runtime RDF store.

### SAREF — Smart Applications REFerence Ontology

SAREF is an ETSI IoT standard (SAREF4BLDG for the buildings extension). It defines standard classes for smart building devices, functions, states, and measurements. SAREF4BLDG aligns with IFC at the element level, enabling information reuse between design-phase BIM and operations-phase IoT data. The 2025 research literature (Tandfonline DOI cited above) found SAREF4BLDG preferable to ifcOWL for IoT integration in practice.

### Project Haystack

Project Haystack is an open-source tagging taxonomy for building equipment data, particularly BMS points. Where Brick provides a graph-based ontology, Haystack provides a flat tagging approach that many BMS vendors support natively. The two are complementary: Haystack tags map to Brick classes, and Brick provides the richer semantic context.

### The PointSav IoT Integration Pattern

```
Physical sensor (BACnet / KNX / MQTT)
        ↓  local MQTT broker on ToteboxOS node
service-BIM ingestion
        ↓  writes to element YAML sidecar
elements/{IFC-GUID}/sensors.yaml

sensors.yaml contents:
  - sensor_id: "HVAC-AHU-3-TEMP-01"
    brick_class: "https://brickschema.org/schema/1.3#Temperature_Sensor"
    ifc_element_guid: "2O2Fr$t4X7Zf8NOew3FLOH"
    protocol: "BACnet/MSTP"
    unit: "°C"
    readings_path: "telemetry/HVAC-AHU-3-TEMP-01.jsonl"
    last_reading: 21.3
    last_reading_timestamp: "2026-04-22T09:15:00Z"
```

Sensor readings are appended to a JSONL (one JSON object per line) time-series file. The file grows append-only. No database engine is required. The entire sensor history is readable by any JSONL-capable tool.

---

## 8. The Interoperability Argument

The most common concern raised by procurement officers and project teams evaluating PointSav is: *"Does adopting this platform mean my architects have to stop using Revit? Do my contractors have to stop using AutoCAD?"*

The answer is no, and the reason is architectural.

### The openBIM Workflow

The ISO 19650-compliant project delivery workflow that every government-mandated project already uses is:

```
Architect authors in Revit / ArchiCAD / Allplan
        ↓  IFC export (at each project milestone)
Coordination platform (BIM 360, Trimble Connect, Solibri)
        ↓  IFC as exchange format
FM platform / archive (PointSav PropertyArchive)
        ↓  IFC as permanent record
```

PointSav sits at the end of this workflow as the permanent archive — the ISO 19650 "Asset Information Model" that ISO 19650 Part 3 (Operation phase) requires to be handed over and maintained. The architect never opens PointSav. The contractor never opens PointSav. They deliver IFC at handover, which is what the law already requires on any mandated project.

### IFC Export Quality

A legitimate concern: Autodesk's native IFC exporter from Revit has documented quality issues — property sets can be incomplete, geometry can be tessellated rather than exact, and some element types export with semantic loss. Three mitigations are available:

1. **Bonsai IFC Exporter for Revit** — an open-source alternative IFC exporter developed by the Bonsai (BlenderBIM) team, available as a Revit plugin. Produces higher-fidelity IFC than Autodesk's native exporter.
2. **IDS validation at ingestion** — the `service-BIM` daemon validates incoming IFC against the property requirements specified in `requirements/handover.ids`. Models that fail validation are flagged before they enter the archive.
3. **COBie** — Construction Operations Building Information Exchange, a structured spreadsheet format for FM data, can supplement IFC where property sets are incomplete.

### The Coordination Export Path

PointSav produces DXF as a coordination output — readable in AutoCAD and every other drafting tool. SVG floor plans are readable in every browser and vector graphics editor. glTF is viewable in Babylon.js, Three.js, Windows 3D Viewer, Blender, and every major 3D application. The archive can produce derivatives for any workflow without compromising the canonical IFC.

### What Changes

The only change for the existing AEC supply chain is that the ISO 19650-required IFC deliverable now goes into a system that actually maintains it. Before PointSav, that IFC file was placed in a Common Data Environment at handover and typically never opened again. The operational team had no tool to work with it. PointSav makes the handover IFC the living operational record.

---

## 9. The Leapfrog Thesis

### Five Structural Gaps the Market Cannot Fill

The following five capabilities are absent from every currently shipping commercial BIM platform. They are absent not through oversight but through structural incompatibility with the subscription cloud model.

**1. Asset-anchored BIM.** No current platform binds a building's digital record to its legal title in a way that makes the record automatically transferable when the asset changes hands. Autodesk Tandem's records disappear when billing lapses. Bentley's iModels require re-authentication to a new tenant. A PointSav PropertyArchive, exported as a Bootable Disk Image, transfers with the deed. The buyer receives the building's complete institutional memory. This maps directly to the tokenised real estate market's unsolved problem: tokenisation captures the transfer of title, but not the transfer of the building's operational record.

**2. Offline-capable BIM.** Basements, rooftops, rural construction sites, air-gapped defence facilities, healthcare campuses with strict data residency requirements, and developing-world connectivity gaps are structurally inaccessible to every cloud-first BIM platform. A Tauri desktop client reading from a local ToteboxOS node operates identically with or without internet connectivity.

**3. Vendor-obsolescence-survivable BIM.** A building lives 50–100 years. A software subscription lives until the vendor changes its pricing model. The PointSav archive, written in IFC-SPF + YAML + SVG + glTF, will be readable in 2076 by tools that do not yet exist, because every format it uses is an ISO standard with a published specification. No hyperscaler can offer this credibly because it undermines subscription renewal.

**4. IoT integration without cloud intermediary.** Current digital-twin architectures funnel sensor data through the vendor's cloud. A PointSav ToteboxOS node ingests BACnet / KNX / MQTT sensor data directly into the archive via a local broker — the data never leaves the owner's premises unless the owner chooses to send it. This matters legally (GDPR data residency, HIPAA, export control) and economically (no per-sensor token charges).

**5. BIM + lease + financial ledger in one portable archive.** A PropertyArchive that holds the building's geometry, its lease register, its financial ledger, and its maintenance history in a single owner-controlled archive is architecturally impossible for any multi-tenant SaaS to offer. Commercial confidentiality, multi-tenant isolation, and financial audit trail requirements all prevent co-mingling these records in a shared cloud. But for a property owner, they are the same asset. The building's value is its lease income stream. The income stream's risk profile is its maintenance history. The maintenance history's physical context is its geometry. These are not four datasets — they are one record about one asset.

### The 2030 Horizon

The convergence of three independent forces by 2030 creates the market that PointSav is architecting toward:

**The tokenisation market.** The tokenised real estate market is projected toward $30 trillion by 2034 (multiple industry forecasts). Every tokenised property currently lacks an operational record. The token represents the title; the building's income history, maintenance condition, and regulatory compliance exist in disconnected silos. A PointSav PropertyArchive, attached to a land title and delivered with the building at sale, is the operational record the tokenisation market is missing.

**The Golden Thread mandate.** The UK Building Safety Act's Golden Thread requirement (in force April 2024) creates a legal obligation for exactly the continuous, transferable, digitally maintained building record that a PropertyArchive delivers. Equivalent legislation is in active development across the EU.

**The seL4 security position.** The seL4 microkernel's formally verified security properties address the one concern that prevents classified, healthcare, and defence clients from adopting cloud BIM: data sovereignty. A building archive running on seL4-hardened ToteboxOS, with air-gapped operation and no cloud dependency, satisfies procurement requirements that exclude every hyperscaler platform by policy.

---

## 10. Bibliography

### Standards and Regulatory Documents

1. buildingSMART International. *IFC 4.3 Formally Approved and Published as an ISO Standard.* buildingsmart.org. April 2024. [https://www.buildingsmart.org/ifc-4-3-formally-approved-and-published-as-an-iso-standard/](https://www.buildingsmart.org/ifc-4-3-formally-approved-and-published-as-an-iso-standard/)

2. ISO. *ISO 16739-1:2024 — Industry Foundation Classes (IFC) for data sharing in the construction and facility management industries.* International Organization for Standardization. 2024.

3. buildingSMART International. *IFC5 Development Repository.* GitHub. [https://github.com/buildingSMART/IFC5-development](https://github.com/buildingSMART/IFC5-development)

4. buildingSMART International. *IDS 1.0 — Information Delivery Specification.* Official standard, 1 June 2024. [https://technical.buildingsmart.org/projects/information-delivery-specification-ids/](https://technical.buildingsmart.org/projects/information-delivery-specification-ids/)

5. EU BIM Task Group. *Position Paper on BIM for Public Procurement.* November 2025. [https://eubim.eu/just-published-position-paper-of-the-eu-bim-task-group-on-bim-for-public-procurement/](https://eubim.eu/just-published-position-paper-of-the-eu-bim-task-group-on-bim-for-public-procurement/)

6. European Commission. *EU Directive 2014/24/EU on Public Procurement.* Official Journal of the European Union. 2014.

7. CEN/TC 442. *Building Information Modelling Standards Portfolio.* Interoperable Europe Portal. [https://interoperable-europe.ec.europa.eu/collection/rolling-plan-ict-standardisation/construction-building-information-modelling](https://interoperable-europe.ec.europa.eu/collection/rolling-plan-ict-standardisation/construction-building-information-modelling)

8. ISO. *ISO 19650 — Information Management Using Building Information Modelling.* International Organization for Standardization. Parts 1–6. 2018–2025.

9. UK Government / HSE. *Keeping Information About a Higher-Risk Building: The Golden Thread.* GOV.UK. September 2024. [https://www.gov.uk/guidance/keeping-information-about-a-higher-risk-building-the-golden-thread](https://www.gov.uk/guidance/keeping-information-about-a-higher-risk-building-the-golden-thread)

10. UK Parliament. *Building Safety Act 2022.* Section 88 — Golden Thread. April 2022. [https://www.legislation.gov.uk/ukpga/2022/30](https://www.legislation.gov.uk/ukpga/2022/30)

11. Building Safety Alliance. *Golden Thread Guidance Documents.* May 2025. [https://buildingsafetyalliance.org.uk/golden-thread-guidance](https://buildingsafetyalliance.org.uk/golden-thread-guidance)

12. Statsbygg. *BIM Manual — SIMBA.* Norwegian Directorate of Public Construction and Property. 2008 (updated). [https://www.statsbygg.no/styringsdokumenter/statsbygg-bim-manual/](https://www.statsbygg.no/styringsdokumenter/statsbygg-bim-manual/)

13. BIMobject. *BIM Mandates 2025: What's Required and Where.* May 2025. [https://business.bimobject.com/blog/bim-mandates-which-countries-will-require-them-in-2025/](https://business.bimobject.com/blog/bim-mandates-which-countries-will-require-them-in-2025/)

14. archBIM.cloud. *BIM Mandate in Public Procurement — Poland 2026.* March 2026. [https://archbim.cloud/en/blog/bim-mandate-public-procurement-poland](https://archbim.cloud/en/blog/bim-mandate-public-procurement-poland)

15. excelize.com. *ISO 19650 BIM Changes Explained: What's Proposed for 2026.* March 2026. [https://excelize.com/blog/iso-19650-bim-changes/](https://excelize.com/blog/iso-19650-bim-changes/)

16. TAAL Tech. *Global BIM Mandates for 2026.* August 2025. [https://www.taaltech.com/global-bim-mandates-for-2026/](https://www.taaltech.com/global-bim-mandates-for-2026/)

### Competitive Landscape

17. Nemetschek SE. *Wikipedia — Corporate History.* [https://en.wikipedia.org/wiki/Nemetschek](https://en.wikipedia.org/wiki/Nemetschek)

18. Graphisoft. *Archicad 29 Launch — 2025 Product Portfolio.* October 2025. [https://www.nemetschek.com/en/news-media/graphisoft-launches-2025-product-portfolio-bold-leap-forward](https://www.nemetschek.com/en/news-media/graphisoft-launches-2025-product-portfolio-bold-leap-forward)

19. Graphisoft. *Announcement: Shift to Subscription Model.* September 2024. [https://www.nemetschek.com/en/news-media/graphisoft-announces-next-phase-its-shift-future-proof-subscription-model](https://www.nemetschek.com/en/news-media/graphisoft-announces-next-phase-its-shift-future-proof-subscription-model)

20. AEC Magazine. *Graphisoft Accelerates Development.* February 2025. [https://aecmag.com/features/graphisoft-accelerates-development/](https://aecmag.com/features/graphisoft-accelerates-development/)

21. Architosh. *Nemetschek Group Acquires HCSS.* April 2026. [https://architosh.com/2026/04/nemetschek-group-acquires-heavy-construction-systems-specialist-llc/](https://architosh.com/2026/04/nemetschek-group-acquires-heavy-construction-systems-specialist-llc/)

22. MarketScreener. *Graphisoft Acquires Distributors in Australia and New Zealand.* February 2026. [https://www.marketscreener.com/news/nemetschek-graphisoft-acquires-distributors-in-australia-and-new-zealand](https://www.marketscreener.com/news/nemetschek-graphisoft-acquires-distributors-in-australia-and-new-zealand)

23. Autodesk. *APS Token Estimator Tool.* Autodesk Platform Services. [https://aps.autodesk.com/blog/introducing-new-token-estimator-tool-aps](https://aps.autodesk.com/blog/introducing-new-token-estimator-tool-aps)

24. Autodesk. *API Pricing Changes and Subscription Pilot.* 2025–2026. [https://aps.autodesk.com/api-pricing-changes-and-subscription-pilot](https://aps.autodesk.com/api-pricing-changes-and-subscription-pilot)

25. AEC Magazine. *The Open Letter to Autodesk: Two Years On.* [https://aecmag.com/bim/the-open-letter-two-years-on/](https://aecmag.com/bim/the-open-letter-two-years-on/)

26. AEC Magazine. *Autodesk Shows Its AI Hand.* [https://aecmag.com/features/autodesk-shows-its-ai-hand/](https://aecmag.com/features/autodesk-shows-its-ai-hand/)

27. Nemetschek. *OpenBIM Position.* [https://www.nemetschek.com/en/topics/open-bim](https://www.nemetschek.com/en/topics/open-bim)

28. Solibri. *Solibri Anywhere (Legacy) Deprecation.*  [https://www.solibri.com/products/solibri-anywhere](https://www.solibri.com/products/solibri-anywhere)

29. Bentley Systems. *iTwin Service Documentation.* [https://www.itwinjs.org/v2/learning/clients/itwinservice/](https://www.itwinjs.org/v2/learning/clients/itwinservice/)

### Open Source Toolchain

30. IfcOpenShell. *The Open Source IFC Toolkit and Geometry Engine.* [https://ifcopenshell.org/](https://ifcopenshell.org/)

31. IfcOpenShell. *GitHub Repository.* [https://github.com/IfcOpenShell/IfcOpenShell](https://github.com/IfcOpenShell/IfcOpenShell)

32. ThatOpen Company. *web-ifc Documentation.* [https://thatopen.github.io/engine_web-ifc/docs/](https://thatopen.github.io/engine_web-ifc/docs/)

33. xeokit. *xeokit-sdk GitHub Repository.* [https://github.com/xeokit/xeokit-sdk](https://github.com/xeokit/xeokit-sdk)

34. Speckle Systems. *GitHub Organisation.* [https://github.com/specklesystems](https://github.com/specklesystems)

35. Khronos Group. *glTF — Runtime 3D Asset Delivery.* [https://www.khronos.org/gltf/](https://www.khronos.org/gltf/)

36. crates.io. *ifc_rs — Rust IFC Parser.* [https://crates.io/crates/ifc_rs](https://crates.io/crates/ifc_rs)

37. crates.io. *gltf — Rust glTF crate.* [https://docs.rs/gltf](https://docs.rs/gltf)

38. crates.io. *resvg — SVG rendering.* [https://crates.io/crates/resvg](https://crates.io/crates/resvg)

### Digital Twin and IoT-BIM Research

39. Chung, J. & Shelden, D. *A Framework of ifcJSON-Based Digital Twin Platform for Monitoring Building Environment Using BIM, IoT, and Semantic Web Technologies.* Proceedings of ICCCBE 2024 — Volume 1. Springer, 2025. [https://impact.ornl.gov/en/publications/a-framework-of-ifcjson-based-digital-twin-platform-for-monitoring/](https://impact.ornl.gov/en/publications/a-framework-of-ifcjson-based-digital-twin-platform-for-monitoring/)

40. Center for Architecture Science and Ecology, Rensselaer. *BIM and IoT-based Digital Twin Dashboard.* January 2026. [https://www.case.rpi.edu/researchprojects/digital-twin-dashboard](https://www.case.rpi.edu/researchprojects/digital-twin-dashboard)

41. Tandfonline. *Development and Demonstration of a Digital Twin Platform Leveraging Ontologies and Data-Driven Simulation Models.* Published online 14 May 2025. DOI: 10.1080/19401493.2025.2504005

42. AlterSquare / Medium. *IoT Meets BIM: Practical First Steps to a Maintainable Digital-Twin Stack.* July 2025. [https://altersquare.medium.com/iot-meets-bim-practical-first-steps-to-a-maintainable-digital-twin-stack-f438cc5b0a8a](https://altersquare.medium.com/iot-meets-bim-practical-first-steps-to-a-maintainable-digital-twin-stack-f438cc5b0a8a)

43. ScienceDirect. *Developing an Automatic Integration Approach to Generate Brick Model from Imperfect Building Information Modelling.* 2024. DOI: 10.1016/j.jobe.2024.022654

44. arxiv.org. *A Scalable and Interoperable Platform for Transforming Building Information into Brick Ontology.* 2025. [https://arxiv.org/pdf/2509.16259](https://arxiv.org/pdf/2509.16259)

45. MDPI Buildings. *Digital Twin-Enabled BIM-IoT Framework for Optimizing Indoor Thermal Comfort Using Machine Learning.* Buildings 2025, 15(10), 1584. DOI: 10.3390/buildings15101584

46. CDBB. *The Gemini Principles.* Centre for Digital Built Britain. 2018.

47. TU Delft. *3DBAG — CityJSONSeq Dataset of Dutch Building Stock.* [https://3dbag.nl/](https://3dbag.nl/)

48. brickschema.org. *Brick Schema 1.3.* [https://brickschema.org/](https://brickschema.org/)

49. ETSI. *SAREF — Smart Applications REFerence Ontology.* ETSI TS 103 264.

50. ICE. *The Golden Thread Running Through The New Building Safety Act.* January 2024. [https://www.ice.org.uk/news-views-insights/inside-infrastructure/golden-thread-through-new-building-safety-regime](https://www.ice.org.uk/news-views-insights/inside-infrastructure/golden-thread-through-new-building-safety-regime)

---

*This document is maintained in `content-wiki-documentation/research/` and published via `media-knowledge-documentation`. It is the founding research document for the PointSav BIM product family.*

*BCSC Disclosure: References to the Sovereign Data Foundation describe intended future roles. No current equity holding or active governance role should be inferred.*

*Last updated: April 2026. Document version: 1.0.*
