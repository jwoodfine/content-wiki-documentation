---
schema: foundry-doc-v1
title: "LLM Substrate Decision — OLMo 3 Family"
slug: llm-substrate-decision
category: architecture
type: topic
quality: published
short_description: "The rationale for selecting OLMo 3 as the local and GPU-burst language model substrate: the only fully open model family — training data, training code, and checkpoints included — that permits continued pretraining and satisfies a Canadian public-company procurement posture."
status: pre-build
last_edited: 2026-05-01
editor: pointsav-engineering
cites: []
paired_with: llm-substrate-decision.es.md
---

The PointSav platform uses the OLMo 3 model family as its language model substrate. OLMo 3 7B runs locally on customer hardware. OLMo 3.1 32B Think runs on a short-lived GPU burst instance for heavier inference tasks. The selection is not primarily about benchmark performance — it is about ownership depth.

## Three levels of openness

The language model market in 2026 offers three distinct depths of openness, and the distinction matters for any organisation planning a five-year compounding trajectory.

**Level 1 — Open weights.** The model's trained parameter files are published. You can run inference and perform LoRA fine-tuning. You cannot inspect the training data, reproduce the training run, or continue pretraining the model from a known checkpoint. Most widely-discussed open models operate at this level.

**Level 2 — Open weights with a permissive license.** Same as Level 1, with a license clean enough to include in a commercial product. This is the level that makes a model usable in a shipped product without legal exposure.

**Level 3 — Fully open model.** Training data, training code, and checkpoints at every stage of training are published, alongside the weights and a permissive license. At this level you can continue pretraining — starting from a known checkpoint, on your own corpus, to produce a derivative model that your organisation subsequently owns.

OLMo 3 is the only model in the 2026 non-Chinese open model landscape that operates at Level 3. Its training data is the Dolma 3 corpus (9.3 trillion tokens, published under the Open Data Commons license). Its training code is published under Apache 2.0. Checkpoints at intermediate stages are available for download.

For a platform designed to compound over a five-year horizon — where the intended outcome is a customer-owned, specialised base model trained on accumulated customer data — Level 3 is the only depth that makes that outcome possible. Level 1 and Level 2 produce fine-tuning capability but not ownership of the base.

## Why each alternative was set aside

Models considered and rejected:

**Phi-4 (Microsoft).** MIT license on the weights; training data closed and Microsoft-proprietary. Fine-tuning is possible; continued pretraining is not, because the training data necessary to reproduce or extend the base is not published.

**Granite 4 (IBM).** Apache 2.0 license on the weights; training data is a closed IBM-proprietary corpus. Same constraint as Phi-4.

**Llama 4 (Meta).** The Llama Community License is not OSI-approved and includes restrictions on commercial use above a user threshold. The license constraint disqualifies it independently of the training data question.

**Mistral 7B.** Apache 2.0 license; training data partially documented but no full open release. Older architecture; weaker on code than 2026 alternatives.

**Chinese-origin models (Qwen, DeepSeek, and related).** Technically capable and in several cases released under MIT or Apache 2.0. The procurement constraint for a Canadian public company is the disqualifying factor: US National Defense Authorization Act precedent from fiscal year 2026 creates regulatory exposure for Canadian public companies incorporating Chinese-origin model infrastructure, regardless of license terms.

## Capability

OLMo 3 32B Think, in the updated OLMo 3.1 December 2025 release, reaches 91.4% on HumanEvalPlus — the measure of practical code generation accuracy — and sits within two percentage points of the leading open-weight model on the standard mathematical reasoning and instruction-following benchmarks. The 7B variant is strong on programming, reading comprehension, and mathematics with a 65,000-token context window.

These numbers do not place OLMo 3 at the absolute frontier of open-weight performance. They do place it firmly in the range where the Doorman — the service that mediates all AI inference calls in the PointSav architecture — produces useful results on the daily tasks it handles. The 7B local variant handles routine work; the 32B burst variant handles tasks requiring extended reasoning. The same vocabulary, tokenizer, and prompt format apply to both, which means the adapter library trained on one is compatible with the other.

## The three compute tiers

The Doorman routes requests among three tiers:

**Tier A — local.** OLMo 3 7B running on the customer's own hardware. Approximately zero marginal cost once the hardware is in place. Default for most operations.

**Tier B — GPU burst.** OLMo 3.1 32B Think on a short-lived GPU instance. Approximately $0.84 per hour at list pricing on major cloud providers, significantly less on spot/preemptible instances. Used for requests the local tier cannot handle efficiently. Idle-shutdown discipline means the instance runs only when a request requires it.

**Tier C — external API.** Third-party language model services via a per-request allowlist. Used only for narrow precision tasks — citation grounding, initial knowledge graph construction, entity disambiguation — where the precision requirement justifies the cost. Every Tier C call is logged at the customer's audit ledger.

The customer's routing configuration determines which tier handles which request. No per-request manual selection is required.

## The intended continued-pretraining path

The platform's intended multi-year trajectory, as currently planned, is to move from using OLMo 3 as a base through a process of continued pretraining that produces PointSav-OLMo-N — a derivative model trained on accumulated Foundry corpus data, customer LoRA adapter distillation, and curated public material. Year two onwards is the intended start window for the first continued-pretraining run, targeting the 7B variant at an estimated cost of $30,000 to $100,000 on cloud GPU infrastructure. This trajectory is planned but not yet initiated; the current platform operates on the published OLMo 3 base.

The material assumption underlying this trajectory is that the Open Data Commons license on Dolma 3 and the Apache 2.0 license on OLMo 3's training code remain in effect and permit commercial continued pretraining. That assumption holds as of May 2026; it would require re-evaluation if the license terms changed.

## See Also

- [[four-tier-slm-substrate]] — the four deployment tiers built on this substrate
- [[apprenticeship-substrate]] — how continued pretraining signal is generated from production work
- [[trajectory-substrate]] — the corpus capture mechanism that feeds continued pretraining
- [[compounding-doorman]] — the service that routes all inference calls across the three compute tiers

## References

1. AllenAI OLMo 3 announcement and technical report — <https://allenai.org/blog/olmo3>
2. Dolma 3 dataset, Open Data Commons license — <https://huggingface.co/datasets/allenai/dolma>
3. OLMo 3.1 release notes (December 2025) — AllenAI engineering blog.
4. `conventions/llm-substrate-decision.md` — source convention for this article.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
