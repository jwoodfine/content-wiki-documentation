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

Last updated: 2026-05-16.

---

## Open

### 2026-05-16 — design-system/ Batch 1: foundation token docs → `pointsav-design-system/docs/foundations/`

| Field | Value |
|---|---|
| State | `pending-destination-commit` |
| Opened | 2026-05-16 |
| Decision | OPUS editorial analysis (project-editorial session, 2026-05-16); operator-ratified |
| Rationale | Foundation token docs (color, typography, spacing, motion) are token specifications — they pair with the YAML token files in `pointsav-design-system/tokens/` and belong beside them, not in the platform engineering wiki. repo-layout.md §3 routing rule applies. |

**Source files (8 — 4 EN+ES pairs):**

| Source path | Destination path |
|---|---|
| `design-system/design-color.md` | `pointsav-design-system/docs/foundations/design-color.md` |
| `design-system/design-color.es.md` | `pointsav-design-system/docs/foundations/design-color.es.md` |
| `design-system/design-typography.md` | `pointsav-design-system/docs/foundations/design-typography.md` |
| `design-system/design-typography.es.md` | `pointsav-design-system/docs/foundations/design-typography.es.md` |
| `design-system/design-spacing.md` | `pointsav-design-system/docs/foundations/design-spacing.md` |
| `design-system/design-spacing.es.md` | `pointsav-design-system/docs/foundations/design-spacing.es.md` |
| `design-system/design-motion.md` | `pointsav-design-system/docs/foundations/design-motion.md` |
| `design-system/design-motion.es.md` | `pointsav-design-system/docs/foundations/design-motion.es.md` |

**Pre-move checklist (destination session):**
- Create `pointsav-design-system/docs/foundations/` directory if absent.
- Commit each file at destination with staging-tier flow before any source-side `git rm`.
- ES pairs may be retained or dropped per project-design's bilingual policy for this repo (design-system repo is naturally EN-only; decision is project-design's).
- Update this entry to `destination-committed` after the destination commit lands.

**Post-move (source session):**
- `git rm` all 8 files from `content-wiki-documentation/design-system/`.
- Add `redirects.yaml` entries so `[[design-color]]`, `[[design-typography]]`, `[[design-spacing]]`, `[[design-motion]]` resolve without red links (or add stub articles with `aliases:` pointing at the design-system surface URL).
- Move this entry to Closed.

---

### 2026-05-16 — design-system/ Batch 2: component guides + wiki-surface docs → `pointsav-design-system/`

| Field | Value |
|---|---|
| State | `pending-destination-commit` |
| Opened | 2026-05-16 |
| Decision | OPUS editorial analysis (project-editorial session, 2026-05-16); operator-ratified |
| Rationale | Component usage guides (HTML+CSS+ARIA recipes) are design-system specifications, not platform documentation. They are addressed to component implementers, not the engineering or financial-community reader of `documentation.pointsav.com`. EN-only format violates the wiki's bilingual rule. Co-location with `pointsav-design-system/components/<name>/` resolves both the routing rule violation and the bilingual defect. Wiki-surface docs describe the nine wiki components; they belong with the component implementations, not in the wiki's own content. |

**Source files — component guides (16 EN-only files):**

| Source path | Destination path |
|---|---|
| `design-system/guide-component-badge.md` | `pointsav-design-system/components/badge/guide.md` |
| `design-system/guide-component-breadcrumb.md` | `pointsav-design-system/components/breadcrumb/guide.md` |
| `design-system/guide-component-button.md` | `pointsav-design-system/components/button/guide.md` |
| `design-system/guide-component-checkbox.md` | `pointsav-design-system/components/checkbox/guide.md` |
| `design-system/guide-component-citation-authority-ribbon.md` | `pointsav-design-system/components/citation-authority-ribbon/guide.md` |
| `design-system/guide-component-freshness-ribbon.md` | `pointsav-design-system/components/freshness-ribbon/guide.md` |
| `design-system/guide-component-home-grid.md` | `pointsav-design-system/components/home-grid/guide.md` |
| `design-system/guide-component-input-text.md` | `pointsav-design-system/components/input-text/guide.md` |
| `design-system/guide-component-link.md` | `pointsav-design-system/components/link/guide.md` |
| `design-system/guide-component-navigation-bar.md` | `pointsav-design-system/components/navigation-bar/guide.md` |
| `design-system/guide-component-notification.md` | `pointsav-design-system/components/notification/guide.md` |
| `design-system/guide-component-research-trail-footer.md` | `pointsav-design-system/components/research-trail-footer/guide.md` |
| `design-system/guide-component-select.md` | `pointsav-design-system/components/select/guide.md` |
| `design-system/guide-component-surface.md` | `pointsav-design-system/components/surface/guide.md` |
| `design-system/guide-component-switch.md` | `pointsav-design-system/components/switch/guide.md` |
| `design-system/guide-component-tab.md` | `pointsav-design-system/components/tab/guide.md` |

**Source files — wiki-surface docs (6 files — 3 EN+ES pairs):**

| Source path | Destination path |
|---|---|
| `design-system/wiki-component-library.md` | `pointsav-design-system/docs/wiki-surface/wiki-component-library.md` |
| `design-system/wiki-component-library.es.md` | `pointsav-design-system/docs/wiki-surface/wiki-component-library.es.md` |
| `design-system/wiki-dark-mode.md` | `pointsav-design-system/docs/wiki-surface/wiki-dark-mode.md` |
| `design-system/wiki-dark-mode.es.md` | `pointsav-design-system/docs/wiki-surface/wiki-dark-mode.es.md` |
| `design-system/wiki-typography-system.md` | `pointsav-design-system/docs/wiki-surface/wiki-typography-system.md` |
| `design-system/wiki-typography-system.es.md` | `pointsav-design-system/docs/wiki-surface/wiki-typography-system.es.md` |

**Pre-move checklist (destination session):**
- Create component subdirectories in `pointsav-design-system/components/` for components without an existing directory (badge, breadcrumb, button, checkbox, input-text, link, navigation-bar, notification, select, surface, switch, tab).
- Create `pointsav-design-system/docs/wiki-surface/` directory.
- Commit all files at destination before any source-side `git rm`.
- Note: `home-grid/`, `citation-authority-ribbon/`, `freshness-ribbon/`, `research-trail-footer/` already have component directories in `pointsav-design-system/components/`; check for existing `guide.md` before writing.
- Update this entry to `destination-committed` after the destination commit lands.

**Post-move (source session):**
- `git rm` all 22 files from `content-wiki-documentation/design-system/`.
- Add `redirects.yaml` entries (or stub aliases) for all 16 `guide-component-*` slugs.
- Rewrite `design-system/_index.md` to remove the component guide section (see cross-reference in Batch 3 checklist — both rewrites happen together after all batches land).
- Move this entry to Closed.

---

### 2026-05-16 — design-system/ Batch 3: spatial/accessibility specs → `pointsav-design-system/`

| Field | Value |
|---|---|
| State | `pending-destination-commit` |
| Opened | 2026-05-16 |
| Decision | OPUS editorial analysis (project-editorial session, 2026-05-16); operator-ratified |
| Rationale | Spatial UI components and accessibility specifications for GIS-surface panels are design-system specifications addressed to engineers building the GIS app, not to the platform-documentation reader. They belong in `pointsav-design-system/` alongside the token files and component implementations they reference. |

**Source files — spatial components (10 files — 5 EN+ES pairs):**

| Source path | Destination path |
|---|---|
| `design-system/country-filter-chips.md` | `pointsav-design-system/components/country-filter-chips/guide.md` |
| `design-system/country-filter-chips.es.md` | `pointsav-design-system/components/country-filter-chips/guide.es.md` |
| `design-system/map-side-drawer.md` | `pointsav-design-system/components/map-side-drawer/guide.md` |
| `design-system/map-side-drawer.es.md` | `pointsav-design-system/components/map-side-drawer/guide.es.md` |
| `design-system/map-stats-panel.md` | `pointsav-design-system/components/map-stats-panel/guide.md` |
| `design-system/map-stats-panel.es.md` | `pointsav-design-system/components/map-stats-panel/guide.es.md` |
| `design-system/climate-zone-tokens.md` | `pointsav-design-system/components/climate-zone-tokens/guide.md` |
| `design-system/climate-zone-tokens.es.md` | `pointsav-design-system/components/climate-zone-tokens/guide.es.md` |
| `design-system/zoom-tier-reveal-pattern.md` | `pointsav-design-system/components/zoom-tier-reveal-pattern/guide.md` |
| `design-system/zoom-tier-reveal-pattern.es.md` | `pointsav-design-system/components/zoom-tier-reveal-pattern/guide.es.md` |

**Source files — accessibility docs (8 files — 4 EN+ES pairs):**

| Source path | Destination path |
|---|---|
| `design-system/neurodiversity-typography-standards.md` | `pointsav-design-system/docs/accessibility/neurodiversity-typography-standards.md` |
| `design-system/neurodiversity-typography-standards.es.md` | `pointsav-design-system/docs/accessibility/neurodiversity-typography-standards.es.md` |
| `design-system/properties-panel-accessibility.md` | `pointsav-design-system/docs/accessibility/properties-panel-accessibility.md` |
| `design-system/properties-panel-accessibility.es.md` | `pointsav-design-system/docs/accessibility/properties-panel-accessibility.es.md` |
| `design-system/spatial-tree-accessibility.md` | `pointsav-design-system/docs/accessibility/spatial-tree-accessibility.md` |
| `design-system/spatial-tree-accessibility.es.md` | `pointsav-design-system/docs/accessibility/spatial-tree-accessibility.es.md` |
| `design-system/viewport-3d-accessibility.md` | `pointsav-design-system/docs/accessibility/viewport-3d-accessibility.md` |
| `design-system/viewport-3d-accessibility.es.md` | `pointsav-design-system/docs/accessibility/viewport-3d-accessibility.es.md` |

**Pre-move checklist (destination session):**
- Create `pointsav-design-system/components/country-filter-chips/`, `components/map-side-drawer/`, `components/map-stats-panel/`, `components/climate-zone-tokens/`, `components/zoom-tier-reveal-pattern/` directories.
- Create `pointsav-design-system/docs/accessibility/` directory.
- Commit all files at destination before any source-side `git rm`.
- Update this entry to `destination-committed` after the destination commit lands.

**Post-move (source session) — all three batches:**
When all three destination commits are confirmed, the source-side cleanup is:
1. `git rm` all 18 files in this batch from `content-wiki-documentation/design-system/`.
2. Rewrite `design-system/_index.md` (and `_index.es.md`) as a four-link MOC covering the 4 surviving pairs (design-philosophy, design-primitive-vocabulary, brand-family-swatch, brand-typography) plus a pointer to `design.pointsav.com` for the working surface.
3. Update `naming-convention.md §4` — narrow `design-system/` description from "components, tokens, foundations, and contribution guides" to "Design-system substrate as a platform component — architectural framing and brand surface context."
4. Add `naming-convention.md §13` amendment entry recording this split decision and its rationale.
5. Create `redirects.yaml` at repo root with entries for all moved slugs.
6. Move all three handoff entries to Closed.
- Move this entry to Closed.

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
