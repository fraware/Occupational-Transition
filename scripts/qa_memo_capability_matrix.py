from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "figures" / "figure5_capability_matrix.csv"
ALLOWED = {"direct", "partial", "none"}
COLS = [
    "worker_outcomes",
    "worker_occupational_transitions",
    "firm_ai_adoption",
    "labor_demand_turnover",
    "occupational_structure_wages",
    "task_exposure_mechanism",
    "worker_firm_ai_linkage",
]


def main() -> int:
    if not CSV.is_file():
        print(f"FAIL: missing {CSV}", file=sys.stderr)
        return 1
    d = pd.read_csv(CSV)
    miss = [c for c in COLS if c not in d.columns]
    if miss:
        print(f"FAIL: missing columns {miss}", file=sys.stderr)
        return 1
    for c in COLS:
        bad = set(d[c].astype(str)) - ALLOWED
        if bad:
            print(f"FAIL: invalid values in {c}: {sorted(bad)}", file=sys.stderr)
            return 1
    print("QA OK:", CSV)
    return 0


if __name__ == "__main__":
    sys.exit(main())

