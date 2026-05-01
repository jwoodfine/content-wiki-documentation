---
schema: foundry-doc-v1
title: "Decode-Time Constraints"
slug: topic-decode-time-constraints
category: architecture
type: topic
quality: complete
short_description: "Decode-time constraints are structural rules applied to a language model's output at each token-emission step, making banned vocabulary or structurally invalid responses mathematically impossible to produce rather than catching them after the fact."
status: pre-build
last_edited: 2026-04-30
editor: pointsav-engineering
cites:
  - ni-51-102
  - llguidance
  - llm-structured-output-2026
  - vllm-multi-lora
  - xgrammar
  - olmo3-allenai
paired_with: topic-decode-time-constraints.es.md
---

# Decode-Time Constraints

> Decode-time constraints are structural rules applied to a language model's output at each token-emission step, making banned vocabulary or structurally invalid responses mathematically impossible to produce rather than catching them after the fact.

**Decode-time constraints** are structural rules the PointSav substrate enforces at the moment a language model emits each token, not after the response is finished. When a rule says "no banned-vocabulary words" or "must produce valid JSON", the runtime makes the violating token mathematically impossible — the model picks from the remaining valid tokens. This is the difference between a human grading work after submission and a guard rail that prevents the violation from happening at emission. The constraint takes the form of a context-free grammar (CFG) or finite-state automaton; the runtime computes — token by token — which next-token candidates would still satisfy the grammar, and zeros out the probability of all others.

This technique is called constrained decoding, structured generation, or grammar-guided generation. Implementations include Microsoft Research's `[llguidance]` library, Carnegie Mellon's `[xgrammar]`, vLLM's structured outputs `[vllm-multi-lora]`, and a growing body of literature on `[llm-structured-output-2026]`.

## Overview

The artefact a content session holds in their head: a `.lark` grammar file says what a valid response looks like. The runtime makes invalid tokens unreachable. There is no "but what if the model emits a banned word" — the banned word literally cannot be sampled.

The substrate ships `service-content/schemas/banned-vocab.lark` — a Lark EBNF grammar declaring eight banned editorial terms (`leverage`, `empower`, `next-generation`, `industry-leading`, `seamless`, `robust`, `cutting-edge`, `world-class`) plus a backtick-quoted-escape rule. The grammar's top-level rule `response` allows any token that is not one of the eight banned forms (case-insensitive); backtick-quoted segments are exempt so that documents can quote a banned term without violating the rule.

## How It Works

Production inference at Tier A (local OLMo 3 7B per `[olmo3-allenai]`) and Tier B (Yo-Yo bursting) loads the grammar via `[llguidance]` and applies it at decode time. Editorial-grade workspace validation (`validate.py`) runs the same grammar in Lark mode for offline checks before content ships.

The pattern composes with the language-protocol-substrate: each genre template (TOPIC, GUIDE, README, contract, policy, and the rest) ships a per-genre grammar fragment. At inference time, the active grammar is `base-grammar ⊕ tenant-grammar ⊕ genre-grammar` — substrate-tier rules combined with tenant-tier customisations combined with the request's genre.

## Architecture

The constraint system is layered:

1. **Base grammar** — universal banned-vocabulary rules applying to every tenant and every genre.
2. **Tenant grammar** — per-customer extensions (brand-specific Do-Not-Use words, required citation density rules, prohibited claim patterns). Authored locally by the tenant and loaded by the Doorman.
3. **Genre grammar** — per-genre structural rules (a TOPIC must have a lead paragraph; a GUIDE must have numbered steps; a regulatory disclosure must carry specific citation fields).

At request time, the Doorman (`service-slm`) composes the three grammar layers, loads the result into the inference runtime, and runs decoding with the composed constraint active.

## Applications

The editorial path becomes structurally auditable:

- A TOPIC committed to a content-wiki repo cannot contain a banned-vocab term — the grammar refused to emit one.
- A GUIDE rendered for a customer cannot contain forbidden tenant-specific terms — that tenant's grammar forbade them.
- A regulatory disclosure draft cannot omit a required citation pattern — the grammar required it.

The discipline shifts from human-grading-after-submission to runtime-impossibility-at-emission. This is the substrate enforcement layer the Compounding Substrate's federated-compounding property depends on; without it, federated training would propagate banned-vocabulary contamination from any tenant's training data into the next year's base model.

## Limitations

Three structural reasons hyperscaler-managed AI cannot match this approach:

**1. The grammar must be authored locally.** A constraint that lives at decode time runs inside the inference loop. To author a grammar specific to a tenant's editorial standards, the tenant needs write access to the grammar file the runtime loads. Hyperscaler-managed AI products treat the grammar as part of the closed model deployment — tenants get structured-output modes, not a tenant-specific grammar that loads at inference time.

**2. The constraint must compose with adapter routing.** Foundry's Doorman routes among three compute tiers and composes adapters per request. Decode-time constraints must travel with the adapter composition. Hyperscaler-managed AI does not expose adapter composition primitives, let alone constraint composition.

**3. The constraint must be auditable.** Per `[ni-51-102]` continuous-disclosure language, every editorial output must be traceable to the rules it was generated under. Foundry's per-tenant audit ledger captures the grammar version, the adapter composition, and the response — together. Hyperscaler-managed AI offers neither the grammar version nor the adapter composition for inspection.

## Forward-Looking

Per `[ni-51-102]` continuous-disclosure language, the trajectory below is `planned` and `intended`:

- Per-genre grammars for the 16 genre templates currently in `service-disclosure/templates/` (Phase 1B grammar covers the universal banned-vocab; per-genre grammars are subsequent work).
- Per-tenant banned-vocab extensions (for example, a customer's brand-specific Do-Not-Use words).
- Live adapter composition with grammar composition through `service-slm`'s Doorman.
- Audit-ledger entries recording `grammar_version + adapter_composition + response_hash` per request.

## See Also

- [[compounding-substrate]]
- [[language-protocol-substrate]]
- [[apprenticeship-substrate]]
- [[sovereign-ai-routing]]
- [[worm-ledger-architecture]]

## References

- `conventions/language-protocol-substrate.md §3` — CFG enforcement within the language-protocol model
- `pointsav-monorepo/service-content/schemas/banned-vocab.lark` — the banned-vocabulary grammar
- `pointsav-monorepo/service-content/schemas/validate.py` — offline validation harness
- `conventions/compounding-substrate.md` — federated-compounding property that depends on this enforcement layer

---
Copyright © 2026 Woodfine Capital Projects Inc.
Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).
PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.