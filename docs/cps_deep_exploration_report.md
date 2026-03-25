# CPS Deep Exploration: Current Frontier and High-Value Extension Potential

## Why this is evidence-first

This report only uses:
- reproducible repository artifacts in `figures/`, `intermediate/`, and `docs/`,
- direct technical documentation from official Census CPS sources,
- direct URL availability checks for CPS monthly files.

No claim below is intended as causal identification of AI effects.

## 1) What CPS already does well in this project

Current pipeline evidence shows CPS already supports a strong worker-side monitoring stack:

- **Monthly labor flow measurement by occupation group and AI tercile** using matched adjacent months (`2019-01` through `2026-01` origin months, with documented handling of `2025-10` gap) from `figures/figure2_panelB_transition_probs.csv` and `intermediate/figure2_panelB_counts_run_metadata.json`.
- **Weighted transition normalization and QA discipline** (row-normalized matrix plus summary metrics) in `docs/t005_figure2_panelB_probs_methodology.md` and `intermediate/figure2_panelB_probs_run_metadata.json`.
- **Supplement-based external validation** (displacement, tenure, occupational mobility) in `figures/figureA3_cps_supp_validation.csv` and `docs/t013_figureA3_cps_supp_validation_methodology.md`.
- **Rolling occupation vulnerability construct** (`intermediate/cps_occ22_exit_risk_monthly.csv`, 1,826 rows) derived from transition probabilities, documented in `scripts/build_cps_occ22_exit_risk_monthly.py` and `intermediate/cps_occ22_exit_risk_monthly_run_metadata.json`.

## 2) Quantitative baseline findings (descriptive only)

### Latest matched month snapshot

From `figures/figure2_panelB_transition_probs.csv` (latest origin month `2026-01`, weighted by origin mass and grouped by frozen AI terciles):

- `high` tercile: retention `0.9292`, exit to unemployment-or-NILF `0.0231`.
- `middle` tercile: retention `0.9070`, exit `0.0337`.
- `low` tercile: retention `0.8931`, exit `0.0531`.

These are descriptive transition shares, not AI treatment effects.

### Multi-year pattern

Across 83 origin months (`2019-01` to `2026-01`), weighted average exit-to-unemployment-or-NILF by tercile:

- `high`: `0.0258`
- `middle`: `0.0443`
- `low`: `0.0621`

Average gap (`high - low`) is `-0.0363` (min `-0.1862`, max `-0.0207`), indicating persistent cross-tercile separation in this descriptive metric.

### Supplement cross-check (January 2024)

From `figures/figureA3_cps_supp_validation.csv`:

- Displaced worker incidence: `low 0.020291`, `middle 0.018779`, `high 0.015372`.
- Mean current job tenure (years): `low 7.430589`, `middle 7.995011`, `high 8.761553`.
- Occupational mobility share: `low 0.067721`, `middle 0.076153`, `high 0.051250`.

This triangulates that the transition signal is not a single-metric artifact.

## 3) What CPS cannot identify yet (hard limits)

Even with the current strong pipeline, CPS public-use data in this configuration cannot identify:

- **Direct worker AI exposure/use** (no worker-level AI usage intensity or task-channel variable in the current monthly stack).
- **Worker-firm linkage** (no employer AI adoption matched to individual workers in public CPS files).
- **Fine local monthly causal inference** (sample and confidentiality constraints; public-use perturbation caveat in CPS public-use documentation).
- **Pure AI-attributable transitions** versus macro/industry shocks without stronger design and/or external linkage.

These limits are consistent with `docs/methods_data.md` and guardrails in `docs/senate_briefing_memo.md`.

## 4) Verified technical cross-checks against official sources

### CPS core weighting and universes

From `docs/references/PublicUseDocumentation_final.pdf`:

- CPS public-use weights have **four implied decimals** and must be divided by `10,000`.
- `PWCMPWGT` is the composited final weight used for headline labor-force calculations.
- Civilian noninstitutional population concept aligns with `PRPERTYP = 2` and age filter logic used in repo methods.
- Linking guidance references `HRHHID`, `HRHHID2`, and `PULINENO` for month-to-month person matching.

### January 2024 supplement weighting and variables

From `docs/references/cpsjan24.pdf`:

- `PWSUPWGT` is the displaced worker supplement weight.
- `PWTENWGT` is the employee tenure/occupational mobility supplement weight.
- `PRDISPWK`, `PTST1TN`, and `PEST20` definitions align with `docs/t013_figureA3_cps_supp_validation_methodology.md`.

### Missing month validation

Direct source URL checks confirm:
- `https://www2.census.gov/programs-surveys/cps/datasets/2025/basic/sep25pub.zip` -> `200`
- `https://www2.census.gov/programs-surveys/cps/datasets/2025/basic/oct25pub.zip` -> `404`
- `https://www2.census.gov/programs-surveys/cps/datasets/2025/basic/nov25pub.zip` -> `200`

This supports the allowlist handling of `2025-10` in metadata.

## 5) Full potential: where a modest CPS extension creates large AI-labor value

The highest marginal value comes from adding a small worker-side AI module that can be integrated with existing CPS longitudinal flow machinery.

Why this is high leverage:

- The project already has robust monthly transition infrastructure and QA.
- A direct AI-use signal at worker level would convert current **proxy-conditioned monitoring** into **direct exposure-stratified monitoring**.
- This enables policy-relevant risk decomposition without requiring a greenfield data architecture.

High-value extension components (details in blueprint):

1. Worker AI-use intensity and frequency.
2. Task channel (substitution vs augmentation) and domain of use.
3. Employer support/adaptation channel (training, role redesign).
4. Perceived near-term job/hours/wage effect signal.
5. Optional short rotating follow-up panel to measure transition differentials by reported AI exposure.

## 6) Non-claim boundaries (strict)

Even after extension, CPS alone still does not give:

- firm-level causal treatment effects,
- full worker-firm matched causal panels,
- exact decomposition of AI vs all concurrent macro shocks without additional assumptions.

The gain is major for **measurement and monitoring precision**, not full causal closure.

## 7) Traceability index

- Core methods overview: `docs/methods_data.md`
- Figure 2 Panel A methods: `docs/t003_figure2_panelA_methodology.md`
- Figure 2 Panel B probabilities: `docs/t005_figure2_panelB_probs_methodology.md`
- Supplement validation methods: `docs/t013_figureA3_cps_supp_validation_methodology.md`
- Transition outputs: `figures/figure2_panelB_transition_probs.csv`
- Supplement outputs: `figures/figureA3_cps_supp_validation.csv`
- Transition metadata: `intermediate/figure2_panelB_counts_run_metadata.json`, `intermediate/figure2_panelB_probs_run_metadata.json`
- Exit-risk metadata: `intermediate/cps_occ22_exit_risk_monthly_run_metadata.json`
- Official CPS public-use documentation: `docs/references/PublicUseDocumentation_final.pdf`
- Official January 2024 supplement technical documentation: `docs/references/cpsjan24.pdf`
