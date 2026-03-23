# Figure 4 — Data sources and provenance

## Primary sources

- **JOLTS LABSTAT time series:** `https://download.bls.gov/pub/time.series/jt/` (see registry and `docs/t008_figure4_panelA_jolts_sector_rates_methodology.md`).
- **CES LABSTAT time series:** `https://download.bls.gov/pub/time.series/ce/` (see `docs/t009_figure4_panelB_ces_sector_index_methodology.md`).
- **Six-sector mapping:** `crosswalks/sector6_crosswalk.csv`.

## Run metadata

- `intermediate/figure4_panelA_jolts_sector_rates_run_metadata.json`
- `intermediate/figure4_panelB_ces_sector_index_run_metadata.json`

## Limitations

- JOLTS sector flows are not occupation-resolved in the public core instrument.
- Sector series are model-assisted for some geographies; this figure uses published series as selected in the build scripts.
