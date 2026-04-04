# Figure 4 — Data sources and provenance

## Primary sources

- **JOLTS LABSTAT time series:** `https://download.bls.gov/pub/time.series/jt/` (see registry and `docs/methodology/tickets/t008_figure4_panelA_jolts_sector_rates_methodology.md`).
- **CES LABSTAT time series:** `https://download.bls.gov/pub/time.series/ce/` (see `docs/methodology/tickets/t009_figure4_panelB_ces_sector_index_methodology.md`).
- **Six-sector mapping:** `crosswalks/sector6_crosswalk.csv`.

## Run metadata

- `intermediate/figure4_panelA_jolts_sector_rates_run_metadata.json`
- `intermediate/figure4_panelB_ces_sector_index_run_metadata.json`

## Provenance pointers

- **Figure CSV outputs:** `figures/figure4_panelA_jolts_sector_rates.csv`, `figures/figure4_panelB_ces_sector_index.csv`
- **Methodology docs:** `docs/methodology/tickets/t008_figure4_panelA_jolts_sector_rates_methodology.md`, `docs/methodology/tickets/t009_figure4_panelB_ces_sector_index_methodology.md`
- **Sector grouping input:** `crosswalks/sector6_crosswalk.csv`

## Reproducibility hashes (SHA256)

- `figures/figure4_panelA_jolts_sector_rates.csv` — `2ad36a9a1f5824ae5e7d271a4c48e15fa0974ed9981ae09c53f7fff367fa8220`
- `figures/figure4_panelB_ces_sector_index.csv` — `5eb11d369fcd7fd273b767a7ba3f540ba0b4a4eedb81440eaf5654cef21f9e21`
- `intermediate/figure4_panelA_jolts_sector_rates_run_metadata.json` — `a644edc0680ce4931ebec0c2d036a3ed569e83a893233ac8f3ccdee604ad1898`
- `intermediate/figure4_panelB_ces_sector_index_run_metadata.json` — `8c6fbaba37ec56f8f0ec5f0c40ce4746538447af44c47b642dc7c6526a3e168d`
- `crosswalks/sector6_crosswalk.csv` — `741f6e827bdce9fd7b25442505ceef9acb700b1dc5bb16d104a1eaca6c55c0de`

## Limitations

- JOLTS sector flows are not occupation-resolved in the public core instrument.
- Sector series are model-assisted for some geographies; this figure uses published series as selected in the build scripts.

## Presentation note

The redesigned Figure 4 preserves the frozen Figure 4 CSV inputs. Panel A now renders the full set of JOLTS flow rates documented in the figure caption and memo—openings, hires, quits, and layoffs/discharges—using the same six-sector comparison set as the frozen build inputs. Panel B preserves the CES payroll-employment index structure and the August 2023 = 100 benchmark.
