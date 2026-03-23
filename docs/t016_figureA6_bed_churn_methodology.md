# T-016 — Figure A6 BED establishment churn

## Purpose

`figures/figureA6_bed_churn.csv` provides quarterly national establishment
churn context from BLS Business Employment Dynamics (BED) for the frozen
six-sector system.

The output retains four published BED employment-rate measures:

- gross job gains rate
- gross job losses rate
- openings rate
- closings rate

## Official data sources

All inputs are official BLS BED LABSTAT files:

- `https://download.bls.gov/pub/time.series/bd/bd.txt`
- `https://download.bls.gov/pub/time.series/bd/bd.series`
- `https://download.bls.gov/pub/time.series/bd/bd.industry`
- `https://download.bls.gov/pub/time.series/bd/bd.ratelevel`
- `https://download.bls.gov/pub/time.series/bd/bd.periodicity`
- `https://download.bls.gov/pub/time.series/bd/bd.dataelement`
- `https://download.bls.gov/pub/time.series/bd/bd.unitanalysis`
- `https://download.bls.gov/pub/time.series/bd/bd.ownership`
- `https://download.bls.gov/pub/time.series/bd/bd.seasonal`
- payload:
  - preferred: `https://download.bls.gov/pub/time.series/bd/bd.data.0.Current`
  - fallback: `https://download.bls.gov/pub/time.series/bd/bd.data.1.AllItems`

Frozen mapping source:

- `crosswalks/sector6_crosswalk.csv`

## Fixed filters and code selections

Series are selected from `bd.series` using the following filter set:

- `seasonal = S`
- `state_code = 00`
- `msa_code = 00000`
- `county_code = 000`
- `unitanalysis_code = 1`
- `dataelement_code = 1` (employment-based BED measures)
- `sizeclass_code = 00`
- `ratelevel_code = R`
- `periodicity_code = Q`
- `ownership_code = 5`

Dataclass mapping for retained measures:

- `gross_job_gains_rate` -> `dataclass_code = 01`
- `openings_rate` -> `dataclass_code = 03`
- `gross_job_losses_rate` -> `dataclass_code = 04`
- `closings_rate` -> `dataclass_code = 06`

## Sector mapping and broadest BED-compatible grouping

The build uses the broadest in-scope BED industry groups from the frozen
crosswalk:

- `MFG` -> `100030`
- `RET` -> `200020`
- `INF` -> `200050`
- `FAS` -> `200060`
- `PBS` -> `200070`
- `HCS` -> `200080`

## Time window and retention rule

- Requested minimum quarter: `2019-Q1`.
- The retained output window is the intersection of quarters with complete
  coverage across all six sectors and all four measures.

## Output schema

`figures/figureA6_bed_churn.csv` columns:

- `quarter`
- `sector6_code`
- `sector6_label`
- `gross_job_gains_rate`
- `gross_job_losses_rate`
- `openings_rate`
- `closings_rate`
- `gains_series_id`
- `losses_series_id`
- `openings_series_id`
- `closings_series_id`

Uniqueness key:

- `quarter, sector6_code`

## Reproducibility and metadata

Run from repository root:

```bash
python scripts/build_figureA6_bed_churn.py
python scripts/qa_figureA6_bed_churn.py
```

Metadata output:

- `intermediate/figureA6_bed_churn_run_metadata.json`

Metadata records:

- exact source URLs and SHA-256 hashes
- payload selection decision (`bd.data.0.Current` vs fallback)
- filter codes used for series resolution
- retained series IDs by sector
- quarter window retained

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

Style and chart standards are documented in `docs/visual_style_guide.md`.

