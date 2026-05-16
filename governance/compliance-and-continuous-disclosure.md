---
schema: foundry-doc-v1
title: "compliance-and-continuous-disclosure"
slug: compliance-and-continuous-disclosure
category: governance
type: concept
quality: complete
short_description: "Compliance and continuous disclosure describes the regulatory frameworks the PointSav architecture addresses and the structural approach it takes to expose audit evidence continuously rather than through annual point-in-time certification cycles."
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-15
editor: pointsav-engineering
paired_with: compliance-and-continuous-disclosure.es.md
cites:
 - ni-51-102
 - osc-sn-51-721
references:
 - id: 1
 text: "NIST, Open Security Controls Assessment Language (OSCAL) — machine-readable formats for representing security control catalogs, baselines, system security plans, and assessment results."
 url: "https://pages.nist.gov/OSCAL/"
 - id: 2
 text: "International Organization for Standardization, ISO/IEC 42001:2023 — Artificial Intelligence Management System (AIMS): requirements for organisations managing AI systems responsibly."
 url: "https://www.iso.org/standard/81230.html"
---

Compliance and continuous disclosure describes the regulatory frameworks the PointSav architecture addresses and the structural approach it takes to evidence those controls. Conventional enterprise compliance relies on annual point-in-time audits: an auditor examines a sample, produces a written report, and the customer holds a certificate that may be stale within weeks of issue. The PointSav substrate is designed for a continuous model: machine-readable controls that update in real time and expose a queryable attestation surface. All compliance certifications and framework targets described here are planned or intended; forward-looking language applies throughout per Canadian securities continuous-disclosure requirements [ni-51-102] [osc-sn-51-721]. By the end of this article, a reader will understand the compliance framework targets, the structural controls approach, and the document-state discipline the architecture enforces.

## How continuous-proof replaces annual audit cycles

The limitation of point-in-time auditing is architectural: a certificate issued after a six-month assessment window is accurate for that window and potentially inaccurate at every subsequent moment. For customers managing regulated records — Reporting Issuers, medical practitioners, legal professionals — the gap between assessment and current posture is a liability.

The PointSav substrate approaches this by placing controls at a level where they cannot be administratively bypassed: if a control can be turned off by an administrator, it is a policy. If it cannot be turned off, it is an architectural guarantee. The intended approach moves controls from the policy layer to the system tier — below the operating system — so that the audit trail is not a feature that was enabled but a structural property that was never absent. [^1]

## Compliance frameworks the architecture addresses

| Framework | Type | What the architecture provides |
|---|---|---|
| SOC 3 (System and Organization Controls 3) | Operational trust | Planned: continuous controls over Security, Availability, Processing Integrity, Confidentiality, Privacy |
| Digital Asset Resolution Package (DARP) | Structural sovereignty | Planned: cryptographic segregation of assets so they remain transferable on vendor failure |
| OSCAL (NIST Open Security Controls Assessment Language) [^1] | Machine-readable compliance | Planned: manifests in `oscal-manifests/` per repository; 60-second self-audit cycle |
| ISO 19650 | Records management | Document-state suffixes enforced across BIM and real-property artefacts |
| ISO/IEC 42001:2023 — AI Management System [^2] | Algorithmic transparency | Planned: immutable log of every AI routing decision through the [[doorman-protocol\|Doorman]] audit boundary |
| DORA (EU Digital Operational Resilience Act) | EU sector regulation | Targeted: supports intended EU customer deployments |
| FedRAMP | US Government | Targeted: supports intended US public-sector deployments |
| GDPR | EU privacy | Targeted: supports intended EU privacy compliance |
| BCSC (NI 51-102, OSC SN 51-721) [ni-51-102] [osc-sn-51-721] | Continuous disclosure | All forward-looking claims carry planned/intended/may/target language |
| SLSA (Supply-chain Levels for Software Artifacts) | Supply-chain integrity | Planned: vendor-side build attestation |
| ISO 15489 | Records management | Repository documentation naming conventions |
| ISO 24495-1 | Plain language | Voice and tone discipline for [[service-content\|service-content]] outputs |

"Targeted" in the table means the architecture is designed with the framework's requirements in mind; certification against that framework is intended but has not been obtained. No compliance claim in this article should be interpreted as a current certification.

## Controls designed below the operating system

Two components are planned at the system tier to carry SOC 3 and DARP obligations:

| Planned component | Role |
|---|---|
| `service-audit` | An intended immutable, append-only log that runs alongside the capability-based manager. Every communication from a [[totebox-os\|Totebox]] to the outside world is intended to hash the capability routing into the microkernel log. Because the component is intended to run below the OS, an administrator cannot disable it without disabling the operating system. |
| `service-resolution` | The planned cryptographic packager for DARP. Intended to ensure every Totebox is structurally segregated. On vendor failure or deliberate system halt, this planned component severs the data and returns it cleanly to the legal owner. |

The design principle is that controls at the policy layer are valid until an administrator overrides them; controls at the system tier cannot be overridden without stopping the system. The second class of control is what institutional fiduciaries require and what these planned components are intended to provide.

## The three assets that constitute Continuous Proof

When the planned dashboard is realised, it is intended to expose three machine-readable assets that together constitute what the architecture calls Continuous Proof — a perpetual attestation surface replacing annual audit-report cycles:

| Planned asset | Contents |
|---|---|
| Hardware Bill of Materials (HBOM) | Every hardware component in the customer's [[os-workplace\|os-workplace]] reference profile |
| Software Bill of Materials (SBOM) | Every dependency used in the customer's deployed substrate |
| Real-Time Audit Log | The current operational heartbeat of the [[diode-standard\|Diode Standard]], intended to be queryable on demand by the customer's own risk-management systems |

All three are planned outputs; the intended delivery timeframe is not published here. Any specific availability date is a forward-looking statement subject to the BCSC continuous-disclosure posture.

## ISO 19650 document-state suffix conventions

The architecture adopts ISO 19650 document-state codes as filename suffix conventions. Audit tooling reads the suffix and routes the artefact accordingly.

| Suffix | ISO 19650 status | Meaning |
|---|---|---|
| `_JW` | S0 | Work in progress — draft, not yet shared |
| `_FIN` | S4 | Final, shared for approval or coordination |
| `_PUB` | A0 | Published and approved for use |
| `_EXE` | CR | Executed or signed — record or as-constructed state |
| `_MCH` / `_DAT` | (matches parent) | Machine-readable version of the parent document |

A `_PUB` file is treated as signed and immutable. A `_JW` file is in flight and carries no verified status. A `_EXE` file has passed operator confirmation at the [[app-console-input|F12 input gate]] and is sealed in the [[worm-ledger-design|WORM ledger]].

## How the BCSC continuous-disclosure posture applies

PointSav operates inside a Canadian regulatory frame. The British Columbia Securities Commission requires that forward-looking statements carry appropriate cautionary language and that claims about current compliance accurately reflect the current state.

Every public document the platform publishes — including this article — applies the following discipline: planned and intended language for controls not yet deployed; no claims of current certification without operator confirmation; all references to the Sovereign Data Foundation in planned and intended terms only, until operator clearance for a different classification.

## See also

- [[architecture-decisions|SYS-ADR-07]] — the architectural decision prohibiting structured data from passing through AI without human verification
- [[architecture-decisions|SYS-ADR-19]] — the architectural decision prohibiting automated AI publishing to verified ledgers
- [[worm-ledger-design]] — the WORM ledger substrate that enforces append-only record-keeping
- [[doorman-protocol]] — the AI gateway whose audit boundary supports ISO/IEC 42001 logging intentions
- [[diode-standard]] — unidirectional command flow that enforces the single-direction control constraint
- [[structural-positioning]] — the eight architectural commitments the compliance posture supports
