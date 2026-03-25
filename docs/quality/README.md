# Quality standards

**When to read this:** Before writing policy-facing KPIs, memo visuals, or static figure outputs; when interpreting `publish_flag`, suppression rules, or visual QA failures.

**Audience:** Authors, replicators, and anyone running `qa_*` scripts or building memo/Virginia packs.

**Related:** [claim audit](../policy/claim_audit.md), [replication README](../replication/README.md), [figure catalog](../figures/figure_catalog.md).

## Contents

- [Reliability framework (policy-facing metrics)](#reliability-framework-policy-facing-metrics)
- [Memo visuals (T-101 to T-108): precision and non-invention rules](#memo-visuals-t-101-to-t-108-precision-and-non-invention-rules)
- [Visual style guide](#visual-style-guide)

---

## Reliability framework (policy-facing metrics)

This framework standardizes uncertainty, publishability, directness labels, and drift monitoring for policy-facing outputs.

### Required fields

All policy-facing KPI tables must include:

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
2. memo/brief build + QA,
3. robustness checks,
4. drift dashboard build + QA,
5. freeze manifest generation.

---

## Memo visuals (T-101 to T-108): precision and non-invention rules

This note documents design choices for the senator-note memo pack so outputs are reproducible, auditable, and not silently overstated. Builders live under `scripts/build_memo_*.py`; QA under `scripts/qa_memo_*.py`.

### 1. BTOS state map (`t105`) — `figures/memo_btos_state_ai_use_latest.csv`

#### Data sources and endpoints

- **Strata catalog:** `GET https://www.census.gov/hfp/btos/api/strata` — rows with `STRATA_TYPE == "state"` define valid two-letter state codes. The memo builder restricts to the fixed set **50 states + DC** (`STATE50_DC` in `scripts/build_memo_btos_state_ai_map.py`), matching the tile layout.
- **Per-state payload:** `GET .../periods/{PERIOD_ID}/data/state/{STATE_ABBR}` returns a JSON object whose values are row dicts (same pattern as national `naics2/XX` pulls in `scripts/build_figure3_panelA_btos_ai_trends.py`).

#### Period alignment (must match national trend file)

- **Rule:** `PERIOD_ID` is taken from the **last row** of `figures/figure3_panelA_btos_ai_trends.csv` after sorting by `period_start_date`.
- **Rationale:** Figure 3 Panel A is the paper’s canonical national BTOS AI series; the state map is explicitly tied to that same vintage so the memo does not mix “national latest” with “state latest” from different collection waves.

#### What is extracted (no imputation)

- **Published field only:** `OPTION_TEXT == "AI current"` and `ANSWER == "Yes"`, using `ESTIMATE_PERCENTAGE` divided by 100 for a share in `[0, 1]`. This mirrors the national extraction logic in `build_figure3_panelA_btos_ai_trends.py`.
- **No synthetic fill:** If the HTTP request fails, or the payload parses but no matching row exists, the state row is still emitted with `missing_ai_current_rate = 1`, `ai_use_current_rate` empty (NaN in CSV), and **`missing_reason`** set so readers can distinguish causes:
  - `published` — value present.
  - `fetch_failed` — network/HTTP/OS error when calling the API.
  - `no_ai_current_yes_row` — response received but no extractable AI-current Yes row (empty payload, schema change, or suppression pattern not represented as that row).

#### Quality gate

- The script **fails closed** if fewer than **45** states have `missing_reason == "published"`. That is a documentation/monitoring floor, not a statistical rule.

#### Visual semantics

- **Tile choropleth** is schematic (not a geographic projection). Colored tiles are states with a published value; **grey dashed** tiles are any non-`published` `missing_reason`. The color scale is **across published states only** (min/max of finite values).

#### CSV columns (audit trail)

| Column | Meaning |
|--------|---------|
| `missing_ai_current_rate` | `0` if a share was extracted; `1` if not. |
| `missing_reason` | `published` \| `fetch_failed` \| `no_ai_current_yes_row` (must match the flag above). |
| `ai_use_current_rate` | Share in `[0,1]` when published; empty/NaN when not. |

#### What this figure does not show

- Not worker-weighted: BTOS is establishment/firm-weighted published shares by stratum.
- Not linked to CPS outcomes: no merge to workers or occupations in this output.
- Not causal: descriptive business-reported adoption only.

---

### 2. Memo dashboard CPS entry KPIs (`t101`) — unemployment / NILF entry for **high** AI tercile

#### Inputs

- **Probabilities / summary rows:** `figures/figure2_panelB_transition_probs.csv`, `record_type == "summary"`, `origin_state` matching `occ22_*`.
- **Origin mass:** recomputed from `figures/figure2_panelB_transition_counts.csv` as, for each `(month, origin_state)`:

  `origin_mass = sum(weighted_transition_count over all destination_state rows for that origin).`

#### Why origin mass is not taken from the probs file

- The probs CSV may carry columns such as `origin_mass` that are **not valid** for merging onto summary rows (e.g. NaN for `occ22_*` summaries while matrix rows carry mass). Using those values would under-weight or drop states incorrectly.
- **Rule:** For this memo KPI only, **drop** `origin_mass`, `weighted_transition_count`, `transition_probability`, and `destination_state` from the summary slice, then **left-merge** the counts-derived `origin_mass` on `(month, origin_state)`.

#### Tercile and metric

- **Mapping:** `intermediate/ai_relevance_terciles.csv` maps `occ22_id` → `occ22_XX` → `ai_relevance_tercile`.
- **Headline:** **high** tercile only for the two KPIs `cps_unemployment_entry_rate` and `cps_nilf_entry_rate`.
- **Metrics:** `metric_name` equals `unemployment_entry_rate` and `nilf_entry_rate` respectively (same names as in `figure2_panelB_transition_probs.csv` summary rows).

#### Weighted mean formula

For a given `month`, metric `M`, and tercile `T`:

Let `O` be the set of `origin_state` values with `ai_relevance_tercile == T`. For each `o in O`, let `p(o)` be the summary `metric_value` and `w(o)` the counts-derived `origin_mass`. Rows with missing `p(o)` or `w(o)` are excluded.

\[
\text{KPI} = \frac{\sum_{o \in O} p(o)\, w(o)}{\sum_{o \in O} w(o)}
\]

This is an **origin-mass-weighted average** of published summary probabilities across high-tercile occupation groups, not a single CPS cross-tab published by BLS as-is.

#### Month selection (explicit, may differ from “latest hours month”)

- **Hours KPI** uses `max(month)` from `figures/figure2_panelA_hours_by_ai_tercile.csv`.
- **Entry KPIs** use the **latest calendar month in descending order** (from distinct `month` in the transition probs file) such that **both** unemployment-entry and NILF-entry KPIs are computable via the formula above. If the latest month is missing one of the two (or merge drops all weights), the builder walks backward until a complete month is found.
- **Consequence:** `reference_period` for hours and for entry KPIs **can differ**. When they differ, the KPI `notes_limits` and `intermediate/memo_dashboard_kpis_run_metadata.json` record the fact (`cps_dashboard_kpi_month_alignment`).

#### Limits

- Matched-month CPS constructs only; not administrative job-to-job data.
- Does not identify AI adoption or causal effects.

---

### 3. CPS month discovery (`scripts/build_figure2_panelA.py` — `discover_months_to_process`)

#### Intent

- Walk forward from **2019-01** while `month_asset_available(y, m)` is true (Census CPS Basic file exists for that month).
- **Allowlisted gaps:** months in `ALLOW_MISSING_MONTHS` are skipped without failing (documented in that module).
- **Publication lag vs. calendar time:** If a month is **before** “today’s” calendar month index and still missing (and not allowlisted), raise — that is an **unexpected interior gap**.
- If the first missing month is **at or after** the current calendar month index, **stop** and return months processed so far. That reflects **files not yet released** rather than a broken pipeline.

#### What this does not do

- It does not invent CPS files or extrapolate series past the last available microfile.

---

### Related files (memo visuals)

| Artifact | Path |
|----------|------|
| Memo dashboard KPI table | `figures/memo_dashboard_kpis.csv` |
| Dashboard build metadata | `intermediate/memo_dashboard_kpis_run_metadata.json` |
| BTOS state table | `figures/memo_btos_state_ai_use_latest.csv` |
| BTOS state build metadata | `intermediate/memo_btos_state_ai_use_latest_run_metadata.json` |
| Virginia briefing KPI table (optional; uses BTOS state row when published) | `figures/virginia_memo_kpis.csv` |
| Virginia KPI build metadata | `intermediate/virginia_memo_kpis_run_metadata.json` |
| Frozen senator brief values (Virginia) | `docs/policy/briefing/senate_briefing_evidence_baseline_va.md` |
| Figure catalog (memo + Virginia stems) | `docs/figures/figure_catalog.md` |

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

- Paper and appendix stems: `tNNN_<chart_slug>` for `T-001`–`T-020`.
- Senator memo pack (additive): stems `t101_memo_dashboard` through `t108_memo_policy_roadmap` (see `docs/figures/figure_catalog.md`).
- Virginia brief pack (additive): stems `va01_virginia_sector_composition` through `va08_virginia_occ_context` (see `docs/figures/figure_catalog.md`).
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
- Memo + Virginia stems (`t101`–`t108`, `va01`–`va06` required in Virginia QA):
  - `python scripts/run_memo_visuals_build.py`
  - `python scripts/run_memo_visuals_qa.py`
- Caption and source-note file coverage (main text):
  - `python scripts/qa_visual_caption_coverage.py`
- QA verifies:
  - expected files exist
  - non-zero file size
  - PNG readability
  - deterministic naming
- QA writes:
  - `intermediate/visuals_run_manifest.json`
