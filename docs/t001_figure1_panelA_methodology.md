# T-001 — Figure 1 Panel A occupational baseline (methodology)

Last source verification refresh: 2026-03-22.

## Scope

Build the national occupational baseline for the fixed 22 occupation groups in `crosswalks/occ22_crosswalk.csv`.

## Official data sources

Registered in `docs/data_registry.csv` under:

- `bls_oews_tables_hub`
- `bls_oews_may2024_national_zip`
- `bls_oews_may2024_technical_notes`
- `bls_oews_may2024_news_release`

Primary file: `oesm24nat.zip` (national OEWS workbook used by `scripts/build_figure1_panelA.py`).

## Geography and reference period

- Geography: United States national estimates only.
- Reference period in current build: May 2024 OEWS (release date April 2, 2025).

## Input mapping and joins

1. Read national OEWS rows where `O_GROUP == "detailed"`.
2. Convert each detailed `OCC_CODE` to SOC major `XX-0000`.
3. Join to `crosswalks/occ22_crosswalk.csv` via `CPS_PRDTOCC1` rows using `soc_major_group_code`.
4. Exclude military by construction (`55-0000` / `PRDTOCC1 == 23` is outside the 1..22 civilian groups).

## Calculations

- `employment`: sum of `TOT_EMP` within each `occ22_id`.
- `employment_share`: `employment / total_employment`, where `total_employment` is OEWS national total row `OCC_CODE == "00-0000"`.
- `median_annual_wage` (group approximation):
  - row `wage_proxy = A_MEDIAN` if numeric, else `A_MEAN`, else `H_MEDIAN * 2080`;
  - group value `sum(TOT_EMP * wage_proxy) / sum(TOT_EMP)`, rounded to nearest dollar for output.

For the May 2024 run, the national total differs from sum of detailed rows by 1,080 jobs; this reconciliation is recorded in `intermediate/figure1_panelA_occ_baseline_meta.csv`.

## Outputs

- `figures/figure1_panelA_occ_baseline.csv`
  - columns: `occupation_group`, `employment`, `employment_share`, `median_annual_wage`
- `intermediate/figure1_panelA_occ_baseline_meta.csv`
  - run metadata and reconciliation fields

## QA checks

Implemented in `scripts/qa_figure1_panelA.py`:

- exactly 22 output rows
- no missing required fields
- one row per occupation group
- employment-share consistency and denominator checks

## Reproducibility commands

```bash
pip install -r requirements.txt
python scripts/build_figure1_panelA.py
python scripts/qa_figure1_panelA.py
```

## Retrieval fallback

If direct `www.bls.gov` download is blocked, place the official OEWS zip at `raw/oesm24nat.zip` and rerun the build.

## Figure rendering

Publication-ready static visuals are generated from the existing figure CSV
outputs (no data-value changes) using:

```bash
python scripts/run_visuals_all.py
python scripts/qa_visuals.py
```

Artifacts:

- `visuals/png/*.png`
- `visuals/vector/*.pdf`
- `intermediate/visuals_run_manifest.json`

Style and chart standards are documented in `docs/visual_style_guide.md`.

