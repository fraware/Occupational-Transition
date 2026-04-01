from __future__ import annotations

from pathlib import Path

from occupational_transition.orchestration import AnalysisBundle, GateStep, PipelineStep


FULL_REBUILD_STEPS: list[PipelineStep] = [
    PipelineStep(
        "PR-000",
        "python scripts/build_crosswalks.py",
        "python scripts/qa_crosswalks.py",
        ("crosswalks/occ22_crosswalk.csv", "crosswalks/sector6_crosswalk.csv", "docs/data_registry.csv"),
    ),
    PipelineStep(
        "T-001",
        "python scripts/build_figure1_panelA.py",
        "python scripts/qa_figure1_panelA.py",
        (
            "figures/figure1_panelA_occ_baseline.csv",
            "intermediate/figure1_panelA_occ_baseline_meta.csv",
            "intermediate/figure1_panelA_run_metadata.json",
        ),
    ),
    PipelineStep(
        "T-002",
        "python scripts/build_figure1_panelB.py",
        "python scripts/qa_figure1_panelB.py",
        (
            "figures/figure1_panelB_task_heatmap.csv",
            "intermediate/ai_relevance_terciles.csv",
            "intermediate/occ22_exposure_components.csv",
            "intermediate/figure1_panelB_meta.csv",
            "intermediate/figure1_panelB_run_metadata.json",
        ),
    ),
    PipelineStep(
        "T-003",
        "python scripts/build_figure2_panelA.py",
        "python scripts/qa_figure2_panelA.py",
        (
            "figures/figure2_panelA_hours_by_ai_tercile.csv",
            "intermediate/figure2_panelA_run_metadata.json",
        ),
    ),
    PipelineStep(
        "T-004",
        "python scripts/build_figure2_panelB_counts.py",
        "python scripts/qa_figure2_panelB_counts.py",
        (
            "figures/figure2_panelB_transition_counts.csv",
            "intermediate/figure2_panelB_counts_run_metadata.json",
            "intermediate/figure2_panelB_attrition_diagnostics.csv",
            "intermediate/figure2_panelB_match_regime_robustness.csv",
            "intermediate/figure2_panelB_missing_month_sensitivity.csv",
        ),
    ),
    PipelineStep(
        "T-005",
        "python scripts/build_figure2_panelB_probs.py",
        "python scripts/qa_figure2_panelB_probs.py",
        (
            "figures/figure2_panelB_transition_probs.csv",
            "intermediate/figure2_panelB_probs_run_metadata.json",
        ),
    ),
    PipelineStep(
        "T-006",
        "python scripts/build_figure3_panelA_btos_ai_trends.py",
        "python scripts/qa_figure3_panelA_btos_ai_trends.py",
        (
            "figures/figure3_panelA_btos_ai_trends.csv",
            "intermediate/figure3_panelA_btos_ai_trends_run_metadata.json",
        ),
    ),
    PipelineStep(
        "T-007",
        "python scripts/build_figure3_panelB_btos_workforce_effects.py",
        "python scripts/qa_figure3_panelB_btos_workforce_effects.py",
        (
            "figures/figure3_panelB_btos_workforce_effects.csv",
            "intermediate/figure3_panelB_btos_workforce_effects_run_metadata.json",
        ),
    ),
    PipelineStep(
        "T-008",
        "python scripts/build_figure4_panelA_jolts_sector_rates.py",
        "python scripts/qa_figure4_panelA_jolts_sector_rates.py",
        (
            "figures/figure4_panelA_jolts_sector_rates.csv",
            "intermediate/figure4_panelA_jolts_sector_rates_run_metadata.json",
        ),
    ),
    PipelineStep(
        "T-009",
        "python scripts/build_figure4_panelB_ces_sector_index.py",
        "python scripts/qa_figure4_panelB_ces_sector_index.py",
        (
            "figures/figure4_panelB_ces_sector_index.csv",
            "intermediate/figure4_panelB_ces_sector_index_run_metadata.json",
        ),
    ),
    PipelineStep(
        "T-010",
        "python scripts/build_figure5_capability_matrix.py",
        "python scripts/qa_figure5_capability_matrix.py",
        (
            "figures/figure5_capability_matrix.csv",
            "intermediate/figure5_capability_matrix_run_metadata.json",
        ),
    ),
    PipelineStep(
        "T-011",
        "python scripts/build_figureA1_asec_welfare_by_ai_tercile.py",
        "python scripts/qa_figureA1_asec_welfare_by_ai_tercile.py",
        (
            "figures/figureA1_asec_welfare_by_ai_tercile.csv",
            "intermediate/figureA1_asec_welfare_by_ai_tercile_run_metadata.json",
        ),
    ),
    PipelineStep(
        "T-012",
        "python scripts/build_figureA2_sipp_event_study.py",
        "python scripts/qa_figureA2_sipp_event_study.py",
        (
            "figures/figureA2_sipp_event_study.csv",
            "intermediate/figureA2_sipp_event_study_run_metadata.json",
        ),
    ),
    PipelineStep(
        "T-013",
        "python scripts/build_figureA3_cps_supp_validation.py",
        "python scripts/qa_figureA3_cps_supp_validation.py",
        (
            "figures/figureA3_cps_supp_validation.csv",
            "intermediate/figureA3_cps_supp_validation_run_metadata.json",
        ),
    ),
    PipelineStep(
        "T-014",
        "python scripts/build_figureA4_abs_structural_adoption.py",
        "python scripts/qa_figureA4_abs_structural_adoption.py",
        (
            "figures/figureA4_abs_structural_adoption.csv",
            "intermediate/figureA4_abs_structural_adoption_run_metadata.json",
        ),
    ),
    PipelineStep(
        "T-015",
        "python scripts/build_figureA5_ces_payroll_hours.py",
        "python scripts/qa_figureA5_ces_payroll_hours.py",
        (
            "figures/figureA5_ces_payroll_hours.csv",
            "intermediate/figureA5_ces_payroll_hours_run_metadata.json",
        ),
    ),
    PipelineStep(
        "T-016",
        "python scripts/build_figureA6_bed_churn.py",
        "python scripts/qa_figureA6_bed_churn.py",
        (
            "figures/figureA6_bed_churn.csv",
            "intermediate/figureA6_bed_churn_run_metadata.json",
        ),
    ),
    PipelineStep(
        "T-017",
        "python scripts/build_figureA7_qcew_state_benchmark.py",
        "python scripts/qa_figureA7_qcew_state_benchmark.py",
        (
            "figures/figureA7_qcew_state_benchmark.csv",
            "intermediate/figureA7_qcew_state_benchmark_run_metadata.json",
        ),
    ),
    PipelineStep(
        "T-018",
        "python scripts/build_figureA8_lehd_benchmark.py",
        "python scripts/qa_figureA8_lehd_benchmark.py",
        (
            "figures/figureA8_lehd_benchmark.csv",
            "intermediate/figureA8_lehd_benchmark_run_metadata.json",
        ),
    ),
    PipelineStep(
        "T-019",
        "python scripts/build_figureA9_acs_local_composition.py",
        "python scripts/qa_figureA9_acs_local_composition.py",
        (
            "figures/figureA9_acs_local_composition.csv",
            "intermediate/figureA9_acs_local_composition_run_metadata.json",
        ),
    ),
    PipelineStep(
        "T-020",
        "python scripts/build_figureA10_nls_longrun.py",
        "python scripts/qa_figureA10_nls_longrun.py",
        (
            "figures/figureA10_nls_longrun.csv",
            "intermediate/figureA10_nls_longrun_run_metadata.json",
        ),
    ),
    PipelineStep(
        "T-021",
        "python scripts/build_occ22_sector_weights.py",
        "python scripts/qa_occ22_sector_weights.py",
        (
            "intermediate/occ22_sector_weights.csv",
            "intermediate/occ22_sector_weights_run_metadata.json",
        ),
    ),
    PipelineStep(
        "T-022",
        "python scripts/build_btos_sector_ai_use_monthly.py",
        "python scripts/qa_btos_sector_ai_use_monthly.py",
        (
            "intermediate/btos_sector_ai_use_monthly.csv",
            "intermediate/btos_sector_ai_use_monthly_run_metadata.json",
        ),
    ),
    PipelineStep(
        "T-023",
        "python scripts/build_awes_occ22_monthly.py",
        "python scripts/qa_awes_occ22_monthly.py",
        ("metrics/awes_occ22_monthly.csv", "intermediate/awes_run_metadata.json"),
    ),
    PipelineStep(
        "T-024",
        "python scripts/build_sector6_stress_monthly.py",
        "python scripts/qa_sector6_stress_monthly.py",
        (
            "intermediate/sector6_stress_monthly.csv",
            "intermediate/sector6_stress_monthly_run_metadata.json",
        ),
    ),
    PipelineStep(
        "T-025",
        "python scripts/build_cps_occ22_exit_risk_monthly.py",
        "python scripts/qa_cps_occ22_exit_risk_monthly.py",
        (
            "intermediate/cps_occ22_exit_risk_monthly.csv",
            "intermediate/cps_occ22_exit_risk_monthly_run_metadata.json",
        ),
    ),
    PipelineStep(
        "T-026",
        "python scripts/build_alpi_occ22_monthly.py",
        "python scripts/qa_alpi_occ22_monthly.py",
        ("metrics/alpi_occ22_monthly.csv", "intermediate/alpi_run_metadata.json"),
    ),
]

CORE_POST_GATES: list[GateStep] = [
    GateStep("Robustness suite", "python scripts/run_robustness_all.py"),
    GateStep("Freeze manifest build", "python scripts/build_freeze_manifest.py"),
    GateStep("Freeze manifest QA", "python scripts/qa_freeze_manifest.py"),
    GateStep("Drift dashboard build", "python scripts/build_drift_dashboard.py"),
    GateStep("Drift dashboard QA", "python scripts/qa_drift_dashboard.py"),
]

OPTIONAL_MEMO_GATES: list[GateStep] = [
    GateStep("Policy visuals build", "python scripts/run_memo_visuals_build.py"),
    GateStep("Policy visuals QA", "python scripts/run_memo_visuals_qa.py"),
]

ANALYSIS_BUNDLES: list[AnalysisBundle] = [
    AnalysisBundle(
        name="quick-start",
        description="Main text baseline and core dynamics (T-001 to T-008).",
        tickets=tuple([f"T-{i:03d}" for i in range(1, 9)]),
    ),
    AnalysisBundle(
        name="core-paper",
        description="All main text figures (T-001 to T-010).",
        tickets=tuple([f"T-{i:03d}" for i in range(1, 11)]),
    ),
    AnalysisBundle(
        name="full-replication",
        description="Full strict rebuild (PR-000 and T-001 to T-026).",
        tickets=("PR-000",) + tuple([f"T-{i:03d}" for i in range(1, 27)]),
    ),
    AnalysisBundle(
        name="release-signoff",
        description="Full replication with release gates and optional signoff checks.",
        tickets=("PR-000",) + tuple([f"T-{i:03d}" for i in range(1, 27)]),
    ),
]


def selectable_steps(bundle: str | None, selected_tickets: list[str] | None) -> list[PipelineStep]:
    if selected_tickets:
        wanted = set(selected_tickets)
        return [s for s in FULL_REBUILD_STEPS if s.ticket in wanted]

    if bundle:
        bundle_map = {b.name: b for b in ANALYSIS_BUNDLES}
        b = bundle_map.get(bundle)
        if b is None:
            raise ValueError(f"Unknown bundle: {bundle}")
        wanted = set(b.tickets)
        return [s for s in FULL_REBUILD_STEPS if s.ticket in wanted]

    return list(FULL_REBUILD_STEPS)


def post_gates(root: Path) -> list[GateStep]:
    gates: list[GateStep] = []
    if (root / "scripts" / "run_memo_visuals_build.py").is_file():
        gates.extend(OPTIONAL_MEMO_GATES)
    gates.extend(CORE_POST_GATES)
    return gates


def list_sources() -> list[dict[str, str]]:
    return [
        {"source": "BLS_OEWS", "mode_hint": "Pinned in T-001 (May 2024 national)."},
        {"source": "O*NET", "mode_hint": "Crosswalk/task metadata used in T-002."},
        {"source": "CPS", "mode_hint": "Rolling public-use microdata for worker-side analyses."},
        {"source": "BTOS", "mode_hint": "Census business-side AI adoption and supplement effects."},
        {"source": "JOLTS", "mode_hint": "LABSTAT rates by selected sectors."},
        {"source": "CES", "mode_hint": "Sector payroll context for Figure 4 panel B."},
        {"source": "ABS/ASEC/SIPP/LEHD/NLS", "mode_hint": "Appendix and robustness ticket families."},
    ]
