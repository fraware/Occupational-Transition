"""
Build intermediate/btos_sector_ai_use_monthly.csv: BTOS current AI-use share by
frozen sector6 and calendar month, with 3-month trailing smoothing.

Uses Census BTOS API naics2 strata aggregated to sector6 (unweighted mean of
constituent naics2 published shares within each collection period / month).

Run from repo root: python scripts/build_btos_sector_ai_use_monthly.py
"""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import pandas as pd

from occupational_transition.awes_alpi_common import SECTOR6_ORDER


@dataclass(frozen=True)
class BtosSectorAiUsePaths:
    root: Path
    inter: Path
    out_csv: Path
    out_meta: Path


def _btos_paths(root: Path) -> BtosSectorAiUsePaths:
    inter = root / "intermediate"
    return BtosSectorAiUsePaths(
        root=root,
        inter=inter,
        out_csv=inter / "btos_sector_ai_use_monthly.csv",
        out_meta=inter / "btos_sector_ai_use_monthly_run_metadata.json",
    )


def run(root: Path) -> None:
    build_btos_sector_ai_use_monthly(_btos_paths(root))


BTOS_API_BASE = "https://www.census.gov/hfp/btos/api"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)

STRATA_TYPE = "naics2"

# BTOS naics2 codes that map into the paper's frozen six sectors (PR-000).
NAICS2_TO_SECTOR6: dict[str, str] = {
    "31": "MFG",
    "44": "RET",
    "51": "INF",
    "52": "FAS",
    "53": "FAS",
    "54": "PBS",
    "55": "PBS",
    "56": "PBS",
    "61": "PBS",
    "62": "HCS",
}

SECTOR6_LABELS: dict[str, str] = {
    "MFG": "Manufacturing",
    "INF": "Information",
    "FAS": "Financial activities",
    "PBS": "Professional and business services",
    "HCS": "Health care and social assistance",
    "RET": "Retail trade",
}


def _request(url: str) -> Request:
    return Request(url, headers={"User-Agent": USER_AGENT})


def _fetch_text(url: str) -> str:
    with urlopen(_request(url), timeout=180) as resp:
        return resp.read().decode("utf-8", "replace")


def _fetch_json(url: str) -> Any:
    return json.loads(_fetch_text(url))


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse_collection_start(s: str) -> datetime:
    for fmt in (
        "%d-%b-%y %I.%M.%S.%f %p",
        "%d-%b-%Y %I.%M.%S.%f %p",
    ):
        try:
            return datetime.strptime(s.strip(), fmt)
        except ValueError:
            continue
    raise ValueError(f"Unrecognized COLLECTION_START: {s!r}")


def period_ids_with_ai_questions(questions_rows: list[dict[str, Any]]) -> set[str]:
    out: set[str] = set()
    for row in questions_rows:
        q = str(row.get("QUESTION") or "")
        if "intelligence" in q.lower():
            pid = row.get("PERIOD_ID")
            if pid is not None:
                out.add(str(pid))
    return out


def extract_yes_rates(
    data_obj: dict[str, Any] | None,
) -> tuple[float | None, float | None]:
    if not data_obj:
        return None, None
    cur: float | None = None
    fut: float | None = None
    for row in data_obj.values():
        if not isinstance(row, dict):
            continue
        if (
            row.get("OPTION_TEXT") == "AI current"
            and row.get("ANSWER") == "Yes"
        ):
            ep = row.get("ESTIMATE_PERCENTAGE")
            if ep is not None and str(ep).strip() != "":
                cur = float(ep) / 100.0
        if (
            row.get("OPTION_TEXT") == "AI future"
            and row.get("ANSWER") == "Yes"
        ):
            ep = row.get("ESTIMATE_PERCENTAGE")
            if ep is not None and str(ep).strip() != "":
                fut = float(ep) / 100.0
    return cur, fut


def trailing_3_month_mean(series: pd.Series) -> pd.Series:
    """Trailing mean over up to 3 ending at t; from series start if shorter."""
    vals = series.astype(float).to_numpy()
    out = []
    for i in range(len(vals)):
        start = max(0, i - 2)
        out.append(float(pd.Series(vals[start : i + 1]).mean()))
    return pd.Series(out, index=series.index)


def build_btos_sector_ai_use_monthly(p: BtosSectorAiUsePaths) -> None:
    generated_at = datetime.now(timezone.utc).isoformat()
    p.inter.mkdir(parents=True, exist_ok=True)

    periods_url = f"{BTOS_API_BASE}/periods"
    questions_url = f"{BTOS_API_BASE}/questions"
    periods_raw = _fetch_text(periods_url).encode("utf-8")
    questions_raw = _fetch_text(questions_url).encode("utf-8")
    periods_list = json.loads(periods_raw.decode("utf-8"))
    questions_list = json.loads(questions_raw.decode("utf-8"))
    if not isinstance(periods_list, list) or not isinstance(questions_list, list):
        raise RuntimeError("Unexpected BTOS API JSON types")

    ai_periods = period_ids_with_ai_questions(questions_list)
    period_by_id = {str(p["PERIOD_ID"]): p for p in periods_list}

    naics_codes = sorted(NAICS2_TO_SECTOR6.keys())
    cell_rows: list[dict[str, Any]] = []
    dropped: list[dict[str, Any]] = []
    data_hashes: list[dict[str, str]] = []

    for pid in sorted(int(x) for x in ai_periods):
        pkey = str(pid)
        if pkey not in period_by_id:
            dropped.append({"period_id": pkey, "reason": "missing_period_metadata"})
            continue
        meta = period_by_id[pkey]
        start_s = str(meta.get("COLLECTION_START") or "")
        try:
            dt = parse_collection_start(start_s)
        except ValueError as e:
            dropped.append({"period_id": pkey, "reason": f"bad_collection_start: {e}"})
            continue
        month = f"{dt.year:04d}-{dt.month:02d}"

        for n2 in naics_codes:
            data_url = f"{BTOS_API_BASE}/periods/{pkey}/data/{STRATA_TYPE}/{n2}"
            try:
                data_raw = _fetch_text(data_url).encode("utf-8")
            except (HTTPError, URLError, OSError, TimeoutError) as e:
                dropped.append(
                    {
                        "period_id": pkey,
                        "naics2": n2,
                        "reason": f"fetch_error: {e}",
                    }
                )
                continue
            payload = json.loads(data_raw.decode("utf-8"))
            cur, _fut = extract_yes_rates(payload)
            if cur is None:
                dropped.append(
                    {
                        "period_id": pkey,
                        "naics2": n2,
                        "reason": "missing_ai_current_rate",
                    }
                )
                continue
            sec = NAICS2_TO_SECTOR6[n2]
            cell_rows.append(
                {
                    "month": month,
                    "btos_period_id": pkey,
                    "period_start_date": dt.date().isoformat(),
                    "naics2": n2,
                    "sector6_code": sec,
                    "btos_ai_use_share_raw_cell": round(cur, 12),
                }
            )
            data_hashes.append(
                {
                    "period_id": pkey,
                    "naics2": n2,
                    "data_sha256": sha256_bytes(data_raw),
                }
            )
        time.sleep(0.25)

    if not cell_rows:
        raise RuntimeError("No BTOS sector cells produced; check API and dropped log.")

    cells = pd.DataFrame(cell_rows)
    # Mean over periods and naics2 cells that fall in the same calendar month and sector6.
    g = cells.groupby(["month", "sector6_code"], as_index=False)[
        "btos_ai_use_share_raw_cell"
    ].mean()
    g = g.rename(columns={"btos_ai_use_share_raw_cell": "btos_ai_use_share_raw"})

    out_rows: list[dict[str, Any]] = []
    for sec in SECTOR6_ORDER:
        sub = g[g["sector6_code"] == sec].sort_values("month").reset_index(drop=True)
        if sub.empty:
            continue
        smooth = trailing_3_month_mean(sub["btos_ai_use_share_raw"])
        for i, r in sub.iterrows():
            out_rows.append(
                {
                    "month": str(r["month"]),
                    "sector6_code": sec,
                    "sector6_label": SECTOR6_LABELS[sec],
                    "btos_ai_use_share_raw": float(r["btos_ai_use_share_raw"]),
                    "btos_ai_use_share_3m": float(smooth.iloc[i]),
                }
            )

    out = pd.DataFrame(out_rows)
    out = out.sort_values(["month", "sector6_code"]).reset_index(drop=True)
    out.to_csv(p.out_csv, index=False)

    meta = {
        "output_csv": str(p.out_csv.relative_to(p.root)).replace("\\", "/"),
        "generated_at_utc": generated_at,
        "formula_version": "AWES BTOS sector monthly v1",
        "smoothing_rule": (
            "btos_ai_use_share_3m = trailing mean of up to 3 consecutive "
            "calendar months of btos_ai_use_share_raw (partial at series start)."
        ),
        "month_rule": (
            "Calendar month assigned from BTOS COLLECTION_START month "
            "(proxy when collection-end metadata unavailable)."
        ),
        "aggregation_rule": (
            "Within month and sector6, mean over BTOS periods and over naics2 "
            "cells published for that sector6."
        ),
        "source_signal": "BTOS AI current (not expected-next-6-month)",
        "endpoints_used": {
            "periods": periods_url,
            "questions": questions_url,
            "data_pattern": (
                f"{BTOS_API_BASE}/periods/{{period_id}}/data/naics2/{{naics2}}"
            ),
        },
        "periods_sha256": sha256_bytes(periods_raw),
        "questions_sha256": sha256_bytes(questions_raw),
        "per_cell_data_hashes_sample": data_hashes[:50],
        "per_cell_data_hashes_count": len(data_hashes),
        "dropped_requests": dropped,
        "row_count": int(len(out)),
    }
    p.out_meta.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"Wrote {p.out_csv} ({len(out)} rows)")

