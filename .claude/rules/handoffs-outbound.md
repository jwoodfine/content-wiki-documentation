# Handoffs outbound — content-wiki-documentation

> Passive outbox for files in this repo that belong in another
> repo per the pattern in workspace §9.
>
> Entries are created by a Root Claude in **this repo** when it
> identifies that a file belongs elsewhere. Entries are moved
> through states by sessions at the appropriate layer:
>
> - `pending-destination-commit` — a Root Claude in the
>   destination repo commits the add-side and updates the entry.
> - `destination-committed` — a later Root Claude session in
>   this repo commits the `git rm` of the source file (or a
>   plain `rm` if the file is untracked) and moves the entry to
>   the closed section below.
>
> Master Claude does not commit in either repo. Its role is
> workspace-level coordination — surfacing pending entries
> during workspace review.

Last updated: 2026-04-23.

---

## Open

### 2026-04-23 — `app-mediakit-knowledge.zip` → `pointsav-monorepo/app-mediakit-knowledge/`

| Field | Value |
|---|---|
| State | `pending-destination-commit` |
| Opened | 2026-04-23 |
| Source | `app-mediakit-knowledge.zip` at this repo's root (untracked) |
| Destination repo | `pointsav-monorepo` |
| Destination path | `app-mediakit-knowledge/` (new top-level crate) |
| Rationale | The ZIP contains a Rust crate. Per Nomenclature Matrix §3, the `app-*` prefix identifies a monorepo project. Crates do not live in content-wiki repos. |
| Notes | Source is untracked, so the close-at-source step is `rm app-mediakit-knowledge.zip` rather than `git rm`. The destination Root Claude extracts the ZIP contents and commits them as a new Active project per workspace §8, with a `CLAUDE.md` and `NEXT.md` per the templates at `~/Foundry/templates/`. The project-registry row is added in the monorepo in the same commit. |
| Reviewer notes | The crate is partially scaffolded — four modules have TODOs (`renderer/toc::extract`, `renderer/footnotes::process_inline`, `renderer/markdown` syntect stage, `search/index::autocomplete`, all `server/handlers` stubs). The destination session takes over implementation from that scaffold state. |

---

## Closed

*(no closed handoffs yet)*
