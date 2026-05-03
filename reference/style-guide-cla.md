---
schema: foundry-doc-v1
title: "Style Guide — Contributor License Agreement"
slug: style-guide-cla
category: reference
type: topic
quality: core
short_description: "Editorial standards for Contributor License Agreements produced through the Foundry language-protocol stack, covering the LEGAL family routing rules, required sections, the bilingual-pair requirement, and the mandatory legal-review disclaimer."
status: pre-build
last_edited: 2026-04-30
editor: pointsav-engineering
cites: []
paired_with: style-guide-cla.es.md
---

> A Contributor License Agreement is a public-facing legal instrument that defines the rights a contributor grants when submitting work — every draft carries a "DRAFT — for legal review" header and is never a substitute for counsel.

A **Contributor License Agreement** (CLA) is a legal document
that specifies the intellectual-property rights a contributor
grants to the project when they submit code, documentation, or
other contributions. In the Foundry language-protocol stack it
belongs to the LEGAL family and routes to Tier C (an external
API such as Claude or GPT) by default, because local SLM models
lack the legal corpus required to draft reliable legal text.
The machine-readable counterpart lives in
`service-disclosure/templates/cla.toml`.

## When to use this template

Use the CLA template when producing or revising a CLA for a
Foundry-affiliated repository. The template applies when:

- A new engineering repository needs a CLA for external
  contributors.
- An existing CLA is being reviewed and improved.
- A bilingual pair is being generated for an existing
  English-only CLA.

The `default_routing = "tier-c"` setting means the Doorman
routes CLA work to a Tier C model unless the operator has
explicitly approved a different route. Local generation in Tier A
or Tier B requires explicit operator approval and is appropriate
only when the operator has a legal corpus large enough to ground
the output.

Every CLA output carries a visible "DRAFT — for legal review"
header in the document. This discipline is not optional. Removing
the header before the document has received formal legal review
is a posture violation.

## Frontmatter fields

CLAs are legal instruments rather than editorial documents and
do not carry YAML frontmatter. The template parameters that
govern routing are set in the `ProtocolRequest`:

| Field | Notes |
|---|---|
| `tenant` | Required. Identifies the legal entity whose CLA is being produced. |
| `genre_template` | `GenreTemplate::Cla` |
| `register` | `legal` — formal register throughout. |
| `routing` | Defaults to Tier C. Override requires operator approval. |

## Structure

The template requires four sections in this order:

| Section | Purpose |
|---|---|
| **Grant** | The rights the contributor grants — typically a copyright licence and a patent licence. This section is the operative heart of the document. |
| **Representations** | The contributor's warranties about the contribution: that they own it, that they have the right to grant the licence, that the contribution is original. |
| **Disclaimer** | Limitations on the contributor's warranty — what the contributor is not warranting. |
| **Signature** | Contributor identity, date, and mechanism for execution. |

When a base CLA exists (such as the Apache Individual CLA or the
Developer Certificate of Origin), reference it by canonical name
and describe the modifications rather than reproducing the base
in full.

## Register and tone

The register is legal. Sentence-length budget: mean around twenty
words, maximum around thirty-six — legal sentences are
intentionally longer than other families because precision and
completeness matter more than brevity. Passive voice is
acceptable when the subject of the obligation is ambiguous or
where legal convention requires it.

Bilingual pair recommended when the contributor base spans
languages. The English text is the binding instrument; the
Spanish translation is explanatory and carries a note that the
English controls.

The banned-vocabulary list applies. Legal drafting that uses
marketing terms ("seamless", "robust") is weak drafting.

## Example

```markdown
<!-- DRAFT — for legal review -->

## Grant

You ("Contributor") hereby grant to [Project Owner]
("Recipient") a perpetual, worldwide, non-exclusive,
royalty-free, irrevocable copyright licence to reproduce,
prepare derivative works of, publicly display, and distribute
your Contributions.

## Representations

You represent that each Contribution is your original creation
and that you have the legal right to grant the above licence.

## Disclaimer

Except as expressly stated, you provide your Contributions
"AS IS", without warranty of any kind.

## Signature

Contributor name: ____________________  Date: __________
```

## See also

- [[style-guide-contract|Style Guide — Contract]]
- [[language-protocol-substrate|Language Protocol Substrate]]
- [[canadian-simple-copyright|Canadian Simple Copyright]]

## References
