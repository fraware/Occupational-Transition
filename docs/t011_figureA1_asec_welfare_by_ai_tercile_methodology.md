# T-011 — Figure A1 annual welfare and income context (CPS ASEC)

## Purpose

`figures/figureA1_asec_welfare_by_ai_tercile.csv` summarizes national, annual person-level outcomes from the Census Current Population Survey (CPS) Annual Social and Economic Supplement (ASEC), grouped by AI relevance terciles defined on the 22 broad occupation groups (`occ22`).

## Data sources (official public use only)

- CPS ASEC March public-use CSV bundles `asecpubYYcsv.zip` from `https://www2.census.gov/programs-surveys/cps/datasets/<year>/march/` (see `docs/data_registry.csv` for landing pages, guidance, and footnotes).
- Person file `pppubYY.csv` inside each bundle (exact path within the ZIP may include a prefix directory in some years).
- Variable definitions follow the Census-published person record layout (`persfmt.txt`) and data dictionary PDF for the corresponding March release.

## Mapping lineage (frozen project artifacts)

- Occupation: `A_DTOCC` (major occupation group, codes 1–22) is mapped to `occ22_id` using `source_system == CPS_PRDTOCC1` rows in `crosswalks/occ22_crosswalk.csv`.
- AI terciles: `occ22_id` joins to `ai_relevance_tercile` in `intermediate/ai_relevance_terciles.csv` (from T-002).

Persons with `A_DTOCC` 0 (not in universe or unknown) or 23 (armed forces) are excluded from all aggregates.

## Weighting

- Person weight variable: `A_FNLWGT` on the ASEC person record.
- Scaling: `A_FNLWGT` is stored with two implied decimal places; the build divides by 100 to obtain person weights for totals and ratios. The exact rule is recorded in `intermediate/figureA1_asec_welfare_by_ai_tercile_run_metadata.json`.

## Outcome definitions

| Output column | Construction |
|---------------|--------------|
| `mean_annual_income` | Weighted mean of `PTOTVAL`, with negative values truncated to 0 before averaging. |
| `poverty_rate` | Weighted mean of `SPM_POOR` (Supplemental Poverty Measure poor flag, 0/1 on the person record). |
| `mean_weeks_worked` | Weighted mean of `WKSWORK` (weeks worked last year, 0–52). |
| `unemployment_incidence` | Among persons with `PEMLR` in {1,2,3,4} (civilian labor force), the share with `PEMLR` in {3,4} (unemployed), both weighted by person weight. |
| `sum_asec_person_weight` | Sum of scaled person weights in the `A_DTOCC` 1–22 universe for that year and tercile. |

## Geography and window

- Geography: national (CPS ASEC is designed for national and selected subnational use; this output does not apply a subnational filter).
- Time window: 2019 through the most recent March ASEC CSV bundle available on Census servers at build time (see metadata `retained_years`).

## Reproducibility

Run from the repository root:

```bash
python scripts/build_figureA1_asec_welfare_by_ai_tercile.py
python scripts/qa_figureA1_asec_welfare_by_ai_tercile.py
```

The build caches each `asecpubYYcsv.zip` under `raw/cps/asec/` and writes SHA-256 hashes and URLs to `intermediate/figureA1_asec_welfare_by_ai_tercile_run_metadata.json`.

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

