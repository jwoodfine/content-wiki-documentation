---
schema: foundry-doc-v1
title: "Style Guide — Terms of Service"
slug: style-guide-terms
category: reference
type: topic
quality: core
short_description: "Editorial standards for the terms template in Foundry's service-disclosure library, covering the six required sections, LEGAL family routing, the mandatory draft header, bilingual pair requirements, and the intentionally longer sentence-length allowance."
status: pre-build
last_edited: 2026-04-30
editor: pointsav-engineering
cites:
  - ni-51-102
paired_with: style-guide-terms.es.md
---

A **Terms of Service** document defines the contract between a service provider and its users — acceptance, service description, payment, termination, liability limits, and governing law — and every draft carries a mandatory header requiring legal review before publication.

The terms template is part of the LEGAL family in Foundry's `service-disclosure` genre-template registry. Like the policy template, terms documents route to Tier C (external API) by default, because the precision cost of a legal error in public-facing terms is significant. The template is public-facing, so a bilingual pair is recommended when the customer base spans languages. This style guide is the human-facing companion to `service-disclosure/templates/terms.toml`.

## When to use this template

Use the terms template when drafting or revising user-facing legal agreements: Terms of Service, Terms of Use, Subscription Agreements, or similar. The template is not for internal governance rules — those use the policy template — and not for license summaries — those use the license-explainer template.

Do not generate Terms of Service text through the AI pipeline without explicit operator approval. The terms template has `default_routing: tier-c` for this reason; local inference at Tier A or Tier B is not appropriate for drafting public legal commitments.

## Frontmatter fields

Terms documents are public-facing legal artefacts. Required frontmatter fields:

| Field | Notes |
|---|---|
| `schema` | `foundry-doc-v1` |
| `title` | Identifies the service and the agreement type (e.g., "PointSav Platform — Terms of Service") |
| `tenant_required` | `true` — terms apply to a specific service and tenant and must name both |
| `status` | Always `pre-build` until legal review is complete; then `stable` |
| `last_edited` | ISO 8601 date — must be updated whenever terms are revised |

When terms reference a governing statute or regulation (consumer protection legislation, privacy law), include the citation ID in the `cites` field. The BCSC continuous-disclosure posture per `[ni-51-102]` applies: forward-looking statements about planned features or pricing changes carry `planned`, `intended`, or `may` language.

## Structure

The template defines six required sections:

**Acceptance** — How a user accepts these terms. Name the acceptance mechanism (clicking "I agree", creating an account, making a purchase) and the effect of that acceptance. State what happens if the user does not accept.

**Service description** — What the service does. One to three paragraphs covering scope, key features, and any material limitations. Avoid promotional language; the description should be accurate and complete, not persuasive.

**Payment** — Rates, billing cycle, refund policy, and late fees if any. If the service has a free tier, state its scope here. Name the currency. Name what happens when payment fails.

**Termination** — Each party's right to end the relationship, the notice period required, and the obligations that survive termination (data handling, unpaid fees, IP ownership). Users and the service provider both have termination rights; state both.

**Limitation of liability** — The caps on the service provider's liability and the carve-outs where those caps do not apply. This section is legally significant; draft with counsel. Name the applicable standard (negligence, gross negligence, wilful misconduct) for each exception.

**Governing law** — The jurisdiction whose law governs the agreement, the venue for disputes, and whether disputes are subject to arbitration or litigation.

## Register and tone

The register is legal. The sentence-length allowance for terms documents is intentionally longer than other templates — mean around twenty words, maximum around thirty-six — because legal precision sometimes requires complex conditional structure. The goal is not long sentences; it is sentences that are no shorter than the law requires.

Grade-12 reading level is the target. Where plain language can replace legal formulation without sacrificing precision, prefer plain language. "You may cancel your account at any time" is clearer and equally binding as "Subscriber may effect termination of the Account at its sole discretion by providing notice through the cancellation mechanism."

The global banned-vocabulary list applies.

## The draft header

Every terms document carries the following header immediately after frontmatter:

```markdown
> **DRAFT — for legal review.** This document has not been reviewed
> by qualified legal counsel and does not constitute legal advice.
> Seek advice appropriate to your jurisdiction before publishing or
> relying on these terms.
```

Remove this header only when legal review is complete. Never omit it as a formatting shortcut.

## See Also

- [[style-guide-policy|Style Guide — Policy]]
- [[style-guide-license-explainer|Style Guide — License Explainer]]
- [[language-protocol-substrate|Language Protocol Substrate]]
- [[canadian-simple-copyright|Canadian Simple Copyright]]

## References
