"""
Single ordered entrypoint: dependencies, full PR-000 to T-026 rebuild + QA,
optional visuals.

This does not delete the git clone; it runs the same strict sequence as
`run_full_clean_rebuild_acceptance.py`, which cleans ticket outputs before each
build step. Raw inputs are fetched by individual build scripts into `raw/`
when missing (see `docs/replication/README.md`).

Usage (from repository root):

    python scripts/run_full_pipeline_from_raw.py

With optional stages:

    python scripts/run_full_pipeline_from_raw.py --with-visuals
    python scripts/run_full_pipeline_from_raw.py --skip-install --with-audit-summary
    python scripts/run_full_pipeline_from_raw.py --source-selection-mode freeze_mode --require-signoff

PowerShell uses `;` between commands if chaining manually:

    pip install -r requirements.txt
    python scripts/run_full_pipeline_from_raw.py
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

if str(Path(__file__).resolve().parents[1] / "src") not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from occupational_transition.orchestration import env_for_source_mode, latest_acceptance_log, run_shell

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Full pipeline: install deps, PR-000 to T-026, optional QA extras."
        ),
    )
    parser.add_argument(
        "--skip-install",
        action="store_true",
        help="Skip pip install -r requirements.txt",
    )
    parser.add_argument(
        "--with-visuals",
        action="store_true",
        help=(
            "After data pipeline PASS, run run_visuals_all.py "
            "and qa_visuals.py"
        ),
    )
    parser.add_argument(
        "--with-audit-summary",
        action="store_true",
        help=(
            "After acceptance, run build_acceptance_audit_summary.py on the "
            "newest full_clean_rebuild acceptance log"
        ),
    )
    parser.add_argument(
        "--source-selection-mode",
        choices=["latest_mode", "freeze_mode"],
        default="latest_mode",
        help="latest_mode uses current rolling sources; freeze_mode enforces baseline comparability checks",
    )
    parser.add_argument(
        "--require-signoff",
        action="store_true",
        help="Require intermediate/release_signoff.json approval in release gating",
    )
    args = parser.parse_args()
    run_env = env_for_source_mode(args.source_selection_mode)

    if not args.skip_install:
        rc, _ = run_shell(
            ROOT,
            "python -m pip install -r requirements.txt && python -m pip install -e .",
            env_overrides=run_env,
        )
        if rc != 0:
            print("FAIL: pip install", file=sys.stderr)
            return rc

    rc, _ = run_shell(ROOT, "python scripts/run_full_clean_rebuild_acceptance.py", env_overrides=run_env)
    if rc != 0:
        return rc

    if args.with_audit_summary:
        log = latest_acceptance_log(ROOT)
        if log is None:
            print(
                "WARN: no full_clean_rebuild_acceptance_*.md found; "
                "skipping audit summary",
                file=sys.stderr,
            )
        else:
            rc, _ = run_shell(
                ROOT,
                "python scripts/build_acceptance_audit_summary.py "
                f'--log "{log.relative_to(ROOT).as_posix()}"',
                env_overrides=run_env,
            )
            if rc != 0:
                return rc

    if args.with_visuals:
        rc, _ = run_shell(ROOT, "python scripts/run_visuals_all.py", env_overrides=run_env)
        if rc != 0:
            return rc
        rc, _ = run_shell(ROOT, "python scripts/qa_visuals.py", env_overrides=run_env)
        if rc != 0:
            return rc

    # Optional Virginia / policy briefing visuals (local-only; Virginia PNG/PDF under
    # docs/states/virginia/visuals/ are gitignored when present).
    memo_orchestrator = ROOT / "scripts" / "run_memo_visuals_build.py"
    if memo_orchestrator.is_file():
        rc, _ = run_shell(ROOT, "python scripts/run_memo_visuals_build.py", env_overrides=run_env)
        if rc != 0:
            return rc
        rc, _ = run_shell(ROOT, "python scripts/run_memo_visuals_qa.py", env_overrides=run_env)
        if rc != 0:
            return rc
    else:
        print(
            "SKIP: policy briefing visuals (scripts/run_memo_visuals_build.py not in tree).",
            file=sys.stderr,
        )
    rc, _ = run_shell(ROOT, "python scripts/run_robustness_all.py", env_overrides=run_env)
    if rc != 0:
        return rc
    rc, _ = run_shell(ROOT, "python scripts/build_freeze_manifest.py", env_overrides=run_env)
    if rc != 0:
        return rc
    rc, _ = run_shell(ROOT, "python scripts/qa_freeze_manifest.py", env_overrides=run_env)
    if rc != 0:
        return rc
    rc, _ = run_shell(ROOT, "python scripts/build_drift_dashboard.py", env_overrides=run_env)
    if rc != 0:
        return rc
    rc, _ = run_shell(ROOT, "python scripts/qa_drift_dashboard.py", env_overrides=run_env)
    if rc != 0:
        return rc
    if args.require_signoff:
        rc, _ = run_shell(ROOT, "python scripts/qa_release_signoff.py", env_overrides=run_env)
        if rc != 0:
            return rc

    print("PASS: run_full_pipeline_from_raw completed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
