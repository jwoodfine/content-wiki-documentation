---
schema: foundry-doc-v1
title: "Open BIM and regulatory acceptance"
slug: open-bim-regulatory-acceptance
short_description: "Building Information Modelling is mandated across most G7 economies for public procurement, with open standards — IFC 4.3, IDS 1.0, COBie — as the delivery requirement rather than proprietary formats. Offline-first, self-hosted BIM platforms are the only architecture type that natively satisfies sovereign data requirements imposed by ITAR, GDPR, HIPAA, and equivalent regulatory frameworks."
category: architecture
type: topic
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-17
editor: pointsav-engineering
cites: [ifc-4-3, iso-19650, ids-1-0]
paired_with: open-bim-regulatory-acceptance.es.md
---

Building Information Modelling is no longer elective in public procurement for most G7 economies. The United States federal government has required IFC-formatted BIM deliverables for major infrastructure and building projects since 2007. The European Union has embedded BIM requirements into public procurement directives enforced across member states. The United Kingdom, Singapore, Norway, Denmark, the Netherlands, and Australia have each issued national mandates or equivalent policy requirements. The regulatory landscape for Open BIM is settled. The open question is which platforms can meet the sovereign data requirements attached to these mandates.

## Defining Open BIM

Open BIM, as defined by buildingSMART International, denotes a workflow and data exchange approach where:

1. Model data is stored and exchanged in vendor-neutral open formats, principally IFC (ISO 16739-1:2024).
2. Classification and property definitions reference open dictionaries, principally bSDD.
3. Constraint specifications are expressed in open constraint languages, principally IDS 1.0.
4. Handover data is formatted to open facility management standards, principally COBie.

Open BIM is distinguished from closed BIM (proprietary format workflows within a single vendor's tool ecosystem) and from federated BIM (multi-model coordination that may use proprietary formats for individual discipline models). Most public tender requirements specify IFC delivery — not any proprietary authoring format.

## United States Federal Mandates

The US federal government is the largest single construction client in the world by value. Three agencies with the largest capital construction programmes have published BIM requirements that effectively mandate IFC-capable workflows.

**General Services Administration (GSA).** The GSA National 3D-4D-BIM Program, launched in 2003 and formalised in the GSA BIM Guide Series from 2007, requires IFC-formatted spatial and programme data for projects above defined thresholds. Facility owners using any authoring tool are required to deliver IFC exports. COBie deliverables are required for handover.

**US Army Corps of Engineers (USACE).** The USACE BIM Roadmap mandates BIM for military construction (MILCON) projects, research facilities, and civil works above $5M. IFC-compatible deliverables are required at design milestones.

**Department of Veterans Affairs (VA) and Naval Facilities Engineering Systems Command (NAVFAC).** Both agencies have published BIM standards that require IFC exports at design milestones and COBie handover packages for new construction and major renovations.

**Federal Acquisition Regulation compatibility.** Apache 2.0 (the licence under which the BIM Object data files are published) is an OSI-approved open source licence. FAR Part 27 provisions for open source software do not prohibit Apache 2.0 licensed data in federal contracts, and the permissive terms create no copyleft complications in government contracting.

## European Union

The EU 2014 Public Procurement Directive (Directive 2014/24/EU) explicitly permits member states to require electronic BIM tools for publicly funded construction and civil engineering contracts. Individual member states have implemented this in varying degrees of stringency.

**Germany.** The Federal Ministry for Digital and Transport (BMDV) issued a BIM roadmap mandating BIM on infrastructure projects, with targets for federal transport infrastructure projects set for 2020 (design phase) and 2025 (full lifecycle).

**Italy.** Legislative Decree 36/2023 (the new Public Contracts Code) mandates BIM for public works contracts above €15 million from January 2023, extending to lower thresholds through 2025.

**Spain.** The Plan de Impulso de la Contratación Pública de Edificación BIM (PPRE 2022-2026) establishes a progressive mandate targeting full implementation across all public works by 2026.

**Denmark.** Denmark has required BIM on state-funded building projects above DKK 5 million since 2013.

**Norway.** Statsbygg (the Norwegian government's main property manager) has required Open BIM deliverables since 2016. The Statsbygg BIM Manual specifies IFC 4.x and LOD requirements by project phase.

**Netherlands.** Rijkswaterstaat and ProRail both operate BIM requirements programmes specifying IFC deliverables and COBie handover data for major infrastructure projects.

**United Kingdom (post-EU).** The UK Government's BIM mandate for Level 2 BIM on centrally procured public sector projects has been in effect since 2016. BS EN ISO 19650 was adopted as the UK national standard in 2019.

## buildingSMART Certification

buildingSMART International operates a software certification programme for IFC import/export implementations. The PointSav BIM platform is intended to achieve buildingSMART certification for its IFC export and import implementations. The IFC 4.3 Reference View and the Design Transfer View are the two target certifications for authoring tools; the BIM Object platform targets certification against the Property Set exchange specification.

## Sovereign Data Architecture as a Procurement Requirement

Several public procurement contexts impose data sovereignty requirements that effectively mandate offline-capable, self-hosted BIM platforms.

**ITAR (International Traffic in Arms Regulations).** US federal and allied defence construction projects involving sensitive facility data are subject to ITAR and EAR. ITAR-controlled data cannot be processed on commercial cloud infrastructure unless that infrastructure holds a FedRAMP High authorisation or equivalent. An offline-first, self-hosted platform that never transmits model data outside the facility network is the only architecture that satisfies ITAR requirements without commercial cloud authorisation.

**GDPR (General Data Protection Regulation).** Building occupancy data, sensor data, and facility management records associated with BIM digital twins may contain personal data. GDPR Article 44 prohibits transfer of personal data to jurisdictions without adequate protection. A self-hosted BIM platform that processes data within EU jurisdiction eliminates the transfer question.

**HIPAA (Health Insurance Portability and Accountability Act).** Healthcare facility construction generates BIM data associated with patient flow and clinical space programming. A self-hosted platform with access controls aligned to the facility's security posture satisfies these requirements without relying on commercial cloud business associate agreements.

## ISO 19650 and the Common Data Environment

ISO 19650 defines requirements for information management and for the Common Data Environment (CDE). The standard is technology-neutral: it specifies what the CDE must do but does not prescribe the technology.

A git repository satisfies the ISO 19650 CDE requirements:

| ISO 19650 concept | Git implementation |
|---|---|
| Information container | IFC file or YAML sidecar |
| Container UID | Git object hash or IFC GUID |
| Status | Branch name (`work-in-progress`, `shared`, `published`) |
| Revision | Git commit hash |
| Classification | Directory path + YAML header |
| Change history | `git log --follow <filename>` |
| CDE workflow states | Git branch merge / pull-request workflow |

A BIM project managed through a git-hosted object vault and model repository operates within an ISO 19650-compliant CDE, without requiring a purpose-built platform.

## Apache 2.0 Licence and Procurement Advantage

The BIM Object data files are published under Apache 2.0. This licence has three properties relevant to public procurement.

**OSI-approved.** Apache 2.0 is on the OSI Open Source Initiative list of approved licences.

**FAR-compatible.** Apache 2.0's permissive terms create no copyleft complications in federal contracting, and the patent grant clause provides additional protection for government use.

**Broad compatibility.** Apache 2.0 is compatible with GPL-3.0, LGPL, MIT, and EUPL-1.2 — enabling combination with components under a range of open source licences without additional compliance analysis.

## Open Questions

**buildingSMART certification timeline.** The IFC 4.3 certification service was not accepting submissions for all view types as of the research date. The certification timeline for the PointSav BIM platform is not fixed. This affects how the platform can be represented in procurement responses requiring certified IFC compliance.

**ITAR facility mapping.** The list of specific facility types where ITAR restrictions apply to BIM data is not publicly enumerated by the US Government. Legal review is required before representing the platform as certified for ITAR-restricted construction. The offline-first architecture is a technical fact that can be stated; any ITAR compliance claim requires counsel review.
