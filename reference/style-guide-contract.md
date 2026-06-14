---
schema: foundry-doc-v1
title: "Style guide — contract"
slug: style-guide-contract
category: reference
type: topic
content_type: topic
quality: complete
short_description: "Editorial standards for contract documents (LEGAL genre) in the platform: parties discipline, recitals format, definitions vocabulary, term and termination clause, and the review-before-binding rule."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-24
editor: pointsav-engineering
cites: []
paired_with: style-guide-contract.es.md
---

> A contract names its parties, defines its terms, and states what each party is bound to do. Every clause is a commitment or a condition — nothing else.

A **contract** (LEGAL genre) is a formal agreement between two or more named parties that creates binding obligations. It is authored in the legal-plain register and reviewed by the responsible governance party before any party signs. This article is the human-facing standard; the machine-readable counterpart lives in `service-disclosure/templates/contract.toml`.

## When to use this template

Use the contract template when:

- A formal binding agreement is required between named parties.
- The obligations, term, and termination conditions need to be explicit and traceable.
- The agreement will be reviewed by `factory-release-engineering` governance before execution.

Informal operational agreements between team members or roles do not require a contract — a [[style-guide-memo|memo]] or [[style-guide-ticket-comment|ticket comment]] records them. Agreements that bind a legal entity (PointSav Digital Systems, Woodfine Management Corp., or a third party) require governance review before any signature.

## Structure

The template requires six sections in this order:

| Section | Purpose |
|---|---|
| **Parties** | The full legal names, registered addresses, and defined short names ("PointSav," "Vendor," "Contributor") of every party to the agreement. |
| **Effective date** | The date on which the agreement takes effect. If conditional on signature, state "the date of the last signature." |
| **Recitals** | Short "Whereas" clauses: the context and intent. Two to five recitals. Not obligations — context for interpretation. |
| **Definitions** | Each defined Term, stated once. Defined terms are capitalised throughout the contract after their first definition. |
| **Terms** | The substantive obligations: what each party must do, by when, and under what conditions. Numbered clauses. |
| **Term and termination** | The duration of the agreement, how it may be terminated, and what happens upon termination (survival clauses, obligations that persist). |

An optional **Signatures** block follows the last section. Its format is determined by the jurisdiction and signature method.

## Register and tone

Legal-plain. Defined terms are capitalised after their first definition. Active voice where possible: "Vendor shall deliver" rather than "Delivery shall be made by Vendor." No "herein," "aforementioned," or "notwithstanding" when plain alternatives exist. Every obligation names a subject and a deadline.

Every agreement that binds a legal entity routes through the system administrator (`open.source@pointsav.com`) for governance review before any signature is obtained. This rule applies without exception.

## See also

- [[style-guide-cla|Style Guide — CLA]]
- [[style-guide-policy|Style Guide — Policy]]
- [[style-guide-terms|Style Guide — Terms of Use]]
- [[language-protocol-substrate|Language Protocol Substrate]]
