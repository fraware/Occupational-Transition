# T-013 — Figure A3 displacement, tenure, and mobility validation (CPS supplement)

## Purpose

`figures/figureA3_cps_supp_validation.csv` validates the worker-transition story in Figure 2 using direct CPS supplement measures of displacement, job tenure at survey date, and occupational mobility from the CPS Displaced Worker / Employee Tenure / Occupational Mobility supplement (January 2024).

## Official data sources

- CPS Displaced Worker / Employee Tenure / Occupational Mobility supplement public-use CSV:
  - `https://www2.census.gov/programs-surveys/cps/datasets/2024/supp/jan24pub.csv`
- CPS Displaced Worker / Employee Tenure / Occupational Mobility supplement technical documentation (record layout, variable scaling, universes, and recodes):
  - `https://www2.census.gov/programs-surveys/cps/techdocs/cpsjan24.pdf`
- Frozen occupation mapping (22 broad occupation groups):
  - `crosswalks/occ22_crosswalk.csv`
- Frozen AI terciles:
  - `intermediate/ai_relevance_terciles.csv`

## Mapping and grouping

- `ai_relevance_tercile` is assigned by:
  1. Using `PRDTOCC1` (detailed occupation recode - job 1) from the January supplement public-use file.
  2. Mapping `PRDTOCC1` to `occ22_id` via `crosswalks/occ22_crosswalk.csv` (`source_system == CPS_PRDTOCC1`).
  3. Joining `occ22_id` to `ai_relevance_tercile` via `intermediate/ai_relevance_terciles.csv`.
- Implementation detail: `PRDTOCC1` is filtered to `1..22` to match the 22-group mapping (code 23 in the crosswalk corresponds to military-specific and has no `occ22_id`).

## Outcomes and computation (weighted)

For each AI tercile `t`, the script computes weighted means/shares using supplement-specific weights from `cpsjan24.pdf`.

### Displacement incidence

- Outcome: `displaced_worker_incidence`
- Variable: `PRDISPWK` (displaced worker indicator recode)
- Valid codes: `{0, 1}` (kept; other values dropped)
- Weight: `PWSUPWGT` scaled by dividing by `10,000` (4 implied decimals in the public-use file)

Computation:

`displaced_worker_incidence(t) = sum(w_disp * I[PRDISPWK==1]) / sum(w_disp)`

### Current job tenure (years)

- Outcome: `mean_current_job_tenure_years`
- Variable: `PTST1TN` (employer tenure recode, expressed in years with two implied decimals)
- Scaling: divide by `100` to express years
- Valid raw range: inclusive `[0, 3100]` (negative special codes dropped; topcoded values retained after range check)
- Weight: `PWTENWGT` scaled by dividing by `10,000`

Computation:

`mean_current_job_tenure_years(t) = sum(w_ten * (PTST1TN/100)) / sum(w_ten)`

### Occupational mobility share

- Outcome: `occupational_mobility_share`
- Variable: `PEST20` (same kind of work a year ago, January 2023)
- Valid codes: `{1, 2}` (kept; other values dropped)
- Mobility definition: `PEST20 == 2` corresponds to “No” (not the same kind of work a year ago)
- Weight: `PWTENWGT` scaled by dividing by `10,000`

Computation:

`occupational_mobility_share(t) = sum(w_ten * I[PEST20==2]) / sum(w_ten)`

## Output schema

Columns in `figures/figureA3_cps_supp_validation.csv`:

- `ai_relevance_tercile` (`low`, `middle`, `high`)
- `displaced_worker_incidence`
- `mean_current_job_tenure_years`
- `occupational_mobility_share`
- `sum_displaced_worker_person_weight` (denominator weight for displacement)
- `sum_job_tenure_person_weight` (denominator weight for tenure and mobility)

Rows are ordered strictly as: `low`, then `middle`, then `high`.

## Implementation and reproducibility

The build streams `jan24pub.csv` row-by-row into deterministic running totals (low-memory approach) and writes a run metadata JSON with:
- source URLs and SHA-256 hashes,
- hashes for the frozen mapping files,
- the exact scaling rules used for `PWSUPWGT`, `PWTENWGT`, and `PTST1TN`.

Run from the repository root:

```bash
python scripts/build_figureA3_cps_supp_validation.py
python scripts/qa_figureA3_cps_supp_validation.py
```

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

