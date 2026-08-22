---
schema: foundry-doc-v1
title: "Single-boundary compute discipline"
slug: single-boundary-compute-discipline
category: substrate
type: topic
content_type: topic
quality: complete
index_group: the-compounding-doorman-and-ai-boundary
short_description: "Every AI inference request in a platform deployment routes exclusively through the Doorman, with bypass structurally prevented at the kernel level."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-01
editor: pointsav-engineering
cites: []
paired_with: single-boundary-compute-discipline.es.md
---

The **Single-Boundary Compute Discipline** is the structural rule that all AI inference traffic in a platform deployment passes through one and only one boundary point: the [[compounding-doorman|Doorman]] (`service-slm`). No process, session, or service reaches an inference tier — local, [[yoyo-compute-substrate|GPU burst]], or external API — except through this boundary.

It is not a preferred-path routing convention that allows bypass by configuration; it is enforced at the kernel and secret boundaries so that no other process on the system can reach inference compute.

## Why one boundary

A single boundary makes four properties structurally guaranteed rather than policy-dependent:

**Audit completeness.** The [[worm-ledger-architecture|audit ledger]] records every inference call. An operator asking "did AI touch this record?" inspects the ledger and receives a definitive answer. If bypass were possible, the ledger would have gaps — and a gapped ledger is inadmissible as a compliance record.

**Corpus completeness.** The [[apprenticeship-substrate|apprenticeship substrate]] captures every Doorman-mediated call as a training tuple. Bypass produces no shadow brief. The training corpus has gaps, and those gaps permanently degrade the quality of the per-tenant [[adapter-composition|adapter]] that accumulates from the corpus.

**Cost control.** Budget caps and kill-switches operate at the Doorman boundary. Bypass routes around the cap. A deployment with a monthly inference budget has no enforceable budget if bypass is possible.

**Sovereignty.** API keys for external providers and the bearer token for GPU burst capacity live exclusively in the Doorman's environment. No other process holds these credentials. When a key is rotated or revoked, the change happens in one place.

## What actually enforces the boundary today

**Bearer-only-in-Doorman.** The GPU burst bearer token and external provider API keys are read from the Doorman's own environment; no cluster session holds them directly.

**Loopback binding.** The Doorman's default bind address is `127.0.0.1`, not a network-reachable interface — a caller on the same machine can reach it, but nothing off-machine can, without a separate reverse proxy or port-forward the operator would have to set up deliberately.

Two mechanisms this article previously described as already enforced are not, currently, backed by code: a kernel-level, UID-scoped iptables rule restricting the local inference server to Doorman-process connections only, and a startup check that refuses to boot with a missing GPU burst bearer token. The real startup behavior defaults an unset bearer token to an empty string rather than refusing to start — a real gap between the intended discipline and what's enforced today, not a design choice. Firewalling the GPU burst instance to the Doorman's host IP is a real, standard cloud-networking control at the infrastructure level, independent of application code.

## What callers send

The Doorman exposes a standard OpenAI-compatible HTTP interface. Callers — whether a task session, the operator TUI, or a customer-built agent — send requests to the Doorman's local binding. The Doorman selects the appropriate compute tier, assembles graph-grounded context (see [[knowledge-graph-grounded-apprenticeship]]), routes the request, records the audit entry, and returns the response.

This interface is also the MCP gateway endpoint (see [[mcp-substrate-protocol]]). There is no separate path for MCP clients.

## Relationship to the three-ring architecture

The [[compounding-doorman|Doorman]] is the entry point to Ring 3. The [[three-ring-architecture]] makes Ring 3 structurally optional — a deployment may operate without AI inference entirely and the deterministic Ring 1 and Ring 2 services remain fully functional. The single-boundary discipline is what makes that optionality safe: because all inference passes through one point, disabling that point produces a clean degraded state rather than a partially-bypassed one.

## Composition

This discipline composes with several other substrate patterns. The [[knowledge-graph-grounded-apprenticeship]] depends on it: graph context is assembled at the Doorman before dispatch; bypass means ungrounded inference. The [[mcp-substrate-protocol]] designates the Doorman as the MCP gateway; bypass breaks the MCP graph. The sovereign substrate enforces customer sovereignty at the Doorman boundary; bypass is a sovereignty leak.

## See also

- [[knowledge-graph-grounded-apprenticeship]] — graph grounding assembled at the Doorman before each request
- [[mcp-substrate-protocol]] — the Doorman as MCP gateway
- [[substrate-without-inference-base-case]] — deterministic-only operation when the Doorman's inference tiers are unavailable
