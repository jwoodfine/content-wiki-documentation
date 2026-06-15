---
schema: foundry-doc-v1
title: "How to federate archives via content mounts"
slug: federate-archives-via-content-mounts
category: how-to
content_type: how-to
type: how-to
status: stable
last_edited: 2026-06-14
editor: pointsav-engineering
paired_with: federate-archives-via-content-mounts.es.md
---

Content mounts allow one knowledge instance to read article content from a second instance's local path without copying files. The reading instance renders the mounted content as if it were native, with wikilinks resolving within their source graph. This guide covers declaring a secondary mount in `knowledge.toml`, verifying the mount is live, and accessing articles from the federated source.

For the federation architecture, see [[federation-via-content-mounts]]. For the knowledge engine that processes mount declarations, see [[app-mediakit-knowledge]].

## Before you begin

You need:

- Two running `app-mediakit-knowledge` instances on the same host or on hosts
  with a shared filesystem (NFS or equivalent)
- Read access from the primary instance's process user to the secondary
  instance's content directory
- `knowledge.toml` write access on the primary instance

## Step 1: Confirm the secondary content path

On the host running the secondary instance, locate its content directory. The
path is the `content_root` value in the secondary instance's `knowledge.toml`:

```shell
grep content_root /path/to/secondary/knowledge.toml
# example output: content_root = "/srv/wiki/media-knowledge-projects"
```

Confirm the primary instance's process user can read the path:

```shell
sudo -u <wiki-process-user> ls /srv/wiki/media-knowledge-projects
```

If the path is on a remote host, mount it before proceeding. The engine reads
mount sources at startup; a path that is absent at that point causes the mount
to be skipped with a warning in the log.

## Step 2: Declare the mount in `knowledge.toml`

Open the primary instance's `knowledge.toml` and add a `[[mount]]` entry:

```toml
[[mount]]
source = "/srv/wiki/media-knowledge-projects"
prefix = "projects"
```

`source` is the absolute path to the secondary content directory. `prefix` is
an optional namespace string that prevents slug collisions when both instances
define articles with the same slug. With `prefix = "projects"`, an article
with slug `topic-co-location-methodology` in the secondary archive resolves as
`projects/topic-co-location-methodology` in the primary.

Omit `prefix` only when you are certain no slug appears in both instances.

## Step 3: Restart the wiki engine

Apply the configuration by restarting the service:

```shell
sudo systemctl restart app-mediakit-knowledge
```

The engine reads `knowledge.toml` once at startup. A `[[mount]]` entry added
after initial start has no effect until the service restarts.

## Step 4: Verify the mount is live

Check the startup log for the mount confirmation line:

```shell
journalctl -u app-mediakit-knowledge --since "1 minute ago" | grep -i mount
# expected: Mounted secondary archive at prefix=projects (N articles)
```

If the output shows `0 articles`, confirm that the `source` path is readable
and contains `.md` files at the expected depth. If the path is absent, the
log line reads `Mount source not found — skipping` rather than a startup error.

## Step 5: Access mounted articles

Navigate the primary instance to confirm articles from the secondary archive
are available. With `prefix = "projects"` and a secondary article at slug
`topic-co-location-methodology`, the URL is:

```
https://<primary-domain>/how-to/projects/topic-co-location-methodology
```

Wikilinks within mounted articles resolve against the secondary archive's own
link graph. A `[[topic-regional-markets-system]]` link inside a mounted
article resolves within the secondary graph, not the primary — cross-graph
links render as red links.

## See also

- [[federation-via-content-mounts]] — the declarative federation architecture and mount model
- [[app-mediakit-knowledge]] — the wiki engine that processes `knowledge.toml` mount declarations
- [[build-a-colocation-map]] — consume location-intelligence data exposed via a mount
- [[self-host-a-deployment]] — provision the instance that will serve federated content
