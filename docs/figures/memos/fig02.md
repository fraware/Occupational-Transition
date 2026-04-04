# Figure 2 memo — Hours and transitions (CPS)

## Question

How do usual weekly hours and broad labor-force and occupational transition patterns differ across AI-relevance terciles in recent CPS data?

## Datasets

- CPS Basic Monthly microdata (public-use files), matched adjacent months for transitions.
- `intermediate/ai_relevance_terciles.csv` from T-002 for occupation-to-tercile mapping.

## Construction

T-003 restricts to the employed civilian noninstitutional population with valid hours and occupation, uses composite person weights, and averages usual weekly hours by month and tercile. T-004 constructs origin and destination states in a 22-occupation plus unemployment plus NILF space. T-005 row-normalizes counts to probabilities and emits summary transition metrics. See `docs/methodology/tickets/t003_*` through `docs/methodology/tickets/t005_*`. Metadata JSONs are under `intermediate/figure2_*`.

## Main takeaway

The figure documents worker-side descriptive patterns at national scale: hours levels by tercile and broad transition flows over time. It supports monitoring, not causal attribution to AI.

## How to read quickly

- Read Panel A first to compare level differences in usual weekly hours across terciles.
- Use the latest-month heatmap in Panel B to see where gross transition mass is concentrated.
- Then read the summary probability lines to track retention, switching, unemployment entry, and NILF entry over time.
- Interpret the full panel as descriptive labor-market movement, not identification of AI treatment effects.

## What the figure does not identify

- Which specific employers adopted AI or whether adoption caused observed transition patterns.
- Worker-firm linkage needed to attribute transitions to adopting establishments.
- Causal effects of AI exposure on hours, retention, or labor-force entry/exit outcomes.

## Possible reviewer objections

- **Match rates:** Review build logs and methodology for months with missing CPS files or sparse matches.
- **Transition definitions:** States are coarse (22 groups plus unemployment/NILF); fine occupation moves within a group appear as retention.

## Redesign objective

Figure 2 should be the paper’s worker-side signal figure.

The visual priority is to make two things legible immediately:

1. the hours gradient across frozen AI-relevance terciles is persistent and economically meaningful;
2. broad worker-side movement differs across the same grouping, but only at a coarse descriptive level.

Implementation rule:

- Preserve the frozen Figure 2 CSVs.
- Keep Panel A visually simple and directly labeled.
- Replace an over-dense movement presentation with a compact transition-summary view.
- Maintain a separate support heatmap output for the latest coarse-state transition structure.
- Run `python scripts/visualize_figure2.py` before visual QA; `scripts/qa_visuals.py` expects PNG+PDF for `hours_timeseries`, `transition_counts_heatmap_latest`, `transition_summary_metrics`, and manuscript stem `figure2_redesigned_composite` (see `docs/figures/figure_catalog.md`).
- For Panel B aggregation and the coarse heatmap, `scripts/visualize_figure2.py` maps `occ22_*` origins to terciles using `intermediate/ai_relevance_terciles.csv` when that file exists locally; if not, it uses the same frozen occ22-to-tercile assignment as Technical Note 1 (embedded fallback in the script).
