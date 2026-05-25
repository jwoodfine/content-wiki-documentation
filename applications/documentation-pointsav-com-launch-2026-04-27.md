---
schema: foundry-doc-v1
title: "documentation.pointsav.com goes live — 2026-04-27"
slug: documentation-pointsav-com-launch-2026-04-27
short_description: "The April 2026 TLS launch of documentation.pointsav.com: serving stack, placeholder posture, BCSC disclosure rationale, and verification commands."
category: applications
type: topic
status: active
bcsc_class: public-disclosure-safe
last_edited: 2026-05-25
editor: pointsav-engineering
paired_with: documentation-pointsav-com-launch-2026-04-27.es.md
cites: [ni-51-102, osc-sn-51-721]
---

# documentation.pointsav.com goes live — 2026-04-27

`https://documentation.pointsav.com` went live with TLS at 16:25 UTC on 2026-04-27. The deployment serves the PointSav engineering wiki over a Let's Encrypt certificate valid through 2026-07-26, with automatic renewal enabled.

---

## What serves today

Four placeholder TOPIC pages render at the public URL. `/wiki/welcome` is the landing topic, explaining the public-preview status. `/wiki/sample-article` exercises the rendering chrome — table of contents, per-section edit pencils, footer block with categories, masthead band, collapsible left-rail table of contents, language switcher, and the Wikipedia layout conventions. `/wiki/sample-forward-looking` exercises the forward-looking-information cautionary banner and cites both [ni-51-102] and [osc-sn-51-721]. `/wiki/sample-citations` exercises inline citation references including the clause-reference form.

Beyond article-rendering paths, the wiki serves: `/healthz` (liveness check); `/` (index page listing all articles); `/search?q=` (full-text search over the on-disk Tantivy index); `/feed.atom` (RFC 4287 syndication feed); `/feed.json` (JSON Feed 1.1); `/sitemap.xml`; `/robots.txt`; `/llms.txt`; and `/git/{slug}` (raw Markdown source).

The editor surface is present in the binary — the `POST /edit/{slug}` route, CodeMirror 6 in-browser editor, citation autocomplete, and the collaborative passthrough relay (default-off, behind `--enable-collab`). The production deployment does not expose the WebSocket route.

---

## Serving stack

**Binary.** A single binary installed at `/usr/local/bin/app-mediakit-knowledge`, built on the cluster feature branch. Build duration was 1 minute 54 seconds.

**systemd unit.** The unit runs the binary as a dedicated unprivileged system user (`local-knowledge:local-knowledge`), bound to the loopback interface on port 9090. Hardening flags include `NoNewPrivileges=true`, `ProtectSystem=strict`, `ProtectHome=true`, and `PrivateTmp=true`.

**Content directory.** The production `--content-dir` flag points at a four-file placeholder subdirectory. The legacy 30+ TOPIC corpus is held in the parent directory pending editorial refinement.

**nginx.** Port 443 terminates TLS and reverse-proxies to the loopback service on port 9090. Port 80 serves only the Let's Encrypt HTTP-01 challenge and issues a 301 redirect to HTTPS.

**OS firewall.** The workspace VM runs ufw. The first certbot run failed because the VM allowed only port 22 at the OS layer, despite the GCP firewall permitting 80 and 443. The fix added `ufw allow 80/tcp` and `ufw allow 443/tcp` to the infrastructure provisioning script so future deployments inherit these ports.

**DNS.** `documentation.pointsav.com` resolves to the workspace VM's public IPv4 address via a DreamHost A record.

---

## Placeholder posture — disclosure rationale

The four-file placeholder subtree was authored specifically to enable the public TLS launch without exposing the legacy TOPIC corpus. The legacy corpus carries known editorial debt: forward-looking framings without cautionary-banner discipline per [ni-51-102], and vocabulary items not compliant with the workspace language policy. Cleaning these in place would have produced numerous unambiguous edits plus a material-change disclosure event under the continuous-disclosure posture for each substantive edit.

The placeholder posture collapses that surface. Four files, written to be clean from the first line, expose only structural prose (no business-outcome claims), only verified facts, and forward-looking framings only inside the explicit demonstration topic where the cautionary-banner pattern is the point of the page. The eventual publication of the refined corpus becomes one material-change event rather than many.

This pattern is generalizable. Any deployment that depends on a corpus being editorially ready can launch with a placeholder content tree, swap `--content-dir` once the corpus is ratified, and avoid an all-or-nothing flip. The source-of-truth inversion — the Markdown tree is canonical; the running binary is a view — makes this swap a single service reload.

---

## Forward-looking items

The following are planned or intended, not committed. Cautionary language applies per [ni-51-102] and [osc-sn-51-721]. Material assumptions include the continued availability of the workspace VM and sustained editorial-pipeline activity.

The editorial pipeline is intended to refine the legacy TOPIC corpus in a separate pass. The expected outcome is a ratified content tree to which `--content-dir` may be swapped, producing a single material-change disclosure event.

The wiki engine is planned for further development through phases covering git2 commit-on-edit, a wikilink graph, a content-addressed federation layer, an MCP server, and a linter that hardens disclosure-class invariants.

---

## Verification

The following checks are reproducible from any external host with TCP/443 connectivity:

```
$ curl -I https://documentation.pointsav.com/healthz
HTTP/2 200

$ curl https://documentation.pointsav.com/healthz
ok

$ curl -I https://documentation.pointsav.com/wiki/welcome
HTTP/2 200

$ curl -I http://documentation.pointsav.com/
HTTP/1.1 301 Moved Permanently

$ openssl s_client -connect documentation.pointsav.com:443 \
    -servername documentation.pointsav.com 2>/dev/null \
    | openssl x509 -noout -dates
notBefore=Apr 27 16:24:00 2026 GMT
notAfter=Jul 26 16:24:00 2026 GMT
```

---

## See Also

- [[app-mediakit-knowledge]]
- [[wikipedia-leapfrog-design]]
- [[source-of-truth-inversion]]
