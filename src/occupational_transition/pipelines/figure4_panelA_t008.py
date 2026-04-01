from __future__ import annotations

import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from occupational_transition.crosswalks import load_sector6_jolts_labels
from occupational_transition.http import sha256_bytes
from occupational_transition.sources.jolts import (
    DATA_FILE_BY_DATAELEMENT,
    DATAELEMENT_TO_RATE_NAME,
    JOLTS_BASE,
    PROVENANCE_FILES,
    fetch_jolts_file_bytes,
    load_jt_series_table,
    parse_data_line,
    period_to_month,
)

MIN_MONTH = "2019-01"
CANONICAL_JOLTS_INDUSTRY_BY_SECTOR6: dict[str, str] = {
    "MFG": "300000",
    "RET": "440000",
    "INF": "510000",
    "FAS": "510099",
    "PBS": "540099",
    "HCS": "620000",
}
SECTOR6_ORDER: list[str] = ["MFG", "INF", "FAS", "PBS", "HCS", "RET"]
RATE_NAME_ORDER: list[str] = [
    "job_openings_rate",
    "hires_rate",
    "quits_rate",
    "layoffs_discharges_rate",
]
OUT_COLS = ["month", "sector6_code", "sector6_label", "rate_name", "rate_value", "series_id"]


def run(root: Path) -> tuple[Path, Path, int]:
    fig = root / "figures"
    inter = root / "intermediate"
    cross = root / "crosswalks" / "sector6_crosswalk.csv"
    out_csv = fig / "figure4_panelA_jolts_sector_rates.csv"
    out_meta = inter / "figure4_panelA_jolts_sector_rates_run_metadata.json"
    generated_at = datetime.now(timezone.utc).isoformat()

    industry_to_sector6 = {v: k for k, v in CANONICAL_JOLTS_INDUSTRY_BY_SECTOR6.items()}
    sector6_labels = load_sector6_jolts_labels(cross)
    file_hashes: list[dict[str, str]] = []
    series_text: str | None = None
    for fname in PROVENANCE_FILES:
        url = f"{JOLTS_BASE}{fname}"
        raw = fetch_jolts_file_bytes(fname)
        file_hashes.append({"file_name": fname, "url": url, "sha256": sha256_bytes(raw)})
        if fname == "jt.series":
            series_text = raw.decode("utf-8", "replace")
    if series_text is None:
        raise RuntimeError("jt.series not loaded")

    target_meta: dict[str, dict[str, str]] = {}
    for row in load_jt_series_table(series_text):
        sid = row.get("series_id", "").strip()
        if not sid:
            continue
        if row.get("seasonal") != "S" or row.get("state_code") != "00":
            continue
        if row.get("area_code") != "00000" or row.get("sizeclass_code") != "00":
            continue
        if row.get("ratelevel_code") != "R":
            continue
        de = row.get("dataelement_code", "")
        ind = row.get("industry_code", "")
        if de not in DATAELEMENT_TO_RATE_NAME or ind not in industry_to_sector6:
            continue
        target_meta[sid] = {
            "sector6_code": industry_to_sector6[ind],
            "sector6_label": sector6_labels[industry_to_sector6[ind]],
            "rate_name": DATAELEMENT_TO_RATE_NAME[de],
            "dataelement_code": de,
            "jolts_industry_code": ind,
        }

    ids_by_file: dict[str, set[str]] = defaultdict(set)
    for sid, meta in target_meta.items():
        ids_by_file[DATA_FILE_BY_DATAELEMENT[meta["dataelement_code"]]].add(sid)

    values_by_series: dict[str, list[tuple[str, float]]] = defaultdict(list)
    for fname, id_set in ids_by_file.items():
        text = fetch_jolts_file_bytes(fname).decode("utf-8", "replace")
        for line in text.splitlines()[1:]:
            parsed = parse_data_line(line)
            if parsed is None:
                continue
            sid, year_s, period, val_raw = parsed
            if sid not in id_set:
                continue
            month = period_to_month(year_s, period)
            if month is None or month < MIN_MONTH:
                continue
            values_by_series[sid].append((month, float(val_raw)))

    out_rows: list[dict[str, Any]] = []
    months_union: set[str] = set()
    for sid, meta in sorted(target_meta.items(), key=lambda kv: (kv[1]["sector6_code"], kv[1]["rate_name"])):
        for month, val in sorted(values_by_series.get(sid, [])):
            months_union.add(month)
            out_rows.append(
                {
                    "month": month,
                    "sector6_code": meta["sector6_code"],
                    "sector6_label": meta["sector6_label"],
                    "rate_name": meta["rate_name"],
                    "rate_value": val,
                    "series_id": sid,
                }
            )

    sector_rank = {c: i for i, c in enumerate(SECTOR6_ORDER)}
    rate_rank = {r: i for i, r in enumerate(RATE_NAME_ORDER)}
    out_rows.sort(key=lambda r: (r["month"], sector_rank[r["sector6_code"]], rate_rank[r["rate_name"]]))

    fig.mkdir(parents=True, exist_ok=True)
    inter.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(out_rows, columns=OUT_COLS).to_csv(out_csv, index=False)

    sorted_months = sorted(months_union)
    meta_out: dict[str, Any] = {
        "ticket": "T-008",
        "generated_at_utc": generated_at,
        "month_window": {
            "min_requested": MIN_MONTH,
            "first_month_in_output": sorted_months[0] if sorted_months else None,
            "last_month_in_output": sorted_months[-1] if sorted_months else None,
        },
        "canonical_jolts_industry_by_sector6": dict(CANONICAL_JOLTS_INDUSTRY_BY_SECTOR6),
        "crosswalk_file": str(cross.relative_to(root)).replace("\\", "/"),
        "source_files_sha256": file_hashes,
        "row_count": len(out_rows),
        "output_csv": str(out_csv.relative_to(root)).replace("\\", "/"),
    }
    out_meta.write_text(json.dumps(meta_out, indent=2), encoding="utf-8")
    return out_csv, out_meta, len(out_rows)
