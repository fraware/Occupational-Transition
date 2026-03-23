"""
Build figures/figure4_panelA_jolts_sector_rates.csv from official BLS LABSTAT
JOLTS time-series files (national, seasonally adjusted published rates only).

Run from repo root: python scripts/build_figure4_panelA_jolts_sector_rates.py
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
FIG = ROOT / "figures"
INTER = ROOT / "intermediate"
CROSS = ROOT / "crosswalks" / "sector6_crosswalk.csv"

OUT_CSV = FIG / "figure4_panelA_jolts_sector_rates.csv"
OUT_META = INTER / "figure4_panelA_jolts_sector_rates_run_metadata.json"

JOLTS_BASE = "https://download.bls.gov/pub/time.series/jt/"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)

# Minimum calendar month (inclusive) for the figure panel.
MIN_MONTH = "2019-01"

# One published national SA industry rate series per frozen sector6 (PR-000). Where
# multiple JOLTS industries map to the same sector6 (e.g. PBS), use the headline
# published industry aggregate for that sector; do not recompute rates across
# industries.
CANONICAL_JOLTS_INDUSTRY_BY_SECTOR6: dict[str, str] = {
    "MFG": "300000",
    "RET": "440000",
    "INF": "510000",
    "FAS": "510099",
    "PBS": "540099",
    "HCS": "620000",
}

# JOLTS data files (LABSTAT) keyed by two-character dataelement_code.
DATA_FILE_BY_DATAELEMENT: dict[str, str] = {
    "JO": "jt.data.2.JobOpenings",
    "HI": "jt.data.3.Hires",
    "QU": "jt.data.5.Quits",
    "LD": "jt.data.6.LayoffsDischarges",
}

DATAELEMENT_TO_RATE_NAME: dict[str, str] = {
    "JO": "job_openings_rate",
    "HI": "hires_rate",
    "QU": "quits_rate",
    "LD": "layoffs_discharges_rate",
}

# Stable presentation order for sector6_code in outputs.
SECTOR6_ORDER: list[str] = ["MFG", "INF", "FAS", "PBS", "HCS", "RET"]

RATE_NAME_ORDER: list[str] = [
    "job_openings_rate",
    "hires_rate",
    "quits_rate",
    "layoffs_discharges_rate",
]

# All LABSTAT inputs required for provenance (including reference files for QA).
PROVENANCE_FILES: list[str] = [
    "jt.series",
    "jt.industry",
    "jt.period",
    "jt.seasonal",
    "jt.data.2.JobOpenings",
    "jt.data.3.Hires",
    "jt.data.5.Quits",
    "jt.data.6.LayoffsDischarges",
]

OUT_COLS = [
    "month",
    "sector6_code",
    "sector6_label",
    "rate_name",
    "rate_value",
    "series_id",
]


def _request(url: str) -> Request:
    return Request(url, headers={"User-Agent": USER_AGENT})


def fetch_bytes(url: str) -> bytes:
    with urlopen(_request(url), timeout=300) as resp:
        return resp.read()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def normalize_jt_row(row: dict[str, str]) -> dict[str, str]:
    return {
        k.strip(): (v.strip() if isinstance(v, str) else v)
        for k, v in row.items()
    }


def load_jt_series_table(text: str) -> list[dict[str, str]]:
    rows = list(csv.DictReader(StringIO(text), delimiter="\t"))
    return [normalize_jt_row(r) for r in rows]


def period_to_month(year_s: str, period: str) -> str | None:
    if not period.startswith("M") or len(period) != 3:
        return None
    try:
        m = int(period[1:], 10)
    except ValueError:
        return None
    if m < 1 or m > 12:
        return None
    try:
        y = int(year_s, 10)
    except ValueError:
        return None
    return f"{y:04d}-{m:02d}"


def parse_data_line(line: str) -> tuple[str, str, str, str] | None:
    """Return (series_id, year, period, value_raw) or None."""
    if not line.strip():
        return None
    parts = line.split("\t")
    if len(parts) < 4:
        return None
    return (
        parts[0].strip(),
        parts[1].strip(),
        parts[2].strip(),
        parts[3].strip(),
    )


def load_sector6_labels() -> dict[str, str]:
    df = pd.read_csv(CROSS)
    sub = df[
        (df["source_program"] == "JOLTS")
        & (df["is_in_scope"] == 1)
        & (df["sector6_code"].notna())
        & (df["sector6_code"].astype(str).str.len() > 0)
    ]
    out: dict[str, str] = {}
    for _, row in sub.iterrows():
        code = str(row["sector6_code"])
        label = str(row["sector6_label"])
        if code not in out:
            out[code] = label
    for code in CANONICAL_JOLTS_INDUSTRY_BY_SECTOR6:
        if code not in out:
            raise RuntimeError(f"missing sector6 label in crosswalk for {code}")
    return out


def main() -> None:
    generated_at = datetime.now(timezone.utc).isoformat()

    industry_to_sector6 = {
        v: k for k, v in CANONICAL_JOLTS_INDUSTRY_BY_SECTOR6.items()
    }
    sector6_labels = load_sector6_labels()

    # Fetch provenance payloads and hashes.
    file_hashes: list[dict[str, str]] = []
    series_text: str | None = None
    for fname in PROVENANCE_FILES:
        url = f"{JOLTS_BASE}{fname}"
        raw = fetch_bytes(url)
        file_hashes.append(
            {"file_name": fname, "url": url, "sha256": sha256_bytes(raw)}
        )
        if fname == "jt.series":
            series_text = raw.decode("utf-8", "replace")

    if series_text is None:
        raise RuntimeError("jt.series not loaded")

    series_rows = load_jt_series_table(series_text)

    allowed_industries = set(CANONICAL_JOLTS_INDUSTRY_BY_SECTOR6.values())

    # series_id -> metadata for target series
    target_meta: dict[str, dict[str, str]] = {}

    for row in series_rows:
        sid = row.get("series_id", "").strip()
        if not sid:
            continue
        if row.get("seasonal") != "S":
            continue
        if row.get("state_code") != "00":
            continue
        if row.get("area_code") != "00000":
            continue
        if row.get("sizeclass_code") != "00":
            continue
        if row.get("ratelevel_code") != "R":
            continue
        de = row.get("dataelement_code", "")
        if de not in DATAELEMENT_TO_RATE_NAME:
            continue
        ind = row.get("industry_code", "")
        if ind not in allowed_industries:
            continue
        sec = industry_to_sector6.get(ind)
        if sec is None:
            continue

        if sid in target_meta:
            raise RuntimeError(f"duplicate series_id in jt.series selection: {sid}")

        target_meta[sid] = {
            "sector6_code": sec,
            "sector6_label": sector6_labels[sec],
            "rate_name": DATAELEMENT_TO_RATE_NAME[de],
            "dataelement_code": de,
            "jolts_industry_code": ind,
        }

    # Expect exactly 24 series (6 sectors x 4 rates).
    expected_n = len(CANONICAL_JOLTS_INDUSTRY_BY_SECTOR6) * len(
        DATAELEMENT_TO_RATE_NAME
    )
    if len(target_meta) != expected_n:
        raise RuntimeError(
            f"expected {expected_n} national SA rate series, got {len(target_meta)}"
        )

    # Group series IDs by LABSTAT data file (dataelement).
    ids_by_file: dict[str, set[str]] = defaultdict(set)
    for sid, meta in target_meta.items():
        de = meta["dataelement_code"]
        fname = DATA_FILE_BY_DATAELEMENT[de]
        ids_by_file[fname].add(sid)

    # Stream observations from each data file.
    values_by_series: dict[str, list[tuple[str, float]]] = defaultdict(list)

    for fname, id_set in ids_by_file.items():
        url = f"{JOLTS_BASE}{fname}"
        raw = fetch_bytes(url)
        text = raw.decode("utf-8", "replace")
        for line in text.splitlines()[1:]:
            parsed = parse_data_line(line)
            if parsed is None:
                continue
            sid, year_s, period, val_raw = parsed
            if sid not in id_set:
                continue
            month = period_to_month(year_s, period)
            if month is None:
                continue
            if month < MIN_MONTH:
                continue
            try:
                val = float(val_raw)
            except ValueError as e:
                raise RuntimeError(
                    f"non-numeric value for {sid} {year_s} {period}: {val_raw!r}"
                ) from e
            values_by_series[sid].append((month, val))

    out_rows: list[dict[str, Any]] = []
    months_union: set[str] = set()

    for sid, meta in sorted(
        target_meta.items(),
        key=lambda kv: (kv[1]["sector6_code"], kv[1]["rate_name"]),
    ):
        pts = values_by_series.get(sid, [])
        if not pts:
            raise RuntimeError(f"no data observations for series {sid}")
        for month, val in sorted(pts):
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

    # Sort for deterministic CSV: month, sector order, rate order.
    sector_rank = {c: i for i, c in enumerate(SECTOR6_ORDER)}
    rate_rank = {r: i for i, r in enumerate(RATE_NAME_ORDER)}

    def sort_key(r: dict[str, Any]) -> tuple[str, int, int]:
        return (
            r["month"],
            sector_rank[str(r["sector6_code"])],
            rate_rank[str(r["rate_name"])],
        )

    out_rows.sort(key=sort_key)

    FIG.mkdir(parents=True, exist_ok=True)
    INTER.mkdir(parents=True, exist_ok=True)

    pd.DataFrame(out_rows, columns=OUT_COLS).to_csv(OUT_CSV, index=False)

    sorted_months = sorted(months_union)
    first_month = sorted_months[0] if sorted_months else None
    last_month = sorted_months[-1] if sorted_months else None

    series_summary = [
        {
            "sector6_code": target_meta[sid]["sector6_code"],
            "rate_name": target_meta[sid]["rate_name"],
            "series_id": sid,
            "jolts_industry_code": target_meta[sid]["jolts_industry_code"],
        }
        for sid in sorted(target_meta, key=lambda s: (target_meta[s]["sector6_code"], s))
    ]

    meta_out: dict[str, Any] = {
        "ticket": "T-008",
        "generated_at_utc": generated_at,
        "assertion_sa_published_rates_only": (
            "Only BLS-published seasonally adjusted national industry rates were "
            "retained; no recomputation of rates from levels or across industries."
        ),
        "assertion_lineage": (
            "Sector assignment uses crosswalks/sector6_crosswalk.csv "
            "(source_program=JOLTS, is_in_scope=1). One canonical JOLTS industry "
            "code per sector6 is used for the panel; JOLTS 610000 (private "
            "educational services) also maps to PBS in the crosswalk but is "
            "excluded here in favor of published 540099 professional and business "
            "services totals."
        ),
        "month_window": {
            "min_requested": MIN_MONTH,
            "first_month_in_output": first_month,
            "last_month_in_output": last_month,
        },
        "canonical_jolts_industry_by_sector6": dict(CANONICAL_JOLTS_INDUSTRY_BY_SECTOR6),
        "crosswalk_file": str(CROSS.relative_to(ROOT)).replace("\\", "/"),
        "source_files_sha256": file_hashes,
        "retained_series": series_summary,
        "row_count": len(out_rows),
        "output_csv": str(OUT_CSV.relative_to(ROOT)).replace("\\", "/"),
    }

    OUT_META.write_text(json.dumps(meta_out, indent=2), encoding="utf-8")

    print(f"Wrote {OUT_CSV} ({len(out_rows)} rows)")
    print(f"Wrote {OUT_META}")


if __name__ == "__main__":
    main()
