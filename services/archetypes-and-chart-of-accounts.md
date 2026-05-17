---
schema: foundry-doc-v1
title: "Archetypes and chart of accounts"
slug: archetypes-and-chart-of-accounts
category: services
type: concept
quality: complete
short_description: "The Chart of Accounts and eleven archetypes are the two-part institutional taxonomy at the core of service-people and service-content, classifying personnel and documents by structural position and functional role rather than by volatile job-title strings."
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-15
editor: pointsav-engineering
paired_with: archetypes-and-chart-of-accounts.es.md
references:
 - id: 1
 text: "IFRS Foundation, IAS 1 — Presentation of Financial Statements, §54–76: Statement of Financial Position — line-item and sub-classification requirements for accounts."
 url: "https://www.ifrs.org/issued-standards/list-of-standards/ias-1-presentation-of-financial-statements/"
 - id: 2
 text: "International Labour Organization, International Standard Classification of Occupations 2008 (ISCO-08): Conceptual Framework and Methodology. ILO, Geneva, 2012."
 url: "https://www.ilo.org/public/english/bureau/stat/isco/docs/publication08.pdf"
---

The Chart of Accounts and the eleven archetypes are the two-part institutional taxonomy at the core of [[service-people]] and [[service-content]]. Together they let the platform classify personnel and documents by structural position and functional role, without relying on volatile job-title text. Unlike a free-text personnel record, the taxonomy is socket-based: each person occupies a fixed position in the Chart and inherits properties from one of eleven immutable archetype classes. By the end of this article, a reader will understand the archetype taxonomy, the Chart of Accounts hierarchy, and the self-healing mechanism their intersection enables.

## Two ledgers, one institution

The taxonomy is built from two interlocking ledgers. One defines the structural anatomy of the organisation. The other defines the functional role of the people inside it.

| Ledger | What it captures | How it changes |
|---|---|---|
| Chart of Accounts | Where authority, risk, and production reside in the organisation — a three-level hierarchy of Profile → Domain → Sub-Domain [^1] | Adjusted deliberately by operators; stable between adjustments |
| Eleven Archetypes | How a person operates and what they produce, regardless of their job title [^2] | Fixed permanently; the eleven categories are exhaustive |

The Chart of Accounts is the institution's general ledger and namespace simultaneously. To a financial reader, every row is a cost or revenue centre. To an engineering reader, every row is a stable namespace path that prevents orphaned documents. [[service-content]] consumes the Chart hierarchy when classifying incoming documents at the F12 gate; [[service-people]] consumes the archetype layer when evaluating personnel alignment.

Neither ledger is a substitute for the other. The Chart captures *where* in the organisation a document or decision belongs; the archetype captures *how* the person producing it operates. Their intersection is the platform's working model of institutional behaviour.

## The eleven archetypes and their evaluator keys

Each of the eleven archetypes maps to a primary organisational function and a machine-readable evaluator key. The key is consumed by the platform's alignment engine when comparing a person's observed behaviour against their structural position.

| Archetype | Primary function | Evaluator key |
|---|---|---|
| The Executive | Authority and strategy | `exec_integrity` |
| The Guardian | Risk and compliance | `risk_variance` |
| The Fiduciary | Fiscal management | `asset_trust` |
| The Architect | Structural systems | `vision_alignment` |
| The Engineer | Logic and data | `logic_efficiency` |
| The Artisan | Craft and aesthetics | `output_fidelity` |
| The Constructor | Physical build | `build_durability` |
| The Catalyst | Growth and momentum | `velocity_factor` |
| The Envoy | Influence and diplomacy | `relation_equity` |
| The Steward | Logistics and support | `system_stability` |
| The Sage | Theory and knowledge | `knowledge_depth` |

The archetypes function as object classes in the software sense: every entity in [[service-people]] inherits properties from one of the eleven base classes, and that inheritance determines which platform functions the system can apply to that person's record. Two people with different job titles who share an archetype share the same computational treatment; two people with the same title but different archetypes do not.

The evaluator keys are not scores. They are dimension labels — the platform tracks the variance of each key over time rather than its absolute value, which makes the system robust to different baseline levels across individuals.

## How the Chart of Accounts anchors to archetype roles

Each row in the Chart of Accounts carries a primary archetype anchor. The anchor is the expected functional role for that structural position. A small illustration from a canonical real-property institutional Chart:

| Profile | Domain | Sub-Domain | Anchor archetype |
|---|---|---|---|
| Compliance | Counsel | Legal Representation | The Guardian |
| Compliance | Accounting | — | The Fiduciary |
| Real Estate | Office Leasing | — | The Catalyst |
| Real Estate | Office Tenants | — | The Steward |
| Construction | Collaborators | Façade Consultants | The Engineer |
| Construction | Collaborators | Landscape Architects | The Artisan |
| Construction | Trades | — | The Constructor |
| IT Support | Contributors | BIM | The Engineer |
| IT Support | Contributors | Data Science | The Sage |
| Personnel | Supervisory Board | — | The Executive |

The Chart spans seven top-level Profiles in a typical deployment: Compliance, Real Estate, Construction, IT Support, Investor Relations, Personnel, and Local Administration. Together they cover the institutional surface of a real-property enterprise. The specific Profiles are operator-configurable; the seven-Profile example represents a reference deployment, not a fixed constraint.

The anchor archetype is used to set expectations, not to restrict access. A Guardian-anchored Compliance Counsel can hold Fiduciary responsibilities if the operator assigns them; the Chart captures the primary anchor, and the alignment engine tracks divergence from it.

## How the platform detects and surfaces organisational drift

The most distinctive property of the dual-ledger design is that [[service-people]] and [[service-content]] use the relationship between the two tables to detect and flag organisational drift. The engine evaluates whether a person's observed behaviour matches their structural position.

| Scenario | Diagnosis | System response |
|---|---|---|
| Chart position matches archetype output | Healthy alignment | No action |
| Chart position matches, archetype output drifts | Functional friction | The system throttles mismatched task routing and re-routes to aligned tasks |
| Chart position mismatches, high archetype signal | Talent discovery | The system flags a potential role mismatch and proposes a Chart adjustment to the administrator |
| Neither dimension matches | Systemic noise | The system suspends metric calculation to prevent contaminating aggregate data; a manual audit is flagged |

The mechanism does not take autonomous personnel action. The platform does not move, promote, or dismiss people. It surfaces structural mismatches and proposes adjustments; an operator makes every decision. The audit trail in service-minutebook captures the proposal, the operator's decision, and the timestamp — the same pattern as the [[app-console-input|F12 input gate]].

## Why socket-based taxonomy outperforms free-text job titles

Conventional HR and relationship-management systems store job titles as free text. Four different strings can describe one role with seniority bands; the database treats them as four entirely different entities, and aggregation across them requires manual normalisation. [^2]

The Chart of Accounts and archetype design resolves this structurally:

| Property | Effect |
|---|---|
| Sockets, not strings | Each person maps to a fixed Profile → Domain → Sub-Domain socket; the title text is supplementary metadata |
| Semantic translation | Updating the definition of a role requires changing one row in the central Chart, not every personnel record that references it |
| Behaviour-aware classification | The archetype layer tracks what the person produces, not what their title claims they produce |

The deterministic identity assigned to an individual by [[service-extraction]] — a content-hash-derived identifier stable across renames and title changes — remains constant; the socket assignment and archetype reading evolve as the operator updates them.

## See also

- [[service-people]] — the service that maintains personnel records against this taxonomy
- [[service-content]] — the service that classifies incoming documents against the Chart of Accounts hierarchy
- [[service-extraction]] — the extraction engine that derives entity identifiers from incoming documents
- [[app-console-input]] — the F12 input gate where operators confirm routing decisions against the Chart
