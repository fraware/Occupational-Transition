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
