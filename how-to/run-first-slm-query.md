---
schema: foundry-doc-v1
title: "Run your first SLM query"
slug: run-first-slm-query
short_description: "Submits a first inference request to Doorman directly over HTTP — the real path, since the console's F9 slot is a monitoring dashboard with no query interface at all."
category: how-to
index_group: working-in-the-console
content_type: how-to
type: how-to
quality: complete
status: active
audience: "Engineers (hands on keyboard); customer operators"
last_edited: 2026-08-06
editor: pointsav-engineering
paired_with: run-first-slm-query.es.md
research_trail:
  sources: [pointsav-monorepo service-slm/scripts/slm-chat.sh (the real working curl-based query tool), service-slm/crates/slm-doorman-server (the /v1/chat/completions route), service-slm/crates/slm-doorman/src/router.rs (tier selection and fallback logic)]
  verification_method: "independently source-verified against pointsav-monorepo on 2026-08-06 by reading the Rust source and the real slm-chat.sh script directly, with file:line citations recorded per claim; this guide replaces its own prior premise entirely — F9 in os-console has no prompt-submission UI of any kind (confirmed by reading its full event-handling code), so the real path is a direct HTTP call to Doorman, not a console feature; also corrected a real tier-fallback misconception (Tier A, not Tier B, is the practical default/minimum) and a real streaming claim from an internal doc that doesn't match the reference script's actual blocking behavior"
---

## Prerequisites

- The local SLM service and Doorman running and reachable (see [[run-local-slm-inference]])
- `curl`, or the reference script at `service-slm/scripts/slm-chat.sh` if you have it available
- Your module identifier for the `X-Foundry-Module-ID` header

## Purpose

Submit a first inference request and get a response back — under a minute once Doorman is up. This is not a console task: F9 in `os-console` is a read-only health dashboard with no way to type or submit a query, so the real path is a direct HTTP call to Doorman.

## Procedure

1. Confirm Doorman is reachable. The default local address is `http://127.0.0.1:9080`, though your deployment may differ.

2. Send a request to the chat-completions endpoint:

   ```bash
   curl -s -X POST \
     -H "Content-Type: application/json" \
     -H "X-Foundry-Module-ID: <your-module-id>" \
     -d '{"messages": [{"role": "user", "content": "Say hello in one sentence."}]}' \
     http://127.0.0.1:9080/v1/chat/completions
   ```

   Headers are forgiving in development: Doorman generates safe defaults when they're absent, specifically so ad-hoc curl probes like this one work without extra setup. Still, set `X-Foundry-Module-ID` explicitly once you're doing real work — it's how the platform attributes usage to your module.

3. Read the response. It arrives as a single JSON payload, not a stream — the whole reply lands in one `content` field once the model finishes, not token by token.

   > **Note:** a reference REPL script exists at `service-slm/scripts/slm-chat.sh` that wraps this same call in a loop, so you can keep a conversation going without retyping headers each time. Despite what an older internal note claims, that script does not stream either — it's the same one blocking call per turn, just looped.

## Expected outcome

A JSON response containing the model's reply in its `content` field, returned as one complete payload.

## Verification

Confirm the response's `content` field holds a real, on-topic reply rather than an error body. An HTTP error status or a JSON `error` field means Doorman couldn't complete the request — check that the local SLM service is actually running before retrying.

> **Note:** you don't need any specific inference tier "up" for this to work. Doorman defaults ordinary requests to the local tier; a higher tier only comes into play for requests explicitly marked high-complexity, and even then it falls back to the local tier automatically on failure rather than failing your request.

## Rollback

Nothing to roll back — a query is read-only against your own conversation history. Sending another request doesn't require undoing the last one.

## Next steps

- [[read-the-command-ledger]] — read platform activity history via its own real HTTP API
- [[use-f-key-model]] — what F9 actually shows, now that you know it isn't where queries go

## See also

- [[run-local-slm-inference]] — start the local SLM service and Doorman on a new deployment
- [[doorman-protocol]] — Doorman's routing and circuit-breaker model
- [[slm-stack-architecture]] — the full inference stack and tier definitions
