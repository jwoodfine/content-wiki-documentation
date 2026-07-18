---
schema: foundry-doc-v1
title: "How to configure the Doorman gateway"
slug: configure-doorman
short_description: "Configures a single-instance Doorman gateway — tier upstream addresses, circuit-breaker thresholds, and verifying tier state through the health endpoint and console F9 dashboard."
category: how-to
content_type: how-to
type: how-to
status: active
last_edited: 2026-07-18
editor: pointsav-engineering
paired_with: configure-doorman.es.md
---

The Doorman gateway routes all inference and entity-lookup requests to the appropriate tier: Tier A (DataGraph), Tier B (local SLM), or Tier C (local fallback). Configuring Doorman means setting the upstream addresses for each tier, defining circuit-breaker thresholds, and verifying the health endpoint after startup. This guide covers a single-instance Doorman deployment.

For the Doorman protocol and circuit-breaker model, see [[doorman-protocol]]. For starting the SLM model that Tier B depends on, see [[run-local-slm-inference]].

**Major correction (2026-07-18):** this guide's tier mapping and configuration mechanism
are inverted against the live source. Direct verification against
`service-slm/docs/deploy/local-doorman.env.example` (which documents itself as generated
against `slm-doorman-server::main.rs`) shows:

- **Doorman is configured via environment variables (`SLM_*`), not a `doorman.toml` file
  with `[tier_a]`/`[tier_b]`/`[tier_c]` sections.** The entire Step 1 configuration example
  below describes a mechanism that does not exist in the live source.
- **Tier A is the local small model**, not DataGraph — `SLM_LOCAL_ENDPOINT` (default
  `http://127.0.0.1:8080`), `SLM_LOCAL_MODEL` (e.g. `Olmo-3-1125-7B-Think-Q4_K_M.gguf`).
- **Tier B is Yo-Yo burst GCE compute**, not "local SLM" — `SLM_YOYO_ENDPOINT`,
  `SLM_YOYO_MODEL` (e.g. `Olmo-3-1125-32B-Think`), optional and disabled by default
  (community-tier mode when unset).
- **Tier C is external vendor API providers** (Anthropic/Gemini/OpenAI), not "local
  fallback" — `SLM_TIER_C_ANTHROPIC_*` etc., all commented out/unconfigured by default.
- The Doorman bind address (`SLM_BIND_ADDR`, default `127.0.0.1:9080`) does match this
  guide's port claim — that detail is not in dispute.
- This matches the tier model already confirmed elsewhere in this wiki and via live
  `get_doorman_status()` checks this session (`has_local`/`has_yoyo`/`has_external`,
  `tier_b.{default,trainer,graph}` sub-labels for Yo-Yo nodes specifically).

**Flagged, not silently rewritten below** — the Steps 1–5 walkthrough, TOML example, and
`circuit_breaker_threshold`/`fallback_message` fields have not been individually verified
against real env-var equivalents; a full rewrite needs the actual `slm-doorman-server`
CLI/env-var reference, not just this correction note. Treat the JSON `/health` response
shape and the F9 console step as unverified pending the same review.

## Prerequisites

- The `slm-doorman-server` binary available on the deployment host
- Network access to the DataGraph endpoint (`service-content`) if Tier A is intended
- The OLMo model binary present at the configured path for Tier B
- A terminal session on the host where Doorman will run

## Step 1: Create the Doorman configuration file

Doorman reads its configuration from a TOML file. Create `doorman.toml`:

```toml
[server]
port = 9080
bind = "127.0.0.1"

[tier_a]
enabled = true
service_content_url = "http://127.0.0.1:9090"
circuit_breaker_threshold = 5
circuit_breaker_timeout_secs = 30

[tier_b]
enabled = true
model_path = "/opt/pointsav/models/olmoe-1b-7b-instruct.gguf"
context_window = 4096
max_tokens = 512

[tier_c]
enabled = true
fallback_message = "Inference unavailable — local fallback only"
```

Adjust `service_content_url` to match the DataGraph service address in your deployment. If the DataGraph is on the same host, `127.0.0.1:9090` is typical. If it is on a separate node, use its network address.

## Step 2: Start the Doorman service

Start the service with the configuration file:

```
slm-doorman-server --config doorman.toml
```

Or as a systemd service:

```
sudo systemctl start slm-doorman-server
```

Doorman logs its startup sequence: it attempts to contact the DataGraph (Tier A), loads the SLM model (Tier B), and confirms Tier C is always available. Any failure to contact Tier A at startup does not prevent Doorman from starting — it marks Tier A's circuit as `OPEN` and routes to Tier B instead.

## Step 3: Verify the health endpoint

Doorman exposes a health endpoint at `/health`:

```
curl http://127.0.0.1:9080/health
```

A healthy response:

```json
{
  "tier_a_state": "CLOSED",
  "tier_b_state": "CLOSED",
  "tier_c_state": "AVAILABLE",
  "active_tier": "A"
}
```

`CLOSED` means the circuit is healthy and routing requests. `OPEN` means the circuit has tripped and Doorman is not routing to that tier. `active_tier` shows which tier is currently receiving requests.

## Step 4: Verify from the console

Open the console and press **F9** to view the Doorman health dashboard. The dashboard reads from the same `/health` endpoint. Tier A, B, and C should show green under normal operation.

If Tier A shows `OPEN` but the DataGraph service is running, check the `service_content_url` in the configuration. A DNS resolution failure or wrong port is the most common cause.

## Step 5: Adjust circuit-breaker thresholds (optional)

The `circuit_breaker_threshold` in `[tier_a]` sets how many consecutive failures trigger the circuit. A lower threshold (e.g., 3) makes the circuit trip faster under transient failures; a higher threshold (e.g., 10) tolerates more errors before falling back. The default of 5 is appropriate for most deployments.

After changing the threshold, restart Doorman for the change to take effect:

```
sudo systemctl restart slm-doorman-server
```

## Key takeaways

- Doorman starts regardless of whether Tier A (DataGraph) is reachable — it marks unavailable tiers as `OPEN` and routes to the next
- The `/health` endpoint is the authoritative source of circuit state — read it directly or via F9 in the console
- Circuit-breaker settings are in `doorman.toml` under `[tier_a]`; changes require a service restart
- Tier C is always available; it never trips

## See also

- [[doorman-protocol]] — the circuit-breaker model and the routing logic between tiers
- [[slm-stack-architecture]] — how the SLM model that Tier B depends on is structured
- [[run-local-slm-inference]] — verifying the SLM service is healthy before Doorman starts
- [[navigate-console-tui]] — reading the Tier status in the console status bar
- [[run-first-slm-query]] — submitting your first inference request once Doorman is configured
