# What U.S. Public Federal Data Can and Cannot Say About AI and Labor

## Subtitle

What Exists, What Works, and What Small Survey Changes Would Unlock

---

## Manuscript status and evidence alignment

This file is the **expanded manuscript** synthesized from the repository. Numeric claims must match frozen outputs for the evidence window you publish against. See [evidence_snapshot.md](evidence_snapshot.md) for tagging policy and the **T-004** transition-count snapshot rule. The bullet skeleton remains in [paper_draft_v1_public_data_ai_labor.md](paper_draft_v1_public_data_ai_labor.md) for comparison.

**Repository state for this revision:** manuscript numbers and examples below are aligned with commit `72f02bf2e7897f5515ab9212f9e6fe6fbcd2c432` (short `72f02bf`). Replace with a [release tag](release_process.md) such as `results-YYYY-MM-DD` when you publish a labeled freeze.

**Before circulation or submission:** A **commit hash documents which file tree** was used, but numbers in prose are only as consistent as the **single coordinated pipeline run** that produced them. Before wider distribution, confirm that every cited figure CSV—and for Figure 2 any dependent `memo_dashboard_kpis.csv` transition KPIs—comes from **one** acceptance or full-pipeline run (same `intermediate/*_run_metadata.json` window), not from a mix of ad hoc rebuilds. See [evidence_snapshot.md](evidence_snapshot.md) (“Commit vs. build-state”).

---

## Abstract

Debates over AI and labor have outpaced the U.S. federal public measurement system. This paper develops a **public-data framework**: a reproducible pipeline (PR-000 through T-020, with extension metrics T-021–T-026) that produces transparent CSV outputs, JSON lineage, and publication visuals for occupational structure and tasks, worker hours and matched-month transitions, business-reported AI adoption and workforce-effect categories, sector labor-demand and payroll context, and a rule-based **capability matrix** of what each major source can support for seven measurement objects—including the absence of a public worker–firm AI linkage.

**Substantive snapshot (descriptive, non-causal):** In the frozen outputs tied to commit `72f02bf`, high–low AI-relevance terciles differ by roughly **four weekly hours** in early 2026 CPS microdata; nationally BTOS firm-weighted **current AI-use** shares reach the **mid-20 percent range** in recent periods; and JOLTS **job-opening rates** in January 2026 differ by **nearly two percentage points** across the six comparison sectors—patterns that illustrate what the public stack can show without worker–firm linkage or AI treatment effects.

**Claim discipline (see [claim_audit.md](claim_audit.md)):** Main-text Figures 1–2 **directly support** Claims 1–2 within descriptive scope. **Claim 3** is **partially** supported: BTOS adoption and published employment-effect rows are direct; task-effect rows in Figure 3 Panel B require **proxy-explicit** wording where detailed supplement item tabulations are absent in public workbooks ([README.md](../README.md) Known Deviations; T-007). **Claim 4** is **directly supported** for sector context without occupation-resolved JOLTS. **Claim 5** splits an **empirical diagnosis** (no integrated public worker–firm AI panel in the matrix) from **policy design judgments** (survey priorities), which are not treatment-effect estimates.

The pipeline also builds optional **monitoring-only** occupation-time indices (AWES and ALPI in `metrics/`), defined in [methods_data.md](methods_data.md): they **do not replace** frozen AI-relevance terciles and **are not causal**. The contribution is disciplined measurement, explicit resolution limits, and a roadmap—chiefly CPS, BTOS, scoped JOLTS supplements, and NLS career items—not firm-level causal identification from public files alone.

---

## 1. Introduction

Research and policy audiences now ask whether AI is displacing work, augmenting tasks, or reshaping hiring faster than surveys can observe. Private and proprietary evidence can move quickly, but U.S. **public** federal data remain the backbone for transparent, reproducible monitoring and for democratic accountability. This paper asks a narrower, operational question: **what can federal public data already support at credible resolution**, and **where do hard limits remain**—not only in theory but in a fully ticketed, rebuildable empirical stack.

The gap this paper targets is not “more AI hype” but **measurement architecture**: a source-by-source audit of what each major instrument observes, combined with a working integration of OEWS, O*NET, CPS, BTOS, and JOLTS (with CES payroll context) in one pipeline. Public-use files **do not** support worker–firm linked causal attribution of AI impacts at national scale; the paper states that boundary throughout. The payoff is twofold: (i) a **descriptive** empirical spine suitable for monitoring and for supplement design, and (ii) a **roadmap** for incremental survey changes that maximize information per respondent burden.

**Outline.** Section 2 establishes occupational employment, wages, and task structure (Figure 1; Claim 1). Section 3 reports worker hours and broad transitions by AI-relevance tercile (Figure 2; Claim 2). Section 4 summarizes business-reported AI use and workforce-effect categories from BTOS (Figure 3; Claim 3, with proxy discipline). Section 5 places sector labor-demand and payroll dynamics from JOLTS and CES (Figure 4; Claim 4). Section 6 states cross-source capability boundaries (Figure 5; Claim 5). Section 7 briefly describes optional monitoring indices (AWES/ALPI). Section 8 condenses methods and data. Section 9 concludes. The appendix deepens worker, firm, demand, geographic, and long-run evidence (Figures A1–A10).

---

## 2. Occupational baseline and task structure (Figure 1; Claim 1)

**Claim 1** is that the paper provides a precise **national** baseline of AI-relevant occupations: employment, wages, and task content, before any dynamic interpretation.

**Main descriptive result.** We find **highly concentrated national employment** across the 22 groups: the largest shares in the baseline OEWS file are in Office and Administrative Support (about **11.8%** of employment), Transportation and Material Moving (about **8.9%**), and Food Preparation and Serving (about **8.8%**), with median annual wages spanning roughly **$34k** to **$121k** across groups; **Panel B** shows wide dispersion in standardized digital-task z-scores and in the AI Task Index, motivating deterministic tercile cuts (`figures/figure1_panelA_occ_baseline.csv`, `figures/figure1_panelB_task_heatmap.csv`).

**Data and construction.** Figure 1 combines BLS OEWS national employment and median annual wages with O*NET Work Activities (Importance scale), aggregated to **22 occupation groups** via the frozen crosswalk `crosswalks/occ22_crosswalk.csv`. T-002 forms z-scores for selected work activities, builds an **AI Task Index** as the mean of four digital-information-related z-scores, and assigns **deterministic AI-relevance terciles** for downstream figures. Outputs include `figures/figure1_panelA_occ_baseline.csv`, `figures/figure1_panelB_task_heatmap.csv`, and `intermediate/ai_relevance_terciles.csv` (build-generated).

**How to read Figure 1.** Panel A ranks groups by employment share and reports median wages. Panel B heatmaps standardized task intensities and the AI Task Index column that drives terciles. The figure is **descriptive and national**; it does not identify causal AI impacts or within-group heterogeneity.

**Geographic scope.** Per the claim audit, **main-text Claim 1** should **not** rest on subnational composition; geographic composition for AI-relevance groups appears in **appendix Figure A9** (ACS PUMS), not in Figure 1.

---

## 3. Worker hours and mobility (Figure 2; Claim 2)

**Claim 2** is that monthly CPS public-use microdata support **national descriptive monitoring** of usual weekly hours and broad occupational and labor-force transitions when persons are matched across **adjacent months**, using composite person weights and AI terciles from T-002.

**Main descriptive result.** We find a **stable weekly-hours gap** between AI-relevance terciles: in **2026-01** weighted mean usual weekly hours are about **40.4** (high), **37.4** (middle), and **36.3** (low)—roughly **four hours** between high and low (`figures/figure2_panelA_hours_by_ai_tercile.csv`). For transition summaries, origin-mass-weighted dashboard KPIs (same evidence window) report **unemployment-entry** and **NILF-entry** shares on the order of **0.7%** and **1.6%** for high-origin mass in **2026-01** (`figures/memo_dashboard_kpis.csv`; construction `docs/memo_visual_precision.md`). These are **descriptive** matched-month constructs, not causal AI effects.

**Data and construction.** T-003 averages usual weekly hours by month and tercile. T-004 builds transition counts in a coarse state space (22 occupation groups plus unemployment and NILF). T-005 row-normalizes to probabilities and produces summary metrics. Panel B combines a **latest-month** transition-count heatmap with time series of retention, occupation switching, unemployment entry, and NILF entry. See `docs/t003_*` through `docs/t005_*` for windows and weight handling.

**Interpretation.** The figure describes **survey-based** mobility and hours patterns by tercile. It does **not** identify which employers adopted AI or causal effects of AI on transitions.

**Evidence snapshot.** Align numeric prose with the same rebuild as your frozen `figures/figure2_*.csv` files; transition **counts** for Panel B are tied to T-004 per [evidence_snapshot.md](evidence_snapshot.md).

---

## 4. Business-side AI adoption (Figure 3; Claim 3)

**Claim 3** is **partially** supported: BTOS provides high-frequency, **business-reported** AI use and supplement-based workforce-effect shares suitable as the public firm-side benchmark—but not linked worker microdata.

**Main descriptive result.** We find that **national firm-weighted current AI-use** shares vary over time in the BTOS API series and reach the **mid-20 percent range** in recent periods (e.g., **25.1%** current and **33.7%** expected for the period starting **2026-01-26** in `figures/figure3_panelA_btos_ai_trends.csv`). In the retained supplement window, **directly published** employment-effect rows are dominated by **“employment did not change”** (**94.6%**), while the three **task-related** categories are **proxy-mapped** at **~27%, 21%, and 20%** shares (`figures/figure3_panelB_btos_workforce_effects.csv`, `evidence_directness` column)—language must remain **proxy-explicit** for those rows.

**Data and construction.** T-006 assembles national firm-weighted series for current and expected AI use by collection period. T-007 reads published AI Supplement Table shares for retained workforce-effect categories. **Known deviations:** the issue template’s locked BTOS window may differ from the first period with AI core questions in the API; the retained series follows published API periods ([README.md](../README.md)). For Panel B, **employment-effect** rows follow published tables; **task-related** categories may use **Scope 2 proxy mapping** when item-25 option rows are not publicly tabulated—prose must say “proxy-interpreted” or equivalent, not direct publication (T-007 methodology).

**Interpretation.** Read Panel A for adoption trends; Panel B for relative size of retained effect categories at business-reported descriptive level. Avoid worker-level or causal claims.

---

## 5. Labor demand and payroll context (Figure 4; Claim 4)

**Claim 4** is that JOLTS and CES provide official **sector-group** labor-demand and payroll context even though public JOLTS is **not** occupation-resolved.

**Main descriptive result.** We find **substantial cross-sector dispersion** in official flows and payroll: in **2026-01** JOLTS **job-opening rates** range from **3.8%** (Manufacturing and Information) to **5.6%** (Health care and social assistance)—about **1.8** percentage points across the six sectors (`figures/figure4_panelA_jolts_sector_rates.csv`). CES payroll employment indexed to August 2023 in the same month spans roughly **94.7** (Information) to **108.7** (Health care) (`figures/figure4_panelB_ces_sector_index.csv`). These are **sector aggregates**, not occupation-level or AI-attributed demand.

**Data and construction.** T-008 maps JOLTS flow rates to six sector groups; T-009 indexes CES payroll employment to 100 in August 2023. Mapping uses `crosswalks/sector6_crosswalk.csv`.

**Interpretation.** Panel A compares openings, hires, quits, and layoffs/discharges rates across sectors; Panel B shows payroll paths. These are **macro sector context**, not occupation-level vacancy or AI-specific demand.

---

## 6. Identification frontier (Figure 5; Claim 5)

**Claim 5** combines an **empirical** statement and a **design** judgment. The matrix in Figure 5 is **not estimated**; it encodes `direct`, `partial`, or `none` for seven empirical objects across five core datasets (CPS, BTOS, JOLTS, OEWS, O*NET), including **`worker_firm_ai_linkage`**, from locked rules in [lineage/t010_paper_notes_matrix.md](lineage/t010_paper_notes_matrix.md) and [lineage/t010_issues.md](lineage/t010_issues.md).

**Main boundary finding.** We find that **`worker_firm_ai_linkage` is coded `none` for all five datasets**—the matrix’s sharpest single statement is that **no** core public source in this stack can directly support integrated worker–firm AI linkage claims. **CPS** is `direct` on worker outcomes and occupational transitions; **BTOS** on `firm_ai_adoption`; **JOLTS** on `labor_demand_turnover`; **OEWS** on occupational structure/wages; **O*NET** on `task_exposure_mechanism` (`figures/figure5_capability_matrix.csv`).

**Empirical diagnosis.** The public stack does not supply an integrated worker–firm AI panel at scale.

**Policy recommendations** (CPS/BTOS modules, scoped JOLTS supplements, NLS items) are **measurement priorities**, not causal payoffs estimated here. Keep abstract and conclusion language consistent with that split per [claim_audit.md](claim_audit.md).

---

## 7. Optional monitoring indices (AWES and ALPI)

The extension pipeline (T-021–T-026) produces **Adoption-Weighted Exposure Score (AWES)** and **AI Labor Pressure Index (ALPI)** in `metrics/`. Both are **descriptive** occupation-time composites for monitoring and prioritization; **neither is causal** and neither replaces frozen AI-relevance terciles. Definitions and limits are in [methods_data.md](methods_data.md). Cite them only with that non-causal framing if included in a journal submission.

---

## 8. Methods and data (condensed)

**Design.** The analysis is **descriptive**: official weights where applicable, frozen crosswalks, and ticketed build/QA scripts. Full construction, universes, time windows, and limitations appear in [methods_data.md](methods_data.md) and per-ticket `docs/t*_methodology.md`. **Authoritative URLs and snapshot fields** are recorded in [data_registry.csv](data_registry.csv).

**Replication.** Environment, download behavior, and commands are in [replication.md](replication.md). Full clean rebuild: `python scripts/run_full_pipeline_from_raw.py` (see [README.md](../README.md)). Acceptance criteria: [acceptance_matrix.md](acceptance_matrix.md). **Evidence freeze:** examples and percentages in this manuscript were checked against commit **`72f02bf`** (`72f02bf2e7897f5515ab9212f9e6fe6fbcd2c432`); substitute an annotated tag (e.g. `results-YYYY-MM-DD`) when you publish a labeled release.

**Option (self-contained journal version).** For submission, paste or adapt subsections from [methods_data.md](methods_data.md) into the journal template; avoid duplicating every ticket verbatim.

---

## 9. Conclusion

The strongest **descriptive** takeaway from the frozen stack is not a causal estimate but a **joint pattern**: large national dispersion in occupational tasks and wages (Figure 1), persistent **hours and transition** differences by AI-relevance tercile in CPS (Figure 2), rising **business-reported AI use** in BTOS with **employment effects** mostly unchanged in published supplement rows (Figure 3), **wide sector gaps** in JOLTS/CES context (Figure 4), and a matrix that marks **worker–firm AI linkage as unsupported everywhere** (Figure 5).

U.S. public federal data can already support a **serious** AI-and-labor measurement program when integrated with explicit **resolution limits**: national occupational structure and tasks (Figure 1), worker hours and broad transitions (Figure 2), business-reported adoption and effects (Figure 3), sector demand and payroll (Figure 4), and explicit capability boundaries (Figure 5). The marginal policy value lies in **targeted survey extensions** and **transparent monitoring**, not in simulating firm-level causal identification from public files. Geographic composition belongs in appendix ACS (Figure A9); sector flows do not substitute for occupation-level demand. BTOS task-effect language must remain **proxy-explicit** where public tables require it.

---

## Appendix — Figures A1–A10 (order per [appendix_outline.md](appendix_outline.md))

The appendix deepens the main text in a fixed order: worker annual welfare (A1), SIPP medium-run adjustment (A2), CPS supplement validation (A3), ABS structural adoption (A4), CES payroll and hours (A5), BED churn (A6), QCEW state benchmark (A7), LEHD public benchmark (A8), **ACS local occupational composition (A9)**—supporting geographic scope for Claim 1 when needed—and NLSY97 long-run careers (A10). Draft paragraphs and figure paths are in [appendix_draft.md](appendix_draft.md); methodological detail is in `docs/t011_*` through `docs/t020_*`. Visual stems are `t011`–`t020` per [figure_catalog.md](figure_catalog.md).

---

## Policy and briefing artifacts (repository)

Optional senator and Virginia-facing materials (`docs/senate_briefing_*.md`, memo stems `t101`–`t108`, Virginia `va01`–`va08`) are **additive** to this manuscript; they are descriptive monitoring aids, not causal estimates. See [paper_draft_v1_public_data_ai_labor.md](paper_draft_v1_public_data_ai_labor.md) for entry points.

---

## References (starting set)

Compile the final bibliography in your journal’s style. Primary program documentation and registry pointers include:

- U.S. Bureau of Labor Statistics. Occupational Employment and Wage Statistics (OEWS); Job Openings and Labor Turnover Survey (JOLTS); Current Employment Statistics (CES); Business Employment Dynamics (BED); Quarterly Census of Employment and Wages (QCEW). See [data_registry.csv](data_registry.csv) for URLs used in builds.
- U.S. Census Bureau / BLS. Current Population Survey (CPS); American Community Survey (ACS); Business Trends and Outlook Survey (BTOS); Annual Business Survey (ABS); SIPP. See registry and `docs/source_notes/fig0*_sources.md`.
- U.S. Department of Labor / O*NET. O*NET database and Work Activities (Importance scale); see registry rows for O*NET downloads.
- National Longitudinal Surveys (NLS). NLSY97 public-use files; see `docs/t020_figureA10_nls_longrun_methodology.md` and registry.

Per-figure source notes: [source_notes/fig01_sources.md](source_notes/fig01_sources.md) through [fig05_sources.md](source_notes/fig05_sources.md).

---

## Figures for submission

Publication-ready **vector PDFs** for main-text stems `t001`–`t010` are under `visuals/vector/` (matching PNGs under `visuals/png/`). Regenerate with `python scripts/run_visuals_all.py` and validate with `python scripts/qa_visuals.py` per [README.md](../README.md). Ensure figure numbering matches this manuscript.

Export to Word or LaTeX via your journal template or Pandoc after content freeze.

---

## Reproducibility and integrity checklist

**Editorial verification (completed for this manuscript draft):**

- [x] At least one **empirical result lead** (we find / main pattern) in each main-text figure section (§§2–6).
- [x] Numeric examples in §§2–6 cite specific paths under `figures/*.csv` (and `figures/memo_dashboard_kpis.csv` where used for Figure 2 KPIs); repository state recorded as commit **`72f02bf`** in this file and [evidence_snapshot.md](evidence_snapshot.md).
- [x] [claim_audit.md](claim_audit.md) caveats reflected: Claim 1 geography → appendix A9 (§2, §9); Claim 3 **partial** support and **proxy-explicit** BTOS Panel B language (abstract, §4, §9); Claim 5 **empirical diagnosis** vs **policy judgment** (abstract, §6, §9).
- [x] [README.md](../README.md) Known Deviations: **T-006** (BTOS Panel A window vs. issue template; first AI-core period in API) and **T-007** (Scope 2 proxy mapping for supplement task rows when item-25 detail absent) stated in §4 and abstract cross-reference.
- [x] Abstract and conclusion treat Claims **3** and **5** as **partial** / split (design vs. diagnosis); no causal overclaim.
- [x] §8 **Replication** cites [replication.md](replication.md), [acceptance_matrix.md](acceptance_matrix.md), and **concrete** commit `72f02bf` / full hash.
- [x] AWES and ALPI framed as **non-causal** monitoring indices only (abstract; §7).

**Operational gate before publication (maintainer, not redundant with items above):**

- [ ] **Single-build confirmation:** After the final pipeline run you intend to stand behind, verify that every number in the manuscript matches the CSV cells and (for Figure 2 transition KPIs) the **same** `intermediate/` lineage as that run—especially `figure2_panelB_transition_counts.csv` → `figure2_panelB_transition_probs.csv` → memo KPI aggregation per [evidence_snapshot.md](evidence_snapshot.md). Optionally attach `intermediate/full_clean_rebuild_acceptance_<UTC>.md` to the release.

The drafting rule remains: **no invented datasets, no synthetic backfilling, and no claims beyond the resolution permitted by the underlying public instruments.**
