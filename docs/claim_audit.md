# Claim audit (frozen five claims)

Source text: `paper-notes.md` section "Recommended final set of 5 core claims" (and the locked wording block that follows).

Mapping: Claim *k* is evaluated against **Figure *k*** main-text outputs (multi-panel figures combine panels listed in `docs/figure_catalog.md`).

Support levels:

- **Supported directly:** The figure’s measured objects are the same objects the claim describes, within documented limits.
- **Supported partially:** The claim is broader than the figure (additional geography, causal language, or sources not in the figure).
- **Not yet supported:** Additional evidence or narrower wording is required.

| Claim | Figure | Support level | Evidence | Caveats / minimal fix |
|-------|--------|---------------|----------|------------------------|
| **1** — Precise baseline description of AI-relevant occupations: employment, wages, geographic distribution, task content | Figure 1 (OEWS baseline + O*NET heatmap; terciles for downstream use) | **Partial** | `figures/figure1_panelA_occ_baseline.csv`, `figures/figure1_panelB_task_heatmap.csv`, `intermediate/ai_relevance_terciles.csv`; memos `docs/figure_memos/fig01.md` | Geographic distribution is **not** in Figure 1 national panels; cite appendix ACS (`figureA9`) or narrow Claim 1 wording to national structure + task content. |
| **2** — Worker-side outcomes and broad occupational mobility via survey inference, not public linked admin microdata | Figure 2 (CPS hours + transitions) | **Supported directly** (within descriptive scope) | `figures/figure2_panelA_hours_by_ai_tercile.csv`, `figures/figure2_panelB_transition_probs.csv`; `docs/figure_memos/fig02.md` | Avoid causal language; transitions are matched-month public-use constructs. |
| **3** — Business-side AI adoption and self-reported workforce effects from business surveys | Figure 3 (BTOS trends + supplement shares) | **Supported directly** (published business-side series) | `figures/figure3_panelA_btos_ai_trends.csv`, `figures/figure3_panelB_btos_workforce_effects.csv`; `docs/figure_memos/fig03.md` | Note documented T-007 mapping notes in `README.md` Known Deviations if reviewers ask about supplement categories. |
| **4** — Labor-demand and turnover dynamics in AI-relevant **sectors** without occupation-resolved public demand flows | Figure 4 (JOLTS + CES by sector6) | **Supported directly** | `figures/figure4_panelA_jolts_sector_rates.csv`, `figures/figure4_panelB_ces_sector_index.csv`; `docs/figure_memos/fig04.md` | Do not claim occupation-level vacancy or hire rates from these panels. |
| **5** — Main gap is lack of a public integrated worker–firm AI panel; extend existing surveys | Figure 5 (capability matrix) | **Supported directly** (architecture/synthesis level) | `figures/figure5_capability_matrix.csv` (includes `worker_firm_ai_linkage`); `docs/figure_memos/fig05.md` | Matrix is documentation-based synthesis, not an estimator; do not reinterpret categorical cells as effect magnitudes. |

## Action items from audit

1. **Claim 1 vs geography:** Either add explicit ACS appendix citation whenever "geographic distribution" appears, or tighten Claim 1 language to match what Figure 1 actually shows (national OEWS + national O*NET aggregation).
2. **Claim 5:** Keep synthesis language tied to `paper-notes.md` symbols and `issues.md` T-010 rules; avoid implying the matrix quantifies welfare or causal AI effects.

## Closure criteria

- Figure 5 parity: the matrix schema and renderer must both use `worker_firm_ai_linkage`.
- Figure 3 panel-B language: task-effect interpretation must remain proxy-explicit when Q25 option rows are absent in public supplements.
- If an audit run is scoped/bounded, the closure file must explicitly state limits before sign-off.

## Sign-off

| Reviewer | Date | Notes |
|----------|------|-------|
| | | |
