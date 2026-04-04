# Figure 3 — Data sources and provenance

## Primary sources

- **BTOS API (national stratum):** Census BTOS public API; published firm-weighted shares. See `docs/methodology/tickets/t006_figure3_panelA_btos_ai_trends_methodology.md`.
- **BTOS AI Supplement Table (XLSX):** Census-published workbook for workforce-effect shares. See `docs/methodology/tickets/t007_figure3_panelB_btos_workforce_effects_methodology.md` and `README.md` (Known Deviations) for task-category mapping notes.

## Run metadata

- `intermediate/figure3_panelA_btos_ai_trends_run_metadata.json`
- `intermediate/figure3_panelB_btos_workforce_effects_run_metadata.json`

## Provenance pointers

- **Figure CSV outputs:** `figures/figure3_panelA_btos_ai_trends.csv`, `figures/figure3_panelB_btos_workforce_effects.csv`
- **Methodology docs:** `docs/methodology/tickets/t006_figure3_panelA_btos_ai_trends_methodology.md`, `docs/methodology/tickets/t007_figure3_panelB_btos_workforce_effects_methodology.md`
- **Interpretation guardrail:** when item-25 option rows are absent in the public supplement workbook, task-effect categories are documented as proxy-based (see `README.md` Known Deviations).

## Reproducibility hashes (SHA256)

- `figures/figure3_panelA_btos_ai_trends.csv` — `e223b68eb9a285e42a7ebc8301d19a376823ef541a2c5978a25fe9cbd13e7e90`
- `figures/figure3_panelB_btos_workforce_effects.csv` — `e539cbdc34c051affad6eda2703375a2e3cf28a6557863b4ee8f0219ac09a02a`
- `intermediate/figure3_panelA_btos_ai_trends_run_metadata.json` — `8f239c99555e43c3f7505889ca7d92126f32f54307d487456f717f2675e0c475`
- `intermediate/figure3_panelB_btos_workforce_effects_run_metadata.json` — `e0ae01a6890c00446241b6823cd7ae399f3b4c34174f60876ef327d83692d86a`

## Limitations

- Business-side measures do not link to individual workers in public files.
- Supplement detail and questionnaire availability can change across waves; methodology docs describe the retained windows and definitions.
- Task-effect rows in Panel B can require documented proxy mappings when questionnaire item-25 option rows are absent in the public `AI_Supplement_Table.xlsx`.

## Presentation note

The redesigned Figure 3 preserves the frozen BTOS figure CSVs and the existing evidence-directness contract. In Panel B, rows coded `direct_published` are rendered separately from rows coded `proxy_mapping` to prevent visual equivalence between direct released evidence and proxy-interpreted indicators.
