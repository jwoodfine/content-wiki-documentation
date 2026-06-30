---
schema: foundry-doc-v1
title: "TUI as corpus producer"
slug: tui-corpus-producer
category: substrate
type: topic
content_type: topic
quality: complete
short_description: "Every terminal interaction with service-slm through the operator TUI is a curated training corpus contribution for the per-tenant adapter."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-15
editor: pointsav-engineering
cites: []
references:
  - id: 1
    text: "Rafailov, R. et al. 'Direct Preference Optimization: Your Language Model is Secretly a Reward Model.' NeurIPS, 2023."
    url: "https://arxiv.org/abs/2305.18290"
  - id: 2
    text: "Zhou, C. et al. 'LIMA: Less Is More for Alignment.' NeurIPS, 2023."
    url: "https://arxiv.org/abs/2305.11206"
paired_with: tui-corpus-producer.es.md
---

The **TUI-as-Corpus-Producer** pattern designates the operator terminal interface (`slm-cli`) as a primary source of high-quality training data for the per-tenant model [[adapter-composition|adapter]]. Every interaction with the [[compounding-doorman|Doorman]] through this interface is a curated corpus contribution.

## Why terminal interactions are high-quality training data

Three properties distinguish system administration and IT-support interactions from general training data:

**Verifiable ground truth.** When an operator follows AI advice — running a suggested command, applying a proposed configuration change — the system either recovers or it does not. Other domains such as creative writing or strategic reasoning lack this immediate-feedback property. IT-support has it by default. The operator knows immediately whether the response was correct.

**Narrow domain.** Archive operations, system conventions, and customer-specific workflow vocabulary form a bounded command set and failure-mode space. Models train more efficiently on bounded domains than on general corpora because the signal-to-noise ratio is higher.

**Domain-expert feedback.** The operator issuing a verdict is the person who knows whether the response was correct — not a proxy labeler separated from the actual work. Published reinforcement-learning-from-human-feedback literature consistently reports that high-quality verdict-signed interaction tuples train an order of magnitude more efficiently than observation-only tuples. [^1]

## The /feedback mechanism

After every assistant response in the TUI, the operator is offered three explicit verdicts:

**Good.** The response was correct and useful. The tuple is flagged as a positive direct preference optimisation example.

**Refine.** The response was close but needed adjustment. The operator provides a correction inline; the tuple captures the response-and-refinement pair as training signal.

**Bad.** The response was wrong. The tuple is flagged as a negative direct preference optimisation example.

If the operator dismisses without providing a verdict, the tuple is captured as unsigned and contributes to supervised fine-tuning but not to direct preference optimisation.

## Adapter quality budget

Published fine-tuning literature suggests 200 to 500 high-quality verdict-signed interactions are sufficient for a first adapter training cycle in a narrow domain. [^2] The platform's intended sequence for each tenant is: accumulate signed interactions from dogfood operations, train the first per-tenant adapter via the [[yo-yo-lora-training-pipeline|LoRA training pipeline]], apply a validation quality gate, and promote the adapter to the deployment. Each subsequent training cycle incorporates additional interactions, progressively tuning the adapter to the customer's specific environment — their systemd units, their [[seed-taxonomy-as-smb-bootstrap|seed taxonomy]], their workflow vocabulary.

## Per-tenant adapter ownership

The corpus produced by a customer's operators trains that customer's adapter, not a general adapter. Per the [[customer-owned-graph-ip]] convention, the trained adapter weights are the customer's property. The platform distributes the model architecture and the training pipeline; the customer retains the trained adapter that results.

## Verdict capture discipline

Some terminal sessions should not contribute to the training corpus: test sessions initiated with a no-corpus flag, sessions interrupted by unavailable tiers before completion, and sessions using forced-tier debug mode are [[worm-ledger-architecture|audit-logged]] but excluded from normal training data. The boundary between operational corpus and test corpus is enforced at the [[compounding-doorman|Doorman's]] verdict intake endpoint.

## See also

- [[single-boundary-compute-discipline]] — the TUI never calls inference tiers directly; all calls route through the Doorman
- [[customer-owned-graph-ip]] — per-tenant adapter weights are the customer's intellectual property
- [[knowledge-graph-grounded-apprenticeship]] — training tuples carry graph context when the Doorman grounds the request

