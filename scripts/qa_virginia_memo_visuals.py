from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures"
PNG = ROOT / "visuals" / "png"
VEC = ROOT / "visuals" / "vector"

VA_FIPS = "51"


def report(errors: list[str]) -> int:
    if errors:
        print("QA failures:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1
    print("QA OK: Virginia memo visuals")
    return 0


def _check_exists(path: Path, errors: list[str]) -> None:
    if not path.is_file():
        errors.append(f"missing file: {path}")


def main() -> int:
    errors: list[str] = []

    profile = FIG / f"state_deep_dive_qcew_{VA_FIPS}_profile.csv"
    ranks = FIG / f"state_deep_dive_qcew_{VA_FIPS}_ranks.csv"
    peers = FIG / f"state_deep_dive_qcew_{VA_FIPS}_peers.csv"
    kpis = FIG / "virginia_memo_kpis.csv"

    for p in [profile, ranks, peers, kpis]:
        _check_exists(p, errors)
    if errors:
        return report(errors)

    dprof = pd.read_csv(profile, dtype={"state_fips": str})
    if len(dprof) != 6:
        errors.append("Virginia profile must have 6 sector rows")
    if (dprof["state_fips"].astype(str).str.zfill(2) != VA_FIPS).any():
        errors.append("Virginia profile includes non-VA rows")
    share_sum = pd.to_numeric(
        dprof["state_sector_employment_share"], errors="coerce"
    ).sum()
    if abs(float(share_sum) - 1.0) > 1e-6:
        errors.append("Virginia profile shares must sum to 1 within tolerance")

    drank = pd.read_csv(ranks, dtype={"state_fips": str})
    if len(drank) != 6:
        errors.append("Virginia ranks must have 6 sector rows")
    for c in ["share_rank_desc", "wage_rank_desc", "num_states_in_sector"]:
        v = pd.to_numeric(drank[c], errors="coerce")
        if v.isna().any():
            errors.append(f"Virginia ranks column not numeric: {c}")
    if (pd.to_numeric(drank["share_rank_desc"], errors="coerce") < 1).any():
        errors.append("share_rank_desc must be >= 1")
    if (pd.to_numeric(drank["wage_rank_desc"], errors="coerce") < 1).any():
        errors.append("wage_rank_desc must be >= 1")

    dkpi = pd.read_csv(kpis)
    req_cols = [
        "kpi_id",
        "kpi_label",
        "value",
        "unit",
        "reference_period",
        "source_path_or_endpoint",
        "notes_limits",
    ]
    miss = [c for c in req_cols if c not in dkpi.columns]
    if miss:
        errors.append(f"virginia_memo_kpis missing columns: {miss}")
    if dkpi.empty:
        errors.append("virginia_memo_kpis.csv is empty")

    required_stems = [
        "va01_virginia_sector_composition",
        "va02_virginia_sector_wages",
        "va03_virginia_peers_sector_shares",
        "va04_virginia_peers_sector_wages",
        "va05_virginia_sector_ranks",
        "va06_virginia_kpi_dashboard",
    ]
    for stem in required_stems:
        _check_exists(PNG / f"{stem}.png", errors)
        _check_exists(VEC / f"{stem}.pdf", errors)

    return report(errors)


if __name__ == "__main__":
    raise SystemExit(main())
