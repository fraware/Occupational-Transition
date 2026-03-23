# Figure 1 — Data sources and provenance

## Primary sources

- **OEWS national occupation employment and wages:** See `docs/data_registry.csv` entries for the OEWS national file used in T-001 (for example `oews_*` / OEWS special request zip URLs). Official program: BLS OEWS.
- **O*NET Work Activities (Importance scale) and SOC crosswalk:** O*NET database zip from the O*NET Resource Center; see registry rows for `onet_*_text_database_zip` and `onet_soc2019_to_soc2018_crosswalk`.
- **22-group mapping:** `crosswalks/occ22_crosswalk.csv` (PR-000).

## Run metadata

- `intermediate/figure1_panelA_run_metadata.json` (T-001)
- `intermediate/figure1_panelB_run_metadata.json` (T-002)

## Limitations

- OEWS and O*NET describe occupational structure and tasks; they do not by themselves identify realized AI labor-market impacts.
- AI-relevance terciles are a rank partition on a constructed index from selected O*NET elements; alternative weighting or element choices can change borders between groups (see robustness scripts under `scripts/robustness/`).
- National panels do not display geographic distribution; for PUMA-level composition use appendix T-019 (`figures/figureA9_acs_local_composition.csv`) when Claim 1 wording references geography.
