"""QA for T-018 Figure A8 LEHD public benchmark."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from urllib.request import Request, urlopen

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FIG_CSV = ROOT / "figures" / "figureA8_lehd_benchmark.csv"
META_JSON = ROOT / "intermediate" / "figureA8_lehd_benchmark_run_metadata.json"

MIN_QUARTER = "2019-Q1"
EXP_COLS = [
    "quarter",
    "benchmark_series_key",
    "benchmark_series_label",
    "benchmark_rate",
    "source_program",
    "source_series_id",
]

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)


def _request(url: str) -> Request:
    return Request(url, headers={"User-Agent": USER_AGENT})


def _fetch_sha256(url: str) -> str:
    with urlopen(_request(url), timeout=600) as resp:
        raw = resp.read()
    return hashlib.sha256(raw).hexdigest()


def _qtuple(q: str) -> tuple[int, int]:
    y, qq = q.split("-Q")
    return int(y), int(qq)


def _is_contiguous_quarters(vals: list[str]) -> bool:
    if not vals:
        return False
    for i in range(1, len(vals)):
        py, pq = _qtuple(vals[i - 1])
        ny, nq = _qtuple(vals[i])
        ey, eq = (py + 1, 1) if pq == 4 else (py, pq + 1)
        if (ny, nq) != (ey, eq):
            return False
    return True


def report(errors: list[str]) -> int:
    if errors:
        print("QA failures:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1
    print("QA OK: figureA8_lehd_benchmark.csv")
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

    try:
        df["benchmark_rate"] = pd.to_numeric(
            df["benchmark_rate"], errors="raise"
        )
    except Exception as exc:
        errors.append(f"benchmark_rate not numeric: {exc}")

    if not (df["benchmark_rate"] >= 0).all():
        errors.append("benchmark_rate must be >= 0")
    if not (df["benchmark_rate"] <= 1).all():
        errors.append("benchmark_rate must be <= 1")

    dup = df.duplicated(["quarter"], keep=False)
    if dup.any():
        errors.append("quarter must be unique")

    q = sorted(df["quarter"].astype(str).tolist())
    if q[0] < MIN_QUARTER:
        errors.append(f"quarter min must be >= {MIN_QUARTER}, got {q[0]}")
    if not _is_contiguous_quarters(q):
        errors.append("quarters are not contiguous")

    if df["benchmark_series_key"].nunique() != 1:
        errors.append("benchmark_series_key must be constant")
    if df["benchmark_series_label"].nunique() != 1:
        errors.append("benchmark_series_label must be constant")
    if df["source_program"].nunique() != 1:
        errors.append("source_program must be constant")
    if df["source_series_id"].nunique() != 1:
        errors.append("source_series_id must be constant")

    meta = json.loads(META_JSON.read_text(encoding="utf-8"))
    if meta.get("ticket") != "T-018":
        errors.append("metadata ticket must be T-018")
    if meta.get("row_count") != len(df):
        errors.append("metadata row_count mismatch")
    if meta.get("output_csv") != "figures/figureA8_lehd_benchmark.csv":
        errors.append("metadata output_csv mismatch")

    qwin = meta.get("quarter_window", {})
    if qwin.get("first_quarter_in_output") != q[0]:
        errors.append("metadata first_quarter_in_output mismatch")
    if qwin.get("last_quarter_in_output") != q[-1]:
        errors.append("metadata last_quarter_in_output mismatch")

    if meta.get("benchmark_series_key") != df["benchmark_series_key"].iloc[0]:
        errors.append("metadata benchmark_series_key mismatch")
    if (
        meta.get("benchmark_series_label")
        != df["benchmark_series_label"].iloc[0]
    ):
        errors.append("metadata benchmark_series_label mismatch")
    if meta.get("source_series_id") != df["source_series_id"].iloc[0]:
        errors.append("metadata source_series_id mismatch")

    hashes = meta.get("source_files_sha256", [])
    if len(hashes) < 3:
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
                f"sha256 mismatch for {name}: "
                f"expected {exp[:16]} got {got[:16]}"
            )

    return report(errors)


if __name__ == "__main__":
    raise SystemExit(main())
