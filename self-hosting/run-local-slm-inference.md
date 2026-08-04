---
schema: foundry-doc-v1
title: "Run local SLM inference"
slug: run-local-slm-inference
short_description: "Starts the local Tier A SLM service, verifies Doorman readiness, and submits an inference request from the console or the API, with all prompt data staying on the deployment."
category: self-hosting
content_type: how-to
type: how-to
quality: complete
status: active
audience: "Engineers (hands on keyboard); customer operators"
last_edited: 2026-08-04
editor: pointsav-engineering
paired_with: run-local-slm-inference.es.md
---

## Prerequisites

- A deployment with the local SLM model binary installed at the path `local-slm.service` expects (see [[self-host-a-deployment]])
- The `slm-doorman` service running and healthy (see [[configure-doorman]])
- A session with User-level access (see [[pair-a-new-device]])

## Purpose

The platform's inference stack runs a small language model locally, on Tier A, reached through the Doorman gateway. All Tier A inference stays on the operator's own hardware — no prompt data leaves the deployment. This guide starts the local model, confirms Doorman sees it as ready, and submits a request — both from the console TUI and directly against the API.

## Procedure

1. Start the local SLM service, if it isn't already running:

   ```
   sudo systemctl start local-slm
   ```

2. Confirm it started cleanly:

   ```
   systemctl is-active local-slm
   journalctl -u local-slm --since "1 minute ago"
   ```

   A healthy start logs the model loading and the service binding its port (default `127.0.0.1:8080`). If it fails, check that the model file named in the unit's configuration is actually present at the path the service expects.

3. Confirm Doorman sees Tier A as ready. In the console, press **F9** to open the SLM Cartridge's health dashboard, which reads Doorman's `/readyz`. `tier_a` (also shown as `A — Local`) must be `true`/green before a request will succeed. Press **R** to refresh.

4. Submit a prompt from the console. With Tier A live, type a prompt at the F9 input line and press Enter — the response streams token-by-token into the output area, and the status bar shows the active tier during generation.

5. Or submit a prompt directly via the API:

   ```
   curl -X POST http://127.0.0.1:9080/v1/chat/completions \
     -H "Content-Type: application/json" \
     -d '{"messages":[{"role":"user","content":"Summarise the role of the Doorman gateway."}]}'
   ```

   The response is an OpenAI-compatible JSON object with a `choices` array; each choice carries the generated text.

## Expected outcome

A prompt sent while Tier A is ready returns a generated response with no data leaving the host — the console's F9 line and the `/v1/chat/completions` call are the same underlying request path, just two different clients.

## Verification

Console inference requests are SYS-ADR-07-safe by construction: only plain prompt text passes through the model layer, never structured platform data (entity records, WORM entries). Confirm Tier A stayed the serving tier rather than silently falling back, by checking `/readyz` again after the request:

```
curl http://127.0.0.1:9080/readyz
```

`tier_a: true` and `ai_available: true` confirm Tier A served the request. If Tier B (Yo-Yo) is configured and Tier A becomes unavailable mid-session, Doorman routes to Tier B automatically rather than failing — see [[doorman-protocol]] for the full fallback order.

## Rollback

Stop the local model service; Doorman itself keeps running and reports `tier_a: false` on its next `/readyz` check rather than crashing:

```
sudo systemctl stop local-slm
```

## Next steps

- [[run-first-slm-query]] — a first, guided query walkthrough from the console
- [[query-the-datagraph]] — a different Doorman-routed capability, entity lookup rather than inference
- [[doorman-protocol]] — the full tier-fallback model, for when Tier A alone isn't enough

## See also

- [[slm-stack-architecture]] — architecture of the local SLM stack and supported model tiers
- [[doorman-protocol]] — the Doorman gateway protocol; readiness, routing, and tier-fallback behaviour
- [[app-console-slm]] — the os-console SLM cartridge and the Doorman health dashboard
- [[run-first-slm-query]] — submitting a query from the console once the model is running
- [[self-host-a-deployment]] — provision the instance that hosts the inference stack
- [[configure-doorman]] — configuring Tier A/B/C before running an inference request
