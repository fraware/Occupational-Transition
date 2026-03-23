"""
QA for Figure A3 CPS supplement validation output (T-013).
Exit code 1 on failure.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FIG_CSV = ROOT / "figures" / "figureA3_cps_supp_validation.csv"
META_JSON = ROOT / "intermediate" / "figureA3_cps_supp_validation_run_metadata.json"

TERCILE_ORDER = ["low", "middle", "high"]
TERCILES_SET = set(TERCILE_ORDER)

EXP_COLS = [
    "ai_relevance_tercile",
    "displaced_worker_incidence",
    "mean_current_job_tenure_years",
    "occupational_mobility_share",
    "sum_displaced_worker_person_weight",
    "sum_job_tenure_person_weight",
]


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _report(errors: list[str]) -> int:
    if errors:
        print("QA failures:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1
    print("QA OK: figureA3_cps_supp_validation.csv")
    return 0


def main() -> int:
    errors: list[str] = []

    if not FIG_CSV.is_file():
        errors.append(f"missing output: {FIG_CSV}")
        return _report(errors)

    df = pd.read_csv(FIG_CSV)
    if list(df.columns) != EXP_COLS:
        errors.append(f"columns must be {EXP_COLS}, got {list(df.columns)}")

    if df.isnull().any().any():
        errors.append("unexpected nulls in output CSV")

    if len(df) != 3:
        errors.append(f"output must have exactly 3 rows (low/middle/high), got {len(df)}")

    if not set(df["ai_relevance_tercile"].unique()) <= TERCILES_SET:
        errors.append(f"invalid tercile labels: {df['ai_relevance_tercile'].unique()}")

    # Strict semantic ordering contract.
    got_order = df["ai_relevance_tercile"].astype(str).tolist()
    if got_order != TERCILE_ORDER:
        errors.append(f"ai_relevance_tercile rows must be ordered {TERCILE_ORDER}, got {got_order}")

    # Numeric bounds.
    for col in ("displaced_worker_incidence", "occupational_mobility_share"):
        if (df[col] < -1e-8).any() or (df[col] > 1 + 1e-8).any():
            errors.append(f"{col} must be in [0,1]")

    if (df["mean_current_job_tenure_years"] < -1e-8).any() or not pd.to_numeric(
        df["mean_current_job_tenure_years"], errors="coerce"
    ).notna().all():
        errors.append("mean_current_job_tenure_years must be finite and nonnegative")

    if (df["sum_displaced_worker_person_weight"] <= 0).any():
        errors.append("sum_displaced_worker_person_weight must be positive")
    if (df["sum_job_tenure_person_weight"] <= 0).any():
        errors.append("sum_job_tenure_person_weight must be positive")

    # Metadata checks.
    if not META_JSON.is_file():
        errors.append(f"missing metadata: {META_JSON}")
        return _report(errors)

    meta = json.loads(META_JSON.read_text(encoding="utf-8"))
    if meta.get("task_id") != "T-013":
        errors.append(f"metadata task_id must be T-013, got {meta.get('task_id')}")

    if meta.get("weight_variable_displacement") != "PWSUPWGT":
        errors.append("metadata weight_variable_displacement must be PWSUPWGT")
    if meta.get("weight_variable_tenure_mobility") != "PWTENWGT":
        errors.append("metadata weight_variable_tenure_mobility must be PWTENWGT")

    if not meta.get("tenure_years_scaling_rule"):
        errors.append("metadata must include tenure_years_scaling_rule")
    if not meta.get("weight_scaling_rule"):
        errors.append("metadata must include weight_scaling_rule")

    if not isinstance(meta.get("sources"), list) or len(meta["sources"]) < 2:
        errors.append("metadata sources must include jan24pub.csv and cpsjan24.pdf entries")

    # Hash checks for source files (expected to be cached by build).
    raw_supp = ROOT / "raw" / "cps" / "supp"
    jan_csv = raw_supp / "jan24pub.csv"
    jan_pdf = raw_supp / "cpsjan24.pdf"
    if not jan_csv.is_file():
        errors.append(f"missing cached source file for hash check: {jan_csv}")
    else:
        src_csv = next((s for s in meta["sources"] if s.get("file_name") == "jan24pub.csv"), None)
        if src_csv is None or not src_csv.get("file_sha256"):
            errors.append("metadata sources missing jan24pub.csv file_sha256")
        else:
            if _sha256_file(jan_csv) != src_csv["file_sha256"]:
                errors.append("jan24pub.csv sha256 mismatch vs metadata")

    if not jan_pdf.is_file():
        errors.append(f"missing cached source file for hash check: {jan_pdf}")
    else:
        src_pdf = next((s for s in meta["sources"] if s.get("file_name") == "cpsjan24.pdf"), None)
        if src_pdf is None or not src_pdf.get("file_sha256"):
            errors.append("metadata sources missing cpsjan24.pdf file_sha256")
        else:
            if _sha256_file(jan_pdf) != src_pdf["file_sha256"]:
                errors.append("cpsjan24.pdf sha256 mismatch vs metadata")

    # Hash checks for frozen lineage.
    lin = meta.get("lineage_file_sha256") or {}
    crosswalk_path = ROOT / "crosswalks" / "occ22_crosswalk.csv"
    terciles_path = ROOT / "intermediate" / "ai_relevance_terciles.csv"
    if "crosswalks/occ22_crosswalk.csv" not in lin:
        errors.append("metadata lineage_file_sha256 missing crosswalk hash")
    else:
        if crosswalk_path.is_file() and _sha256_file(crosswalk_path) != lin["crosswalks/occ22_crosswalk.csv"]:
            errors.append("occ22_crosswalk.csv sha256 mismatch vs metadata")

    if "intermediate/ai_relevance_terciles.csv" not in lin:
        errors.append("metadata lineage_file_sha256 missing terciles hash")
    else:
        if terciles_path.is_file() and _sha256_file(terciles_path) != lin["intermediate/ai_relevance_terciles.csv"]:
            errors.append("ai_relevance_terciles.csv sha256 mismatch vs metadata")

    return _report(errors)


if __name__ == "__main__":
    raise SystemExit(main())

