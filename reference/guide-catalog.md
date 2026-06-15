---
schema: foundry-doc-v1
title: "Developer Guide Index"
slug: guide-catalog
category: reference
type: topic
content_type: topic
status: stable
last_edited: 2026-06-14
editor: pointsav-engineering
paired_with: guide-catalog.es.md
aliases:
  - developer-guide-index
---

The Developer Guide Index lists the task-oriented how-to guides for the PointSav platform, organised by developer concern. Each guide covers a specific task a developer performs when building with or deploying the platform. For the underlying architecture that each guide draws on, follow the article wikilinks within each guide.

Internal operator runbooks for the Woodfine fleet deployment are not listed here — they are operational documents for provisioning and maintenance, not public developer guides.

## Getting started

These guides cover the first steps for a developer new to the platform — setting up device authorization and opening a working session.

- [[pair-a-new-device]] — register a new device and assign it a pairing tier (INPUT, USER, or INTERFACE)
- [[open-first-totebox-session]] — open a scoped working session in a Totebox Archive and navigate the session lifecycle

## Machine authorization

These guides cover the cryptographic device pairing that controls platform access.

- [[pair-a-new-device]] — the core pairing workflow; covers all four pairing types (ADMIN, INPUT, USER, INTERFACE) and how to verify and revoke

For the authorization model that underpins pairing, see [[machine-based-auth]] and [[pairing-as-permission]].

## Integration & data

These guides cover consuming platform data and connecting external applications.

- [[build-a-colocation-map]] — authenticate against the GIS tile API and render tier-coloured cluster markers in MapLibre
- [[authenticate-binary-downloads]] — verify Ed25519-signed binary releases from the private distribution endpoint
- [[federate-archives-via-content-mounts]] — declare a secondary content mount in `knowledge.toml` and access federated articles across instances

## Self-hosting

These guides cover deploying and running platform components on operator-controlled infrastructure.

- [[self-host-a-deployment]] — provision a named deployment instance, start the gateway, and connect it to the upstream platform
- [[run-local-slm-inference]] — start the local SLM service, verify the Doorman health endpoint, and submit inference requests from os-console

## See also

- [[machine-based-auth]] — the machine-based authorization model underlying all platform access
- [[totebox-orchestration-development]] — the session orchestration model that governs how Totebox Archives are used
- [[app-mediakit-knowledge]] — the wiki engine serving this documentation instance
