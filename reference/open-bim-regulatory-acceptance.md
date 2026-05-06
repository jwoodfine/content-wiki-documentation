---
schema: foundry-doc-v1
title: "Open BIM and Regulatory Acceptance"
slug: open-bim-regulatory-acceptance
category: reference
type: topic
quality: core
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-06
editor: pointsav-engineering
cites: [eupl-1-2]
paired_with: open-bim-regulatory-acceptance.es.md
---

Building Information Modelling is no longer elective in public procurement for most G7 economies. The United States federal government has required IFC-formatted BIM deliverables for major infrastructure and building projects since 2007. The European Union has embedded BIM requirements into public procurement directives enforced across member states. The United Kingdom, Singapore, Norway, Denmark, the Netherlands, and Australia have each issued national mandates or equivalent policy requirements. The regulatory landscape for Open BIM is settled: IFC-capable workflows are now a baseline procurement requirement. The open question is which platforms can meet the sovereign data requirements attached to these mandates.

## Defining Open BIM

Open BIM, as defined by buildingSMART International, denotes a workflow and data exchange approach where:

1. Model data is stored and exchanged in vendor-neutral open formats, principally IFC (ISO 16739-1:2024).
2. Classification and property definitions reference open dictionaries, principally bSDD.
3. Constraint specifications are expressed in open constraint languages, principally IDS 1.0.
4. Handover data is formatted to open facility management standards, principally COBie.

Open BIM is distinguished from closed BIM (proprietary format workflows within a single vendor's tool ecosystem) and from federated BIM (multi-model coordination that may use proprietary formats for individual discipline models). The Open BIM distinction matters for public procurement because most public tender requirements specify IFC delivery in a vendor-neutral format.

## United States Federal Mandates

The US federal government is the largest single construction client in the world by value. Three agencies with the largest capital construction programmes have published BIM requirements that effectively mandate IFC-capable workflows.

**General Services Administration (GSA).** The GSA National 3D-4D-BIM Program, launched in 2003 and formalised in the GSA BIM Guide Series from 2007, requires IFC-formatted spatial and programme data for projects above defined thresholds. Facility owners using proprietary BIM authoring tools are required to deliver IFC exports in vendor-neutral format. COBie deliverables are required for handover.

**US Army Corps of Engineers (USACE).** The USACE BIM Roadmap (2012, updated 2015) mandates BIM for military construction (MILCON) projects, research facilities, and civil works above $5M. IFC-compatible deliverables are required at design milestones. USACE facility data standards reference COBie and IFC Property Sets.

**Department of Veterans Affairs (VA) and Naval Facilities Engineering Systems Command (NAVFAC).** Both agencies have published BIM standards that require IFC exports at design milestones and COBie handover packages for new construction and major renovations.

**Federal Acquisition Regulation compatibility.** EUPL-1.2 (the licence under which the PointSav BIM platform is published) is recognised as an OSI-approved open source licence. The FAR Part 27 (Patents, Data, and Copyrights) provisions for open source software do not prohibit EUPL-1.2 licensed software in federal contracts.

## European Union

The EU 2014 Public Procurement Directive (Directive 2014/24/EU) explicitly permits member states to require electronic BIM tools for publicly funded construction and civil engineering contracts. Article 22(4) reads: "For public works contracts and design contests, Member States may require the use of specific electronic tools, such as of building information electronic modelling tools or similar."

Individual member states have implemented this in varying degrees of stringency.

**Germany.** The Federal Ministry for Digital and Transport (BMDV) issued a BIM roadmap mandating BIM on infrastructure projects, with full Open BIM targets for federal transport infrastructure projects at 2020 (design phase) and 2025 (full lifecycle).

**Italy.** Legislative Decree 36/2023 (the new Public Contracts Code) mandates BIM for public works contracts above €15 million from January 2023, extending to lower thresholds through 2025. IFC-compatible deliverables are required.

**Spain.** The Plan de Impulso de la Contratación Pública de Edificación BIM (PPRE 2022–2026) establishes a progressive mandate for BIM on public construction contracts, targeting full implementation across all public works by 2026. IFC is the specified exchange format.

**Denmark.** Denmark has required BIM on state-funded building projects above DKK 5 million since 2013. Denmark is among the earliest national mandates in Europe.

**Norway.** Statsbygg (the Norwegian government's main property manager) has required Open BIM deliverables since 2016. The Statsbygg BIM Manual specifies IFC 4.x and LOD requirements by project phase.

**Netherlands.** Rijkswaterstaat (national infrastructure) and ProRail (rail infrastructure) both operate BIM requirements programmes specifying IFC deliverables and COBie handover data for major infrastructure projects.

**Poland.** The Polish Government enacted BIM requirements for major public works in 2021 under the Public Procurement Law.

**United Kingdom (post-EU).** The UK Government's BIM mandate for Level 2 BIM on centrally procured public sector projects has been in effect since 2016, issued under the Government Construction Strategy. BS EN ISO 19650 (the international standard for information management using BIM) was adopted as the UK national standard in 2019.

## buildingSMART Certification

buildingSMART International operates a software certification programme for IFC import/export implementations. Software achieving buildingSMART certification has been verified to produce conformant IFC files that round-trip through certified importers without data loss. This certification is recognised in procurement requirements across multiple jurisdictions as evidence of Open BIM compliance.

The PointSav BIM platform is intended to achieve buildingSMART certification for its IFC export and import implementations. The IFC 4.3 Reference View and the Design Transfer View are the target certifications for authoring tools; the BIM Token platform targets certification against the Property Set exchange specification. A certification timeline will be announced when the buildingSMART certification service accepts submissions for the applicable view types.

## Sovereign Data Architecture as a Procurement Requirement

Several public procurement contexts impose data sovereignty requirements that effectively mandate offline-capable, self-hosted BIM platforms. Three regulatory frameworks drive this.

**ITAR (International Traffic in Arms Regulations).** US federal and allied defence construction projects involving classified facility data may be subject to ITAR and EAR (Export Administration Regulations). BIM models for defence facilities may contain ITAR-controlled spatial and structural data. An offline-first, self-hosted platform that never transmits model data outside the facility network satisfies ITAR requirements without commercial cloud authorisation. (Legal review is required before asserting ITAR compliance for a specific facility type.)

**GDPR (General Data Protection Regulation).** Building occupancy data, sensor data, and facility management records associated with BIM digital twins may contain personal data. GDPR Article 44 prohibits transfer of personal data to jurisdictions without adequate protection unless specific safeguard mechanisms are in place. A self-hosted BIM platform that processes data within EU jurisdiction eliminates the transfer question.

**HIPAA (Health Insurance Portability and Accountability Act).** Healthcare facility construction and operation generates BIM data associated with patient flow, clinical space programming, and medical equipment layout. Where this data can be linked to identifiable patient populations, HIPAA's physical safeguard requirements may apply. A self-hosted platform with access controls aligned to the facility's security posture satisfies these requirements without relying on commercial cloud business associate agreements.

The PointSav BIM platform is designed for offline-first operation. The BIM token vault is a git repository. The application server is a self-hosted binary. No telemetry is transmitted. No model data leaves the operating environment unless explicitly exported by an authorised user.

## ISO 19650 and the Common Data Environment

ISO 19650 (Information management using building information modelling) defines the requirements for information management processes across the project lifecycle and for the Common Data Environment (CDE) — the shared data infrastructure through which project information is exchanged.

ISO 19650 Part 1 (Concepts) and Part 2 (Delivery phase) are technology-neutral. A git repository satisfies the ISO 19650 CDE requirements:

- **Information containers**: git objects identified by content-addressed SHA-256 hashes.
- **Issue and receive workflow**: pull request and review workflow.
- **Revision-controlled audit trail**: git commit history with author, timestamp, and content hash is tamper-evident.
- **Status management**: git branch naming conventions and tag annotations.

This equivalence means that a BIM project managed through a git-hosted token vault and model repository is operating within an ISO 19650-compliant CDE, without requiring a purpose-built CDE platform. This is a structural cost advantage for small and medium-sized AEC firms.

## EUPL-1.2 Licence and Procurement Advantage

The PointSav BIM platform is published under the European Union Public Licence version 1.2 (EUPL-1.2). This licence has three properties relevant to public procurement.

**OSI-approved.** EUPL-1.2 is listed on the OSI Open Source Initiative list of approved licences. Procurement requirements referencing "OSI-approved open source" are satisfied by EUPL-1.2.

**FAR-compatible.** FAR Part 27 analysis identifies no general prohibition on EUPL-1.2 licensed software in federal contracting. EUPL-1.2's compatibility list includes GPL-2.0, GPL-3.0, AGPL-3.0, and EUPL-1.1 — enabling combination with GPL-family code without additional compliance work.

**EU public body alignment.** EUPL-1.2 was authored by the European Commission for software produced by or for EU public bodies. Contracting authorities in EU member states have a policy preference for EUPL-1.2 licensed software under the Commission's EUPL guidance.

## See Also

- [[flat-file-bim-leapfrog]]
- [[city-code-as-composable-geometry]]
- [[bim-token-what-it-is]]
- [[bcsc-disclosure-posture]]
- [[leapfrog-2030-architecture]]

## References

- IFC 4.3 (ISO 16739-1:2024) — buildingSMART International
- ISO 19650 Parts 1 and 2 — ISO
- COBie (Construction Operations Building Information Exchange) v3 — buildingSMART
- IDS 1.0 (Information Delivery Specification) — buildingSMART International
- EUPL v1.2 — European Commission
- EU Directive 2014/24/EU — European Parliament and Council
- ITAR / EAR — US Department of State / Commerce
- GDPR 2016/679 — European Parliament and Council

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*

*Woodfine Capital Projects™, Woodfine Management Corp™, PointSav Digital Systems™, Totebox Orchestration™, and Totebox Archive™ are trademarks of Woodfine Capital Projects Inc., used in Canada, the United States, Latin America, and Europe. All other trademarks are the property of their respective owners.*
