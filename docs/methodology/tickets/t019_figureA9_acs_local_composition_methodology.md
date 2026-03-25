# T-019 — Figure A9 ACS local occupational composition

## Purpose

`figures/figureA9_acs_local_composition.csv` provides a descriptive geographic view of where workers in AI-relevant
occupation groups are concentrated, using ACS PUMS microdata summarized to PUMA geography.

This is an appendix benchmark/structure table: it should not be interpreted as a transition engine or used for causal identification.

## Official data sources

Retained ACS PUMS person microdata (deterministically resolved by the build script; documented run example):

- `https://www2.census.gov/programs-surveys/acs/data/pums/2024/1-Year/csv_pus.zip`
- Zip member read by the build script: `psam_pusa.csv`

Frozen in-repo mappings (shared across figures):

- `crosswalks/occ22_crosswalk.csv` (map ACS occupation codes to the frozen 22-group system)
- `intermediate/ai_relevance_terciles.csv` (map frozen `occ22_id` to `low` / `middle` / `high`)

## Universe, filters, and mapping lineage

### Universe

Person records from the retained ACS PUMS zip that satisfy all filters below.

### Filters applied

The build script applies:

- `PUMA` must be present and numeric, and the code must not be `00000`
- `PWGTP` must be present and strictly positive (ACS person weight)
- `OCCP` must be present and numeric, and must map into one of the frozen 22 occupation groups via
  `census_occ_code_range` intervals in `crosswalks/occ22_crosswalk.csv`
- If the input contains an `ESR` field, keep only `ESR==1` records (employed). If `ESR` is absent, no ESR filter is applied.

### Occupation grouping (ACS -> `occ22_id`)

1. Parse ACS occupation code `OCCP` as an integer.
2. Build a 22-interval index from `crosswalks/occ22_crosswalk.csv` using the `census_occ_code_range` bounds.
3. Assign each `OCCP` to exactly one frozen `occ22_id` by interval membership.

### AI terciles (`occ22_id` -> `low` / `middle` / `high`)

Join each retained `occ22_id` to its AI tercile label from `intermediate/ai_relevance_terciles.csv`.

## Aggregation and formulas

Geography: PUMA.

For each PUMA `p`:

`population_weight_sum[p] = sum(PWGTP) over included person records in p`

For each occupation group `occ22_id = k`:

`occ22_share_k[p] = sum(PWGTP) over included records in p mapped to occ22_id=k / population_weight_sum[p]`

AI tercile shares:

`high_ai_tercile_share[p] = sum(PWGTP) over included records in p mapped to high tercile / population_weight_sum[p]`

and similarly for `middle_ai_tercile_share[p]` and `low_ai_tercile_share[p]`.

`occ22_share_sum_check[p]` is the direct numeric sum of the 22 `occ22_share_k[p]` values for QA.

## Output schema

`figures/figureA9_acs_local_composition.csv` columns:

- `acs_year`
- `puma`
- `population_weight_sum`
- `high_ai_tercile_share`
- `middle_ai_tercile_share`
- `low_ai_tercile_share`
- `occ22_share_sum_check`
- `occ22_share_1` ... `occ22_share_22`

Uniqueness:

- Exactly one row per `puma`.

## Reproducibility and metadata

Run from repository root:

```bash
python scripts/build_figureA9_acs_local_composition.py
python scripts/qa_figureA9_acs_local_composition.py
```

Metadata output:

- `intermediate/figureA9_acs_local_composition_run_metadata.json`

Metadata includes:

- the resolved ACS PUMS zip + member file used for the documented run
- SHA-256 hashes for the ACS zip, the frozen crosswalk, and the AI terciles file
- the exact filters and normalization convention used

## QA and interpretation note

QA enforces:

- PUMA uniqueness (one row per PUMA)
- per-PUMA weighted shares in `[0,1]`
- AI tercile shares summing to 1 within tolerance
- `occ22_share_sum_check` matching the sum of 22 occupation shares

Interpretation:

This figure is descriptive composition context only; it does not model transitions or causal effects.

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

