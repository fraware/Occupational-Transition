# Figure 2 memo — Hours and transitions (CPS)

## Question

How do usual weekly hours and broad labor-force and occupational transition patterns differ across AI-relevance terciles in recent monthly CPS data?

## Datasets

- CPS Basic Monthly microdata (public-use files), matched adjacent months for transitions.
- `intermediate/ai_relevance_terciles.csv` from T-002 for occupation-to-tercile mapping.

## Construction

T-003 restricts to the employed civilian noninstitutional population with valid hours and occupation, uses composite person weights, and averages usual weekly hours by month and tercile. T-004 constructs origin and destination states in a 22-occupation plus unemployment plus NILF space; T-005 row-normalizes counts to probabilities and emits summary transition metrics. See `docs/t003_*` through `docs/t005_*`; metadata JSONs under `intermediate/figure2_*`.

## Main takeaway

The figure documents descriptive worker-side patterns at national scale: hours levels by tercile and broad transition flows over time, suitable for monitoring rather than causal attribution to AI.

## What the figure does not identify

- Which employers adopted AI or caused specific transitions.
- Subnational or detailed-occupation stable estimates without additional pooling.
- Causal effects of AI exposure on hours or transitions.

## Possible reviewer objections

- **Match rates:** Review build logs and methodology for months with missing CPS files or sparse matches.
- **Transition definitions:** States are coarse (22 groups plus unemployment/NILF); fine occupation moves within a group appear as retention.
