# Figure catalog (main text)

Stable slugs map paper figures to pipeline outputs and visual stems (`docs/visual_style_guide.md`).

| Paper figure | Panels / charts | Figure CSV(s) | Visual stem(s) (`visuals/png`) |
|--------------|-----------------|---------------|--------------------------------|
| Figure 1 | Occupational baseline (Panel A); O*NET task heatmap and AI terciles (Panel B) | `figures/figure1_panelA_occ_baseline.csv`, `figures/figure1_panelB_task_heatmap.csv`, `intermediate/ai_relevance_terciles.csv` | `t001_occupation_share_barh`, `t002_task_heatmap` |
| Figure 2 | Hours by AI tercile (Panel A); transition counts heatmap and summary metrics (Panel B) | `figures/figure2_panelA_hours_by_ai_tercile.csv`, `figures/figure2_panelB_transition_counts.csv`, `figures/figure2_panelB_transition_probs.csv` | `t003_hours_timeseries`, `t004_transition_counts_heatmap_latest`, `t005_transition_summary_metrics` |
| Figure 3 | BTOS AI-use trends (Panel A); supplement workforce effects (Panel B) | `figures/figure3_panelA_btos_ai_trends.csv`, `figures/figure3_panelB_btos_workforce_effects.csv` | `t006_btos_ai_trends`, `t007_btos_workforce_effects_barh` |
| Figure 4 | JOLTS sector rates (Panel A); CES payroll index (Panel B) | `figures/figure4_panelA_jolts_sector_rates.csv`, `figures/figure4_panelB_ces_sector_index.csv` | `t008_jolts_openings_rate`, `t009_ces_payroll_index` |
| Figure 5 | Capability matrix | `figures/figure5_capability_matrix.csv` | `t010_capability_matrix_heatmap` |

## Caption and source note files

| Paper figure | Caption | Source note |
|--------------|---------|-------------|
| Figure 1 | `docs/captions/fig01_caption.md` | `docs/source_notes/fig01_sources.md` |
| Figure 2 | `docs/captions/fig02_caption.md` | `docs/source_notes/fig02_sources.md` |
| Figure 3 | `docs/captions/fig03_caption.md` | `docs/source_notes/fig03_sources.md` |
| Figure 4 | `docs/captions/fig04_caption.md` | `docs/source_notes/fig04_sources.md` |
| Figure 5 | `docs/captions/fig05_caption.md` | `docs/source_notes/fig05_sources.md` |

## Style lock

- Shared style: `scripts/viz_style.py`, `docs/visual_style_guide.md`.
- Do not change palette, font, or axis formats for a single figure without updating the style guide and regenerating all visuals.
