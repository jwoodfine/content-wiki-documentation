---
schema: foundry-doc-v1
title: "Deploy a knowledge instance"
slug: deploy-knowledge-instance
short_description: "Deploys an instance of app-mediakit-knowledge from a local content path: write a knowledge.toml [site] + [[mount]] configuration, build the binary, and start it with the serve subcommand."
category: self-hosting
index_group: getting-the-platform-running
content_type: how-to
type: how-to
quality: complete
status: active
audience: "Engineers (hands on keyboard); customer operators"
last_edited: 2026-08-04
editor: pointsav-engineering
paired_with: deploy-knowledge-instance.es.md
---

## Prerequisites

- The `app-mediakit-knowledge` binary built from the monorepo (see [[install-toolchain]])
- One or more `media-knowledge-*` content repository clones on the deployment host
- A deployment port not occupied by another service (default `127.0.0.1:9090`)
- A terminal session on the host

## Purpose

A knowledge instance is a running deployment of `app-mediakit-knowledge`, the engine that serves the platform's documentation and project wikis. Deploying one means writing a `knowledge.toml` that names a `[site]` and at least one content `[[mount]]`, then starting the binary against it with the `serve` subcommand.

## Procedure

1. Locate or clone the content repository you want to serve:

   ```
   ls ~/Foundry/clones/project-editorial/media-knowledge-documentation/
   ```

   If it isn't cloned yet:

   ```
   git clone git@github.com:pointsav/media-knowledge-documentation.git
   ```

2. Write `knowledge.toml`:

   ```toml
   [site]
   title = "PointSav Documentation"
   brand = "pointsav"            # "pointsav" or "woodfine" — selects the token set
   bind = "127.0.0.1:9090"
   instance = "documentation"    # "documentation" | "projects" | "corporate"

   [[mount]]
   path = "/path/to/media-knowledge-documentation"
   role = "primary"              # the primary mount is editable; others are read-only
   ```

   `[site]` fields other than `title` all have defaults (`brand` → `"pointsav"`, `bind` → `"127.0.0.1:9090"`, `state_dir` → `/var/lib/local-knowledge/state`) — set them explicitly only when they need to differ. `[[mount]]` is repeatable; a second, read-only mount is how a single instance federates content from another archive (see [[use-knowledge-mounts]]).

3. Build the binary, if you don't already have one:

   ```
   cd ~/Foundry/clones/<your-archive>/pointsav-monorepo
   cargo build -p app-mediakit-knowledge --release
   ```

   The binary lands at `target/release/app-mediakit-knowledge`. Copy it to the deployment host if that's a different machine.

4. Start the instance:

   ```
   app-mediakit-knowledge serve --knowledge-toml knowledge.toml
   ```

   `--knowledge-toml` can also be supplied via the `WIKI_KNOWLEDGE_TOML` environment variable, which is the form a systemd unit typically uses. A sibling `check` subcommand (`app-mediakit-knowledge check --knowledge-toml knowledge.toml`) validates the configuration and content without starting a server — useful as a CI gate before deploying a config change.

## Expected outcome

The instance binds to the address in `[site].bind`, reads Markdown directly from every mounted path, and serves the wiki. Content edits in the repository appear on the next request — there is no build or reindex step between an edit and it showing up.

## Verification

Fetch the home page:

```
curl -s http://127.0.0.1:9090/ | head -20
```

The response should contain rendered HTML from the mount's `index.md`. Fetch a category page to confirm routing:

```
curl -s http://127.0.0.1:9090/category/architecture | grep '<title>'
```

If a page 404s, confirm the `path` in `[[mount]]` points at a directory that actually contains the expected category folder, and that `knowledge.toml`'s `check` subcommand passes cleanly first.

## Rollback

Stop the process (or `systemctl stop` the unit, if running as one). No state is written outside `state_dir`; removing or reverting `knowledge.toml` and restarting returns the instance to its prior configuration. The content repository itself is untouched by serving it — reverting a bad content edit is a normal `git` operation in that repo, not a deployment rollback.

## Next steps

- [[use-knowledge-mounts]] — mount a second, read-only content repository into this instance
- [[federate-archives-via-content-mounts]] — serve content from multiple archives through one instance
- [[self-host-a-deployment]] — the broader appliance-image deployment path this instance can run inside

## See also

- [[app-mediakit-knowledge]] — the wiki server architecture and the three-instance model
- [[use-knowledge-mounts]] — mounting content from multiple repositories into one instance
- [[install-toolchain]] — building the binary from the monorepo source
- [[self-host-a-deployment]] — the broader deployment procedure of which this is one component
- [[federate-archives-via-content-mounts]] — how to serve content from multiple archives in one instance
