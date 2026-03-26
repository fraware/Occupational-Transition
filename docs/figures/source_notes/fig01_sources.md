# Figure 1 — Data sources and provenance

## Primary sources

- **OEWS national occupation employment and wages:** See `docs/data_registry.csv` entries for the OEWS national file used in T-001 (for example `oews_*` / OEWS special request zip URLs). Official program: BLS OEWS.
- **O*NET Work Activities (Importance scale) and SOC crosswalk:** O*NET database zip from the O*NET Resource Center; see registry rows for `onet_*_text_database_zip` and `onet_soc2019_to_soc2018_crosswalk`.
- **22-group mapping:** `crosswalks/occ22_crosswalk.csv` (PR-000).

## Run metadata

- `intermediate/figure1_panelA_run_metadata.json` (T-001)
- `intermediate/figure1_panelB_run_metadata.json` (T-002)

## Provenance pointers

- **Figure CSV outputs:** `figures/figure1_panelA_occ_baseline.csv`, `figures/figure1_panelB_task_heatmap.csv`
- **Methodology docs:** `docs/methodology/tickets/t001_figure1_panelA_methodology.md`, `docs/methodology/tickets/t002_figure1_panelB_methodology.md`
- **Derived grouping input used downstream:** `intermediate/ai_relevance_terciles.csv`

## Reproducibility hashes (SHA256)

- `figures/figure1_panelA_occ_baseline.csv` — `f3d0e58516bd231cecb05c27889c40644021fbe892def9a7ccdd698d53602555`
- `figures/figure1_panelB_task_heatmap.csv` — `3d9e4090bfed6a1e3cd04305b79b292d7c4f0e32c4099a58f41d7f6e4f1046f0`
- `intermediate/ai_relevance_terciles.csv` — `ed51a3d2884c246a6229a2a1c79a49ad7551b700047eae5a4dff7cac5754433b`
- `intermediate/figure1_panelA_run_metadata.json` — `86fe15822f9a030c87ae7de0307ba4348dadd244e57e462855aaa94853336edc`
- `intermediate/figure1_panelB_run_metadata.json` — `522784782e7af9436725975d2e0d66f14351e07a29fe678faa7612b783a0e60d`
- `crosswalks/occ22_crosswalk.csv` — `947ea24f0791b473da0eefa1e0798b3c9b6a6afe55f975368851dc430d3230a4`

## Limitations

- OEWS and O*NET describe occupational structure and tasks; they do not by themselves identify realized AI labor-market impacts.
- AI-relevance terciles are a rank partition on a constructed index from selected O*NET elements; alternative weighting or element choices can change borders between groups (see robustness scripts under `scripts/robustness/`).
- National panels do not display geographic distribution; for PUMA-level composition use appendix T-019 (`figures/figureA9_acs_local_composition.csv`) when Claim 1 wording references geography.
