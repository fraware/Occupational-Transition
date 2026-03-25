# Virginia deep dive (briefing module)

This note provides a Virginia-specific slice of the reproducible pipeline that is **additive** (it does not change any main figure or visuals outputs). The current deep dive is built from the state-level benchmark in **T-017 (QCEW state benchmark)**.

## What is included (now)

- **State sector composition + wages (QCEW):** Virginia’s employment shares across the project’s frozen six-sector system, plus average weekly wages, for the **single retained QCEW period** used in T-017.
- **Comparisons for briefing:** Virginia’s **rank** among the states present in the T-017 output (per sector), and a **peer comparison table** for VA neighbors + DC.

## How to (re)build

From repo root:

```bash
python scripts/build_figureA7_qcew_state_benchmark.py
python scripts/qa_figureA7_qcew_state_benchmark.py

python scripts/build_state_qcew_deep_dive.py --state-fips 51
python scripts/qa_state_qcew_deep_dive.py --state-fips 51
python scripts/build_virginia_memo_kpis.py
python scripts/visualize_virginia_memo.py
python scripts/qa_virginia_memo_visuals.py
```

## Outputs (Virginia = FIPS 51)

- `figures/state_deep_dive_qcew_51_profile.csv`
  - Virginia’s six-sector profile (shares + wages) for the retained period.
- `figures/state_deep_dive_qcew_51_ranks.csv`
  - Virginia’s within-sector rank across the states contained in `figureA7_qcew_state_benchmark.csv`.
- `figures/state_deep_dive_qcew_51_peers.csv`
  - Virginia vs default peers (**DC, KY, MD, NC, TN, WV**) for each sector.
- `intermediate/state_deep_dive_qcew_51_run_metadata.json`
  - Parameters and output paths for provenance.
- `figures/virginia_memo_kpis.csv`
  - Briefing KPI extract sourced from Virginia deep-dive tables (and BTOS state table when available).
- `intermediate/virginia_memo_kpis_run_metadata.json`
  - KPI extraction lineage and retained period.
- `visuals/png/va01_virginia_sector_composition.png` (+ matching PDF)
- `visuals/png/va02_virginia_sector_wages.png` (+ matching PDF)
- `visuals/png/va03_virginia_peers_sector_shares.png` (+ matching PDF)
- `visuals/png/va04_virginia_peers_sector_wages.png` (+ matching PDF)
- `visuals/png/va05_virginia_sector_ranks.png` (+ matching PDF)
- `visuals/png/va06_virginia_kpi_dashboard.png` (+ matching PDF)
- Optional when source inputs exist: `va07_virginia_btos_state_highlight`, `va08_virginia_occ_context`

## Current headline numbers (from the latest run)

Retained period: **2025 Q3** (as defined by T-017’s deterministic “latest available” rule).

Virginia sector employment share (six-sector denominator):

- **Health care and social assistance (HCS):** 37.62%
- **Manufacturing (MFG):** 28.69%
- **Retail trade (RET):** 16.00%
- **Professional and business services (PBS):** 15.95%
- **Financial activities (FAS):** 1.41%
- **Information (INF):** 0.32%

Selected Virginia ranks within the T-017 state set (rank 1 = highest):

- **RET share rank:** 1 of 31
- **MFG share rank:** 4 of 31
- **INF wage rank:** 5 of 31
- **FAS wage rank:** 4 of 31

## Notes and limits (important for briefing language)

- These are **official QCEW published values** aggregated to a frozen six-sector mapping; they are a **structural benchmark**, not a measure of AI exposure or adoption.
- The “state total employment” denominator here is **restricted to the six in-scope sectors** (per T-017), not total statewide employment across all NAICS.
- State ranks are computed over the states present in the **T-017 output** (which enforces complete six-sector coverage for the retained period).

## Senator-facing documentation (uses this module)

| Document | Role |
|----------|------|
| `docs/policy/briefing/senate_briefing_memo.md` | Full memo, executive summary, visual decision table, federal action matrix, non-claims |
| `docs/policy/briefing/senate_briefing_evidence_baseline_va.md` | Frozen headline values and canonical file list |
| `docs/policy/briefing/senate_briefing_lineage_va.md` | Metric-to-source and visual-to-CSV lineage |
| `docs/policy/briefing/senate_briefing_script_va.md` | Two-minute spoken brief |
| `docs/policy/briefing/senate_briefing_qa_va.md` | Hearing-style Q&A with evidence pointers |
| `docs/policy/briefing/senator_handout_1page_va.md` | One-page staff handout |
| `docs/policy/briefing/senator_packet_order_va.md` | Print order and live briefing sequence |
| `docs/policy/claim_audit.md` | Senator brief claim ledger (Virginia package) |

**Full memo + Virginia build in one pass:** `python scripts/run_memo_visuals_build.py` then `python scripts/run_memo_visuals_qa.py` (see `docs/replication/README.md`).
