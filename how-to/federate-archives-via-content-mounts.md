---
schema: foundry-doc-v1
title: "Federate archives via content mounts"
slug: federate-archives-via-content-mounts
short_description: "Federates a second knowledge instance's articles into a running instance through a knowledge.toml [[mount]] entry — a flat, merged namespace with no isolation, not a URL-prefixed federation scheme."
category: how-to
content_type: how-to
type: how-to
quality: complete
status: active
audience: "Engineers (hands on keyboard); customer operators"
last_edited: 2026-08-06
editor: pointsav-engineering
paired_with: federate-archives-via-content-mounts.es.md
research_trail:
  sources: [pointsav-monorepo app-mediakit-knowledge/src/config.rs (Mount struct), app.rs (router table, primary()/first() bug), content/walk.rs (index build, slug collision), content/render.rs (wikilink resolution)]
  verification_method: "independently source-verified against pointsav-monorepo on 2026-08-06 by reading the Rust source directly, with file:line citations recorded per claim; this guide replaces its own prior fictional URL-namespace schema with the real mechanism confirmed while rewriting use-knowledge-mounts.md in the same pass — content mounts are one flat merged namespace, not isolated federated sub-spaces"
---

## Prerequisites

- Two `media-knowledge-*` content repositories on the same filesystem (or a shared mount like NFS)
- Read access from the primary instance's process user to the secondary repository's content directory
- `knowledge.toml` write access on the primary instance

## Purpose

Read a second instance's articles from a running instance without copying files — the mechanism `app-mediakit-knowledge` calls a content mount. This is narrower than a "federation" in the isolated, namespaced sense the term usually implies: mounted content joins the same flat slug space as everything else the instance already serves.

## Procedure

1. On the host running the secondary content, confirm the primary instance's process user can read it:

   ```
   sudo -u <wiki-process-user> ls /srv/wiki/media-knowledge-projects
   ```

   If the path is on a remote host, mount it locally first. A path that's absent at startup causes the mount to be skipped, not to error.

2. Declare the mount in the primary instance's `knowledge.toml`. See [[use-knowledge-mounts]] for the full mechanical steps and the real `Mount` schema (`path`, `role`, `blueprint_set` — no URL-prefix field exists).

3. Restart the primary instance. Both the config and the mounted content are read once, at startup — changes on either side require a restart to take effect.

4. Access an article from the mounted repository at the same `/wiki/<slug>` path pattern the primary uses for its own articles — there is no separate namespace or prefix to navigate to.

## Expected outcome

The primary instance serves both its own articles and the mounted repository's articles, indistinguishably, from one merged content index.

## Verification

Confirm an article you know exists only in the mounted repository resolves correctly, and — critically — confirm neither repository has an article with a slug the other one also uses. See [[use-knowledge-mounts]]'s verification steps for exactly how to check.

> **Warning:** wikilinks inside mounted articles resolve into the same merged namespace as everything else, with no existence check — a `[[some-slug]]` link works if that slug exists anywhere across every mount, and produces a dead link if it doesn't, regardless of which repository originally contained it. Don't assume a mounted article's internal links stay scoped to its own source repository.

## Rollback

Remove the `[[mount]]` entry and restart. See [[use-knowledge-mounts]] for what to check if a slug collision already shadowed an article before you noticed.

## Next steps

- [[use-knowledge-mounts]] — the full step-by-step mechanics and the real schema
- [[deploy-knowledge-instance]] — provision the instance that will serve federated content

## See also

- [[app-mediakit-knowledge]] — the wiki engine that processes mount declarations
