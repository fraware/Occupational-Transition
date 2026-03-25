# Virginia evidence baseline (senator brief)

This file freezes the exact evidence bundle and values used in the Virginia
senator brief package. It is intended to prevent claim drift between memo
drafts, visuals, and testimony preparation.

## Frozen reference period and peer set

- Retained benchmark period: **2025 Q3**
- State FIPS: **51 (Virginia)**
- Peer set (state FIPS): **11, 21, 24, 37, 47, 54** (DC, KY, MD, NC, TN, WV)

Primary provenance:

- `intermediate/state_deep_dive_qcew_51_run_metadata.json`
- `intermediate/virginia_memo_kpis_run_metadata.json`

## Canonical source files for senator brief claims

- `figures/state_deep_dive_qcew_51_profile.csv`
- `figures/state_deep_dive_qcew_51_ranks.csv`
- `figures/state_deep_dive_qcew_51_peers.csv`
- `figures/virginia_memo_kpis.csv`
- `figures/memo_btos_state_ai_use_latest.csv` (optional KPI input; included in
  current run)

## Frozen headline values (current run)

From `figures/state_deep_dive_qcew_51_profile.csv`:

- HCS share: **37.6217165586%**
- MFG share: **28.6928222745%**
- RET share: **15.9981403518%**
- PBS share: **15.9516491464%**
- FAS share: **1.4128160756%**
- INF share: **0.3228555932%**

From `figures/state_deep_dive_qcew_51_ranks.csv`:

- RET share rank: **1 of 31**
- MFG share rank: **4 of 31**
- INF wage rank: **5 of 31**
- FAS wage rank: **4 of 31**

From `figures/virginia_memo_kpis.csv`:

- Virginia BTOS current AI use share: **0.186** (18.6%), reference **BTOS period 95**
- Virginia HCS share minus peer mean: **-21.4574784837 pp**

## Visual spine references

The Virginia narrative spine uses:

- `va01_virginia_sector_composition`
- `va02_virginia_sector_wages`
- `va03_virginia_peers_sector_shares`
- `va04_virginia_peers_sector_wages`
- `va05_virginia_sector_ranks`
- `va06_virginia_kpi_dashboard`

## Usage rules

- Use these values directly for senator-facing narrative unless the data
  pipeline is rerun and this file is refreshed.
- Any new claim must point to one of the canonical source files above and, when
  possible, to metadata in `intermediate/*_run_metadata.json`.
- Claims about causality, worker-firm linkage, or fine-grained local monthly
  attribution remain out of scope for this evidence bundle.

## Related senator packet files

- Full narrative: `docs/policy/briefing/senate_briefing_memo.md`
- One-page handout: `docs/policy/briefing/senator_handout_1page_va.md`
- Print and briefing sequence: `docs/policy/briefing/senator_packet_order_va.md`
- Lineage appendix: `docs/policy/briefing/senate_briefing_lineage_va.md`
- Spoken script and Q&A: `docs/policy/briefing/senate_briefing_script_va.md`, `docs/policy/briefing/senate_briefing_qa_va.md`
- Claim audit rows: `docs/policy/claim_audit.md` (Senator brief claim ledger)

