# T-020 — Figure A10 NLS long-run career adaptation

## Purpose

`figures/figureA10_nls_longrun.csv` provides national long-run worker
adaptation context by following weighted outcomes across NLSY97 interview rounds,
stratified by each respondent's baseline AI-relevance tercile.

This appendix figure is interpretive context and does not replace the paper's
main empirical spine.

## Official data sources

Retained official public-use sources:

- `https://www.bls.gov/nls/getting-started/accessing-data.htm`
- `https://www.bls.gov/nls/notices/2024/nlsy97-data-release-20.htm`
- `https://www.bls.gov/nls/getting-started/nlsy97_all_1997-2019.zip`

Frozen in-repo mappings:

- `crosswalks/occ22_crosswalk.csv`
- `intermediate/ai_relevance_terciles.csv`

## Cohort, rounds, and geography

- Cohort: NLSY97 public-use full extract (`nlsy97_all_1997-2019.zip`)
- Geography: national only (public-use)
- Retained rounds in this build: `1997, 1998, 1999, 2000, 2001, 2002, 2003,
  2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2013, 2015, 2017, 2019`

## Baseline AI-tercile assignment

1. For each respondent, identify earliest retained round with valid
   `YEMP_OCCODE-2002.01`.
2. Map that occupation code into `occ22_id` using
   `crosswalks/occ22_crosswalk.csv`.
3. Map `occ22_id` into `low` / `middle` / `high` using
   `intermediate/ai_relevance_terciles.csv`.
4. Keep this tercile fixed as the respondent baseline tercile for all rounds.

## Weighting

- Round-appropriate public-use weight: `SAMPLING_WEIGHT_CC`
- Implied decimals: 2 (`weight = raw / 100`)
- Aggregation: weighted means by `survey_round × baseline_ai_tercile`

## Outcome construction

For each retained round and baseline tercile:

- `occupation_switch_rate`:
  weighted share with valid current mapped occupation where
  `current_occ22 != baseline_occ22`
- `employment_rate`:
  weighted mean of annual weekly employed share from `EMP_STATUS_{year}.*`
- `unemployment_rate`:
  weighted mean of annual weekly unemployed share from `EMP_STATUS_{year}.*`
- `nilf_rate`:
  weighted mean of annual weekly not-in-labor-force share from
  `EMP_STATUS_{year}.*`
- `mean_annual_earnings`:
  weighted mean of `CV_INCOME_FAMILY` when available, otherwise
  `CV_INCOME_GROSS_YR`
- `training_participation_rate`:
  weighted share with `CV_ENROLLSTAT` in enrolled statuses `8..11`

## Output schema

`figures/figureA10_nls_longrun.csv` columns:

- `survey_round`
- `baseline_ai_tercile`
- `weighted_n`
- `occupation_switch_rate`
- `employment_rate`
- `unemployment_rate`
- `nilf_rate`
- `mean_annual_earnings`
- `training_participation_rate`
- `source_program`
- `source_series_id`

Uniqueness key:

- `survey_round, baseline_ai_tercile`

## Reproducibility and metadata

Run from repository root:

```bash
python scripts/build_figureA10_nls_longrun.py
python scripts/qa_figureA10_nls_longrun.py
```

Metadata:

- `intermediate/figureA10_nls_longrun_run_metadata.json`

Metadata records:

- source URLs and local cache path
- SHA-256 for raw source zip
- crosswalk and tercile lineage hashes
- retained rounds
- weighting and outcome definitions

## Limitation statement

Figure A10 is long-run descriptive context from public NLS data and should not
be interpreted as near-real-time AI-shock evidence or as causal identification
of employer AI adoption effects.

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

