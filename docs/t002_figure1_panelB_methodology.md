# T-002 — Figure 1 Panel B task heatmap and AI Task Index (methodology)

Last source verification refresh: 2026-03-22.

## Scope

Build a national 22-group task heatmap and AI relevance terciles using O*NET task-content measures and OEWS employment weights.

## Official data sources

Registered in `docs/data_registry.csv` under O*NET `onet_*` entries and OEWS `bls_oews_*` entries.

Primary files:

- O*NET text bundle `db_30_2_text.zip` (default runtime pin `30.2`)
- O*NET-SOC crosswalk `2019_to_SOC_Crosswalk.csv`
- OEWS national file `oesm24nat.zip`

## Geography and reference period

- Geography: United States national estimates only.
- O*NET reference: version selected by `--onet-version` (default `30.2`).
- OEWS reference in current build: May 2024 national file.

## Input mapping and joins

1. Read `Work Activities.txt` and keep `Scale ID == "IM"` rows for six fixed descriptors:
   - Analyzing Data or Information
   - Processing Information
   - Documenting/Recording Information
   - Working with Computers
   - Assisting and Caring for Others
   - Handling and Moving Objects
2. Map `O*NET-SOC Code` to `2018 SOC Code` with official crosswalk.
3. Collapse to SOC-detail-by-descriptor means.
4. Join to OEWS detailed employment (`O_GROUP == "detailed"`, `TOT_EMP`).
5. Map SOC detail to SOC major and then to `occ22` via `crosswalks/occ22_crosswalk.csv`; exclude military (`55-0000`).

## Calculations

- Employment-weighted descriptor scores by `occ22`:
  - `score = sum(employment * descriptor_value) / sum(employment)`
- Z-scores across the 22 groups for each descriptor (`ddof=0`).
- AI Task Index:
  - mean of z-scores for the four digital-information descriptors:
    - Analyzing Data or Information
    - Processing Information
    - Documenting/Recording Information
    - Working with Computers
- Deterministic terciles:
  - sort by (`ai_task_index`, `occ22_id`)
  - assign low ranks 1-7, middle 8-14, high 15-22
  - resulting counts: 7 / 7 / 8

## Outputs

- `figures/figure1_panelB_task_heatmap.csv`
  - columns: `occupation_group`, `occ22_id`, six `z_*` descriptor columns
- `intermediate/ai_relevance_terciles.csv`
  - columns: `occupation_group`, `occ22_id`, `ai_task_index`, `ai_relevance_tercile`
- `intermediate/figure1_panelB_meta.csv`
  - run metadata (O*NET version, scale, OEWS source path, tercile rule)

## QA checks

Implemented in `scripts/qa_figure1_panelB.py`:

- exactly 22 rows in each output
- all 22 occupation groups present once
- no missing z-score values
- valid AI index and tercile labels
- deterministic tercile count check (7/7/8)

## Reproducibility commands

```bash
pip install -r requirements.txt
python scripts/build_figure1_panelB.py
python scripts/qa_figure1_panelB.py
```

Optional explicit pin:

```bash
python scripts/build_figure1_panelB.py --onet-version 30.2
```

## Interpretation and license

The AI Task Index is a paper-defined grouping construct, not a direct measure of realized AI adoption. O*NET content is released under CC BY 4.0; follow attribution guidance from `https://www.onetcenter.org/database.html`.

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

