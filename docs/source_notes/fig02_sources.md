# Figure 2 — Data sources and provenance

## Primary sources

- **CPS Basic Monthly Public Use Files:** Census/BLS CPS microdata; see `docs/data_registry.csv` for monthly CPS file URLs and `docs/t003_figure2_panelA_methodology.md`, `docs/t004_figure2_panelB_counts_methodology.md`, `docs/t005_figure2_panelB_probs_methodology.md`.
- **AI-relevance terciles:** `intermediate/ai_relevance_terciles.csv` from T-002.

## Run metadata

- `intermediate/figure2_panelA_run_metadata.json`
- `intermediate/figure2_panelB_counts_run_metadata.json`
- `intermediate/figure2_panelB_probs_run_metadata.json`

## Provenance pointers

- **Figure CSV outputs:** `figures/figure2_panelA_hours_by_ai_tercile.csv`, `figures/figure2_panelB_transition_counts.csv`, `figures/figure2_panelB_transition_probs.csv`
- **Methodology docs:** `docs/t003_figure2_panelA_methodology.md`, `docs/t004_figure2_panelB_counts_methodology.md`, `docs/t005_figure2_panelB_probs_methodology.md`
- **Tercile mapping input:** `intermediate/ai_relevance_terciles.csv`

## Limitations

- Transitions are inferred from matched adjacent months at broad occupation and labor-force states; they are not administrative job-to-job records.
- Results are national; subnational cells are not claimed in the main specification.
