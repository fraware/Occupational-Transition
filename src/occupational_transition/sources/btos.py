"""Census Business Trends and Outlook Survey (BTOS) public API helpers."""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Callable
from urllib.error import HTTPError, URLError

from occupational_transition.http import fetch_text_cached, sha256_bytes

BTOS_API_BASE = "https://www.census.gov/hfp/btos/api"

# National published tabulation: all NAICS sectors (BTOS stratum naics2 XX).
STRATA_TYPE = "naics2"
STRATA_VALUE = "XX"


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
    """
    Return (current_yes_share, expected_6m_yes_share) in 0..1 from one data payload.
    """
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


@dataclass
class BtosNationalTrendsResult:
    """Output of :func:`build_btos_ai_trends_national_xx`."""

    rows: list[dict[str, Any]]
    dropped: list[dict[str, Any]]
    periods_raw: bytes
    questions_raw: bytes
    per_period_data_hashes: list[dict[str, str]] = field(default_factory=list)


def build_btos_ai_trends_national_xx(
    fetch_text: Callable[[str], str],
    *,
    sleep_between_periods_s: float = 0.25,
    api_base: str = BTOS_API_BASE,
    strata_type: str = STRATA_TYPE,
    strata_value: str = STRATA_VALUE,
) -> BtosNationalTrendsResult:
    """
    Build national naics2=XX AI current / expected 6m Yes shares for each BTOS period
    that has AI questions in the catalog and complete data payload.
    """
    periods_url = f"{api_base}/periods"
    questions_url = f"{api_base}/questions"
    periods_raw = fetch_text(periods_url).encode("utf-8")
    questions_raw = fetch_text(questions_url).encode("utf-8")

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
                f"{api_base}/periods/{pkey}/data/{strata_type}/{strata_value}"
            )
            try:
                data_raw = fetch_text(data_url).encode("utf-8")
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
                    "source_series_id": f"{strata_type}_{strata_value}",
                    "evidence_directness": "direct_published",
                }
            )
            data_hashes.append(
                {"period_id": pkey, "data_sha256": sha256_bytes(data_raw)}
            )
        finally:
            time.sleep(sleep_between_periods_s)

    return BtosNationalTrendsResult(
        rows=rows_out,
        dropped=dropped,
        periods_raw=periods_raw,
        questions_raw=questions_raw,
        per_period_data_hashes=data_hashes,
    )


def build_btos_ai_trends_national_xx_cached(
    *,
    cache_dir: Path | None = None,
    sleep_between_periods_s: float = 0.25,
    api_base: str = BTOS_API_BASE,
    strata_type: str = STRATA_TYPE,
    strata_value: str = STRATA_VALUE,
    timeout: float = 180.0,
    retries: int = 3,
) -> BtosNationalTrendsResult:
    """
    Convenience wrapper around :func:`build_btos_ai_trends_national_xx` that
    caches all BTOS JSON endpoints under a local cache directory.
    """

    def ft(url: str) -> str:
        return fetch_text_cached(
            url,
            cache_dir=cache_dir,
            timeout=timeout,
            retries=retries,
        )

    return build_btos_ai_trends_national_xx(
        ft,
        sleep_between_periods_s=sleep_between_periods_s,
        api_base=api_base,
        strata_type=strata_type,
        strata_value=strata_value,
    )
