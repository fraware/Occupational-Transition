from __future__ import annotations

from pathlib import Path

from occupational_transition.orchestration import AnalysisBundle, GateStep, PipelineStep


FULL_REBUILD_STEPS: list[PipelineStep] = [
    PipelineStep(
        "PR-000",
        "python -m occupational_transition.run_step build PR-000",
        "python -m occupational_transition.run_step qa PR-000",
        ("crosswalks/occ22_crosswalk.csv", "crosswalks/sector6_crosswalk.csv", "docs/data_registry.csv"),
        build_module="occupational_transition.pipelines.pr000_crosswalks:run",
        qa_module="occupational_transition.qa.crosswalks:main",
    ),
    PipelineStep(
        "T-001",
        "python -m occupational_transition.run_step build T-001",
        "python -m occupational_transition.run_step qa T-001",
        (
            "figures/figure1_panelA_occ_baseline.csv",
            "intermediate/figure1_panelA_occ_baseline_meta.csv",
            "intermediate/figure1_panelA_run_metadata.json",
        ),
        build_module="occupational_transition.pipelines.figure1_panelA_t001:run",
        qa_module="occupational_transition.qa.figure1_panelA:main",
    ),
    PipelineStep(
        "T-002",
        "python -m occupational_transition.run_step build T-002",
        "python -m occupational_transition.run_step qa T-002",
        (
            "figures/figure1_panelB_task_heatmap.csv",
            "intermediate/ai_relevance_terciles.csv",
            "intermediate/occ22_exposure_components.csv",
            "intermediate/figure1_panelB_meta.csv",
            "intermediate/figure1_panelB_run_metadata.json",
        ),
        build_module="occupational_transition.pipelines.figure1_panelB_t002:run",
        qa_module="occupational_transition.qa.figure1_panelB:main",
    ),
    PipelineStep(
        "T-003",
        "python -m occupational_transition.run_step build T-003",
        "python -m occupational_transition.run_step qa T-003",
        (
            "figures/figure2_panelA_hours_by_ai_tercile.csv",
            "intermediate/figure2_panelA_run_metadata.json",
        ),
        build_module="occupational_transition.pipelines.figure2_panelA_t003:run",
        qa_module="occupational_transition.qa.figure2_panelA_t003:main",
    ),
    PipelineStep(
        "T-004",
        "python -m occupational_transition.run_step build T-004",
        "python -m occupational_transition.run_step qa T-004",
        (
            "figures/figure2_panelB_transition_counts.csv",
            "intermediate/figure2_panelB_counts_run_metadata.json",
            "intermediate/figure2_panelB_attrition_diagnostics.csv",
            "intermediate/figure2_panelB_match_regime_robustness.csv",
            "intermediate/figure2_panelB_missing_month_sensitivity.csv",
        ),
        build_module="occupational_transition.pipelines.figure2_panelB_counts_t004:run",
        qa_module="occupational_transition.qa.figure2_panelB_counts_t004:main",
    ),
    PipelineStep(
        "T-005",
        "python -m occupational_transition.run_step build T-005",
        "python -m occupational_transition.run_step qa T-005",
        (
            "figures/figure2_panelB_transition_probs.csv",
            "intermediate/figure2_panelB_probs_run_metadata.json",
        ),
        build_module="occupational_transition.pipelines.figure2_panelB_probs_t005:run",
        qa_module="occupational_transition.qa.figure2_panelB_probs_t005:main",
    ),
    PipelineStep(
        "T-006",
        "python -m occupational_transition.run_step build T-006",
        "python -m occupational_transition.run_step qa T-006",
        (
            "figures/figure3_panelA_btos_ai_trends.csv",
            "intermediate/figure3_panelA_btos_ai_trends_run_metadata.json",
        ),
        build_module="occupational_transition.pipelines.figure3_panelA_t006:run",
        qa_module="occupational_transition.qa.figure3_panelA_t006:main",
    ),
    PipelineStep(
        "T-007",
        "python -m occupational_transition.run_step build T-007",
        "python -m occupational_transition.run_step qa T-007",
        (
            "figures/figure3_panelB_btos_workforce_effects.csv",
            "intermediate/figure3_panelB_btos_workforce_effects_run_metadata.json",
        ),
        build_module="occupational_transition.pipelines.figure3_panelB_t007:run",
        qa_module="occupational_transition.qa.figure3_panelB_t007:main",
    ),
    PipelineStep(
        "T-008",
        "python -m occupational_transition.run_step build T-008",
        "python -m occupational_transition.run_step qa T-008",
        (
            "figures/figure4_panelA_jolts_sector_rates.csv",
            "intermediate/figure4_panelA_jolts_sector_rates_run_metadata.json",
        ),
        build_module="occupational_transition.pipelines.figure4_panelA_t008:run",
        qa_module="occupational_transition.qa.figure4_panelA_t008:main",
    ),
    PipelineStep(
        "T-009",
        "python -m occupational_transition.run_step build T-009",
        "python -m occupational_transition.run_step qa T-009",
        (
            "figures/figure4_panelB_ces_sector_index.csv",
            "intermediate/figure4_panelB_ces_sector_index_run_metadata.json",
        ),
        build_module="occupational_transition.pipelines.figure4_panelB_t009:run",
        qa_module="occupational_transition.qa.figure4_panelB_t009:main",
    ),
    PipelineStep(
        "T-010",
        "python -m occupational_transition.run_step build T-010",
        "python -m occupational_transition.run_step qa T-010",
        (
            "figures/figure5_capability_matrix.csv",
            "intermediate/figure5_capability_matrix_run_metadata.json",
        ),
        build_module="occupational_transition.pipelines.figure5_capability_t010:run",
        qa_module="occupational_transition.qa.figure5_capability_t010:main",
    ),
    PipelineStep(
        "T-011",
        "python -m occupational_transition.run_step build T-011",
        "python -m occupational_transition.run_step qa T-011",
        (
            "figures/figureA1_asec_welfare_by_ai_tercile.csv",
            "intermediate/figureA1_asec_welfare_by_ai_tercile_run_metadata.json",
        ),
        build_module="occupational_transition.pipelines.figureA1_t011:run",
        qa_module="occupational_transition.qa.figureA1_t011:main",
    ),
    PipelineStep(
        "T-012",
        "python -m occupational_transition.run_step build T-012",
        "python -m occupational_transition.run_step qa T-012",
        (
            "figures/figureA2_sipp_event_study.csv",
            "intermediate/figureA2_sipp_event_study_run_metadata.json",
        ),
        build_module="occupational_transition.pipelines.figureA2_t012:run",
        qa_module="occupational_transition.qa.figureA2_t012:main",
    ),
    PipelineStep(
        "T-013",
        "python -m occupational_transition.run_step build T-013",
        "python -m occupational_transition.run_step qa T-013",
        (
            "figures/figureA3_cps_supp_validation.csv",
            "intermediate/figureA3_cps_supp_validation_run_metadata.json",
        ),
        build_module="occupational_transition.pipelines.figureA3_t013:run",
        qa_module="occupational_transition.qa.figureA3_t013:main",
    ),
    PipelineStep(
        "T-014",
        "python -m occupational_transition.run_step build T-014",
        "python -m occupational_transition.run_step qa T-014",
        (
            "figures/figureA4_abs_structural_adoption.csv",
            "intermediate/figureA4_abs_structural_adoption_run_metadata.json",
        ),
        build_module="occupational_transition.pipelines.figureA4_t014:run",
        qa_module="occupational_transition.qa.figureA4_t014:main",
    ),
    PipelineStep(
        "T-015",
        "python -m occupational_transition.run_step build T-015",
        "python -m occupational_transition.run_step qa T-015",
        (
            "figures/figureA5_ces_payroll_hours.csv",
            "intermediate/figureA5_ces_payroll_hours_run_metadata.json",
        ),
        build_module="occupational_transition.pipelines.figureA5_t015:run",
        qa_module="occupational_transition.qa.figureA5_t015:main",
    ),
    PipelineStep(
        "T-016",
        "python -m occupational_transition.run_step build T-016",
        "python -m occupational_transition.run_step qa T-016",
        (
            "figures/figureA6_bed_churn.csv",
            "intermediate/figureA6_bed_churn_run_metadata.json",
        ),
        build_module="occupational_transition.pipelines.figureA6_t016:run",
        qa_module="occupational_transition.qa.figureA6_t016:main",
    ),
    PipelineStep(
        "T-017",
        "python -m occupational_transition.run_step build T-017",
        "python -m occupational_transition.run_step qa T-017",
        (
            "figures/figureA7_qcew_state_benchmark.csv",
            "intermediate/figureA7_qcew_state_benchmark_run_metadata.json",
        ),
        build_module="occupational_transition.pipelines.figureA7_t017:run",
        qa_module="occupational_transition.qa.figureA7_t017:main",
    ),
    PipelineStep(
        "T-018",
        "python -m occupational_transition.run_step build T-018",
        "python -m occupational_transition.run_step qa T-018",
        (
            "figures/figureA8_lehd_benchmark.csv",
            "intermediate/figureA8_lehd_benchmark_run_metadata.json",
        ),
        build_module="occupational_transition.pipelines.figureA8_t018:run",
        qa_module="occupational_transition.qa.figureA8_t018:main",
    ),
    PipelineStep(
        "T-019",
        "python -m occupational_transition.run_step build T-019",
        "python -m occupational_transition.run_step qa T-019",
        (
            "figures/figureA9_acs_local_composition.csv",
            "intermediate/figureA9_acs_local_composition_run_metadata.json",
        ),
        build_module="occupational_transition.pipelines.figureA9_t019:run",
        qa_module="occupational_transition.qa.figureA9_t019:main",
    ),
    PipelineStep(
        "T-020",
        "python -m occupational_transition.run_step build T-020",
        "python -m occupational_transition.run_step qa T-020",
        (
            "figures/figureA10_nls_longrun.csv",
            "intermediate/figureA10_nls_longrun_run_metadata.json",
        ),
        build_module="occupational_transition.pipelines.figureA10_t020:run",
        qa_module="occupational_transition.qa.figureA10_t020:main",
    ),
    PipelineStep(
        "T-021",
        "python -m occupational_transition.run_step build T-021",
        "python -m occupational_transition.run_step qa T-021",
        (
            "intermediate/occ22_sector_weights.csv",
            "intermediate/occ22_sector_weights_run_metadata.json",
        ),
        build_module="occupational_transition.pipelines.occ22_sector_weights_t021:run",
        qa_module="occupational_transition.qa.occ22_sector_weights_t021:main",
    ),
    PipelineStep(
        "T-022",
        "python -m occupational_transition.run_step build T-022",
        "python -m occupational_transition.run_step qa T-022",
        (
            "intermediate/btos_sector_ai_use_monthly.csv",
            "intermediate/btos_sector_ai_use_monthly_run_metadata.json",
        ),
        build_module="occupational_transition.pipelines.btos_sector_ai_use_t022:run",
        qa_module="occupational_transition.qa.btos_sector_ai_use_t022:main",
    ),
    PipelineStep(
        "T-023",
        "python -m occupational_transition.run_step build T-023",
        "python -m occupational_transition.run_step qa T-023",
        ("metrics/awes_occ22_monthly.csv", "intermediate/awes_run_metadata.json"),
        build_module="occupational_transition.pipelines.awes_occ22_monthly_t023:run",
        qa_module="occupational_transition.qa.awes_occ22_monthly_t023:main",
    ),
    PipelineStep(
        "T-024",
        "python -m occupational_transition.run_step build T-024",
        "python -m occupational_transition.run_step qa T-024",
        (
            "intermediate/sector6_stress_monthly.csv",
            "intermediate/sector6_stress_monthly_run_metadata.json",
        ),
        build_module="occupational_transition.pipelines.sector6_stress_monthly_t024:run",
        qa_module="occupational_transition.qa.sector6_stress_monthly_t024:main",
    ),
    PipelineStep(
        "T-025",
        "python -m occupational_transition.run_step build T-025",
        "python -m occupational_transition.run_step qa T-025",
        (
            "intermediate/cps_occ22_exit_risk_monthly.csv",
            "intermediate/cps_occ22_exit_risk_monthly_run_metadata.json",
        ),
        build_module="occupational_transition.pipelines.cps_occ22_exit_risk_t025:run",
        qa_module="occupational_transition.qa.cps_occ22_exit_risk_t025:main",
    ),
    PipelineStep(
        "T-026",
        "python -m occupational_transition.run_step build T-026",
        "python -m occupational_transition.run_step qa T-026",
        ("metrics/alpi_occ22_monthly.csv", "intermediate/alpi_run_metadata.json"),
        build_module="occupational_transition.pipelines.alpi_occ22_monthly_t026:run",
        qa_module="occupational_transition.qa.alpi_occ22_monthly_t026:main",
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
        {
            "source": "catalog",
            "mode_hint": "Run `ot catalog` on docs/data_registry.csv rows (program, cadence, extractor).",
        },
        {"source": "BLS_OEWS", "mode_hint": "Pinned in T-001 (May 2024 national)."},
        {"source": "O*NET", "mode_hint": "Crosswalk/task metadata used in T-002."},
        {"source": "CPS", "mode_hint": "Rolling public-use microdata for worker-side analyses."},
        {"source": "BTOS", "mode_hint": "Census business-side AI adoption and supplement effects."},
        {"source": "JOLTS", "mode_hint": "LABSTAT rates by selected sectors."},
        {"source": "CES", "mode_hint": "Sector payroll context for Figure 4 panel B."},
        {"source": "ABS/ASEC/SIPP/LEHD/NLS", "mode_hint": "Appendix and robustness ticket families."},
    ]
