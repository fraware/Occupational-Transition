# Examples (library-only)

Run from the **repository root** after a normal install:

```bash
pip install -e .
python examples/01_btos_national.py
```

| Script | Network | Description |
|--------|---------|-------------|
| [01_btos_national.py](01_btos_national.py) | Yes | National BTOS AI-use series via `occupational_transition.sources.btos` |
| [02_occ22_from_crosswalk.py](02_occ22_from_crosswalk.py) | No | Load `occ22` labels from committed `crosswalks/occ22_crosswalk.csv` |
| [03_jolts_parse_offline.py](03_jolts_parse_offline.py) | No | Parse a tiny embedded LABSTAT snippet with `sources.jolts` helpers |
| [04_sector6_labels.py](04_sector6_labels.py) | No | JOLTS in-scope sector labels from `crosswalks/sector6_crosswalk.csv` |
| [05_onet_soc_crosswalk.py](05_onet_soc_crosswalk.py) | Yes (once) | Download O*NET–SOC crosswalk into `raw/` and load with pandas |
| [compare_two_sources.py](compare_two_sources.py) | Yes (once) | Fetch two LABSTAT reference files via `catalog.fetch_by_dataset_id` and compare line counts |

These scripts do **not** run the full paper pipeline (`scripts/run_full_pipeline_from_raw.py`). For replication, see [docs/replication/README.md](../docs/replication/README.md).
