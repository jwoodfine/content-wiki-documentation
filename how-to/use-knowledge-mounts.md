---
schema: foundry-doc-v1
title: "How to use declarative knowledge mounts"
slug: use-knowledge-mounts
short_description: "Adds a secondary content repository to a running knowledge instance through a knowledge.toml mount, serving its articles under a URL prefix after a restart."
category: how-to
content_type: how-to
type: how-to
status: active
last_edited: 2026-07-18
editor: pointsav-engineering
paired_with: use-knowledge-mounts.es.md
---

Knowledge mounts allow a single wiki instance to serve content from multiple source repositories under a unified URL space. A mount is declared in `knowledge.toml` — the instance reads the source path at startup and makes its articles available at the configured category prefix. This guide covers adding a secondary content mount to an existing instance.

For the federation architecture that mounts enable, see [[federate-archives-via-content-mounts]]. For deploying the wiki server in the first place, see [[deploy-knowledge-instance]].

**Major correction (2026-07-18):** the mount schema and URL-prefix behavior this guide
describes do not match the live `app-mediakit-knowledge` source (same source verified for
[[deploy-knowledge-instance]]'s correction). The real TOML array-of-tables key is
`[[mount]]` (singular — `#[serde(rename = "mount")]`), not `[[mounts]]` used throughout
this guide. The real `Mount` struct has exactly three fields: `path`, `role` (default
`"primary"`; the doc comment states "First primary mount is editable; guide mounts are
read-only" — a two-value editability flag, not a URL namespace), and `blueprint_set` (a
list of allowed article types, e.g. `["TOPIC", "GUIDE"]`). **There is no `prefix` field
and no `label` field anywhere in the real schema** — Step 2's `prefix = "projects"` /
`label = "Projects"` example and Step 4's `/projects/<slug>` URL-prefix verification
describe a mechanism (per-mount URL namespacing) this code does not appear to implement;
the real `role` field governs editability, not routing. There is also no `[content]`
block to add the mount "after" (see the linked correction on [[deploy-knowledge-instance]]
for that schema's real shape). **Flagged, not silently rewritten** — the real mount
model may route by a different, unverified mechanism (or may not yet support multi-source
URL-prefixed serving at all); needs project-totebox or project-knowledge confirmation of
how `[[mount]]` entries actually surface in routing before this guide's steps are
corrected.

## Prerequisites

- A running knowledge instance with a `knowledge.toml` configuration (see [[deploy-knowledge-instance]])
- A second `media-knowledge-*` content repository cloned on the same host
- Terminal access to restart the knowledge service

## Step 1: Identify the secondary content path

The secondary content repository must be a `media-knowledge-*` clone on the same filesystem as the running instance. Note its absolute path:

```
ls /path/to/media-knowledge-projects/
```

Confirm it has a valid `index.md` and category subdirectories before adding the mount — the wiki server will warn at startup if the mount path is empty or malformed.

## Step 2: Add the mount to knowledge.toml

Open `knowledge.toml` and add a `[[mounts]]` section after the `[content]` block:

```toml
[content]
primary_path = "/path/to/media-knowledge-documentation"
instance_name = "documentation"

[[mounts]]
path = "/path/to/media-knowledge-projects"
prefix = "projects"
label = "Projects"
```

`path` is the absolute filesystem path to the secondary repository. `prefix` is the URL prefix under which the mounted content will appear (e.g., mounted articles are served at `/projects/<slug>`). `label` appears in the navigation header to identify the mounted section.

Multiple mounts are supported — add additional `[[mounts]]` sections for each secondary repository.

## Step 3: Restart the knowledge instance

The mount configuration is read at startup. Restart the service for the new mount to take effect:

```
sudo systemctl restart app-mediakit-knowledge
```

Or if running directly:

```
# stop the running process, then:
app-mediakit-knowledge --config knowledge.toml
```

## Step 4: Verify the mount is serving

Fetch an article from the mounted category:

```
curl -s http://127.0.0.1:9090/projects/<slug-from-media-knowledge-projects>/
```

A successful response returns the rendered article HTML. If the response is 404, check:

1. The `prefix` in `knowledge.toml` matches the URL path segment you used
2. The `path` points to a directory with a `_index.md` in at least one subdirectory
3. The service restarted cleanly (check `journalctl -u app-mediakit-knowledge`)

## Step 5: Confirm wikilink isolation

Wikilinks inside mounted content resolve against the mounted repository's own slug namespace. A `[[slug]]` in a projects article will NOT resolve against a documentation article's slug — each mount is isolated. Cross-mount links must use full URLs.

This isolation is by design: the three live instances (documentation, projects, corporate) serve distinct editorial domains; mixing their slug namespaces would cause resolution conflicts.

## Key takeaways

- Mounts extend a running instance with content from a second repository, served under a URL prefix
- Mount configuration lives in `knowledge.toml` under `[[mounts]]`; restart is required after changes
- Wikilink resolution is per-mount — `[[slug]]` in a mounted section resolves against that section's slugs only
- Multiple mounts are supported; add one `[[mounts]]` block per additional repository

## See also

- [[federate-archives-via-content-mounts]] — the federation architecture that declarative mounts implement
- [[deploy-knowledge-instance]] — deploying the wiki server that mounts extend
- [[app-mediakit-knowledge]] — the wiki server architecture including the mount and render pipeline
- [[export-structured-data]] — exporting article content from a mounted repository via the wiki API
