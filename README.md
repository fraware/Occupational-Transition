# Occupational-Transition

Public-data paper pipeline: shared crosswalks, figures, and documentation.

## Public release

- **License:** [LICENSE](LICENSE) (MIT). Third-party PDFs and auxiliary tables are listed in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
- **Contributing and security:** [CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md).
- **What is committed vs generated:** [docs/committed_outputs.md](docs/committed_outputs.md) (frozen CSVs in git; large `raw/` downloads and `intermediate/` artifacts are local).
- **Replication:** Full runs can require **many gigabytes** of disk space and hours of download or compute; see [docs/replication.md](docs/replication.md).
- **Git history size:** If `.git` is unexpectedly large, see [docs/git_history_hygiene.md](docs/git_history_hygiene.md).

## Pipeline status

| Ticket | Scripts (build / QA) | Primary outputs |
|--------|----------------------|-----------------|
| PR-000 | `build_crosswalks.py` / `qa_crosswalks.py` | `crosswalks/occ22_crosswalk.csv`, `crosswalks/sector6_crosswalk.csv`, `docs/data_registry.csv` |
| T-001 | `build_figure1_panelA.py` / `qa_figure1_panelA.py` | `figures/figure1_panelA_occ_baseline.csv`, `intermediate/figure1_panelA_occ_baseline_meta.csv`, `intermediate/figure1_panelA_run_metadata.json` |
| T-002 | `build_figure1_panelB.py` / `qa_figure1_panelB.py` | `figures/figure1_panelB_task_heatmap.csv`, `intermediate/ai_relevance_terciles.csv`, `intermediate/figure1_panelB_meta.csv`, `intermediate/figure1_panelB_run_metadata.json` |
| T-003 | `build_figure2_panelA.py` / `qa_figure2_panelA.py` | `figures/figure2_panelA_hours_by_ai_tercile.csv`, `intermediate/figure2_panelA_run_metadata.json` |
| T-004 | `build_figure2_panelB_counts.py` / `qa_figure2_panelB_counts.py` | `figures/figure2_panelB_transition_counts.csv`, `intermediate/figure2_panelB_counts_run_metadata.json` |
| T-005 | `build_figure2_panelB_probs.py` / `qa_figure2_panelB_probs.py` | `figures/figure2_panelB_transition_probs.csv`, `intermediate/figure2_panelB_probs_run_metadata.json` |
| T-006 | `build_figure3_panelA_btos_ai_trends.py` / `qa_figure3_panelA_btos_ai_trends.py` | `figures/figure3_panelA_btos_ai_trends.csv`, `intermediate/figure3_panelA_btos_ai_trends_run_metadata.json` |
| T-007 | `build_figure3_panelB_btos_workforce_effects.py` / `qa_figure3_panelB_btos_workforce_effects.py` | `figures/figure3_panelB_btos_workforce_effects.csv`, `intermediate/figure3_panelB_btos_workforce_effects_run_metadata.json` |
| T-008 | `build_figure4_panelA_jolts_sector_rates.py` / `qa_figure4_panelA_jolts_sector_rates.py` | `figures/figure4_panelA_jolts_sector_rates.csv`, `intermediate/figure4_panelA_jolts_sector_rates_run_metadata.json` |
| T-009 | `build_figure4_panelB_ces_sector_index.py` / `qa_figure4_panelB_ces_sector_index.py` | `figures/figure4_panelB_ces_sector_index.csv`, `intermediate/figure4_panelB_ces_sector_index_run_metadata.json` |
| T-010 | `build_figure5_capability_matrix.py` / `qa_figure5_capability_matrix.py` | `figures/figure5_capability_matrix.csv`, `intermediate/figure5_capability_matrix_run_metadata.json` |
| T-011 | `build_figureA1_asec_welfare_by_ai_tercile.py` / `qa_figureA1_asec_welfare_by_ai_tercile.py` | `figures/figureA1_asec_welfare_by_ai_tercile.csv`, `intermediate/figureA1_asec_welfare_by_ai_tercile_run_metadata.json` |
| T-012 | `build_figureA2_sipp_event_study.py` / `qa_figureA2_sipp_event_study.py` | `figures/figureA2_sipp_event_study.csv`, `intermediate/figureA2_sipp_event_study_run_metadata.json` |
| T-013 | `build_figureA3_cps_supp_validation.py` / `qa_figureA3_cps_supp_validation.py` | `figures/figureA3_cps_supp_validation.csv`, `intermediate/figureA3_cps_supp_validation_run_metadata.json` |
| T-014 | `build_figureA4_abs_structural_adoption.py` / `qa_figureA4_abs_structural_adoption.py` | `figures/figureA4_abs_structural_adoption.csv`, `intermediate/figureA4_abs_structural_adoption_run_metadata.json` |
| T-015 | `build_figureA5_ces_payroll_hours.py` / `qa_figureA5_ces_payroll_hours.py` | `figures/figureA5_ces_payroll_hours.csv`, `intermediate/figureA5_ces_payroll_hours_run_metadata.json` |
| T-016 | `build_figureA6_bed_churn.py` / `qa_figureA6_bed_churn.py` | `figures/figureA6_bed_churn.csv`, `intermediate/figureA6_bed_churn_run_metadata.json` |
| T-017 | `build_figureA7_qcew_state_benchmark.py` / `qa_figureA7_qcew_state_benchmark.py` | `figures/figureA7_qcew_state_benchmark.csv`, `intermediate/figureA7_qcew_state_benchmark_run_metadata.json` |
| T-018 | `build_figureA8_lehd_benchmark.py` / `qa_figureA8_lehd_benchmark.py` | `figures/figureA8_lehd_benchmark.csv`, `intermediate/figureA8_lehd_benchmark_run_metadata.json` |
| T-019 | `build_figureA9_acs_local_composition.py` / `qa_figureA9_acs_local_composition.py` | `figures/figureA9_acs_local_composition.csv`, `intermediate/figureA9_acs_local_composition_run_metadata.json` |
| T-020 | `build_figureA10_nls_longrun.py` / `qa_figureA10_nls_longrun.py` | `figures/figureA10_nls_longrun.csv`, `intermediate/figureA10_nls_longrun_run_metadata.json` |

Extension tickets **T-021 through T-026** (AWES, ALPI, related intermediates) use scripts under `scripts/build_*` and `scripts/qa_*` as listed in [docs/methods_data.md](docs/methods_data.md). Senator memo visuals (`t101`–`t108`) and Virginia pack outputs (`va01`–`va08`) are enforced as post-ticket policy gates in strict acceptance.

## Full replication (clean)

From the repository root, with Python 3.10+ and network access for first-run downloads:

```bash
pip install -r requirements.txt
python scripts/run_full_pipeline_from_raw.py
```

This runs the strict ticket-by-ticket pipeline (`PR-000` through `T-020`), writes `intermediate/full_clean_rebuild_acceptance_<UTC>.md`, and exits non-zero on the first failed build or QA step.

Optional flags:

- `--with-audit-summary` — builds `intermediate/full_clean_rebuild_acceptance_<UTC>_audit_summary.md` from the new log
- `--with-visuals` — after a successful data pipeline, runs `run_visuals_all.py` and `qa_visuals.py`
- `--skip-install` — skips `pip install`
- `--source-selection-mode freeze_mode` — enforces drift comparability against an existing baseline snapshot
- `--require-signoff` — requires approved `intermediate/release_signoff.json` before final PASS

Prerequisites, directory layout, recovery from download failures, and acceptance review pointers: [docs/replication.md](docs/replication.md). Runtime can range from hours on a single machine when large files (for example NLSY97, ACS PUMS) are fetched and processed.

## Repo quality standard

- Every retained output must include machine-readable JSON lineage metadata under `intermediate/*run_metadata.json`.
- Every QA script validates strict schema/domain checks and local SHA-256 lineage against cached artifacts.
- Policy-facing KPI tables must include uncertainty/reliability fields (`se`, `ci_lower`, `ci_upper`, `weighted_n`, `effective_n`, `cv`) and deterministic publication fields (`publish_flag`, `suppression_reason`, `reliability_tier`).
- Policy-facing KPI tables must include `evidence_directness` with one of `direct_published`, `derived_transform`, `proxy_mapping`.
- Registry entries in `docs/data_registry.csv` use canonical HTTPS URLs and explicit values for release/last-modified fields (`Not reported by source` / `Not observed at build snapshot` when unavailable).
- Dynamic source selectors must record an explicit selection rule and selection mode in metadata.

## Methodology and registry

| Topic | Document |
|-------|----------|
| Crosswalks | [docs/pr000_crosswalk_methodology.md](docs/pr000_crosswalk_methodology.md) |
| T-001 | [docs/t001_figure1_panelA_methodology.md](docs/t001_figure1_panelA_methodology.md) |
| T-002 | [docs/t002_figure1_panelB_methodology.md](docs/t002_figure1_panelB_methodology.md) |
| T-003 | [docs/t003_figure2_panelA_methodology.md](docs/t003_figure2_panelA_methodology.md) |
| T-004 | [docs/t004_figure2_panelB_counts_methodology.md](docs/t004_figure2_panelB_counts_methodology.md) |
| T-005 | [docs/t005_figure2_panelB_probs_methodology.md](docs/t005_figure2_panelB_probs_methodology.md) |
| T-006 | [docs/t006_figure3_panelA_btos_ai_trends_methodology.md](docs/t006_figure3_panelA_btos_ai_trends_methodology.md) |
| T-007 | [docs/t007_figure3_panelB_btos_workforce_effects_methodology.md](docs/t007_figure3_panelB_btos_workforce_effects_methodology.md) |
| T-008 | [docs/t008_figure4_panelA_jolts_sector_rates_methodology.md](docs/t008_figure4_panelA_jolts_sector_rates_methodology.md) |
| T-009 | [docs/t009_figure4_panelB_ces_sector_index_methodology.md](docs/t009_figure4_panelB_ces_sector_index_methodology.md) |
| T-010 | [docs/t010_figure5_capability_matrix_methodology.md](docs/t010_figure5_capability_matrix_methodology.md) |
| T-011 | [docs/t011_figureA1_asec_welfare_by_ai_tercile_methodology.md](docs/t011_figureA1_asec_welfare_by_ai_tercile_methodology.md) |
| T-012 | [docs/t012_figureA2_sipp_event_study_methodology.md](docs/t012_figureA2_sipp_event_study_methodology.md) |
| T-013 | [docs/t013_figureA3_cps_supp_validation_methodology.md](docs/t013_figureA3_cps_supp_validation_methodology.md) |
| T-014 | [docs/t014_figureA4_abs_structural_adoption_methodology.md](docs/t014_figureA4_abs_structural_adoption_methodology.md) |
| T-015 | [docs/t015_figureA5_ces_payroll_hours_methodology.md](docs/t015_figureA5_ces_payroll_hours_methodology.md) |
| T-016 | [docs/t016_figureA6_bed_churn_methodology.md](docs/t016_figureA6_bed_churn_methodology.md) |
| T-017 | [docs/t017_figureA7_qcew_state_benchmark_methodology.md](docs/t017_figureA7_qcew_state_benchmark_methodology.md) |
| T-018 | [docs/t018_figureA8_lehd_benchmark_methodology.md](docs/t018_figureA8_lehd_benchmark_methodology.md) |
| T-019 | [docs/t019_figureA9_acs_local_composition_methodology.md](docs/t019_figureA9_acs_local_composition_methodology.md) |
| T-020 | [docs/t020_figureA10_nls_longrun_methodology.md](docs/t020_figureA10_nls_longrun_methodology.md) |
| Source URLs and snapshot dates | [docs/data_registry.csv](docs/data_registry.csv) |

## Quick runbook

### What to run most of the time

```bash
pip install -r requirements.txt
python scripts/run_full_pipeline_from_raw.py --with-audit-summary
```

This executes `PR-000` through `T-020` in strict order (build + QA), writes:

- `intermediate/full_clean_rebuild_acceptance_<UTC>.md`
- `intermediate/full_clean_rebuild_acceptance_<UTC>_audit_summary.md`

It also runs policy-facing hardening gates:

- memo/brief build and QA,
- robustness suite,
- drift dashboard build + QA,
- freeze manifest generation + QA.

### Targeted reruns

- Single ticket: run the ticket’s `build_*.py` then matching `qa_*.py` from the pipeline table above.
- Full acceptance only: `python scripts/run_full_clean_rebuild_acceptance.py`
- Summary from an existing log: `python scripts/build_acceptance_audit_summary.py --log <path>`

### Core shared outputs (PR-000)

- `crosswalks/occ22_crosswalk.csv`
- `crosswalks/sector6_crosswalk.csv`
- `docs/data_registry.csv`

### Notes for replicators

- First run requires network access and can take hours due to large official files.
- Use `docs/replication.md` for failure recovery (403s, large-download retries, cache/hash issues).
- Use the methodology table above for per-ticket assumptions and field definitions.

## Known Deviations From Issue Templates

- **T-006 window start:** The issue template states a locked start at `2023-08-28`. In current Census BTOS API responses, AI core rows for the national series first appear at `2023-09-11` (`PERIOD_ID 31`), so retained output begins there. See `docs/t006_figure3_panelA_btos_ai_trends_methodology.md`.
- **T-007 task-category source mapping:** The issue template specifies six frozen supplement workforce-effect categories as published shares. The current public `AI_Supplement_Table.xlsx` does not expose questionnaire item 25 option rows; implementation therefore uses documented Scope 2 proxy mappings for the three task-related keys while preserving exact published employment-effect rows. See `docs/t007_figure3_panelB_btos_workforce_effects_methodology.md`.

## Visualization pipeline

Render publication-ready visuals from existing `figures/*.csv` outputs:

```bash
python scripts/run_visuals_all.py
python scripts/qa_visuals.py
```

Outputs:
- `visuals/png/*.png`
- `visuals/vector/*.pdf`
- `intermediate/visuals_run_manifest.json`

Style standards: `docs/visual_style_guide.md`

Caption/source-note coverage check for main-text figures:

```bash
python scripts/qa_visual_caption_coverage.py
```

One-command visual acceptance (render + QA + log):

```bash
python scripts/run_visuals_acceptance.py
```

If you intentionally skip long appendix rebuild tickets, run `python scripts/qa_visuals.py` to validate the retained visual stems and treat `run_visuals_acceptance.py` as full-scope (all figures) coverage.

### Senator memo visuals and Virginia brief pack (additive)

Orchestrated build and QA (does not replace `run_visuals_all.py` for paper `t001`–`t020`):

```bash
python scripts/run_memo_visuals_build.py
python scripts/run_memo_visuals_qa.py
```

Outputs include `figures/memo_*.csv`, Virginia deep-dive CSVs under `figures/state_deep_dive_qcew_51_*.csv`, `figures/virginia_memo_kpis.csv`, and stems `t101`–`t108` plus `va01`–`va08` under `visuals/png/` and `visuals/vector/`. Precision rules: [docs/memo_visual_precision.md](docs/memo_visual_precision.md). Virginia module detail: [docs/virginia_deep_dive.md](docs/virginia_deep_dive.md).

## Post-implementation docs (quick index)

- Committed outputs inventory: [docs/committed_outputs.md](docs/committed_outputs.md)
- Replication: [docs/replication.md](docs/replication.md)
- Acceptance matrix: [docs/acceptance_matrix.md](docs/acceptance_matrix.md)
- Figure catalog, captions, source notes: [docs/figure_catalog.md](docs/figure_catalog.md), `docs/captions/`, `docs/source_notes/`
- Figure memos (main text): `docs/figure_memos/fig01.md`–`fig05.md`
- Claim audit: [docs/claim_audit.md](docs/claim_audit.md)
- Senator briefing (Virginia): [docs/senate_briefing_memo.md](docs/senate_briefing_memo.md), [docs/senate_briefing_evidence_baseline_va.md](docs/senate_briefing_evidence_baseline_va.md), [docs/senate_briefing_lineage_va.md](docs/senate_briefing_lineage_va.md), [docs/senate_briefing_script_va.md](docs/senate_briefing_script_va.md), [docs/senate_briefing_qa_va.md](docs/senate_briefing_qa_va.md), [docs/senator_handout_1page_va.md](docs/senator_handout_1page_va.md), [docs/senator_packet_order_va.md](docs/senator_packet_order_va.md), [docs/virginia_deep_dive.md](docs/virginia_deep_dive.md)
- Methods/data: [docs/methods_data.md](docs/methods_data.md)
- Main draft (skeleton): [docs/paper_draft_v1_public_data_ai_labor.md](docs/paper_draft_v1_public_data_ai_labor.md)
- Final paper draft (expanded): [docs/paper_final.md](docs/paper_final.md); evidence snapshot: [docs/evidence_snapshot.md](docs/evidence_snapshot.md)
- Appendix: [docs/appendix_outline.md](docs/appendix_outline.md), [docs/appendix_draft.md](docs/appendix_draft.md)
- Release/freeze: [docs/release_process.md](docs/release_process.md), `python scripts/build_freeze_manifest.py`
- Reliability framework: [docs/reliability_framework.md](docs/reliability_framework.md)
- Independent replication: [docs/replication_checklist.md](docs/replication_checklist.md)

## Robustness and freeze helpers

Robustness checks for Figures 1-5 (writes reports to `intermediate/robustness/`):

```bash
python scripts/run_robustness_all.py
```

Build a results-freeze hash manifest (figures + run metadata + visuals manifest when present):

```bash
python scripts/build_freeze_manifest.py
```
