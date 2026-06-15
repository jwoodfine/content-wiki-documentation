---
schema: foundry-doc-v1
title: "How to run your first SLM query"
slug: run-first-slm-query
category: how-to
content_type: how-to
type: how-to
status: active
last_edited: 2026-06-14
editor: pointsav-engineering
paired_with: run-first-slm-query.es.md
---

The SLM Cartridge at F9 routes inference requests through Doorman to the on-premises language model. No prompt data is transmitted to an external provider — the model runs locally. This guide covers opening the SLM slot, checking that Doorman has a live circuit, and submitting your first prompt.

For the inference architecture, see [[app-console-slm]] and [[slm-stack-architecture]]. For setting up the inference stack on a new deployment, see [[run-local-slm-inference]].

## Prerequisites

- An active Totebox session with F9 available
- The local SLM service running on the host instance
- Doorman running and reachable on the local port

## Steps

### 1. Open the SLM Cartridge

Press **F9**. The Doorman health dashboard fills the slot area. It shows three rows:

| Row | What it shows |
|---|---|
| Tier A | DataGraph (service-content) availability |
| Tier B | SLM model availability |
| Tier C | Local fallback availability |

A green indicator means the tier is available; a red indicator or `OPEN` means the circuit breaker has tripped and that tier is temporarily bypassed.

### 2. Confirm inference is available

For inference to work, at minimum Tier B must show a live circuit. If Tier B shows `OPEN`, press **R** to refresh. If it remains open, the local SLM service may not be running — see [[run-local-slm-inference]] for startup steps.

### 3. Submit a prompt

Navigate to the prompt input line (shown at the bottom of the slot area). Type your prompt and press **Enter**. The response streams into the slot area above the input line.

Prompts are processed by the local model only. Context is drawn from the Totebox session and the connected DataGraph entities, not from external sources.

### 4. Read the response

The response streams token by token. When complete, the cursor returns to the input line. To start a new prompt, type and press Enter again. Prior responses remain visible by scrolling up.

Press **Esc** to clear the current prompt without submitting.

## Check inference tier in the status bar

The status bar shows the current SLM tier as a single letter (`A`, `B`, or `C`) next to the active slot label. This updates in real time as circuit states change. If the tier drops during a long-running prompt, the response may be truncated — resubmit when the circuit recovers.

## Key takeaways

- Doorman is the gateway — the Cartridge never connects to the model directly
- Tier B minimum is needed for inference; Tier A is needed for DataGraph entity context
- Press R in F9 to refresh circuit state without switching slots
- All inference is on-premises; no data leaves the host machine

## See also

- [[app-console-slm]] — the SLM Cartridge and Doorman health dashboard
- [[slm-stack-architecture]] — the full inference stack and tier definitions
- [[doorman-protocol]] — Doorman's circuit-breaker model and routing rules
- [[run-local-slm-inference]] — start the SLM service and Doorman on a new instance
- [[navigate-console-tui]] — console navigation basics
