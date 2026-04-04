"""Unified build/QA entrypoint via ``python -m occupational_transition.run_step``."""

from __future__ import annotations

import argparse
import importlib
from pathlib import Path

from occupational_transition.manifests import FULL_REBUILD_STEPS
from occupational_transition.orchestration import PipelineStep, run_shell
from occupational_transition.paths import repo_root

# Fallback shell commands when build_module / qa_module are unset on PipelineStep.
LEGACY_BUILD_CMDS: dict[str, str] = {
    "PR-000": "python scripts/build_crosswalks.py",
    "T-001": "python scripts/build_figure1_panelA.py",
    "T-002": "python scripts/build_figure1_panelB.py",
    "T-003": "python scripts/build_figure2_panelA.py",
    "T-004": "python scripts/build_figure2_panelB_counts.py",
    "T-005": "python scripts/build_figure2_panelB_probs.py",
    "T-006": "python scripts/build_figure3_panelA_btos_ai_trends.py",
    "T-007": "python scripts/build_figure3_panelB_btos_workforce_effects.py",
    "T-008": "python scripts/build_figure4_panelA_jolts_sector_rates.py",
    "T-009": "python scripts/build_figure4_panelB_ces_sector_index.py",
    "T-010": "python scripts/build_figure5_capability_matrix.py",
    "T-011": "python scripts/build_figureA1_asec_welfare_by_ai_tercile.py",
    "T-012": "python scripts/build_figureA2_sipp_event_study.py",
    "T-013": "python scripts/build_figureA3_cps_supp_validation.py",
    "T-014": "python scripts/build_figureA4_abs_structural_adoption.py",
    "T-015": "python scripts/build_figureA5_ces_payroll_hours.py",
    "T-016": "python scripts/build_figureA6_bed_churn.py",
    "T-017": "python scripts/build_figureA7_qcew_state_benchmark.py",
    "T-018": "python scripts/build_figureA8_lehd_benchmark.py",
    "T-019": "python scripts/build_figureA9_acs_local_composition.py",
    "T-020": "python scripts/build_figureA10_nls_longrun.py",
    "T-021": "python scripts/build_occ22_sector_weights.py",
    "T-022": "python scripts/build_btos_sector_ai_use_monthly.py",
    "T-023": "python scripts/build_awes_occ22_monthly.py",
    "T-024": "python scripts/build_sector6_stress_monthly.py",
    "T-025": "python scripts/build_cps_occ22_exit_risk_monthly.py",
    "T-026": "python scripts/build_alpi_occ22_monthly.py",
}

LEGACY_QA_CMDS: dict[str, str] = {
    "PR-000": "python scripts/qa_crosswalks.py",
    "T-001": "python scripts/qa_figure1_panelA.py",
    "T-002": "python scripts/qa_figure1_panelB.py",
    "T-003": "python scripts/qa_figure2_panelA.py",
    "T-004": "python scripts/qa_figure2_panelB_counts.py",
    "T-005": "python scripts/qa_figure2_panelB_probs.py",
    "T-006": "python scripts/qa_figure3_panelA_btos_ai_trends.py",
    "T-007": "python scripts/qa_figure3_panelB_btos_workforce_effects.py",
    "T-008": "python scripts/qa_figure4_panelA_jolts_sector_rates.py",
    "T-009": "python scripts/qa_figure4_panelB_ces_sector_index.py",
    "T-010": "python scripts/qa_figure5_capability_matrix.py",
    "T-011": "python scripts/qa_figureA1_asec_welfare_by_ai_tercile.py",
    "T-012": "python scripts/qa_figureA2_sipp_event_study.py",
    "T-013": "python scripts/qa_figureA3_cps_supp_validation.py",
    "T-014": "python scripts/qa_figureA4_abs_structural_adoption.py",
    "T-015": "python scripts/qa_figureA5_ces_payroll_hours.py",
    "T-016": "python scripts/qa_figureA6_bed_churn.py",
    "T-017": "python scripts/qa_figureA7_qcew_state_benchmark.py",
    "T-018": "python scripts/qa_figureA8_lehd_benchmark.py",
    "T-019": "python scripts/qa_figureA9_acs_local_composition.py",
    "T-020": "python scripts/qa_figureA10_nls_longrun.py",
    "T-021": "python scripts/qa_occ22_sector_weights.py",
    "T-022": "python scripts/qa_btos_sector_ai_use_monthly.py",
    "T-023": "python scripts/qa_awes_occ22_monthly.py",
    "T-024": "python scripts/qa_sector6_stress_monthly.py",
    "T-025": "python scripts/qa_cps_occ22_exit_risk_monthly.py",
    "T-026": "python scripts/qa_alpi_occ22_monthly.py",
}


def _step(ticket: str) -> PipelineStep:
    for s in FULL_REBUILD_STEPS:
        if s.ticket == ticket:
            return s
    raise SystemExit(f"Unknown ticket: {ticket}")


def _import_callable(spec: str):
    mod_name, _, attr = spec.partition(":")
    if not attr:
        raise ValueError(f"Invalid module spec {spec!r} (expected 'module:attribute')")
    mod = importlib.import_module(mod_name)
    return getattr(mod, attr)


def _coerce_qa_exit_code(result: object, *, spec: str) -> int:
    """Normalize ``main()`` return values for ``run_qa`` (explicit contract)."""
    if result is None:
        return 0
    if isinstance(result, bool):
        raise TypeError(
            f"QA callable {spec!r} returned bool; use int exit codes "
            "(0 success, non-zero failure)."
        )
    if isinstance(result, int):
        return result
    raise TypeError(
        f"QA callable {spec!r} must return int | None, got {type(result).__name__}"
    )


def run_build(root: Path, ticket: str) -> int:
    step = _step(ticket)
    if step.build_module:
        fn = _import_callable(step.build_module)
        fn(root)
        return 0
    cmd = LEGACY_BUILD_CMDS.get(ticket)
    if not cmd:
        raise SystemExit(f"No legacy build command for {ticket}")
    rc, _ = run_shell(root, cmd)
    return rc


def run_qa(root: Path, ticket: str) -> int:
    step = _step(ticket)
    if step.qa_module:
        main_fn = _import_callable(step.qa_module)
        return _coerce_qa_exit_code(main_fn(), spec=step.qa_module)
    cmd = LEGACY_QA_CMDS.get(ticket)
    if not cmd:
        raise SystemExit(f"No legacy QA command for {ticket}")
    rc, _ = run_shell(root, cmd)
    return rc


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run pipeline build or QA for one ticket.",
    )
    parser.add_argument("verb", choices=["build", "qa"])
    parser.add_argument("ticket", help="Ticket id, e.g. PR-000 or T-001")
    args = parser.parse_args()
    root = repo_root()
    if args.verb == "build":
        rc = run_build(root, args.ticket)
    else:
        rc = run_qa(root, args.ticket)
    raise SystemExit(rc)


if __name__ == "__main__":
    main()
