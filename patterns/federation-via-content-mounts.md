---
schema: foundry-doc-v1
title: "Content mounts and federation"
slug: federation-via-content-mounts
short_description: "The wiki engine renders curated articles committed directly to its repository alongside content mounted from separate local directories, sharing one URL surface and search index."
category: patterns
type: topic
content_type: topic
quality: complete
status: active
audience: vendor-public
bcsc_class: public-disclosure-safe
language_protocol: PROSE-TOPIC
last_edited: 2026-08-22
editor: pointsav-engineering
cites: []
paired_with: federation-via-content-mounts.es.md
index_group: interface-and-user-experience
---

The content-mount pattern combines two authoring modes in a single wiki instance: curated editorial articles committed directly to the knowledge repository, and content mounted from a separate local directory. **A reader browsing the wiki cannot tell which mode produced any given article.** Both render into the same category pages, the same search index, the same navigation, with no visible seam. Local directory mounting is live today; a further extension — mounting content fetched automatically from a remote git repository rather than an already-local path — remains a design direction, not a shipped capability.

## The hybrid model

A deployed wiki instance is configured by a `knowledge.toml` manifest at the content directory root. The manifest declares one or more mounts, each pointing to a local directory, alongside any articles committed directly to the repository. Exactly one mount may hold the `primary` role — the editable article set; any additional mounts are read-only. Both render into the same URL namespace.

Direct commits into the primary mount are the correct choice for content that is editorial in nature — platform reference articles, design-system notes, governance documents — where the knowledge repository is the canonical home and editing flows through the standard staging-tier commit path. A read-only mount is the correct choice for content whose canonical home is a different repository entirely — the wiki surfaces it without taking on editing responsibility for it.

**Why it matters:** a wiki instance can surface content it does not own without ever becoming responsible for editing it — the canonical home stays wherever the content actually lives.

## How mounts work today

A mount entry in `knowledge.toml` declares a local filesystem path, a role (`primary` or read-only), and a `blueprint_set` — a list of content-type names the mount is expected to contain. The engine walks each declared mount's directory at startup and builds its content index from what it finds there; a mount's directory must already exist on disk when the engine starts.

**What this does not yet do: fetch content from a remote repository on the wiki's own initiative.** A mount today is a pointer to an already-present local directory, not a git remote the engine clones or pulls on a schedule. Getting content from a separate repository into a mount's directory is a step performed outside the wiki engine — by whatever process keeps that directory populated — not something the engine does for itself.

**Why it matters:** an operator evaluating this pattern today should expect to keep a mount's directory populated themselves — the engine reads what is already there, it does not go fetch anything on its own yet.

## Blueprints

The `blueprint_set` field lets a mount declare which content types it is expected to hold — `TOPIC` and `GUIDE` are the two names in current use. This is a declared expectation carried in configuration; it does not yet drive content-type-specific validation or routing behavior beyond that declaration.

**Why it matters:** a reader inspecting a mount's configuration can tell what kind of content to expect there without opening a single file — the declaration is the documentation.

## Per-instance isolation

Each wiki instance reads only the mounts declared in its own `knowledge.toml`. Two instances could in principle point their mounts at directories sourced from the same upstream content, and still present entirely different article sets depending on their own mount configuration — isolation is a property of each instance's own configuration, not something coordinated centrally.

**Why it matters:** misconfiguring one wiki instance's mounts can never leak content into, or pull content out of, a second instance — each instance's article set is entirely its own configuration's doing.

## What a remote-fetch extension would add

Extending local-path mounting to remote-repository fetching — the wiki engine cloning and periodically refreshing a git remote into a mount's directory itself, rather than relying on an external process to keep that directory current — is a real design direction for this pattern, not yet built. The natural extension alongside it is per-article provenance metadata (which source repository and path an article came from) and edit-URL routing (sending an editor back to the source repository's own edit path rather than accepting a write locally) — neither of which exists in the mount configuration today.

**Why it matters:** naming this as a planned direction rather than a shipped feature means a reader is never misled into thinking the engine already manages remote repositories on its own.

## Relationship to source-of-truth inversion

This pattern extends [[source-of-truth-inversion]] from a single-repository topology toward a multi-repository one. The invariant is the same: git is canonical, the running binary is a view. What a mount adds is that "the canonical repository" is no longer necessarily the wiki's own repository — a mounted directory's real canonical home can be wherever the process populating it draws from.

**Why it matters:** a reader who already understands source-of-truth inversion does not need a second mental model for mounts — it is the same canonical/view invariant, just with more than one canonical repository in play.

## See also

- [[app-mediakit-knowledge]] — the engine that implements this pattern
- [[source-of-truth-inversion]] — the foundational design choice this pattern extends
- [[knowledge-wiki-leapfrog-architecture]] — the broader IA and navigation philosophy
