---
title: "Decode-Time Constraints"
slug: topic-decode-time-constraints
category: architecture
status: pre-build
last_edited: 2026-04-27
editor: pointsav-engineering
cites:
  - ni-51-102
  - llguidance
  - llm-structured-output-2026
  - vllm-multi-lora
  - xgrammar
  - olmo3-allenai
---

The substrate enforces structural rules at the moment the model emits
each token, not after the response is finished. When the rule says "no
banned-vocabulary words" or "must produce valid JSON", the runtime
makes the violating token mathematically impossible — the model picks
from the set of remaining valid tokens. This is the difference between
a human grading work after submission and a guard rail that prevents
the violation from happening in the first place.

## Definition

A decode-time constraint is a structural rule applied to a language
model's output at each token-emission step. The constraint takes the
form of a context-free grammar (CFG) or finite-state automaton; the
runtime computes — token by token — which next-token candidates would
still satisfy the grammar, and zeros out the probability of all
others.

The technique is called constrained decoding, structured generation,
or grammar-guided generation. Implementations include Microsoft
Research's `[llguidance]` library, Carnegie Mellon's `[xgrammar]`,
vLLM's structured outputs `[vllm-multi-lora]`, and a growing body of
literature on `[llm-structured-output-2026]`.

The artefact a content session holds in their head: a `.lark` grammar
file says what a valid response looks like. The runtime makes invalid
tokens unreachable. There is no "but what if the model emits a banned
word" — the banned word literally cannot be sampled.

## How Foundry uses this

The substrate ships `service-content/schemas/banned-vocab.lark` — a
Lark EBNF grammar declaring eight banned editorial terms (`leverage`,
`empower`, `next-generation`, `industry-leading`, `seamless`,
`robust`, `cutting-edge`, `world-class`) plus a backtick-quoted-escape
rule. The grammar's top-level rule `response` allows any token that
is not one of the eight banned forms (case-insensitive); backtick-
quoted segments are exempt so that documents can quote a banned term
without violating the rule.

Production inference at Tier A (local OLMo 3 7B per `[olmo3-allenai]`)
and Tier B (Yo-Yo bursting) loads the grammar via `[llguidance]` and
applies it at decode time. Editorial-grade workspace validation
(`validate.py`) runs the same grammar in Lark mode for offline checks
before content ships.

The pattern composes with the language-protocol-substrate: each genre
template (TOPIC, GUIDE, README, contract, policy, and the rest) ships
a per-genre grammar fragment. At inference time, the active grammar
is `base-grammar ⊕ tenant-grammar ⊕ genre-grammar` — substrate-tier
rules combined with tenant-tier customisations combined with the
request's genre.

## Why hyperscaler-managed AI cannot match this

Three structural reasons.

**1. The grammar must be authored locally.** A constraint that lives
at decode time runs inside the inference loop. To author a grammar
specific to a tenant's editorial standards (banned vocabulary,
required citation density, prohibited claim patterns), the tenant
needs write access to the grammar file the runtime loads.
Hyperscaler-managed AI products treat the grammar as part of the
closed model deployment — tenants get OpenAI's JSON-mode or
Anthropic's structured-output, not "here is your tenant-specific
grammar that loads at inference time."

**2. The constraint must compose with adapter routing.** Foundry's
Doorman (`service-slm`) routes among three compute tiers and composes
adapters per request. Decode-time constraints must travel with the
adapter composition — a TOPIC request with `tenant=woodfine` loads
woodfine's PROSE adapter AND woodfine's banned-vocab grammar AND the
TOPIC genre-grammar. Hyperscaler-managed AI does not expose adapter
composition primitives, let alone constraint composition.

**3. The constraint must be auditable.** Per `[ni-51-102]`
continuous-disclosure language, every editorial output must be
traceable to the rules it was generated under. Foundry's per-tenant
audit ledger captures the grammar version, the adapter composition,
and the response — together. Hyperscaler-managed AI offers neither
the grammar version nor the adapter composition for inspection; the
model is opaque.

## What this enables in Foundry

The Compounding Substrate's editorial path becomes mathematically
auditable:

- A TOPIC committed to a content-wiki repo cannot contain a
  banned-vocab term — the grammar refused to emit one.
- A GUIDE rendered for a Customer cannot contain forbidden tenant-
  specific terms — that tenant's grammar forbade them.
- A regulatory disclosure draft cannot omit a required citation
  pattern — the grammar required it.

The discipline shifts from human-grading-after-submission to
runtime-impossibility-at-emission. This is the substrate enforcement
layer the Compounding Substrate's federated-compounding property
depends on; without it, federated training would propagate banned-
vocabulary contamination from any tenant's training data into the
next year's base model.

## Forward-looking — pending substrate work

Per `[ni-51-102]` continuous-disclosure language, the trajectory
below is `planned` and `intended`:

- Per-genre grammars for the 16 genre templates currently in
  `service-disclosure/templates/` (Phase 1B grammar covers the
  universal banned-vocab; per-genre grammars are subsequent work).
- Per-tenant banned-vocab extensions (e.g., a Customer's brand-
  specific Do-Not-Use words).
- Live adapter composition with grammar composition through
  `service-slm`'s Doorman.
- Audit-ledger entries recording
  `grammar_version + adapter_composition + response_hash` per
  request.

## See also

- [The Compounding Substrate](topic-compounding-substrate.md)
- [The Language-Protocol Substrate](topic-language-protocol-substrate.md)
- [The Apprenticeship Substrate](topic-apprenticeship-substrate.md)
- The convention this article reflects:
  `~/Foundry/conventions/language-protocol-substrate.md` §3 (CFG
  enforcement)
- The grammar:
  `pointsav-monorepo/service-content/schemas/banned-vocab.lark`
- The validation harness:
  `pointsav-monorepo/service-content/schemas/validate.py`
