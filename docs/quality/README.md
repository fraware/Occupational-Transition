# Quality standards

**When to read this:** Before writing KPI tables or static figure outputs; when interpreting `publish_flag`, suppression rules, or visual QA failures.

**Audience:** Authors, replicators, and anyone running `qa_*` scripts.

**Related:** [claim audit](../policy/claim_audit.md), [replication README](../replication/README.md), [figure catalog](../figures/figure_catalog.md).

## Contents

- [Reliability framework](#reliability-framework)
- [Visual style guide](#visual-style-guide)

---

## Reliability framework

This framework standardizes uncertainty, publishability, directness labels, and drift monitoring for released outputs.

### Required fields

All KPI tables must include:

- `weighted_n`, `effective_n`, `cv`
- `se`, `ci_lower`, `ci_upper`, `ci_level`, `variance_method`
- `reliability_tier`, `publish_flag`, `suppression_reason`, `pooling_applied`
- `evidence_directness` (`direct_published`, `derived_transform`, `proxy_mapping`)

### Deterministic suppression rules

Thresholds are centrally defined in `config/reliability_thresholds.json`:

- `minimum_weighted_n`
- `minimum_effective_n`
- `maximum_cv`
- `pooling_windows_months`

`publish_flag` is true only when all three criteria pass. Otherwise `suppression_reason` records deterministic reason codes.

### Uncertainty conventions

- `ci_level` defaults to 0.95.
- For transformed KPI outputs without published variance, `variance_method` uses documented approximation tags (for example `cv_approximation_kpi`).
- Ordinal or rank KPIs must not present synthetic intervals as if they were source-published precision. Keep the uncertainty columns in-schema, but set `variance_method` to an explicit non-applicable tag (for example `not_applicable_ordinal_rank`) and leave `se` / `ci_lower` / `ci_upper` blank unless the source publishes a meaningful uncertainty measure for that statistic.
- For direct published survey rates with published uncertainty, retain source-implied semantics and mark `evidence_directness=direct_published`.

### CPS transition reliability extensions

T-004 now publishes:

- `intermediate/figure2_panelB_attrition_diagnostics.csv`
- `intermediate/figure2_panelB_match_regime_robustness.csv`
- `intermediate/figure2_panelB_missing_month_sensitivity.csv`

These diagnostics cover demographic/occupation stratified matching, regime sensitivity, and missing-month scenario effects.

### Drift monitoring

Policy KPI drift is tracked in:

- `intermediate/drift/drift_dashboard.csv`
- `intermediate/drift/drift_dashboard_run_metadata.json`

Alert categories: `info`, `watch`, `critical`. Release mode fails when critical alerts are present.

### Release gates

Release-quality runs must include:

1. full ticket rebuild + QA,
2. analysis build + QA,
3. robustness checks,
4. drift dashboard build + QA,
5. freeze manifest generation.

---

## Visual style guide

This guide defines deterministic publication-ready static rendering for figure outputs (`T-001` to `T-020`).

### Scope

- Input data: `figures/*.csv` only.
- Output artifacts:
  - `visuals/png/*.png`
  - `visuals/vector/*.pdf`
- No data transformations beyond figure-level CSV content.

### Global style defaults

- Engine: Matplotlib static rendering.
- Background: white.
- Grid: light dashed grid.
- Font family: DejaVu Sans.
- Export DPI: 220.
- Default line width: 2.0.
- Default marker size: 5.0.

### Semantic color mapping

- AI terciles:
  - low: `#2ca02c`
  - middle: `#ff7f0e`
  - high: `#1f77b4`
- Neutral reference lines: `#4d4d4d`.
- Sector sequences: fixed 6-color palette in `scripts/viz_style.py`.

### Naming conventions

- Paper and appendix stems: `<chart_slug>` (no ticket prefix), for example `occupation_share_barh` and `nls_occupation_switch_rate`.
- Each stem must generate both:
  - `visuals/png/<stem>.png`
  - `visuals/vector/<stem>.pdf`

### Chart grammar by family

- Time series: line chart with consistent axis format and reference baseline when applicable.
- Matrix transitions: heatmap with fixed color scale and explicit labels.
- Composition/benchmark distributions: sorted bars or horizontal bars.
- Capability matrices: categorical heatmap with direct/partial/none legend.

### Style lock (sign-off)

After editorial sign-off, treat `scripts/viz_style.py` as frozen for this paper version: do not change fonts, palette hex values, DPI, or axis date formats for individual figures in isolation. Any global adjustment requires updating this guide, regenerating all stems under `visuals/png/` and `visuals/vector/`, and recording a new acceptance run.

Figure-to-stem mapping and caption paths: `docs/figures/figure_catalog.md`.

### Reproducibility and QA

- Render commands (paper `t001`–`t020`):
  - `python scripts/run_visuals_all.py`
- Visual QA (paper `t001`–`t020`):
  - `python scripts/qa_visuals.py`
- Caption and source-note file coverage (main text):
  - `python scripts/qa_visual_caption_coverage.py`
- QA verifies:
  - expected files exist
  - non-zero file size
  - PNG readability
  - deterministic naming
- QA writes:
  - `intermediate/visuals_run_manifest.json`
