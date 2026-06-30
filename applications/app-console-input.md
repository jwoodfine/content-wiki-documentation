---
schema: foundry-doc-v1
title: "Console input application"
slug: app-console-input
category: applications
type: app
content_type: topic
quality: complete
short_description: "app-console-input is the F12 surface in os-console — the structured input gate through which raw external files enter a Totebox before being sealed into the verified ledger."
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-05-15
editor: pointsav-engineering
paired_with: app-console-input.es.md
cites:
 - ni-51-102
 - osc-sn-51-721
references:
  - id: 1
    text: "NIST, Artificial Intelligence Risk Management Framework (AI RMF 1.0), NIST AI 100-1, January 2023. Section 5: Human oversight and accountability in AI deployments."
    url: "https://doi.org/10.6028/NIST.AI.100-1"
  - id: 2
    text: "International Organization for Standardization, ISO/IEC 27001:2022 — Information security management systems, Annex A.8.15: Logging."
    url: "https://www.iso.org/standard/82875.html"
---

`app-console-input` is the F12 surface in [[console-os|os-console]] — the only path through which raw external files enter a [[totebox-os|Totebox]] before being sealed into the [[worm-ledger-design|WORM ledger]]. The surface routes every incoming document through a structured human verification step, holding the operator accountable for each [[service-extraction|extracted]] claim before it advances to verified status. Unlike a [[service-slm|language model]] interface or autosave pipeline, it presents binary choices — the system proposes, the operator confirms or rejects — so every fiduciary decision carries an operator signature in the [[worm-ledger-design|audit trail]]. By the end of this article, a reader will understand the F12 workflow, the Verification Surveyor pattern, and the audit properties the gate enforces.

## How the F12 session unfolds

A typical F12 session has a deterministic five-step shape. Each step has a clear boundary; the operator does not skip forward or batch decisions.

| Step | Operator action | System response |
|---|---|---|
| 1 | Drag a file from the desktop into the F12 window | The system computes a content hash and strips execution permissions |
| 2 | Select a category from the [[archetypes-and-chart-of-accounts|Chart of Accounts]] (Profile → Domain → Sub-Domain) | The system prepares a routing destination |
| 3 | Review the entities and themes the system pre-extracted via [[service-extraction]] and [[service-content]] | The system displays a Yes / No verification prompt for each claim |
| 4 | Approve or reject each claim with single keystrokes | Approved claims advance to L5 verified status; rejected claims are quarantined |
| 5 | Confirm the routing destination | The file is sealed into service-minutebook or service-bookkeeper; a ledger entry is written; the [[worm-ledger-design|audit log]] captures the operator identity, timestamp, and routing decision |

The interaction is keyboard-only and intentionally fast. The operator does not type filenames, fill out metadata forms, or compose database queries. [[service-extraction]] and [[service-content]] have already done the computational work; the operator's role is to verify or reject each claim in sequence, then confirm the destination.

This sequential structure is deliberate. Bundling multiple steps into a single confirmation would reduce the resolution of the [[worm-ledger-design|audit trail]] — each claim would inherit the same timestamp rather than carrying its own decision record. The five-step gate preserves per-claim audit granularity.

## The Verification Surveyor pattern — binary choices over open forms

The F12 interaction model is sometimes described as the Verification Surveyor: rather than presenting the operator with a blank form, the system presents a binary choice — "I extracted this fact; is it correct? Yes or No." [^1]

The pattern has three properties:

| Property | Effect |
|---|---|
| Low cognitive load | The operator processes a stream of Yes/No decisions rather than authoring structured data |
| Fiduciary clarity | Every claim that enters the verified ledger carries an explicit operator decision, not a system default |
| Audit completeness | The [[worm-ledger-design|audit record]] captures the exact decision on each claim, not only the final routing destination |

This model reflects a deliberate boundary between platform and operator. [[service-extraction]] and [[service-content]] handle entity detection, theme classification, and routing suggestion. The operator handles the binary gate. Institutions subject to continuous-disclosure obligations [ni-51-102] [osc-sn-51-721] and electronic-record standards [^2] can point to a specific, timestamped operator decision for every document that enters the verified ledger.

The pattern differs from AI-assisted autofill, where a model populates fields and the operator accepts by omission. In F12, silence is never acceptance. Every claim that advances to verified status requires an explicit affirmative keystroke from the operator.

## Why the verification step is architecturally mandatory

If [[service-extraction]] or [[service-content]] were to route a source document into the wrong account without human confirmation, the downstream verified ledger would carry a mathematically compromised entry from that point forward. Re-sorting the document later does not repair the audit trail — the original entry already carries a verification timestamp that records a decision no human made.

[[architecture-decisions|SYS-ADR-10]] makes F12 mandatory precisely because this failure mode is structural, not probabilistic: any architecture that delegates the final routing decision to an automated system creates a ledger entry without an accountable human author. [[architecture-decisions|SYS-ADR-07]] extends the principle to structured data more broadly — no AI-produced record enters a verified ledger without a human confirmation step. [[architecture-decisions|SYS-ADR-19]] closes the remaining path — no automated publishing to verified ledgers, regardless of confidence score.

Institutional fiduciaries — asset managers, lawyers, regulated financial entities — require an audit trail they can defend under examination. The F12 gate is what makes that defense possible: every entry in service-minutebook and service-bookkeeper traces to a specific operator, a specific decision, and a specific timestamp. [^2]

## What the F12 surface is not

F12 is not a chat interface. The operator does not compose queries or converse with [[service-slm|the language model]]. The surface is structured: a file, a [[archetypes-and-chart-of-accounts|Chart of Accounts]] selection, a sequence of binary prompts, and a confirmation. All language-model work occurs upstream in [[service-extraction]] and [[service-content]] before the F12 session begins; the operator never sees raw model output.

F12 is not an autosave surface. A document enters the [[worm-ledger-design|WORM ledger]] only when the operator explicitly confirms the routing destination. This protects the audit trail from partial writes and abandoned sessions. Drafts in progress do not accumulate in the ledger; a document only lands when the operator reaches step five and confirms.

F12 is not a bulk-import interface. The operator may have a queue of documents to process, but each passes through the five-step gate individually, producing a distinct audit record per document. The sequential constraint is not a throughput limitation — it is an audit discipline. [[architecture-decisions|SYS-ADR-10]] is unambiguous on this point: the F12 boundary is mandatory per document.

## See also

- [[architecture-decisions|SYS-ADR-07]] — the architectural decision mandating human verification before structured data enters a verified ledger
- [[architecture-decisions|SYS-ADR-10]] — the architectural decision mandating F12 as the required input gate
- [[architecture-decisions|SYS-ADR-19]] — the architectural decision prohibiting automated publishing to verified ledgers
- [[console-os|os-console]] — the operating system that hosts the F12 surface
- [[service-extraction]] — the upstream entity and theme extraction engine
- [[service-content]] — the upstream classification and routing engine
- [[worm-ledger-design]] — the design principles behind the WORM ledger substrate
- [[machine-based-auth]] — the authentication layer that ties ledger entries to verified operator identity
