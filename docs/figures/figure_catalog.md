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
- Memo and Virginia stems (`t101`–`t108`, required `va01`–`va06`) are validated by `scripts/run_memo_visuals_qa.py` (including `scripts/qa_virginia_memo_visuals.py`).
- Bounded drift-validation may cover main stems (`t001` to `t010`) first; when used, scope must be explicitly documented in the run evidence.

## Senator note visuals (memo pack)

Precision, formulas, and month-alignment rules for memo KPIs and BTOS state map: `docs/quality/README.md#memo-visuals-t-101-to-t-108-precision-and-non-invention-rules`.

Each stem below also has a matching PDF under `visuals/vector/` with the same filename.

| Memo visual | Figure CSV(s) | Visual stem(s) (`visuals/png`) |
|-------------|----------------|--------------------------------|
| Visual 1 — What we can measure now dashboard | `figures/memo_dashboard_kpis.csv` | `memo_dashboard` |
| Visual 2 — BTOS two-panel trend/composition | `figures/figure3_panelA_btos_ai_trends.csv`, `figures/figure3_panelB_btos_workforce_effects.csv` | `memo_btos_two_panel` |
| Visual 3 — CPS transition flow map | `figures/memo_cps_transition_flows.csv` | `memo_cps_sankey` |
| Visual 4 — Occupation bubble scatter | `figures/memo_occ_bubble_scatter.csv` | `memo_occ_bubble_scatter` |
| Visual 5 — BTOS state choropleth | `figures/memo_btos_state_ai_use_latest.csv` | `memo_btos_state_choropleth` |
| Visual 6 — Resolution boundary ladder | `figures/memo_resolution_ladder.csv` | `memo_resolution_ladder` |
| Visual 7 — Memo capability matrix | `figures/figure5_capability_matrix.csv` | `memo_capability_matrix` |
| Visual 8 — Policy roadmap | `figures/memo_policy_roadmap.csv` | `memo_policy_roadmap` |

## Virginia memo pack (additive)

| Virginia visual | Figure CSV(s) | Visual stem(s) (`visuals/png` and `visuals/vector`) |
|-----------------|----------------|--------------------------------|
| VA 1 — Six-sector composition | `figures/state_deep_dive_qcew_51_profile.csv` | `virginia_sector_composition` |
| VA 2 — Six-sector wages | `figures/state_deep_dive_qcew_51_profile.csv` | `virginia_sector_wages` |
| VA 3 — Peer shares comparison | `figures/state_deep_dive_qcew_51_peers.csv` | `virginia_peers_sector_shares` |
| VA 4 — Peer wages comparison | `figures/state_deep_dive_qcew_51_peers.csv` | `virginia_peers_sector_wages` |
| VA 5 — State rank profile | `figures/state_deep_dive_qcew_51_ranks.csv` | `virginia_sector_ranks` |
| VA 6 — Virginia KPI dashboard | `figures/virginia_memo_kpis.csv` | `virginia_kpi_dashboard` |
| VA 7 — BTOS state highlight (optional) | `figures/memo_btos_state_ai_use_latest.csv` | `virginia_btos_state_highlight` |
| VA 8 — Occupation context (optional) | `figures/memo_occ_bubble_scatter.csv` | `virginia_occ_context` |

**Build and QA (Virginia tables and stems):** `scripts/build_state_qcew_deep_dive.py`, `scripts/qa_state_qcew_deep_dive.py`, `scripts/build_virginia_memo_kpis.py`, `scripts/visualize_virginia_memo.py`, `scripts/qa_virginia_memo_visuals.py`. These are also invoked at the end of `scripts/run_memo_visuals_build.py` and `scripts/run_memo_visuals_qa.py`.

**Memo orchestrator:** full memo + Virginia pack — `python scripts/run_memo_visuals_build.py` then `python scripts/run_memo_visuals_qa.py` (see `docs/replication/README.md`).

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

Generate the packaging manifest (Main, Appendix, Memo, Virginia, and AWES/ALPI monitoring visuals):

`python scripts/build_visual_packaging_manifest.py`

Output:

`docs/figures/visual_packaging_manifest.md`
