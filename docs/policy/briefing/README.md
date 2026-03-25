# Senator and staff briefing pack (Virginia)

This folder is **isolated** from general policy documentation on purpose. It holds **senate- and senator-facing narrative**, **hearing-style Q&A**, **print order**, **frozen headline values**, and **Virginia-specific technical summary** built from the same reproducible `figures/` and `intermediate/*_run_metadata.json` lineage as the empirical stack.

Treat these files as **operationally sensitive**: distribution, attribution, and reuse should follow your institution’s rules for legislative or external-facing materials.

**Separation from the claim audit:** [claim audit](../claim_audit.md) is the **repository-wide** ledger for what the evidence supports, including rows that reference briefing artifacts when those claims are published externally. This `briefing/` folder holds **narrative, Q&A, and packet order** optimized for staff workflow; it is not a substitute for the audit. When a briefing sentence goes public, the supporting row in the claim audit should cite the same CSV or metadata path the build produced. Conversely, draft language here may lag the audit—treat the audit as the cross-check before any “approved for release” statement.

## Contents (index)

| File | Role |
|------|------|
| [senate_briefing_memo.md](senate_briefing_memo.md) | Full memo, executive summary, visual decision table, federal action matrix, non-claims |
| [senate_briefing_evidence_baseline_va.md](senate_briefing_evidence_baseline_va.md) | Frozen headline values and canonical file list |
| [senate_briefing_lineage_va.md](senate_briefing_lineage_va.md) | Metric-to-source and visual-to-CSV lineage |
| [senate_briefing_script_va.md](senate_briefing_script_va.md) | Short spoken brief |
| [senate_briefing_qa_va.md](senate_briefing_qa_va.md) | Hearing-style Q&A with evidence pointers |
| [senator_handout_1page_va.md](senator_handout_1page_va.md) | One-page staff handout |
| [senator_packet_order_va.md](senator_packet_order_va.md) | Print order and live briefing sequence |
| [senator_cps_condensed_brief.md](senator_cps_condensed_brief.md) | Condensed CPS-oriented brief |
| [virginia_deep_dive.md](virginia_deep_dive.md) | Virginia tables, stems `va01`–`va08`, rebuild pointers |

## Related (outside this folder)

- Senator-facing claim ledger: [claim audit](../claim_audit.md) (`docs/policy/claim_audit.md` from repo root)
- Figure and stem catalog: [figure catalog](../../figures/figure_catalog.md)
- Replication / memo build orchestration: [replication README](../../replication/README.md)
