---
schema: foundry-doc-v1
title: "Console input application"
slug: app-console-input
category: applications
type: app
content_type: topic
quality: complete
index_group: input-and-developer-surfaces
short_description: "app-console-input is the F12 surface in os-console — a path, a confirm prompt, and a submission, through which raw external files enter a Totebox before being sealed into the verified ledger."
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-08-24
editor: pointsav-engineering
paired_with: app-console-input.es.md
cites:
 - ni-51-102
 - np-51-201
references:
  - id: 1
    text: "NIST, Artificial Intelligence Risk Management Framework (AI RMF 1.0), NIST AI 100-1, January 2023. Section 5: Human oversight and accountability in AI deployments."
    url: "https://doi.org/10.6028/NIST.AI.100-1"
  - id: 2
    text: "International Organization for Standardization, ISO/IEC 27001:2022 — Information security management systems, Annex A.8.15: Logging."
    url: "https://www.iso.org/standard/82875.html"
---

`app-console-input` is the F12 surface in [[console-os|os-console]] — the only path through which raw external files enter a [[totebox-os|Totebox]] before being sealed into the [[worm-ledger-design|WORM ledger]]. The surface holds the operator accountable for every file that enters the ledger: nothing is submitted without an explicit, keyboard-confirmed operator decision, so every fiduciary act carries an operator signature in the [[worm-ledger-design|audit trail]]. By the end of this article, a reader will understand the F12 workflow and the audit properties the gate enforces.

## How the F12 session unfolds

A session moves through four states in order: **Entry**, where the operator types the file's path; **Confirm**, a single yes/no prompt showing the exact path back; **Submitting**, while the cartridge posts to the ingest endpoint and waits; and **Done** (or **Error** on failure). Cancelling from Entry or Confirm returns to Entry with nothing submitted.

| Step | Operator action | System response |
|---|---|---|
| Entry | Type a file path | The cartridge accepts free-text path entry |
| Confirm | Press Y to submit, N or Esc to cancel | The cartridge shows the exact path back for a final yes/no decision |
| Submitting | Wait | The cartridge posts the file's path, the operator's identity, and the tenant to the ingest endpoint over HTTP |
| Done | — | The cartridge records the result — success, a warning, or an error — to a local audit log, and extends a local rolling ledger with the submission |

### Every submission is signed and chained

The interaction is keyboard-only and deliberately narrow: one path, one confirmation, one submission. There is no bulk-import mode and no metadata form — a document is either submitted through this exact sequence or it never enters the ledger.

Two audit trails record every submission, not one. Locally, the cartridge maintains a rolling hash — each successful submission's ledger entry is chained onto the previous one (`new_root = SHA256(prior_root ‖ payload_id)`), so the local sequence of submissions is independently verifiable end to end, entry by entry. The cartridge also writes a local audit record — timestamp, operator, tenant, path, ledger reference, and outcome — viewable at any time from the Entry screen. Separately, the file itself is appended to the platform's ledger service, which returns its own ledger reference back to the cartridge.

## Why the confirm step is architecturally mandatory

If a file entered the ledger without an operator explicitly confirming it, the ledger would carry an entry with no accountable human author from that point forward. There is no later step that repairs this: the entry already carries a timestamp asserting a decision no human made.

### Architectural decisions enforcing the gate

[[architecture-decisions|SYS-ADR-10]] makes F12 mandatory precisely because this failure mode is structural, not probabilistic: any path that lets a file reach the ledger without an explicit operator confirmation creates an unaccountable entry. [[architecture-decisions|SYS-ADR-07]] extends the principle to structured data more broadly — no AI-produced record enters a verified ledger without a human confirmation step. [[architecture-decisions|SYS-ADR-19]] closes the remaining path — no automated publishing to verified ledgers, regardless of confidence score.

Institutional fiduciaries — asset managers, lawyers, regulated financial entities — require an audit trail they can defend under examination. The F12 gate is what makes that defense possible: every submission traces to a specific operator, a specific confirmation, and a specific timestamp. [^2]

## What the F12 surface is not

F12 is not a chat interface. The operator does not compose queries or converse with [[service-slm|the language model]] — there is no model in this loop at all. The surface is a fixed sequence: a path, a yes/no confirmation, and a submission.

F12 is not an autosave surface. A file enters the ledger only when the operator explicitly presses Y at the confirm prompt. Cancelling at any point before that leaves nothing recorded.

F12 is not a bulk-import interface. The operator may have several files to submit, but each passes through the full path→confirm→submit sequence individually, producing its own audit record. The one-file-at-a-time constraint is not a throughput limitation — it is an audit discipline. [[architecture-decisions|SYS-ADR-10]] is unambiguous on this point: the F12 boundary is mandatory per file.

## See also

- [[architecture-decisions|SYS-ADR-07]] — the architectural decision mandating human verification before structured data enters a verified ledger
- [[architecture-decisions|SYS-ADR-10]] — the architectural decision mandating F12 as the required input gate
- [[architecture-decisions|SYS-ADR-19]] — the architectural decision prohibiting automated publishing to verified ledgers
- [[console-os|os-console]] — the operating system that hosts the F12 surface
- [[worm-ledger-design]] — the design principles behind the WORM ledger substrate
- [[machine-based-auth]] — the authentication layer that ties ledger entries to verified operator identity
