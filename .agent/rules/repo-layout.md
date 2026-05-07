# Repo layout — content-wiki-documentation

> Defines allowed files at repo root and inside category directories,
> where misplaced items belong, and the defect-closure procedure.
> Companion to `content-contract.md` (which governs file *contents*);
> this file governs file *placement*.

Last updated: 2026-05-03.

---

## 1. Root allowed-files list

Only the following may appear at repo root:

| File / directory | Purpose |
|---|---|
| `README.md` | English project overview (GitHub landing) |
| `README.es.md` | Spanish project overview (bilingual per workspace §6) |
| `LICENSE` | Repository licence (CC-BY-4.0 per factory-release-engineering v1.0.1) |
| `CODE_OF_CONDUCT.md` | Governance scaffold |
| `CHANGELOG.md` | Meaningful-change log (create when first entry lands) |
| `NEXT.md` | Repo-scope open items |
| `AGENT.md` | Repo-level session guide |
| `.gitignore` | Untracked-file rules |
| `.git/` | Git metadata |
| `.github/` | Issue templates, workflows, profile material |
| `.agent/` | Local rule files (see §4 of `AGENT.md`) |
| `index.md` | Wiki home (served at `/` by app-mediakit-knowledge) |
| `featured-topic.yaml` | Homepage featured article selection (YAML pointer to a slug) |

Anything else at repo root is a layout defect until closed.

## 2. Category directory layout

Below repo root, content lives in **category directories**. Each
category directory contains:

| File | Purpose |
|---|---|
| `_index.md` | Category landing page (served at `/<category>`) |
| `<slug>.md` | Articles or Guides, one per file, filename stem == slug |

Category directory names are lowercase kebab-case. Depth is strictly
two — no nested subcategory directories (see `content-contract.md`
§2 for the reasoning).

Binaries, images, CSVs, YAML-only structured records, and code do
not live inside category directories.

## 3. Where misplaced items belong

When a file is found at repo root or inside a category directory
and does not fit the allowed lists above, route it to its proper
home:

| Found | Route to |
|---|---|
| Source code (Rust, Python, TypeScript, etc.) | `pointsav-monorepo/<prefix>-<name>/` — via outbox in `handoffs-outbound.md` |
| Compiled binaries, `.zip`, `.tar.gz` archives | Never check in. If the file is the input to a migration, handoff its extracted contents per §9. |
| Design-system material (tokens, component specs, brand guidelines) | `pointsav-design-system/` — via outbox |
| Operational scripts, tool-*.sh | `~/Foundry/bin/` workspace root (Master Claude scope) |
| YAML-only structured records without Markdown bodies | Classify per `cleanup-log.md`: become article, become article front-matter, or cross-repo move |
| Images used inline in articles | `<category>/<slug>.assets/` alongside the article (to be specified — not yet in contract) |
| Large reference PDFs / research dumps | Not this repo. Consider `pointsav-media-assets` or out-of-repo storage. |
| **Operational Guides (`guide-*.md`)** | Misplaced guides in other repos (e.g. `content-wiki-projects`) MUST be moved here. |

## 4. Defect-closure procedure

When a layout defect is identified:

1. **Identify.** Record the file path and the rule it violates in
   `cleanup-log.md` as a dated `Open` entry.
2. **Determine correct home.** Use the table in §3 above. If
   ambiguous, surface the question in the same cleanup-log entry
   rather than guessing.
3. **Move.**
   - Intra-repo moves: `git mv <old> <new>`; update any wikilinks
     that referenced the old slug.
   - Cross-repo moves: open an entry in `handoffs-outbound.md`
     with state `pending-destination-commit`. Do not `git rm` from
     this repo until the destination commit has landed. Follow
     the pattern in workspace §9.
4. **Update callers.** If the moved file was referenced by other
   articles via `[[slug]]`, update those references. If the slug
   itself changed, rewrite every wikilink that pointed at it.
5. **Log closure.** Move the cleanup-log entry from `Open` to the
   closed section with a dated close line.

**Rules are not loosened to accommodate misplaced files.** If a
file does not fit, move it. If the rule itself is wrong, propose
the rule change explicitly in `cleanup-log.md` and surface it for
decision before rewriting the rule.

## 5. Existing layout state (as of 2026-04-23)

The repo is in a transitional state. Pre-existing files at repo
root that predate this layout rule:

- Markdown topic files (`topic-*.md`, `TOPIC-*.md`, `TOPIC_*.md`)
  — migrate into category directories as normalisation proceeds.
- YAML structured records (`topic-*.yaml`, `sys-adr-*.yaml`,
  `service-*-01.yaml`, `os-workplace-01.yaml`) — classify per §3.
- `glossary-documentation.csv` — classify per §3; CSVs have no
  contracted home today.
- `README-pointsav-wiki.md` — redundant with `README.md`?
  Classification needed.
- `TOPIC-ARCHITECTURE.md`, `TOPIC-EDGE-01.md`, `TOPIC-STORAGE-01.md`,
  `TOPIC_TELEMETRY_ARCHITECTURE.md`, `TOPIC-TEMPLATE-LEDGER.md`
  — candidates for category `_index.md` promotion.

Each file carries an entry in `cleanup-log.md`. Until closed, their
presence at repo root is a logged defect, not a tolerated state.
