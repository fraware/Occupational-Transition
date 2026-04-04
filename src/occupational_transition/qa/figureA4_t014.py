"""Ticket QA (from scripts/qa_figureA4_abs_structural_adoption.py)."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pandas as pd

from occupational_transition.paths import repo_root

EXPECTED_COLS = [
    "abs_reference_year",
    "industry_code",
    "industry_label",
    "firm_size_class",
    "measure_key",
    "measure_label",
    "weighted_share",
    "source_table_id",
]

EXPECTED_MEASURE_KEYS = {
    "ai_total_use",
    "ai_workforce_increased",
    "ai_workforce_decreased",
    "ai_workforce_unchanged",
}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    root = repo_root()
    FIG_CSV = root / "figures" / "figureA4_abs_structural_adoption.csv"
    META_JSON = (
        root / "intermediate" / "figureA4_abs_structural_adoption_run_metadata.json"
    )
    if not FIG_CSV.is_file():
        return _qa_report_stderr([f"missing {FIG_CSV}"])
    if not META_JSON.is_file():
        return _qa_report_stderr([f"missing {META_JSON}"])

    errors: list[str] = []
    df = pd.read_csv(FIG_CSV)
    if list(df.columns) != EXPECTED_COLS:
        errors.append(f"columns must be {EXPECTED_COLS}, got {list(df.columns)}")

    if df.empty:
        errors.append("output CSV must not be empty")

    if df["abs_reference_year"].astype(str).nunique() != 1:
        errors.append("abs_reference_year must be constant")

    if set(df["measure_key"]) != EXPECTED_MEASURE_KEYS:
        errors.append("measure_key set does not match expected T-014 measures")

    dup = df.duplicated(
        subset=["abs_reference_year", "industry_code", "firm_size_class", "measure_key"]
    )
    if dup.any():
        errors.append("duplicate rows detected on uniqueness key")

    shares = pd.to_numeric(df["weighted_share"], errors="coerce")
    if shares.isna().any():
        errors.append("weighted_share must be numeric")
    elif (shares < -1e-9).any() or (shares > 1.0 + 1e-9).any():
        errors.append("weighted_share must be in [0,1]")

    if (df["industry_code"].astype(str).str.len() > 2).any():
        errors.append("industry_code must be 2-digit NAICS code or '00'")

    if (
        df["source_table_id"].nunique() != 1
        or str(df["source_table_id"].iloc[0]) != "ABSTCB2018"
    ):
        errors.append("source_table_id must be ABSTCB2018")

    for col in ["industry_label", "firm_size_class", "measure_label"]:
        if df[col].isna().any() or (df[col].astype(str).str.strip() == "").any():
            errors.append(f"{col} must be non-empty")

    meta = json.loads(META_JSON.read_text(encoding="utf-8"))
    if meta.get("task_id") != "T-014":
        errors.append("metadata task_id must be T-014")
    if meta.get("geography") != "national":
        errors.append("metadata geography must be national")
    if meta.get("grouping_scope") != "industry_and_firm_size_only":
        errors.append("metadata grouping_scope mismatch")
    if meta.get("source_table_id") != "ABSTCB2018":
        errors.append("metadata source_table_id must be ABSTCB2018")

    scale = meta.get("scale", {})
    if scale.get("output_unit") != "share":
        errors.append("metadata scale.output_unit must be share")

    source_urls = [s.get("url", "") for s in meta.get("sources", [])]
    if not any("census.gov/programs-surveys/abs/data.html" in u for u in source_urls):
        errors.append("metadata sources missing ABS data hub URL")
    if not any(
        "census.gov/programs-surveys/abs/data/tables.html" in u for u in source_urls
    ):
        errors.append("metadata sources missing ABS tables hub URL")
    if not any("api.census.gov/data/2018/abstcb" in u for u in source_urls):
        errors.append("metadata sources missing ABSTCB API URL")

    artifacts = meta.get("downloaded_artifacts", [])
    json_art = None
    for a in artifacts:
        p = str(a.get("path", "")).replace("\\", "/")
        if p.endswith("raw/abs/abstcb_2018_us_national.json"):
            json_art = a
            break
    if json_art is None:
        errors.append(
            "metadata downloaded_artifacts missing local ABS API json artifact"
        )
    else:
        art_path = root / str(json_art["path"])
        if not art_path.is_file():
            errors.append(f"artifact file missing: {art_path}")
        else:
            expected = str(json_art.get("sha256", ""))
            got = sha256_file(art_path)
            if expected != got:
                errors.append("artifact sha256 mismatch for ABS API json file")

    if errors:
        return _qa_report_stderr(errors)

    print("QA OK: figureA4_abs_structural_adoption.csv")
    return 0


def _qa_report_stderr(errors: list[str]) -> int:
    import sys

    print("QA failures:", file=sys.stderr)
    for e in errors:
        print(f"  - {e}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    main()
