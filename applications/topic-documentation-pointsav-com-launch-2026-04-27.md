---
schema: foundry-topic-v1
status: published
last_edited: 2026-04-30
category: applications
audience: vendor-public
bcsc_class: current-fact
language_protocol: PROSE-TOPIC
cites:
  - ni-51-102
  - osc-sn-51-721
references:
  - https://documentation.pointsav.com/
  - https://documentation.pointsav.com/healthz
  - ~/Foundry/CHANGELOG.md (workspace v0.1.29 entry, 2026-04-27)
  - ~/Foundry/infrastructure/local-knowledge/local-knowledge.service
---

`https://documentation.pointsav.com` went live with TLS at 16:25 UTC on 2026-04-27 under workspace version v0.1.29. The deployment serves the PointSav engineering wiki (`app-mediakit-knowledge`) over a Let's Encrypt ACME-issued certificate, valid through 2026-07-26, with certbot's automatic renewal scheduled.

The launch closes a path that began in the project-knowledge cluster session 1 (Phase 1 of the wiki engine), continued through session 2 (Phase 1.1 Wikipedia muscle-memory chrome) and session 3 (Phase 2, all 7 steps, plus Phase 3 Steps 3.1–3.4), and finished with a Master session at workspace v0.1.29 that rebuilt the binary from cluster HEAD, installed it at `/usr/local/bin/app-mediakit-knowledge`, created the runtime state directory at `/var/lib/local-knowledge/state`, pointed the systemd unit's `--content-dir` flag at the placeholder content tree, and ran certbot's nginx integration to obtain the TLS certificate.

The binary rebuild took 1 minute 54 seconds. The systemd service entered the `active` state without warnings. Loopback smoke on `127.0.0.1:9090` confirmed all routes returning 200. External smoke on `https://documentation.pointsav.com` confirmed all routes returning 200 — including the HTTP→HTTPS 301 redirect that certbot's nginx automation installed alongside the certificate.

## The gap the launch surfaced

The launch surfaced one previously-undetected gap. The workspace VM ran ufw with `default deny incoming` and only `22/tcp` allowed at the OS layer, despite the GCP firewall already permitting 80 and 443 through the `allow-https-documentation` rule against the `documentation-public` target tag. The first certbot run failed with "Timeout during connect" before the gap was diagnosed.

The fix landed at workspace tier in v0.1.29: `infrastructure/configure/configure-ubuntu-foundry.sh` was extended to add `ufw allow 80/tcp` and `ufw allow 443/tcp` rules alongside the existing `22/tcp` rule, so future VM provisioning inherits these ports. Live ufw was updated in the same Master pass and verified via `ufw status numbered` before the second certbot run succeeded. The `proofreader.woodfinegroup.com` vhost queued for next was also unblocked at the OS layer as a consequence.

The specific reason this gap had escaped earlier observation: the v0.1.21 deployment had only been smoke-tested from inside the VM and from internal hosts on the same VPC, both of which bypass the OS firewall layer.

## What serves today

Four placeholder TOPIC pages render at the public URL. `/wiki/welcome` is the landing TOPIC, explaining the public-preview status and linking to the three sample articles. `/wiki/sample-article` exercises the rendering chrome — table of contents, per-section edit pencils, footer block with categories, hatnote, collapsible left-rail TOC, language switcher, and the Wikipedia muscle-memory layout that Phase 1.1 added. `/wiki/sample-forward-looking` exercises the forward-looking-information cautionary banner, citing both `ni-51-102` and `osc-sn-51-721` against the workspace citation registry. `/wiki/sample-citations` exercises inline `[citation-id]` references including the clause-reference form (`[c2sp-tlog-tiles §2]`).

The full route surface from Phases 1, 1.1, 2, and 3 is operational. Beyond the article-rendering paths, the wiki serves: `/healthz` (liveness check returning the literal string `ok`); `/` (the index page listing all articles); `/search?q=` (full-text search over BM25 against the on-disk Tantivy index at `/var/lib/local-knowledge/state/search/`); `/feed.atom` (RFC 4287 syndication feed); `/feed.json` (JSON Feed 1.1); `/sitemap.xml` (sitemaps.org compliant); `/robots.txt` (crawler discovery); `/llms.txt` (the llmstxt.org convention for LLM crawlers); and `/git/{slug}` (raw markdown source).

The editor surface from Phase 2 is present in the binary — the `POST /edit/{slug}` route, CodeMirror 6 in-browser editor with atomic write semantics, the squiggle linting framework with seven deterministic rules, citation autocomplete, and the three-keystroke ladder stubs for the Doorman MCP integration that Phase 4 is planned to wire up. The collab passthrough relay from Phase 2 Step 7 is present but default-off behind `--enable-collab`; the production deployment does not currently load any Yjs JavaScript.

## Operational substrate

The serving stack is conventional Linux + nginx + systemd + Let's Encrypt, with substrate-specific touches at the boundaries.

**Binary layout.** The app-mediakit-knowledge crate compiles to a single binary installed at `/usr/local/bin/app-mediakit-knowledge`. The release build was produced inside the cluster sub-clone on the `cluster/project-knowledge` feature branch.

**systemd unit.** `/etc/systemd/system/local-knowledge.service` runs the binary as a dedicated unprivileged system user (`local-knowledge:local-knowledge`), bound to the loopback interface on port 9090. Hardening flags include `NoNewPrivileges=true`, `ProtectSystem=strict`, `ProtectHome=true`, `PrivateTmp=true`, and an explicit `ReadWritePaths=` list naming the runtime state directory. The unit's `ExecStart` line invokes the binary with `--content-dir`, `--citations-yaml`, and `--state-dir` flags explicitly. The unit configuration is version-controlled as Infrastructure-as-Code at `~/Foundry/infrastructure/local-knowledge/local-knowledge.service`.

**State directory.** `/var/lib/local-knowledge/state` contains the on-disk Tantivy search index and any future redb databases Phase 4 is planned to introduce. The Tantivy index is rebuilt on every binary startup, so a state-directory wipe is non-destructive.

**Content tree.** The current `--content-dir` value points at the four-file placeholder subdirectory the project-knowledge cluster authored before launch. This deliberately avoids exposing the legacy 30+ TOPIC corpus; the legacy corpus is held for the project-language editorial cleanup pass.

**nginx vhost.** Port 443 terminates TLS and reverse-proxies to the loopback service on port 9090. Port 80 serves only the certbot HTTP-01 challenge and otherwise issues a 301 redirect to the equivalent HTTPS URL.

**certbot.** The certificate was provisioned via certbot's nginx integration. The HTTP-01 challenge succeeded on the second attempt (the first having timed out at the ufw layer, before the firewall fix). Auto-renewal is enabled via certbot's systemd timer; expiry is 2026-07-26.

**DNS.** `documentation.pointsav.com` resolves to the workspace VM's public IPv4 address `34.53.65.203`, configured as a DreamHost-side A record.

## The placeholder posture — disclosure discipline by construction

The cluster authored the four-file `launch-placeholder/` subtree to enable the public TLS launch without exposing the legacy 30+ TOPIC corpus inherited from earlier development phases. The legacy corpus carries known editorial debt — language treating the Sovereign Data Foundation as a current equity holder rather than a planned counterparty, forward-looking framings without the cautionary-banner discipline NI 51-102 requires, and occasional Do-Not-Use vocabulary items from the workspace language policy.

The placeholder posture collapses the disclosure surface. Four files, written specifically to be BCSC-clean from the first keystroke, expose only structural prose (no business-outcome claims), only verified facts (cert dates, route names), and forward-looking framings only inside the explicit demonstration TOPIC (`sample-forward-looking.md`) where the cautionary-banner pattern is the point of the page. The eventual publication of the refined legacy corpus becomes one material-change event ("first publication of corpus") rather than 23 to 30 separate events.

The pattern is generalisable. Any future deployment that depends on a corpus being editorially ready can launch with a placeholder content tree, swap `--content-dir` once the corpus is ratified, and avoid the all-or-nothing flip. The substrate's source-of-truth inversion makes this swap a single systemd reload.

## Verification

The following checks are reproducible from any external host with TCP/443 connectivity.

```
$ curl -I https://documentation.pointsav.com/healthz
HTTP/1.1 200 OK

$ curl https://documentation.pointsav.com/healthz
ok

$ curl -I https://documentation.pointsav.com/wiki/welcome
HTTP/1.1 200 OK

$ curl -I http://documentation.pointsav.com/
HTTP/1.1 301 Moved Permanently

$ openssl s_client -connect documentation.pointsav.com:443 \
    -servername documentation.pointsav.com 2>/dev/null \
    | openssl x509 -noout -dates
notBefore=Apr 27 16:24:00 2026 GMT
notAfter=Jul 26 16:24:00 2026 GMT
```

The on-substrate IaC paths backing the launch: `infrastructure/local-knowledge/local-knowledge.service` (systemd unit, version-controlled); the inbox-archive entry for v0.1.29 in this cluster's `.claude/inbox-archive.md`; and the workspace `CHANGELOG.md` entry for v0.1.29.

## What is planned next

The forward-looking framings in this section are *planned*, not *committed*. Cautionary language applies per [ni-51-102] and [osc-sn-51-721]. The reasonable basis is the trajectory of the project-knowledge and project-language clusters as of 2026-04-27; material assumptions include the continued availability of the workspace VM and operator clearance of the Phase 4 design review.

The project-knowledge cluster *plans* to author bulk drafts of substantive TOPIC content covering the wiki engine itself, the substrate-native compatibility surface, and the launch milestone narrative. The project-language cluster *plans* to refine the legacy 30+ TOPIC corpus over a separate editorial pass, intended to produce a ratified content tree for which `--content-dir` *may* be swapped — producing a single material-change disclosure event rather than many.

The wiki engine itself *plans* further development through Phases 4–8 (git2 commit-on-edit, history and blame, redb wikilink graph, federation seam, MCP server, OpenAPI 3.1, image handling, per-tenant shaping, disclosure-class linter). These plans *may* shift in response to operator decisions, customer requirements, or substrate-level doctrine changes. Material changes will be disclosed via signed commits and CHANGELOG entries.

## See also

- [[topic-app-mediakit-knowledge]] — the wiki engine architecture
- [[topic-source-of-truth-inversion]] — the canonical / view / ephemeral pattern
- [[topic-substrate-native-compatibility]] — why the Action API shim was dropped

## Provenance

Current-fact narrative, authored 2026-04-27 immediately following the v0.1.29 launch. Cert validity (through 2026-07-26) is verifiable via `openssl s_client` until that date. Public smoke results in the Verification section are reproducible from any external host. Refined by project-language 2026-04-30.

---

*Copyright © 2026 Woodfine Capital Projects Inc. Licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). PointSav™ and Foundry™ are unregistered trademarks of Woodfine Capital Projects Inc.*
