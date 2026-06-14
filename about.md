---
schema: foundry-doc-v1
title: "About PointSav Knowledge"
slug: about
category: governance
type: governance
content_type: topic
quality: complete
short_description: "PointSav Knowledge is the engineering documentation wiki for the PointSav platform, serving engineers, architects, and institutional readers."
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-27
editor: pointsav-engineering
---

PointSav Knowledge is the engineering documentation wiki for the PointSav platform. It serves engineers, architects, compliance reviewers, and institutional readers who need precise technical reference material.

## What this wiki covers

The wiki documents the PointSav platform as it is designed and built:

- Platform architecture and the design decisions that constrain it
- Substrate concepts — the foundational mechanisms that compose the platform
- Named design patterns recurring across services, applications, and deployments
- Operating systems (`os-*`), autonomous services (`service-*`), and applications (`app-*`)
- Governance — architecture decision records, licensing, contributor model, compliance posture
- Infrastructure — fleet deployment topology, storage, network, telemetry
- Reference material — nomenclature, style guide, glossary

## How it is built

PointSav Knowledge runs on `app-mediakit-knowledge`, a sovereign wiki engine written in Rust. Content is stored as flat Markdown files in a Git repository. The engine provides BM25 full-text search, bilingual routing (English and Spanish), claim-layer citation verification, and a Git-native revision history.

The engine runs on customer hardware under Woodfine Management Corp. It has no dependency on third-party cloud infrastructure for content storage or retrieval.

## Licence

All content in this wiki is licensed under [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).

## Contributing

Contributions to this wiki are welcome. See [[contribute]] for how to propose additions or corrections.

## Contact

[open.source@pointsav.com](mailto:open.source@pointsav.com)
