# Appendix Draft (Placeholder Prose)

This file contains appendix-ready paragraphs in the order defined in `docs/appendix_outline.md`. Replace bracketed notes with final numbers and citations from the manuscript.

## A1 — Annual welfare and income by AI tercile (T-011)

CPS ASEC provides annual income, poverty, weeks worked, and unemployment incidence by AI-relevance tercile on national public-use files. This appendix deepens Figure 2's monthly worker layer with annual welfare context. Identification limits follow ASEC documentation: national and state-oriented analysis is supported, while fine subnational direct estimation is not a core strength of the instrument.

**Figure:** `figures/figureA1_asec_welfare_by_ai_tercile.csv` — visual `t011_asec_mean_income`.

## A2 — SIPP medium-run adjustment (T-012)

SIPP panel data support event-time profiles of employment, income, and program participation around occupational events at the person-month level, grouped by AI-relevance tercile. Runtime and sample-design constraints are documented in `docs/t012_figureA2_sipp_event_study_methodology.md`.

**Figure:** `figures/figureA2_sipp_event_study.csv` — visual `t012_sipp_event_employment`.

## A3 — CPS supplement validation (T-013)

Selected CPS supplements provide direct displacement, tenure, and mobility questions. This appendix compares incidence and mobility measures by AI tercile for the retained supplement extract.

**Figure:** `figures/figureA3_cps_supp_validation.csv` — visual `t013_cps_supp_mobility_share`.

## A4 — ABS structural adoption (T-014)

The Annual Business Survey supports a richer annual technology and workforce-impact structure than high-frequency BTOS. This appendix summarizes published ABS measure shares for retained industry and size classes in the build.

**Figure:** `figures/figureA4_abs_structural_adoption.csv` — visual `t014_abs_measure_shares`.

## A5 — CES payroll and hours (T-015)

CES series complement Figure 4 by reporting payroll and average weekly-hours indices alongside employment for sector groups.

**Figure:** `figures/figureA5_ces_payroll_hours.csv` — visual `t015_ces_payroll_index_mean`.

## A6 — BED churn (T-016)

Business Employment Dynamics gross job gains and losses, openings, and closings rates provide establishment-flow context at the sector level.

**Figure:** `figures/figureA6_bed_churn.csv` — visual `t016_bed_gross_job_gains`.

## A7 — QCEW state benchmark (T-017)

QCEW supports state-level employment and wage benchmarks by detailed industry mapped to sector groups.

**Figure:** `figures/figureA7_qcew_state_benchmark.csv` — visual `t017_qcew_top20_state_employment`.

## A8 — LEHD public benchmark (T-018)

Public LEHD J2J-style rates benchmark worker-reallocation concepts that are not occupation microdata in public release.

**Figure:** `figures/figureA8_lehd_benchmark.csv` — visual `t018_lehd_benchmark_rate`.

## A9 — ACS local occupational composition (T-019)

ACS PUMS describes local PUMA-level occupational composition and AI-tercile shares for descriptive geographic context. This appendix does not claim short-horizon transitions from ACS alone.

**Figure:** `figures/figureA9_acs_local_composition.csv` — visual `t019_top30_puma_high_ai_share`.

## A10 — NLSY97 long-run careers (T-020)

NLSY97 supports long-horizon occupation switching and labor-force states by baseline AI tercile. Weights and cohort restrictions follow `docs/t020_figureA10_nls_longrun_methodology.md`.

**Figure:** `figures/figureA10_nls_longrun.csv` — visual `t020_nls_occupation_switch_rate`.
