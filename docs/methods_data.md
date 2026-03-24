# Methods and data (consolidated)

This document summarizes sources, universes, time windows, geography, grouping, weighting, and limitations for the reproducible pipeline (`PR-000` through `T-020`). Authoritative per-ticket detail remains in `docs/t*_methodology.md` rows referenced from `README.md` and in `docs/data_registry.csv`.

## Crosswalks and registry (PR-000)

- **Occupation:** 22-group taxonomy `crosswalks/occ22_crosswalk.csv` (CPS / SOC 2018 aligned). Methodology: `docs/pr000_crosswalk_methodology.md`.
- **Sector:** Six-sector demand groups `crosswalks/sector6_crosswalk.csv` for BTOS, JOLTS, CES, BED, QCEW-aligned inputs.
- **Registry:** `docs/data_registry.csv` records canonical HTTPS download URLs, dataset identifiers, and provenance metadata fields required by QA.

## Figure 1 — Occupational baseline and task heatmap (T-001, T-002)

- **T-001:** BLS OEWS national occupation employment and median annual wage; mapped to `occ22_id`; employment shares sum to national totals within the OEWS universe.
- **T-002:** O*NET Work Activities (Importance scale) merged via SOC crosswalk; scores aggregated to `occ22_id` using OEWS employment weights within groups; z-scores across 22 groups; AI Task Index = mean of four digital-information-related task z-scores; deterministic tercile cutoffs. Outputs: `figures/figure1_panelA_occ_baseline.csv`, `figures/figure1_panelB_task_heatmap.csv`, `intermediate/ai_relevance_terciles.csv`.

**Limits:** OEWS and O*NET are not realized AI-impact measures; terciles are ordinals for grouping.

## Figure 2 — CPS hours and transitions (T-003–T-005)

- **Universe:** Civilian noninstitutional population age 16+; employed with valid hours for Panel A; matched adjacent months for Panel B.
- **Weights:** CPS composite person weight (`PWCMPWGT`) scaled per methodology.
- **Time:** Monthly series from January 2019 through the most recently available month, subject to file availability rules in build scripts.
- **Geography:** National.
- **Outputs:** `figures/figure2_panelA_hours_by_ai_tercile.csv`, `figures/figure2_panelB_transition_counts.csv`, `figures/figure2_panelB_transition_probs.csv`.

**Limits:** Public-use CPS identifiers support household/person matching as implemented; not administrative job-to-job records.

## Figure 3 — BTOS (T-006, T-007)

- **Panel A:** Census BTOS API published national firm-weighted shares for AI use series retained in metadata.
- **Panel B:** Published supplement table shares for workforce-effect categories; see methodology for window and any documented proxy mapping.
- **Outputs:** `figures/figure3_panelA_btos_ai_trends.csv`, `figures/figure3_panelB_btos_workforce_effects.csv`.

**Limits:** Business-reported; not linked to worker microdata in public files.

## Figure 4 — JOLTS and CES sector series (T-008, T-009)

- **Mapping:** Detailed industries or series map to `sector6_code` via `sector6_crosswalk.csv`.
- **JOLTS:** Published flow rates as selected in the build (openings, hires, quits, layoffs/discharges).
- **CES:** Payroll employment levels indexed to August 2023 = 100.
- **Outputs:** `figures/figure4_panelA_jolts_sector_rates.csv`, `figures/figure4_panelB_ces_sector_index.csv`.

**Limits:** JOLTS public core is not occupation-resolved; CES is establishment/industry-based.

## Figure 5 — Capability matrix (T-010)

- Non-estimated categorical matrix from `paper-notes.md` / `issues.md` rules; five datasets by seven empirical objects (including `worker_firm_ai_linkage`); `scripts/build_figure5_capability_matrix.py`.
- **Output:** `figures/figure5_capability_matrix.csv`.

## Appendix figures (T-011–T-020)

| Ticket | Short description | Primary output CSV |
|--------|-------------------|-------------------|
| T-011 | CPS ASEC welfare by AI tercile | `figures/figureA1_asec_welfare_by_ai_tercile.csv` |
| T-012 | SIPP event-study panel | `figures/figureA2_sipp_event_study.csv` |
| T-013 | CPS supplement validation | `figures/figureA3_cps_supp_validation.csv` |
| T-014 | ABS structural adoption | `figures/figureA4_abs_structural_adoption.csv` |
| T-015 | CES payroll/hours context | `figures/figureA5_ces_payroll_hours.csv` |
| T-016 | BED churn | `figures/figureA6_bed_churn.csv` |
| T-017 | QCEW state benchmark | `figures/figureA7_qcew_state_benchmark.csv` |
| T-018 | LEHD public benchmark | `figures/figureA8_lehd_benchmark.csv` |
| T-019 | ACS PUMS local composition | `figures/figureA9_acs_local_composition.csv` |
| T-020 | NLSY97 long-run outcomes | `figures/figureA10_nls_longrun.csv` |

Each ticket has a matching `docs/tNNN_*_methodology.md` file with full source and universe detail.

## Provenance artifacts

- JSON lineage: `intermediate/*run_metadata.json` (ticket, output paths, source selection rules, SHA-256 of cached inputs where applicable).
- Full rebuild log: `intermediate/full_clean_rebuild_acceptance_*.md`.
- Acceptance summary tables (optional): `intermediate/full_clean_rebuild_acceptance_*_audit_summary.md`.
- Drift-specific closure notes (when used): `intermediate/drift_closure_<UTC>.md`.

## Replication command

See `docs/replication.md` and `python scripts/run_full_pipeline_from_raw.py`.
