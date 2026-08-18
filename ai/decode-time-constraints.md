---
schema: foundry-doc-v1
title: "Decode-time constraints"
slug: decode-time-constraints
category: ai
type: topic
content_type: topic
quality: complete
index_group: the-doorman-boundary
short_description: "The constrained-decoding technique, and a clear line between it and what PointSav has built today: an advisory post-generation linter, with the grammar-based mechanism itself planned, not shipped."
status: active
bcsc_class: public-disclosure-safe
forward_looking: true
last_edited: 2026-08-17
editor: pointsav-engineering
cites:
 - ni-51-102
 - llguidance
 - llm-structured-output-2026
 - vllm-multi-lora
 - xgrammar
 - olmo3-allenai
paired_with: decode-time-constraints.es.md

---


> Decode-time constraints are structural rules applied to a language model's output at each token-emission step, making banned vocabulary or structurally invalid responses mathematically impossible to produce rather than catching them after the fact. This is a real, established technique. What PointSav has built toward it for editorial vocabulary enforcement today is narrower: an advisory linter that runs after generation.

**Decode-time constraints**, as a technique, are structural rules a runtime enforces at the moment a language model emits each token, not after the response is finished. When a rule says "no banned-vocabulary words" or "must produce valid JSON", the runtime makes the violating token mathematically impossible — the model picks from the remaining valid tokens. The constraint takes the form of a context-free grammar (CFG) or finite-state automaton; the runtime computes — token by token — which next-token candidates would still satisfy the grammar, and zeros out the probability of all others. This technique is called constrained decoding, structured generation, or grammar-guided generation, and is well established in the literature: Microsoft Research's `[llguidance]` library, Carnegie Mellon's `[xgrammar]`, vLLM's structured outputs `[vllm-multi-lora]`, and a growing body of literature on `[llm-structured-output-2026]`.

## What's live today

Editorial vocabulary enforcement on this platform does not use decode-time constraints. The current mechanism is an advisory word list checked by a linter that runs after generation, not during it; no commit is ever blocked on a hit, and violations are logged as warnings for editorial review.

Production Tier A inference rejects grammar-constrained decoding outright and escalates to Tier B instead of enforcing one — the local runtime does not support it. `llguidance` is used elsewhere on the platform, at the Doorman's HTTP request boundary, to validate arbitrary caller-supplied grammar syntax — an input-validation step, unrelated to banned-vocabulary enforcement.

## The full mechanism, planned

Everything below this point describes a design — coherent and buildable, consistent with the general technique above — not a shipped system. Every present-tense verb in this section describes something planned or intended, not a current capability.

**The intended mechanism.** A grammar declares which vocabulary is disallowed; the runtime would make the violating token unreachable rather than catching it after the fact. The grammar would compose in three layers: a **base grammar** (universal banned-vocabulary rules for every tenant and genre), a **tenant grammar** (per-customer extensions — brand-specific Do-Not-Use words, citation-density rules, prohibited claim patterns, authored locally by the tenant), and a **genre grammar** (per-genre structural rules — a TOPIC needing a lead paragraph, a GUIDE needing numbered steps, a regulatory disclosure needing specific citation fields). At request time the [[doorman-protocol|Doorman]] would compose the three layers and run decoding with the composed constraint active.

**Why this would matter if built.** The editorial path would become structurally auditable rather than relying on after-the-fact review: a TOPIC could not contain a banned-vocab term because the grammar refused to emit one; a tenant's forbidden terms could not appear in that tenant's output; a required citation pattern could not be silently omitted. This is the shape of enforcement the [[compounding-substrate|Compounding Substrate]]'s federated-compounding property would eventually depend on, to keep one tenant's vocabulary violations from propagating into a shared base model — but that dependency is itself forward-looking, not a description of how federated training works today.

## Why this design, if built, would be structurally hard for hyperscaler-managed AI to match

Three reasons, each conditional on the design above actually being built — not a claim about a live capability:

**1. The grammar would need to be authored locally.** A constraint living at decode time runs inside the inference loop; authoring a grammar specific to a tenant's editorial standards requires write access to the grammar file the runtime loads. Hyperscaler-managed AI products treat the grammar as part of the closed model deployment — tenants get structured-output modes, not a tenant-specific grammar loaded at inference time.

**2. The constraint would need to compose with adapter routing.** The Doorman already routes among three compute tiers (see [[doorman-protocol]]); a decode-time constraint would need to travel with whatever adapter composition serves a given request. Hyperscaler-managed AI does not expose adapter composition primitives, let alone constraint composition — this reason holds regardless of whether the grammar layer itself is built yet.

**3. The constraint would need to be auditable.** Per `[ni-51-102]` continuous-disclosure language, every editorial output should be traceable to the rules it was generated under. Today's audit ledger (see [[doorman-protocol]]) does not carry a grammar-version or response-hash field.

## Forward-Looking

Per `[ni-51-102]` continuous-disclosure language, this platform describes the grammar-based mechanism as `planned` and `intended`, not built. In rough dependency order:

- A real base grammar (universal banned-vocabulary rules), replacing today's advisory linter.
- Per-genre grammar fragments — no genre-template directory exists yet to attach them to.
- Per-tenant banned-vocab extensions (for example, a customer's brand-specific Do-Not-Use words).
- Live adapter composition with grammar composition through the Doorman.
- Audit-ledger entries recording `grammar_version` + `adapter_composition` + `response_hash` per request — today's ledger schema has none of these fields (see [[doorman-protocol]]).

## See also

- [[compounding-substrate]]
- [[language-protocol-substrate]]
- [[apprenticeship-substrate]]
- [[sovereign-ai-routing]]
- [[worm-ledger-architecture]]
