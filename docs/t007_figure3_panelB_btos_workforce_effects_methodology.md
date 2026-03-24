# T-007 — Figure 3 Panel B BTOS workforce effects

## Outputs

- `figures/figure3_panelB_btos_workforce_effects.csv` — six frozen categories with national published weighted shares (unit: share in `[0, 1]`).
- `intermediate/figure3_panelB_btos_workforce_effects_run_metadata.json` — source URL, file hash, universe, window, per-category mapping, fallback documentation.

## Official sources

| Role | Location |
|------|----------|
| Primary tabular product | `https://www.census.gov/hfp/btos/downloads/AI_Supplement_Table.xlsx` |
| BTOS experimental landing (context) | `https://www.census.gov/data/experimental-data-products/business-trends-and-outlook-survey.html` |
| AI supplement questionnaire (wording) | `https://www2.census.gov/data/experimental-data-products/business-trends-and-outlook-survey/questionnaire-ai-supplement.pdf` |
| Pooled-window corroboration (research product) | `https://www.census.gov/hfp/btos/downloads/CES-WP-24-16.pdf` (Table 5 and Table 6 notes on six two-week panels) |

## Geography and universe

- Geography: **national** (`National Response Estimates` sheet).
- Respondent universe: **Scope 2** in the workbook data dictionary — businesses that reported using artificial intelligence to produce goods or services in the **last six months**.

## Frozen time window

- **window_start**: `2023-12-04`
- **window_end**: `2024-02-25`

These endpoints match the T-007 design. Census CES-WP-24-16 describes pooling across **six** two-week collection panels for the AI supplement; first and last reference periods in that paper align to early December 2023 through mid-February 2024 (see Table 5/6 notes). The CSV records the paper’s frozen calendar endpoints for traceability.

## Category mapping

### Employment effects (exact published rows)

The workbook tabulates internal **Question ID 6.0** for Scope 2:

- `employment_increased` — Answer `Increased`
- `employment_decreased` — Answer `Decreased`
- `employment_did_not_change` — Answer `Did not change`

These match **CES-WP-24-16 Table 6 Panel A** (Last 6 months, firm-weighted) for the pooled supplement window.

### Task-effect categories (questionnaire item 25)

The public `AI_Supplement_Table.xlsx` used by this pipeline **does not** include separate rows for questionnaire **item 25** (*Select all that apply*: perform a task previously done by an employee; supplement or enhance a task; introduce a new task; none of the above). A binary search of the downloaded workbook confirms those answer strings are absent.

**Primary-source rule:** the build script first looks for published rows whose question text matches item 25. If Census adds those rows in a future release, they are used automatically and recorded as `exact_published_q25` in metadata.

**Documented fallback rule:** when item 25 is absent, the pipeline uses **other published Scope 2 rows in the same workbook** as interpretive proxies, not as statistical equivalents to item 25:

| Frozen `category_key` | Published proxy used (Scope 2) | Interpretation limit |
|----------------------|--------------------------------|----------------------|
| `perform_task_previously_done_by_employee` | Question ID **3.0**, Answer **Yes** | Published incidence of using AI to perform tasks previously done by employees (discussed in CES-WP-24-16 as the task-replacement incidence among AI users). Not identical to selecting only the item 25 “perform” option conditional on the business-functions grid. |
| `supplement_or_enhance_task_performed_by_employee` | Question ID **7.0**, Answer **Trained current staff to use AI** | Organizational adjustment to use AI; **not** the item 25 “supplement or enhance” option. |
| `introduce_new_task_not_previously_done_by_employee` | Question ID **7.0**, Answer **Developed new workflows** | Organizational process change; **not** the item 25 “introduce a new task” option. |

**Official archive/v1 fallback URL:** the build script attempts `https://www.census.gov/hfp/btos/downloads/archive/v1/AI_Supplement_Table.xlsx`. As of implementation, that URL did not return a valid Excel workbook (HTML response). Any future valid archive file that contains item 25 tabulations should be preferred when the script is re-run.

## Percent parsing

`Estimate` cells are published as percent strings (for example `26.6%`). The pipeline converts to numeric shares in `[0, 1]` once.

## Reproducibility

Requires network access to Census.

```bash
pip install -r requirements.txt
python scripts/build_figure3_panelB_btos_workforce_effects.py
python scripts/qa_figure3_panelB_btos_workforce_effects.py
```

## QA checks

Implemented in `scripts/qa_figure3_panelB_btos_workforce_effects.py`: six frozen keys, column schema, non-missing labels and shares, share bounds, national universe and window consistency, primary-source URL and file hash presence, and per-category mapping entries in metadata.

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

