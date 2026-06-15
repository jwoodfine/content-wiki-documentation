---
schema: foundry-doc-v1
title: "How to run local SLM inference"
slug: run-local-slm-inference
category: how-to
content_type: how-to
type: how-to
status: active
last_edited: 2026-06-14
editor: pointsav-engineering
paired_with: run-local-slm-inference.es.md
---

The PointSav inference stack runs a small language model locally via the Doorman gateway. All inference stays on the operator's hardware — no prompt data leaves the deployment. This guide covers starting the local SLM service, verifying the Doorman health endpoint, and submitting an inference request — both from the console TUI and directly via the API.

For the inference stack architecture, see [[slm-stack-architecture]] and [[doorman-protocol]]. For the console cartridge that surfaces local inference in the TUI, see [[app-console-slm]].

## Prerequisites

- A deployment with the OLMo model binary installed at the expected path (see [[self-host-a-deployment]])
- The `slm-doorman-server` service running and healthy
- A session with at least USER-level access (see [[pair-a-new-device]])

## Step 1: Start the SLM service

If the SLM service is not already running, start it:

```
sudo systemctl start slm-doorman-server
```

Verify it started cleanly:

```
systemctl is-active slm-doorman-server
journalctl -u slm-doorman-server --since "1 minute ago"
```

A healthy start produces a log line indicating the model loaded and the Doorman is listening on its configured port. If the service fails to start, check the model binary path in the service configuration — the OLMo binary must be present at the path the service expects.

## Step 2: Verify Doorman health from the console

Press **F9** in the console to open the SLM Cartridge. The Doorman health dashboard shows:

- `A — DataGraph`: availability of the entity store (not required for pure inference)
- `B — SLM`: should show green once the model is loaded and Doorman is reachable
- `C — Local fallback`: always available; used when Tier B is degraded

Tier B must be green before inference requests will succeed. Press **R** to refresh the health status.

## Step 3: Submit an inference request from the console

With Tier B live, submit a prompt at the F9 input line. Type your prompt text and press Enter. The model response streams token-by-token into the output area. The status bar shows the active inference tier (`B`) during generation.

Inference requests through the console are SYS-ADR-07-safe — no structured platform data passes through the model layer. The model receives plain prompt text only.

## Step 4: Submit an inference request directly via API

For programmatic use, call the Doorman inference endpoint:

```
curl -X POST http://127.0.0.1:<doorman-port>/v1/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <session-token>" \
  -d '{
    "prompt": "Summarise the role of the Doorman gateway:",
    "max_tokens": 200
  }'
```

The response is a JSON object with a `choices` array. Each choice contains the generated text. The `model` field in the response confirms which tier served the request.

## Step 5: Check the circuit breaker state

The Doorman circuit breaker opens automatically if the SLM service becomes unresponsive. When open, all inference requests fall through to Tier C (local fallback). To check the circuit state:

```
curl http://127.0.0.1:<doorman-port>/health
```

The response includes `tier_b_state`: `CLOSED` (healthy) or `OPEN` (tripped). A tripped circuit resets after the configured cool-down period, or immediately after the SLM service recovers.

## Key takeaways

- All inference runs on-premises; no prompt data leaves the deployment
- Tier B (SLM) must show green in the F9 health dashboard before inference requests succeed
- The Doorman circuit breaker falls back to Tier C automatically when the model is unresponsive
- SYS-ADR-07 applies: do not pass structured platform data (entity records, WORM entries) through the model layer

## See also

- [[slm-stack-architecture]] — architecture of the local SLM stack and supported model tiers
- [[doorman-protocol]] — the Doorman gateway protocol; health, routing, and circuit-breaker behaviour
- [[app-console-slm]] — the os-console SLM cartridge and the Doorman health dashboard
- [[run-first-slm-query]] — submitting a query from the console once the model is running
- [[self-host-a-deployment]] — provision the instance that hosts the inference stack
