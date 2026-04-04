# Virginia case study (FIPS 51)

Descriptive **structural** benchmarks for Virginia from the same six-sector QCEW frame as **T-017** (national state benchmark). This module is **additive**: it does not change main-text figure outputs.

## Reading order

1. [virginia_deep_dive.md](virginia_deep_dive.md) — outputs, rebuild commands, headline numbers, limits.
2. [methodology ticket T-017](../methodology/tickets/t017_figureA7_qcew_state_benchmark_methodology.md) — underlying QCEW aggregation and state benchmark rules.
3. [paper/methods_data.md](../paper/methods_data.md) — how the Virginia slice relates to the manuscript (short subsection).

## Rebuild (tracked scripts)

From repo root, after T-017 is built and QA’d:

```bash
python scripts/build_state_qcew_deep_dive.py --state-fips 51
python scripts/qa_state_qcew_deep_dive.py --state-fips 51
```

This writes `figures/state_deep_dive_qcew_51_*.csv` and `intermediate/state_deep_dive_qcew_51_run_metadata.json` (paths may be gitignored in your clone; see `.gitignore`).

## Optional: memo KPIs and visuals

Briefing KPI extraction and static charts (`va01`–`va08`, file stems `virginia_*`) use local scripts such as `scripts/build_virginia_memo_kpis.py`, `scripts/visualize_virginia_memo.py`, and `scripts/qa_virginia_memo_visuals.py`. PNG/PDF outputs are written under **[visuals/](visuals/)** (`docs/states/virginia/visuals/png` and `.../vector`). Those scripts and their CSV/visual outputs are **optional** and may be **gitignored**; if present, run them after the deep-dive step. Details: [virginia_deep_dive.md](virginia_deep_dive.md).

## Senator- or staff-facing narrative (local-only)

If your tree includes `docs/policy/briefing/` senate or senator Virginia pack files, they are **not** required for federal replication. The tracked technical spec remains this folder and [claim_audit.md](../../policy/claim_audit.md) (including the SB-VA ledger rows).
