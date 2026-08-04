---
schema: foundry-doc-v1
title: "Configure the Doorman gateway"
slug: configure-doorman
short_description: "Configures a single-instance Doorman gateway via environment variables — Tier A local endpoint, optional Tier B Yo-Yo burst compute, optional Tier C external providers — and verifies tier state through /readyz."
category: self-hosting
index_group: wiring-up-inference
content_type: how-to
type: how-to
quality: complete
status: active
audience: "Engineers (hands on keyboard); customer operators"
last_edited: 2026-08-04
editor: pointsav-engineering
paired_with: configure-doorman.es.md
---

## Prerequisites

- The `slm-doorman-server` binary (or the `slm-doorman` systemd unit) available on the deployment host
- The local SLM model binary present at the path Tier A expects (see `local-slm.service`)
- A terminal session on the host where Doorman will run
- Network access to a Yo-Yo GCE endpoint, if Tier B burst compute is wanted (optional)
- API keys for Anthropic, Gemini, or OpenAI, if Tier C external fallback is wanted (optional)

## Purpose

The Doorman gateway routes inference and audit-proxy requests to one of three tiers: Tier A (a local small model), Tier B (Yo-Yo GCE burst compute, optional), or Tier C (external vendor APIs, optional). Doorman is configured entirely through environment variables — there is no configuration file. A Doorman with only Tier A configured is a complete, valid deployment ("community-tier mode"); Tiers B and C are additive, not required.

## Procedure

1. Set the bind address. Doorman listens on `SLM_BIND_ADDR` (default `127.0.0.1:9080` — loopback only; put a TLS-terminating reverse proxy in front for anything beyond same-host traffic).

2. Set the Tier A (local) endpoint and model. `SLM_LOCAL_ENDPOINT` must match the address `local-slm.service` binds to (default `http://127.0.0.1:8080`). `SLM_LOCAL_MODEL` must match the model filename that service loaded at boot (for example `Olmo-3-1125-7B-Think-Q4_K_M.gguf`). These two variables are the only ones required for Doorman to start and serve requests.

3. Optional: set the Tier B (Yo-Yo) variables. Leave every `SLM_YOYO_*` variable empty or unset to stay in community-tier mode (Tier A only) — Doorman boots cleanly either way. To enable Tier B, set at minimum `SLM_YOYO_ENDPOINT` (the Yo-Yo GCE inference URL) and `SLM_YOYO_BEARER` (a static bearer token for the dev/staging path; a real GCP Workload Identity deployment replaces this with a provider-specific token). `SLM_YOYO_MODEL` names the model served at that endpoint.

4. Optional: set the Tier C (external) variables. Each provider (`SLM_TIER_C_ANTHROPIC_*`, `SLM_TIER_C_GEMINI_*`, `SLM_TIER_C_OPENAI_*`) needs its own endpoint, API key, and per-million-token input/output rates. Any provider left unset stays disabled; the audit-proxy route (`POST /v1/audit/proxy`) returns `503` with an explanatory "unconfigured" message until at least one is set — this is correct, expected behavior, not an error state.

5. Place the populated variables in an `EnvironmentFile` (for example `/etc/local-doorman/local-doorman.env`) and point the systemd unit's `EnvironmentFile=` directive at it, or add the values as inline `Environment=` lines in a unit drop-in. Values in the `EnvironmentFile` take precedence over any inline `Environment=` lines already in the unit.

6. Start the service:

   ```
   sudo systemctl start slm-doorman
   ```

## Expected outcome

Doorman starts and begins accepting requests on `SLM_BIND_ADDR`, regardless of whether Tier B or Tier C are configured. `GET /healthz` returns `200` immediately as a liveness check. `GET /readyz` returns readiness plus tier state once Doorman has finished building its internal router.

## Verification

Check readiness and tier state:

```
curl http://127.0.0.1:9080/readyz
```

A healthy Tier-A-only ("community-tier") response includes:

```json
{
  "tier_a": true,
  "tier_b": false,
  "tier_c": false,
  "has_local": true,
  "has_yoyo": false,
  "has_external": false,
  "ai_available": true
}
```

`tier_a`/`tier_b`/`tier_c` (and their `has_local`/`has_yoyo`/`has_external` equivalents) are booleans, not a circuit-state string — a tier reads `true` once its dependency is reachable, `false` otherwise. `ai_available` is `true` whenever any one tier is up. Tier B additionally exposes its own circuit-breaker detail at `GET /v1/status/yoyo` (Yo-Yo node circuit states) — a Tier-B request that hits an open Yo-Yo circuit falls back to Tier A automatically rather than failing.

Confirm routing, not just readiness, by submitting a real request:

```
curl -X POST http://127.0.0.1:9080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"Say hello in one word."}]}'
```

## Rollback

Stop the service and remove or comment out the variables you changed:

```
sudo systemctl stop slm-doorman
```

Tier B and Tier C are additive and independently disable-able — clearing `SLM_YOYO_ENDPOINT` or a `SLM_TIER_C_*` provider's key returns Doorman to community-tier mode on the next restart without affecting Tier A.

## Next steps

- [[run-local-slm-inference]] — submit inference requests once Doorman is running
- [[doorman-protocol]] — the full routing and circuit-breaker model
- [[navigate-console-tui]] — read tier status from the console's F9 dashboard

## See also

- [[doorman-protocol]] — the circuit-breaker model and the routing logic between tiers
- [[slm-stack-architecture]] — how the SLM model that Tier A depends on is structured
- [[run-local-slm-inference]] — verifying the SLM service is healthy before Doorman starts
- [[navigate-console-tui]] — reading tier status in the console status bar
- [[run-first-slm-query]] — submitting your first inference request once Doorman is configured
