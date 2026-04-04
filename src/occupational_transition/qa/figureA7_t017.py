"""Ticket QA (from scripts/qa_figureA7_qcew_state_benchmark.py)."""

from __future__ import annotations

import hashlib
import json
import sys
from urllib.request import Request, urlopen

import pandas as pd

from occupational_transition.paths import repo_root

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)

EXP_COLS = [
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
    "source_industry_aggregation_note",
]
EXP_SECTORS = {"MFG", "INF", "FAS", "PBS", "HCS", "RET"}


def _request(url: str) -> Request:
    return Request(url, headers={"User-Agent": USER_AGENT})


def _fetch_sha256(url: str) -> str:
    with urlopen(_request(url), timeout=600) as resp:
        data = resp.read()
    return hashlib.sha256(data).hexdigest()


def report(errors: list[str]) -> int:
    if errors:
        print("QA failures:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1
    print("QA OK: figureA7_qcew_state_benchmark.csv")
    return 0


def main() -> int:
    root = repo_root()
    FIG_CSV = root / "figures" / "figureA7_qcew_state_benchmark.csv"
    META_JSON = (
        root / "intermediate" / "figureA7_qcew_state_benchmark_run_metadata.json"
    )
    errors: list[str] = []
    if not FIG_CSV.is_file():
        errors.append(f"missing output: {FIG_CSV}")
        return report(errors)
    if not META_JSON.is_file():
        errors.append(f"missing metadata: {META_JSON}")
        return report(errors)

    df = pd.read_csv(FIG_CSV, dtype={"state_fips": str})
    if list(df.columns) != EXP_COLS:
        errors.append(f"columns must be {EXP_COLS}, got {list(df.columns)}")
    if df.empty:
        errors.append("csv is empty")
        return report(errors)

    for c in EXP_COLS:
        if c in df.columns and df[c].isna().any():
            errors.append(f"NaN in {c}")

    for c in [
        "qcew_year",
        "qcew_quarter",
        "sector_employment",
        "state_total_employment",
        "state_sector_employment_share",
        "average_weekly_wage",
    ]:
        try:
            df[c] = pd.to_numeric(df[c], errors="raise")
        except Exception as exc:
            errors.append(f"{c} not numeric: {exc}")

    if (df["qcew_quarter"] < 1).any() or (df["qcew_quarter"] > 4).any():
        errors.append("qcew_quarter must be in 1..4")

    state_fips_ok = df["state_fips"].astype(str).str.match(r"^\d{2}$")
    if not state_fips_ok.all():
        errors.append("state_fips must be 2-digit numeric")

    dup = df.duplicated(["qcew_year", "qcew_quarter", "state_fips", "sector6_code"])
    if dup.any():
        errors.append("duplicate year/quarter/state/sector rows")

    if df["qcew_year"].nunique() != 1 or df["qcew_quarter"].nunique() != 1:
        errors.append("output must contain one retained qcew year/quarter only")

    sectors = set(df["sector6_code"].astype(str).unique())
    if sectors != EXP_SECTORS:
        errors.append(
            "sector set mismatch: "
            f"expected {sorted(EXP_SECTORS)}, got {sorted(sectors)}"
        )

    counts = df.groupby("state_fips", as_index=False).size()
    bad = counts[counts["size"] != 6]
    if not bad.empty:
        errors.append(
            "each state must have 6 sector rows; offending states: "
            f"{bad['state_fips'].tolist()[:12]}"
        )

    if not (df["sector_employment"] > 0).all():
        errors.append("sector_employment must be > 0")
    if not (df["state_total_employment"] > 0).all():
        errors.append("state_total_employment must be > 0")
    if not (df["average_weekly_wage"] > 0).all():
        errors.append("average_weekly_wage must be > 0")

    shares = df["state_sector_employment_share"]
    if not ((shares >= 0) & (shares <= 1)).all():
        errors.append("state_sector_employment_share must be in [0,1]")

    sum_df = df.groupby("state_fips", as_index=False)[
        "state_sector_employment_share"
    ].sum()
    off = sum_df[(sum_df["state_sector_employment_share"] - 1.0).abs() > 1e-6]
    if not off.empty:
        errors.append(
            "state share sums != 1 within tolerance for states: "
            f"{off['state_fips'].tolist()[:12]}"
        )

    tdf = df.groupby("state_fips", as_index=False)["state_total_employment"].nunique()
    if (tdf["state_total_employment"] != 1).any():
        errors.append("state_total_employment must be constant within state")

    meta = json.loads(META_JSON.read_text(encoding="utf-8"))
    if meta.get("ticket") != "T-017":
        errors.append("metadata ticket must be T-017")
    if meta.get("row_count") != len(df):
        errors.append("metadata row_count mismatch")
    if meta.get("crosswalk_file") != "crosswalks/sector6_crosswalk.csv":
        errors.append("metadata crosswalk_file mismatch")
    if "retained_period" not in meta:
        errors.append("metadata retained_period missing")

    rp = meta.get("retained_period", {})
    y = int(df["qcew_year"].iloc[0])
    q = int(df["qcew_quarter"].iloc[0])
    if rp.get("qcew_year") != y:
        errors.append("metadata retained_period qcew_year mismatch")
    if rp.get("qcew_quarter") != f"Q{q}":
        errors.append("metadata retained_period qcew_quarter mismatch")

    hashes = meta.get("source_files_sha256", [])
    if len(hashes) < 2:
        errors.append("metadata source_files_sha256 missing expected entries")
    for h in hashes:
        name = h.get("file_name")
        url = h.get("url")
        exp = h.get("sha256")
        if not name or not url or not exp:
            errors.append(f"incomplete hash entry: {h!r}")
            continue
        try:
            got = _fetch_sha256(url)
        except Exception as exc:
            errors.append(f"could not verify hash for {name}: {exc}")
            continue
        if got != exp:
            errors.append(
                f"sha256 mismatch for {name}: " f"expected {exp[:16]} got {got[:16]}"
            )

    return report(errors)


if __name__ == "__main__":
    raise SystemExit(main())
