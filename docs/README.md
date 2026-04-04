# Documentation hub

**Occupational Transition** — **public data, AI, and US labor markets** (broad, search-friendly); **US labor market measurement from public data** (measurement-first, not hype); **reproducible US labor and AI indicators** (step-based builds and run history); **open data pipeline for AI and labor economics** (library, single build steps, or full replication—see sections below).

**Start here if…**

- You want to **import the Python package** or run small examples → [Library](#library-user--integrator) (read [library README](library/README.md) first).
- You need to **reproduce figures from raw** or validate CI acceptance → [Replication](#replicator).
- You are **writing or reviewing the paper** → [Paper](#paper-author).
- You work on **policy claims and scope wording** → [Policy](#policy).
- You want a **state-level case study** (optional; national pipeline first) → [State case studies](#state-case-studies).

This repository is both an installable package (`occupational_transition`) for US public-data extraction and a step-by-step figure pipeline for the empirical paper. The four phrases above are the default positioning for docs and discovery. The sections below give **numbered reading orders** by role; the **master table** lists every major document with a one-line purpose.

## Start quickly

1. [start_here.md](start_here.md) — fastest path from install to first run.
2. [analysis_catalog.md](analysis_catalog.md) — choose analyses by intent.
3. [source_selection.md](source_selection.md) — pick `latest_mode` vs `freeze_mode`.

---

## Library user / integrator

1. [library/README.md](library/README.md) — package map, reuse modes, CLI, Sphinx API build, positioning vs agencies.
2. [examples/README.md](../examples/README.md) and scripts under [`examples/`](../examples/).
3. [methodology/pr000_crosswalk_methodology.md](methodology/pr000_crosswalk_methodology.md) if you touch occupation or sector mappings.
4. [data_registry.csv](data_registry.csv) for canonical source URLs.

---

## Replicator

1. [replication/README.md](replication/README.md) — one-command build, flags, committed vs generated outputs, independent checklist.
2. [replication/acceptance_matrix.md](replication/acceptance_matrix.md) — build-step checks and QA mapping.
3. [methodology/README.md](methodology/README.md) — index to per-step methodology notes.
4. [replication/project_maintenance.md](replication/project_maintenance.md) — git object hygiene, results tags, Zenodo alignment.
5. [quality/README.md](quality/README.md) — visual style lock and reliability rules before signing off visuals.

---

## Paper author

1. [paper/methods_data.md](paper/methods_data.md) — methods and data narrative aligned with the build.
2. [paper/paper.md](paper/paper.md) — full manuscript text.
3. [paper/appendix_draft.md](paper/appendix_draft.md) — appendix prose and outline (top of file).
4. [paper/evidence_snapshot.md](paper/evidence_snapshot.md) — locking numbers to a run.
5. [figures/figure_catalog.md](figures/figure_catalog.md) and [figures/README.md](figures/README.md) for stems, captions, and source notes.

---

## Policy

1. [policy/claim_audit.md](policy/claim_audit.md) — cross-cutting claim ledger (paper claims and referenced evidence, including SB-VA rows for the Virginia package).
2. [quality/README.md](quality/README.md) — reliability standards and visual QA rules.

Legislative narrative under `docs/policy/briefing/` may be **local-only** in some clones; see repository `.gitignore`.

---

## State case studies

1. [states/README.md](states/README.md) — federal-first scope and index of state modules.
2. [states/virginia/README.md](states/virginia/README.md) — Virginia (FIPS 51) reading order and rebuild notes.

---

## Master table (major documents)

| Document | Purpose | When to read |
|----------|---------|----------------|
| [library/README.md](library/README.md) | Single entry for package use, reuse, related work, API HTML build | Integrating or extending the library |
| [replication/README.md](replication/README.md) | Full rebuild, outputs inventory, replication checklist | Reproducing results |
| [replication/acceptance_matrix.md](replication/acceptance_matrix.md) | Full technical mapping of build steps, outputs, QA checks, and results | After acceptance runs; gate checks |
| [replication/project_maintenance.md](replication/project_maintenance.md) | History hygiene, tags, freeze manifest | Before public push; release milestones |
| [methodology/pr000_crosswalk_methodology.md](methodology/pr000_crosswalk_methodology.md) | Crosswalk rules and assumptions | Any change to `crosswalks/` |
| [methodology/README.md](methodology/README.md) | Build-step index and how to read a methodology note | Tracing a figure to assumptions |
| [methodology/tickets/](methodology/tickets/) | Per-step methodology and QA anchors | Deep dive per figure |
| [figures/figure_catalog.md](figures/figure_catalog.md) | Stems, caption paths, source notes | Figures and visuals |
| [figures/README.md](figures/README.md) | How catalog, captions, and source notes relate | First time using `figures/` docs |
| [paper/methods_data.md](paper/methods_data.md) | Manuscript-facing methods | Writing results |
| [paper/paper.md](paper/paper.md) | Final manuscript text | Publication track |
| [paper/appendix_draft.md](paper/appendix_draft.md) | Appendix prose + outline | Appendix editing |
| [paper/evidence_snapshot.md](paper/evidence_snapshot.md) | Frozen-number snapshot | Locking prose to a build |
| [paper/README.md](paper/README.md) | Paper folder reading order | Orientation |
| [quality/README.md](quality/README.md) | Reliability framework and visual style | QA and publication visuals |
| [policy/claim_audit.md](policy/claim_audit.md) | Claim support ledger | Any external claim |
| [states/README.md](states/README.md) | Optional state case studies (national pipeline first) | State-level briefings or extensions |
| [states/virginia/README.md](states/virginia/README.md) | Virginia (FIPS 51) case study index | VA deep dive and optional memo visuals |
| [data_registry.csv](data_registry.csv) | Dataset IDs and HTTPS URLs | Downloads and citations |
| [archive/README.md](archive/README.md) | Role of full issue / paper-note archives | Traceability, not onboarding |
| [references/README.md](references/README.md) | PDF reference packs | CPS/BLS documentation |
| [lineage/](lineage/) | Canonical traceability matrices | Paper line edits vs build |

---

## Folder map (quick)

| Folder | Role |
|--------|------|
| [library/](library/) | Package-oriented documentation ([README](library/README.md)); thin stubs retain old filenames for bookmarks |
| [replication/](replication/) | Rebuild guide, acceptance matrix, maintenance |
| [methodology/](methodology/) | Crosswalk methodology + per-step methodology (`tickets/`) |
| [figures/](figures/) | Catalog, [README](figures/README.md), captions, source notes |
| [paper/](paper/) | Manuscript, methods, appendix, evidence snapshot |
| [policy/](policy/) | Claim audit |
| [states/](states/) | Optional state case studies ([README](states/README.md)) |
| [quality/](quality/) | Reliability and visual style ([README](quality/README.md)) |
| [archive/](archive/) | Long-form archives (`issues_full`, `paper_notes_full`) |
| [references/](references/) | PDFs and index |
| [lineage/](lineage/) | Canonical matrices for audits |
| [sphinx/](sphinx/) | Sphinx source (build output under `sphinx/_build/`, not tracked) |

---

## Maintenance

- **Canonical repository:** [github.com/fraware/Occupational-Transition](https://github.com/fraware/Occupational-Transition).
- **Historical path rewrites:** [meta/path_migration_map.json](meta/path_migration_map.json) (for automation and external bookmarks; consumed by `scripts/rewrite_docs_paths.py` where applicable).
- **Stale path guard:** `python scripts/check_stale_doc_paths.py` (CI).
- **Technical code mappings:** full PR/T step labels are documented only in [methodology/README.md](methodology/README.md) and [replication/acceptance_matrix.md](replication/acceptance_matrix.md).

---

## Thin stubs (legacy paths)

Some former top-level doc paths remain as short redirects: `library/overview.md`, `replication/replication.md`, `quality/reliability_framework.md`, etc. Prefer links to the `README.md` targets above.
