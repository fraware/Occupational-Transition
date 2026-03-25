# Visual Style Guide

This guide defines deterministic publication-ready static rendering for figure outputs (`T-001` to `T-020`).

## Scope
- Input data: `figures/*.csv` only.
- Output artifacts:
  - `visuals/png/*.png`
  - `visuals/vector/*.pdf`
- No data transformations beyond figure-level CSV content.

## Global Style Defaults
- Engine: Matplotlib static rendering.
- Background: white.
- Grid: light dashed grid.
- Font family: DejaVu Sans.
- Export DPI: 220.
- Default line width: 2.0.
- Default marker size: 5.0.

## Semantic Color Mapping
- AI terciles:
  - low: `#2ca02c`
  - middle: `#ff7f0e`
  - high: `#1f77b4`
- Neutral reference lines: `#4d4d4d`.
- Sector sequences: fixed 6-color palette in `scripts/viz_style.py`.

## Naming Conventions
- Paper and appendix stems: `tNNN_<chart_slug>` for `T-001`–`T-020`.
- Senator memo pack (additive): stems `t101_memo_dashboard` through `t108_memo_policy_roadmap` (see `docs/figure_catalog.md`).
- Virginia brief pack (additive): stems `va01_virginia_sector_composition` through `va08_virginia_occ_context` (see `docs/figure_catalog.md`).
- Each stem must generate both:
  - `visuals/png/<stem>.png`
  - `visuals/vector/<stem>.pdf`

## Chart Grammar by Family
- Time series: line chart with consistent axis format and reference baseline when applicable.
- Matrix transitions: heatmap with fixed color scale and explicit labels.
- Composition/benchmark distributions: sorted bars or horizontal bars.
- Capability matrices: categorical heatmap with direct/partial/none legend.

## Style lock (sign-off)

After editorial sign-off, treat `scripts/viz_style.py` as frozen for this paper version: do not change fonts, palette hex values, DPI, or axis date formats for individual figures in isolation. Any global adjustment requires updating this guide, regenerating all stems under `visuals/png/` and `visuals/vector/`, and recording a new acceptance run.

Figure-to-stem mapping and caption paths: `docs/figure_catalog.md`.

## Reproducibility and QA
- Render commands (paper `t001`–`t020`):
  - `python scripts/run_visuals_all.py`
- Visual QA (paper `t001`–`t020`):
  - `python scripts/qa_visuals.py`
- Memo + Virginia stems (`t101`–`t108`, `va01`–`va06` required in Virginia QA):
  - `python scripts/run_memo_visuals_build.py`
  - `python scripts/run_memo_visuals_qa.py`
- Caption and source-note file coverage (main text):
  - `python scripts/qa_visual_caption_coverage.py`
- QA verifies:
  - expected files exist
  - non-zero file size
  - PNG readability
  - deterministic naming
- QA writes:
  - `intermediate/visuals_run_manifest.json`

