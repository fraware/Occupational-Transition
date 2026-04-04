# Replication

**Audience:** Anyone reproducing pipeline outputs from a clean clone through final figure CSVs under `figures/`, and optionally publication visuals under `visuals/`.

**Related:** [acceptance_matrix.md](acceptance_matrix.md), [project_maintenance.md](project_maintenance.md), [local scheduling / catalog refresh](../operations/local_scheduling.md), [library README](../library/README.md), [quality README](../quality/README.md).

## Contents

- [Replication from a clean clone](#replication-from-a-clean-clone)
- [Committed outputs vs build-generated](#committed-outputs-vs-build-generated)
- [Independent replication checklist](#independent-replication-checklist)
- [Local catalog refresh scheduling](../operations/local_scheduling.md) (optional `ot refresh` / Task Scheduler)

---

## Replication from a clean clone

This section describes how to reproduce pipeline outputs from a clean clone of the repository through final figure CSVs under `figures/`, and optionally publication visuals under `visuals/`.

### Prerequisites

- Python 3.10 or newer (3.11+ recommended).
- Network access for first-run downloads from Census, BLS, and other agencies listed in `docs/data_registry.csv`.
- Sufficient disk space for `raw/` caches and large public-use files (multi-gigabyte downloads are possible for NLSY97 and ACS PUMS; see methodology step notes).

### Directory layout

| Path | Role |
|------|------|
| `raw/` | Cached official downloads produced by build scripts when files are not already present |
| `figures/` | Final tidy CSV outputs for main-text and appendix figures |
| `metrics/` | Optional occupation-time monitoring metrics (AWES, ALPI; T-023 and T-026) |
| `intermediate/` | JSON run metadata, QA logs, manifests, and derived intermediates (for example `ai_relevance_terciles.csv`) |
| `crosswalks/` | Frozen occupation and sector crosswalks (`PR-000`) |
| `visuals/png/`, `visuals/vector/` | Static charts (optional stage) |
| `scripts/` | Build, QA, visualization, and orchestration scripts |

### One-command full build (PR-000 through T-026)

From the repository root, after creating a virtual environment if desired:

```bash
python -m pip install -r requirements.txt
python -m pip install -e .
python scripts/run_full_pipeline_from_raw.py
```

Profile/CLI alternative:

```bash
ot run --profile config/profiles/full-replication.toml
```

T-021 requires BLS OEWS industry-by-occupation inputs: either `raw/oesm24in4.zip` (see `docs/data_registry.csv`) or pre-extracted `*.xlsx` workbooks under `raw/oesm24in4_extract/`, in addition to the national file used in T-001/T-002.

This runs `scripts/run_full_clean_rebuild_acceptance.py`, which:

- Deletes expected outputs for each build step before rebuilding
- Runs each build script then its QA script in order
- Writes a timestamped log to `intermediate/full_clean_rebuild_acceptance_<UTC>.md`

#### Optional flags

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

### What must exist vs what is downloaded

- **Crosswalk inputs:** `scripts/build_crosswalks.py` expects certain reference files under `raw/` as documented in `docs/methodology/pr000_crosswalk_methodology.md`. If they are absent, the script may fetch or guide you to place them.
- **Per-figure sources:** Each `scripts/build_figure*.py` documents URLs and cache paths. First execution typically downloads into `raw/` and records hashes in `intermediate/*run_metadata.json`.
- **Registry:** `docs/data_registry.csv` is generated or updated by `build_crosswalks.py` and some figure builds; QA enforces HTTPS links and required fields.

### Failure modes and recovery

| Symptom | Likely cause | What to do |
|---------|----------------|------------|
| HTTP 403 / blocked download | Remote server requires browser-like headers or blocks scripted access | Retry later; check methodology doc for Referer/User-Agent; verify URL still valid |
| `MemoryError` on very large files | Whole-file read of multi-GB CSV | Use a machine with more RAM or ensure streaming build path (NLSY97, ACS) |
| QA hash mismatch | Cached `raw/` file changed or corrupted | Delete the specific cached file and rerun so it re-downloads |
| Missing month in CPS window | Public file not yet published for a calendar month | Documented allowlists may skip known gaps; see build script notes |

### Acceptance and audit

After a successful run, review:

- `intermediate/full_clean_rebuild_acceptance_*.md` (full log)
- `intermediate/full_clean_rebuild_acceptance_*_audit_summary.md` (if generated)
- `docs/replication/acceptance_matrix.md` (step-level criteria vs automated QA)

Reliability gates:

- `python scripts/run_robustness_all.py`
- `python scripts/build_drift_dashboard.py`
- `python scripts/qa_drift_dashboard.py`
- `python scripts/build_freeze_manifest.py`
- `python scripts/qa_freeze_manifest.py`
- `python scripts/qa_release_signoff.py` (when `--require-signoff` is used)

#### Bounded rerun option (faster validation)

If you need a quicker drift-validation pass (for example while avoiding long appendix rebuild steps), you can:

1. Run targeted rebuild scripts for the affected steps.
2. Generate an audit summary from the selected acceptance log:
   - `python scripts/build_acceptance_audit_summary.py --log <path_to_log>`
3. Run main visual QA:
   - `python scripts/qa_visuals.py`

In that mode, explicitly record scope limits in a closure note (for example, which late
steps were not rerun) so reviewers do not misread it as a full `PR-000` through
`T-026` replication.

### Visual style lock

Publication figures use `scripts/viz_style.py` and [quality README — Visual style guide](../quality/README.md#visual-style-guide). Do not change colors or fonts ad hoc without updating the quality doc and regenerating all visuals.

## Committed outputs vs build-generated

This inventory aligns [README.md](../../README.md) and [acceptance_matrix.md](acceptance_matrix.md) with what is **tracked in git** versus produced locally by the pipeline.

### Tracked in git

- **Crosswalks and registry:** `crosswalks/*.csv`, `docs/data_registry.csv`
- **Figures (CSV):** All paths under `figures/*.csv` listed by `git ls-files figures`. This includes main-text and appendix tables checked in as frozen outputs.
- **Metrics:** `metrics/awes_occ22_monthly.csv`, `metrics/alpi_occ22_monthly.csv`
- **Visuals:** `visuals/png/*.png`, `visuals/vector/*.pdf`

### Build-generated (not committed; typical paths)

These are required for a full strict rebuild but are not versioned in the repository:

| Output | Typical path | When it appears |
|--------|----------------|-----------------|
| T-004 transition counts | `figures/figure2_panelB_transition_counts.csv` | After `build_figure2_panelB_counts.py` (feeds T-005 downstream rates) |
| AI relevance terciles | `intermediate/ai_relevance_terciles.csv` | After T-002 build |
| Run metadata | `intermediate/*run_metadata.json` | Per-step build scripts |
| Acceptance logs | `intermediate/full_clean_rebuild_acceptance_*.md` | After `run_full_clean_rebuild_acceptance.py` or full pipeline |
| Visual manifest | `intermediate/visuals_run_manifest.json` | After `run_visuals_all.py` |

Replicators should run the commands in [Replication from a clean clone](#replication-from-a-clean-clone) to generate these artifacts; the committed `figures/` set is the **published snapshot** for the paper and policy tables that are checked in.

### Note on T-004

`figures/figure2_panelB_transition_counts.csv` is listed in the acceptance matrix and README build-step table but is **not** a committed file in the default snapshot: it is produced by the CPS pipeline and consumed on disk by `build_figure2_panelB_probs.py`. Obtain it by running T-004 build (see [t004_figure2_panelB_counts_methodology.md](../methodology/tickets/t004_figure2_panelB_counts_methodology.md)).

---

## Independent replication checklist

Use this checklist for a second person who did not implement the pipeline. **Do not sign off** until every required step passes.

### Environment

- [ ] Python 3.10+ installed.
- [ ] Fresh clone of the repository at a known commit hash: `________________`.
- [ ] Sufficient disk space and network access for downloads described in [Replication from a clean clone](#replication-from-a-clean-clone).

### Data pipeline

- [ ] `pip install -r requirements.txt` succeeds.
- [ ] `python scripts/run_full_pipeline_from_raw.py` exits 0.
- [ ] Acceptance log exists: `intermediate/full_clean_rebuild_acceptance_*.md` with overall PASS.
- [ ] Optional: `python scripts/run_full_pipeline_from_raw.py --with-audit-summary` produces an audit summary table.

### Validation mode (select one)

- [ ] **Full replication mode (for freeze/sign-off):** complete `PR-000` through `T-020` plus full visuals coverage.
- [ ] **Bounded drift-validation mode (faster):** limited rerun with explicit scope note; not eligible for final freeze sign-off.
- [ ] If bounded mode used, closure note path recorded: `________________`.

### Main figures (CSV)

Confirm files exist and are non-empty:

- [ ] `figures/figure1_panelA_occ_baseline.csv`
- [ ] `figures/figure1_panelB_task_heatmap.csv`
- [ ] `intermediate/ai_relevance_terciles.csv`
- [ ] `figures/figure2_panelA_hours_by_ai_tercile.csv`
- [ ] `figures/figure2_panelB_transition_probs.csv`
- [ ] `figures/figure3_panelA_btos_ai_trends.csv`
- [ ] `figures/figure3_panelB_btos_workforce_effects.csv`
- [ ] `figures/figure4_panelA_jolts_sector_rates.csv`
- [ ] `figures/figure4_panelB_ces_sector_index.csv`
- [ ] `figures/figure5_capability_matrix.csv`
- [ ] `figures/figure6_policy_roadmap.csv`

### Visuals (optional stage)

- [ ] `python scripts/run_visuals_all.py` exits 0.
- [ ] `python scripts/qa_visuals.py` exits 0.
- [ ] `python scripts/qa_visual_caption_coverage.py` exits 0.
- [ ] If `run_visuals_all.py` is expected to fail due to intentionally skipped appendix inputs, this is documented in closure notes and main-figure stems are still verified.

### Drift and freeze (policy release mode)

- [ ] `python scripts/build_drift_dashboard.py` exits 0.
- [ ] `python scripts/qa_drift_dashboard.py` exits 0.
- [ ] `intermediate/drift/drift_dashboard.csv` contains no `critical` alerts.
- [ ] `python scripts/build_freeze_manifest.py` exits 0.
- [ ] `python scripts/qa_freeze_manifest.py` exits 0.
- [ ] `python scripts/qa_release_signoff.py` exits 0 (approved sign-off file present).

### Spot-check mapping (sample)

Pick **one** build step and trace source URL from `docs/data_registry.csv` to a cached file path named in `intermediate/*run_metadata.json` for that build step. Record:

- Build step: `____`
- Registry `dataset_id`: `____`
- Local cache path observed: `____`
- SHA-256 matches metadata: yes / no

### Robustness (required in release mode)

- [ ] `python scripts/run_robustness_all.py` exits 0 (or reviewer notes acceptable failures in `intermediate/robustness/`).

### Sign-off

| Field | Value |
|-------|-------|
| Replicator name | |
| Date | |
| Commit hash | |
| Pass / Fail | |
| Notes | |
