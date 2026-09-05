---
schema: foundry-doc-v1
title: "Anti-homogenization discipline"
slug: anti-homogenization-discipline
category: governance
type: topic
content_type: topic
quality: complete
index_group: platform-disciplines
short_description: "Anti-homogenization discipline resists AI writing assistants pulling contributors toward a single voice, by flagging potential issues rather than silently rewriting text."
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-04-30
editor: pointsav-engineering
cites:
 - ni-51-102
paired_with: anti-homogenization-discipline.es.md
---


> Anti-homogenization discipline is the architectural posture that resists AI writing assistants pulling contributors toward a single voice, by defaulting to flagging potential issues rather than silently rewriting text.

Most AI writing assistants silently coerce their users toward a single voice. Cornell research (arXiv 2409.11360, 2024) found that AI suggestions push non-Western writers toward Western register at higher rates, with smaller productivity gains because the writers spend additional time correcting the AI's drift away from their authentic voice. **Anti-homogenization discipline** is the architectural posture that resists this drift explicitly, operating alongside the [[language-protocol-substrate]] that governs editorial task routing.

A writing assistant trained centrally on a homogeneous corpus will, on average, suggest edits that move text toward that corpus's centroid. For users whose voice already sits at the centroid, the assistant is helpful. For users whose voice does not, the assistant is a constant force pulling them toward someone else's voice — usually the voice of the speaker with the largest training-data presence.

## The problem in concrete terms

The Cornell finding is concrete: writers from non-Western contexts spent more time editing AI suggestions back toward their original voice than they saved by accepting suggestions. Net productivity for those users was lower. The assistant was not neutral; it was actively counter-productive.

The same dynamic operates across organisations. A platform-hosted writing assistant fine-tuned on a generic corpus will push every customer's voice toward that corpus's centroid. A distinctive corporate voice — terse, formal, region-specific, trade-specific — will erode under continuous use.

## Flag, not rewrite

The platform's default editorial action is `flag`, not `rewrite`. When the assistant identifies a potential issue, it surfaces the issue and proposes an edit; it does not silently rewrite the user's text. The user's voice is the authority unless the user explicitly delegates a rewrite.

This default applies across every audit-logged editorial event type — `prose-edit`, `design-edit`, `graph-mutation`, `anchor-event`, and `verdict-issued`: the assistant flags banned vocabulary, register drift, or a proposed change and lets the contributor accept or reject it, rather than applying it silently.

A user who explicitly requests "rewrite this in institutional register" gets a rewrite. The flag-don't-rewrite default does not block delegation; it requires the delegation to be explicit.

## Per-tenant adapters preserve voice

The platform's adapter-composition design separates the per-tenant adapter from the protocol adapter. The per-tenant adapter trains on the customer's own corpus inside the customer's own [[totebox-os|substrate]]. It learns the customer's voice — the words they use, the sentence rhythms they favour, the register they default to.

The intended mechanism: when the protocol adapter (PROSE / COMMS / LEGAL / TRANSLATE) composes with the per-tenant adapter at request time, the output reflects both — the genre conventions of the protocol and the voice of the tenant. Composition itself is not live yet; today it returns a symbolic composed identifier rather than merging adapter weights, pending a runtime capability the platform depends on but does not control the timeline of. A README authored inside Customer A's substrate is designed to sound like Customer A once composition ships; the same README inside Customer B's substrate, like Customer B.

This is the Writer Brand IQ pattern adapted to customer data ownership — brand-voice adapters that work without the customer's text leaving the customer's substrate, once composition is operational.

## Forward-looking — federated voice preservation

Per `[ni-51-102]` continuous-disclosure language, the trajectory toward federated voice preservation is forward-looking. The current state: per-tenant adapters live in the customer's substrate and never leave. The planned trajectory: aggregated improvements may feed back to a shared base model when the customer chooses to contribute, under explicit consent, with no leakage of corpus contents either direction.

A customer who does not contribute continues to benefit from base-model improvements driven by customers who do. A customer who does contribute receives the base-model improvements without sacrificing their voice — the per-tenant adapter continues to differentiate them.

## What anti-homogenization is not

It is not a refusal to suggest improvements. The discipline is the opposite of inertia — every editorial action is designed to produce a verdict-signed training tuple that improves the per-tenant adapter over time. That pipeline captures real activity today; the verdict-signing step itself — a human confirming an edit before it trains the adapter — has not processed a real verdict yet. The customer's voice is preserved, not frozen, once the loop closes end to end.

It is not a rejection of standardisation. The platform's banned-vocabulary list, sentence-length budgets, and register parameters are standardised across all tenants because the absence of `leverage` and `seamless` is universally an improvement. Standardisation operates at the level of mechanical defects; voice operates at the level above that.

It is not a passive posture. The discipline is active — flag-don't-rewrite requires the assistant to surface what it sees rather than silently smoothing it over.

## Operational tests

A new editorial feature satisfies the anti-homogenization discipline if:

1. Every automated edit is surfaced as a proposal, not a silent rewrite, unless the user has explicitly delegated rewriting.
2. The per-tenant adapter is loaded at request time and composed with the protocol adapter rather than bypassed.
3. The training pipeline produces verdict-signed tuples that feed continued pretraining on the customer's adapter, not on a shared adapter.
4. The customer can audit which adapters were active for any editorial action by reading the adapter-composition log in the apprenticeship corpus.

## See also

- [[language-protocol-substrate]]
- [[customer-hostability]]
- [[contributor-model]]
