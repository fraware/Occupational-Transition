# T-014 — Figure A4 ABS structural heterogeneity (technology adoption and workforce impact)

## Purpose

`figures/figureA4_abs_structural_adoption.csv` provides national structural heterogeneity cuts from official Census ABS technology tables, using only published percentages for:
- AI adoption (`Artificial Intelligence: Total use`)
- AI workforce impact (`Increased`, `Decreased`, `Did not change` number of workers employed)

The figure keeps only industry and firm-size groupings (no state/local rows).

## Official data sources

- ABS data hub:
  - `https://www.census.gov/programs-surveys/abs/data.html`
- ABS tables hub:
  - `https://www.census.gov/programs-surveys/abs/data/tables.html`
- ABS technology module page (most recent available technology module with workforce-impact content):
  - `https://www.census.gov/data/tables/2019/econ/abs/2019-abs-automation-technology-module.html`
- ABS API dataset used for extraction:
  - `https://api.census.gov/data/2018/abstcb`

## Retained module/year and geography

- ABS technology module retained: `ABSTCB2018` (2019 ABS technology release covering reference year 2018)
- `abs_reference_year` in output is `2018`
- Geography filter is national only (`for=us:*`)

## Grouping and filtering rules

National totals and demographic totals are enforced using:
- `SEX=001`
- `ETH_GROUP=001`
- `RACE_GROUP=00`
- `VET_GROUP=001`

Structural cuts are built from published tables only:
- Industry cut: `NAICS2017` 2-digit codes, `NSFSZFI=001` (`All firms`)
- Firm-size cut: `NAICS2017=00` (`All sectors`), `NSFSZFI != 001`

No state or sub-state rows are retained.

## Measures extracted

`measure_key` and `measure_label` mapping:
- `ai_total_use` -> `Artificial Intelligence: Total use`
- `ai_workforce_increased` -> `Artificial Intelligence: Increased number of workers employed by this business`
- `ai_workforce_decreased` -> `Artificial Intelligence: Decreased number of workers employed by this business`
- `ai_workforce_unchanged` -> `Artificial Intelligence: Did not change number of workers employed by this business`

All values are taken from `FIRMPDEMP_PCT` (published percent of employer firms).

## Scale and transformation

- Source scale: percent (`FIRMPDEMP_PCT`)
- Output scale: share in `[0,1]`
- Transformation: `weighted_share = FIRMPDEMP_PCT / 100.0`

No incompatible recomputation is used.

## Output contract

Columns in `figures/figureA4_abs_structural_adoption.csv`:
- `abs_reference_year`
- `industry_code`
- `industry_label`
- `firm_size_class`
- `measure_key`
- `measure_label`
- `weighted_share`
- `source_table_id`

Uniqueness key:
- `abs_reference_year, industry_code, firm_size_class, measure_key`

## Reproducibility

Run from repository root:

```bash
python scripts/build_figureA4_abs_structural_adoption.py
python scripts/qa_figureA4_abs_structural_adoption.py
```

The build writes:
- `figures/figureA4_abs_structural_adoption.csv`
- `intermediate/figureA4_abs_structural_adoption_run_metadata.json`
- cached API response: `raw/abs/abstcb_2018_us_national.json`

Run metadata records:
- exact source URLs
- selected module/year
- transformation and measure dictionary
- SHA-256 hashes for downloaded artifacts

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

