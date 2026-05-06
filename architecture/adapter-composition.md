---
schema: foundry-doc-v1
title: "The Adapter Composition Algebra"
slug: adapter-composition
category: architecture
type: topic
quality: published
short_description: The operating-system metaphor for AI in PointSav — the Doorman as kernel, adapters as processes, service-content as filesystem — and the composition algebra that assembles per-request intelligence from versioned, customer-owned LoRA adapter layers.
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-01
editor: pointsav-engineering
cites:
  - lorax-predibase
  - s-lora-2024
  - federated-lora-2502-05087
paired_with: adapter-composition.es.md
---

The **Adapter Composition Algebra** is the model that governs how AI intelligence is assembled at request time in a PointSav deployment. Its central metaphor maps precisely to an operating system: the Doorman (`service-slm`) is the kernel; LoRA adapters are processes; `service-content` is the filesystem; the base model is firmware. The analogy is not illustrative — it is operational.

## The algebra

At request time, the Doorman composes adapters by stacking onto the base model:

```
composed_weights =
    base_model[OLMo-3-1125-7B-Q4]
    ⊕ constitutional_adapter[doctrine_vM.m.p]
    ⊕ engineering_adapter[pointsav_vN]?
    ⊕ tenant_adapter[<tenant>_vK]?
    ⊕ role_adapter[master | root | task]
    ⊕ cluster_adapter[<cluster-name>_vJ]?
```

Where `?` denotes an optional adapter loaded only when the request context applies. `⊕` is the LoRA-stacking operator — a rank-r delta added to the base model weights at runtime.

The composition is deterministic given the request context. There is no runtime decision about which adapters to use; the context determines the composition.

## Adapter typology and routing rules

| Adapter | Loaded when | Ownership |
|---|---|---|
| `constitutional` | Always — every Foundry deployment | Constitutional adapter; ships with the knowledge commons (Apache 2.0) |
| `engineering` | Request scope is "build or modify the platform" | Vendor-curated; offered to Customers via service contract |
| `tenant` | Request scope operates on tenant data | Inside Customer Totebox; per-tenant; never leaves customer storage |
| `role` | Request originates from a Master/Root/Task session | Universal across deployments; learned from doctrine and role-tagged trajectories |
| `cluster` | Request scope is a specific project cluster | Per-cluster; declared in the cluster manifest |

The constitutional adapter is universal and is loaded by every Foundry deployment. The tenant adapter is strictly per-tenant and is produced and held inside the Customer Totebox. The engineering adapter ships with the knowledge commons and is not treated as private vendor IP.

## Implementation

The algebra runs on production 2026 multi-LoRA serving infrastructure:

- **LoRAX (Predibase)** — multi-LoRA inference server; thousands of adapters per GPU; per-request hot-swap; per-tenant private adapters
- **S-LoRA** — adapter isolation per dynamic computation; shared static backbone via secure IPC; significant time-to-first-token reduction
- **vLLM Multi-LoRA** — hot-swap at request time without reloading the base model

PointSav's contribution is the composition pattern — which adapters compose, in what order, under what doctrinal constraint — not the serving layer itself.

## Adapter versioning

Each adapter carries a name, a semver version, the doctrine version it was trained against, a provenance field naming the corpus shards it was distilled from, and a signature signed by the trainer's identity. A composed request must reconcile adapter versions. The default policy loads adapters whose `doctrine_version` matches the deployment's current `doctrine_version`. Version mismatch surfaces as an operational signal — the deployment's MANIFEST records the active doctrine version and the discrepancy becomes visible.

This solves AI drift at the substrate level: the model is verifiably aligned to a specific doctrine version, and any mismatch is a first-class observable rather than a silent degradation.

## The OS-of-AI metaphor

The analogy maps precisely:

| OS concept | AI concept | Foundry artifact |
|---|---|---|
| Firmware | Pretrained base model | OLMo 3 7B / 32B GGUF |
| Kernel | Request router | Doorman (`service-slm`) |
| Process | Composable behavior unit | LoRA adapter |
| Filesystem | Structured knowledge | `service-content` (LadybugDB graph) |
| System call | Tool invocation | MCP server interface |
| Virtual memory | Per-tenant isolation | `moduleId`-keyed partitions |
| Kernel module | Cluster-scoped capability | Cluster adapter |
| User profile | Role boundary | Role adapter |
| Constitution / charter | OS license + principles | Constitutional adapter |
| Package manager | Adapter library + signing | `data/adapters/` + signed manifests |

Customers install and uninstall adapters as packages. Adapter signatures are verified before composition. Per-tenant isolation is enforced at the serving layer the way virtual memory isolation is enforced at the kernel layer.

This frames the substrate for small and medium businesses as **the operating system of AI** — composable intelligence with a flat architecture rather than a single closed product. Any adapter can be swapped without touching the others. The customer owns the adapters trained on their own corpus. The doctrine is the soul; the corpus is the mind; the adapters are the personality.

## Practical composition ceiling

Production multi-LoRA research demonstrates that composing 2–3 adapters per request works cleanly. Composing 5 or more adapters per request crosses into multi-task interference. The algebra stays at a maximum of three runtime adapters per request by design. Register, brand voice, document sub-type, and target audience parameters live in prompt scaffolding (the genre template layer), not as additional adapters.

## The Vendor LLM tier

When the Vendor's engineering corpus accumulates sufficient scale — planned for Year 2 or later, at version 0.5.0 onward — continued pretraining may produce a model whose capability crosses an inflection from SLM to a larger model. This larger model may be offered as a Doorman tier in Customer deployments alongside Tier C external APIs, under service contract. Customer Doormans would then be able to route to the Vendor LLM for queries that exceed local Tier A capacity and where Tier C is undesirable.

This tier is intended to be a byproduct of the substrate work as the corpus matures, not a separately developed product.

## See Also

- [[compounding-doorman]] — the Doorman that implements the kernel role in this algebra
- [[apprenticeship-substrate]] — the mechanism that produces the per-tenant adapter corpus
- [[language-protocol-substrate]] — the language-family adapter taxonomy that extends this algebra for editorial work
- [[knowledge-commons]] — how constitutional and engineering adapters are published as commons artifacts

## References

1. LoRAX — Predibase multi-LoRA inference server, open source.
2. S-LoRA — scalable serving of thousands of concurrent LoRA adapters, MLSys 2024.
3. Federated LoRA, arXiv 2502.05087.

---

## Provenance

Source material: `conventions/adapter-composition.md` (ratified 2026-04-26, doctrine v0.0.2). Disciplines applied: no body H1; structural positioning (multi-LoRA infrastructure providers retained as factual technical references, not competitive contrast); BCSC forward-looking framing on Vendor LLM tier (planned/may/Year 2 or later); banned-vocabulary pass; workspace-internal adapter paths adapted to general form.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).*

*Woodfine Capital Projects™, Woodfine Management Corp™, PointSav Digital Systems™, Totebox Orchestration™, and Totebox Archive™ are trademarks of Woodfine Capital Projects Inc., used in Canada, the United States, Latin America, and Europe. All other trademarks are the property of their respective owners.*
