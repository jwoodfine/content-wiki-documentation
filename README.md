<div align="center">

# PointSav — Technical Documentation Wiki
### *The Engineering Library for the PointSav Platform*

[![Status: Active](https://img.shields.io/badge/Status-Active-22863a.svg?style=flat-square)](#)
[![Role: Documentation](https://img.shields.io/badge/Role-Technical_Library-0075ca.svg?style=flat-square)](#)

<br/>

**[→ Engineering Monorepo](https://github.com/pointsav/pointsav-monorepo)** &nbsp;·&nbsp; **[→ Design System](https://github.com/pointsav/pointsav-design-system)** &nbsp;·&nbsp; **[→ Live Deployment](https://github.com/woodfine/woodfine-fleet-deployment)** &nbsp;·&nbsp; **[→ pointsav.com](https://pointsav.com)**

</div>

---

## About This Repository

This is the technical library for the PointSav platform. It contains Architecture Decision Records, service specifications, operational guides, and the platform glossary. Where the engineering monorepo contains the code, this repository contains the reasoning behind it.

The intended reader is anyone who needs to understand not just what the platform does, but why specific architectural choices were made — auditors, incoming contributors, institutional partners, and technical due diligence reviewers.

---

## Architecture Decision Records

ADRs are formal commitments to specific design choices. They are not proposals — they represent decisions already made, implemented, and binding on all future development.

**Compliance and Data Architecture**

`SYS-ADR-06.yaml` — Why the compliance archive and the intelligence layer are two physically separate systems, and why querying one for the other's purpose produces incorrect results.

`SYS-ADR-07.yaml` — Why structured data (CSV, JSON, spreadsheets) is forbidden from routing through AI processing, and why all inbound compound files must be vaulted before any extraction logic is applied.

`SYS-ADR-10.yaml` — Why F12 is the mandatory human checkpoint for all base asset ingestion and why there is no batch import path that bypasses it.

**Security Architecture**

`SYS-ADR-08.yaml` — Why systemd is classified as a quarantined foreign component and what constraints govern its temporary use on Debian cloud relays.

`SYS-ADR-13.yaml` — Why the master routing node and its cryptographic keys reside on physical hardware the executive controls, rather than on cloud infrastructure.

`SYS-ADR-16.yaml` — Why WireGuard's layer-3 topology requires application-level unicast for fleet commands and why UDP broadcast is prohibited.

**User Interface Architecture**

`SYS-ADR-11.yaml` — Why ConsoleOS is split into a stateless Chassis and isolated Cartridges, and why each F-key function is a separately deployable unit.

`SYS-ADR-14.yaml` — Why static UI requests and API calls route through separate ports (8888 and 8080) at the NGINX layer.

`SYS-ADR-15.yaml` — Why two-layer cache destruction is enforced on every outbound UI payload.

`SYS-ADR-17.yaml` — The Derivative Architecture: Base Assets, First Derivative, and Third Derivative — and why these three layers must never be conflated.

`SYS-ADR-18.yaml` — Why ConsoleOS is a routing terminal, not a web application, and what this means for how outputs reach the operator.

`SYS-ADR-19.yaml` — Why automated AI publishing to verified ledgers is prohibited, and the Verification Airgap (Git for Knowledge) model that enforces this.

---

## Service Specifications

**The Data Pipeline**

`topic-service-email.md` — How the mail service pulls from Microsoft 365, why it applies zero intelligence to content, and what the hard cap of 3 emails per folder per cycle protects against.

`topic-service-extraction.md` — How the deterministic parser routes structured versus unstructured payloads, why the raw file is always vaulted before extraction begins, and how transaction IDs maintain chain of custody.

`topic-service-slm.md` — How the AI Gateway operates in two simultaneous roles: local point-in-time execution and the doorman protocol that prevents corporate records from reaching external AI models. The three operator paths — no AI, DIY via doorman, packaged product.

`topic-service-people.md` — How the personnel ledger operates as a flat-file state machine, the Verification Surveyor workflow, and the daily verification limit design rationale.

`topic-service-content.md` — How the knowledge index self-heals, the four control valves that govern taxonomy update rates, and why slow update rates are a feature rather than a limitation.

`topic-service-search.md` — How the Tantivy-based inverted index provides air-gappable full-text search without a running database engine, and what DARP compliance requires.

`topic-service-egress.md` — How Cold Storage Entanglement works, the cryptographic chunking mechanism, and how physical drives are mathematically locked to specific archives.

**Infrastructure and Security**

`topic-service-fs.md` — How the immutable ledger enforces WORM compliance at the filesystem level and why even an administrator cannot delete records.

`topic-ppn-topology.md` — The PointSav Private Network architecture, WireGuard mesh design, and the Command Authority model.

`TOPIC-TELEMETRY-ARCHITECTURE.md` — The four-tier telemetry routing model, zero-cookie pipeline design, and the pull diode pattern.

---

## Operational Guides

`topic-zero-touch-launch.md` — The four-phase Zero-Touch Launch Cycle: One-Click Launch, TUI Administrator, Cold Storage Entanglement, and Stateful Extraction (The Transferable Ledger).

`topic-verification-surveyor.md` — The human-in-the-loop identity verification workflow, the air-gap rationale, and the daily throttle design.

`topic-crypto-attestation.md` — Client-side SHA-256 payload attestation for public-facing disclosures, browser-native implementation, and the institutional audit use case.

`topic-sovereign-ai-routing.md` — The external AI routing model: payload sanitisation, anonymised structural skeleton, local re-hydration, and why the external model never holds actual corporate records.

---

## Glossaries

Three machine-readable glossaries support the platform's bilingual (English/Spanish) institutional voice:

| Glossary | Contents |
|:---|:---|
| `glossary-corporate.csv` | Financial and investment terminology — Direct-Hold Solutions, LP structures, four-jurisdiction entity names, BCSC compliance terms |
| `glossary-projects.csv` | Real estate and physical architecture — building typologies, co-location strategy, sustainability certifications, national tenant categories |
| `glossary-documentation.csv` | Platform and technology — all OS types, services, deployment prefixes, ConsoleOS variants |

---

## Contributing

This wiki is maintained by PointSav Digital Systems contributors. All additions must reference an ADR, service specification, or glossary entry. Content that cannot be traced to the platform architecture does not belong here.

**[→ github.com/pointsav](https://github.com/pointsav)** &nbsp;·&nbsp; **[→ open.source@pointsav.com](mailto:open.source@pointsav.com)**

---

*© 2026 PointSav Digital Systems™. All rights reserved.*

*→ Versión en español: [README.es.md](./README.es.md)*

<!-- BEGIN: factory-release-engineering license-section -->
<!-- ================================================================== -->
<!-- This section is generated from factory-release-engineering.         -->
<!-- Do not edit here. Propose changes upstream.                          -->
<!-- ================================================================== -->

## License

This repository is licensed under the **CC-BY-4.0**. See the
`LICENSE` file in the root of this repository for the full legal text,
which is authoritative.



Copyright (c) 2026 Woodfine Capital Projects Inc.. All rights not expressly
granted by the license are reserved.

<!-- ================================================================== -->
<!-- Esta sección se genera desde factory-release-engineering.           -->
<!-- No editar aquí. Proponga cambios río arriba.                         -->
<!-- ================================================================== -->

## Licencia

Este repositorio se distribuye bajo la **CC-BY-4.0**. Véase el
archivo `LICENSE` en la raíz del repositorio para consultar el texto
legal completo, el cual es la versión autoritativa.



Copyright (c) 2026 Woodfine Capital Projects Inc.. Se reservan todos los
derechos no concedidos expresamente por la licencia.
<!-- END: factory-release-engineering license-section -->
