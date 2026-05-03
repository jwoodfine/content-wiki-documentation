---
schema: foundry-doc-v1
title: "Style Guide — Policy"
slug: topic-style-guide-policy
category: reference
type: topic
quality: core
short_description: "Editorial standards for the policy template in Foundry's service-disclosure library, covering the four required sections, LEGAL family routing, the mandatory draft header, reading-level requirements, and the distinction from Terms of Service."
status: pre-build
last_edited: 2026-04-30
editor: pointsav-engineering
cites: []
paired_with: topic-style-guide-policy.es.md
---

A **policy document** in Foundry defines a rule — a code of conduct, an acceptable-use policy, a security-disclosure procedure, or a data-handling standard — written at grade-12 reading level so that every staff member, not only legal counsel, can read and apply it.

The policy template is part of the LEGAL family in Foundry's `service-disclosure` genre-template registry. LEGAL family documents route to Tier C (external API) by default, because their content carries compliance risk and benefits from the precision of the highest-quality available model. Every policy document produced through this template carries a "DRAFT — for legal review" header and is never a substitute for counsel. This style guide is the human-facing companion to `service-disclosure/templates/policy.toml`.

## When to use this template

Use the policy template when your organisation needs a written rule that governs conduct or procedure — employee conduct, acceptable use of systems, security reporting procedures, data retention standards, or similar. A policy is not a one-off decision; it is a standing rule that applies repeatedly until revised or withdrawn.

Do not use the policy template for a one-time decision record — that is a memo. Do not use it for user-facing legal agreements — those use the terms template.

## Frontmatter fields

Policy documents are internal governance artefacts. Required frontmatter fields:

| Field | Notes |
|---|---|
| `schema` | `foundry-doc-v1` |
| `title` | Identifies the policy by name and version if applicable |
| `tenant_required` | `true` — a policy applies to a specific organisation and must name it |
| `status` | Always `pre-build` until legal review is complete; then `stable` |
| `last_edited` | ISO 8601 date — must be updated when the policy is revised |

The `cites` field is used when the policy references an external regulatory instrument (a statute, a standard, a regulatory guideline). Citation IDs resolve against `~/Foundry/citations.yaml`.

## Structure

The template defines four required sections:

**Scope** — Who and what the policy covers. Name the organisation, the staff roles the policy applies to, the systems or activities it governs, and any explicit exclusions. A policy whose scope is ambiguous will be applied inconsistently.

**Policy statement** — The rule itself, in plain language. State what is required, permitted, or prohibited. One rule per sentence where possible; policies that embed multiple rules in a single complex sentence are difficult to enforce.

**Procedures** — How the policy is operationalised. Reporting procedures, review cadence, approval authorities, and escalation paths. A policy without procedures is aspirational rather than operational.

**Enforcement** — Consequences for breach and the appeal path. Name the consequence categories (verbal warning, written warning, termination, regulatory referral) proportionate to the severity of the breach. Name who decides and who hears appeals. A policy without an enforcement section is unenforceable; that absence may itself be a compliance liability.

## Register and tone

The register is legal, but the reading level is grade-12 — not legal-professional. A policy that staff members cannot parse cannot be followed. The sentence-length target is slightly longer than operational templates: mean around eighteen words, maximum around thirty-two.

Plain-language equivalents replace legalese wherever the meaning is preserved. "A staff member must not" replaces "No employee shall"; "you may report concerns to" replaces "grievances may be directed to the appropriate authority".

The global banned-vocabulary list applies.

## The draft header

Every policy document produced through this template carries the following header immediately after the frontmatter:

```markdown
> **DRAFT — for legal review.** This document has not been reviewed
> by qualified legal counsel and does not constitute legal advice.
> Seek advice appropriate to your jurisdiction before adopting.
```

Remove this header only when legal review is complete and the document's `status` is updated to `stable`. Do not remove it as a formatting convenience.

## See Also

- [[topic-style-guide-terms|Style Guide — Terms of Service]]
- [[topic-style-guide-memo|Style Guide — Memo]]
- [[topic-language-protocol-substrate|Language Protocol Substrate]]
- [[topic-canadian-simple-copyright|Canadian Simple Copyright]]

## References
