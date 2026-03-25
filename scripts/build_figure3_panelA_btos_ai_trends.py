"""
Build figures/figure3_panelA_btos_ai_trends.csv from official Census BTOS API
published weighted shares (national NAICS all-sectors stratum naics2=XX).

Run from repo root: python scripts/build_figure3_panelA_btos_ai_trends.py
"""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from occupational_transition.http import sha256_bytes
from occupational_transition.sources.btos import (
    BTOS_API_BASE,
    STRATA_TYPE,
    STRATA_VALUE,
    build_btos_ai_trends_national_xx_cached,
)

FIG = ROOT / "figures"
INTER = ROOT / "intermediate"
OUT_CSV = FIG / "figure3_panelA_btos_ai_trends.csv"
OUT_META = INTER / "figure3_panelA_btos_ai_trends_run_metadata.json"

OUT_COLS = [
    "period_start_date",
    "btos_period_id",
    "ai_use_current_rate",
    "ai_use_expected_6m_rate",
    "source_series_id",
    "evidence_directness",
]


def main() -> None:
    periods_url = f"{BTOS_API_BASE}/periods"
    questions_url = f"{BTOS_API_BASE}/questions"

    result = build_btos_ai_trends_national_xx_cached(
        sleep_between_periods_s=0.25,
    )

    if not result.rows:
        raise RuntimeError(
            "No BTOS AI rows produced. Check API availability and dropped_periods."
        )

    df = pd.DataFrame(result.rows, columns=OUT_COLS)
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
        "periods_sha256": sha256_bytes(result.periods_raw),
        "questions_sha256": sha256_bytes(result.questions_raw),
        "per_period_data_hashes": result.per_period_data_hashes,
        "dropped_periods": result.dropped,
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
