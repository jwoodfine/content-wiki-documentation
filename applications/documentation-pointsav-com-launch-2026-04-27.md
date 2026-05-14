---
schema: foundry-doc-v1
title: "documentation.pointsav.com — launch record (2026-04-27)"
slug: documentation-pointsav-com-launch-2026-04-27
category: applications
type: topic
quality: complete
short_description: "The operational record of documentation.pointsav.com going live at 16:25 UTC on 2026-04-27: the serving stack, the BCSC-clean placeholder posture, the ufw gap surfaced and fixed, and the verification surfaces available from any external host."
status: active
audience: vendor-public
bcsc_class: current-fact
language_protocol: PROSE-TOPIC
last_edited: 2026-05-14
editor: pointsav-engineering
paired_with: documentation-pointsav-com-launch-2026-04-27.es.md
cites:
  - ni-51-102
  - osc-sn-51-721
references:
  - id: 1
    text: "documentation.pointsav.com — PointSav engineering documentation wiki."
    url: "https://documentation.pointsav.com/"
  - id: 2
    text: "BCSC NI 51-102 — Continuous Disclosure Obligations."
    url: "https://www.bcsc.bc.ca/securities-law/law-and-policy/instruments-and-policies/5-ongoing-requirements-for-issuers-insiders/current/51-102"
---

`https://documentation.pointsav.com`[^1] went live with TLS at 16:25 UTC on 2026-04-27 under workspace version v0.1.29. The deployment serves the PointSav engineering wiki (`app-mediakit-knowledge`) over a Let's Encrypt ACME-issued certificate, valid through 2026-07-26, with certbot's automatic renewal scheduled.

The launch closes a path that began with Phase 1 of the wiki engine, continued through Phase 1.1 (Wikipedia muscle-memory chrome) and Phase 2 plus Phase 3, and finished with a deployment session that rebuilt the binary from source, installed it at `/usr/local/bin/app-mediakit-knowledge`, created the runtime state directory at `/var/lib/local-knowledge/state`, pointed the systemd unit's `--content-dir` flag at the placeholder content tree, and fired certbot's nginx integration to obtain the TLS certificate.

## The launch

Six deployment actions were executed against the queued redeploy sequence. The binary rebuild took 1 minute 54 seconds. The systemd service entered the `active` state without warnings. Loopback smoke on `127.0.0.1:9090` confirmed all routes returning 200. External smoke on `https://documentation.pointsav.com` confirmed all routes returning 200 — including the HTTP→HTTPS 301 redirect that certbot's nginx automation installed alongside the certificate.

The launch surfaced one previously-undetected gap. The workspace VM ran ufw with `default deny incoming` and only `22/tcp` allowed at the OS layer, despite the GCP firewall already permitting 80 and 443 through the `allow-https-documentation` rule against the `documentation-public` target tag. The first certbot run failed with "Timeout during connect" before the gap was diagnosed. The fix landed at infrastructure level in v0.1.29: `infrastructure/configure/configure-ubuntu-foundry.sh` was extended to add `ufw allow 80/tcp` and `ufw allow 443/tcp` rules alongside the existing `22/tcp` rule, so future VM provisioning inherits these ports. Live ufw was updated in the same deployment pass and verified via `ufw status numbered` before the second certbot run succeeded.

## What serves at launch

Four placeholder article pages render at the public URL. `/wiki/welcome` is the landing article, explaining the public-preview status and linking to the three sample articles. `/wiki/sample-article` exercises the rendering chrome — table of contents, per-section edit pencils, footer block with categories, masthead band, collapsible left-rail TOC, language switcher, and the Wikipedia muscle-memory layout pattern. `/wiki/sample-forward-looking` exercises the forward-looking-information cautionary banner and cites both `ni-51-102` and `osc-sn-51-721` against the citation registry. `/wiki/sample-citations` exercises inline `[citation-id]` references including the clause-reference form (`[c2sp-tlog-tiles §2]`).

The full route surface from Phases 1, 1.1, 2, and 3 is operational. Beyond the article-rendering paths, the wiki serves: `/healthz` (liveness check returning the literal string `ok`); `/` (the index page listing all articles); `/search?q=` (full-text search over BM25 against the on-disk Tantivy index at `/var/lib/local-knowledge/state/search/`); `/feed.atom` (RFC 4287 syndication feed); `/feed.json` (JSON Feed 1.1); `/sitemap.xml` (sitemaps.org compliant); `/robots.txt` (crawler discovery); `/llms.txt` (LLM crawler convention); and `/git/{slug}` (raw markdown source).

The editor surface from Phase 2 is present in the binary — the `POST /edit/{slug}` route, CodeMirror 6 in-browser editor with markdown highlighting and atomic write semantics, the squiggle linting framework with seven deterministic rules and cited authority hover-cards, citation autocomplete, and the three-keystroke ladder stubs for the Doorman MCP integration that Phase 4 is planned to wire. The collab passthrough relay from Phase 2 Step 7 is present but default-off behind the `--enable-collab` CLI flag; the production deployment does not currently load any Yjs JavaScript and does not expose the WebSocket route.

## Operational substrate

The serving stack is conventional Linux + nginx + systemd + Let's Encrypt, with substrate-specific touches at the boundaries.

**Binary layout.** The `app-mediakit-knowledge` crate compiles to a single binary installed at `/usr/local/bin/app-mediakit-knowledge`. Build duration was 1 minute 54 seconds for `cargo build --release` from a warm target directory. The binary is installed mtime-stamped 2026-04-27 16:16Z.

**systemd unit.** `/etc/systemd/system/local-knowledge.service` runs the binary as a dedicated unprivileged system user (`local-knowledge:local-knowledge`), bound to the loopback interface on port 9090. Hardening flags include `NoNewPrivileges=true`, `ProtectSystem=strict`, `ProtectHome=true`, `PrivateTmp=true`, and an explicit `ReadWritePaths=` list naming the runtime state directory at `/var/lib/local-knowledge/state`. The unit's `ExecStart` line invokes the binary with `--content-dir`, `--citations-yaml`, and `--state-dir` flags explicitly, plus matching environment variables for redundancy. The unit is version-controlled as Infrastructure-as-Code at `infrastructure/local-knowledge/local-knowledge.service`.

**State directory.** `/var/lib/local-knowledge/state` contains the on-disk Tantivy search index and any future redb databases that Phase 4 is planned to introduce for the wikilink graph. The Tantivy index is rebuilt on every binary startup, so a state-directory wipe is non-destructive — the canonical content is the markdown tree, not the index.

**Content tree.** The launch `--content-dir` points at the four-file placeholder subdirectory. This deliberately avoids exposing the legacy 30+ article corpus held for editorial review; that corpus's `--content-dir` swap will be a single systemd reload once the corpus is ready.

**nginx vhost.** Port 443 terminates TLS and reverse-proxies to the loopback service on port 9090. Port 80 serves only the certbot HTTP-01 challenge and otherwise issues a 301 redirect to the equivalent HTTPS URL.

**ufw.** The OS firewall on the workspace VM allows 22/tcp for SSH, 80/tcp for HTTP and ACME challenges, and 443/tcp for HTTPS. The v0.1.29 fix to add 80 and 443 is described in the previous section.

**DreamHost A record.** `documentation.pointsav.com` resolves to the workspace VM's public IPv4 address `34.53.65.203`, configured as a DreamHost-side A record. Confirmed resolving at 2026-04-26T23:00Z prior to the launch session.

**certbot.** The certificate was provisioned via certbot's nginx integration — `certbot --nginx -d documentation.pointsav.com --email open.source@pointsav.com --agree-tos --no-eff-email`. Auto-renewal is enabled via certbot's systemd timer; expiry is 2026-07-26.

## The placeholder posture — BCSC-clean by construction

The four-file `launch-placeholder/` subtree was authored specifically to enable the public TLS launch without exposing the legacy 30+ article corpus inherited from earlier development phases. The legacy corpus carries known editorial debt — language treating the Sovereign Data Foundation as a current equity holder rather than a planned counterparty, forward-looking framings without the cautionary-banner discipline NI 51-102[^2] requires, and occasional vocabulary items from the workspace language policy. Cleaning these in place would have produced 23 unambiguous edits plus 6 operator-decision items, plus a material-change disclosure event for each substantive edit under the continuous-disclosure posture.

The placeholder posture collapses that surface. Four files, written specifically to be BCSC-clean from the first keystroke, expose only structural prose (no business-outcome claims), only verified facts (certificate dates, route names), and forward-looking framings only inside the explicit demonstration article (`sample-forward-looking.md`) where the cautionary-banner pattern is the point of the page. The eventual publication of the refined corpus becomes ONE material-change event ("first publication of corpus") rather than 23 to 30 separate events.

The placeholder discipline is operationally cheap. The four files exercise every Phase 2 and Phase 3 UI surface a single-tenant operator would see in the first browsing session — the index list, article rendering, the FLI cautionary banner, citation references, search hits, Atom and JSON Feed entries, sitemap entries, raw markdown via `/git/{slug}`. UI/UX evaluation can proceed against the live URL without depending on the corpus cleanup timeline.

The pattern is generalisable. Any future deployment that depends on a corpus being editorially ready can launch with a placeholder content tree, swap `--content-dir` once the corpus is ratified, and avoid the all-or-nothing flip. The substrate's source-of-truth inversion (the markdown tree is canonical; the running binary is a view) makes this swap a single systemd reload.

## What is planned next

The forward-looking framings in this section are *planned*, not *committed*. Cautionary language applies per [ni-51-102] and [osc-sn-51-721].

The editorial pipeline *plans* to refine the legacy 30+ article corpus over a separate pass. The expected outcome is a ratified content tree to which `--content-dir` *may* be swapped, producing a single material-change disclosure event.

The wiki engine *plans* further development through Phase 4 (git2 commit-on-edit, history and blame via gitoxide, redb wikilink graph, blake3 hash storage as a federation seam, MCP server, smart-HTTP read-only Git remote, OpenAPI 3.1 specification), Phase 5 (image and asset handling), Phase 6 (per-tenant shaping for customer wikis), Phase 7 (federation and content-addressed retrieval against the blake3 substrate), and Phase 8 (the linter that hardens disclosure-class invariants into compile-time checks). The Phase 4 plan awaits operator clearance of seven open questions before implementation begins.

These plans *may* shift in response to operator decisions, customer requirements, or substrate-level changes. Material changes to the trajectory will be disclosed via signed commits and changelog entries on this domain.

## Verification

The following checks are reproducible from any external host with TCP/443 connectivity and a recent OpenSSL or curl:

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

The certificate's `notBefore` is 16:24Z, one minute before the v0.1.29 launch timestamp, reflecting the certbot internal clock; the public-facing launch is the 16:25Z timestamp recorded in the deployment.

## See also

- [[app-mediakit-knowledge]] — the wiki engine architecture, route surface, and build phases
- [[source-of-truth-inversion]] — the canonical / view / ephemeral pattern this deployment embodies
- [[collab-via-passthrough-relay]] — the WebSocket relay implementation (default-off at launch)
