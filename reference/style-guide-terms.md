---
schema: foundry-doc-v1
title: "Style guide — terms of use"
slug: style-guide-terms
category: reference
type: topic
quality: complete
short_description: "Editorial standards for terms-of-use documents (LEGAL genre) in the platform: opening clause, required sections, defined-term discipline, liability-disclaimer conventions, and the governance review requirement."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-24
editor: pointsav-engineering
cites: []
paired_with: style-guide-terms.es.md
---

> Terms of use state what a user may do with a service, what they may not do, and what the service owes them in return. Use constitutes acceptance.

**Terms of use** (LEGAL genre) are the binding rules that govern a user's access to and use of a service or site. They are published where users can read them before using the service — the opening clause makes clear that use of the service constitutes acceptance. Every terms-of-use document executed under this platform routes through `factory-release-engineering` governance for review before publication. This article is the human-facing standard; the machine-readable counterpart lives in `service-disclosure/templates/terms.toml`.

## When to use this template

Use terms of use when:

- A service or site is made available to users outside the Foundry workspace.
- The service's permitted and prohibited uses need to be on record.
- Liability limitations and warranty disclaimers need to be formally stated.

Internal tooling used only by workspace members does not require public terms of use — a policy document covers internal-use obligations.

## Structure

The template requires an opening clause and five sections in this order:

**Opening clause** (before any heading): One sentence stating what service these terms govern and that use of the service constitutes acceptance of these terms.

| Section | Purpose |
|---|---|
| **Definitions** | Each defined Term, stated once. Capitalised after first definition. |
| **Acceptance** | How a user accepts the terms — by signing up, accessing the service, or clicking "I agree." What acceptance binds: the user to these terms; the service provider to the described service. |
| **Use of the service** | Permitted uses, prohibited uses, and the user's obligations (for example, account security, accurate registration). Numbered for traceability. |
| **Liability and disclaimers** | The warranty disclaimer and the limitation of liability. Must be in plain language: excessive legalese reduces enforceability. Standard formulations ("THE SERVICE IS PROVIDED 'AS IS'") may be used but must be followed by a plain-language equivalent. |
| **Changes to these terms** | How the terms may change, what constitutes notice to users, and the effective date of changes. |

Optional sections (at the end): Governing law and jurisdiction, Contact.

## Register and tone

Legal-plain. Active voice where possible. Every defined Term is capitalised on every use after its definition. BCSC posture applies where the service touches investment or disclosure material: forward-looking claims about service features or roadmap carry "planned / intended / may / target" language.

## See also

- [[style-guide-policy|Style Guide — Policy]]
- [[style-guide-contract|Style Guide — Contract]]
- [[style-guide-cla|Style Guide — CLA]]
- [[language-protocol-substrate|Language Protocol Substrate]]
