# Figure catalog (main text)

Stable slugs map paper figures to pipeline outputs and visual stems (`docs/quality/README.md#visual-style-guide`).

| Paper figure | Panels / charts | Figure CSV(s) | Visual stem(s) (`visuals/png`) |
|--------------|-----------------|---------------|--------------------------------|
| Figure 1 | Occupational baseline (Panel A); O*NET task heatmap and AI terciles (Panel B) | `figures/figure1_panelA_occ_baseline.csv`, `figures/figure1_panelB_task_heatmap.csv`, `intermediate/ai_relevance_terciles.csv` | `occupation_share_barh`, `task_heatmap` |
| Figure 2 | Hours by AI tercile (Panel A); transition counts heatmap and summary metrics (Panel B) | `figures/figure2_panelA_hours_by_ai_tercile.csv`, `figures/figure2_panelB_transition_counts.csv`, `figures/figure2_panelB_transition_probs.csv` | `hours_timeseries`, `transition_counts_heatmap_latest`, `transition_summary_metrics` |
| Figure 3 | BTOS AI-use trends (Panel A); supplement workforce effects (Panel B) | `figures/figure3_panelA_btos_ai_trends.csv`, `figures/figure3_panelB_btos_workforce_effects.csv` | `btos_ai_trends`, `btos_workforce_effects_barh` |
| Figure 4 | JOLTS sector rates (Panel A); CES payroll index (Panel B) | `figures/figure4_panelA_jolts_sector_rates.csv`, `figures/figure4_panelB_ces_sector_index.csv` | `jolts_openings_rate`, `ces_payroll_index` |
| Figure 5 | Capability matrix | `figures/figure5_capability_matrix.csv` | `capability_matrix_heatmap` |

## Caption and source note files

| Paper figure | Caption | Source note |
|--------------|---------|-------------|
| Figure 1 | `docs/figures/captions/fig01_caption.md` | `docs/figures/source_notes/fig01_sources.md` |
| Figure 2 | `docs/figures/captions/fig02_caption.md` | `docs/figures/source_notes/fig02_sources.md` |
| Figure 3 | `docs/figures/captions/fig03_caption.md` | `docs/figures/source_notes/fig03_sources.md` |
| Figure 4 | `docs/figures/captions/fig04_caption.md` | `docs/figures/source_notes/fig04_sources.md` |
| Figure 5 | `docs/figures/captions/fig05_caption.md` | `docs/figures/source_notes/fig05_sources.md` |

## Style lock

- Shared style: `scripts/viz_style.py`, `docs/quality/README.md#visual-style-guide`.
- Do not change palette, font, or axis formats for a single figure without updating the style guide and regenerating all visuals.

## Validation coverage

- Full visual validation covers main and appendix stems (`t001` to `t020`) via `scripts/qa_visuals.py`.
- Bounded drift-validation may cover main stems (`t001` to `t010`) first; when used, scope must be explicitly documented in the run evidence.

## Monitoring metric visuals (AWES/ALPI)

These are additive descriptive monitoring visuals derived from `metrics/` outputs, not main-paper figures.

| Monitoring visual | Metric CSV(s) | Visual stem(s) (`visuals/png` and `visuals/vector`) |
|-------------------|---------------|--------------------------------|
| AWES top occupations (latest month) | `metrics/awes_occ22_monthly.csv` | `awes_top20_latest` |
| ALPI top occupations (latest month) | `metrics/alpi_occ22_monthly.csv` | `alpi_top20_latest` |
| AWES/ALPI monthly median trend | `metrics/awes_occ22_monthly.csv`, `metrics/alpi_occ22_monthly.csv` | `awes_alpi_monthly_median` |
| AWES vs ALPI cross-section (latest month) | `metrics/awes_occ22_monthly.csv`, `metrics/alpi_occ22_monthly.csv` | `awes_vs_alpi_latest_scatter` |

Build: `python scripts/visualize_awes_alpi.py`  
QA: `python scripts/qa_awes_alpi_visuals.py`

## Publication packaging manifest

Generate the packaging manifest (Main, Appendix, and AWES/ALPI monitoring visuals):

`python scripts/build_visual_packaging_manifest.py`

Output:

`docs/figures/visual_packaging_manifest.md`
