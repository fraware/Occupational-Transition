# Methods and data (consolidated)

This document summarizes sources, universes, time windows, geography, grouping, weighting, and limitations for the reproducible pipeline (`PR-000` through `T-026`). Authoritative per-ticket detail remains in `docs/methodology/tickets/t*_methodology.md` files referenced from `README.md` and in `docs/data_registry.csv`.

## Crosswalks and registry (PR-000)

- **Occupation:** 22-group taxonomy `crosswalks/occ22_crosswalk.csv` (CPS / SOC 2018 aligned). Methodology: `docs/methodology/pr000_crosswalk_methodology.md`.
- **Sector:** Six-sector demand groups `crosswalks/sector6_crosswalk.csv` for BTOS, JOLTS, CES, BED, QCEW-aligned inputs.
- **Registry:** `docs/data_registry.csv` records canonical HTTPS download URLs, dataset identifiers, and provenance metadata fields required by QA.

## Figure 1 — Occupational baseline and task heatmap (T-001, T-002)

- **T-001:** BLS OEWS national occupation employment and median annual wage; mapped to `occ22_id`; employment shares sum to national totals within the OEWS universe.
- **T-002:** O*NET Work Activities (Importance scale) merged via SOC crosswalk; scores aggregated to `occ22_id` using OEWS employment weights within groups; z-scores across 22 groups; AI Task Index = mean of four digital-information-related task z-scores; deterministic tercile cutoffs. Outputs: `figures/figure1_panelA_occ_baseline.csv`, `figures/figure1_panelB_task_heatmap.csv`, `intermediate/ai_relevance_terciles.csv`, `intermediate/occ22_exposure_components.csv` (continuous exposure percentile for AWES; does not change frozen terciles).

**Limits:** OEWS and O*NET are not realized AI-impact measures; terciles are ordinals for grouping. OEWS is an official wage-and-salary nonfarm establishment baseline (not a full census of all workers).

## Figure 2 — CPS hours and transitions (T-003–T-005)

- **Universe:** Civilian noninstitutional population age 16+; employed with valid hours for Panel A; matched adjacent months for Panel B.
- **Weights:** CPS composite person weight (`PWCMPWGT`) scaled per methodology.
- **Time:** Monthly series from January 2019 through the most recently available month, subject to file availability rules in build scripts.
- **Geography:** National.
- **Outputs:** `figures/figure2_panelA_hours_by_ai_tercile.csv`, `figures/figure2_panelB_transition_counts.csv`, `figures/figure2_panelB_transition_probs.csv`.

**Limits:** Public-use CPS identifiers support household/person matching as implemented; not administrative job-to-job records.

## Figure 3 — BTOS (T-006, T-007)

- **Panel A:** Census BTOS API published national firm-weighted shares for AI use series retained in metadata.
- **Panel B:** Published supplement-table shares for workforce-effect categories; see methodology for the retained window and any documented proxy mapping.
- **Outputs:** `figures/figure3_panelA_btos_ai_trends.csv`, `figures/figure3_panelB_btos_workforce_effects.csv`.

**Limits:** Business-reported; not linked to worker microdata in public files. In Figure 3 Panel B, employment-effect rows are direct published rows, while task-effect interpretation is proxy-based where item-25 rows are absent.

## Figure 4 — JOLTS and CES selected-sector series (T-008, T-009)

- **Mapping:** Detailed industries or series map to `sector6_code` via `sector6_crosswalk.csv`.
- **JOLTS:** Published flow rates as selected in the build (openings, hires, quits, layoffs/discharges).
- **CES:** Payroll employment levels indexed to August 2023 = 100.
- **Outputs:** `figures/figure4_panelA_jolts_sector_rates.csv`, `figures/figure4_panelB_ces_sector_index.csv`.

**Limits:** JOLTS public core is not occupation-resolved; CES is establishment/industry-based.

## AWES and ALPI monitoring metrics (T-021–T-026)

Composite **descriptive** occupation-time indices for monitoring and prioritization. **Neither AWES nor ALPI is causal**; both are built from public sources and must be described as monitoring or prioritization metrics, not estimates of treatment effects.

- **AWES (Adoption-Weighted Exposure Score):** `metrics/awes_occ22_monthly.csv`. Normalized O*NET/OEWS exposure (`exposure_pct` from `intermediate/occ22_exposure_components.csv`) times an occupation-specific BTOS adoption mix. Weights: OEWS industry-by-occupation employment aggregated to `occ22` and frozen `sector6` (`intermediate/occ22_sector_weights.csv`); BTOS current AI-use shares by sector and month with smoothed 3-month trailing mean (`intermediate/btos_sector_ai_use_monthly.csv`). `awes_pct` is the percentile rank of `awes_raw` over all occupation-month rows. **Interpretation:** High AWES means high structural exposure and location in sectors where businesses report more AI use; low AWES means one or both are weak.

- **ALPI (AI Labor Pressure Index):** `metrics/alpi_occ22_monthly.csv`. Equal-weight average of `awes_pct`, occupation-weighted sector demand stress (`intermediate/sector6_stress_monthly.csv` from JOLTS/CES), and trailing 12-month CPS exit-risk vulnerability (`intermediate/cps_occ22_exit_risk_monthly.csv`). `alpi_pct` is the percentile rank of `alpi_raw` over occupation-month rows. **Interpretation:** High ALPI combines exposure, adoption environment, demand stress, and weaker short-run employment resilience; low ALPI means weaker joint pressure.

- **AI relevance terciles:** Default main-text grouping remains `intermediate/ai_relevance_terciles.csv` (frozen); AWES and ALPI **complement, not replace** terciles.

- **Coverage flag:** `sector6_coverage_share` and `coverage_flag_low` mark occupations with weak OEWS retained-sector employment coverage; figures and rankings should display the flag or exclude low-coverage occupations with a note.

**Limits:** AWES/ALPI inherit limits of OEWS, O*NET, BTOS, JOLTS, CES, and CPS transition constructs; they do not identify causal AI impacts.

## Figure 5 — Capability matrix (T-010)

- Non-estimated categorical matrix from `docs/lineage/t010_paper_notes_matrix.md` / `docs/lineage/t010_issues.md` rules; five datasets by seven empirical objects (including `worker_firm_ai_linkage`); `scripts/build_figure5_capability_matrix.py`.
- **Output:** `figures/figure5_capability_matrix.csv`.

## Figure 6 — Policy roadmap (synthesis; visualization-only)

- **Input:** `figures/figure6_policy_roadmap.csv` encodes box layout and narrative blocks (current public observables, identification frontier, near-term survey agenda, long-run horizon). It is a **design and synthesis** artifact aligned with the manuscript survey-design discussion (Section 8), not a statistical estimate from raw microdata.
- **Render:** `python scripts/visualize_figure6_policy_roadmap.py` writes stem `policy_roadmap` under `visuals/png` and `visuals/vector`.

**Limits:** The roadmap does not add new empirical series; it formalizes policy logic consistent with Figures 1–5 and the public-data identification frontier.

## Appendix figures (T-011–T-020) and extension metrics (T-021–T-026)

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
| T-021 | OEWS occupation–sector6 weights | `intermediate/occ22_sector_weights.csv` |
| T-022 | BTOS sector6 AI use (monthly) | `intermediate/btos_sector_ai_use_monthly.csv` |
| T-023 | AWES occupation-monthly | `metrics/awes_occ22_monthly.csv` |
| T-024 | Sector6 stress (JOLTS/CES) | `intermediate/sector6_stress_monthly.csv` |
| T-025 | CPS occ22 exit risk (12m) | `intermediate/cps_occ22_exit_risk_monthly.csv` |
| T-026 | ALPI occupation-monthly | `metrics/alpi_occ22_monthly.csv` |

Each appendix ticket has a matching `docs/methodology/tickets/tNNN_*_methodology.md` file where applicable; T-021–T-026 are documented in this section and in `intermediate/*_run_metadata.json`.

## Virginia case study (additive; not a paper figure ticket)

State-level **structural** benchmarks for Virginia (FIPS 51) are derived from **T-017** (`figures/figureA7_qcew_state_benchmark.csv`) via `scripts/build_state_qcew_deep_dive.py`, which writes `figures/state_deep_dive_qcew_51_profile.csv`, `figures/state_deep_dive_qcew_51_ranks.csv`, and `figures/state_deep_dive_qcew_51_peers.csv` with metadata in `intermediate/state_deep_dive_qcew_51_run_metadata.json`. Methodology for the underlying QCEW aggregation: `docs/methodology/tickets/t017_figureA7_qcew_state_benchmark_methodology.md`. Tracked operational summary: `docs/states/virginia/virginia_deep_dive.md` and `docs/states/virginia/README.md`.

Optional briefing KPIs and static Virginia visuals (`va01`–`va08`) use scripts such as `build_virginia_memo_kpis.py` and `visualize_virginia_memo.py` when present (see `intermediate/virginia_memo_kpis_run_metadata.json`). These outputs are **descriptive** (composition, peer comparison, ranks, optional BTOS state context when published). They do **not** identify causal AI effects or worker–firm linked impacts. Legislative narrative files under `docs/policy/briefing/` may be **local-only** in some clones; cross-cutting claim discipline remains `docs/policy/claim_audit.md` (including SB-VA rows).

## Provenance artifacts

- JSON lineage: `intermediate/*run_metadata.json` (ticket, output paths, source selection rules, SHA-256 of cached inputs where applicable).
- Full rebuild log: `intermediate/full_clean_rebuild_acceptance_*.md`.
- Acceptance summary tables (optional): `intermediate/full_clean_rebuild_acceptance_*_audit_summary.md`.
- Drift-specific closure notes (when used): `intermediate/drift_closure_<UTC>.md`.

## Reliability and suppression contract (policy-facing outputs)

Policy-facing KPI tables (memo and briefing outputs) include:

- uncertainty fields: `se`, `ci_lower`, `ci_upper`, `ci_level`, `variance_method`,
- reliability fields: `weighted_n`, `effective_n`, `cv`, `reliability_tier`,
- publishability fields: `publish_flag`, `suppression_reason`, `pooling_applied`,
- evidence directness: `evidence_directness` in `{direct_published, derived_transform, proxy_mapping}`.

Thresholds are centralized in `config/reliability_thresholds.json` and enforced in build/QA code via `occupational_transition.reliability`.

## Replication command

See `docs/replication/README.md` and `python scripts/run_full_pipeline_from_raw.py`.
