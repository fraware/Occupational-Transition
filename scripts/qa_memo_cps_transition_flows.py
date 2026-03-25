from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "figures" / "memo_cps_transition_flows.csv"
ALLOWED = {"low", "middle", "high", "unemployed", "nilf"}


def main() -> int:
    if not CSV.is_file():
        print(f"FAIL: missing {CSV}", file=sys.stderr)
        return 1
    d = pd.read_csv(CSV)
    req = ["month", "origin_group", "destination_group", "weighted_count", "share_of_origin"]
    miss = [c for c in req if c not in d.columns]
    if miss:
        print(f"FAIL: missing columns {miss}", file=sys.stderr)
        return 1
    if set(d["origin_group"]) - ALLOWED:
        print("FAIL: bad origin_group values", file=sys.stderr)
        return 1
    if set(d["destination_group"]) - ALLOWED:
        print("FAIL: bad destination_group values", file=sys.stderr)
        return 1
    if (pd.to_numeric(d["weighted_count"], errors="coerce") < 0).any():
        print("FAIL: negative weighted_count", file=sys.stderr)
        return 1
    if ((pd.to_numeric(d["share_of_origin"], errors="coerce") < 0) | (pd.to_numeric(d["share_of_origin"], errors="coerce") > 1)).any():
        print("FAIL: share_of_origin outside [0,1]", file=sys.stderr)
        return 1
    sums = d.groupby(["month", "origin_group"], as_index=False)["share_of_origin"].sum()
    if ((sums["share_of_origin"] - 1.0).abs() > 1e-6).any():
        print("FAIL: shares do not sum to 1 by origin group", file=sys.stderr)
        return 1
    print("QA OK:", CSV)
    return 0


if __name__ == "__main__":
    sys.exit(main())

