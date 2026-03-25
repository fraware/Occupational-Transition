"""QA for state deep dive outputs derived from T-017 (Figure A7)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures"

SECTOR6_ORDER = ["MFG", "INF", "FAS", "PBS", "HCS", "RET"]


def report(errors: list[str]) -> int:
    if errors:
        print("QA failures:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1
    print("QA OK: state deep dive QCEW outputs")
    return 0


def _as_fips2(x: str) -> str:
    s = str(x).strip()
    if not s.isdigit():
        raise ValueError(f"state_fips must be numeric, got {x!r}")
    return s.zfill(2)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--state-fips", default="51")
    args = ap.parse_args()
    state_fips = _as_fips2(args.state_fips)

    errors: list[str] = []
    prof = FIG / f"state_deep_dive_qcew_{state_fips}_profile.csv"
    ranks = FIG / f"state_deep_dive_qcew_{state_fips}_ranks.csv"
    peers = FIG / f"state_deep_dive_qcew_{state_fips}_peers.csv"

    for p in [prof, ranks, peers]:
        if not p.is_file():
            errors.append(f"missing output: {p}")
            return report(errors)

    dprof = pd.read_csv(prof, dtype={"state_fips": str})
    exp_prof_cols = [
        "qcew_year",
        "qcew_quarter",
        "state_fips",
        "state_name",
        "sector6_code",
        "sector6_label",
        "sector_employment",
        "state_total_employment",
        "state_sector_employment_share",
        "average_weekly_wage",
        "sector_share_pct",
        "average_weekly_wage_usd",
    ]
    if list(dprof.columns) != exp_prof_cols:
        errors.append(
            f"profile columns must be {exp_prof_cols}, got {list(dprof.columns)}"
        )
    if dprof.empty or len(dprof) != 6:
        errors.append("profile must have exactly 6 sector rows")
    if (dprof["state_fips"].astype(str).str.zfill(2) != state_fips).any():
        errors.append("profile contains rows for wrong state_fips")
    sectors = dprof["sector6_code"].astype(str).tolist()
    if sectors != SECTOR6_ORDER:
        errors.append(f"profile sector order must be {SECTOR6_ORDER}, got {sectors}")

    drank = pd.read_csv(ranks, dtype={"state_fips": str})
    exp_rank_cols = [
        "qcew_year",
        "qcew_quarter",
        "state_fips",
        "state_name",
        "sector6_code",
        "sector6_label",
        "state_sector_employment_share",
        "average_weekly_wage",
        "share_rank_desc",
        "wage_rank_desc",
        "num_states_in_sector",
        "sector_share_pct",
    ]
    if list(drank.columns) != exp_rank_cols:
        errors.append(
            f"ranks columns must be {exp_rank_cols}, got {list(drank.columns)}"
        )
    if drank.empty or len(drank) != 6:
        errors.append("ranks must have exactly 6 sector rows")
    if (drank["share_rank_desc"] < 1).any() or (drank["wage_rank_desc"] < 1).any():
        errors.append("ranks must be positive integers (>=1)")
    if (drank["num_states_in_sector"] < 2).any():
        errors.append("num_states_in_sector must be >= 2")

    dpeers = pd.read_csv(peers, dtype={"state_fips": str})
    exp_peers_cols = [
        "qcew_year",
        "qcew_quarter",
        "state_fips",
        "state_name",
        "sector6_code",
        "sector6_label",
        "sector_employment",
        "state_total_employment",
        "state_sector_employment_share",
        "sector_share_pct",
        "average_weekly_wage",
    ]
    if list(dpeers.columns) != exp_peers_cols:
        errors.append(
            f"peers columns must be {exp_peers_cols}, got {list(dpeers.columns)}"
        )
    if dpeers.empty:
        errors.append("peers is empty")
    if state_fips not in set(dpeers["state_fips"].astype(str).str.zfill(2).unique()):
        errors.append("peers must include the focal state row(s)")
    if not set(dpeers["sector6_code"].astype(str).unique()).issuperset(
        set(SECTOR6_ORDER)
    ):
        errors.append("peers must include all six sectors")

    return report(errors)


if __name__ == "__main__":
    raise SystemExit(main())
