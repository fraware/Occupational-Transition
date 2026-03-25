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
import glob
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _run(cmd: str, *, extra_env: dict[str, str] | None = None) -> int:
    env = os.environ.copy()
    if extra_env:
        env.update(extra_env)
    proc = subprocess.run(
        cmd,
        cwd=ROOT,
        shell=True,
        env=env,
    )
    return proc.returncode


def _latest_acceptance_log() -> Path | None:
    pattern = str(ROOT / "intermediate" / "full_clean_rebuild_acceptance_*.md")
    paths = [
        Path(p)
        for p in glob.glob(pattern)
        if "_audit_summary" not in p and p.endswith(".md")
    ]
    if not paths:
        return None
    return max(paths, key=lambda p: p.stat().st_mtime)


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
    run_env = {"SOURCE_SELECTION_MODE": args.source_selection_mode}

    if not args.skip_install:
        rc = _run("python -m pip install -r requirements.txt", extra_env=run_env)
        if rc != 0:
            print("FAIL: pip install", file=sys.stderr)
            return rc

    rc = _run("python scripts/run_full_clean_rebuild_acceptance.py", extra_env=run_env)
    if rc != 0:
        return rc

    if args.with_audit_summary:
        log = _latest_acceptance_log()
        if log is None:
            print(
                "WARN: no full_clean_rebuild_acceptance_*.md found; "
                "skipping audit summary",
                file=sys.stderr,
            )
        else:
            rc = _run(
                "python scripts/build_acceptance_audit_summary.py "
                f'--log "{log.relative_to(ROOT).as_posix()}"',
                extra_env=run_env,
            )
            if rc != 0:
                return rc

    if args.with_visuals:
        rc = _run("python scripts/run_visuals_all.py", extra_env=run_env)
        if rc != 0:
            return rc
        rc = _run("python scripts/qa_visuals.py", extra_env=run_env)
        if rc != 0:
            return rc

    # Reliability hardening gates for policy-facing releases.
    rc = _run("python scripts/run_memo_visuals_build.py", extra_env=run_env)
    if rc != 0:
        return rc
    rc = _run("python scripts/run_memo_visuals_qa.py", extra_env=run_env)
    if rc != 0:
        return rc
    rc = _run("python scripts/run_robustness_all.py", extra_env=run_env)
    if rc != 0:
        return rc
    rc = _run("python scripts/build_freeze_manifest.py", extra_env=run_env)
    if rc != 0:
        return rc
    rc = _run("python scripts/qa_freeze_manifest.py", extra_env=run_env)
    if rc != 0:
        return rc
    rc = _run("python scripts/build_drift_dashboard.py", extra_env=run_env)
    if rc != 0:
        return rc
    rc = _run("python scripts/qa_drift_dashboard.py", extra_env=run_env)
    if rc != 0:
        return rc
    if args.require_signoff:
        rc = _run("python scripts/qa_release_signoff.py", extra_env=run_env)
        if rc != 0:
            return rc

    print("PASS: run_full_pipeline_from_raw completed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
