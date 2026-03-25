# Hearing Q&A (Virginia senator brief)

## Q1) Are you claiming AI caused these Virginia labor outcomes?
No. The package is descriptive and monitoring-oriented. It does not identify
causal AI treatment effects.
Evidence: `docs/senate_briefing_memo.md` non-claims section; `docs/methods_data.md`.

## Q2) Why should we trust these numbers?
Each headline metric maps to explicit pipeline outputs and run metadata with
deterministic selection rules and reproducibility checks.
Evidence: `docs/senate_briefing_lineage_va.md`; `intermediate/state_deep_dive_qcew_51_run_metadata.json`; `intermediate/virginia_memo_kpis_run_metadata.json`.

## Q3) Why focus on Virginia specifically if the federal datasets are national?
National instruments still support a policy-relevant Virginia readout when
state-level benchmark and peer comparisons are extracted consistently.
Evidence: `figures/state_deep_dive_qcew_51_profile.csv`; `figures/state_deep_dive_qcew_51_peers.csv`.

## Q4) What does rank 1 of 31 in retail share actually imply?
It implies Virginia's sector mix is unusually concentrated in retail within the
retained benchmark set, which should influence oversight priorities, not causal
inference.
Evidence: `figures/state_deep_dive_qcew_51_ranks.csv`; `va05_virginia_sector_ranks`.

## Q5) Why not build a new federal AI labor data system now?
Near-term policy payoff is higher from upgrading existing surveys quickly, while
longer-run linked architecture planning continues in parallel.
Evidence: `docs/senate_briefing_memo.md` federal action matrix; `docs/claim_audit.md`.

## Q6) What is the immediate ask to agencies in the next quarter?
Scope and standardize: finalize CPS module wording, BTOS core-item continuity,
and metadata publication standards.
Evidence: `docs/senate_briefing_memo.md` (0-3 month horizon section).

## Q7) How do BTOS state AI-use values fit this brief?
They provide business-reported adoption context, which is useful for monitoring
and trend interpretation but not worker-level causal claims.
Evidence: `figures/memo_btos_state_ai_use_latest.csv`; `figures/virginia_memo_kpis.csv`; `docs/memo_visual_precision.md`.

## Q8) Why compare Virginia to DC/MD/NC/TN/KY/WV?
That peer frame strengthens regional policy interpretation for Senate audiences
and highlights where Virginia's structure diverges from nearby labor markets.
Evidence: `intermediate/state_deep_dive_qcew_51_run_metadata.json` peer list; `figures/state_deep_dive_qcew_51_peers.csv`.

## Q9) What are the strongest guardrails to avoid overclaiming?
Three guardrails: descriptive-not-causal framing, no worker-firm linkage
inference from public files, and no fine-grained local monthly causal claims.
Evidence: `docs/senate_briefing_memo.md` non-claims; `docs/methods_data.md`.

## Q10) What should we expect by 9-18 months if Congress supports this path?
A scoped JOLTS supplement pilot can improve occupation-aware demand context and
yield evaluable evidence on feasibility and burden.
Evidence: `docs/senate_briefing_memo.md` 9-18 month action row; `figures/figure4_panelA_jolts_sector_rates.csv`; `figures/figure4_panelB_ces_sector_index.csv`.

