---
schema: foundry-doc-v1
title: "Single-boundary compute discipline"
slug: single-boundary-compute-discipline
category: substrate
type: topic
content_type: topic
quality: complete
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

## Four enforcement mechanisms

The single-boundary discipline is structural, not policy:

**Bearer-only-in-Doorman.** All inference credentials — the GPU burst bearer token and all external provider API keys — exist only in the Doorman's environment file. No cluster session has read access to them. Without credentials, a bypass attempt fails at the authentication layer.

**Firewall.** The GPU burst instance accepts inbound connections only from the Doorman's host IP. External API provider endpoints have rate limits and audit visibility only at the Doorman. Network-level enforcement is a second structural layer.

**UID-owner iptables on the local tier.** The local inference server binds to a loopback address and accepts connections only from the Doorman process UID, enforced via iptables on the kernel output chain. Any other process on the same machine attempting a direct connection is dropped at the kernel boundary.

**Startup verification.** On boot, the Doorman verifies that its GPU burst bearer token is present when a burst endpoint is configured, and refuses to start with an unset bearer. Misconfiguration cannot accidentally allow burst traffic to flow without audit.

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
