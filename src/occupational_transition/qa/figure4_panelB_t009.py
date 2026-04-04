"""Ticket QA (from scripts/qa_figure4_panelB_ces_sector_index.py)."""

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
    "month",
    "sector6_code",
    "sector6_label",
    "ces_payroll_employment_thousands",
    "index_aug2023_100",
    "series_id",
]

EXP_SECTOR6 = {"MFG", "INF", "FAS", "PBS", "HCS", "RET"}

MIN_MONTH = "2019-01"
BASE_MONTH = "2023-08"

INDEX_TOL = 1e-6


def _request(url: str) -> Request:
    return Request(url, headers={"User-Agent": USER_AGENT})


def _fetch_sha256(url: str) -> str:
    with urlopen(_request(url), timeout=600) as resp:
        data = resp.read()
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    root = repo_root()
    FIG_CSV = root / "figures" / "figure4_panelB_ces_sector_index.csv"
    META_JSON = (
        root / "intermediate" / "figure4_panelB_ces_sector_index_run_metadata.json"
    )
    errors: list[str] = []

    if not FIG_CSV.is_file():
        errors.append(f"missing output: {FIG_CSV}")
        return _report(errors)

    df = pd.read_csv(FIG_CSV)
    if list(df.columns) != EXP_COLS:
        errors.append(f"columns must be {EXP_COLS}, got {list(df.columns)}")

    for c in EXP_COLS:
        if c in df.columns and df[c].isna().any():
            errors.append(f"NaN in {c}")

    if df.empty:
        errors.append("csv is empty")
        return _report(errors)

    try:
        df["ces_payroll_employment_thousands"] = pd.to_numeric(
            df["ces_payroll_employment_thousands"], errors="raise"
        )
        df["index_aug2023_100"] = pd.to_numeric(df["index_aug2023_100"], errors="raise")
    except Exception as e:
        errors.append(f"numeric columns: {e}")

    if str(df["month"].min()) < MIN_MONTH:
        errors.append(f"month must be >= {MIN_MONTH}, got min={df['month'].min()}")

    sectors = set(df["sector6_code"].astype(str).unique())
    if sectors != EXP_SECTOR6:
        errors.append(
            f"sector6_code set must be {sorted(EXP_SECTOR6)}, " f"got {sorted(sectors)}"
        )

    dup = df.duplicated(["month", "sector6_code"], keep=False)
    if dup.any():
        errors.append("duplicate month x sector6_code rows")

    grp = df.groupby("month", as_index=False).size()
    bad_sizes = grp[grp["size"] != 6]
    if not bad_sizes.empty:
        errors.append(
            "each month must have 6 rows; "
            f"offending months: {bad_sizes['month'].tolist()[:12]}"
        )

    if not (df["ces_payroll_employment_thousands"] >= -1e-9).all():
        errors.append("ces_payroll_employment_thousands must be nonnegative")

    if not (df["index_aug2023_100"] >= -1e-9).all():
        errors.append("index_aug2023_100 must be nonnegative")

    base = df[df["month"].astype(str) == BASE_MONTH]
    if len(base) != 6:
        errors.append(f"expected 6 rows for base month {BASE_MONTH}, got {len(base)}")
    else:
        bad_idx = base["index_aug2023_100"] - 100.0
        if (bad_idx.abs() > INDEX_TOL).any():
            errors.append(
                f"index_aug2023_100 must be 100 in {BASE_MONTH} for each " "sector"
            )

    bad_sa = ~df["series_id"].astype(str).str.slice(2, 3).eq("S")
    if bad_sa.any():
        errors.append(
            "all series_id values must be seasonally adjusted (third character S)"
        )

    if not META_JSON.is_file():
        errors.append(f"missing metadata: {META_JSON}")
        return _report(errors)

    meta = json.loads(META_JSON.read_text(encoding="utf-8"))

    if meta.get("ticket") != "T-009":
        errors.append("metadata ticket must be T-009")

    if not meta.get("assertion_sa_published_ces_only"):
        errors.append("metadata missing assertion_sa_published_ces_only")

    mw = meta.get("month_window") or {}
    if mw.get("first_month_in_output") != str(df["month"].min()):
        errors.append("metadata first_month_in_output does not match csv min month")
    if mw.get("last_month_in_output") != str(df["month"].max()):
        errors.append("metadata last_month_in_output does not match csv max month")
    if mw.get("index_base_month") != BASE_MONTH:
        errors.append(f"metadata index_base_month must be {BASE_MONTH}")

    if meta.get("row_count") != len(df):
        errors.append(
            f"metadata row_count {meta.get('row_count')} != csv rows {len(df)}"
        )

    retained = meta.get("retained_series") or []
    if len(retained) != 6:
        errors.append(f"retained_series must list 6 series, got {len(retained)}")

    exp_cross = "crosswalks/sector6_crosswalk.csv"
    if meta.get("crosswalk_file") != exp_cross:
        errors.append(f"metadata crosswalk_file must be {exp_cross}")

    file_entries = meta.get("source_files_sha256") or []
    if len(file_entries) < 8:
        errors.append("metadata source_files_sha256 must include all T-009 inputs")

    for entry in file_entries:
        name = entry.get("file_name")
        url = entry.get("url")
        expected = entry.get("sha256")
        if not name or not url or not expected:
            errors.append(f"incomplete hash entry: {entry!r}")
            continue
        try:
            got = _fetch_sha256(url)
        except Exception as e:
            errors.append(f"could not verify hash for {name}: {e}")
            continue
        if got != expected:
            errors.append(
                f"sha256 mismatch for {name}: metadata has {expected[:16]}... "
                f"live file has {got[:16]}... (re-run build after BLS updates)"
            )

    return _report(errors)


def _report(errors: list[str]) -> int:
    if errors:
        print("QA failures:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1
    print("QA OK: figure4_panelB_ces_sector_index.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
