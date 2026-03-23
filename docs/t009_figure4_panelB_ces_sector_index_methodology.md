# T-009 — Figure 4 Panel B CES payroll employment index

## Outputs

- `figures/figure4_panelB_ces_sector_index.csv` — monthly national CES payroll employment (thousands) by frozen `sector6_code`, re-expressed as an index with `2023-08 = 100` per sector.
- `intermediate/figure4_panelB_ces_sector_index_run_metadata.json` — LABSTAT file URLs, SHA-256 hashes, month window, canonical CES `series_id` list, and lineage notes.

## Official sources

All inputs are retrieved from the BLS LABSTAT CES directory:

- Index: `https://download.bls.gov/pub/time.series/ce/`
- Survey and file layout: `ce.txt`
- Series definitions: `ce.series`
- Supersector labels: `ce.supersector` (also registered as `bls_ce_supersector` in `docs/data_registry.csv`)
- Industry codes: `ce.industry` (also `bls_ce_industry`)
- Datatype codes: `ce.datatype`
- Period codes: `ce.period`
- Seasonality codes: `ce.seasonal`
- Data: `ce.data.01a.CurrentSeasAE` (all seasonally adjusted all-employee series; see `ce.txt` Section 2)

Registry rows for T-009-specific files: see `docs/data_registry.csv` (`bls_ce_*` entries dated 2026-03-22).

## Geography and frequency

- **Geography:** CES national estimates only (LABSTAT CE national database).
- **Frequency:** monthly rows (`period` codes `M01` … `M12`).

## Seasonal adjustment and employment concept

- **Seasonally adjusted only:** `ce.series` field `seasonal` must be `S`. LABSTAT `series_id` values for these series use the `CES` prefix (third character `S`), consistent with `ce.txt` series-id decomposition.
- **All employees, thousands:** `data_type_code` = `01` per `ce.datatype` / `ce.txt` (datatype 01 = all employees, thousands).

## Time window

- Retained months satisfy `month >= 2019-01` through the latest month available in the published BLS files at run time.

## Sector mapping (PR-000)

Frozen six-sector codes and labels are taken from `crosswalks/sector6_crosswalk.csv` (`source_program == CES`, `source_level == ces_supersector`, `is_in_scope == 1`).

**Canonical published CES supersector series (one per `sector6_code`, avoiding double-counting durable/nondurable manufacturing):**

| sector6_code | sector6_label | CES `supersector_code` | CES `industry_code` (8-digit supersector total) |
|--------------|---------------|--------------------------|--------------------------------------------------|
| MFG | Manufacturing | 30 | 30000000 |
| RET | Retail trade | 42 | 42000000 |
| INF | Information | 50 | 50000000 |
| FAS | Financial activities | 55 | 55000000 |
| PBS | Professional and business services | 60 | 60000000 |
| HCS | Health care and social assistance | 65 | 65000000 |

**Design note:** CES supersector `65` is titled “Private education and health services” in LABSTAT. PR-000 maps this row to `sector6_code` **HCS** (“Health care and social assistance”) for the frozen six-sector comparison. The index therefore reflects the combined CES supersector employment series, not health alone.

## Indexing rule

For each sector, let `E_{t}` be published CES employment in thousands for month `t`, and `E_{2023-08}` the value in `2023-08`. Then:

`index_aug2023_100 = 100 * (E_{t} / E_{2023-08})`.

No values are imputed beyond published CES levels.

## QA

```bash
python scripts/qa_figure4_panelB_ces_sector_index.py
```

Checks include column schema, uniqueness of `month` x `sector6_code`, six sectors per month, `2023-08` index equals 100 for each sector, SA `series_id` pattern, and SHA-256 consistency between metadata and live LABSTAT files.

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

