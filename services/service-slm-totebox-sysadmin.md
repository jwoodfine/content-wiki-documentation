---
schema: foundry-doc-v1
title: "SLM as Totebox sysadmin — the plan"
slug: service-slm-totebox-sysadmin
category: services
type: topic
content_type: topic
quality: complete
index_group: ring-3-ai-gateway
short_description: "A planned direction for service-slm: using its real, already-operational capture-then-verdict training pipeline to build a Totebox sysadmin assistant — the specific task taxonomy and tooling described here are not yet built."
status: active
audience: vendor-public
bcsc_class: forward-looking
language_protocol: PROSE-TOPIC
last_edited: 2026-09-05
editor: pointsav-engineering
cites:
 - olmo3-allenai
 - federated-lora-2502-05087
 - lorax-predibase
 - s-lora-2024
 - constitutional-ai-2212-08073
 - vllm-multi-lora
 - ni-51-102
 - np-51-201
paired_with: service-slm-totebox-sysadmin.es.md
---

[[service-slm]] is intended to become the operational assistant for
[[totebox-os|Totebox]] deployments — an AI that helps an operator diagnose and resolve
day-to-day sysadmin problems instead of requiring them to search documentation or escalate
to engineering. This is a planned direction, not a shipped feature: what's real today is the
underlying training substrate; what's planned is directing it at sysadmin work specifically.

## What's real today

The [[apprenticeship-substrate|apprenticeship pipeline]] this plan would build on is real and
operational. It captures a corpus tuple for any labeled task type at `stage_at_capture:
review`, `verdict: null`, on every relevant commit — automatic, no operator action. A senior
identity later reviews captured tuples and signs a verdict (approve, refine, reject, or defer)
using an SSH signature verified against the workspace's signer registry. This capture-then-
verdict-sign mechanism is generic — it already runs today for engineering task types, not
sysadmin ones — and per-tenant LoRA adapters composed at request time by the Doorman are a
real, working capability.

## The proposed task taxonomy

A survey of the operational guides across Totebox deployment clusters suggests roughly ten
recurring categories of sysadmin work a trained assistant could help with: node provisioning,
ingress-pipeline diagnosis, sovereign data extraction, cold-storage egress, review of
AI-drafted records against verified ones, search-index operations, identity and pairing
operations, adapter deployment validation, audit-trail reconciliation, and schema-conforming
data import. Each would need its own task type registered in the pipeline above, with its own
corpus of real operator interactions, before an adapter could be trained for it.

## Why service-slm rather than an external API, if built

The reasoning for keeping this work local rather than routing it to a third-party API applies
regardless of whether the specific taxonomy above is what ships: every one of these task
categories touches tenant data — personnel records, corporate ledgers, property archives,
audit trails — and routing that data to an external service for routine sysadmin operations
would break the platform's data-sovereignty guarantee. A model running inside the customer's
own Doorman boundary is the architecture where the data never leaves the customer's own
infrastructure. Per-tenant LoRA adapters, once trained on a customer's own operational corpus,
would also make the assistant more accurate for that customer specifically than a generic
service could be — the customer's own interaction history stays within their own substrate,
available for training, without external transmission.

## Cost and timeline

Any cost or timeline figures for this capability — per-request cost at scale, training-run
cost, adapter promotion thresholds — are planned targets pending real operational data,
not measured figures. [ni-51-102] [np-51-201]

## What this is not

No sysadmin task type has been registered in the apprenticeship pipeline. The task taxonomy
above, and the specific tools it names, are a proposal for how the pipeline's existing
capture-then-verdict mechanism could be extended to sysadmin work — not an inventory of what
exists today. No sysadmin-specific adapter has been trained, and no cost or timeline figure
above is a measured value.

## See also

- [[service-slm]] — the service that would implement this capability
- [[compounding-doorman]] — the operational pattern the Doorman implements
- [[apprenticeship-substrate]] — the real capture-and-verdict-signing pipeline this plan builds on
- [[brief-queue-substrate]] — the durable queue that keeps corpus capture continuous across compute-tier transitions
- [[pointsav-llm]] — the related, separately-planned commercial specialist-model product
