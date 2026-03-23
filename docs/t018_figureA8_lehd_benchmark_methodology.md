# T-018 — Figure A8 LEHD public benchmark

## Purpose

`figures/figureA8_lehd_benchmark.csv` provides a national quarterly benchmark
series from public LEHD Job-to-Job Rates (J2JR) data.

This appendix output is intentionally benchmark-only context and does not
reconstruct microdata transitions.

## Official data sources

All retained inputs are official Census LEHD public endpoints:

- `https://lehd.ces.census.gov/data/j2j/latest_release/us/`
- `https://lehd.ces.census.gov/data/j2j/latest_release/us/j2jr/j2jr_us_manifest.txt`
- `https://lehd.ces.census.gov/data/j2j/latest_release/us/j2jr/j2jr_us_d_f_gn_n_oslp_s.csv.gz`

## Benchmark definition and filters

Retained benchmark:

- `J2JHireR` from the J2JR compact national seasonally adjusted table

Applied fixed filters:

- `periodicity = Q`
- `seasonadj = S`
- `geo_level = N`, `geography = 00` (national only)
- `ind_level = A`, `industry = 00` (all industries)
- `ownercode = A00`
- `sex = 0`, `agegrp = A00`, `race = A0`, `ethnicity = A0`, `education = E0`
- `firmage = 0`, `firmsize = 0`
- `agg_level = 1`

## Time window

- Requested minimum quarter: `2019-Q1`
- Retained output: contiguous quarterly series from `2019-Q1` through latest
  available retained quarter in the current release.

## Output schema

`figures/figureA8_lehd_benchmark.csv` columns:

- `quarter`
- `benchmark_series_key`
- `benchmark_series_label`
- `benchmark_rate`
- `source_program`
- `source_series_id`

Uniqueness key:

- `quarter`

## Reproducibility and metadata

Run from repository root:

```bash
python scripts/build_figureA8_lehd_benchmark.py
python scripts/qa_figureA8_lehd_benchmark.py
```

Metadata output:

- `intermediate/figureA8_lehd_benchmark_run_metadata.json`

Metadata includes:

- exact source URLs
- SHA-256 hashes of downloaded artifacts
- retained quarter window
- benchmark definition and applied filters
- explicit direct-use assertion (published J2JR rate only)

## Limitation statement

This figure uses published aggregate LEHD rates as a benchmark and should not
be interpreted as public linked microdata suitable for occupation-level causal
transition identification.

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

