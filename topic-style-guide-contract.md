---
schema: foundry-doc-v1
title: "Style Guide — Contract"
slug: topic-style-guide-contract
category: reference
type: topic
quality: core
short_description: "Editorial standards for contract drafts produced through the Foundry language-protocol stack, covering the LEGAL family routing rules, required sections, the professional register, and the mandatory legal-review disclaimer."
status: pre-build
last_edited: 2026-04-30
editor: pointsav-engineering
cites: []
paired_with: topic-style-guide-contract.es.md
---

> A contract draft produced through the Foundry stack routes to Tier C by default and carries a "DRAFT — for legal review" header without exception — local generation requires explicit operator approval.

A **contract** in the Foundry language-protocol stack belongs to
the LEGAL family alongside the CLA template. It is the most
structurally constrained template in the stack: five required
sections in a fixed order, a professional reading level, and
routing that defaults to Tier C because substantive contract
drafting requires a legal corpus that local SLM models do not
carry. The machine-readable counterpart lives in
`service-disclosure/templates/contract.toml`.

## When to use this template

Use the contract template when producing or revising a contract
for a Foundry-affiliated tenant — a service agreement, a vendor
agreement, an employment contract, or any other bilateral
instrument. The template is appropriate when:

- A new contract needs to be drafted from a term sheet or
  instructions.
- An existing contract is being reviewed and improved for
  clarity or completeness.
- A template contract needs to be adapted for a specific
  counterparty.

The `default_routing = "tier-c"` setting means the Doorman
sends contract work to a Tier C model unless the operator has
explicitly enabled a different route. Local generation in
Tier A or Tier B is permitted only when the tenant has a
legal corpus large enough to support it and the operator has
confirmed the route. This is not a cost-optimisation decision;
it is a risk-management one.

Every contract output carries a "DRAFT — for legal review"
header. Removing the header before formal legal review is a
posture violation.

## Frontmatter fields

Contracts are legal instruments and do not carry YAML
frontmatter. The routing parameters are set in the
`ProtocolRequest`:

| Field | Notes |
|---|---|
| `tenant` | Required. Identifies the legal entity whose contract is being produced. |
| `genre_template` | `GenreTemplate::Contract` |
| `register` | `legal` — professional register throughout. |
| `routing` | Defaults to Tier C. Override requires explicit operator approval. |

## Structure

The template requires five sections in this order:

| Section | Purpose |
|---|---|
| **Parties** | Full legal names of all parties to the agreement, including registered addresses. |
| **Recitals** | Background context for the agreement. Conventional "WHEREAS" form. One recital per relevant background fact; typically two to five recitals. |
| **Definitions** | Defined terms listed in alphabetical order. Capitalised throughout the document when used. |
| **Operative clauses** | Numbered clauses stating the obligations, rights, and covenants of each party. One obligation per clause. |
| **Signature block** | Execution signatures with names, titles, dates, and counterpart provisions if applicable. |

Optional sections — Schedules, Annexures, Representations and
Warranties — are added after the signature block when the
agreement requires them.

## Register and tone

The register is professional legal. Sentence-length budget: mean
around twenty-two words, maximum around forty — the longest budget
of any Foundry template. Legal precision requires completeness
and specificity that is incompatible with short sentences in
operative clauses.

Active voice is preferred in operative clauses ("Party A shall
deliver") over passive ("Delivery shall be made by Party A").
Passive is acceptable in definitions and recitals.

The banned-vocabulary list applies. Marketing-grade terms have no
place in contract language. Terms like "robust", "seamless", and
"leverage" are legally meaningless and weaken the instrument.

## Example

```markdown
<!-- DRAFT — for legal review -->

## Parties

This Agreement is entered into between:
**PointSav Digital Systems Inc.** ("Vendor"), and
**Woodfine Management Corp.** ("Customer").

## Recitals

WHEREAS the Vendor has developed a platform for document
management and business operations; and

WHEREAS the Customer wishes to obtain access to that platform
on the terms set out below;

## Definitions

"Platform" means the software and services described in
Schedule A.

## Operative clauses

1.1 The Vendor shall provide the Customer with access to the
Platform commencing on the Effective Date.

## Signature block

Signed by PointSav Digital Systems Inc.: _______________
Date: __________
```

## See also

- [[topic-style-guide-cla|Style Guide — Contributor License Agreement]]
- [[topic-language-protocol-substrate|Language Protocol Substrate]]
- [[topic-canadian-simple-copyright|Canadian Simple Copyright]]

## References
