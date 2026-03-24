# Figure 3 — Data sources and provenance

## Primary sources

- **BTOS API (national stratum):** Census BTOS public API; published firm-weighted shares. See `docs/t006_figure3_panelA_btos_ai_trends_methodology.md`.
- **BTOS AI Supplement Table (XLSX):** Census-published workbook for workforce-effect shares. See `docs/t007_figure3_panelB_btos_workforce_effects_methodology.md` and `README.md` (Known Deviations) for task-category mapping notes.

## Run metadata

- `intermediate/figure3_panelA_btos_ai_trends_run_metadata.json`
- `intermediate/figure3_panelB_btos_workforce_effects_run_metadata.json`

## Provenance pointers

- **Figure CSV outputs:** `figures/figure3_panelA_btos_ai_trends.csv`, `figures/figure3_panelB_btos_workforce_effects.csv`
- **Methodology docs:** `docs/t006_figure3_panelA_btos_ai_trends_methodology.md`, `docs/t007_figure3_panelB_btos_workforce_effects_methodology.md`
- **Interpretation guardrail:** when item-25 option rows are absent in the public supplement workbook, task-effect categories are documented as proxy-based (see `README.md` Known Deviations).

## Limitations

- Business-side measures do not link to individual workers in public files.
- Supplement detail and questionnaire availability can change across waves; methodology docs describe the retained windows and definitions.
- Task-effect rows in Panel B can require documented proxy mappings when questionnaire item-25 option rows are absent in the public `AI_Supplement_Table.xlsx`.
