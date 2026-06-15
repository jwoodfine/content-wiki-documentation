---
schema: foundry-doc-v1
title: "How to federate archives via content mounts"
slug: federate-archives-via-content-mounts
category: how-to
content_type: how-to
type: how-to
status: stub
last_edited: 2026-06-14
editor: pointsav-engineering
paired_with: federate-archives-via-content-mounts.es.md
---

Content mounts allow one knowledge instance to read article content from a second instance's local path without copying files. The reading instance renders the mounted content as if it were native, with wikilinks resolving within their source graph. This guide covers declaring a secondary mount in `knowledge.toml`, verifying the mount is live, and accessing articles from the federated source.

For the federation architecture, see [[federation-via-content-mounts]]. For the knowledge engine that processes mount declarations, see [[app-mediakit-knowledge]].

## See also

- [[federation-via-content-mounts]] — the declarative federation architecture and mount model
- [[app-mediakit-knowledge]] — the wiki engine that processes `knowledge.toml` mount declarations
- [[build-a-colocation-map]] — consume location-intelligence data exposed via a mount
- [[self-host-a-deployment]] — provision the instance that will serve federated content
