from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "figures" / "memo_policy_roadmap.csv"


def main() -> int:
    if not CSV.is_file():
        print(f"FAIL: missing {CSV}", file=sys.stderr)
        return 1
    d = pd.read_csv(CSV)
    req = ["effort_tier", "instrument", "proposed_addition", "unlocks", "key_boundary"]
    miss = [c for c in req if c not in d.columns]
    if miss:
        print(f"FAIL: missing columns {miss}", file=sys.stderr)
        return 1
    allowed = {"low", "medium", "large"}
    bad = set(d["effort_tier"].astype(str)) - allowed
    if bad:
        print(f"FAIL: invalid effort_tier values {sorted(bad)}", file=sys.stderr)
        return 1
    print("QA OK:", CSV)
    return 0


if __name__ == "__main__":
    sys.exit(main())

