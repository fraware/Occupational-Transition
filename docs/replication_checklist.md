# Independent replication checklist

Use this checklist for a second person who did not implement the pipeline. **Do not sign off** until every required step passes.

## Environment

- [ ] Python 3.10+ installed.
- [ ] Fresh clone of the repository at a known commit hash: `________________`.
- [ ] Sufficient disk space and network access for downloads described in `docs/replication.md`.

## Data pipeline

- [ ] `pip install -r requirements.txt` succeeds.
- [ ] `python scripts/run_full_pipeline_from_raw.py` exits 0.
- [ ] Acceptance log exists: `intermediate/full_clean_rebuild_acceptance_*.md` with overall PASS.
- [ ] Optional: `python scripts/run_full_pipeline_from_raw.py --with-audit-summary` produces an audit summary table.

## Validation mode (select one)

- [ ] **Full replication mode (for freeze/sign-off):** complete `PR-000` through `T-020` plus full visuals coverage.
- [ ] **Bounded drift-validation mode (faster):** limited rerun with explicit scope note; not eligible for final freeze sign-off.
- [ ] If bounded mode used, closure note path recorded: `________________`.

## Main figures (CSV)

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

## Visuals (optional stage)

- [ ] `python scripts/run_visuals_all.py` exits 0.
- [ ] `python scripts/qa_visuals.py` exits 0.
- [ ] `python scripts/qa_visual_caption_coverage.py` exits 0.
- [ ] If `run_visuals_all.py` is expected to fail due to intentionally skipped appendix inputs, this is documented in closure notes and main-figure stems are still verified.

## Senator memo and Virginia pack (optional; policy/briefing deliverables)

Skip if replication scope is paper figures only. If senator memo or Virginia visuals are in scope:

- [ ] `python scripts/run_memo_visuals_build.py` exits 0.
- [ ] `python scripts/run_memo_visuals_qa.py` exits 0.
- [ ] Confirm core Virginia stems exist: `visuals/png/va01_virginia_sector_composition.png` through `va06_virginia_kpi_dashboard.png` (and matching PDFs under `visuals/vector/`).
- [ ] Confirm `figures/state_deep_dive_qcew_51_profile.csv` and `figures/virginia_memo_kpis.csv` exist when Virginia brief is claimed current.

## Spot-check mapping (sample)

Pick **one** ticket and trace source URL from `docs/data_registry.csv` to a cached file path named in `intermediate/*run_metadata.json` for that ticket. Record:

- Ticket: `____`
- Registry `dataset_id`: `____`
- Local cache path observed: `____`
- SHA-256 matches metadata: yes / no

## Robustness (optional)

- [ ] `python scripts/run_robustness_all.py` exits 0 (or reviewer notes acceptable failures in `intermediate/robustness/`).

## Sign-off

| Field | Value |
|-------|-------|
| Replicator name | |
| Date | |
| Commit hash | |
| Pass / Fail | |
| Notes | |
