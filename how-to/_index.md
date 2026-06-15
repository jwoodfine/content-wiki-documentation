---
schema: foundry-doc-v1
title: "Developer Guides"
slug: how-to
category: how-to
content_type: how-to
type: topic
status: active
last_edited: 2026-06-14
editor: pointsav-engineering
paired_with: _index.es.md
---

Step-by-step developer guides for building with and on the PointSav platform. Each guide addresses a specific task — follow it start to finish, then refer back to the related architecture articles when you need the underlying theory.

For the concepts behind each guide, start in [[architecture]] or [[patterns]]. For platform architecture overview, see [[totebox-orchestration-development]].

## Getting started

The foundation: authenticate your device and open your first session.

- [[pair-a-new-device|Pair a new device]] — enroll a machine using machine-based authorization; no username or password required
- [[open-first-totebox-session|Open your first Totebox session]] — navigate to an archive, read your inbox, and start contributing

## Machine authorization

Credential and access control operations.

- [[pair-a-new-device|Pair a new device]] — the core enrollment flow
- [[authenticate-binary-downloads|Authenticate binary downloads]] — verify and fetch signed binaries from the private distribution endpoint

## Integration & data

Connect external data pipelines and build location-intelligence applications.

- [[build-a-colocation-map|Build a co-location map]] — query the GIS engine API and render a MapLibre cluster layer
- [[federate-archives-via-content-mounts|Federate archives via content mounts]] — mount wiki content from one archive into a second instance using declarative TOML mounts

## Self-hosting

Deploy the platform on your own infrastructure.

- [[self-host-a-deployment|Self-host a deployment]] — provision a Totebox Archive on a supported compute node
- [[run-local-slm-inference|Run local SLM inference]] — route inference through Doorman to the on-premises language model

## See also

- [[architecture/_index|Architecture]] — cross-cutting platform architecture
- [[patterns/_index|Patterns]] — named design patterns used across the platform
- [[totebox-session]] — what a Totebox session is and what it can do
- [[machine-based-auth]] — how machine-based authorization works
