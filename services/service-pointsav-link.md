---
schema: foundry-doc-v1
title: "service-pointsav-link"
slug: service-pointsav-link
short_description: "service-pointsav-link is a named but unbuilt adapter concept for connecting an os-* node to a PointSav fleet — no corresponding package exists in the monorepo today."
category: services
index_group: specialist-and-domain-services
type: topic
content_type: topic
status: stable
bcsc_class: public-disclosure-safe
language: en
paired_with: service-pointsav-link.es.md
last_edited: 2026-08-22
editor: pointsav-engineering
---

`service-pointsav-link` names a concept, not a shipped package: a hot-pluggable adapter that
would connect an `os-*` node to fleet management, translating authority commands into
subject-executable operations. No crate by this name, and no `pointsav-protocol` package,
exists anywhere in the platform's source. The concept appears in internal planning material
with a status of "conceptual" — scoped and named, not built.

## What the design would do

The described shape, as recorded in planning material: a Subject node ships with the adapter
absent by default, so it carries no code capable of initiating contact with an authority. An
operator activates it with a single command, which installs the adapter and registers the
node with a fleet pairing registry. If the adapter crashes or is removed, the Subject keeps
running its own workloads — only the fleet's visibility into it goes dark. This shape, if
built, would be one concrete implementation of the [[diode-standard|Diode Standard]]: an
authority-to-subject channel with no reverse path for commands.

## What exists instead

The platform's real one-directional mechanisms are documented on [[diode-standard]], which
covers each in detail: a pull-and-wipe egress pair, a pull-based telemetry pipeline, an
ingestion component that names its own logic "the ingress diode," and a directional
code-promotion pipeline with hard reverse-flow guards. None of these is the adapter described
here, and none is a general-purpose fleet-command link — each satisfies the one-directional
rule for its own narrow purpose.

Whether this specific adapter is a planned component not yet built, or a design renamed or
superseded by one of those other mechanisms, is an open question flagged for the owning
engineering group. This article does not guess at an answer.

## See also

- [[diode-standard]] — the design rule this adapter would implement, and the real mechanisms
  that follow it today
- [[machine-based-auth]] — how two machines authenticate before any connection, real or
  conceptual, is permitted
- [[os-network-admin]] — the authority side this adapter's design would connect to
