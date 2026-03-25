# Committed outputs vs build-generated

This inventory aligns [README.md](../README.md) and [acceptance_matrix.md](acceptance_matrix.md) with what is **tracked in git** versus produced locally by the pipeline.

## Tracked in git

- **Crosswalks and registry:** `crosswalks/*.csv`, `docs/data_registry.csv`
- **Figures (CSV):** All paths under `figures/*.csv` listed by `git ls-files figures`. This includes main-text, appendix, memo, and Virginia KPI tables that are checked in as frozen outputs.
- **Metrics:** `metrics/awes_occ22_monthly.csv`, `metrics/alpi_occ22_monthly.csv`
- **Visuals:** `visuals/png/*.png`, `visuals/vector/*.pdf`

## Build-generated (not committed; typical paths)

These are required for a full strict rebuild but are **gitignored** or otherwise not versioned:

| Output | Typical path | When it appears |
|--------|----------------|-----------------|
| T-004 transition counts | `figures/figure2_panelB_transition_counts.csv` | After `build_figure2_panelB_counts.py` (feeds T-005 and downstream memo KPIs) |
| AI relevance terciles | `intermediate/ai_relevance_terciles.csv` | After T-002 build |
| Run metadata | `intermediate/*run_metadata.json` | Per-ticket build scripts |
| Acceptance logs | `intermediate/full_clean_rebuild_acceptance_*.md` | After `run_full_clean_rebuild_acceptance.py` or full pipeline |
| Visual manifest | `intermediate/visuals_run_manifest.json` | After `run_visuals_all.py` |

Replicators should run the commands in [replication.md](replication.md) to generate these artifacts; the committed `figures/` set is the **published snapshot** for the paper and policy tables that are checked in.

## Note on T-004

`figures/figure2_panelB_transition_counts.csv` is listed in the acceptance matrix and README ticket table but is **not** a committed file in the default snapshot: it is produced by the CPS pipeline and consumed on disk by `build_figure2_panelB_probs.py` and memo scripts. Obtain it by running T-004 build (see [t004_figure2_panelB_counts_methodology.md](t004_figure2_panelB_counts_methodology.md)).
