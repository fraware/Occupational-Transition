# Appendix Draft (Placeholder Prose)

This file contains appendix-ready paragraphs in strict order. Replace bracketed notes with final numbers and citations from the manuscript.

## Outline (strict order)

Build appendix text and figures only after main-text claims and figures are stable. Order:

1. **A1–A3:** Worker-side extensions aligned with Figure 2 (`figureA1`, `figureA2`, `figureA3`).
2. **A4:** Firm-side structural adoption (`figureA4`).
3. **A5–A8:** Demand, payroll, churn, benchmarks (`figureA5` through `figureA8`).
4. **A9–A10:** Geography and long-run careers (`figureA9`, `figureA10`).

No new appendix scope without a new ticket beyond T-020.

| Appendix | Ticket | CSV output |
|----------|--------|------------|
| A1 | T-011 | `figures/figureA1_asec_welfare_by_ai_tercile.csv` |
| A2 | T-012 | `figures/figureA2_sipp_event_study.csv` |
| A3 | T-013 | `figures/figureA3_cps_supp_validation.csv` |
| A4 | T-014 | `figures/figureA4_abs_structural_adoption.csv` |
| A5 | T-015 | `figures/figureA5_ces_payroll_hours.csv` |
| A6 | T-016 | `figures/figureA6_bed_churn.csv` |
| A7 | T-017 | `figures/figureA7_qcew_state_benchmark.csv` |
| A8 | T-018 | `figures/figureA8_lehd_benchmark.csv` |
| A9 | T-019 | `figures/figureA9_acs_local_composition.csv` |
| A10 | T-020 | `figures/figureA10_nls_longrun.csv` |

Visual stems: `asec_mean_income` through `nls_occupation_switch_rate` per [quality README — Visual style guide](../quality/README.md#visual-style-guide) and [figure catalog](../figures/figure_catalog.md) (appendix subsection to be added if needed).

---

## A1 — Annual welfare and income by AI tercile (T-011)

CPS ASEC provides annual income, poverty, weeks worked, and unemployment incidence by AI-relevance tercile on national public-use files. This appendix deepens Figure 2's monthly worker layer with annual welfare context. Identification limits follow ASEC documentation: national and state-oriented analysis is supported, while fine subnational direct estimation is not a core strength of the instrument.

**Figure:** `figures/figureA1_asec_welfare_by_ai_tercile.csv` — visual `asec_mean_income`.

## A2 — SIPP medium-run adjustment (T-012)

SIPP panel data support event-time profiles of employment, income, and program participation around occupational events at the person-month level, grouped by AI-relevance tercile. Runtime and sample-design constraints are documented in `docs/methodology/tickets/t012_figureA2_sipp_event_study_methodology.md`.

**Figure:** `figures/figureA2_sipp_event_study.csv` — visual `sipp_event_employment`.

## A3 — CPS supplement validation (T-013)

Selected CPS supplements provide direct displacement, tenure, and mobility questions. This appendix compares incidence and mobility measures by AI tercile for the retained supplement extract.

**Figure:** `figures/figureA3_cps_supp_validation.csv` — visual `cps_supp_mobility_share`.

## A4 — ABS structural adoption (T-014)

The Annual Business Survey supports a richer annual technology and workforce-impact structure than high-frequency BTOS. This appendix summarizes published ABS measure shares for retained industry and size classes in the build.

**Figure:** `figures/figureA4_abs_structural_adoption.csv` — visual `abs_measure_shares`.

## A5 — CES payroll and hours (T-015)

CES series complement Figure 4 by reporting payroll and average weekly-hours indices alongside employment for sector groups.

**Figure:** `figures/figureA5_ces_payroll_hours.csv` — visual `ces_payroll_index_mean`.

## A6 — BED churn (T-016)

Business Employment Dynamics gross job gains and losses, openings, and closings rates provide establishment-flow context at the sector level.

**Figure:** `figures/figureA6_bed_churn.csv` — visual `bed_gross_job_gains`.

## A7 — QCEW state benchmark (T-017)

QCEW supports state-level employment and wage benchmarks by detailed industry mapped to sector groups.

**Figure:** `figures/figureA7_qcew_state_benchmark.csv` — visual `qcew_top20_state_employment`.

## A8 — LEHD public benchmark (T-018)

Public LEHD J2J-style rates benchmark worker-reallocation concepts that are not occupation microdata in public release.

**Figure:** `figures/figureA8_lehd_benchmark.csv` — visual `lehd_benchmark_rate`.

## A9 — ACS local occupational composition (T-019)

ACS PUMS describes local PUMA-level occupational composition and AI-tercile shares for descriptive geographic context. This appendix does not claim short-horizon transitions from ACS alone.

**Figure:** `figures/figureA9_acs_local_composition.csv` — visual `top30_puma_high_ai_share`.

## A10 — NLSY97 long-run careers (T-020)

NLSY97 supports long-horizon occupation switching and labor-force states by baseline AI tercile. Weights and cohort restrictions follow `docs/methodology/tickets/t020_figureA10_nls_longrun_methodology.md`.

**Figure:** `figures/figureA10_nls_longrun.csv` — visual `nls_occupation_switch_rate`.
