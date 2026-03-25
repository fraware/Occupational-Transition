# T-012 — Figure A2 medium-run adjustment (SIPP event study)

## Purpose

`figures/figureA2_sipp_event_study.csv` summarizes national, weighted event-time paths around the first observed occupational or employment-status transition after a baseline month in which the respondent is employed in a mapped `occ22` major group, using Census Survey of Income and Program Participation (SIPP) public-use person-month microdata.

## Data sources (official public use only)

- SIPP datasets index: `https://www.census.gov/programs-surveys/sipp/data/datasets.html`
- Annual primary person-month files (pipe-delimited CSV inside each `pu{YYYY}_csv.zip` on `www2.census.gov`), retained for this build for releases **2022, 2023, and 2024** (post-2019 panels with matching public schemas for required variables).
- SIPP technical documentation and data dictionaries: `https://www.census.gov/programs-surveys/sipp/tech-documentation/complete-technical-documentation.html` and `https://www.census.gov/programs-surveys/sipp/tech-documentation/data-dictionaries.html`
- Weight guidance for 2018+ SIPP: `https://www2.census.gov/programs-surveys/sipp/Select_weights_2018_SIPP_JUN24.pdf`

## Mapping lineage (frozen project artifacts)

- Occupation on the job record: `TJB1_OCC` (2018 Census occupation code) mapped to `occ22_id` using `source_system == CPS_PEIO1OCD_2018` rows in `crosswalks/occ22_crosswalk.csv`.
- AI terciles: `occ22_id` joined to `ai_relevance_tercile` in `intermediate/ai_relevance_terciles.csv` (T-002).

## Event definition

For each person identified by `SSUID`, `PNUM`, and `SPANEL`, person-month rows are ordered by `SWAVE` then `MONTHCODE`. The transition month (`event_time = 0`) is the **first** month such that:

- the prior month is in the survey month universe (`RIN_UNIV == 1`), age at least 16, employed under `RMESR` employed codes, and `TJB1_OCC` maps to an `occ22` code in 1–22; and
- the transition month is either not employed under those `RMESR` codes, or is employed with a different mapped `occ22` in 1–22.

Only the first qualifying transition per person is used.

## Event window and weighting

- Event-time index `k` runs from **-12** through **+24** months relative to the transition month when all three AI terciles have strictly positive summed person weights for that `k` (incomplete `k` are omitted from the output table).
- Person-month weight: `WPFINWGT` (final person weight on the SIPP person-month record).

## Outcomes (weighted means by `event_time` and `ai_relevance_tercile`)

| Output column | Definition |
|---------------|------------|
| `mean_employment_rate` | Share with `RMESR` in the employed codes documented in run metadata. |
| `mean_monthly_income` | Weighted mean of `TPTOTINC` with missing or invalid amounts treated as 0. |
| `mean_snap_participation` | Weighted mean of an indicator that `RSNAP_MNYN == 1` (SNAP receipt in the reference month). |
| `sum_person_weight` | Sum of `WPFINWGT` for person-months contributing to that cell. |

## Implementation note (ingestion)

The primary `pu.csv` inside each panel ZIP is large. The build script streams rows with Python `csv.DictReader` into a temporary on-disk SQLite table, creates an index on person and time, then reads in sorted order so person-month sequences are correct even when raw rows are not contiguous. This avoids loading the full file into memory (which can fail on typical machines) while keeping a deterministic sort for each person.

## Operational risk controls

- `out of memory` risk: avoided by streaming CSV rows into SQLite in fixed-size batches rather than loading full panel CSV files into pandas memory.
- Person chronology risk from noncontiguous raw rows: controlled by explicit `ORDER BY ssuid, pnum, spanel, swave, monthcode` prior to per-person event detection.
- Windows file-lock risk on scratch databases: controlled by unique scratch filenames per run (`_sipp_panel_<year>_<uuid>.sqlite`) so concurrent or interrupted runs do not reuse the same path.
- Residual artifact risk after interrupted runs: scratch SQLite files may persist in `intermediate/`; safe to delete after confirming no active T-012 build process.

## QA-critical ordering requirement

The output must contain tercile rows in this exact order for each `event_time`: `low`, `middle`, `high`. This is a deterministic schema contract enforced by `scripts/qa_figureA2_sipp_event_study.py`.

## Reproducibility

Run from the repository root (requires network access to Census `www2.census.gov` on first run; files cache under `raw/sipp/`):

```bash
python scripts/build_figureA2_sipp_event_study.py
python scripts/qa_figureA2_sipp_event_study.py
```

Hashes, URLs, and panel list are recorded in `intermediate/figureA2_sipp_event_study_run_metadata.json`.

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

