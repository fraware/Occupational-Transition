from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import pandas as pd

from occupational_transition.http import sha256_bytes
from occupational_transition.sources.btos import (
    BTOS_API_BASE,
    STRATA_TYPE,
    STRATA_VALUE,
    build_btos_ai_trends_national_xx_cached,
)

OUT_COLS = [
    "period_start_date",
    "btos_period_id",
    "ai_use_current_rate",
    "ai_use_expected_6m_rate",
    "source_series_id",
    "evidence_directness",
]


def run(root: Path) -> tuple[Path, Path, int]:
    fig = root / "figures"
    inter = root / "intermediate"
    out_csv = fig / "figure3_panelA_btos_ai_trends.csv"
    out_meta = inter / "figure3_panelA_btos_ai_trends_run_metadata.json"

    periods_url = f"{BTOS_API_BASE}/periods"
    questions_url = f"{BTOS_API_BASE}/questions"
    result = build_btos_ai_trends_national_xx_cached(sleep_between_periods_s=0.25)
    if not result.rows:
        raise RuntimeError("No BTOS AI rows produced. Check API availability.")

    df = pd.DataFrame(result.rows, columns=OUT_COLS).sort_values("period_start_date")
    df = df.reset_index(drop=True)
    for c in ("ai_use_current_rate", "ai_use_expected_6m_rate"):
        df[c] = df[c].round(12)

    fig.mkdir(parents=True, exist_ok=True)
    inter.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_csv, index=False)

    meta = {
        "output_csv": str(out_csv.relative_to(root)).replace("\\", "/"),
        "btos_api_base": BTOS_API_BASE,
        "endpoints_used": {
            "periods": periods_url,
            "questions": questions_url,
            "data_pattern": f"{BTOS_API_BASE}/periods/{{period_id}}/data/{STRATA_TYPE}/{STRATA_VALUE}",
        },
        "national_stratum": {
            "strata_type": STRATA_TYPE,
            "strata_value": STRATA_VALUE,
            "interpretation": "Published BTOS national all-sectors NAICS stratum (XX).",
        },
        "periods_sha256": sha256_bytes(result.periods_raw),
        "questions_sha256": sha256_bytes(result.questions_raw),
        "per_period_data_hashes": result.per_period_data_hashes,
        "dropped_periods": result.dropped,
        "first_row_period_start": df["period_start_date"].iloc[0],
        "last_row_period_start": df["period_start_date"].iloc[-1],
        "today_run_date": date.today().isoformat(),
    }
    out_meta.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    return out_csv, out_meta, len(df)
