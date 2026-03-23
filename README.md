# Occupational-Transition

Public-data paper pipeline: shared crosswalks, figures, and documentation.

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

Later tickets (T-021 onward) are defined in `issues.md` but do not yet have build scripts in this repository unless added in a future change.

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

Prerequisites, directory layout, recovery from download failures, and acceptance review pointers: [docs/replication.md](docs/replication.md). Runtime can range from hours on a single machine when large files (for example NLSY97, ACS PUMS) are fetched and processed.

## Repo quality standard

- Every retained output must include machine-readable JSON lineage metadata under `intermediate/*run_metadata.json`.
- Every QA script validates strict schema/domain checks and local SHA-256 lineage against cached artifacts.
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

## PR-000 shared outputs

- `crosswalks/occ22_crosswalk.csv` — 22-group occupation taxonomy (CPS / SOC 2018).
- `crosswalks/sector6_crosswalk.csv` — six-sector demand taxonomy (BTOS, JOLTS, CES, BED, QCEW-aligned NAICS).
- `docs/data_registry.csv` — source URLs and snapshot metadata.

## Rebuild crosswalks

Place official inputs under `raw/` (see `docs/data_registry.csv`), then:

```bash
pip install -r requirements.txt
python scripts/build_crosswalks.py
python scripts/qa_crosswalks.py
```

Methodology: [docs/pr000_crosswalk_methodology.md](docs/pr000_crosswalk_methodology.md).

## T-001 Figure 1 Panel A (OEWS national baseline)

```bash
python scripts/build_figure1_panelA.py
python scripts/qa_figure1_panelA.py
```

Output: `figures/figure1_panelA_occ_baseline.csv` plus `intermediate/figure1_panelA_occ_baseline_meta.csv` and `intermediate/figure1_panelA_run_metadata.json`. Methodology: [docs/t001_figure1_panelA_methodology.md](docs/t001_figure1_panelA_methodology.md).

## T-002 Figure 1 Panel B (O*NET task heatmap and AI terciles)

```bash
python scripts/build_figure1_panelB.py
python scripts/qa_figure1_panelB.py
```

Outputs: `figures/figure1_panelB_task_heatmap.csv`, `intermediate/ai_relevance_terciles.csv`, `intermediate/figure1_panelB_meta.csv`, and `intermediate/figure1_panelB_run_metadata.json`. Methodology: [docs/t002_figure1_panelB_methodology.md](docs/t002_figure1_panelB_methodology.md).

## T-003 Figure 2 Panel A (CPS usual weekly hours by AI tercile)

```bash
python scripts/build_figure2_panelA.py
python scripts/qa_figure2_panelA.py
```

Output: `figures/figure2_panelA_hours_by_ai_tercile.csv` (columns: `month`, `ai_relevance_tercile`, `mean_usual_weekly_hours`, `sum_composite_weight`) plus `intermediate/figure2_panelA_run_metadata.json`. Methodology: [docs/t003_figure2_panelA_methodology.md](docs/t003_figure2_panelA_methodology.md).

## T-004 Figure 2 Panel B (CPS matched-person transition counts)

```bash
python scripts/build_figure2_panelB_counts.py
python scripts/qa_figure2_panelB_counts.py
```

Output: `figures/figure2_panelB_transition_counts.csv` (columns: `month`, `origin_state`, `destination_state`, `weighted_transition_count`) plus `intermediate/figure2_panelB_counts_run_metadata.json`. Methodology: [docs/t004_figure2_panelB_counts_methodology.md](docs/t004_figure2_panelB_counts_methodology.md).

## T-005 Figure 2 Panel B (transition probabilities from T-004 counts)

Requires T-004 outputs. Then:

```bash
python scripts/build_figure2_panelB_probs.py
python scripts/qa_figure2_panelB_probs.py
```

Output: `figures/figure2_panelB_transition_probs.csv` (matrix and summary rows keyed by `record_type`) plus `intermediate/figure2_panelB_probs_run_metadata.json`. Methodology: [docs/t005_figure2_panelB_probs_methodology.md](docs/t005_figure2_panelB_probs_methodology.md).

## T-006 Figure 3 Panel A (BTOS AI-use trends)

Requires network access to Census `https://www.census.gov/hfp/btos/api/`.

```bash
python scripts/build_figure3_panelA_btos_ai_trends.py
python scripts/qa_figure3_panelA_btos_ai_trends.py
```

Output: `figures/figure3_panelA_btos_ai_trends.csv` (columns: `period_start_date`, `btos_period_id`, `ai_use_current_rate`, `ai_use_expected_6m_rate`, `source_series_id`) plus `intermediate/figure3_panelA_btos_ai_trends_run_metadata.json`. Methodology: [docs/t006_figure3_panelA_btos_ai_trends_methodology.md](docs/t006_figure3_panelA_btos_ai_trends_methodology.md).

## T-007 Figure 3 Panel B (BTOS AI supplement workforce effects)

Requires network access to Census `https://www.census.gov/hfp/btos/downloads/AI_Supplement_Table.xlsx`.

```bash
python scripts/build_figure3_panelB_btos_workforce_effects.py
python scripts/qa_figure3_panelB_btos_workforce_effects.py
```

Output: `figures/figure3_panelB_btos_workforce_effects.csv` (columns: `category_key`, `category_label`, `weighted_share`, `window_start`, `window_end`, `source_series_id`) plus `intermediate/figure3_panelB_btos_workforce_effects_run_metadata.json`. Methodology: [docs/t007_figure3_panelB_btos_workforce_effects_methodology.md](docs/t007_figure3_panelB_btos_workforce_effects_methodology.md).

## T-008 Figure 4 Panel A (JOLTS sector rates)

Requires network access to BLS LABSTAT `https://download.bls.gov/pub/time.series/jt/`.

```bash
python scripts/build_figure4_panelA_jolts_sector_rates.py
python scripts/qa_figure4_panelA_jolts_sector_rates.py
```

Output: `figures/figure4_panelA_jolts_sector_rates.csv` (columns: `month`, `sector6_code`, `sector6_label`, `rate_name`, `rate_value`, `series_id`) plus `intermediate/figure4_panelA_jolts_sector_rates_run_metadata.json`. Methodology: [docs/t008_figure4_panelA_jolts_sector_rates_methodology.md](docs/t008_figure4_panelA_jolts_sector_rates_methodology.md).

## T-009 Figure 4 Panel B (CES payroll employment index)

Requires network access to BLS LABSTAT `https://download.bls.gov/pub/time.series/ce/`.

```bash
python scripts/build_figure4_panelB_ces_sector_index.py
python scripts/qa_figure4_panelB_ces_sector_index.py
```

Output: `figures/figure4_panelB_ces_sector_index.csv` (columns: `month`, `sector6_code`, `sector6_label`, `ces_payroll_employment_thousands`, `index_aug2023_100`, `series_id`) plus `intermediate/figure4_panelB_ces_sector_index_run_metadata.json`. Methodology: [docs/t009_figure4_panelB_ces_sector_index_methodology.md](docs/t009_figure4_panelB_ces_sector_index_methodology.md).

## T-010 Figure 5 (capability matrix)

No network required. Uses in-repo `issues.md` and `paper-notes.md` as rule sources.

```bash
python scripts/build_figure5_capability_matrix.py
python scripts/qa_figure5_capability_matrix.py
```

Output: `figures/figure5_capability_matrix.csv` (columns: `dataset_label`, seven empirical-object keys, `legend_direct`, `legend_partial`, `legend_none`) plus `intermediate/figure5_capability_matrix_run_metadata.json`. Methodology: [docs/t010_figure5_capability_matrix_methodology.md](docs/t010_figure5_capability_matrix_methodology.md).

## T-011 Figure A1 (CPS ASEC annual welfare and income by AI tercile)

Requires network access to Census `https://www2.census.gov/programs-surveys/cps/datasets/<year>/march/asecpubYYcsv.zip` for each retained ASEC year (cached under `raw/cps/asec/`).

```bash
python scripts/build_figureA1_asec_welfare_by_ai_tercile.py
python scripts/qa_figureA1_asec_welfare_by_ai_tercile.py
```

Output: `figures/figureA1_asec_welfare_by_ai_tercile.csv` (columns: `year`, `ai_relevance_tercile`, `mean_annual_income`, `poverty_rate`, `mean_weeks_worked`, `unemployment_incidence`, `sum_asec_person_weight`) plus `intermediate/figureA1_asec_welfare_by_ai_tercile_run_metadata.json`. Methodology: [docs/t011_figureA1_asec_welfare_by_ai_tercile_methodology.md](docs/t011_figureA1_asec_welfare_by_ai_tercile_methodology.md).

## T-012 Figure A2 (SIPP event-study, medium-run adjustment)

Requires network access to Census `https://www2.census.gov/programs-surveys/sipp/data/datasets/<year>/pu<year>_csv.zip` for each retained SIPP panel release year (cached under `raw/sipp/`). Depends on T-002 outputs (`intermediate/ai_relevance_terciles.csv`) and crosswalks. Runtime can be 30 minutes or more on a typical laptop because each panel file is large and the build materializes a sorted SQLite table before aggregation.

```bash
python scripts/build_figureA2_sipp_event_study.py
python scripts/qa_figureA2_sipp_event_study.py
```

Output: `figures/figureA2_sipp_event_study.csv` (columns: `event_time`, `ai_relevance_tercile`, `mean_employment_rate`, `mean_monthly_income`, `mean_snap_participation`, `sum_person_weight`) plus `intermediate/figureA2_sipp_event_study_run_metadata.json`. Methodology: [docs/t012_figureA2_sipp_event_study_methodology.md](docs/t012_figureA2_sipp_event_study_methodology.md).

Operational notes:
- Build runtime can exceed 30 minutes because each panel is materialized to a temporary SQLite table, indexed, then read in sorted person-time order.
- Temporary files are created under `intermediate/` as `_sipp_panel_<year>_<uuid>.sqlite`; interrupted runs may leave these behind and they can be deleted when no build is running.
- Run only one T-012 build at a time to avoid unnecessary disk contention.
- QA enforces tercile row order per event time as `low`, `middle`, `high`; outputs with the same values but a different order will fail QA.

## T-013 Figure A3 (CPS supplement validation: displacement, tenure, mobility)

Requires network access to Census `https://www2.census.gov/programs-surveys/cps/datasets/2024/supp/jan24pub.csv` and `https://www2.census.gov/programs-surveys/cps/techdocs/cpsjan24.pdf` (cached under `raw/cps/supp/` after first run).

```bash
python scripts/build_figureA3_cps_supp_validation.py
python scripts/qa_figureA3_cps_supp_validation.py
```

Output: `figures/figureA3_cps_supp_validation.csv` (columns: `ai_relevance_tercile`, `displaced_worker_incidence`, `mean_current_job_tenure_years`, `occupational_mobility_share`, `sum_displaced_worker_person_weight`, `sum_job_tenure_person_weight`) plus `intermediate/figureA3_cps_supp_validation_run_metadata.json`. Methodology: [docs/t013_figureA3_cps_supp_validation_methodology.md](docs/t013_figureA3_cps_supp_validation_methodology.md).

## T-014 Figure A4 (ABS structural heterogeneity: technology adoption and workforce impact)

Requires network access to Census ABS tables/API (`https://www.census.gov/programs-surveys/abs/data/tables.html` and `https://api.census.gov/data/2018/abstcb`) and writes a cached API extract under `raw/abs/`.

```bash
python scripts/build_figureA4_abs_structural_adoption.py
python scripts/qa_figureA4_abs_structural_adoption.py
```

Output: `figures/figureA4_abs_structural_adoption.csv` (columns: `abs_reference_year`, `industry_code`, `industry_label`, `firm_size_class`, `measure_key`, `measure_label`, `weighted_share`, `source_table_id`) plus `intermediate/figureA4_abs_structural_adoption_run_metadata.json`. Methodology: [docs/t014_figureA4_abs_structural_adoption_methodology.md](docs/t014_figureA4_abs_structural_adoption_methodology.md).

## T-015 Figure A5 (CES payroll and hours context)

Requires network access to BLS LABSTAT CES files under `https://download.bls.gov/pub/time.series/ce/` and writes cached files under `raw/bls/ce/`.

```bash
python scripts/build_figureA5_ces_payroll_hours.py
python scripts/qa_figureA5_ces_payroll_hours.py
```

Output: `figures/figureA5_ces_payroll_hours.csv` (columns: `month`, `sector6_code`, `sector6_label`, `ces_payroll_employment_thousands`, `ces_avg_weekly_hours`, `payroll_index_aug2023_100`, `hours_index_aug2023_100`, `employment_series_id`, `hours_series_id`) plus `intermediate/figureA5_ces_payroll_hours_run_metadata.json`. Methodology: [docs/t015_figureA5_ces_payroll_hours_methodology.md](docs/t015_figureA5_ces_payroll_hours_methodology.md).

## T-016 Figure A6 (BED establishment churn)

Requires network access to BLS BED LABSTAT files under `https://download.bls.gov/pub/time.series/bd/` and writes cached files under `raw/bls/bd/`.

```bash
python scripts/build_figureA6_bed_churn.py
python scripts/qa_figureA6_bed_churn.py
```

Output: `figures/figureA6_bed_churn.csv` (columns: `quarter`, `sector6_code`, `sector6_label`, `gross_job_gains_rate`, `gross_job_losses_rate`, `openings_rate`, `closings_rate`, `gains_series_id`, `losses_series_id`, `openings_series_id`, `closings_series_id`) plus `intermediate/figureA6_bed_churn_run_metadata.json`. Methodology: [docs/t016_figureA6_bed_churn_methodology.md](docs/t016_figureA6_bed_churn_methodology.md).

## T-017 Figure A7 (QCEW state benchmark)

Requires network access to BLS QCEW downloads (`https://www.bls.gov/cew/downloadable-data-files.htm` and the latest `qtrly_singlefile` ZIP under `https://data.bls.gov/cew/data/files/<year>/csv/`) and writes cached files under `raw/bls/qcew/`.

```bash
python scripts/build_figureA7_qcew_state_benchmark.py
python scripts/qa_figureA7_qcew_state_benchmark.py
```

Output: `figures/figureA7_qcew_state_benchmark.csv` (columns: `qcew_year`, `qcew_quarter`, `state_fips`, `state_name`, `sector6_code`, `sector6_label`, `sector_employment`, `state_total_employment`, `state_sector_employment_share`, `average_weekly_wage`, `source_industry_aggregation_note`) plus `intermediate/figureA7_qcew_state_benchmark_run_metadata.json`. Methodology: [docs/t017_figureA7_qcew_state_benchmark_methodology.md](docs/t017_figureA7_qcew_state_benchmark_methodology.md).

## T-018 Figure A8 (LEHD public benchmark)

Requires network access to LEHD J2J public release endpoints under `https://lehd.ces.census.gov/data/j2j/latest_release/us/j2jr/` and writes cached files under `raw/lehd/j2j/`.

```bash
python scripts/build_figureA8_lehd_benchmark.py
python scripts/qa_figureA8_lehd_benchmark.py
```

Output: `figures/figureA8_lehd_benchmark.csv` (columns: `quarter`, `benchmark_series_key`, `benchmark_series_label`, `benchmark_rate`, `source_program`, `source_series_id`) plus `intermediate/figureA8_lehd_benchmark_run_metadata.json`. Methodology: [docs/t018_figureA8_lehd_benchmark_methodology.md](docs/t018_figureA8_lehd_benchmark_methodology.md).

## T-019 Figure A9 (ACS local occupational composition)

Requires network access to Census ACS PUMS person microdata (cached under `raw/acs/pums/`) unless the zip is already present locally.

```bash
python scripts/build_figureA9_acs_local_composition.py
python scripts/qa_figureA9_acs_local_composition.py
```

Output: `figures/figureA9_acs_local_composition.csv` (columns: `acs_year`, `puma`, `population_weight_sum`, `high_ai_tercile_share`, `middle_ai_tercile_share`, `low_ai_tercile_share`, `occ22_share_sum_check`, `occ22_share_1`..`occ22_share_22`) plus `intermediate/figureA9_acs_local_composition_run_metadata.json`. Methodology: [docs/t019_figureA9_acs_local_composition_methodology.md](docs/t019_figureA9_acs_local_composition_methodology.md).

## T-020 Figure A10 (NLS long-run career adaptation)

Requires network access to official BLS NLS public-use download endpoints at first run and writes cache under `raw/nls/`.

```bash
python scripts/build_figureA10_nls_longrun.py
python scripts/qa_figureA10_nls_longrun.py
```

Output: `figures/figureA10_nls_longrun.csv` (columns: `survey_round`, `baseline_ai_tercile`, `weighted_n`, `occupation_switch_rate`, `employment_rate`, `unemployment_rate`, `nilf_rate`, `mean_annual_earnings`, `training_participation_rate`, `source_program`, `source_series_id`) plus `intermediate/figureA10_nls_longrun_run_metadata.json`. Methodology: [docs/t020_figureA10_nls_longrun_methodology.md](docs/t020_figureA10_nls_longrun_methodology.md).

## Known Deviations From Issue Templates

- **T-006 window start:** The issue template states a locked start at `2023-08-28`. In current Census BTOS API responses, AI core rows for the national series first appear at `2023-09-11` (`PERIOD_ID 31`), so retained output begins there. See `docs/t006_figure3_panelA_btos_ai_trends_methodology.md`.
- **T-007 task-category source mapping:** The issue template specifies six frozen supplement workforce-effect categories as published shares. The current public `AI_Supplement_Table.xlsx` does not expose questionnaire item 25 option rows; implementation therefore uses documented Scope 2 proxy mappings for the three task-related keys while preserving exact published employment-effect rows. See `docs/t007_figure3_panelB_btos_workforce_effects_methodology.md`.

## Visualization Pipeline

Publication-ready static figure artifacts can be rendered from existing
`figures/*.csv` outputs without changing underlying data scripts.

```bash
python scripts/run_visuals_all.py
python scripts/qa_visuals.py
```

Outputs:
- `visuals/png/*.png`
- `visuals/vector/*.pdf`
- `intermediate/visuals_run_manifest.json`

Standards and palette rules:
- `docs/visual_style_guide.md`

## Post-implementation documentation

- Full replication (clean clone): [docs/replication.md](docs/replication.md), entrypoint `scripts/run_full_pipeline_from_raw.py`
- Acceptance matrix (issues criteria): [docs/acceptance_matrix.md](docs/acceptance_matrix.md)
- Figure catalog, captions, source notes: [docs/figure_catalog.md](docs/figure_catalog.md), `docs/captions/`, `docs/source_notes/`
- Figure memos (main text): `docs/figure_memos/fig01.md`–`fig05.md`
- Claim audit (Claims 1–5 vs Figures 1–5): [docs/claim_audit.md](docs/claim_audit.md)
- Robustness reports: `scripts/run_robustness_all.py` (outputs under `intermediate/robustness/`)
- Methods / data (consolidated): [docs/methods_data.md](docs/methods_data.md)
- Manuscript draft: [docs/paper_draft_v1_public_data_ai_labor.md](docs/paper_draft_v1_public_data_ai_labor.md)
- Appendix outline and draft: [docs/appendix_outline.md](docs/appendix_outline.md), [docs/appendix_draft.md](docs/appendix_draft.md)
- Results freeze procedure: [docs/release_process.md](docs/release_process.md), manifest `scripts/build_freeze_manifest.py`
- Independent replication checklist: [docs/replication_checklist.md](docs/replication_checklist.md)
- Caption coverage QA: `python scripts/qa_visual_caption_coverage.py`
