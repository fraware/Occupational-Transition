# Senator Brief (Condensed): CPS and AI-Labor Measurement

## Bottom line

Public CPS data already supports a credible worker-side AI-and-labor monitoring system today, but it does not support causal AI attribution. The highest-value federal action is a modest CPS worker AI module that plugs into the existing monthly transition pipeline, improving decision quality without overpromising what the data can prove.

## What is already proven with current CPS pipeline

Using reproducible repository outputs and metadata:

- Monthly matched-person transition analysis is operational for 83 retained origin months from `2019-01` to `2026-01` in `figures/figure2_panelB_transition_probs.csv` and `intermediate/figure2_panelB_counts_run_metadata.json`. Because the official Basic CPS file for `2025-10` is missing, the retained transition-origin series omits both `2025-09` and `2025-10`; the pipeline does not bridge non-consecutive months across that gap.
- Transition probabilities are normalized and QA-checked in `docs/t005_figure2_panelB_probs_methodology.md` and `intermediate/figure2_panelB_probs_run_metadata.json`.
- Independent supplement evidence (displacement, tenure, mobility) is integrated in `figures/figureA3_cps_supp_validation.csv` with methods in `docs/t013_figureA3_cps_supp_validation_methodology.md`.
- Occupation-level rolling vulnerability signals are produced in `intermediate/cps_occ22_exit_risk_monthly.csv` (lineage in `intermediate/cps_occ22_exit_risk_monthly_run_metadata.json`).

## Core descriptive findings for policy monitoring

From `figures/figure2_panelB_transition_probs.csv` (latest origin month `2026-01`, weighted by origin mass):

- High AI-relevance tercile: retention `0.9292`, exit to unemployment-or-NILF `0.0231`.
- Middle AI-relevance tercile: retention `0.9070`, exit `0.0337`.
- Low AI-relevance tercile: retention `0.8931`, exit `0.0531`.

Across 83 retained origin months (`2019-01` to `2026-01`, excluding `2025-09` and `2025-10` because the official `2025-10` Basic CPS file is missing), average exit-to-unemployment-or-NILF rates are:

- High `0.0258`
- Middle `0.0443`
- Low `0.0621`

Supplement cross-check (`figures/figureA3_cps_supp_validation.csv`, January 2024):

- Displaced worker incidence: low `0.020291`, middle `0.018779`, high `0.015372`.
- Mean current job tenure (years): low `7.430589`, middle `7.995011`, high `8.761553`.
- Occupational mobility share: low `0.067721`, middle `0.076153`, high `0.051250`.

These are descriptive patterns and should not be interpreted as causal AI effects.

## What current CPS cannot identify

Even with the current pipeline, public-use CPS cannot directly identify:

- worker-level AI exposure intensity (no direct AI-use variable in current monthly stack),
- worker-firm matched AI treatment effects,
- precise local monthly causal AI effects separated from concurrent macro shocks.

This is consistent with guardrails in `docs/methods_data.md` and `docs/senate_briefing_memo.md`.

## Verified technical discipline (official source checks)

From `docs/references/PublicUseDocumentation_final.pdf`:

- CPS public-use weights have four implied decimals and require division by `10,000`.
- `PWCMPWGT` is the composited final weight for headline labor-force calculations.
- Month-to-month linking guidance uses `HRHHID`, `HRHHID2`, and `PULINENO`.

From `docs/references/cpsjan24.pdf`:

- `PWSUPWGT` is the displaced-worker supplement weight.
- `PWTENWGT` is the tenure/occupational-mobility supplement weight.
- Variable definitions align with `PRDISPWK`, `PTST1TN`, and `PEST20` usage in project methods.

Direct file availability check confirms `oct25pub.zip` is missing while adjacent files are available:

- `.../sep25pub.zip` -> `200`
- `.../oct25pub.zip` -> `404`
- `.../nov25pub.zip` -> `200`

## Highest-value extension path (practical, near-term)

### Recommendation

Add a compact CPS worker AI module, then merge those responses into the existing CPS transition framework.

### Minimal high-yield module components

1. AI use prevalence/intensity (`AIUSE_ANY`, `AIUSE_FREQ`, `AIUSE_TASK_SHARE`).
2. Task channel (augmentation vs substitution and domain).
3. Adaptation supports (training offered, tool mandate/optionality, role redesign).
4. Near-term perceived labor effects (hours, earnings, job security).
5. Optional short rotating follow-up for improved temporal sequencing.

### Why this is high payoff

- Converts proxy-conditioned monitoring into direct worker AI-exposure monitoring.
- Enables channel-specific policy diagnostics (for example: high AI use + low training + rising exits).
- Preserves current CPS infrastructure and reproducibility standards.

## Guardrails for testimony and oversight

- Do not claim causal AI impact estimates from CPS public-use outputs alone.
- Do not claim worker-firm linked treatment effects.
- Keep granular state-occupation-month claims pooled and denominator-checked.
- Label outputs as descriptive monitoring and risk signals.
- For policy-facing KPI tables, require uncertainty/reliability fields, deterministic
  publish/suppress flags, and explicit evidence directness labels.

## Decision-ready federal asks

1. Scope and cognitively test a short CPS AI worker module now.
2. Field and publish stable descriptive tables with full metadata lineage.
3. Evaluate an optional short follow-up design for stronger transition interpretation.

## Traceability list

- `docs/methods_data.md`
- `docs/t005_figure2_panelB_probs_methodology.md`
- `docs/t013_figureA3_cps_supp_validation_methodology.md`
- `figures/figure2_panelB_transition_probs.csv`
- `figures/figureA3_cps_supp_validation.csv`
- `intermediate/figure2_panelB_counts_run_metadata.json`
- `intermediate/figure2_panelB_probs_run_metadata.json`
- `intermediate/cps_occ22_exit_risk_monthly_run_metadata.json`
- `docs/references/PublicUseDocumentation_final.pdf`
- `docs/references/cpsjan24.pdf`
