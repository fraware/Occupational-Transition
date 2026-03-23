"""QA for T-015 Figure A5 CES payroll and hours context."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from urllib.request import Request, urlopen

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FIG_CSV = ROOT / "figures" / "figureA5_ces_payroll_hours.csv"
META_JSON = ROOT / "intermediate" / "figureA5_ces_payroll_hours_run_metadata.json"

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)

EXP_COLS = [
    "month",
    "sector6_code",
    "sector6_label",
    "ces_payroll_employment_thousands",
    "ces_avg_weekly_hours",
    "payroll_index_aug2023_100",
    "hours_index_aug2023_100",
    "employment_series_id",
    "hours_series_id",
]

EXP_SECTORS = {"MFG", "INF", "FAS", "PBS", "HCS", "RET"}
MIN_MONTH = "2019-01"
BASE_MONTH = "2023-08"
INDEX_TOL = 1e-6


def _request(url: str) -> Request:
    return Request(url, headers={"User-Agent": USER_AGENT})


def _fetch_sha256(url: str) -> str:
    with urlopen(_request(url), timeout=600) as resp:
        data = resp.read()
    return hashlib.sha256(data).hexdigest()


def _months_contiguous(months: list[str]) -> bool:
    if not months:
        return False
    ys = [int(m.split("-")[0]) for m in months]
    ms = [int(m.split("-")[1]) for m in months]
    for i in range(1, len(months)):
        py, pm = ys[i - 1], ms[i - 1]
        ey, em = ys[i], ms[i]
        n_y, n_m = (py + 1, 1) if pm == 12 else (py, pm + 1)
        if (ey, em) != (n_y, n_m):
            return False
    return True


def report(errors: list[str]) -> int:
    if errors:
        print("QA failures:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1
    print("QA OK: figureA5_ces_payroll_hours.csv")
    return 0


def main() -> int:
    errors: list[str] = []

    if not FIG_CSV.is_file():
        errors.append(f"missing output: {FIG_CSV}")
        return report(errors)
    if not META_JSON.is_file():
        errors.append(f"missing metadata: {META_JSON}")
        return report(errors)

    df = pd.read_csv(FIG_CSV)
    if list(df.columns) != EXP_COLS:
        errors.append(f"columns must be {EXP_COLS}, got {list(df.columns)}")

    if df.empty:
        errors.append("csv is empty")
        return report(errors)

    for c in EXP_COLS:
        if c in df.columns and df[c].isna().any():
            errors.append(f"NaN in {c}")

    for c in [
        "ces_payroll_employment_thousands",
        "ces_avg_weekly_hours",
        "payroll_index_aug2023_100",
        "hours_index_aug2023_100",
    ]:
        try:
            df[c] = pd.to_numeric(df[c], errors="raise")
        except Exception as exc:
            errors.append(f"{c} not numeric: {exc}")

    if str(df["month"].min()) < MIN_MONTH:
        errors.append(f"month must be >= {MIN_MONTH}, got min={df['month'].min()}")

    months = sorted(df["month"].astype(str).unique().tolist())
    if not _months_contiguous(months):
        errors.append("months are not contiguous")

    sectors = set(df["sector6_code"].astype(str).unique())
    if sectors != EXP_SECTORS:
        errors.append(f"sector set mismatch: expected {sorted(EXP_SECTORS)}, got {sorted(sectors)}")

    dup = df.duplicated(["month", "sector6_code"], keep=False)
    if dup.any():
        errors.append("duplicate month x sector rows")

    counts = df.groupby("month", as_index=False).size()
    bad = counts[counts["size"] != 6]
    if not bad.empty:
        errors.append(f"each month must have 6 sectors; offending months: {bad['month'].tolist()[:12]}")

    if not (df["ces_payroll_employment_thousands"] > 0).all():
        errors.append("ces_payroll_employment_thousands must be > 0")
    if not (df["ces_avg_weekly_hours"] > 0).all():
        errors.append("ces_avg_weekly_hours must be > 0")
    if not (df["payroll_index_aug2023_100"] > 0).all():
        errors.append("payroll_index_aug2023_100 must be > 0")
    if not (df["hours_index_aug2023_100"] > 0).all():
        errors.append("hours_index_aug2023_100 must be > 0")

    base = df[df["month"].astype(str) == BASE_MONTH]
    if len(base) != 6:
        errors.append(f"expected 6 rows for base month {BASE_MONTH}, got {len(base)}")
    else:
        if (base["payroll_index_aug2023_100"] - 100.0).abs().gt(INDEX_TOL).any():
            errors.append("payroll index not 100 at base month for all sectors")
        if (base["hours_index_aug2023_100"] - 100.0).abs().gt(INDEX_TOL).any():
            errors.append("hours index not 100 at base month for all sectors")

    if (~df["employment_series_id"].astype(str).str.slice(2, 3).eq("S")).any():
        errors.append("employment_series_id must be seasonally adjusted")
    if (~df["hours_series_id"].astype(str).str.slice(2, 3).eq("S")).any():
        errors.append("hours_series_id must be seasonally adjusted")

    meta = json.loads(META_JSON.read_text(encoding="utf-8"))
    if meta.get("ticket") != "T-015":
        errors.append("metadata ticket must be T-015")
    if meta.get("row_count") != len(df):
        errors.append("metadata row_count mismatch")
    if meta.get("crosswalk_file") != "crosswalks/sector6_crosswalk.csv":
        errors.append("metadata crosswalk_file mismatch")

    window = meta.get("month_window", {})
    if window.get("base_month") != BASE_MONTH:
        errors.append(f"metadata base month must be {BASE_MONTH}")
    if window.get("first_month_in_output") != str(df["month"].min()):
        errors.append("metadata first_month_in_output mismatch")
    if window.get("last_month_in_output") != str(df["month"].max()):
        errors.append("metadata last_month_in_output mismatch")

    dt = meta.get("datatype_codes", {})
    if (dt.get("employment") or {}).get("code") != "01":
        errors.append("metadata employment datatype code must be 01")
    if (dt.get("hours") or {}).get("code") != "02":
        errors.append("metadata hours datatype code must be 02")

    retained = meta.get("retained_series") or []
    if len(retained) != 6:
        errors.append("metadata retained_series must have 6 rows")

    hashes = meta.get("source_files_sha256") or []
    if len(hashes) < 6:
        errors.append("metadata source_files_sha256 missing expected entries")
    for entry in hashes:
        name = entry.get("file_name")
        url = entry.get("url")
        exp = entry.get("sha256")
        if not name or not url or not exp:
            errors.append(f"incomplete hash entry: {entry!r}")
            continue
        try:
            got = _fetch_sha256(url)
        except Exception as exc:
            errors.append(f"could not verify hash for {name}: {exc}")
            continue
        if got != exp:
            errors.append(f"sha256 mismatch for {name}: expected {exp[:16]} got {got[:16]}")

    return report(errors)


if __name__ == "__main__":
    raise SystemExit(main())
