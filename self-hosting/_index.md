---
schema: foundry-doc-v1
title: "Self-Hosting"
slug: self-hosting-index
category: self-hosting
type: topic
content_type: topic
index_type: thematic
index_scope: self-hosting
quality: complete
short_description: "Running the platform on your own infrastructure: booting the seL4 appliance images, deploying the wiki engine, and wiring up local inference."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-08-04
editor: pointsav-engineering
paired_with: _index.es.md
---

**Self-hosting** means running platform components on infrastructure you control rather than a hosted instance — booting the published seL4 appliance images, standing up the wiki engine against your own content, and wiring the inference gateway to your own hardware. Every component here degrades gracefully rather than refusing to start: a deployment with only one piece running is still a valid, useful deployment.

<!-- START-HERE-HIGHLIGHT: engine reads this block to render the single "start here" card
     (reuses the existing cluster-card--start-here component). Do not add more than one. -->

**Start here:** [Self-host a deployment](/wiki/self-host-a-deployment) — boots the two independent seL4 appliance images (`os-totebox`, `app-orchestration-slm`) that everything else in this category runs on top of.

<!-- END-START-HERE-HIGHLIGHT -->

## Getting the platform running

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: getting-running -->
- [Self-host a deployment](/wiki/self-host-a-deployment) — boot the `os-totebox` and `app-orchestration-slm` appliance images under QEMU
- [Deploy a knowledge instance](/wiki/deploy-knowledge-instance) — serve a documentation, projects, or corporate wiki from a local content path
<!-- END AUTO-GENERATED -->

## Wiring up inference

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: wiring-inference -->
- [Configure the Doorman gateway](/wiki/configure-doorman) — set Tier A/B/C endpoints through environment variables, no config file
- [Run local SLM inference](/wiki/run-local-slm-inference) — start the local model and submit a request through Doorman
<!-- END AUTO-GENERATED -->

## What this is not

This page is not a substitute for reading the linked guides — each one carries its own prerequisites, verification steps, and rollback procedure that this page doesn't repeat. It does not cover day-to-day platform operation once a deployment is running (pairing devices, issuing tokens, scaling access) — those guides stay in [How You Run It](/category/how-to) until they get the same category treatment in a later pass.

## See also

- [How You Run It](/category/how-to) — the remaining day-to-day operational guides
- [Where It Runs](/category/infrastructure) — the architecture these guides deploy against
- [Security and Trust](/category/security) — the identity and permissions model self-hosted deployments participate in
