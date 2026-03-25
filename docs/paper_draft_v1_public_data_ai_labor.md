# What U.S. Public Federal Data Can and Cannot Say About AI and Labor

**Expanded manuscript (full prose):** [paper_final.md](paper_final.md). **Evidence tagging:** [evidence_snapshot.md](evidence_snapshot.md).

## Subtitle
What Exists, What Works, and What Small Survey Changes Would Unlock

## Abstract
This paper develops a public-data framework for measuring AI and labor-market change in the United States. Using reproducible outputs from a full PR-000 through T-026 pipeline, we show that existing federal public data support a credible descriptive architecture for occupational structure and tasks, worker outcomes and mobility, business adoption, labor-demand flows, and cross-dataset identification limits. The pipeline also produces optional **monitoring-only** occupation-time composites (AWES and ALPI in `metrics/`), defined in `docs/methods_data.md`, which **do not replace** frozen AI-relevance terciles and **are not causal** estimates. The public measurement stack is strongest when it combines worker-side and business-side sources at coarse, policy-relevant resolution; it is weakest where occupation-level demand flows and worker-firm linkage are required for high-precision attribution. The paper contributes a source-by-source measurement audit, an empirical public-data stack, a sample-sufficiency rule for responsible inference, and a concrete low-, medium-, and high-effort roadmap for improving AI labor measurement through CPS, BTOS, JOLTS, and NLS pathways. The argument is not that public data are sufficient for firm-level causal identification, but that they are already strong enough for credible monitoring and for prioritizing high-yield survey additions.

## 1. Introduction
**Thesis.** Debates on AI and labor markets have moved faster than the U.S. public measurement architecture; this paper asks what federal public data can already support at credible resolution, and where hard limits remain.

**Dataset sentence.** The empirical core uses OEWS, O*NET, CPS, BTOS, and JOLTS in a single ticketed pipeline with full JSON lineage (`intermediate/*run_metadata.json`), with CES used as a contextual payroll series in Section 4.

**Figure discussion.** Figures 1-5 provide the main-text descriptive spine: occupational structure and task-intensity ranking (Figure 1), worker hours and matched-month transitions (Figure 2), business-reported AI adoption and workforce-effect categories (Figure 3), sector labor-demand and payroll context (Figure 4), and cross-source capability boundaries (Figure 5). Visuals: `visuals/png/t001_*.png` through `t010_*.png` per `docs/figure_catalog.md`.

**Identification boundary.** Public files do not support worker-firm linked causal identification of AI impacts at scale.

**Implication.** The contribution is disciplined measurement and a roadmap for survey extensions, not firm-level causal estimates from public data alone.

---

## Section 1 — Occupational baseline (Figure 1; Claim 1)
**Thesis.** A credible AI-and-labor paper must start from official occupational employment, wages, and task structure before interpreting any dynamic evidence.

**Dataset sentence.** Figure 1 combines BLS OEWS national estimates with O*NET Work Activities (Importance) aggregated to the paper’s 22 occupation groups and deterministic AI-relevance terciles (`intermediate/ai_relevance_terciles.csv`).

**Figure discussion.** Panel A reports national employment shares and median annual wages by the 22-group occupation taxonomy. Panel B reports standardized O*NET task intensities and the AI Task Index used for deterministic tercile assignment. This section is descriptive baseline measurement, not causal inference. See `docs/captions/fig01_caption.md` and `docs/figure_memos/fig01.md`.

**Identification boundary.** OEWS and O*NET describe national occupational structure and task content, not realized AI treatment effects; geographic composition is handled separately in the appendix using ACS.

**Implication.** Downstream worker and firm figures use the same tercile partition for consistent grouping.

---

## Section 2 — Worker hours and mobility (Figure 2; Claim 2)
**Thesis.** Monthly CPS public-use microdata support national descriptive monitoring of worker hours and broad occupational and labor-force transitions when matched across adjacent months.

**Dataset sentence.** CPS Basic Monthly files, January 2019 onward, with composite person weights and AI terciles from T-002.

**Figure discussion.** Panel A reports weighted mean usual weekly hours by month and AI-relevance tercile. Panel B combines a latest-month transition-count heatmap with time-series probabilities for retention, occupation switching, unemployment entry, and NILF entry. This section is descriptive matched-month survey monitoring, not causal attribution to AI adoption. See `docs/captions/fig02_caption.md` and `docs/figure_memos/fig02.md`.

**Identification boundary.** Transitions are survey-based constructs, not administrative job-to-job records; national scope only in the main specification.

**Implication.** These series are appropriate for monitoring and for motivating CPS supplement design; they do not identify firm-level AI adoption effects.

---

## Section 3 — Business-side AI adoption (Figure 3; Claim 3)
**Thesis.** Census BTOS publishes high-frequency business-reported AI use and supplement-based workforce-effect shares suitable as the public firm-side benchmark.

**Dataset sentence.** BTOS API national series and the published AI Supplement Table for workforce-effect categories.

**Figure discussion.** Panel A reports national BTOS firm-weighted shares for current and expected AI use by collection period. Panel B reports retained AI-supplement workforce-effect categories. Employment-effect rows are directly published, while task-effect interpretation remains proxy-based when item-25 option rows are not publicly tabulated. This section is descriptive business-reported evidence, not linked worker-level causal analysis. See `docs/captions/fig03_caption.md`, `docs/source_notes/fig03_sources.md`, and `README.md` Known Deviations.

**Identification boundary.** Business surveys do not link to worker microdata in public release.

**Implication.** BTOS should be central in any public-data monitoring stack alongside CPS, with minimal high-yield additions that preserve burden constraints.

---

## Section 4 — Labor demand and payroll context (Figure 4; Claim 4)
**Thesis.** JOLTS and CES provide official labor-demand and payroll context for selected comparison sectors, even though public JOLTS is not occupation-resolved.

**Dataset sentence.** BLS LABSTAT JOLTS and CES series mapped through `crosswalks/sector6_crosswalk.csv`.

**Figure discussion.** Panel A reports JOLTS openings, hires, quits, and layoffs/discharges rates by six-sector group. Panel B reports CES payroll employment indexed to 100 in August 2023 for the same sectors. This section is sector-context evidence and does not resolve occupation-level demand measurement. See `docs/captions/fig04_caption.md` and `docs/figure_memos/fig04.md`.

**Identification boundary.** Sector flows cannot substitute for occupation-specific vacancy or hire measurement.

**Implication.** Policy proposals to extend JOLTS should assume coarse occupation groupings or rotating supplements consistent with sample and modeling constraints documented by BLS.

---

## Section 5 — Identification frontier (Figure 5; Claim 5)
**Thesis.** The main structural gap in public measurement is the absence of an integrated worker-firm AI panel.

**Dataset sentence.** Figure 5 is a non-estimated synthesis coded from `docs/lineage/t010_paper_notes_matrix.md` and `docs/lineage/t010_issues.md` (T-010 rules; `figures/figure5_capability_matrix.csv`).

**Figure discussion.** The matrix encodes `direct`, `partial`, or `none` support for seven empirical objects across five core datasets as a rule-driven documentation synthesis. It provides an empirical diagnosis of capability boundaries. Any survey-priority recommendation is a policy design judgment rather than a causal estimate. See `docs/captions/fig05_caption.md` and `docs/figure_memos/fig05.md`.

**Identification boundary.** Cells are interpretive documentation, not statistical estimates.

**Implication.** A practical policy design judgment is to prioritize CPS and BTOS modules, scoped JOLTS supplements, and NLS career items over greenfield systems, while reserving linked-administrative ideals for long-run infrastructure discussions.

---

## Conclusion
**Thesis.** U.S. public federal data already support a serious AI-and-labor measurement program when integrated with explicit resolution limits.

**Dataset sentence.** Full reproducibility is defined by `docs/replication.md` and `python scripts/run_full_pipeline_from_raw.py`.

**Figure discussion.** Main-text figures align with Claims 1–5 subject to `docs/claim_audit.md` (Claim 1 in main text is scoped to employment, wages, and task content; geography is appendix evidence).

**Identification boundary.** Public data cannot yet deliver firm-level AI causal attribution at scale.

**Implication.** The marginal policy value is in targeted survey extensions and transparent monitoring, not in pretending the public stack resolves every identification object.

---

## Methods and data reference
Consolidated methods: `docs/methods_data.md`. Registry: `docs/data_registry.csv`.

## Policy and briefing artifacts (repository)

The same pipeline outputs support policy-facing materials that are **additive** to this manuscript: senator memo narrative, frozen Virginia evidence, lineage tables, hearing Q&A, one-page handout, print packet order, and optional memo visuals (`t101`–`t108`) plus Virginia visuals (`va01`–`va08`). Primary entry points: `docs/senate_briefing_memo.md`, `docs/senate_briefing_evidence_baseline_va.md`, `docs/senate_briefing_lineage_va.md`, `docs/senate_briefing_script_va.md`, `docs/senate_briefing_qa_va.md`, `docs/senator_handout_1page_va.md`, `docs/senator_packet_order_va.md`. Technical summary and rebuild commands: `docs/virginia_deep_dive.md`; figure and stem catalog: `docs/figure_catalog.md`; orchestrated build/QA: `scripts/run_memo_visuals_build.py`, `scripts/run_memo_visuals_qa.py` (see `docs/replication.md`). Senator-facing claims are logged in `docs/claim_audit.md` (Senator brief claim ledger). These artifacts are descriptive monitoring support, not causal estimates.

## Appendix
Order and draft paragraphs: `docs/appendix_outline.md`, `docs/appendix_draft.md`.

## Reproducibility and integrity
- Full clean rebuild: `scripts/run_full_clean_rebuild_acceptance.py` (invoked by `run_full_pipeline_from_raw.py`).
- Acceptance matrix: `docs/acceptance_matrix.md`.
- Claim audit: `docs/claim_audit.md`.
- Robustness reports: `scripts/run_robustness_all.py` outputs under `intermediate/robustness/`.
- Results freeze procedure: `docs/release_process.md`; manifest: `scripts/build_freeze_manifest.py`.

The drafting rule for this manuscript is conservative: no invented datasets, no synthetic backfilling, and no claims that exceed the resolution permitted by the underlying public instruments.
