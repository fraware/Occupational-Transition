# Figure 1 memo — Occupational baseline and task heatmap

## Question

What are the national size and wage levels of the paper's broad occupation groups, and how do selected O*NET task dimensions vary across them?

## Datasets

- BLS Occupational Employment and Wage Statistics (OEWS), national occupation detail, for employment and median wage inputs.
- O*NET Work Activities (Importance scale) for task scores at the SOC level, aggregated to 22 groups.
- Frozen crosswalk `crosswalks/occ22_crosswalk.csv`.

## Construction

T-001 maps detailed OEWS occupations to `occ22_id`, sums employment, computes shares, and attaches median annual wage. T-002 aggregates O*NET work-activity scores using OEWS employment weights within groups, z-scores six elements, and forms the AI Task Index as the mean of four digital-information-related z-scores. Terciles are deterministic ranks on that index. See `docs/t001_figure1_panelA_methodology.md` and `docs/t002_figure1_panelB_methodology.md`. Lineage is recorded in `intermediate/figure1_panelA_run_metadata.json` and `intermediate/figure1_panelB_run_metadata.json`.

## Main takeaway

The paper's occupation groups vary widely in size and wage level. Task-intensity profiles also differ systematically, supporting a transparent AI-relevance ordering for downstream analysis.

## How to read quickly

- Start with Panel A to identify large employment-share groups and their wage levels.
- Move to Panel B to compare each group’s standardized task profile against the overall mean.
- Use the AI Task Index column as the deterministic ranking backbone for tercile assignment.
- Treat the figure as a baseline structure map for later worker- and firm-side panels.

## What the figure does not identify

- Causal impacts of AI adoption on employment, wages, or task change.
- Worker-level or establishment-level variation within each aggregated occupation group.
- Geographic composition differences (the figure is national; local composition appears in appendix Figure A9).

## Possible reviewer objections

- **Index construction:** The AI Task Index uses a fixed subset of O*NET elements; robustness checks compare alternative weightings and rank stability (`scripts/robustness/`).
- **OEWS vintage:** National file year follows the build’s pinned or “most recent available” rule; cite run metadata for the exact file.
