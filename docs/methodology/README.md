# Methodology

**Audience:** Anyone tracing a figure or table back to data universes, weights, time windows, and known deviations.

**Do not merge** the per-step files under [`tickets/`](tickets/): each file is the QA and review anchor for one build step (diff-friendly, deep-linked from [acceptance_matrix.md](../replication/acceptance_matrix.md) and build metadata).

## PR-000 (crosswalks and registry)

- [pr000_crosswalk_methodology.md](pr000_crosswalk_methodology.md) — occupation (`occ22`) and sector (`sector6`) crosswalks plus `docs/data_registry.csv` rules.

## Build-step index (PR-000 through T-020)

Build and QA pairs are defined in `scripts/run_full_clean_rebuild_acceptance.py`. Extensions after T-020 (for example T-021, T-022) follow the same pattern; see that script for the authoritative ordered list.

| Build step | Primary figure / output | Build script | QA script | Methodology memo |
|--------|-------------------------|--------------|-----------|------------------|
| PR-000 | Crosswalks + registry | `build_crosswalks.py` | `qa_crosswalks.py` | [pr000_crosswalk_methodology.md](pr000_crosswalk_methodology.md) |
| T-001 | Figure 1 Panel A | `build_figure1_panelA.py` | `qa_figure1_panelA.py` | [t001_figure1_panelA_methodology.md](tickets/t001_figure1_panelA_methodology.md) |
| T-002 | Figure 1 Panel B, terciles | `build_figure1_panelB.py` | `qa_figure1_panelB.py` | [t002_figure1_panelB_methodology.md](tickets/t002_figure1_panelB_methodology.md) |
| T-003 | Figure 2 Panel A | `build_figure2_panelA.py` | `qa_figure2_panelA.py` | [t003_figure2_panelA_methodology.md](tickets/t003_figure2_panelA_methodology.md) |
| T-004 | Figure 2 Panel B counts | `build_figure2_panelB_counts.py` | `qa_figure2_panelB_counts.py` | [t004_figure2_panelB_counts_methodology.md](tickets/t004_figure2_panelB_counts_methodology.md) |
| T-005 | Figure 2 Panel B probs | `build_figure2_panelB_probs.py` | `qa_figure2_panelB_probs.py` | [t005_figure2_panelB_probs_methodology.md](tickets/t005_figure2_panelB_probs_methodology.md) |
| T-006 | Figure 3 Panel A (BTOS AI) | `build_figure3_panelA_btos_ai_trends.py` | `qa_figure3_panelA_btos_ai_trends.py` | [t006_figure3_panelA_btos_ai_trends_methodology.md](tickets/t006_figure3_panelA_btos_ai_trends_methodology.md) |
| T-007 | Figure 3 Panel B (BTOS workforce) | `build_figure3_panelB_btos_workforce_effects.py` | `qa_figure3_panelB_btos_workforce_effects.py` | [t007_figure3_panelB_btos_workforce_effects_methodology.md](tickets/t007_figure3_panelB_btos_workforce_effects_methodology.md) |
| T-008 | Figure 4 Panel A (JOLTS) | `build_figure4_panelA_jolts_sector_rates.py` | `qa_figure4_panelA_jolts_sector_rates.py` | [t008_figure4_panelA_jolts_sector_rates_methodology.md](tickets/t008_figure4_panelA_jolts_sector_rates_methodology.md) |
| T-009 | Figure 4 Panel B (CES) | `build_figure4_panelB_ces_sector_index.py` | `qa_figure4_panelB_ces_sector_index.py` | [t009_figure4_panelB_ces_sector_index_methodology.md](tickets/t009_figure4_panelB_ces_sector_index_methodology.md) |
| T-010 | Figure 5 capability matrix | `build_figure5_capability_matrix.py` | `qa_figure5_capability_matrix.py` | [t010_figure5_capability_matrix_methodology.md](tickets/t010_figure5_capability_matrix_methodology.md) |
| T-011 | Appendix A1 | `build_figureA1_asec_welfare_by_ai_tercile.py` | `qa_figureA1_asec_welfare_by_ai_tercile.py` | [t011_figureA1_asec_welfare_by_ai_tercile_methodology.md](tickets/t011_figureA1_asec_welfare_by_ai_tercile_methodology.md) |
| T-012 | Appendix A2 | `build_figureA2_sipp_event_study.py` | `qa_figureA2_sipp_event_study.py` | [t012_figureA2_sipp_event_study_methodology.md](tickets/t012_figureA2_sipp_event_study_methodology.md) |
| T-013 | Appendix A3 | `build_figureA3_cps_supp_validation.py` | `qa_figureA3_cps_supp_validation.py` | [t013_figureA3_cps_supp_validation_methodology.md](tickets/t013_figureA3_cps_supp_validation_methodology.md) |
| T-014 | Appendix A4 | `build_figureA4_abs_structural_adoption.py` | `qa_figureA4_abs_structural_adoption.py` | [t014_figureA4_abs_structural_adoption_methodology.md](tickets/t014_figureA4_abs_structural_adoption_methodology.md) |
| T-015 | Appendix A5 | `build_figureA5_ces_payroll_hours.py` | `qa_figureA5_ces_payroll_hours.py` | [t015_figureA5_ces_payroll_hours_methodology.md](tickets/t015_figureA5_ces_payroll_hours_methodology.md) |
| T-016 | Appendix A6 | `build_figureA6_bed_churn.py` | `qa_figureA6_bed_churn.py` | [t016_figureA6_bed_churn_methodology.md](tickets/t016_figureA6_bed_churn_methodology.md) |
| T-017 | Appendix A7 | `build_figureA7_qcew_state_benchmark.py` | `qa_figureA7_qcew_state_benchmark.py` | [t017_figureA7_qcew_state_benchmark_methodology.md](tickets/t017_figureA7_qcew_state_benchmark_methodology.md) |
| T-018 | Appendix A8 | `build_figureA8_lehd_benchmark.py` | `qa_figureA8_lehd_benchmark.py` | [t018_figureA8_lehd_benchmark_methodology.md](tickets/t018_figureA8_lehd_benchmark_methodology.md) |
| T-019 | Appendix A9 | `build_figureA9_acs_local_composition.py` | `qa_figureA9_acs_local_composition.py` | [t019_figureA9_acs_local_composition_methodology.md](tickets/t019_figureA9_acs_local_composition_methodology.md) |
| T-020 | Appendix A10 | `build_figureA10_nls_longrun.py` | `qa_figureA10_nls_longrun.py` | [t020_figureA10_nls_longrun_methodology.md](tickets/t020_figureA10_nls_longrun_methodology.md) |

## How to read a build-step methodology memo

Use the same checklist for every `tickets/tNNN_*.md` file (and PR-000):

1. **Universe** — population, geography, and inclusion filters.
2. **Weights** — survey weights, establishment vs worker weighting, and any renormalization.
3. **Time windows** — months, years, BTOS periods, and alignment across merged sources.
4. **Construction** — variable definitions, crosswalk joins, and aggregation level.
5. **Outputs** — canonical CSV paths and columns referenced by QA.
6. **Known deviations** — differences from issue-template wording; cross-check [acceptance_matrix.md](../replication/acceptance_matrix.md) **PASS WITH NOTE** rows and the repository [README.md](../../README.md) Known Deviations if present.

For memo and Virginia-only builders (stems `t101`–`t108`, `va01`–`va08`), see [quality README — Memo visuals](../quality/README.md#memo-visuals-t-101-to-t-108-precision-and-non-invention-rules), the [Virginia case study](../states/virginia/README.md), and (when present locally) [policy/briefing/README.md](../policy/briefing/README.md).
