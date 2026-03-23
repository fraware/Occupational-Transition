"""QA for T-016 Figure A6 BED establishment churn."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from urllib.request import Request, urlopen

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FIG_CSV = ROOT / "figures" / "figureA6_bed_churn.csv"
META_JSON = ROOT / "intermediate" / "figureA6_bed_churn_run_metadata.json"

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)

EXP_COLS = [
    "quarter",
    "sector6_code",
    "sector6_label",
    "gross_job_gains_rate",
    "gross_job_losses_rate",
    "openings_rate",
    "closings_rate",
    "gains_series_id",
    "losses_series_id",
    "openings_series_id",
    "closings_series_id",
]
EXP_SECTORS = {"MFG", "INF", "FAS", "PBS", "HCS", "RET"}
MIN_QUARTER = "2019-Q1"


def _request(url: str) -> Request:
    return Request(url, headers={"User-Agent": USER_AGENT})


def _fetch_sha256(url: str) -> str:
    with urlopen(_request(url), timeout=600) as resp:
        data = resp.read()
    return hashlib.sha256(data).hexdigest()


def _quarter_tuple(q: str) -> tuple[int, int]:
    y, qq = q.split("-Q")
    return int(y), int(qq)


def _contiguous_quarters(vals: list[str]) -> bool:
    if not vals:
        return False
    for i in range(1, len(vals)):
        py, pq = _quarter_tuple(vals[i - 1])
        ny, nq = _quarter_tuple(vals[i])
        ey, eq = (py + 1, 1) if pq == 4 else (py, pq + 1)
        if (ny, nq) != (ey, eq):
            return False
    return True


def report(errors: list[str]) -> int:
    if errors:
        print("QA failures:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1
    print("QA OK: figureA6_bed_churn.csv")
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
        "gross_job_gains_rate",
        "gross_job_losses_rate",
        "openings_rate",
        "closings_rate",
    ]:
        try:
            df[c] = pd.to_numeric(df[c], errors="raise")
        except Exception as exc:
            errors.append(f"{c} not numeric: {exc}")

    if str(df["quarter"].min()) < MIN_QUARTER:
        errors.append(
            f"quarter must be >= {MIN_QUARTER}, got min={df['quarter'].min()}"
        )
    qlist = sorted(df["quarter"].astype(str).unique().tolist())
    if not _contiguous_quarters(qlist):
        errors.append("quarters are not contiguous")

    sectors = set(df["sector6_code"].astype(str).unique())
    if sectors != EXP_SECTORS:
        errors.append(
            "sector set mismatch: "
            f"expected {sorted(EXP_SECTORS)}, got {sorted(sectors)}"
        )

    dup = df.duplicated(["quarter", "sector6_code"], keep=False)
    if dup.any():
        errors.append("duplicate quarter x sector rows")

    counts = df.groupby("quarter", as_index=False).size()
    bad = counts[counts["size"] != 6]
    if not bad.empty:
        errors.append(
            "each quarter must have 6 sectors; "
            f"offending: {bad['quarter'].tolist()[:12]}"
        )

    for c in [
        "gross_job_gains_rate",
        "gross_job_losses_rate",
        "openings_rate",
        "closings_rate",
    ]:
        if df[c].isna().any():
            errors.append(f"{c} contains missing values")
        if not (df[c] >= 0).all():
            errors.append(f"{c} must be nonnegative")
        if not (df[c] < 1000).all():
            errors.append(f"{c} fails sanity bound")

    # Series IDs stable by sector for each measure.
    for sid_col in [
        "gains_series_id",
        "losses_series_id",
        "openings_series_id",
        "closings_series_id",
    ]:
        per_sector = df.groupby("sector6_code")[sid_col].nunique()
        if (per_sector != 1).any():
            errors.append(f"{sid_col} must be stable per sector")

    meta = json.loads(META_JSON.read_text(encoding="utf-8"))
    if meta.get("ticket") != "T-016":
        errors.append("metadata ticket must be T-016")
    if meta.get("row_count") != len(df):
        errors.append("metadata row_count mismatch")
    if meta.get("crosswalk_file") != "crosswalks/sector6_crosswalk.csv":
        errors.append("metadata crosswalk_file mismatch")

    qwin = meta.get("quarter_window", {})
    if qwin.get("first_quarter_in_output") != str(df["quarter"].min()):
        errors.append("metadata first_quarter_in_output mismatch")
    if qwin.get("last_quarter_in_output") != str(df["quarter"].max()):
        errors.append("metadata last_quarter_in_output mismatch")

    sf = meta.get("series_filters", {})
    exp_filters = {
        "seasonal": "S",
        "state_code": "00",
        "msa_code": "00000",
        "county_code": "000",
        "unitanalysis_code": "1",
        "dataelement_code": "1",
        "sizeclass_code": "00",
        "ratelevel_code": "R",
        "periodicity_code": "Q",
        "ownership_code": "5",
    }
    if sf != exp_filters:
        errors.append("metadata series_filters mismatch")

    code_map = meta.get("measure_code_mapping", {})
    for k in [
        "gross_job_gains_rate",
        "gross_job_losses_rate",
        "openings_rate",
        "closings_rate",
    ]:
        if k not in code_map:
            errors.append(f"metadata measure_code_mapping missing {k}")

    hashes = meta.get("source_files_sha256", [])
    if len(hashes) < 10:
        errors.append("metadata source_files_sha256 missing expected files")
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
                f"sha256 mismatch for {name}: "
                f"expected {exp[:16]} got {got[:16]}"
            )

    return report(errors)


if __name__ == "__main__":
    raise SystemExit(main())
