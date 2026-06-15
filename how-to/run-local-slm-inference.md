---
schema: foundry-doc-v1
title: "How to run local SLM inference"
slug: run-local-slm-inference
category: how-to
content_type: how-to
type: how-to
status: stub
last_edited: 2026-06-14
editor: pointsav-engineering
paired_with: run-local-slm-inference.es.md
---

The PointSav inference stack runs a small language model locally via the Doorman gateway. All inference stays on the operator's hardware — no prompt data is sent to an external provider. This guide covers starting the local SLM service, verifying the Doorman health endpoint, and submitting your first inference request from os-console.

For the inference stack architecture, see [[slm-stack-architecture]] and [[doorman-protocol]]. For the console cartridge that surfaces local inference in the TUI, see [[app-console-slm]].

## See also

- [[slm-stack-architecture]] — architecture of the local SLM stack and supported model tiers
- [[doorman-protocol]] — the Doorman gateway protocol; health, routing, and circuit-breaker behaviour
- [[app-console-slm]] — the os-console SLM cartridge and the Doorman health dashboard
- [[open-first-totebox-session]] — the operator context in which inference is available
- [[self-host-a-deployment]] — provision the instance that hosts the inference stack
