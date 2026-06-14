---
schema: foundry-doc-v1
title: "Style guide — policy"
slug: style-guide-policy
category: reference
type: topic
content_type: topic
quality: complete
short_description: "Editorial standards for policy documents (LEGAL genre) in the platform: scope discipline, numbered rule format, enforcement clause, review cadence, and the distinction between a policy and an ADR."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-24
editor: pointsav-engineering
cites: []
paired_with: style-guide-policy.es.md
---

> A policy states what is required, who is bound, and what happens when the rule is violated. Every sentence in a policy is either a rule or support for a rule.

A **policy** (LEGAL genre) is a binding statement of required behaviour within a defined scope. It differs from an ADR (which records a one-time architectural decision and its rationale — see [[architecture-decisions|Architecture Decision Records]]) and from a convention (which describes an agreed pattern). A policy names its rules, its enforcement mechanism, and its review cadence. This article is the human-facing standard; the machine-readable counterpart lives in `service-disclosure/templates/policy.toml`.

## When to use this template

Use a policy when:

- Behaviour must be uniform across a team, project, or organisation.
- Deviation has real consequences and those consequences need to be stated.
- The rule needs a review cadence so it does not silently go stale.

Do not write a policy for a preference or a guideline. A policy requires enforcement; a guideline carries the word "preferred" or "recommended" and does not.

## Structure

The template requires five sections in this order:

| Section | Purpose |
|---|---|
| **Scope** | Who and what this policy applies to. Named roles, systems, or contexts. Explicit about what it does not apply to. |
| **Policy** | The rules, numbered. Each rule is a complete, standalone statement. The first word is an obligation: "All X must…", "No Y may…", "Every Z is required to…". |
| **Enforcement** | What happens when a rule is violated. Must name a consequence or a process — not a vague "will be addressed." |
| **Review** | How often this policy is reviewed and by whom. Minimum annual. Policies in fast-moving domains review every six months. |
| **See also** | Links to the ADRs, conventions, or laws that this policy implements or is required by. |

## Register and tone

Legal-plain. Active voice. No hedges: a policy either requires something or it does not. "Should" and "encouraged" are not policy language — use "must" or "shall" for requirements, or move the statement to a convention.

Sentence-length budget: target under twenty-five words per rule. Numbered rules are paragraphs, not bullets — each stands alone. The Scope section must be precise enough that a new team member can determine, without asking, whether the policy binds them.

## See also

- [[architecture-decisions|SYS-ADR-07 — No AI on Structured Data]]
- [[style-guide-architecture|Style Guide — ARCHITECTURE]]
- [[language-protocol-substrate|Language Protocol Substrate]]
