---
schema: foundry-doc-v1
title: "TUI as Corpus Producer"
slug: tui-corpus-producer
category: architecture
type: topic
quality: published
short_description: "Every terminal interaction with service-slm through the operator TUI is a curated training corpus contribution for the per-tenant adapter."
status: pre-build
last_edited: 2026-05-01
editor: pointsav-engineering
cites: []
paired_with: tui-corpus-producer.es.md
---

The **TUI-as-Corpus-Producer** pattern designates the operator terminal interface (`slm-cli`) as a primary source of high-quality training data for the per-tenant model adapter. Every interaction with the Doorman through this interface is a curated corpus contribution. The pattern encodes Doctrine claim #45.

## Why terminal interactions are high-quality training data

Three properties distinguish system administration and IT-support interactions from general training data:

**Verifiable ground truth.** When an operator follows AI advice — running a suggested command, applying a proposed configuration change — the system either recovers or it does not. Other domains such as creative writing or strategic reasoning lack this immediate-feedback property. IT-support has it by default. The operator knows immediately whether the response was correct.

**Narrow domain.** Archive operations, system conventions, and customer-specific workflow vocabulary form a bounded command set and failure-mode space. Models train more efficiently on bounded domains than on general corpora because the signal-to-noise ratio is higher.

**Domain-expert feedback.** The operator issuing a verdict is the person who knows whether the response was correct — not a proxy labeler separated from the actual work. Published reinforcement-learning-from-human-feedback literature consistently reports that high-quality verdict-signed interaction tuples train an order of magnitude more efficiently than observation-only tuples.

## The /feedback mechanism

After every assistant response in the TUI, the operator is offered three explicit verdicts:

**Good.** The response was correct and useful. The tuple is flagged as a positive direct preference optimisation example.

**Refine.** The response was close but needed adjustment. The operator provides a correction inline; the tuple captures the response-and-refinement pair as training signal.

**Bad.** The response was wrong. The tuple is flagged as a negative direct preference optimisation example.

If the operator dismisses without providing a verdict, the tuple is captured as unsigned and contributes to supervised fine-tuning but not to direct preference optimisation.

## Adapter quality budget

Published fine-tuning literature suggests 200 to 500 high-quality verdict-signed interactions are sufficient for a first adapter training cycle in a narrow domain. Foundry's intended sequence for each tenant is: accumulate signed interactions from dogfood operations, train the first per-tenant adapter, apply a validation quality gate, and promote the adapter to the deployment. Each subsequent training cycle incorporates additional interactions, progressively tuning the adapter to the customer's specific environment — their systemd units, their seed taxonomy, their workflow vocabulary.

## Per-tenant adapter ownership

The corpus produced by a customer's operators trains that customer's adapter, not a general adapter. Per the [[customer-owned-graph-ip]] convention, the trained adapter weights are the customer's property. Foundry distributes the model architecture and the training pipeline; the customer retains the trained adapter that results.

## Verdict capture discipline

Some terminal sessions should not contribute to the training corpus: test sessions initiated with a no-corpus flag, sessions interrupted by unavailable tiers before completion, and sessions using forced-tier debug mode are audit-logged but excluded from normal training data. The boundary between operational corpus and test corpus is enforced at the Doorman's verdict intake endpoint.

## See Also

- [[single-boundary-compute-discipline]] — the TUI never calls inference tiers directly; all calls route through the Doorman
- [[customer-owned-graph-ip]] — per-tenant adapter weights are the customer's intellectual property
- [[knowledge-graph-grounded-apprenticeship]] — training tuples carry graph context when the Doorman grounds the request

## References

1. Doctrine claim #45 — TUI-as-Corpus-Producer (ratified v0.1.0).
2. `conventions/apprenticeship-substrate.md` §7D — TUI extension to the apprenticeship substrate.
3. Published OLMo 2 fine-tuning literature on quality-over-volume for narrow-domain adapters.

---

## Provenance

Source: `convention-tui-corpus-producer.md` (refined 2026-04-30). Workspace-internal file paths, implementation scaffolding details, and open questions removed. BCSC forward-looking framing applied to adapter training schedule claims (described as intended targets, not guarantees).

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
