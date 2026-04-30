---
schema: foundry-doc-v1
title: "documentation.pointsav.com Launch — 2026-04-27"
slug: topic-documentation-pointsav-com-launch-2026-04-27
category: reference
type: topic
quality: complete
short_description: "This article records the public launch of documentation.pointsav.com on 2026-04-27 at 16:25 UTC, the serving stack provisioned for that launch, and the forward-looking build trajectory for the wiki engine."
status: pre-build
last_edited: 2026-04-30
editor: pointsav-engineering
cites:
  - ni-51-102
  - osc-sn-51-721
paired_with: topic-documentation-pointsav-com-launch-2026-04-27.es.md
---

# documentation.pointsav.com Launch — 2026-04-27

> This article records the public launch of documentation.pointsav.com on 2026-04-27 at 16:25 UTC, the serving stack provisioned for that launch, and the forward-looking build trajectory for the wiki engine.

**`https://documentation.pointsav.com`** went live with TLS at 16:25 UTC on 2026-04-27 under workspace version v0.1.29. The deployment serves the PointSav engineering wiki (`app-mediakit-knowledge`, the wiki engine shipped under the project-knowledge cluster) over a Let's Encrypt ACME-issued certificate, valid through 2026-07-26, with certbot's automatic renewal scheduled.

The launch closes a path that began in the project-knowledge cluster session 1 (Phase 1 of the wiki engine), continued through session 2 (Phase 1.1 Wikipedia muscle-memory chrome) and session 3 (Phase 2 all 7 steps plus Phase 3 Steps 3.1–3.4), and finished with a Master session at workspace v0.1.29 that rebuilt the binary, installed it at `/usr/local/bin/app-mediakit-knowledge`, created the runtime state directory at `/var/lib/local-knowledge/state`, and fired certbot's nginx integration to obtain the TLS certificate.

## The launch

Six Master-side actions were delivered against the queued redeploy sequence. The binary rebuild took 1 minute 54 seconds. The systemd service entered the `active` state without warnings. Loopback smoke on `127.0.0.1:9090` confirmed all routes returning 200. External smoke on `https://documentation.pointsav.com` confirmed all routes returning 200 — including the HTTP to HTTPS 301 redirect that certbot's nginx automation installed alongside the certificate.

The launch surfaced one previously-undetected gap. The workspace VM ran ufw with `default deny incoming` and only `22/tcp` allowed at the OS layer, despite the GCP firewall already permitting 80 and 443 through the `allow-https-documentation` rule. The first certbot run failed with "Timeout during connect" before the gap was diagnosed. The fix landed at workspace tier in v0.1.29: `infrastructure/configure/configure-ubuntu-foundry.sh` was extended to add `ufw allow 80/tcp` and `ufw allow 443/tcp` rules alongside the existing `22/tcp` rule. Live ufw was updated in the same Master pass before the second certbot run succeeded. The `proofreader.woodfinegroup.com` vhost queued for next is now also unblocked at the OS layer as a consequence.

## What serves today

Four placeholder TOPIC pages render at the public URL. `/wiki/welcome` is the landing TOPIC, explaining the public-preview status and linking to the three sample articles. `/wiki/sample-article` exercises the rendering chrome — table of contents, per-section edit pencils, footer block with categories, masthead band, collapsible left-rail TOC, language switcher, and the Wikipedia muscle-memory layout pattern that Phase 1.1 added. `/wiki/sample-forward-looking` exercises the forward-looking-information cautionary banner and cites both `[ni-51-102]` and `[osc-sn-51-721]` against the workspace citation registry. `/wiki/sample-citations` exercises inline `[citation-id]` references including the clause-reference form.

The full route surface from Phases 1, 1.1, 2, and 3 is operational. Beyond article-rendering paths, the wiki serves: `/healthz` (liveness check); `/` (index page); `/search?q=` (full-text search over BM25 against the on-disk Tantivy index); `/feed.atom` (RFC 4287); `/feed.json` (JSON Feed 1.1); `/sitemap.xml` (sitemaps.org compliant); `/robots.txt` (crawler discovery); `/llms.txt` (llmstxt.org convention for LLM crawlers); and `/git/{slug}` (raw markdown source).

The editor surface from Phase 2 is present in the binary — the `POST /edit/{slug}` route, CodeMirror 6 in-browser editor with markdown highlighting and atomic write semantics, the squiggle linting framework with seven deterministic rules and cited authority hover-cards, citation autocomplete, and the three-keystroke ladder stubs for the Doorman MCP integration that Phase 4 intends to wire up. The collab passthrough relay from Phase 2 Step 7 is present but default-off behind the `--enable-collab` CLI flag.

## Operational substrate

The serving stack is conventional Linux plus nginx plus systemd plus Let's Encrypt, with substrate-specific touches at the boundaries.

**Binary layout.** The `app-mediakit-knowledge` crate compiles to a single binary installed at `/usr/local/bin/app-mediakit-knowledge`. The release build was produced inside the cluster sub-clone at `/srv/foundry/clones/project-knowledge/pointsav-monorepo/app-mediakit-knowledge/` on the `cluster/project-knowledge` feature branch. Build duration was 1 minute 54 seconds for `cargo build --release` from a warm target directory.

**systemd unit.** `/etc/systemd/system/local-knowledge.service` runs the binary as a dedicated unprivileged system user (`local-knowledge:local-knowledge`), bound to the loopback interface on port 9090. Hardening flags include `NoNewPrivileges=true`, `ProtectSystem=strict`, `ProtectHome=true`, `PrivateTmp=true`, and an explicit `ReadWritePaths=` list naming the runtime state directory. The unit's `ExecStart` line invokes the binary with `--content-dir`, `--citations-yaml`, and `--state-dir` flags explicitly. The unit configuration is kept in version control at `~/Foundry/infrastructure/local-knowledge/local-knowledge.service`.

**State directory.** `/var/lib/local-knowledge/state` contains the on-disk Tantivy search index and any future redb databases that Phase 4 intends to introduce for the wikilink graph. The directory is chowned to `local-knowledge:local-knowledge`. The Tantivy index is rebuilt on every binary startup, so a state-directory wipe is non-destructive.

**Content tree.** The current `--content-dir` value points at `/srv/foundry/clones/project-knowledge/content-wiki-documentation/launch-placeholder/`, the four-file placeholder subdirectory the project-knowledge cluster authored before launch. This deliberately avoids exposing the legacy 30-plus TOPIC corpus that lives one directory up; the legacy corpus is held for the project-language cluster's editorial cleanup pass.

**nginx vhost.** Port 443 terminates TLS and reverse-proxies to the loopback service on port 9090. Port 80 serves only the certbot HTTP-01 challenge and otherwise issues a 301 redirect to the equivalent HTTPS URL.

**ufw.** The OS firewall on the workspace VM allows 22/tcp for SSH, 80/tcp for HTTP and ACME challenges, and 443/tcp for HTTPS. The v0.1.29 fix to add 80 and 443 to ufw is described above.

**DreamHost A record.** `documentation.pointsav.com` resolves to the workspace VM's public IPv4 address `34.53.65.203`, configured as a DreamHost-side A record. Operator confirmed the resolution at 2026-04-26T23:00Z prior to the launch session.

**certbot.** The certificate was provisioned via certbot's nginx integration. The HTTP-01 challenge succeeded on the second attempt (the first having timed out at the ufw layer, before the firewall fix). Auto-renewal is enabled via certbot's systemd timer; expiry is 2026-07-26.

## Placeholder posture

The cluster authored the four-file `launch-placeholder/` subtree specifically to enable the public TLS launch without exposing the legacy 30-plus TOPIC corpus inherited from earlier development phases. The legacy corpus carries known editorial debt: language treating the Sovereign Data Foundation as a planned counterparty in current tense, forward-looking framings without the cautionary-banner discipline `[ni-51-102]` requires, and occasional Do-Not-Use vocabulary items. Cleaning these in place would have produced 23 unambiguous edits plus 6 contested operator-decision items, plus a material-change disclosure event for each substantive edit under the workspace's continuous-disclosure posture.

The placeholder posture collapses that surface. Four files, written specifically to be disclosure-clean from the first keystroke, expose only structural prose, only verified facts, and forward-looking framings only inside the explicit demonstration TOPIC where the cautionary-banner pattern is the point of the page. The eventual publication of the refined legacy corpus becomes one material-change event rather than 23 to 30 separate events.

## What's next

The forward-looking framings in this section are planned, not committed. Cautionary language applies per `[ni-51-102]` and `[osc-sn-51-721]`. The reasonable basis is the trajectory of the project-knowledge and project-language clusters as of 2026-04-27; material assumptions include the continued availability of the workspace VM, the project-language cluster's editorial-pipeline ratification per Doctrine claim #35, and operator clearance of the Phase 4 review for the wiki engine.

The project-knowledge cluster plans to author bulk drafts of substantive TOPIC content covering the wiki engine itself, the substrate-native compatibility surface, and the launch milestone narrative. These drafts are intended to enter the editorial gateway via the drafts-outbound input port, where the project-language cluster may refine them to register-conformant, banned-vocabulary-clean, BCSC-grounded posture with bilingual pairs and citation-registry resolution. Refined output would hand off to `content-wiki-documentation` via the existing handoffs-outbound mechanism.

The project-language cluster plans to refine the legacy 30-plus TOPIC corpus over a separate editorial pass. The expected outcome is a ratified content tree to which `--content-dir` may be swapped, producing a single material-change disclosure event.

The wiki engine itself plans further development through Phase 4 (git2 commit-on-edit, history and blame via gix, redb wikilink graph, blake3 hash storage, MCP server via rmcp, smart-HTTP read-only Git remote, OpenAPI 3.1 specification), Phase 5 (image and asset handling), Phase 6 (per-tenant shaping for Customer wikis), Phase 7 (federation and content-addressed retrieval), and Phase 8 (the linter that hardens disclosure-class invariants into compile-time checks).

These plans may shift in response to operator decisions, customer requirements, or substrate-level changes to the doctrine. Material changes to the trajectory will be disclosed via signed commits and CHANGELOG entries on this domain.

## Verification

The following checks are reproducible from any external host with TCP/443 connectivity:

```
$ curl -I https://documentation.pointsav.com/healthz
HTTP/1.1 200 OK
Server: nginx/1.24.0 (Ubuntu)

$ curl https://documentation.pointsav.com/healthz
ok

$ curl -I https://documentation.pointsav.com/wiki/welcome
HTTP/1.1 200 OK

$ curl -I https://documentation.pointsav.com/feed.atom
HTTP/1.1 200 OK

$ curl -I http://documentation.pointsav.com/
HTTP/1.1 301 Moved Permanently

$ openssl s_client -connect documentation.pointsav.com:443 \
    -servername documentation.pointsav.com 2>/dev/null \
    | openssl x509 -noout -dates
notBefore=Apr 27 16:24:00 2026 GMT
notAfter=Jul 26 16:24:00 2026 GMT
```

The certificate's `notBefore` is 16:24Z, one minute before the v0.1.29 inbox message timestamp, reflecting certbot's internal clock; the public-facing launch is the 16:25Z timestamp Master recorded.

The on-substrate IaC paths backing the launch: `infrastructure/local-knowledge/local-knowledge.service` (systemd unit, version-controlled in `~/Foundry`); the inbox-archive entry for v0.1.29 in this cluster's `.claude/inbox-archive.md` (mailbox record of the Master pass that produced the launch); and the workspace `CHANGELOG.md` entry for v0.1.29 (release-engineering record).

## See Also

- [[topic-app-mediakit-knowledge]]
- [[topic-substrate-native-compatibility]]
- [[topic-reverse-funnel-editorial-pattern]]
- [[topic-customer-hostability]]

## References
