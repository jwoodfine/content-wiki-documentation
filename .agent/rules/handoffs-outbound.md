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

*(no open handoffs)*

---

## Closed

### 2026-04-23 — `app-mediakit-knowledge.zip` → `pointsav-monorepo/app-mediakit-knowledge/`

`Closed: 2026-05-08.`

| Field | Value |
|---|---|
| State | `destination-committed` |
| Opened | 2026-04-23 |
| Closed | 2026-05-08 |
| Source | `app-mediakit-knowledge.zip` at this repo's root (untracked) |
| Destination repo | `pointsav-monorepo` |
| Destination path | `app-mediakit-knowledge/` |
| Rationale | Rust crate; `app-*` prefix belongs in monorepo per Nomenclature Matrix §3. |
| Resolution | Crate committed to `pointsav-monorepo/app-mediakit-knowledge/` via Stage 6 promotion in prior sessions. Source ZIP was untracked and has been removed from filesystem. |
