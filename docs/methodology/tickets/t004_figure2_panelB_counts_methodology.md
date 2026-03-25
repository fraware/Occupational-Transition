# T-004 — Figure 2 Panel B: matched-person transition counts

Last source verification refresh: 2026-03-22.

## Scope

Build national weighted transition counts between adjacent calendar months using CPS Basic Monthly public-use person records matched on public identifiers. Output is **counts only** (no row normalization; that is T-005).

## Outputs

- `figures/figure2_panelB_transition_counts.csv` — columns `month` (origin month of the transition), `origin_state`, `destination_state`, `weighted_transition_count`.
- `intermediate/figure2_panelB_counts_run_metadata.json` — months available, allowlisted gaps, per-pair match diagnostics, layout URLs, and SHA-256 hashes for origin and destination `.dat` files.

## Data sources (official)

| Role | Source |
|------|--------|
| CPS hub | U.S. Census Bureau: `https://www.census.gov/programs-surveys/cps/data/datasets.html` |
| CPS Basic Monthly | `https://www.census.gov/data/datasets/time-series/demo/cps/cps-basic.html` |
| Retrieval pattern | `https://www2.census.gov/programs-surveys/cps/datasets/<year>/basic/` |
| Weights / PEMLR | `https://www2.census.gov/programs-surveys/cps/methodology/PublicUseDocumentation_final.pdf` |
| Record layout | Year-specific `YYYY_Basic_CPS_Public_Use_Record_Layout_plus_IO_Code_list.txt`; if a year file is unavailable, the build script falls back to the 2020 layout (same pattern as T-003). |
| Revisions / gaps | `https://www.census.gov/programs-surveys/cps/data/datasets/cps-basic-footnotes.html` |

Registry: `docs/data_registry.csv` (including `census_cps_t004_public_match_key`).

## Time and geography

- **Reference period:** January 2019 through the most recent month with a published Basic CPS file (as detected at run time), paired only when two consecutive calendar months both have files.
- **Geography:** national.

## Matching key

Person records are matched across months using public-use fields `HRHHID`, `HRHHID2`, and `PULINENO` as defined in the official Basic CPS record layout for each file year. The pipeline concatenates them into a single string key after stripping whitespace.

## Universe and filters (per person-month)

Applied before matching:

1. `PRPERTYP = 2` (civilian) and `PRTAGE >= 16`.
2. `PWCMPWGT > 0` (positive composite weight after numeric parse).
3. State labels are built from `PEMLR` and `PRDTOCC1` as below.

## 24-state origin/destination system

Deterministic mapping:

- If `PEMLR` is in `{1, 2}` (employed): if `PRDTOCC1` is in `1..22`, state is `occ22_01` .. `occ22_22`; otherwise state is `nilf` (includes military occupation code 23 and other non-civilian mappings).
- If `PEMLR` is in `{3, 4}` (unemployed): state is `unemployed`.
- Otherwise: state is `nilf`.

The crosswalk `crosswalks/occ22_crosswalk.csv` documents the CPS `PRDTOCC1` 1–22 labels; this build uses numeric codes directly for the `occ22_XX` state names.

## Transitions and weights

For each pair of **consecutive calendar months** `(t, t+1)` where both monthly files exist:

1. Inner-join person rows on the match key.
2. `origin_state` is the state in month `t`; `destination_state` is the state in month `t+1`.
3. `weighted_transition_count` is the sum of `PWCMPWGT / 10_000` from the **origin** month for all matched persons in each `(origin_state, destination_state)` cell.

Rows are aggregated to `month` (origin month in `YYYY-MM` form), `origin_state`, `destination_state`.

## Missing official months

When a calendar month has no published Basic CPS file (for example October 2025 per Census footnotes), there is no adjacent pair spanning that gap. The pipeline does not impute months; it only forms pairs between months that both appear in the retrieved series. The allowlisted missing month is recorded in metadata and QA for consistency with T-003.

## Interpretation limits

These are **matched public-use record transitions**, not causal job-to-job estimates. Match rates vary by month; see `pairs` in the run metadata.

## Reproducibility commands

```bash
pip install -r requirements.txt
python scripts/build_figure2_panelB_counts.py
python scripts/qa_figure2_panelB_counts.py
```

## QA checks

Implemented in `scripts/qa_figure2_panelB_counts.py`:

- required columns and no missing values in those columns
- `origin_state` and `destination_state` in the 24-value design set
- unique `(month, origin_state, destination_state)` rows
- non-negative `weighted_transition_count`; strictly positive total weight by origin month
- origin months start at `2019-01`
- metadata `allow_missing_months` matches the project allowlist (`2025-10`)
- CSV origin months align with `pairs` in metadata

## Figure rendering

Publication-ready static visuals are generated from the existing figure CSV
outputs (no data-value changes) using:

```bash
python scripts/run_visuals_all.py
python scripts/qa_visuals.py
```

Artifacts:

- `visuals/png/*.png`
- `visuals/vector/*.pdf`
- `intermediate/visuals_run_manifest.json`

Style and chart standards are documented in `docs/quality/README.md#visual-style-guide`.

