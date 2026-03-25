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
| `metrics/` | Optional occupation-time monitoring metrics (AWES, ALPI; T-023 and T-026) |
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

T-021 requires BLS OEWS industry-by-occupation inputs: either `raw/oesm24in4.zip` (see `docs/data_registry.csv`) or pre-extracted `*.xlsx` workbooks under `raw/oesm24in4_extract/`, in addition to the national file used in T-001/T-002.

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
| `--source-selection-mode freeze_mode` | Require baseline comparability in drift checks (fails if no baseline snapshot exists) |
| `--require-signoff` | Require approved `intermediate/release_signoff.json` via `qa_release_signoff.py` |

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

Policy-facing reliability gates:

- `python scripts/run_memo_visuals_build.py`
- `python scripts/run_memo_visuals_qa.py`
- `python scripts/run_robustness_all.py`
- `python scripts/build_drift_dashboard.py`
- `python scripts/qa_drift_dashboard.py`
- `python scripts/build_freeze_manifest.py`
- `python scripts/qa_freeze_manifest.py`
- `python scripts/qa_release_signoff.py` (when `--require-signoff` is used)

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

## Senator memo visuals and Virginia brief pack (optional, additive)

These steps are **not** part of the default `run_full_clean_rebuild_acceptance.py` ticket list. They produce memo stems `t101`–`t108`, Virginia stems `va01`–`va08`, related `figures/memo_*.csv`, `figures/state_deep_dive_qcew_51_*.csv`, and `figures/virginia_memo_kpis.csv`.

**Prerequisites:** Figure inputs for the memo pipeline must exist (for example `figures/figure3_panelA_btos_ai_trends.csv`, Figure 1–2 outputs, Figure 4–5, and crosswalk/intermediate artifacts as listed in `scripts/run_memo_visuals_build.py`). Virginia QCEW tables require **T-017** first: `figures/figureA7_qcew_state_benchmark.csv` from `scripts/build_figureA7_qcew_state_benchmark.py`.

**One-command build and QA:**

```bash
python scripts/run_memo_visuals_build.py
python scripts/run_memo_visuals_qa.py
```

**Targeted Virginia-only rebuild** (after T-017 is current):

```bash
python scripts/build_state_qcew_deep_dive.py --state-fips 51
python scripts/qa_state_qcew_deep_dive.py --state-fips 51
python scripts/build_virginia_memo_kpis.py
python scripts/visualize_virginia_memo.py
python scripts/qa_virginia_memo_visuals.py
```

**Documentation:** precision rules for memo KPIs and BTOS state map — `docs/memo_visual_precision.md`. Figure and stem catalog — `docs/figure_catalog.md`. Virginia methodology summary — `docs/virginia_deep_dive.md`. Senator-facing narrative and provenance — `docs/senate_briefing_memo.md`, `docs/senate_briefing_evidence_baseline_va.md`, `docs/senate_briefing_lineage_va.md`.
