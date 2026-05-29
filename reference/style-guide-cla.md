---
schema: foundry-doc-v1
title: "Style guide — CLA"
slug: style-guide-cla
category: reference
type: topic
quality: complete
short_description: "Editorial standards for Contributor License Agreements (LEGAL-CLA genre) in the platform: canonical CLA authority, required sections, the patent-license discipline, and the factory-release-engineering review requirement."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-24
editor: pointsav-engineering
cites: []
paired_with: style-guide-cla.es.md
---

> A CLA transfers specific intellectual property rights from a contributor to the project. The canonical text is governed by factory-release-engineering — this template is for drafting or explaining one, not for executing one.

A **Contributor License Agreement** (LEGAL-CLA genre) is an agreement between a project and a contributor that grants the project the rights it needs to use, modify, and redistribute the contributor's work. A CLA is not a copyright transfer — the contributor retains copyright and grants a [[disclosure-substrate|license]]. Every CLA executed under this platform routes through `factory-release-engineering` governance before it binds any party. This article is the human-facing standard; the machine-readable counterpart lives in `service-disclosure/templates/cla.toml`.

## When to use this template

Use this template when:

- An open-source project in `pointsav-monorepo` accepts external contributions and needs a contribution framework.
- A contributor's rights need to be explicit to satisfy a downstream licensing requirement.
- A governance review of an existing CLA is needed for comparison against the canonical text.

The canonical CLA text is maintained by `factory-release-engineering`. Do not draft a CLA for execution without routing it through [[style-guide-policy|governance review]].

## Structure

The template requires a header block and five sections:

**Header block** (before any heading):

```
Agreement:   Contributor License Agreement — <project name>
Contributor: <full legal name or entity name>
```

| Section | Purpose |
|---|---|
| **Definitions** | Three defined terms: Contribution (what the contributor submits), Project (what they contribute to), Contributor (who is agreeing). Defined exactly once. |
| **Grant of copyright license** | The specific copyright rights the Contributor grants the Project. Minimum: reproduce, prepare derivative works, publicly display, publicly perform, distribute. |
| **Grant of patent license** | Any patent rights the Contributor holds that are necessarily infringed by their Contribution, granted to the Project. Must include a defensive-termination clause: if the Contributor initiates patent litigation against the Project based on the Contribution, the patent license terminates. |
| **Representations** | The Contributor's representations that they have the right to make the Contribution — original authorship, employer consent where applicable, no conflicting agreements. Must be concrete, not vague ("I believe I have the right" is not sufficient). |
| **Scope** | What the agreement covers and what it explicitly does not — for example, that the Contributor retains copyright; that the agreement does not transfer moral rights in jurisdictions where these are inalienable. |

## Register and tone

Legal-plain. Defined terms are capitalised. Active voice where possible. Representations must be stated precisely — vague claims reduce enforceability and create ambiguity about what the Contributor actually represents.

## See also

- [[style-guide-contract|Style Guide — Contract]]
- [[style-guide-license-explainer|Style Guide — License Explainer]]
- [[style-guide-terms|Style Guide — Terms of Use]]
- [[language-protocol-substrate|Language Protocol Substrate]]
