# Appendix: Virginia headline metric lineage

This appendix maps each senator-facing Virginia metric to its figure source and
metadata provenance artifact.

| Headline metric | Value (current run) | Figure/source file | Metadata/provenance artifact | Notes/limits |
|-----------------|---------------------|--------------------|------------------------------|--------------|
| Virginia HCS share (six-sector denominator) | 37.6217165586% | `figures/state_deep_dive_qcew_51_profile.csv` | `intermediate/state_deep_dive_qcew_51_run_metadata.json` | Descriptive QCEW benchmark; not causal. |
| Virginia manufacturing share (six-sector denominator) | 28.6928222745% | `figures/state_deep_dive_qcew_51_profile.csv` | `intermediate/state_deep_dive_qcew_51_run_metadata.json` | Descriptive QCEW benchmark; not causal. |
| Virginia retail share rank | 1 of 31 | `figures/state_deep_dive_qcew_51_ranks.csv` | `intermediate/state_deep_dive_qcew_51_run_metadata.json` | Rank among retained benchmark states only. |
| Virginia manufacturing share rank | 4 of 31 | `figures/state_deep_dive_qcew_51_ranks.csv` | `intermediate/state_deep_dive_qcew_51_run_metadata.json` | Rank among retained benchmark states only. |
| Virginia information sector weekly wage rank | 5 of 31 | `figures/state_deep_dive_qcew_51_ranks.csv` | `intermediate/state_deep_dive_qcew_51_run_metadata.json` | Relative rank only; not effect size. |
| Virginia financial activities wage rank | 4 of 31 | `figures/state_deep_dive_qcew_51_ranks.csv` | `intermediate/state_deep_dive_qcew_51_run_metadata.json` | Relative rank only; not effect size. |
| Virginia HCS share minus peer mean | -21.4574784837 pp | `figures/virginia_memo_kpis.csv` (from `state_deep_dive_qcew_51_peers.csv`) | `intermediate/virginia_memo_kpis_run_metadata.json` | Peer set: DC, KY, MD, NC, TN, WV plus VA. |
| Virginia BTOS current AI use share | 0.186 (18.6%) | `figures/virginia_memo_kpis.csv` (from `figures/memo_btos_state_ai_use_latest.csv`) | `intermediate/virginia_memo_kpis_run_metadata.json` | Business-reported adoption signal; descriptive only. |

## Visual-to-source map (`va01`-`va06`)

| Visual stem | Data file(s) |
|-------------|--------------|
| `va01_virginia_sector_composition` | `figures/state_deep_dive_qcew_51_profile.csv` |
| `va02_virginia_sector_wages` | `figures/state_deep_dive_qcew_51_profile.csv` |
| `va03_virginia_peers_sector_shares` | `figures/state_deep_dive_qcew_51_peers.csv` |
| `va04_virginia_peers_sector_wages` | `figures/state_deep_dive_qcew_51_peers.csv` |
| `va05_virginia_sector_ranks` | `figures/state_deep_dive_qcew_51_ranks.csv` |
| `va06_virginia_kpi_dashboard` | `figures/virginia_memo_kpis.csv` |

## Rebuild/verification commands

```bash
python scripts/build_state_qcew_deep_dive.py --state-fips 51
python scripts/build_virginia_memo_kpis.py
python scripts/visualize_virginia_memo.py
python scripts/qa_state_qcew_deep_dive.py --state-fips 51
python scripts/qa_virginia_memo_visuals.py
```

