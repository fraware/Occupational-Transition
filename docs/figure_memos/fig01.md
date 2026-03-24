# Figure 1 memo — Occupational baseline and task heatmap

## Question

What is the national size and wage level of broad occupation groups used in the paper, and how do selected O*NET task dimensions vary across those groups?

## Datasets

- BLS Occupational Employment and Wage Statistics (OEWS), national occupation detail, for employment and median wage inputs.
- O*NET Work Activities (Importance scale) for task scores at the SOC level, aggregated to 22 groups.
- Frozen crosswalk `crosswalks/occ22_crosswalk.csv`.

## Construction

T-001 maps detailed OEWS occupations to `occ22_id`, sums employment, computes shares, and attaches median annual wage. T-002 aggregates O*NET work-activity scores using OEWS employment weights within groups, z-scores six elements, and forms the AI Task Index as the mean of four digital-information-related z-scores; terciles are deterministic ranks on that index. See `docs/t001_figure1_panelA_methodology.md` and `docs/t002_figure1_panelB_methodology.md`; lineage in `intermediate/figure1_panelA_run_metadata.json` and `intermediate/figure1_panelB_run_metadata.json`.

## Main takeaway

The paper’s occupation groups span very different sizes and wage levels, and task intensity profiles differ systematically across groups in a way that supports a transparent AI-relevance ordering for downstream analysis.

## What the figure does not identify

- Realized labor-market impacts of AI adoption.
- Within-group heterogeneity at detailed SOC or establishment level.
- Geographic variation (national OEWS and national aggregation to 22 groups in these panels).

## Possible reviewer objections

- **Index construction:** The AI Task Index uses a fixed subset of O*NET elements; robustness checks compare alternative weightings and rank stability (`scripts/robustness/`).
- **OEWS vintage:** National file year follows the build’s pinned or “most recent available” rule; cite run metadata for the exact file.
