# Figure 2 — Data sources and provenance

## Primary sources

- **CPS Basic Monthly Public Use Files:** Census/BLS CPS microdata; see `docs/data_registry.csv` for monthly CPS file URLs and `docs/methodology/tickets/t003_figure2_panelA_methodology.md`, `docs/methodology/tickets/t004_figure2_panelB_counts_methodology.md`, `docs/methodology/tickets/t005_figure2_panelB_probs_methodology.md`.
- **AI-relevance terciles:** `intermediate/ai_relevance_terciles.csv` from T-002.

## Run metadata

- `intermediate/figure2_panelA_run_metadata.json`
- `intermediate/figure2_panelB_counts_run_metadata.json`
- `intermediate/figure2_panelB_probs_run_metadata.json`

## Provenance pointers

- **Figure CSV outputs:** `figures/figure2_panelA_hours_by_ai_tercile.csv`, `figures/figure2_panelB_transition_counts.csv`, `figures/figure2_panelB_transition_probs.csv`
- **Methodology docs:** `docs/methodology/tickets/t003_figure2_panelA_methodology.md`, `docs/methodology/tickets/t004_figure2_panelB_counts_methodology.md`, `docs/methodology/tickets/t005_figure2_panelB_probs_methodology.md`
- **Tercile mapping input:** `intermediate/ai_relevance_terciles.csv`

## Reproducibility hashes (SHA256)

- `figures/figure2_panelA_hours_by_ai_tercile.csv` — `a6ad843f745726659242bd71c6234ac0a5487878be01d00e4794d6af3414bb78`
- `figures/figure2_panelB_transition_counts.csv` — `b80cc59cb1b116e51ebf0c732776ee90f521cf9bb63a03e72440ba6f06255efc`
- `figures/figure2_panelB_transition_probs.csv` — `e717ba341276a3b9e004f20e168a24527790d81c24fb5eef9db874a8191d67a1`
- `intermediate/ai_relevance_terciles.csv` — `ed51a3d2884c246a6229a2a1c79a49ad7551b700047eae5a4dff7cac5754433b`
- `intermediate/figure2_panelA_run_metadata.json` — `93b6515be95ba5a485464135af79e7ecb84a92b34b92a082459197efdadf9e8b`
- `intermediate/figure2_panelB_counts_run_metadata.json` — `7b2bafcd2b8b257e093dd8e450487ec2004dfe834105ba4632a1c1af19f066c2`
- `intermediate/figure2_panelB_probs_run_metadata.json` — `d4fd6beda35cc4bed9dc56865b2bd62575123c10c0e86ba26570b5ff3b44ffa2`

## Limitations

- Transitions are inferred from matched adjacent months at broad occupation and labor-force states; they are not administrative job-to-job records.
- Results are national; subnational cells are not claimed in the main specification.

## Presentation note

The redesigned Figure 2 preserves the frozen Figure 2 CSV inputs. Panel B’s summary metrics are aggregated from the frozen transition-probabilities layer using the paper’s fixed low-, middle-, and high-AI-relevance occupation grouping. The separate support visual stem **`transition_coarse_matrix_latest`** presents the **latest month** coarse-state transition matrix as **row-normalized probabilities** (from `figure2_panelB_transition_probs.csv`), after grouping occupation origins and destinations into low, middle, high, unemployed, and NILF—not a weighted-count heatmap.
