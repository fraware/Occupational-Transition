# T-008 — Figure 4 Panel A JOLTS sector rates

## Outputs

- `figures/figure4_panelA_jolts_sector_rates.csv` — monthly national **seasonally adjusted** JOLTS **rates** (published values only) for the fixed six-sector taxonomy, one canonical JOLTS industry per `sector6_code`.
- `intermediate/figure4_panelA_jolts_sector_rates_run_metadata.json` — LABSTAT file URLs, SHA-256 hashes, month window, retained BLS `series_id` list, and lineage notes.

## Official sources

All inputs are retrieved from the BLS LABSTAT JOLTS directory:

- Index: `https://download.bls.gov/pub/time.series/jt/`
- Series definitions: `jt.series`
- Industry labels (reference): `jt.industry` (also registered as `bls_jt_industry` in `docs/data_registry.csv`)
- Period codes: `jt.period`
- Seasonality codes: `jt.seasonal`
- Data (levels and rates, partitioned by measure):
  - `jt.data.2.JobOpenings`
  - `jt.data.3.Hires`
  - `jt.data.5.Quits`
  - `jt.data.6.LayoffsDischarges`

Registry rows for T-008-specific files: see `docs/data_registry.csv` (`bls_jt_*` entries dated 2026-03-21).

## Geography and frequency

- **Geography:** national United States only. In `jt.series`, this corresponds to `state_code == 00`, `area_code == 00000`, and `sizeclass_code == 00` (all size classes, national tabulation).
- **Frequency:** monthly rows only (`period` codes `M01` … `M12`). Annual-average rows (`M13` and related) are excluded by construction.

## Seasonal adjustment and rate versus level

- **Seasonally adjusted only:** `jt.series` field `seasonal` must be `S`. LABSTAT `series_id` values for these series begin with `JTS` (third character `S`), consistent with BLS JOLTS documentation (`jt.txt`).
- **Rates only:** `ratelevel_code == R` in `jt.series`. Level rows (`L`) are never read.

## Time window

- Retained months satisfy `month >= 2019-01` through the most recent month available in the published BLS files at run time.

## Sector mapping (PR-000)

Frozen six-sector labels and codes come from `crosswalks/sector6_crosswalk.csv` (`source_program == JOLTS`, `is_in_scope == 1`).

**Canonical JOLTS industry code per `sector6_code` (one published national industry rate series per sector):**

| sector6_code | sector6_label | JOLTS `industry_code` | Rationale |
|--------------|---------------|------------------------|-----------|
| MFG | Manufacturing | 300000 | Manufacturing total |
| RET | Retail trade | 440000 | Retail trade |
| INF | Information | 510000 | Information |
| FAS | Financial activities | 510099 | Financial activities (published aggregate) |
| PBS | Professional and business services | 540099 | Professional and business services (published aggregate) |
| HCS | Health care and social assistance | 620000 | Health care and social assistance |

The crosswalk also maps JOLTS `610000` (private educational services) to `PBS`. This pipeline **does not** use `610000` because the panel uses a **single** published national industry series per `sector6_code`; `540099` is the headline professional and business services aggregate for PBS. No rates are recomputed across industries.

## Rate identifiers

`rate_name` values are:

- `job_openings_rate` — `dataelement_code` `JO`
- `hires_rate` — `HI`
- `quits_rate` — `QU`
- `layoffs_discharges_rate` — `LD`

## Data lineage

- `series_id` in the CSV is the exact BLS LABSTAT identifier for each observed rate.
- `rate_value` is the published numeric rate from the corresponding `jt.data.*` file; no recomputation from levels or cross-industry aggregation.

## QA

```bash
python scripts/qa_figure4_panelA_jolts_sector_rates.py
```

Checks include column schema, uniqueness of `month` by `sector6_code` by `rate_name`, a full 6-by-4 grid per month, nonnegative numeric rates, SA-only `series_id` pattern, and consistency between metadata SHA-256 hashes and the retained LABSTAT files (re-download verification).

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

