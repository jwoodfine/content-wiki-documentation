---
schema: foundry-doc-v1
title: "How to self-host a deployment"
slug: self-host-a-deployment
category: how-to
content_type: how-to
type: how-to
status: stub
last_edited: 2026-06-14
editor: pointsav-engineering
paired_with: self-host-a-deployment.es.md
---

A PointSav deployment is a named, numbered instance of a gateway configuration provisioned on operator-controlled infrastructure. Each deployment runs the same software distribution substrate as the hosted service, with all data and keys held locally. This guide covers provisioning a new deployment instance, verifying the gateway starts correctly, and connecting it to the upstream platform.

For the deployment architecture, see [[deployment-patterns]] and [[edge-deployment]]. For the software distribution model that supplies signed binaries to your instance, see [[software-distribution-substrate]].

## See also

- [[deployment-patterns]] — gateway configuration patterns and deployment topologies
- [[edge-deployment]] — edge instance architecture and connectivity model
- [[software-distribution-substrate]] — how signed binary releases are delivered
- [[authenticate-binary-downloads]] — verify the binary before running it
- [[configure-doorman]] — wire up the inference gateway after the deployment is running
