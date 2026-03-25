# Reliability framework (policy-facing metrics)

This framework standardizes uncertainty, publishability, directness labels, and drift monitoring for policy-facing outputs.

## Required fields

All policy-facing KPI tables must include:

- `weighted_n`, `effective_n`, `cv`
- `se`, `ci_lower`, `ci_upper`, `ci_level`, `variance_method`
- `reliability_tier`, `publish_flag`, `suppression_reason`, `pooling_applied`
- `evidence_directness` (`direct_published`, `derived_transform`, `proxy_mapping`)

## Deterministic suppression rules

Thresholds are centrally defined in `config/reliability_thresholds.json`:

- `minimum_weighted_n`
- `minimum_effective_n`
- `maximum_cv`
- `pooling_windows_months`

`publish_flag` is true only when all three criteria pass. Otherwise `suppression_reason` records deterministic reason codes.

## Uncertainty conventions

- `ci_level` defaults to 0.95.
- For transformed KPI outputs without published variance, `variance_method` uses documented approximation tags (for example `cv_approximation_kpi`).
- Ordinal or rank KPIs must not present synthetic intervals as if they were source-published precision. Keep the uncertainty columns in-schema, but set `variance_method` to an explicit non-applicable tag (for example `not_applicable_ordinal_rank`) and leave `se` / `ci_lower` / `ci_upper` blank unless the source publishes a meaningful uncertainty measure for that statistic.
- For direct published survey rates with published uncertainty, retain source-implied semantics and mark `evidence_directness=direct_published`.

## CPS transition reliability extensions

T-004 now publishes:

- `intermediate/figure2_panelB_attrition_diagnostics.csv`
- `intermediate/figure2_panelB_match_regime_robustness.csv`
- `intermediate/figure2_panelB_missing_month_sensitivity.csv`

These diagnostics cover demographic/occupation stratified matching, regime sensitivity, and missing-month scenario effects.

## Drift monitoring

Policy KPI drift is tracked in:

- `intermediate/drift/drift_dashboard.csv`
- `intermediate/drift/drift_dashboard_run_metadata.json`

Alert categories: `info`, `watch`, `critical`. Release mode fails when critical alerts are present.

## Release gates

Release-quality runs must include:

1. full ticket rebuild + QA,
2. memo/brief build + QA,
3. robustness checks,
4. drift dashboard build + QA,
5. freeze manifest generation.
