# T-017 — Figure A7 QCEW state benchmark

## Purpose

`figures/figureA7_qcew_state_benchmark.csv` provides a state-level benchmark
for the frozen six-sector system using official BLS QCEW published values.
The output retains one reference period and reports:

- sector employment
- state total employment (within the six in-scope sectors)
- state sector employment share
- average weekly wage

## Official data sources

All T-017 inputs are official BLS QCEW public sources:

- `https://www.bls.gov/cew/downloadable-data-files.htm`
- `https://data.bls.gov/cew/data/files/2025/csv/2025_qtrly_singlefile.zip`
- frozen mapping:
  - `crosswalks/sector6_crosswalk.csv`

## Retained period and deterministic selection

Selection rule implemented in build metadata:

1. Parse the official QCEW downloadable-files page.
2. Select the most recent available `qtrly_singlefile` link year.
3. Within that file, retain the most recent observed quarter.

In the documented run example, this resolves to:

- `qcew_year = 2025`
- `qcew_quarter = Q3`

## Filters and mapping

Rows are filtered to:

- `own_code = 1` (private ownership, published QCEW values)
- state geography only (`area_fips` ends with `000`, excluding `00000`)
- NAICS rows mapped by 2-digit prefix to the frozen six-sector crosswalk
  (`QCEW` + `qcew_naics2_via_ces`, `is_in_scope = 1`)

## Aggregation and normalization

For each retained `state × sector6` cell:

- `sector_employment`: sum of `month3_emplvl` across retained mapped rows
- `average_weekly_wage`: employment-weighted mean of published
  `avg_wkly_wage` across retained mapped rows

State denominator:

- `state_total_employment = sum(sector_employment)` over six sectors in each
  state.

Share definition:

- `state_sector_employment_share = sector_employment / state_total_employment`

## Output schema

`figures/figureA7_qcew_state_benchmark.csv` columns:

- `qcew_year`
- `qcew_quarter`
- `state_fips`
- `state_name`
- `sector6_code`
- `sector6_label`
- `sector_employment`
- `state_total_employment`
- `state_sector_employment_share`
- `average_weekly_wage`
- `source_industry_aggregation_note`

Uniqueness key:

- `qcew_year, qcew_quarter, state_fips, sector6_code`

## Reproducibility and metadata

Run from repository root:

```bash
python scripts/build_figureA7_qcew_state_benchmark.py
python scripts/qa_figureA7_qcew_state_benchmark.py
```

Metadata output:

- `intermediate/figureA7_qcew_state_benchmark_run_metadata.json`

Metadata records:

- exact source URLs and SHA-256 hashes
- retained period and deterministic selection rule
- crosswalk lineage and crosswalk SHA-256
- filter codes and aggregation conventions

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

## Related additive outputs (not T-017 QA)

Virginia-specific tables and visuals derived from `figures/figureA7_qcew_state_benchmark.csv` are documented in `docs/states/virginia/virginia_deep_dive.md` and built via `scripts/build_state_qcew_deep_dive.py` (separate from this ticket’s QA script).

