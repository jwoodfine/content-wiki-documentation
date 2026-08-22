---
schema: foundry-doc-v1
title: "Model tier discipline"
slug: model-tier-discipline
category: patterns
type: topic
content_type: topic
quality: complete
index_group: collaboration-and-editorial-workflow
short_description: "The Doorman routes every inference request to one of three compute tiers — local, burst GPU, or external API — based on a complexity hint and live budget state, not a caller's direct choice."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-08-22
editor: pointsav-engineering
cites: []
paired_with: model-tier-discipline.es.md
---

A platform that routes every inference request through the same fixed compute path spends significantly more per output than necessary, or fails requests that a cheaper path could have served. Model tier discipline is the [[doorman-protocol|Doorman service]]'s routing discipline: every inference request carries a complexity hint, and the Doorman — not the caller — decides which of three compute tiers actually serves it, based on that hint plus live budget caps and warm-instance state.

## Three tiers, one router

The Doorman defines three inference routes:

**Local** — on-host inference, currently a quantized OLMo 3 7B model served over HTTP on the same machine as the Doorman. No network egress, no per-request cost beyond the machine's own power draw.

**Yoyo** — burst compute on a preemptible multi-cloud GPU instance, currently a larger OLMo 3 model tuned for deeper reasoning. Used when a request's complexity exceeds what the local tier can serve well, at the cost of the burst-instance's startup latency and running cost.

**External** — an external API (Anthropic, Google, or OpenAI), reserved for narrow, precision-critical tasks and gated behind an explicit allowlist rather than opened to arbitrary requests. **A request only reaches an external API when the task genuinely needs it — every request defaults toward staying on infrastructure the operator controls, not away from it.**

## The caller hints; the Doorman decides

A caller does not pick a tier directly. It submits a complexity hint — low, medium, or high — describing the shape of the work, and the Doorman maps that hint to a concrete tier using its own budget caps and current instance state. The same "high complexity" hint might route to Yoyo when a burst instance is already warm, or hold at Local under tight budget conditions — the caller's hint is an input to the routing decision, not the decision itself.

This indirection is what makes the discipline enforceable rather than aspirational. If callers picked their own tier, cost discipline would depend on every caller consistently choosing the cheapest tier that would work — the same problem a platform with no tier guidance has, just moved one layer down. Routing through the Doorman means the enforcement point is one piece of code, not every caller's judgment.

## Why this matters for cost

Running work at whichever tier can actually serve it — rather than defaulting every request to the most capable tier available — produces a large effective cost multiplier at a fixed compute budget. Simple, well-specified requests that a local model handles correctly never touch the more expensive burst or external tiers at all. The savings compound: a platform running at tier discipline sustains substantially more request volume within the same infrastructure cost than one that does not.

## See also

- [[service-slm-operationalization-plan]] — the compute routing architecture the Doorman implements
- [[doorman-protocol]] — the Doorman service that performs this routing at the inference gateway
- [[zero-container-runtime]] — the deployment discipline the Doorman itself follows as a systemd-managed binary
