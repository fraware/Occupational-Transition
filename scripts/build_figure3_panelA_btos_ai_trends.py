"""
Build figures/figure3_panelA_btos_ai_trends.csv from official Census BTOS API
published weighted shares (national NAICS all-sectors stratum naics2=XX).

Run from repo root: python scripts/build_figure3_panelA_btos_ai_trends.py
"""

from __future__ import annotations

import hashlib
import json
import time
from datetime import date, datetime
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures"
INTER = ROOT / "intermediate"
OUT_CSV = FIG / "figure3_panelA_btos_ai_trends.csv"
OUT_META = INTER / "figure3_panelA_btos_ai_trends_run_metadata.json"

BTOS_API_BASE = "https://www.census.gov/hfp/btos/api"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)

# National published tabulation: all NAICS sectors (BTOS stratum naics2 XX).
STRATA_TYPE = "naics2"
STRATA_VALUE = "XX"

OUT_COLS = [
    "period_start_date",
    "btos_period_id",
    "ai_use_current_rate",
    "ai_use_expected_6m_rate",
    "source_series_id",
]


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
    """Parse BTOS API COLLECTION_START like '28-AUG-23 12.00.00.000000 AM'."""
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
    """Periods where the questions catalog includes AI core wording."""
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
    """Return (current_yes_share, expected_6m_yes_share) in 0..1 from one data payload."""
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


def main() -> None:
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

    rows_out: list[dict[str, Any]] = []
    dropped: list[dict[str, Any]] = []
    data_hashes: list[dict[str, str]] = []

    for pid in sorted(int(x) for x in ai_periods):
        try:
            pkey = str(pid)
            if pkey not in period_by_id:
                dropped.append(
                    {"period_id": pkey, "reason": "missing_period_metadata"}
                )
                continue
            meta = period_by_id[pkey]
            start_s = str(meta.get("COLLECTION_START") or "")
            try:
                dt = parse_collection_start(start_s)
            except ValueError as e:
                dropped.append(
                    {
                        "period_id": pkey,
                        "reason": f"bad_collection_start: {e}",
                    }
                )
                continue

            data_url = (
                f"{BTOS_API_BASE}/periods/{pkey}/data/"
                f"{STRATA_TYPE}/{STRATA_VALUE}"
            )
            try:
                data_raw = _fetch_text(data_url).encode("utf-8")
            except (HTTPError, URLError, OSError, TimeoutError) as e:
                dropped.append(
                    {"period_id": pkey, "reason": f"fetch_error: {e}"}
                )
                continue

            payload = json.loads(data_raw.decode("utf-8"))
            if payload is None:
                dropped.append(
                    {
                        "period_id": pkey,
                        "reason": "api_returned_null_payload",
                    }
                )
                continue

            cur, fut = extract_yes_rates(payload)
            if cur is None or fut is None:
                dropped.append(
                    {
                        "period_id": pkey,
                        "reason": f"missing_yes_estimate cur={cur} fut={fut}",
                    }
                )
                continue

            rows_out.append(
                {
                    "period_start_date": dt.date().isoformat(),
                    "btos_period_id": pkey,
                    "ai_use_current_rate": cur,
                    "ai_use_expected_6m_rate": fut,
                    "source_series_id": f"{STRATA_TYPE}_{STRATA_VALUE}",
                }
            )
            data_hashes.append(
                {"period_id": pkey, "data_sha256": sha256_bytes(data_raw)}
            )
        finally:
            time.sleep(0.25)

    if not rows_out:
        raise RuntimeError(
            "No BTOS AI rows produced. Check API availability and dropped_periods."
        )

    df = pd.DataFrame(rows_out, columns=OUT_COLS)
    df = df.sort_values("period_start_date").reset_index(drop=True)
    for c in ("ai_use_current_rate", "ai_use_expected_6m_rate"):
        df[c] = df[c].round(12)

    FIG.mkdir(parents=True, exist_ok=True)
    INTER.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_CSV, index=False)

    meta = {
        "output_csv": str(OUT_CSV.relative_to(ROOT)),
        "btos_api_base": BTOS_API_BASE,
        "endpoints_used": {
            "periods": periods_url,
            "questions": questions_url,
            "data_pattern": (
                f"{BTOS_API_BASE}/periods/{{period_id}}/data/"
                f"{STRATA_TYPE}/{STRATA_VALUE}"
            ),
        },
        "national_stratum": {
            "strata_type": STRATA_TYPE,
            "strata_value": STRATA_VALUE,
            "interpretation": (
                "Published BTOS national all-sectors NAICS stratum (XX) "
                "weights per BTOS methodology"
            ),
        },
        "rates_extracted": (
            "ESTIMATE_PERCENTAGE for ANSWER Yes and OPTION_TEXT "
            "AI current / AI future; divided by 100 for 0..1 share"
        ),
        "periods_sha256": sha256_bytes(periods_raw),
        "questions_sha256": sha256_bytes(questions_raw),
        "per_period_data_hashes": data_hashes,
        "dropped_periods": dropped,
        "first_row_period_start": df["period_start_date"].iloc[0],
        "last_row_period_start": df["period_start_date"].iloc[-1],
        "today_run_date": date.today().isoformat(),
        "notes": (
            "AI core questions first appear in the BTOS questions catalog at "
            "PERIOD_ID 31 (collection starting 2023-09-11 per API). "
            "Period 30 (2023-08-28) has no AI rows in the questions endpoint."
        ),
    }
    OUT_META.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"Wrote {OUT_CSV} ({len(df)} rows). Metadata: {OUT_META}")


if __name__ == "__main__":
    main()
