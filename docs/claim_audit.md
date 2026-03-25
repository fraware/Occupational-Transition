# Claim audit (frozen five claims)

Source text: `docs/archive/paper_notes_full.md` section "Recommended final set of 5 core claims" (and the locked wording block that follows).

Mapping: Claim *k* is evaluated against **Figure *k*** main-text outputs (multi-panel figures combine panels listed in `docs/figure_catalog.md`).

Support levels:

- **Supported directly:** The figure’s measured objects are the same objects the claim describes, within documented limits.
- **Supported partially:** The claim is broader than the figure (additional geography, causal language, or sources not in the figure).
- **Not yet supported:** Additional evidence or narrower wording is required.

| Claim | Figure | Support level | Evidence | Caveats / minimal fix |
|-------|--------|---------------|----------|------------------------|
| **1** — Precise baseline description of AI-relevant occupations: employment, wages, and task content | Figure 1 (OEWS baseline + O*NET heatmap; terciles for downstream use) | **Supported directly** | `figures/figure1_panelA_occ_baseline.csv`, `figures/figure1_panelB_task_heatmap.csv`, `intermediate/ai_relevance_terciles.csv`; memos `docs/figure_memos/fig01.md` | Geographic distribution evidence is handled in appendix ACS (`figureA9`), not in Figure 1 main-text panels. |
| **2** — Worker-side outcomes and broad occupational mobility via survey inference, not public linked admin microdata | Figure 2 (CPS hours + transitions) | **Supported directly** (within descriptive scope) | `figures/figure2_panelA_hours_by_ai_tercile.csv`, `figures/figure2_panelB_transition_probs.csv`; `docs/figure_memos/fig02.md` | Avoid causal language; transitions are matched-month public-use constructs. |
| **3** — Business-side AI adoption and self-reported workforce effects from business surveys | Figure 3 (BTOS trends + supplement shares) | **Partial** | `figures/figure3_panelA_btos_ai_trends.csv`, `figures/figure3_panelB_btos_workforce_effects.csv`; `docs/figure_memos/fig03.md` | Direct for adoption and published employment-effect rows; task-effect interpretation is proxy-based where item-25 rows are absent (see T-007 methodology and `README.md` Known Deviations). |
| **4** — Labor-demand and turnover dynamics in selected comparison sectors without occupation-resolved public demand flows | Figure 4 (JOLTS + CES by sector6) | **Supported directly** | `figures/figure4_panelA_jolts_sector_rates.csv`, `figures/figure4_panelB_ces_sector_index.csv`; `docs/figure_memos/fig04.md` | Do not claim occupation-level vacancy or hire rates from these panels. |
| **5** — Main gap is lack of a public integrated worker–firm AI panel; extend existing surveys | Figure 5 (capability matrix) | **Partial** | `figures/figure5_capability_matrix.csv` (includes `worker_firm_ai_linkage`); `docs/figure_memos/fig05.md` | Direct for the missing integrated panel diagnosis; partial for the policy recommendation (design judgment, not an estimated effect). |

## Composite monitoring metrics (AWES / ALPI; T-021–T-026)

**AWES** (`metrics/awes_occ22_monthly.csv`) and **ALPI** (`metrics/alpi_occ22_monthly.csv`) are **descriptive** occupation-time indices for monitoring and prioritization. They are **not causal** and do not estimate treatment effects. They **complement** the frozen AI-relevance terciles (`intermediate/ai_relevance_terciles.csv`) and inherit the limits of OEWS, O*NET, BTOS, JOLTS, CES, and CPS transition constructs. Method detail: `docs/methods_data.md` (AWES and ALPI section).

## Action items from audit

1. **Claim 1 scope discipline:** Keep Claim 1 in main text scoped to employment, wages, and task content; route geographic composition statements to appendix ACS evidence (`figureA9`).
2. **Claim 3 wording discipline:** Keep proxy-explicit language for Figure 3 panel-B task-effect interpretation in captions, results prose, and summaries when item-25 rows are absent in public supplements.
3. **Claim 5 split:** Keep a clear split between (a) empirical diagnosis (missing integrated panel) and (b) policy design recommendation (survey-extension priority), including in abstract, conclusion, and policy-facing text.

## Closure criteria

- Figure 5 parity: the matrix schema and renderer must both use `worker_firm_ai_linkage`.
- Figure 3 panel-B language: task-effect interpretation must remain proxy-explicit when Q25 option rows are absent in public supplements.
- If an audit run is scoped/bounded, the closure file must explicitly state limits before sign-off.

## Sign-off

Fill before public freeze; remove underscores when complete.

| Reviewer | Date | Notes |
|----------|------|-------|
| _Name_ | _YYYY-MM-DD_ | _Optional notes_ |

## Senator brief claim ledger (Virginia package)

This ledger enforces the policy-facing claim discipline for the Virginia
senator brief artifacts.

| Claim ID | Claim (short) | Claim type | Evidence file path | Metadata/provenance path | Guardrail note |
|----------|----------------|------------|--------------------|---------------------------|----------------|
| SB-VA-01 | Virginia HCS and manufacturing concentration in retained benchmark frame | `descriptive_fact` | `figures/state_deep_dive_qcew_51_profile.csv` | `intermediate/state_deep_dive_qcew_51_run_metadata.json` | Six-sector denominator only; not all-industry statewide share. |
| SB-VA-02 | Virginia peer-relative rank position (for example RET rank 1, MFG rank 4) | `descriptive_fact` | `figures/state_deep_dive_qcew_51_ranks.csv` | `intermediate/state_deep_dive_qcew_51_run_metadata.json` | Relative ordering only; not causal or effect magnitude. |
| SB-VA-03 | Virginia differs from nearby peers in sector structure and wage profile | `inference` | `figures/state_deep_dive_qcew_51_peers.csv` | `intermediate/state_deep_dive_qcew_51_run_metadata.json` | Peer comparison supports prioritization framing, not causal explanation. |
| SB-VA-04 | Virginia KPI dashboard provides actionable oversight monitoring stack | `inference` | `figures/virginia_memo_kpis.csv` | `intermediate/virginia_memo_kpis_run_metadata.json` | Monitoring construct only; does not estimate treatment effects. |
| SB-VA-05 | BTOS state AI-use contributes business-side adoption context in Virginia | `descriptive_fact` | `figures/memo_btos_state_ai_use_latest.csv` | `intermediate/virginia_memo_kpis_run_metadata.json` | Business-reported adoption; not worker-level causal evidence. |
| SB-VA-06 | Priority sequence should be CPS module + BTOS stability + scoped JOLTS pilot | `policy_judgment` | `docs/senate_briefing_memo.md` | `docs/senate_briefing_lineage_va.md` | Policy design recommendation grounded in capability limits, not estimated causal payoff. |
| SB-VA-07 | Brief is descriptive and excludes worker-firm linked causal claims | `descriptive_fact` | `docs/senate_briefing_memo.md` | `docs/methods_data.md` | Must remain explicit in testimony and hearing responses. |

### Rewrites applied in this pass

- Strengthened non-claim language in the memo to explicitly exclude:
  - causal AI effect estimation,
  - worker-firm linked inference from public files,
  - fine-grained local monthly causal attribution.
- Kept policy actions framed as design judgments supported by descriptive
  evidence and measurement constraints.

### Reliability field requirement (policy-facing tables)

For dashboard and briefing KPI tables, each claim-supporting row should include:

- uncertainty (`se`, `ci_lower`, `ci_upper`, `ci_level`, `variance_method`),
- reliability (`weighted_n`, `effective_n`, `cv`, `reliability_tier`),
- publishability (`publish_flag`, `suppression_reason`, `pooling_applied`),
- evidence directness (`direct_published`, `derived_transform`, `proxy_mapping`).
