"""T-009: Figure 4 Panel B CES sector payroll index from BLS LABSTAT."""

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

CES_BASE = "https://download.bls.gov/pub/time.series/ce/"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)

MIN_MONTH = "2019-01"
BASE_MONTH = "2023-08"

# Canonical CES national supersector totals (avoids double-counting 30/31/32 for MFG).
# Maps sector6_code -> CES supersector_code (2-digit string).
CANONICAL_SUPERSECTOR_BY_SECTOR6: dict[str, str] = {
    "MFG": "30",
    "RET": "42",
    "INF": "50",
    "FAS": "55",
    "PBS": "60",
    "HCS": "65",
}

SECTOR6_ORDER: list[str] = ["MFG", "INF", "FAS", "PBS", "HCS", "RET"]

DATA_FILE_SA_AE = "ce.data.01a.CurrentSeasAE"

PROVENANCE_FILES: list[str] = [
    "ce.txt",
    "ce.series",
    "ce.supersector",
    "ce.industry",
    "ce.datatype",
    "ce.period",
    "ce.seasonal",
    DATA_FILE_SA_AE,
]

OUT_COLS = [
    "month",
    "sector6_code",
    "sector6_label",
    "ces_payroll_employment_thousands",
    "index_aug2023_100",
    "series_id",
]


def _request(url: str) -> Request:
    return Request(url, headers={"User-Agent": USER_AGENT})


def fetch_bytes(url: str) -> bytes:
    with urlopen(_request(url), timeout=300) as resp:
        return resp.read()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def normalize_ce_row(row: dict[str, str]) -> dict[str, str]:
    return {
        k.strip(): (v.strip() if isinstance(v, str) else v)
        for k, v in row.items()
    }


def load_ce_series_table(text: str) -> list[dict[str, str]]:
    rows = list(csv.DictReader(StringIO(text), delimiter="\t"))
    return [normalize_ce_row(r) for r in rows]


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


def ces_supersector_total_industry_code(supersector: str) -> str:
    """8-digit CES industry_code for published supersector total employment."""
    return f"{supersector.strip()}000000"


def load_sector6_labels_from_crosswalk(cross: Path) -> dict[str, str]:
    """Labels for canonical CES supersectors from PR-000 crosswalk."""
    df = pd.read_csv(cross)
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
        if sc in inv:
            sec = inv[sc]
            label = str(row.get("sector6_label", "")).strip()
            if label and sec not in out:
                out[sec] = label
    for sec in CANONICAL_SUPERSECTOR_BY_SECTOR6:
        if sec not in out:
            raise RuntimeError(
                f"missing CES ces_supersector label in crosswalk for {sec}"
            )
    return out


def resolve_series_ids(series_rows: list[dict[str, str]]) -> dict[str, str]:
    """sector6_code -> series_id for national SA all-employees supersector totals."""
    out: dict[str, str] = {}
    for sec, ss in CANONICAL_SUPERSECTOR_BY_SECTOR6.items():
        want_ind = ces_supersector_total_industry_code(ss)
        matches: list[str] = []
        for row in series_rows:
            if row.get("seasonal") != "S":
                continue
            if row.get("data_type_code") != "01":
                continue
            if row.get("supersector_code") != ss:
                continue
            if row.get("industry_code") != want_ind:
                continue
            sid = row.get("series_id", "").strip()
            if sid:
                matches.append(sid)
        if len(matches) != 1:
            raise RuntimeError(
                f"expected exactly one CES series for {sec} "
                f"(supersector {ss}), got {len(matches)}"
            )
        out[sec] = matches[0]
    return out


def run(root: Path) -> None:
    """T-009 build entrypoint for ``run_step``."""
    fig = root / "figures"
    inter = root / "intermediate"
    cross = root / "crosswalks" / "sector6_crosswalk.csv"
    out_csv = fig / "figure4_panelB_ces_sector_index.csv"
    out_meta = inter / "figure4_panelB_ces_sector_index_run_metadata.json"

    generated_at = datetime.now(timezone.utc).isoformat()
    sector6_labels = load_sector6_labels_from_crosswalk(cross)

    file_hashes: list[dict[str, str]] = []
    series_text: str | None = None
    for fname in PROVENANCE_FILES:
        url = f"{CES_BASE}{fname}"
        raw = fetch_bytes(url)
        file_hashes.append(
            {"file_name": fname, "url": url, "sha256": sha256_bytes(raw)}
        )
        if fname == "ce.series":
            series_text = raw.decode("utf-8", "replace")

    if series_text is None:
        raise RuntimeError("ce.series not loaded")

    series_rows = load_ce_series_table(series_text)
    series_by_sector = resolve_series_ids(series_rows)
    target_ids = set(series_by_sector.values())

    values_by_series: dict[str, list[tuple[str, float]]] = defaultdict(list)

    data_url = f"{CES_BASE}{DATA_FILE_SA_AE}"
    with urlopen(_request(data_url), timeout=600) as resp:
        header = True
        for raw_line in resp:
            line = raw_line.decode("utf-8", "replace")
            if header:
                header = False
                continue
            parsed = parse_data_line(line)
            if parsed is None:
                continue
            sid, year_s, period, val_raw = parsed
            if sid not in target_ids:
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

    # Base-month employment for indexing.
    base_emp: dict[str, float] = {}
    for sec, sid in series_by_sector.items():
        pts = {m: v for m, v in values_by_series.get(sid, [])}
        if BASE_MONTH not in pts:
            raise RuntimeError(
                f"missing {BASE_MONTH} observation for series {sid} ({sec})"
            )
        base_emp[sec] = pts[BASE_MONTH]

    out_rows: list[dict[str, Any]] = []
    months_union: set[str] = set()

    for sec in SECTOR6_ORDER:
        sid = series_by_sector[sec]
        base = base_emp[sec]
        for month, emp in sorted(values_by_series.get(sid, [])):
            months_union.add(month)
            idx = 100.0 * (emp / base)
            out_rows.append(
                {
                    "month": month,
                    "sector6_code": sec,
                    "sector6_label": sector6_labels[sec],
                    "ces_payroll_employment_thousands": emp,
                    "index_aug2023_100": idx,
                    "series_id": sid,
                }
            )

    sector_rank = {c: i for i, c in enumerate(SECTOR6_ORDER)}

    def sort_key(r: dict[str, Any]) -> tuple[str, int]:
        return (r["month"], sector_rank[str(r["sector6_code"])])

    out_rows.sort(key=sort_key)

    sorted_months = sorted(months_union)
    first_month = sorted_months[0] if sorted_months else None
    last_month = sorted_months[-1] if sorted_months else None

    fig.mkdir(parents=True, exist_ok=True)
    inter.mkdir(parents=True, exist_ok=True)

    pd.DataFrame(out_rows, columns=OUT_COLS).to_csv(out_csv, index=False)

    retained = [
        {
            "sector6_code": sec,
            "ces_supersector_code": CANONICAL_SUPERSECTOR_BY_SECTOR6[sec],
            "ces_industry_code": ces_supersector_total_industry_code(
                CANONICAL_SUPERSECTOR_BY_SECTOR6[sec]
            ),
            "series_id": series_by_sector[sec],
        }
        for sec in SECTOR6_ORDER
    ]

    meta_out: dict[str, Any] = {
        "ticket": "T-009",
        "generated_at_utc": generated_at,
        "assertion_sa_published_ces_only": (
            "Only BLS-published national CES seasonally adjusted "
            "all-employees employment (datatype 01) was used; no modeled "
            "reconstruction beyond indexing published levels."
        ),
        "assertion_lineage": (
            "Sector labels and canonical CES supersector totals follow "
            "crosswalks/sector6_crosswalk.csv (source_program=CES, "
            "source_level=ces_supersector, is_in_scope=1). "
            "Supersector 65 (private education and health services) is mapped "
            "to sector6 HCS per PR-000; it combines private education and "
            "health services employment at the CES supersector level."
        ),
        "month_window": {
            "min_requested": MIN_MONTH,
            "index_base_month": BASE_MONTH,
            "first_month_in_output": first_month,
            "last_month_in_output": last_month,
        },
        "canonical_ces_supersector_by_sector6": dict(
            CANONICAL_SUPERSECTOR_BY_SECTOR6
        ),
        "crosswalk_file": str(cross.relative_to(root)).replace("\\", "/"),
        "source_files_sha256": file_hashes,
        "retained_series": retained,
        "row_count": len(out_rows),
        "output_csv": str(out_csv.relative_to(root)).replace("\\", "/"),
    }

    out_meta.write_text(json.dumps(meta_out, indent=2), encoding="utf-8")

    print(f"Wrote {out_csv} ({len(out_rows)} rows)")
    print(f"Wrote {out_meta}")
