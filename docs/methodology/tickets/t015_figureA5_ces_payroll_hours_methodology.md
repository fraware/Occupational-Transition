# T-015 — Figure A5 CES payroll and hours context

## Purpose

`figures/figureA5_ces_payroll_hours.csv` provides appendix context on
national payroll employment and average weekly hours across the frozen
six-sector taxonomy, with both metrics indexed to August 2023 = 100.

## Official data sources

All inputs are from official BLS CES LABSTAT files:

- `https://download.bls.gov/pub/time.series/ce/ce.txt`
- `https://download.bls.gov/pub/time.series/ce/ce.series`
- `https://download.bls.gov/pub/time.series/ce/ce.datatype`
- `https://download.bls.gov/pub/time.series/ce/ce.period`
- `https://download.bls.gov/pub/time.series/ce/ce.seasonal`
- `https://download.bls.gov/pub/time.series/ce/ce.data.0.ALLCESSeries`

Frozen sector mapping is read from:

- `crosswalks/sector6_crosswalk.csv`

## Variable and filter rules

The build uses only published CES national seasonally adjusted series:

- Employment level metric:
  - datatype code `01` (`ALL EMPLOYEES, THOUSANDS`)
- Hours metric:
  - datatype code `02` (`AVERAGE WEEKLY HOURS OF ALL EMPLOYEES`)
- Seasonality:
  - `seasonal = S` only
- Frequency:
  - monthly periods `M01..M12` only
- Geography:
  - national CES series (implicit in selected canonical supersector totals)

## Sector mapping and retained canonical series

Sector totals use CES supersector total industry codes
(`industry_code = supersector_code + "000000"`):

- `MFG` -> supersector `30`
- `RET` -> supersector `42`
- `INF` -> supersector `50`
- `FAS` -> supersector `55`
- `PBS` -> supersector `60`
- `HCS` -> supersector `65`

For each sector, exactly one datatype `01` series and exactly one datatype
`02` series are retained.

## Time window and indexing

- Retained window starts at `2019-01` and extends through the most recent available
  month with both employment and hours observations.
- Base month is `2023-08`.

For each sector and month:

- `payroll_index_aug2023_100 = ces_payroll_employment_thousands / payroll_base_2023_08 * 100`
- `hours_index_aug2023_100 = ces_avg_weekly_hours / hours_base_2023_08 * 100`

## Output schema

`figures/figureA5_ces_payroll_hours.csv` columns:

- `month`
- `sector6_code`
- `sector6_label`
- `ces_payroll_employment_thousands`
- `ces_avg_weekly_hours`
- `payroll_index_aug2023_100`
- `hours_index_aug2023_100`
- `employment_series_id`
- `hours_series_id`

Uniqueness key:

- `month, sector6_code`

## Reproducibility and metadata

Run from repository root:

```bash
python scripts/build_figureA5_ces_payroll_hours.py
python scripts/qa_figureA5_ces_payroll_hours.py
```

Metadata output:

- `intermediate/figureA5_ces_payroll_hours_run_metadata.json`

Metadata records:

- exact source URLs
- SHA-256 hashes for downloaded files
- retained series IDs by sector
- datatype codes and labels
- requested window start and base month

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

