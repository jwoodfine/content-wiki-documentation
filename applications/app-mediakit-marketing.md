---
schema: foundry-doc-v1
title: "app-mediakit-marketing"
slug: app-mediakit-marketing
category: applications
type: topic
quality: core
status: active
bcsc_class: vendor-public
last_edited: 2026-05-07
editor: pointsav-engineering
cites: []
paired_with: app-mediakit-marketing.es.md
---

`app-mediakit-marketing` is the PointSav marketing landing page server. It delivers
multi-tenant web marketing surfaces from a statically compiled Rust binary backed by
flat-file content, applying a WordPress.org-compatible URL and navigation vocabulary
over the PointSav leapfrog-2030 internal architecture. The application shipped at v0.0.1
MVP in May 2026, serving two simultaneous production deployments on the foundry-workspace
VM.

## Function

The server presents each tenant's public marketing presence at a configurable domain.
WordPress muscle-memory is preserved at the UX layer: the admin interface exposes
Dashboard, Pages, Media, and Themes vocabulary familiar to anyone who has operated a
WordPress site. Internally the application uses no PHP, no MySQL, and no plugin
infrastructure.

Each tenant instance reads content from a configurable flat-file content directory and
serves pages, media assets, and structured metadata over HTTP. A single compiled binary
serves both the Woodfine and PointSav tenants through environment variable configuration.

## Architecture

`app-mediakit-marketing` follows the PointSav leapfrog-2030 pattern:

- **Substrate:** Rust + Axum web framework; statically linked binary
- **Content layer:** Flat-file content directories; no database dependency
- **DataGraph references:** Entity references resolved against the PointSav DataGraph at
  runtime
- **Multi-tenant routing:** Tenant identity (`TENANT_ID`) configured via environment
  variable; a single binary instance serves one tenant
- **WordPress UX surface:** Route vocabulary (`/wp-admin/`, `/wp-admin/post.php`,
  `/wp-admin/upload.php`) and navigation labels match WordPress.org conventions at the
  HTTP layer

## Deployments

Two simultaneous production deployments operate on the foundry-workspace VM:

| Deployment | Tenant | Domain | Port |
|---|---|---|---|
| `media-marketing-landing-1` | Woodfine | home.woodfinegroup.com | 9102 |
| `media-marketing-landing-2` | PointSav | home.pointsav.com | 9101 |

Both instances serve from the same binary, separated by environment variable sets in
each systemd unit.

## Version State

v0.0.1 delivers the core multi-tenant server, WordPress-compatible navigation, and basic
flat-file content serving. DataGraph entity integration, media upload handling, and the
full WordPress-equivalent admin dashboard are planned for subsequent milestones.

## Tier Compatibility

The server is Tier 0 compatible: it runs on a single low-cost VM alongside other
PointSav substrate services without requiring dedicated compute. Both deployments run
concurrently on the foundry-workspace VM (e2-medium, 2 vCPU, 4 GB RAM).

## See Also

- [[app-mediakit-knowledge]]
- [[app-orchestration-bim]]
- [[leapfrog-2030-architecture]]
