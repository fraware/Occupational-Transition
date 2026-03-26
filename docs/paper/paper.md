# What U.S. Public Federal Data Can and Cannot Say About AI and Labor

## Subtitle

What Exists, What Works, and What Small Survey Changes Would Unlock

---

## Manuscript status and evidence alignment

This file is the publication manuscript for the repository's empirical stack. Quantitative claims should be read as valid for one coordinated frozen run.

Evidence-tagging rules are in [evidence_snapshot.md](evidence_snapshot.md). Replication and freeze procedures are in [../replication/README.md](../replication/README.md) and [../replication/project_maintenance.md](../replication/project_maintenance.md#results-freeze-and-tagging).

The current draft aligns with commit `72f02bf2e7897f5515ab9212f9e6fe6fbcd2c432` (short `72f02bf`). Replace this with the final release tag before circulation.

---

## Abstract

Debates over AI and labor market change have outpaced the federal public measurement system. This paper develops a reproducible public-data framework that integrates occupational structure and tasks, worker outcomes and transitions, business-reported AI adoption, sector labor-demand context, and explicit cross-source capability limits.

The framework yields three descriptive findings from frozen outputs. First, AI-relevance groups differ materially in worker outcomes: in early 2026 CPS data, high- and low-AI-relevance terciles differ by roughly four weekly hours (`figures/figure2_panelA_hours_by_ai_tercile.csv`). Second, business-reported AI use in BTOS reaches the mid-20 percent range in recent periods (`figures/figure3_panelA_btos_ai_trends.csv`). Third, labor-demand conditions differ across sectors: January 2026 job-opening rates differ by nearly two percentage points across the six comparison sectors (`figures/figure4_panelA_jolts_sector_rates.csv`).

The framework also identifies hard boundaries. The capability matrix (`figures/figure5_capability_matrix.csv`) shows that no core source in this stack supports direct worker-firm AI linkage. As a result, high-confidence firm-level causal attribution remains outside the scope of current public files. The policy implication is incremental: prioritize targeted survey upgrades in CPS, BTOS, scoped JOLTS supplements, and longitudinal pathways, while using the existing public stack for transparent monitoring.

---

## 1. Introduction

Public concern about AI and work has intensified, but measurement often lags rhetoric. Claims about displacement, augmentation, and wage pressure are now common, yet many are not anchored to reproducible public evidence. This paper asks a narrower question: what can U.S. federal public data already measure with discipline, and where are the non-negotiable limits?

Our answer is based on an integrated empirical system rather than stand-alone tables. We combine OEWS, O*NET, CPS, BTOS, JOLTS, and CES context in one reproducible workflow with explicit metadata and quality checks. This design produces a common language of evidence across figures and supports consistent claim discipline.

The boundary condition is explicit. Current public files do not provide an integrated worker-firm AI panel at national scale. We therefore focus on descriptive measurement and survey design priorities, not on treatment-effect identification that the data cannot support.

The paper contributes two outputs. First, it provides a transparent monitoring spine for researchers and policy teams. Second, it provides a survey-priority roadmap focused on marginal information gain per respondent burden.

---

## 2. Occupational baseline and task structure (Figure 1; Claim 1)

The analysis begins with a national baseline because dynamic interpretation is credible only when occupational composition and task structure are clearly defined.

Figure 1 Panel A reports national employment shares and median annual wages across 22 occupation groups (`figures/figure1_panelA_occ_baseline.csv`). Employment is concentrated: Office and Administrative Support is about 11.8 percent, Transportation and Material Moving about 8.9 percent, and Food Preparation and Serving about 8.8 percent. Median annual wages span roughly $34k to $121k across groups.

Panel B reports standardized task intensities and the AI Task Index used for deterministic tercile assignment (`figures/figure1_panelB_task_heatmap.csv`; build-generated terciles in `intermediate/ai_relevance_terciles.csv`). The index is a descriptive grouping instrument, not a treatment variable.

Interpretation is intentionally narrow. Figure 1 supports national descriptive statements about occupational structure, wages, and task content. It does not support causal AI-impact claims and does not replace geographic decomposition, which is handled in appendix evidence.

---

## 3. Worker hours and mobility (Figure 2; Claim 2)

Figure 2 evaluates what monthly CPS public-use microdata can support for descriptive monitoring when respondents are matched across adjacent months.

Panel A reports weighted mean usual weekly hours by month and AI-relevance tercile (`figures/figure2_panelA_hours_by_ai_tercile.csv`). In 2026-01, the high tercile averages about 40.4 hours, compared with 37.4 in the middle and 36.3 in the low tercile, for a high-low gap of roughly four hours.

Panel B combines transition counts and summary probabilities from the same CPS transition machinery (`figures/figure2_panelB_transition_counts.csv`, `figures/figure2_panelB_transition_probs.csv`). Supporting aggregates in `figures/memo_dashboard_kpis.csv` place unemployment-entry and NILF-entry rates near 0.7 percent and 1.6 percent for high-origin mass in the referenced window.

These are survey-based descriptive constructs. They are suitable for monitoring broad labor-market movement by AI-relevance groups, but they do not identify firm adoption channels or treatment effects.

---

## 4. Business-side AI adoption (Figure 3; Claim 3)

Figure 3 introduces business-side evidence from Census BTOS.

Panel A tracks national firm-weighted current and expected AI use over collection periods (`figures/figure3_panelA_btos_ai_trends.csv`). In recent periods, current AI-use shares reach the mid-20 percent range.

Panel B summarizes retained workforce-effect categories from the BTOS supplement (`figures/figure3_panelB_btos_workforce_effects.csv`). Employment-effect rows are directly published. Selected task-effect rows require explicit proxy language when fine-grained public tabulations are unavailable. This distinction should be maintained in manuscript prose, captions, and policy outputs.

Figure 3 therefore provides a credible descriptive business benchmark. It does not link firms to workers and cannot, on its own, support worker-level causal attribution.

---

## 5. Labor demand and payroll context (Figure 4; Claim 4)

Figure 4 provides official sector labor-demand context. JOLTS and CES series are mapped to six comparison sectors through `crosswalks/sector6_crosswalk.csv`.

In January 2026, JOLTS job-opening rates range from about 3.8 percent to 5.6 percent across sectors (`figures/figure4_panelA_jolts_sector_rates.csv`), a spread of roughly 1.8 percentage points. CES payroll employment indexed to August 2023 spans roughly 94.7 to 108.7 in the same month (`figures/figure4_panelB_ces_sector_index.csv`).

These patterns are informative for sector context and comparative pressure. They do not resolve occupation-level demand mechanisms.

---

## 6. Identification frontier (Figure 5; Claim 5)

Figure 5 is a rule-based synthesis, not a statistical estimate. It records whether each core source provides direct, partial, or no support for seven measurement objects (`figures/figure5_capability_matrix.csv`), using locked rules in `docs/lineage/`.

The central empirical boundary is clear: worker-firm AI linkage is unsupported across all five core sources in the stack. The matrix also identifies concrete strengths: CPS for worker outcomes and transitions, BTOS for firm AI adoption, JOLTS for labor-demand turnover context, OEWS for occupational structure and wages, and O*NET for task-exposure mechanisms.

This distinction matters for inference. The matrix is an empirical diagnosis of capability boundaries. Policy recommendations that follow are design judgments, not estimated treatment effects.

---

## 7. Optional monitoring indices (AWES and ALPI)

The extended workflow produces AWES and ALPI in `metrics/` as occupation-time monitoring composites. These indices are descriptive by design. They do not replace the frozen AI-relevance tercile framework and should not be interpreted causally.

Definitions and limitations are documented in [methods_data.md](methods_data.md).

---

## 8. Methods and data (condensed)

The empirical design is descriptive and reproducible: official weights where applicable, frozen crosswalks, explicit build and QA scripts, and machine-readable run metadata (`intermediate/*_run_metadata.json`). Source URLs and snapshot fields are maintained in [data_registry.csv](../data_registry.csv).

Full construction detail (universes, windows, and assumptions) is in [methods_data.md](methods_data.md) and `docs/methodology/tickets/`.

Replication procedures and run controls are in [../replication/README.md](../replication/README.md) and [../replication/acceptance_matrix.md](../replication/acceptance_matrix.md).

---

## 9. Conclusion

U.S. public federal data already support a serious AI-and-labor measurement program when used with explicit limits. The integrated evidence shows persistent differences in occupational structure and worker outcomes by AI-relevance group, measurable business-reported adoption dynamics, and meaningful sector-demand dispersion.

The same evidence defines a hard boundary: current public files do not provide the linked worker-firm AI information required for high-confidence causal attribution at scale. That boundary should be treated as a design fact, not a rhetorical inconvenience.

The practical path forward is incremental and high-yield: strengthen CPS and BTOS modules, add scoped JOLTS enhancements where feasible, and preserve longitudinal channels for career dynamics. Within those limits, the current public stack is already strong enough for transparent monitoring and policy-relevant descriptive analysis.

---

## Appendix and companion materials

- Appendix prose and order: [appendix_draft.md](appendix_draft.md)
- Methods and data narrative: [methods_data.md](methods_data.md)
- Claim audit: [../policy/claim_audit.md](../policy/claim_audit.md)
- Figure catalog and notes: [../figures/figure_catalog.md](../figures/figure_catalog.md)
- Replication and run controls: [../replication/README.md](../replication/README.md)

Policy and briefing materials under `docs/policy/briefing/` are additive descriptive outputs and should not be interpreted as causal evidence.

---

## Reproducibility gate before publication

- Confirm that all numeric statements match one frozen run window.
- Verify that dependent Figure 2 transition artifacts are internally aligned within that same run.
- Record and cite the final commit or release tag, and archive the acceptance log with release materials.
