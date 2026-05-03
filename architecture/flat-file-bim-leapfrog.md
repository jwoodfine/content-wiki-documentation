---
schema: foundry-doc-v1
type: topic
slug: flat-file-bim-leapfrog
title: The Flat-File BIM Leapfrog
audience: vendor-public
bcsc_class: vendor-public
language: en
paired_with: flat-file-bim-leapfrog.es.md
---

# The Flat-File BIM Leapfrog

PointSav’s Building Design System achieves a structural competitive advantage by adopting five architectural constraints that are individually simple but collectively occupy a market category hyperscalers cannot enter without cannibalizing their own revenue models. By prioritizing flat-file storage, open standards, a Rust-based offline-first architecture, and the EUPL license, Foundry delivers a BIM substrate that is inherently owned by the asset holder rather than rented from a cloud vendor.

## Structural Constraints as Competitive Moat

The strategy is predicated on five foundational architectural decisions:

1.  **Flat-File Storage:** All building data resides in human-readable, plain-text files.
2.  **Open Standards:** Strict adherence to ISO-standardized IFC, IDS, and BCF.
3.  **Rust + Tauri:** A high-performance, memory-safe execution environment.
4.  **Offline-First:** Full functionality without mandatory internet connectivity.
5.  **EUPL-Licensed:** Open-source legal protection that is procurement-friendly for governments.

## Production Maturity of the Open BIM Stack

As of 2024, the open BIM standards stack has reached sufficient maturity for commercial-grade infrastructure. IFC 4.3 (ISO 16739-1:2024) extends the schema from buildings to civil infrastructure, including bridges, rail, and waterways. The canonical serialization (IFC-SPF) remains a plain-text format (ISO 10303-21) that is readable in any standard text editor.

Foundry canonicalizes on IFC-SPF today, with intended opportunistic mirroring to ifcJSON. While IFC 5/IFCX is in development, the PointSav architecture is designed such that future migration is intended to be a serialization swap rather than a core rewrite.

## Flat-File Definition and Taxonomy

"Flat-file BIM" refers to a directory of plain-text and standardized binary files accessible without proprietary SDKs.

| Format | Standard | Role |
| :--- | :--- | :--- |
| **IFC-SPF (.ifc)** | ISO 16739-1:2024 | Authoritative geometry + semantics |
| **IDS 1.0** | buildingSMART (2024) | Validation contract |
| **BCF 3.0** | buildingSMART | Collaboration history |
| **Per-element YAML** | Local Convention | Sensor and work-order metadata |
| **glTF 2.0** | ISO/IEC 12113:2022 | Visualization cache |

The `.ifc` file serves as the authoritative spatial state, while YAML sidecars handle dynamic data such as sensor readings and lease references.

## Five Differentiated Capabilities

### 1. Asset-Anchored BIM
The digital twin travels with the property deed. Unlike multi-tenant SaaS models where data is "rented," a flat-file twin is owned like the physical building—permanently and transferably.

### 2. Offline-Capable Field Operations
By construction, cloud-authoritative twins are unusable in air-gapped facilities, basements, or remote construction sites. Foundry preserves full BIM functionality without network dependency.

### 3. Vendor-Obsolescence Survival
Buildings have a 50-year lifespan; proprietary formats often last fewer than five. A flat-file substrate ensures data remains readable for decades after the software vendor disappears.

### 4. Direct IoT Integration
Per-element YAML sidecars ingest sensor data via local MQTT brokers. This eliminates sensor-count-based token charges and satisfies strict data residency requirements (GDPR, HIPAA).

### 5. Unified Asset Archive
The building, lease, and ledger converge into a single portable archive. The Totebox Archive is the first architecture where a building’s legal, financial, and spatial identity are a single, portable artifact.

## Regulatory and Security Alignment

The architecture satisfies mandatory open-standard requirements for US federal agencies (GSA, VA), EU member states, and Singapore’s CORENET X. It is uniquely positioned to meet ITAR air-gapped requirements and EU Data Act sovereignty mandates.

## Strategic Trade-offs

PointSav acknowledges that real-time multi-user design workshops are currently faster in synchronous cloud SaaS. Additionally, while the substrate is designed to be AI-ready, a generative BIM authoring tool is not planned for the v0.0.1 release. These are deliberate trade-offs to prioritize an offline-first, vendor-independent posture.


---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*

*Woodfine Capital Projects™, Woodfine Management Corp™, PointSav Digital Systems™, Totebox Orchestration™, and Totebox Archive™ are trademarks of Woodfine Capital Projects Inc., used in Canada, the United States, Latin America, and Europe. All other trademarks are the property of their respective owners.*
