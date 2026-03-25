"""
Build a state-specific deep dive from Figure A7 (QCEW state benchmark).

This script is intentionally additive: it reads the existing Figure A7 CSV and
writes separate, state-namespaced outputs intended for briefings.

Inputs:
- figures/figureA7_qcew_state_benchmark.csv (T-017)

Outputs (default: Virginia, FIPS 51):
- figures/state_deep_dive_qcew_<state_fips>_profile.csv
- figures/state_deep_dive_qcew_<state_fips>_ranks.csv
- figures/state_deep_dive_qcew_<state_fips>_peers.csv
- intermediate/state_deep_dive_qcew_<state_fips>_run_metadata.json
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures"
INTER = ROOT / "intermediate"

IN_A7 = FIG / "figureA7_qcew_state_benchmark.csv"

SECTOR6_ORDER = ["MFG", "INF", "FAS", "PBS", "HCS", "RET"]

# Default peer set for Virginia briefings: neighbors + DC.
# (WV=54, MD=24, DC=11, NC=37, TN=47, KY=21)
DEFAULT_VA_PEERS = ["11", "21", "24", "37", "47", "54"]


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _as_fips2(x: str) -> str:
    s = str(x).strip()
    if not s.isdigit():
        raise ValueError(f"state_fips must be numeric, got {x!r}")
    return s.zfill(2)


def _parse_peers(peers_csv: str) -> list[str]:
    if not peers_csv.strip():
        return []
    out: list[str] = []
    for raw in peers_csv.split(","):
        f = _as_fips2(raw)
        if f not in out:
            out.append(f)
    return out


def _assert_expected_a7_schema(df: pd.DataFrame) -> None:
    required = [
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
    ]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise RuntimeError(f"A7 input missing columns: {missing}")
    if df.empty:
        raise RuntimeError("A7 input is empty")
    if df["qcew_year"].nunique() != 1 or df["qcew_quarter"].nunique() != 1:
        raise RuntimeError(
            "A7 input must contain a single retained qcew year/quarter"
        )


def _rank_desc(s: pd.Series) -> pd.Series:
    # Rank 1 = highest value; deterministic ties via 'min'
    return s.rank(method="min", ascending=False).astype(int)


def _peer_frame(
    df: pd.DataFrame, peers: Iterable[str], state_fips: str
) -> pd.DataFrame:
    keep = set([_as_fips2(state_fips), *[_as_fips2(p) for p in peers]])
    sub = df[df["state_fips"].isin(keep)].copy()
    if sub.empty:
        raise RuntimeError(f"no rows for state/peer set: {sorted(keep)}")
    return sub


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--state-fips",
        default="51",
        help="2-digit state FIPS (default: 51 for Virginia)",
    )
    ap.add_argument(
        "--peers",
        default=",".join(DEFAULT_VA_PEERS),
        help=(
            "Comma-separated 2-digit FIPS peer set "
            "(default: VA neighbors + DC)"
        ),
    )
    args = ap.parse_args()

    state_fips = _as_fips2(args.state_fips)
    peer_fips = _parse_peers(args.peers)

    FIG.mkdir(parents=True, exist_ok=True)
    INTER.mkdir(parents=True, exist_ok=True)

    if not IN_A7.is_file():
        raise FileNotFoundError(
            f"missing input {IN_A7}. Run: "
            "python scripts/build_figureA7_qcew_state_benchmark.py"
        )

    df = pd.read_csv(IN_A7, dtype={"state_fips": str})
    df["state_fips"] = df["state_fips"].astype(str).str.zfill(2)
    _assert_expected_a7_schema(df)

    qcew_year = int(df["qcew_year"].iloc[0])
    qcew_quarter = int(df["qcew_quarter"].iloc[0])

    # Normalize sector ordering for deterministic outputs.
    df["sector6_code"] = pd.Categorical(
        df["sector6_code"].astype(str),
        categories=SECTOR6_ORDER,
        ordered=True,
    )
    df = df.sort_values(["state_fips", "sector6_code"]).reset_index(drop=True)

    if state_fips not in set(df["state_fips"].unique()):
        raise RuntimeError(f"state_fips={state_fips} not present in A7 input")

    out_profile = FIG / f"state_deep_dive_qcew_{state_fips}_profile.csv"
    out_ranks = FIG / f"state_deep_dive_qcew_{state_fips}_ranks.csv"
    out_peers = FIG / f"state_deep_dive_qcew_{state_fips}_peers.csv"
    out_meta = INTER / f"state_deep_dive_qcew_{state_fips}_run_metadata.json"

    # 1) Profile: the state rows as-is (with small extras for briefing use).
    prof = df[df["state_fips"] == state_fips].copy()
    prof = prof[
        [
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
        ]
    ].copy()
    prof["sector_share_pct"] = (
        100.0 * prof["state_sector_employment_share"].astype(float)
    )
    prof["average_weekly_wage_usd"] = prof["average_weekly_wage"].astype(float)
    prof = prof.sort_values(["sector6_code"]).reset_index(drop=True)
    prof.to_csv(out_profile, index=False)

    # 2) Ranks: how the state compares across all states in A7.
    tmp = df.copy()
    tmp["share_rank_desc"] = tmp.groupby(["sector6_code"], observed=True)[
        "state_sector_employment_share"
    ].transform(_rank_desc)
    tmp["wage_rank_desc"] = tmp.groupby(["sector6_code"], observed=True)[
        "average_weekly_wage"
    ].transform(_rank_desc)
    tmp["num_states_in_sector"] = tmp.groupby(["sector6_code"], observed=True)[
        "state_fips"
    ].transform("nunique")
    ranks = tmp[tmp["state_fips"] == state_fips].copy()
    ranks = ranks[
        [
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
        ]
    ].copy()
    ranks["sector_share_pct"] = (
        100.0 * ranks["state_sector_employment_share"].astype(float)
    )
    ranks = ranks.sort_values(["sector6_code"]).reset_index(drop=True)
    ranks.to_csv(out_ranks, index=False)

    # 3) Peers: VA vs peers (including VA) with both share and wage.
    peers_df = _peer_frame(df, peer_fips, state_fips).copy()
    peers_df["sector_share_pct"] = (
        100.0 * peers_df["state_sector_employment_share"].astype(float)
    )
    peers_df = peers_df[
        [
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
    ].copy()
    peers_df = peers_df.sort_values(["sector6_code", "state_fips"]).reset_index(
        drop=True
    )
    peers_df.to_csv(out_peers, index=False)

    meta = {
        "generated_at_utc": _utc_now_iso(),
        "input": {
            "figure": "T-017",
            "path": str(IN_A7.relative_to(ROOT)).replace("\\", "/"),
            "qcew_year": qcew_year,
            "qcew_quarter": qcew_quarter,
        },
        "parameters": {
            "state_fips": state_fips,
            "peers": peer_fips,
            "sector6_order": SECTOR6_ORDER,
            "ranking": {
                "method": "min",
                "ascending": False,
                "rank_1_is": "highest",
            },
        },
        "outputs": {
            "profile_csv": str(out_profile.relative_to(ROOT)).replace("\\", "/"),
            "ranks_csv": str(out_ranks.relative_to(ROOT)).replace("\\", "/"),
            "peers_csv": str(out_peers.relative_to(ROOT)).replace("\\", "/"),
        },
    }
    out_meta.write_text(json.dumps(meta, indent=2), encoding="utf-8")

    print(f"Wrote {out_profile}")
    print(f"Wrote {out_ranks}")
    print(f"Wrote {out_peers}")
    print(f"Wrote {out_meta}")


if __name__ == "__main__":
    main()
