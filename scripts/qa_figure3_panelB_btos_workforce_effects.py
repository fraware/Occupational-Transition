"""
QA for figures/figure3_panelB_btos_workforce_effects.csv and run metadata.

Run from repo root: python scripts/qa_figure3_panelB_btos_workforce_effects.py
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FIG_CSV = ROOT / "figures" / "figure3_panelB_btos_workforce_effects.csv"
META_JSON = ROOT / (
    "intermediate/figure3_panelB_btos_workforce_effects_run_metadata.json"
)

EXPECTED_KEYS = [
    "perform_task_previously_done_by_employee",
    "supplement_or_enhance_task_performed_by_employee",
    "introduce_new_task_not_previously_done_by_employee",
    "employment_increased",
    "employment_decreased",
    "employment_did_not_change",
]

EXPECTED_COLS = [
    "category_key",
    "category_label",
    "weighted_share",
    "window_start",
    "window_end",
    "source_series_id",
    "evidence_directness",
]

WINDOW_START = "2023-12-04"
WINDOW_END = "2024-02-25"


def main() -> None:
    errors: list[str] = []

    if not FIG_CSV.is_file():
        raise SystemExit(f"missing {FIG_CSV}")
    if not META_JSON.is_file():
        raise SystemExit(f"missing {META_JSON}")

    df = pd.read_csv(FIG_CSV)
    if list(df.columns) != EXPECTED_COLS:
        errors.append(f"columns must be {EXPECTED_COLS}, got {list(df.columns)}")

    if len(df) != 6:
        errors.append(f"expected 6 rows, got {len(df)}")

    keys = df["category_key"].tolist()
    if set(keys) != set(EXPECTED_KEYS):
        errors.append(f"category_key set mismatch: {keys}")

    if list(df["category_key"]) != EXPECTED_KEYS:
        errors.append("category_key ordering must match frozen design order")

    if df["window_start"].nunique() != 1 or df["window_end"].nunique() != 1:
        errors.append("window_start and window_end must be constant across rows")
    elif (
        str(df["window_start"].iloc[0]) != WINDOW_START
        or str(df["window_end"].iloc[0]) != WINDOW_END
    ):
        errors.append("window bounds do not match frozen T-007 design")

    cl = df["category_label"]
    if cl.isna().any() or (cl.astype(str) == "").any():
        errors.append("category_label must be non-empty")

    sid = df["source_series_id"]
    if sid.isna().any() or (sid.astype(str) == "").any():
        errors.append("source_series_id must be non-empty")
    allowed_directness = {"direct_published", "proxy_mapping", "derived_transform"}
    got_directness = set(df["evidence_directness"].astype(str).unique())
    if not got_directness.issubset(allowed_directness):
        errors.append("invalid evidence_directness values")

    shares = df["weighted_share"].astype(float)
    if shares.isna().any():
        errors.append("weighted_share has missing values")
    if (shares < -1e-9).any() or (shares > 1.0 + 1e-9).any():
        errors.append("weighted_share must be in [0, 1]")

    meta = json.loads(META_JSON.read_text(encoding="utf-8"))
    if meta.get("geography") != "national":
        errors.append("metadata geography must be national")
    w0 = meta.get("window_start")
    w1 = meta.get("window_end")
    if w0 != WINDOW_START or w1 != WINDOW_END:
        errors.append("metadata window bounds must match CSV")

    if meta.get("universe_scope_code") != 2:
        errors.append(
            "metadata universe_scope_code must be 2 "
            "(AI-using firms, last 6 months)"
        )

    pmap = meta.get("category_mapping") or {}
    if pmap.get("scope_code") != 2:
        errors.append("category_mapping.scope_code must be 2")

    src = meta.get("primary_source_url", "")
    if "census.gov" not in src.lower() or "AI_Supplement_Table" not in src:
        errors.append("primary_source_url must point to Census AI_Supplement_Table.xlsx")

    if not meta.get("primary_file_sha256"):
        errors.append("primary_file_sha256 must be present")

    # Fallback documentation consistency
    uf = meta.get("used_fallback_workbook")
    if uf is True:
        if not meta.get("fallback_file_sha256"):
            errors.append(
                "fallback_file_sha256 required when used_fallback_workbook is true"
            )
    elif uf is False:
        pass
    else:
        errors.append("used_fallback_workbook must be boolean")

    if meta.get("fallback_reason") in (None, ""):
        errors.append(
            "fallback_reason must document primary vs fallback outcome"
        )

    cats = pmap.get("category_to_source") or {}
    for k in EXPECTED_KEYS:
        if k not in cats:
            errors.append(f"category_to_source missing {k}")

    if errors:
        raise SystemExit("QA failures:\n- " + "\n- ".join(errors))

    print("QA OK: figure3_panelB_btos_workforce_effects.csv")


if __name__ == "__main__":
    main()
