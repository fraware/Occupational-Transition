# Replication guide

This document describes how to reproduce pipeline outputs from a clean clone of the repository through final figure CSVs under `figures/`, and optionally publication visuals under `visuals/`.

## Prerequisites

- Python 3.10 or newer (3.11+ recommended).
- Network access for first-run downloads from Census, BLS, and other agencies listed in `docs/data_registry.csv`.
- Sufficient disk space for `raw/` caches and large public-use files (multi-gigabyte downloads are possible for NLSY97 and ACS PUMS; see ticket methodology docs).

## Directory layout

| Path | Role |
|------|------|
| `raw/` | Cached official downloads produced by build scripts when files are not already present |
| `figures/` | Final tidy CSV outputs for main-text and appendix figures |
| `intermediate/` | JSON run metadata, QA logs, manifests, and derived intermediates (for example `ai_relevance_terciles.csv`) |
| `crosswalks/` | Frozen occupation and sector crosswalks (`PR-000`) |
| `visuals/png/`, `visuals/vector/` | Static charts (optional stage) |
| `scripts/` | Build, QA, visualization, and orchestration scripts |

## One-command full build (PR-000 through T-020)

From the repository root, after creating a virtual environment if desired:

```bash
python -m pip install -r requirements.txt
python scripts/run_full_pipeline_from_raw.py
```

This runs `scripts/run_full_clean_rebuild_acceptance.py`, which:

- Deletes expected outputs for each ticket before rebuilding
- Runs each build script then its QA script in order
- Writes a timestamped log to `intermediate/full_clean_rebuild_acceptance_<UTC>.md`

### Optional flags

| Flag | Effect |
|------|--------|
| `--skip-install` | Skip `pip install -r requirements.txt` |
| `--with-visuals` | After a successful data pipeline, run `run_visuals_all.py` and `qa_visuals.py` |
| `--with-audit-summary` | After acceptance, build a short table via `build_acceptance_audit_summary.py` |

Example:

```bash
python scripts/run_full_pipeline_from_raw.py --with-audit-summary --with-visuals
```

On Windows PowerShell, use `;` instead of `&&` between commands if you run steps manually.

## What must exist vs what is downloaded

- **Crosswalk inputs:** `scripts/build_crosswalks.py` expects certain reference files under `raw/` as documented in `docs/pr000_crosswalk_methodology.md`. If they are absent, the script may fetch or guide you to place them.
- **Per-figure sources:** Each `scripts/build_figure*.py` documents URLs and cache paths. First execution typically downloads into `raw/` and records hashes in `intermediate/*run_metadata.json`.
- **Registry:** `docs/data_registry.csv` is generated or updated by `build_crosswalks.py` and some figure builds; QA enforces HTTPS links and required fields.

## Failure modes and recovery

| Symptom | Likely cause | What to do |
|---------|----------------|------------|
| HTTP 403 / blocked download | Remote server requires browser-like headers or blocks scripted access | Retry later; check methodology doc for Referer/User-Agent; verify URL still valid |
| `MemoryError` on very large files | Whole-file read of multi-GB CSV | Use a machine with more RAM or ensure streaming build path (NLSY97, ACS) |
| QA hash mismatch | Cached `raw/` file changed or corrupted | Delete the specific cached file and rerun so it re-downloads |
| Missing month in CPS window | Public file not yet published for a calendar month | Documented allowlists may skip known gaps; see build script notes |

## Acceptance and audit

After a successful run, review:

- `intermediate/full_clean_rebuild_acceptance_*.md` (full log)
- `intermediate/full_clean_rebuild_acceptance_*_audit_summary.md` (if generated)
- `docs/acceptance_matrix.md` (ticket-level criteria vs automated QA)

### Bounded rerun option (faster validation)

If you need a quicker drift-validation pass (for example while avoiding long appendix rebuild tickets), you can:

1. Run targeted rebuild scripts for the affected tickets.
2. Generate an audit summary from the selected acceptance log:
   - `python scripts/build_acceptance_audit_summary.py --log <path_to_log>`
3. Run main visual QA:
   - `python scripts/qa_visuals.py`

In that mode, explicitly record scope limits in a closure note (for example, which late tickets were not rerun) so reviewers do not misread it as a full `PR-000` through `T-020` replication.

## Visual style lock

Publication figures use `scripts/viz_style.py` and `docs/visual_style_guide.md`. Do not change colors or fonts ad hoc without updating the style guide and regenerating all visuals.
