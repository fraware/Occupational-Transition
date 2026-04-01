"""
Run strict ticket-by-ticket rebuild + QA with checkpoints and log.

This script:
- Deletes expected ticket output artifacts before each build step.
- Runs build then QA for PR-000 through T-026 in strict order.
- Writes a timestamped markdown acceptance log under intermediate/.

Usage:
    python scripts/run_full_clean_rebuild_acceptance.py
"""

from __future__ import annotations

import datetime as dt
import os
import subprocess
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INTER = ROOT / "intermediate"


Ticket = tuple[str, str, str, list[str]]
Gate = tuple[str, str]

TICKETS: list[Ticket] = [
    (
        "PR-000",
        "python scripts/build_crosswalks.py",
        "python scripts/qa_crosswalks.py",
        [
            "crosswalks/occ22_crosswalk.csv",
            "crosswalks/sector6_crosswalk.csv",
            "docs/data_registry.csv",
        ],
    ),
    (
        "T-001",
        "python scripts/build_figure1_panelA.py",
        "python scripts/qa_figure1_panelA.py",
        [
            "figures/figure1_panelA_occ_baseline.csv",
            "intermediate/figure1_panelA_occ_baseline_meta.csv",
            "intermediate/figure1_panelA_run_metadata.json",
        ],
    ),
    (
        "T-002",
        "python scripts/build_figure1_panelB.py",
        "python scripts/qa_figure1_panelB.py",
        [
            "figures/figure1_panelB_task_heatmap.csv",
            "intermediate/ai_relevance_terciles.csv",
            "intermediate/occ22_exposure_components.csv",
            "intermediate/figure1_panelB_meta.csv",
            "intermediate/figure1_panelB_run_metadata.json",
        ],
    ),
    (
        "T-003",
        "python scripts/build_figure2_panelA.py",
        "python scripts/qa_figure2_panelA.py",
        [
            "figures/figure2_panelA_hours_by_ai_tercile.csv",
            "intermediate/figure2_panelA_run_metadata.json",
        ],
    ),
    (
        "T-004",
        "python scripts/build_figure2_panelB_counts.py",
        "python scripts/qa_figure2_panelB_counts.py",
        [
            "figures/figure2_panelB_transition_counts.csv",
            "intermediate/figure2_panelB_counts_run_metadata.json",
            "intermediate/figure2_panelB_attrition_diagnostics.csv",
            "intermediate/figure2_panelB_match_regime_robustness.csv",
            "intermediate/figure2_panelB_missing_month_sensitivity.csv",
        ],
    ),
    (
        "T-005",
        "python scripts/build_figure2_panelB_probs.py",
        "python scripts/qa_figure2_panelB_probs.py",
        [
            "figures/figure2_panelB_transition_probs.csv",
            "intermediate/figure2_panelB_probs_run_metadata.json",
        ],
    ),
    (
        "T-006",
        "python scripts/build_figure3_panelA_btos_ai_trends.py",
        "python scripts/qa_figure3_panelA_btos_ai_trends.py",
        [
            "figures/figure3_panelA_btos_ai_trends.csv",
            "intermediate/figure3_panelA_btos_ai_trends_run_metadata.json",
        ],
    ),
    (
        "T-007",
        "python scripts/build_figure3_panelB_btos_workforce_effects.py",
        "python scripts/qa_figure3_panelB_btos_workforce_effects.py",
        [
            "figures/figure3_panelB_btos_workforce_effects.csv",
            (
                "intermediate/"
                "figure3_panelB_btos_workforce_effects_run_metadata.json"
            ),
        ],
    ),
    (
        "T-008",
        "python scripts/build_figure4_panelA_jolts_sector_rates.py",
        "python scripts/qa_figure4_panelA_jolts_sector_rates.py",
        [
            "figures/figure4_panelA_jolts_sector_rates.csv",
            "intermediate/figure4_panelA_jolts_sector_rates_run_metadata.json",
        ],
    ),
    (
        "T-009",
        "python scripts/build_figure4_panelB_ces_sector_index.py",
        "python scripts/qa_figure4_panelB_ces_sector_index.py",
        [
            "figures/figure4_panelB_ces_sector_index.csv",
            "intermediate/figure4_panelB_ces_sector_index_run_metadata.json",
        ],
    ),
    (
        "T-010",
        "python scripts/build_figure5_capability_matrix.py",
        "python scripts/qa_figure5_capability_matrix.py",
        [
            "figures/figure5_capability_matrix.csv",
            "intermediate/figure5_capability_matrix_run_metadata.json",
        ],
    ),
    (
        "T-011",
        "python scripts/build_figureA1_asec_welfare_by_ai_tercile.py",
        "python scripts/qa_figureA1_asec_welfare_by_ai_tercile.py",
        [
            "figures/figureA1_asec_welfare_by_ai_tercile.csv",
            (
                "intermediate/"
                "figureA1_asec_welfare_by_ai_tercile_run_metadata.json"
            ),
        ],
    ),
    (
        "T-012",
        "python scripts/build_figureA2_sipp_event_study.py",
        "python scripts/qa_figureA2_sipp_event_study.py",
        [
            "figures/figureA2_sipp_event_study.csv",
            "intermediate/figureA2_sipp_event_study_run_metadata.json",
        ],
    ),
    (
        "T-013",
        "python scripts/build_figureA3_cps_supp_validation.py",
        "python scripts/qa_figureA3_cps_supp_validation.py",
        [
            "figures/figureA3_cps_supp_validation.csv",
            "intermediate/figureA3_cps_supp_validation_run_metadata.json",
        ],
    ),
    (
        "T-014",
        "python scripts/build_figureA4_abs_structural_adoption.py",
        "python scripts/qa_figureA4_abs_structural_adoption.py",
        [
            "figures/figureA4_abs_structural_adoption.csv",
            "intermediate/figureA4_abs_structural_adoption_run_metadata.json",
        ],
    ),
    (
        "T-015",
        "python scripts/build_figureA5_ces_payroll_hours.py",
        "python scripts/qa_figureA5_ces_payroll_hours.py",
        [
            "figures/figureA5_ces_payroll_hours.csv",
            "intermediate/figureA5_ces_payroll_hours_run_metadata.json",
        ],
    ),
    (
        "T-016",
        "python scripts/build_figureA6_bed_churn.py",
        "python scripts/qa_figureA6_bed_churn.py",
        [
            "figures/figureA6_bed_churn.csv",
            "intermediate/figureA6_bed_churn_run_metadata.json",
        ],
    ),
    (
        "T-017",
        "python scripts/build_figureA7_qcew_state_benchmark.py",
        "python scripts/qa_figureA7_qcew_state_benchmark.py",
        [
            "figures/figureA7_qcew_state_benchmark.csv",
            "intermediate/figureA7_qcew_state_benchmark_run_metadata.json",
        ],
    ),
    (
        "T-018",
        "python scripts/build_figureA8_lehd_benchmark.py",
        "python scripts/qa_figureA8_lehd_benchmark.py",
        [
            "figures/figureA8_lehd_benchmark.csv",
            "intermediate/figureA8_lehd_benchmark_run_metadata.json",
        ],
    ),
    (
        "T-019",
        "python scripts/build_figureA9_acs_local_composition.py",
        "python scripts/qa_figureA9_acs_local_composition.py",
        [
            "figures/figureA9_acs_local_composition.csv",
            "intermediate/figureA9_acs_local_composition_run_metadata.json",
        ],
    ),
    (
        "T-020",
        "python scripts/build_figureA10_nls_longrun.py",
        "python scripts/qa_figureA10_nls_longrun.py",
        [
            "figures/figureA10_nls_longrun.csv",
            "intermediate/figureA10_nls_longrun_run_metadata.json",
        ],
    ),
    (
        "T-021",
        "python scripts/build_occ22_sector_weights.py",
        "python scripts/qa_occ22_sector_weights.py",
        [
            "intermediate/occ22_sector_weights.csv",
            "intermediate/occ22_sector_weights_run_metadata.json",
        ],
    ),
    (
        "T-022",
        "python scripts/build_btos_sector_ai_use_monthly.py",
        "python scripts/qa_btos_sector_ai_use_monthly.py",
        [
            "intermediate/btos_sector_ai_use_monthly.csv",
            "intermediate/btos_sector_ai_use_monthly_run_metadata.json",
        ],
    ),
    (
        "T-023",
        "python scripts/build_awes_occ22_monthly.py",
        "python scripts/qa_awes_occ22_monthly.py",
        [
            "metrics/awes_occ22_monthly.csv",
            "intermediate/awes_run_metadata.json",
        ],
    ),
    (
        "T-024",
        "python scripts/build_sector6_stress_monthly.py",
        "python scripts/qa_sector6_stress_monthly.py",
        [
            "intermediate/sector6_stress_monthly.csv",
            "intermediate/sector6_stress_monthly_run_metadata.json",
        ],
    ),
    (
        "T-025",
        "python scripts/build_cps_occ22_exit_risk_monthly.py",
        "python scripts/qa_cps_occ22_exit_risk_monthly.py",
        [
            "intermediate/cps_occ22_exit_risk_monthly.csv",
            "intermediate/cps_occ22_exit_risk_monthly_run_metadata.json",
        ],
    ),
    (
        "T-026",
        "python scripts/build_alpi_occ22_monthly.py",
        "python scripts/qa_alpi_occ22_monthly.py",
        [
            "metrics/alpi_occ22_monthly.csv",
            "intermediate/alpi_run_metadata.json",
        ],
    ),
]

_POST_GATES_CORE: list[Gate] = [
    ("Robustness suite", "python scripts/run_robustness_all.py"),
    ("Freeze manifest build", "python scripts/build_freeze_manifest.py"),
    ("Freeze manifest QA", "python scripts/qa_freeze_manifest.py"),
    ("Drift dashboard build", "python scripts/build_drift_dashboard.py"),
    ("Drift dashboard QA", "python scripts/qa_drift_dashboard.py"),
]


def _post_gates() -> list[Gate]:
    """Policy briefing memo/Virginia gates run only if local optional scripts exist."""
    gates: list[Gate] = []
    if (ROOT / "scripts" / "run_memo_visuals_build.py").is_file():
        gates.append(("Policy visuals build", "python scripts/run_memo_visuals_build.py"))
        gates.append(("Policy visuals QA", "python scripts/run_memo_visuals_qa.py"))
    gates.extend(_POST_GATES_CORE)
    return gates


def _run(cmd: str) -> tuple[int, str]:
    env = os.environ.copy()
    # Escalate common silent-dataframe-mutation warnings in strict acceptance mode.
    env["PYTHONWARNINGS"] = ",".join(
        [
            "error::FutureWarning",
            "error::pandas.errors.SettingWithCopyWarning",
        ]
    )
    proc = subprocess.run(
        cmd,
        cwd=ROOT,
        shell=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=env,
    )
    return proc.returncode, proc.stdout


def _delete_outputs(paths: list[str]) -> list[str]:
    deleted: list[str] = []
    for rel in paths:
        p = ROOT / rel
        if p.exists():
            p.unlink()
            deleted.append(rel)
    return deleted


def main() -> int:
    INTER.mkdir(parents=True, exist_ok=True)
    ts = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    log_path = INTER / f"full_clean_rebuild_acceptance_{ts}.md"

    lines: list[str] = []
    lines.append("# Full Clean Rebuild Acceptance Log")
    lines.append("")
    lines.append(
        f"- Started UTC: {dt.datetime.now(dt.timezone.utc).isoformat()}"
    )
    lines.append("- Scope: PR-000 through T-026")
    lines.append("- Mode: strict ticket-by-ticket rebuild with checkpoints")
    lines.append("")

    failures = 0
    start_all = time.time()

    for ticket, build_cmd, qa_cmd, outputs in TICKETS:
        t0 = time.time()
        lines.append(f"## {ticket}")
        lines.append("")

        deleted = _delete_outputs(outputs)
        lines.append(
            f"- Checkpoint cleanup deleted: {deleted if deleted else 'none'}"
        )

        rc_b, out_b = _run(build_cmd)
        if "SettingWithCopyWarning" in out_b:
            rc_b = 1
            out_b = out_b + "\n[STRICT WARNING POLICY] SettingWithCopyWarning escalated to failure.\n"
        lines.append(f"- Build command: `{build_cmd}`")
        lines.append(f"- Build exit code: `{rc_b}`")
        lines.append("")
        lines.append("### Build Output")
        lines.append("```text")
        lines.append(out_b.rstrip() if out_b.strip() else "(no output)")
        lines.append("```")

        missing = [p for p in outputs if not (ROOT / p).exists()]
        lines.append(
            f"- Output existence check: `{missing if missing else 'all present'}`"
        )

        rc_q, out_q = _run(qa_cmd)
        lines.append(f"- QA command: `{qa_cmd}`")
        lines.append(f"- QA exit code: `{rc_q}`")
        lines.append("")
        lines.append("### QA Output")
        lines.append("```text")
        lines.append(out_q.rstrip() if out_q.strip() else "(no output)")
        lines.append("```")

        elapsed = round(time.time() - t0, 2)
        ticket_ok = rc_b == 0 and rc_q == 0 and not missing
        if not ticket_ok:
            failures += 1
        lines.append(
            f"- Checkpoint result: `{'PASS' if ticket_ok else 'FAIL'}`"
        )
        lines.append(f"- Elapsed seconds: `{elapsed}`")
        lines.append("")

        log_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

        if not ticket_ok:
            lines.append("Stopping early after first failure in strict mode.")
            log_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
            print(f"FAILED at {ticket}. See log: {log_path}")
            return 1

    total_elapsed = round(time.time() - start_all, 2)
    lines.append("## Post-Ticket Release Gates")
    lines.append("")
    for gate_name, gate_cmd in _post_gates():
        rc_g, out_g = _run(gate_cmd)
        lines.append(f"- Gate: `{gate_name}`")
        lines.append(f"- Command: `{gate_cmd}`")
        lines.append(f"- Exit code: `{rc_g}`")
        lines.append("```text")
        lines.append(out_g.rstrip() if out_g.strip() else "(no output)")
        lines.append("```")
        lines.append("")
        log_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        if rc_g != 0:
            lines.append("Stopping after failed post-ticket release gate.")
            log_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
            print(f"FAILED at post gate: {gate_name}. See log: {log_path}")
            return 1

    lines.append("## Final Summary")
    lines.append("")
    lines.append(f"- Failures: `{failures}`")
    lines.append(f"- Total elapsed seconds: `{total_elapsed}`")
    lines.append("- Overall result: `PASS`")
    lines.append("")
    lines.append(
        f"- Finished UTC: {dt.datetime.now(dt.timezone.utc).isoformat()}"
    )
    log_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"PASS. Acceptance log written: {log_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
