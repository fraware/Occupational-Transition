"""
Build Figure A5 CES payroll and hours context (T-015).

Output:
- figures/figureA5_ces_payroll_hours.csv
- intermediate/figureA5_ces_payroll_hours_run_metadata.json
"""

from __future__ import annotations

import csv
import hashlib
import json
from collections import defaultdict
from datetime import datetime, timezone
from io import StringIO
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "raw" / "bls" / "ce"
FIG = ROOT / "figures"
INTER = ROOT / "intermediate"
CROSS = ROOT / "crosswalks" / "sector6_crosswalk.csv"

OUT_CSV = FIG / "figureA5_ces_payroll_hours.csv"
OUT_META = INTER / "figureA5_ces_payroll_hours_run_metadata.json"

CES_BASE = "https://download.bls.gov/pub/time.series/ce/"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)

MIN_MONTH = "2019-01"
BASE_MONTH = "2023-08"

SECTOR6_ORDER = ["MFG", "INF", "FAS", "PBS", "HCS", "RET"]

# Canonical CES national supersector totals.
CANONICAL_SUPERSECTOR_BY_SECTOR6: dict[str, str] = {
    "MFG": "30",
    "RET": "42",
    "INF": "50",
    "FAS": "55",
    "PBS": "60",
    "HCS": "65",
}

OUT_COLS = [
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

STATIC_FILES = ["ce.txt", "ce.series", "ce.datatype", "ce.period", "ce.seasonal"]
DATA_FILE_ALL = "ce.data.0.ALLCESSeries"


def _request(url: str) -> Request:
    return Request(url, headers={"User-Agent": USER_AGENT})


def fetch_bytes(url: str) -> bytes:
    with urlopen(_request(url), timeout=300) as resp:
        return resp.read()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def normalize_row(row: dict[str, str]) -> dict[str, str]:
    return {k.strip(): (v.strip() if isinstance(v, str) else v) for k, v in row.items()}


def load_tsv_table(text: str) -> list[dict[str, str]]:
    rows = list(csv.DictReader(StringIO(text), delimiter="\t"))
    return [normalize_row(r) for r in rows]


def period_to_month(year_s: str, period: str) -> str | None:
    if not period.startswith("M") or len(period) != 3:
        return None
    try:
        y = int(year_s)
        m = int(period[1:])
    except ValueError:
        return None
    if m < 1 or m > 12:
        return None
    return f"{y:04d}-{m:02d}"


def parse_data_line(line: str) -> tuple[str, str, str, str] | None:
    if not line.strip():
        return None
    parts = line.split("\t")
    if len(parts) < 4:
        return None
    return parts[0].strip(), parts[1].strip(), parts[2].strip(), parts[3].strip()


def ces_supersector_total_industry_code(supersector: str) -> str:
    return f"{supersector}000000"


def load_sector6_labels_from_crosswalk() -> dict[str, str]:
    df = pd.read_csv(CROSS)
    inv = {v: k for k, v in CANONICAL_SUPERSECTOR_BY_SECTOR6.items()}
    out: dict[str, str] = {}
    for _, row in df.iterrows():
        if row.get("source_program") != "CES":
            continue
        if int(row.get("is_in_scope", 0)) != 1:
            continue
        if str(row.get("source_level", "")).strip() != "ces_supersector":
            continue
        sc = str(row.get("source_code", "")).strip()
        if sc in inv and inv[sc] not in out:
            out[inv[sc]] = str(row.get("sector6_label", "")).strip()

    for sec in CANONICAL_SUPERSECTOR_BY_SECTOR6:
        if sec not in out:
            raise RuntimeError(f"missing CES supersector label in crosswalk for {sec}")
    return out


def resolve_series_ids(series_rows: list[dict[str, str]], data_type_code: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for sec, supersector in CANONICAL_SUPERSECTOR_BY_SECTOR6.items():
        want_ind = ces_supersector_total_industry_code(supersector)
        hits: list[str] = []
        for row in series_rows:
            if row.get("seasonal") != "S":
                continue
            if row.get("data_type_code") != data_type_code:
                continue
            if row.get("supersector_code") != supersector:
                continue
            if row.get("industry_code") != want_ind:
                continue
            sid = str(row.get("series_id", "")).strip()
            if sid:
                hits.append(sid)
        if len(hits) != 1:
            raise RuntimeError(
                f"expected exactly one series for {sec} datatype {data_type_code}, got {len(hits)}"
            )
        out[sec] = hits[0]
    return out


def collect_values(
    target_ids: set[str], file_names: list[str]
) -> dict[str, list[tuple[str, float]]]:
    out: dict[str, list[tuple[str, float]]] = defaultdict(list)
    for fname in file_names:
        url = f"{CES_BASE}{fname}"
        with urlopen(_request(url), timeout=600) as resp:
            first = True
            for raw_line in resp:
                line = raw_line.decode("utf-8", "replace")
                if first:
                    first = False
                    continue
                parsed = parse_data_line(line)
                if parsed is None:
                    continue
                sid, year_s, period, value_raw = parsed
                if sid not in target_ids:
                    continue
                month = period_to_month(year_s, period)
                if month is None or month < MIN_MONTH:
                    continue
                try:
                    value = float(value_raw)
                except ValueError as exc:
                    raise RuntimeError(
                        f"non-numeric CES value for {sid} {year_s} {period}: {value_raw!r}"
                    ) from exc
                out[sid].append((month, value))
    return out


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    FIG.mkdir(parents=True, exist_ok=True)
    INTER.mkdir(parents=True, exist_ok=True)

    generated_at = datetime.now(timezone.utc).isoformat()
    sector6_labels = load_sector6_labels_from_crosswalk()

    file_hashes: list[dict[str, str]] = []
    series_text: str | None = None

    for fname in STATIC_FILES:
        url = f"{CES_BASE}{fname}"
        raw = fetch_bytes(url)
        file_hashes.append({"file_name": fname, "url": url, "sha256": sha256_bytes(raw)})
        (RAW / fname).write_bytes(raw)
        if fname == "ce.series":
            series_text = raw.decode("utf-8", "replace")

    if series_text is None:
        raise RuntimeError("failed to load ce.series")

    series_rows = load_tsv_table(series_text)
    employment_series = resolve_series_ids(series_rows, data_type_code="01")
    hours_series = resolve_series_ids(series_rows, data_type_code="02")

    data_files = [DATA_FILE_ALL]
    for fname in data_files:
        url = f"{CES_BASE}{fname}"
        raw = fetch_bytes(url)
        file_hashes.append({"file_name": fname, "url": url, "sha256": sha256_bytes(raw)})
        (RAW / fname).write_bytes(raw)

    emp_values = collect_values(set(employment_series.values()), data_files)
    hrs_values = collect_values(set(hours_series.values()), data_files)

    out_rows: list[dict[str, Any]] = []
    months_union: set[str] = set()

    for sec in SECTOR6_ORDER:
        emp_sid = employment_series[sec]
        hrs_sid = hours_series[sec]
        emp_map = {m: v for m, v in emp_values.get(emp_sid, [])}
        hrs_map = {m: v for m, v in hrs_values.get(hrs_sid, [])}

        if BASE_MONTH not in emp_map or BASE_MONTH not in hrs_map:
            raise RuntimeError(f"missing base month {BASE_MONTH} for sector {sec}")

        common_months = sorted(set(emp_map.keys()) & set(hrs_map.keys()))
        for month in common_months:
            months_union.add(month)
            emp = emp_map[month]
            hrs = hrs_map[month]
            out_rows.append(
                {
                    "month": month,
                    "sector6_code": sec,
                    "sector6_label": sector6_labels[sec],
                    "ces_payroll_employment_thousands": emp,
                    "ces_avg_weekly_hours": hrs,
                    "payroll_index_aug2023_100": 100.0 * (emp / emp_map[BASE_MONTH]),
                    "hours_index_aug2023_100": 100.0 * (hrs / hrs_map[BASE_MONTH]),
                    "employment_series_id": emp_sid,
                    "hours_series_id": hrs_sid,
                }
            )

    if not out_rows:
        raise RuntimeError("no output rows built")

    sector_rank = {s: i for i, s in enumerate(SECTOR6_ORDER)}
    out_rows.sort(key=lambda r: (r["month"], sector_rank[r["sector6_code"]]))

    first_month = min(months_union)
    last_month = max(months_union)

    df = pd.DataFrame(out_rows, columns=OUT_COLS)
    df.to_csv(OUT_CSV, index=False)

    retained_series: list[dict[str, str]] = []
    for sec in SECTOR6_ORDER:
        ss = CANONICAL_SUPERSECTOR_BY_SECTOR6[sec]
        retained_series.append(
            {
                "sector6_code": sec,
                "sector6_label": sector6_labels[sec],
                "ces_supersector_code": ss,
                "employment_series_id": employment_series[sec],
                "hours_series_id": hours_series[sec],
            }
        )

    meta_out: dict[str, Any] = {
        "ticket": "T-015",
        "generated_at_utc": generated_at,
        "output_csv": str(OUT_CSV.relative_to(ROOT)).replace("\\", "/"),
        "crosswalk_file": str(CROSS.relative_to(ROOT)).replace("\\", "/"),
        "assertion_published_ces_only": (
            "Only BLS-published national CES seasonally adjusted series are used "
            "for datatype 01 (all employees, thousands) and datatype 02 "
            "(average weekly hours of all employees)."
        ),
        "month_window": {
            "min_requested": MIN_MONTH,
            "base_month": BASE_MONTH,
            "first_month_in_output": first_month,
            "last_month_in_output": last_month,
        },
        "canonical_supersector_by_sector6": CANONICAL_SUPERSECTOR_BY_SECTOR6,
        "retained_series": retained_series,
        "datatype_codes": {
            "employment": {"code": "01", "label": "ALL EMPLOYEES, THOUSANDS"},
            "hours": {
                "code": "02",
                "label": "AVERAGE WEEKLY HOURS OF ALL EMPLOYEES",
            },
        },
        "source_files_sha256": file_hashes,
        "row_count": int(len(df)),
    }
    OUT_META.write_text(json.dumps(meta_out, indent=2), encoding="utf-8")
    print(f"Wrote {OUT_CSV} ({len(df)} rows)")
    print(f"Wrote {OUT_META}")


if __name__ == "__main__":
    main()
