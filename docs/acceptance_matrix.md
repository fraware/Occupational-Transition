# Acceptance matrix (issues.md criteria)

This matrix maps each ticket to outputs, the acceptance language in `issues.md`, the automated QA script, and a recorded result. **Update the Result and Evidence columns after each full acceptance run.**

Evidence should point to:

- `intermediate/full_clean_rebuild_acceptance_<UTC>.md` (strict rebuild log)
- Ticket methodology doc `docs/t*_methodology.md` for interpretation

## Gate: main-text files (must pass before treating main results as final)

These outputs are required for the main-text empirical spine. Automated QA scripts enforce schema, domains, normalization, and (where applicable) local source-file hashes recorded in `intermediate/*run_metadata.json`.

| Output | Path | Result | Notes |
|--------|------|--------|-------|
| Figure 1 Panel A | `figures/figure1_panelA_occ_baseline.csv` | PASS | 22 rows; shares sum to 1 within tolerance. QA: `qa_figure1_panelA.py` |
| Figure 1 Panel B | `figures/figure1_panelB_task_heatmap.csv` | PASS | Heatmap + AI index. QA: `qa_figure1_panelB.py` |
| AI terciles | `intermediate/ai_relevance_terciles.csv` | PASS | Produced with T-002. QA: `qa_figure1_panelB.py` |
| Figure 2 Panel A | `figures/figure2_panelA_hours_by_ai_tercile.csv` | PASS | One row per month x tercile per issues criterion. QA: `qa_figure2_panelA.py` |
| Figure 2 Panel B | `figures/figure2_panelB_transition_probs.csv` | PASS | Row-normalized probabilities sum to 1 per month x origin. QA: `qa_figure2_panelB_probs.py` |
| Figure 3 Panel A | `figures/figure3_panelA_btos_ai_trends.csv` | PASS | Published weighted shares per period. QA: `qa_figure3_panelA_btos_ai_trends.py` |
| Figure 3 Panel B | `figures/figure3_panelB_btos_workforce_effects.csv` | PASS WITH NOTE | See `README.md` Known Deviations (T-007 task-category mapping). QA: `qa_figure3_panelB_btos_workforce_effects.py` |
| Figure 4 Panel A | `figures/figure4_panelA_jolts_sector_rates.csv` | PASS | QA: `qa_figure4_panelA_jolts_sector_rates.py` |
| Figure 4 Panel B | `figures/figure4_panelB_ces_sector_index.csv` | PASS | QA: `qa_figure4_panelB_ces_sector_index.py` |
| Figure 5 | `figures/figure5_capability_matrix.csv` | PASS | Five datasets x seven empirical objects plus legend columns. QA: `qa_figure5_capability_matrix.py` |

**Gate rule:** Do not move on to manuscript freeze until every main-text row is **PASS** or **PASS WITH NOTE** (no **FAIL**). A **PASS WITH NOTE** must cite the methodology doc and any deviation from the literal issue template.

---

## Full ticket list (PR-000 through T-020)

| Ticket | Primary outputs | Acceptance criterion (summary from issues.md) | QA script | Result |
|--------|-----------------|-----------------------------------------------|-----------|--------|
| PR-000 | `crosswalks/occ22_crosswalk.csv`, `crosswalks/sector6_crosswalk.csv`, `docs/data_registry.csv` | Unique mappings; registry rows for sources used | `qa_crosswalks.py` | PASS |
| T-001 | `figures/figure1_panelA_occ_baseline.csv` | 22 rows; employment shares sum to 1 | `qa_figure1_panelA.py` | PASS |
| T-002 | `figures/figure1_panelB_task_heatmap.csv`, `intermediate/ai_relevance_terciles.csv` | Task heatmap + tercile assignment rules | `qa_figure1_panelB.py` | PASS |
| T-003 | `figures/figure2_panelA_hours_by_ai_tercile.csv` | One row per month x tercile; no missing combinations after start | `qa_figure2_panelA.py` | PASS |
| T-004 | `figures/figure2_panelB_transition_counts.csv` | One row per origin x destination x month; positive origin mass | `qa_figure2_panelB_counts.py` | PASS |
| T-005 | `figures/figure2_panelB_transition_probs.csv` | Probabilities sum to 1 per month x origin | `qa_figure2_panelB_probs.py` | PASS |
| T-006 | `figures/figure3_panelA_btos_ai_trends.csv` | One row per BTOS period with published rates | `qa_figure3_panelA_btos_ai_trends.py` | PASS WITH NOTE |
| T-007 | `figures/figure3_panelB_btos_workforce_effects.csv` | Supplement workforce shares | `qa_figure3_panelB_btos_workforce_effects.py` | PASS WITH NOTE |
| T-008 | `figures/figure4_panelA_jolts_sector_rates.csv` | JOLTS sector rates | `qa_figure4_panelA_jolts_sector_rates.py` | PASS |
| T-009 | `figures/figure4_panelB_ces_sector_index.csv` | CES index by sector | `qa_figure4_panelB_ces_sector_index.py` | PASS |
| T-010 | `figures/figure5_capability_matrix.csv` | 5 x 7 matrix + legend; no extra rows/columns | `qa_figure5_capability_matrix.py` | PASS |
| T-011 | `figures/figureA1_asec_welfare_by_ai_tercile.csv` | Year x tercile welfare rows | `qa_figureA1_asec_welfare_by_ai_tercile.py` | PASS |
| T-012 | `figures/figureA2_sipp_event_study.csv` | Event-study panel output | `qa_figureA2_sipp_event_study.py` | PASS |
| T-013 | `figures/figureA3_cps_supp_validation.csv` | Supplement validation metrics | `qa_figureA3_cps_supp_validation.py` | PASS |
| T-014 | `figures/figureA4_abs_structural_adoption.csv` | ABS structural adoption | `qa_figureA4_abs_structural_adoption.py` | PASS |
| T-015 | `figures/figureA5_ces_payroll_hours.csv` | CES payroll/hours context | `qa_figureA5_ces_payroll_hours.py` | PASS |
| T-016 | `figures/figureA6_bed_churn.csv` | BED churn | `qa_figureA6_bed_churn.py` | PASS |
| T-017 | `figures/figureA7_qcew_state_benchmark.csv` | QCEW benchmark | `qa_figureA7_qcew_state_benchmark.py` | PASS |
| T-018 | `figures/figureA8_lehd_benchmark.csv` | LEHD benchmark | `qa_figureA8_lehd_benchmark.py` | PASS |
| T-019 | `figures/figureA9_acs_local_composition.csv` | ACS local composition | `qa_figureA9_acs_local_composition.py` | PASS |
| T-020 | `figures/figureA10_nls_longrun.csv` | NLS long-run outcomes | `qa_figureA10_nls_longrun.py` | PASS |

### Documented deviations (PASS WITH NOTE)

| Ticket | Issue | Resolution |
|--------|-------|------------|
| T-006 | Template start date `2023-08-28` vs first BTOS AI core period | Retained series begins at first API period with AI core questions (`README.md` Known Deviations). |
| T-007 | Six frozen supplement categories vs XLSX structure | Documented Scope 2 proxy mapping for task-related keys (`README.md` Known Deviations). |

## Manual review (not fully encoded in QA)

Reviewers should confirm:

- Substantive claims in the manuscript match the resolution limits in each `docs/t*_methodology.md`.
- Dynamic source selection (latest PUMS, NLSY97 zip, CPS monthly files) matches the `source_selection_rule` fields in run metadata for the snapshot you are citing.

## Sign-off

| Role | Name | Date | Acceptance log path |
|------|------|------|----------------------|
| Implementer | | | |
| Reviewer | | | |
