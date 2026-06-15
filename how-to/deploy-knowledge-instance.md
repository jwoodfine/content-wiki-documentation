---
schema: foundry-doc-v1
title: "How to deploy a knowledge instance"
slug: deploy-knowledge-instance
category: how-to
content_type: how-to
type: how-to
status: active
last_edited: 2026-06-14
editor: pointsav-engineering
paired_with: deploy-knowledge-instance.es.md
---

A knowledge instance is a running deployment of `app-mediakit-knowledge` — the wiki server that renders the platform's documentation and project wikis. Deploying an instance means building the binary, writing a `knowledge.toml` configuration file pointing at the content repositories, and starting the service. This guide covers deploying a single-instance wiki from a local content path.

For the three-instance model (documentation, projects, corporate), see [[app-mediakit-knowledge]]. For declarative content mounts, see [[use-knowledge-mounts]].

## Prerequisites

- The `app-mediakit-knowledge` binary built from the monorepo (see [[install-toolchain]])
- One or more `media-knowledge-*` content repository clones on the deployment host
- A deployment port (e.g., 9090) that is not occupied by another service
- A terminal session on the host

## Step 1: Locate the content repository

The wiki server reads Markdown from a local path. Identify the path to the content repository you want to serve:

```
ls ~/Foundry/clones/project-editorial/media-knowledge-documentation/
```

The repository must contain an `index.md` at root and category subdirectories with `_index.md` landing pages. If the content has not yet been cloned, clone it first:

```
git clone git@github.com:pointsav/media-knowledge-documentation.git
```

## Step 2: Write the configuration file

Create `knowledge.toml` in the deployment directory:

```toml
[server]
port = 9090
bind = "0.0.0.0"

[content]
primary_path = "/path/to/media-knowledge-documentation"
instance_name = "documentation"

[search]
enabled = true
index_path = "/var/lib/knowledge/search-index"

[auth]
enabled = false   # set true + configure MBA if editor UI is needed
```

`primary_path` must be an absolute path to a `media-knowledge-*` clone. `instance_name` appears in the rendered header and in log messages — use a short, descriptive value.

## Step 3: Build or locate the binary

If you have not already built the binary, build it from the monorepo:

```
cd ~/Foundry/clones/<your-archive>/pointsav-monorepo
cargo build -p app-mediakit-knowledge --release
```

The binary appears at `target/release/app-mediakit-knowledge`. Copy it to the deployment host if they are different machines.

## Step 4: Start the instance

Run the binary with the configuration file:

```
app-mediakit-knowledge --config knowledge.toml
```

Or start it as a systemd service using the provided unit file template (if available in the deployment). The service logs startup messages: it reads the content path, builds the search index, and starts listening on the configured port.

## Step 5: Verify the instance is serving

Fetch the wiki home page:

```
curl -s http://127.0.0.1:9090/ | head -20
```

The response should contain HTML for the wiki home page rendered from `index.md`. Fetch a category page to confirm article routing:

```
curl -s http://127.0.0.1:9090/architecture/ | grep '<title>'
```

If any page returns a 404, check that `primary_path` in `knowledge.toml` points to a directory containing the expected category folder.

## Key takeaways

- The wiki server reads content directly from the local file path — changes to the content repository appear immediately without a service restart
- `instance_name` in the configuration is the label used in logs and the rendered header
- The search index is built at startup and lives at `index_path` — changing this path requires clearing the old index directory
- Three separate instances with three content paths serve documentation, projects, and corporate wikis independently

## See also

- [[app-mediakit-knowledge]] — the wiki server architecture and the three-instance model
- [[use-knowledge-mounts]] — mounting content from multiple repositories into one instance
- [[install-toolchain]] — building the binary from the monorepo source
- [[self-host-a-deployment]] — the broader deployment procedure of which this is one component
- [[federate-archives-via-content-mounts]] — how to serve content from multiple archives in one instance
