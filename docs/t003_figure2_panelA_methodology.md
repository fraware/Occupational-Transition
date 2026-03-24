# T-003 — Figure 2 Panel A: usual weekly hours by AI-relevance tercile

Last source verification refresh: 2026-03-22.

## Scope

Build national monthly usual weekly hours by frozen AI relevance tercile using CPS Basic Monthly public-use files.

## Outputs

- `figures/figure2_panelA_hours_by_ai_tercile.csv` — national monthly series by tercile with columns `month`, `ai_relevance_tercile`, `mean_usual_weekly_hours`, and `sum_composite_weight`.
- `intermediate/figure2_panelA_run_metadata.json` — provenance: months processed, allowlisted gaps, retrieval asset kind (`zip`, `dat_gz`, or `cached_dat`), CPS source URLs, SHA-256 hashes, and record layout file used.

## Data sources (official)

| Role | Source |
|------|--------|
| CPS hub | U.S. Census Bureau, CPS data products: `https://www.census.gov/programs-surveys/cps/data/datasets.html` |
| CPS Basic Monthly | `https://www.census.gov/data/datasets/time-series/demo/cps/cps-basic.html` |
| Retrieval pattern | `https://www2.census.gov/programs-surveys/cps/datasets/<year>/basic/` |
| Weights / methodology | `https://www2.census.gov/programs-surveys/cps/methodology/PublicUseDocumentation_final.pdf` (composite weight `PWCMPWGT`) |
| Record layout | Year-specific `YYYY_Basic_CPS_Public_Use_Record_Layout_plus_IO_Code_list.txt` under each year’s `basic/` folder; if a year file is absent, the pipeline uses the 2020 layout (see `scripts/build_figure2_panelA.py`). |
| Revisions / gaps | `https://www.census.gov/programs-surveys/cps/data/datasets/cps-basic-footnotes.html` |

Registry rows: `docs/data_registry.csv` (CPS T-003 entries).

## Time and geography

- **Reference period:** January 2019 through the most recent month with a published Basic CPS file on Census servers (as detected at run time).
- **Geography:** national (all states in the CPS public-use file).

## Universe and filters

Person-level records from the Basic CPS monthly person file (fixed-width person records, 1000 characters per line in sampled years).

1. **Civilian noninstitutional population age 16+:** `PRPERTYP = 2`, `PRTAGE >= 16` (per project specification).
2. **Employed:** `PEMLR` in `{1, 2}` (employed, at work or with a job but not at work).
3. **Valid usual hours:** `PEHRUSL1` numeric and between 1 and 99 (excludes NIU / invalid codes stored as negative or non-numeric in the fixed field).
4. **Civilian occupation groups:** `PRDTOCC1` in `1..22` (exclude military code `23`).
5. **Weight:** composite final weight `PWCMPWGT` with four implied decimals; analysis weight = `PWCMPWGT / 10_000` per CPS public-use documentation.

## Input mapping and joins

1. Map `PRDTOCC1` to `occ22_id` using `CPS_PRDTOCC1` rows in `crosswalks/occ22_crosswalk.csv` (civilian codes 1–22).
2. Join `occ22_id` to frozen `intermediate/ai_relevance_terciles.csv` from T-002 to assign `low` / `middle` / `high`.

## Calculations

For each calendar month (from interview fields `HRYEAR4`, `HRMONTH`) and each AI relevance tercile:

`mean_usual_weekly_hours = sum(weight * PEHRUSL1) / sum(weight)` where `weight = PWCMPWGT / 10_000`.

The CSV also includes `sum_composite_weight` (sum of scaled weights in the estimation cell) for transparency and QA.

## Missing official months

- **October 2025:** No Basic CPS public-use microdata file was published (documented on the Census CPS Basic footnotes page). The pipeline skips this month and records it in metadata and QA allowlists.

## File retrieval notes

- Primary artifact is `monYYpub.zip` (e.g. `jan19pub.zip`). The pipeline verifies the ZIP magic bytes (`PK\x03\x04`).
- If a ZIP download returns an HTML error page (observed for `feb20pub.zip` behind the Census CDN in some environments), the pipeline falls back to `monYYpub.dat.gz`, decompresses to `monYYpub.dat`, and parses the same fixed-width layout.

## Reproducibility commands

```bash
pip install -r requirements.txt
python scripts/build_figure2_panelA.py
python scripts/qa_figure2_panelA.py
```

## QA checks

Implemented in `scripts/qa_figure2_panelA.py`:

- one row per `month x ai_relevance_tercile`
- exactly 3 terciles per retained month
- no missing required fields
- positive `sum_composite_weight`
- month sequence starts at `2019-01` and matches build metadata
- only allowlisted official missing months (allowlist at verification time: `2025-10`)

## Revision policy

CPS Basic files may be re-released with corrected weights or identifiers. Re-running the build overwrites outputs and updates `figure2_panelA_run_metadata.json` with new hashes and the layout URL used for each run.

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

