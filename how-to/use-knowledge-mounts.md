---
schema: foundry-doc-v1
title: "Use declarative knowledge mounts"
slug: use-knowledge-mounts
short_description: "Adds a secondary content repository to a running knowledge instance via a knowledge.toml [[mount]] entry — into the same flat slug namespace as the primary, since no URL-prefix isolation exists."
category: how-to
content_type: how-to
type: how-to
quality: complete
status: active
audience: "Engineers (hands on keyboard); customer operators"
last_edited: 2026-08-06
editor: pointsav-engineering
paired_with: use-knowledge-mounts.es.md
research_trail:
  sources: [pointsav-monorepo app-mediakit-knowledge/src/config.rs (Mount struct), app.rs (router table, primary()/first() bug), content/walk.rs (index build, slug collision), content/render.rs (wikilink resolution)]
  verification_method: "independently source-verified against pointsav-monorepo on 2026-08-06 by reading the Rust source directly, with file:line citations recorded per claim; both prior Correction notes on this guide had already confirmed the field names were wrong, but this pass goes further and confirms the entire URL-prefix/isolation premise is false — mounted content merges into one flat namespace with no isolation mechanism at all, a materially different and more consequential finding than a field-naming fix"
---

## Prerequisites

- A running knowledge instance with a `knowledge.toml` configuration (see [[deploy-knowledge-instance]])
- A second `media-knowledge-*` content repository cloned on the same filesystem
- Terminal access to restart the knowledge service

## Purpose

Add a second content repository to a running instance so its articles are indexed alongside the primary's — a few minutes to configure. Read the whole guide before relying on this in production: the real mechanism has no isolation between mounts, and that's a genuine, currently-unmitigated risk if the two repositories share any slugs.

## Procedure

1. Note the absolute path to the secondary repository:

   ```
   ls /path/to/media-knowledge-projects/
   ```

2. Add a `[[mount]]` entry to `knowledge.toml`. The real schema has exactly three fields — `path`, `role`, and `blueprint_set` — and there is no `prefix` or `label` field:

   ```toml
   [[mount]]
   path = "/path/to/media-knowledge-projects"
   role = "primary"
   blueprint_set = ["TOPIC", "GUIDE"]
   ```

   `role` defaults to `"primary"` if omitted. The first mount with `role = "primary"` supplies the instance's site chrome (its `important-information.md`, `categories.yaml`, and `redirects.yaml`) — that is the only thing `role` currently affects. `blueprint_set` is parsed but not currently enforced anywhere in the engine; don't rely on it to restrict which article types get served.

   > **Warning:** every mount's articles are indexed into one shared, flat slug namespace — there is no URL prefix, no per-mount routing, and no isolation of any kind. If both repositories contain an article with the same slug, whichever mount is listed later in `knowledge.toml` silently overwrites the earlier one in the index, with no warning at startup. Before adding a mount, check for slug collisions between the two repositories yourself; the engine will not catch them for you.

3. Restart the knowledge service. Configuration and content are both read once at startup — there is no hot-reload:

   ```
   sudo systemctl restart app-mediakit-knowledge
   ```

## Expected outcome

Articles from the secondary repository become reachable at the same `/wiki/<slug>` path pattern as the primary's own articles — not under a separate prefix.

## Verification

Fetch an article you know exists only in the secondary repository, using its plain slug:

```
curl -s http://127.0.0.1:9090/wiki/<slug-from-secondary-repo>/
```

A successful response returns the rendered article. If you get the *wrong* article's content, or content that doesn't match what you expect, that's a slug collision — check both repositories for the same slug and rename one before proceeding.

## Rollback

Remove the `[[mount]]` block from `knowledge.toml` and restart the service. If a collision already occurred, confirm which article was actually served in the meantime before assuming the primary's version was untouched — a shadowed article's own content on disk is never modified by this, only which one the running instance served.

## Next steps

- [[federate-archives-via-content-mounts]] — the broader federation concept this mechanism implements
- [[deploy-knowledge-instance]] — deploying the wiki server that mounts extend

## See also

- [[app-mediakit-knowledge]] — the wiki server architecture, including the content index and render pipeline
