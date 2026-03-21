# Occupational-Transition

Public-data paper pipeline: shared crosswalks, figures, and documentation.

## PR-000 shared outputs

- `crosswalks/occ22_crosswalk.csv` — 22-group occupation taxonomy (CPS / SOC 2018).
- `crosswalks/sector6_crosswalk.csv` — six-sector demand taxonomy (BTOS, JOLTS, CES, BED, QCEW-aligned NAICS).
- `docs/data_registry.csv` — source URLs and snapshot metadata.

## Rebuild crosswalks

Place official inputs under `raw/` (see `docs/data_registry.csv`), then:

```bash
pip install -r requirements.txt
python scripts/build_crosswalks.py
python scripts/qa_crosswalks.py
```

Methodology: [docs/pr000_crosswalk_methodology.md](docs/pr000_crosswalk_methodology.md).
