# T-006 — Figure 3 Panel A: BTOS AI-use trends (methodology)

Last source verification refresh: 2026-03-22.

## Scope

National time series of published BTOS firm-weighted shares for current AI use and expected AI use over the next six months, using the Census BTOS public API. No microdata are recomputed.

## Outputs

- `figures/figure3_panelA_btos_ai_trends.csv` — one row per BTOS collection period with available national `naics2=XX` data.
- `intermediate/figure3_panelA_btos_ai_trends_run_metadata.json` — endpoint URLs, SHA-256 hashes of `periods` and `questions` responses, per-period data hashes, and periods dropped when the API returns no payload or incomplete Yes estimates.

## Official data sources

| Role | Source |
|------|--------|
| BTOS product | `https://www.census.gov/data/experimental-data-products/business-trends-and-outlook-survey.html` |
| API documentation | `https://www.census.gov/hfp/btos/api_docs` |
| API reference PDF | `https://www.census.gov/hfp/btos/downloads/BTOS%20API%20Reference%20Documentation.pdf` |
| Periods | `GET https://www.census.gov/hfp/btos/api/periods` |
| Questions | `GET https://www.census.gov/hfp/btos/api/questions` |
| Stratum data | `GET https://www.census.gov/hfp/btos/api/periods/{period}/data/naics2/XX` |

Registry rows: `docs/data_registry.csv` (`census_btos_*` T-006 entries).

## Geography and stratum

- **Geography:** United States national estimate from the BTOS **NAICS all-sectors** stratum (`naics2` = `XX`), not a state or metro cell.

## Time window

- The BTOS AI core questions appear in the public `questions` catalog starting at **PERIOD_ID 31** (collection beginning **2023-09-11** per the API `periods` list). Period **30** (2023-08-28 to 2023-09-10) has no AI rows in the `questions` endpoint, so the empirical series begins at the first period with both AI questions and a non-null `data` payload for `naics2/XX`.
- Later periods may return a JSON `null` body until Census publishes that wave; those periods are listed under `dropped_periods` in the run metadata and are omitted from the CSV.

## Extraction rules

For each retained `PERIOD_ID`:

1. **Period start date:** calendar date of `COLLECTION_START` from the `periods` response (parsed to `YYYY-MM-DD` for `period_start_date`).
2. **Current AI use rate:** `ESTIMATE_PERCENTAGE` for the response row with `OPTION_TEXT == "AI current"` and `ANSWER == "Yes"`, divided by 100 to express a share in [0, 1].
3. **Expected AI use (next six months) rate:** same for `OPTION_TEXT == "AI future"` and `ANSWER == "Yes"`.

Wording of the underlying `QUESTION` text was updated in some waves (for example, broader “business functions” language); selection uses **OptionText** and **Answer** fields, not question text, so published shares remain comparable at the Yes-share level.

## Question wording updates

Census documents AI question updates (for example, `https://www.census.gov/hfp/btos/downloads/AI%20Question%20Wording%20Updates.pdf` linked from the BTOS visualization page). This pipeline does not merge or adjust estimates across definitions beyond the published API.

## Reproducibility commands

```bash
pip install -r requirements.txt
python scripts/build_figure3_panelA_btos_ai_trends.py
python scripts/qa_figure3_panelA_btos_ai_trends.py
```

## QA checks

Implemented in `scripts/qa_figure3_panelA_btos_ai_trends.py`:

- fixed column schema and no missing values
- `source_series_id` equals `naics2_XX`
- rates in [0, 1]
- `period_start_date` on or after 2023-08-28 and sorted ascending
- no duplicate period keys
- metadata includes `periods_sha256`, `questions_sha256`, and `per_period_data_hashes` aligned with output rows

## Interpretation limits

Values are published BTOS shares for the specified national stratum, subject to Census disclosure and sampling methodology. They are not establishment counts or causal adoption effects.

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

Style and chart standards are documented in `docs/quality/README.md#visual-style-guide`.

