---
title: "Anti-Homogenization Discipline"
slug: topic-anti-homogenization-discipline
category: architecture
status: pre-build
last_edited: 2026-04-27
editor: pointsav-engineering
cites:
  - ni-51-102
---

# Anti-Homogenization Discipline

Most AI writing assistants silently coerce their users toward a
single voice. Cornell research (arXiv 2409.11360, 2024) found
that AI suggestions push non-Western writers toward Western
register at higher rates, with smaller productivity gains because
the writers spend additional time correcting the AI's drift away
from their authentic voice. Foundry's anti-homogenization
discipline is the architectural posture that resists this drift
explicitly.

## The problem in concrete terms

A writing assistant trained centrally on a homogeneous corpus
will, on average, suggest edits that move text toward that
corpus's centroid. For users whose voice already sits at the
centroid, the AI is helpful. For users whose voice does not,
the AI is a constant force pulling them toward someone else's
voice — usually the voice of the speaker with the largest
training-data presence.

The Cornell finding is concrete: writers from non-Western
contexts spent more time editing AI suggestions back toward
their original voice than they saved by accepting suggestions.
Net productivity for those users was lower. The AI was not
neutral; it was actively counter-productive.

The same dynamic operates across organisations. A Foundry-
hosted writing assistant fine-tuned on a generic corpus will
push every customer's voice toward that corpus's centroid. A
distinctive corporate voice — terse, formal, region-specific,
trade-specific — will erode under continuous use.

## The discipline — flag, don't rewrite

Foundry's default editorial action is `flag`, not `rewrite`.
When the assistant identifies a potential issue, it surfaces
the issue and proposes an edit; it does not silently rewrite
the user's text. The user's voice is the authority unless the
user explicitly delegates a rewrite.

This default applies across every editorial task-type:

- `prose-edit` — flag banned vocabulary, register drift,
  citation gaps; do not rewrite.
- `register-tighten` — propose tightenings; mark them clearly
  as proposals; let the user accept individually.
- `frontmatter-normalize` — fill in missing fields; never
  silently overwrite a present-but-unconventional value.
- `citation-insert` — propose `[citation-id]` references;
  surface the candidate citation source for verification.

A user who explicitly requests "rewrite this in Bloomberg
register" gets a rewrite. The flag-don't-rewrite default does
not block delegation; it requires the delegation to be
explicit.

## Per-tenant adapters preserve voice

Foundry's adapter-composition algebra (Doctrine claim #22)
separates the per-tenant adapter from the protocol adapter.
The per-tenant adapter trains on the customer's own corpus
inside the customer's own substrate. It learns the customer's
voice — what words they use, what sentence rhythms they
favour, what register they default to.

When the protocol adapter (PROSE / COMMS / LEGAL / TRANSLATE)
composes with the per-tenant adapter at request time, the
output reflects both: the genre conventions of the protocol
and the voice of the tenant. A README authored by Foundry
inside Customer A's substrate sounds like Customer A; the same
README authored by Foundry inside Customer B's substrate
sounds like Customer B.

This is the Writer Brand IQ pattern adapted to customer
sovereignty. Writer.com established that brand-voice adapters
work; Foundry establishes that they work without the
customer's text leaving the customer's substrate.

## Forward-looking — federated voice preservation

Per `[ni-51-102]` continuous-disclosure language, the
trajectory toward federated voice preservation is forward-
looking. The current state: per-tenant adapters live in the
customer's substrate and never leave. The planned trajectory:
aggregated improvements may feed back to a shared base model
when the customer chooses to contribute, under explicit
consent, with no leakage of corpus contents either direction.

A customer who does not contribute continues to benefit from
base-model improvements driven by customers who do. A customer
who does contribute receives the base-model improvements
without sacrificing their voice — the per-tenant adapter
continues to differentiate them.

## What anti-homogenization is not

It is not a refusal to suggest improvements. The discipline is
the opposite of inertia — every editorial action produces a
verdict-signed training tuple that improves the per-tenant
adapter over time. The customer's voice is preserved, not
frozen.

It is not a rejection of standardisation. Foundry's banned-
vocabulary list, sentence-length budgets, and register
parameters are standardised across all tenants because the
absence of `leverage` and `seamless` is universally an
improvement. Standardisation operates at the level of
mechanical defects (verbal tics, marketing diction); voice
operates at the level above that.

It is not a passive posture. The discipline is active —
flag-don't-rewrite requires the assistant to surface what it
sees rather than silently smoothing it over. A passive
assistant that accepts every input as-is teaches no voice and
preserves no voice.

## Operational tests

A new editorial feature satisfies the anti-homogenization
discipline if:

1. Every automated edit is surfaced as a proposal, not a
   silent rewrite, unless the user has explicitly delegated
   rewriting.
2. The per-tenant adapter is loaded at request time and
   composed with the protocol adapter rather than bypassed.
3. The training pipeline produces verdict-signed tuples that
   feed continued pretraining on the customer's adapter, not
   on a shared adapter.
4. The customer can audit which adapters were active for any
   editorial action — by reading the adapter-composition log
   in the apprenticeship corpus.

## See also

- [The Language-Protocol Substrate](topic-language-protocol-substrate.md)
- [Customer Hostability](topic-customer-hostability.md)
- The Cornell study: AI suggestions and non-Western writers,
  arXiv 2409.11360 (2024) — referenced in
  `~/Foundry/conventions/language-protocol-substrate.md` §1.
- The convention this article reflects:
  `~/Foundry/conventions/language-protocol-substrate.md` §2
