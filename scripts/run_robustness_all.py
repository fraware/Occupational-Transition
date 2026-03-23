"""
Run all robustness scripts and write a combined log under intermediate/robustness/.

Does not modify figures/ or production intermediate outputs (only reports).

Usage:
    python scripts/run_robustness_all.py
"""

from __future__ import annotations

import datetime as dt
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CMDS = [
    "python scripts/robustness/figure1_tercile_stability.py",
    "python scripts/robustness/figure2_cps_checks.py",
    "python scripts/robustness/figure3_btos_consistency.py",
    "python scripts/robustness/figure4_sector_crosswalk.py",
    "python scripts/robustness/figure5_matrix_trace.py",
]


def main() -> int:
    ts = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    log_dir = ROOT / "intermediate" / "robustness"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / f"robustness_run_{ts}.md"

    lines: list[str] = [
        "# Robustness run",
        "",
        f"- UTC: {dt.datetime.now(dt.timezone.utc).isoformat()}",
        "",
    ]
    failures = 0
    for cmd in CMDS:
        lines.append(f"## `{cmd}`")
        lines.append("")
        proc = subprocess.run(
            cmd,
            cwd=ROOT,
            shell=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        lines.append("```text")
        lines.append(proc.stdout.rstrip() or "(no output)")
        lines.append("```")
        lines.append(f"- exit code: `{proc.returncode}`")
        lines.append("")
        if proc.returncode != 0:
            failures += 1

    lines.append("## Summary")
    lines.append(f"- failures: `{failures}`")
    log_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {log_path}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
