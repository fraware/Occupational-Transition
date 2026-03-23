"""QA for Figure 4 Panel A JOLTS sector rates (T-008). Exit 1 on failure."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from urllib.request import Request, urlopen

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FIG_CSV = ROOT / "figures" / "figure4_panelA_jolts_sector_rates.csv"
META_JSON = (
    ROOT / "intermediate" / "figure4_panelA_jolts_sector_rates_run_metadata.json"
)

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)

EXP_COLS = [
    "month",
    "sector6_code",
    "sector6_label",
    "rate_name",
    "rate_value",
    "series_id",
]

EXP_SECTOR6 = {"MFG", "INF", "FAS", "PBS", "HCS", "RET"}

EXP_RATE_NAMES = {
    "job_openings_rate",
    "hires_rate",
    "quits_rate",
    "layoffs_discharges_rate",
}

MIN_MONTH = "2019-01"


def _request(url: str) -> Request:
    return Request(url, headers={"User-Agent": USER_AGENT})


def _fetch_sha256(url: str) -> str:
    with urlopen(_request(url), timeout=300) as resp:
        data = resp.read()
    return hashlib.sha256(data).hexdigest()


def main() -> int:
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

    # Schema and types
    try:
        df["rate_value"] = pd.to_numeric(df["rate_value"], errors="raise")
    except Exception as e:
        errors.append(f"rate_value not numeric: {e}")

    if "rate_value" in df.columns:
        if not (df["rate_value"] >= -1e-9).all():
            errors.append("rate_value must be nonnegative")
        if not (df["rate_value"] < 1e6).all():
            errors.append("rate_value unexpectedly large (sanity bound)")

    # Month range
    if str(df["month"].min()) < MIN_MONTH:
        errors.append(
            f"month must be >= {MIN_MONTH}, got min={df['month'].min()}"
        )

    # Sectors
    sectors = set(df["sector6_code"].astype(str).unique())
    if sectors != EXP_SECTOR6:
        errors.append(
            f"sector6_code set must be {sorted(EXP_SECTOR6)}, "
            f"got {sorted(sectors)}"
        )

    # Rate names
    rates = set(df["rate_name"].astype(str).unique())
    if rates != EXP_RATE_NAMES:
        errors.append(f"rate_name set mismatch: {sorted(rates)}")

    # Uniqueness
    dup = df.duplicated(["month", "sector6_code", "rate_name"], keep=False)
    if dup.any():
        errors.append("duplicate month x sector6_code x rate_name rows")

    # Complete grid: each month has 24 rows (6 sectors x 4 rates)
    grp = df.groupby("month", as_index=False).size()
    bad_sizes = grp[grp["size"] != 24]
    if not bad_sizes.empty:
        errors.append(
            "each month must have 24 rows (6 sectors x 4 rates); "
            f"offending months: {bad_sizes['month'].tolist()[:12]}"
        )

    # Per month-sector: exactly one row per rate_name
    g2 = df.groupby(["month", "sector6_code", "rate_name"]).size()
    if (g2 != 1).any():
        errors.append("duplicate or missing rate within a month-sector group")

    # Seasonally adjusted published convention: LABSTAT series_id uses code S at position 3 (1-based)
    # 0-based index 2 == 'S' for JTS... national SA series.
    bad_sa = ~df["series_id"].astype(str).str.slice(2, 3).eq("S")
    if bad_sa.any():
        errors.append(
            "all series_id values must be seasonally adjusted (third character S)"
        )

    # Metadata
    if not META_JSON.is_file():
        errors.append(f"missing metadata: {META_JSON}")
        return _report(errors)

    meta = json.loads(META_JSON.read_text(encoding="utf-8"))

    if meta.get("ticket") != "T-008":
        errors.append("metadata ticket must be T-008")

    if not meta.get("assertion_sa_published_rates_only"):
        errors.append("metadata missing assertion_sa_published_rates_only")

    mw = meta.get("month_window") or {}
    if mw.get("first_month_in_output") != str(df["month"].min()):
        errors.append(
            "metadata first_month_in_output does not match csv min month"
        )
    if mw.get("last_month_in_output") != str(df["month"].max()):
        errors.append(
            "metadata last_month_in_output does not match csv max month"
        )

    if meta.get("row_count") != len(df):
        errors.append(
            f"metadata row_count {meta.get('row_count')} != csv rows {len(df)}"
        )

    retained = meta.get("retained_series") or []
    if len(retained) != 24:
        errors.append(
            f"retained_series must list 24 series, got {len(retained)}"
        )

    # Crosswalk reference
    if meta.get("crosswalk_file") != "crosswalks/sector6_crosswalk.csv":
        errors.append("metadata crosswalk_file must be crosswalks/sector6_crosswalk.csv")

    # Hash consistency with live BLS LABSTAT files
    file_entries = meta.get("source_files_sha256") or []
    if len(file_entries) < 8:
        errors.append(
            "metadata source_files_sha256 must include all T-008 inputs"
        )

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
    print("QA OK: figure4_panelA_jolts_sector_rates.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
