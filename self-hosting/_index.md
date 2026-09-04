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
last_edited: 2026-09-04
editor: pointsav-engineering
paired_with: _index.es.md
---

**Self-hosting** means running platform components on infrastructure you control rather than a hosted instance — booting the published seL4 appliance images, standing up the wiki engine against your own content, and wiring the inference gateway to your own hardware. Every component here degrades gracefully rather than refusing to start: a deployment with only one piece running is still a valid, useful deployment.

<!-- START-HERE-HIGHLIGHT: engine reads this block to render the single "start here" card
     (reuses the existing cluster-card--start-here component). Do not add more than one. -->

**Start here:** [[self-host-a-deployment|Self-host a deployment]] — boots the two independent seL4 appliance images (`os-totebox`, `app-orchestration-slm`) that everything else in this category runs on top of.

<!-- END-START-HERE-HIGHLIGHT -->

## Getting the platform running

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: getting-running -->
- [[self-host-a-deployment|Self-host a deployment]] — Boots the published os-totebox and app-orchestration-slm seL4 appliance images under QEMU, with configuration baked in at build time via device-tree bootargs, and verifies both come up healthy.
- [[deploy-knowledge-instance|Deploy a knowledge instance]] — Deploys an instance of app-mediakit-knowledge from a local content path: write a knowledge.toml [site] + [[mount]] configuration, build the binary, and start it with the serve subcommand.
<!-- END AUTO-GENERATED -->

## Wiring up inference

<!-- AUTO-GENERATED MEMBERSHIP: DO NOT EDIT BELOW — regenerate from index_group: wiring-inference -->
- [[configure-doorman|Configure the Doorman gateway]] — Configures a single-instance Doorman gateway via environment variables — Tier A local endpoint, optional Tier B Yo-Yo burst compute, optional Tier C external providers — and verifies tier state through /readyz.
- [[run-local-slm-inference|Run local SLM inference]] — Starts the local Tier A SLM service, verifies Doorman readiness, and submits an inference request from the console or the API, with all prompt data staying on the deployment.
<!-- END AUTO-GENERATED -->

Each guide carries its own prerequisites, verification steps, and rollback procedure; this
page doesn't repeat them. Day-to-day operation of a running deployment is in
[How You Run It](/category/how-to).

## See also

- [How You Run It](/category/how-to) — the remaining day-to-day operational guides
- [Where It Runs](/category/infrastructure) — the architecture these guides deploy against
- [Security and Trust](/category/security) — the identity and permissions model self-hosted deployments participate in
