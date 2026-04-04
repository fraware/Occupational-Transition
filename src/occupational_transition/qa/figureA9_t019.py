"""Ticket QA (from scripts/qa_figureA9_acs_local_composition.py)."""

from __future__ import annotations

import hashlib
import json
import math
import sys
from pathlib import Path
from urllib.request import Request

import pandas as pd

from occupational_transition.paths import repo_root

ACS_YEAR_COL = "acs_year"

AI_SHARE_COLS = [
    "high_ai_tercile_share",
    "middle_ai_tercile_share",
    "low_ai_tercile_share",
]

OCC22_SHARE_COLS = [f"occ22_share_{i}" for i in range(1, 23)]
EXP_COLS = [
    "acs_year",
    "puma",
    "population_weight_sum",
    *AI_SHARE_COLS,
    "occ22_share_sum_check",
    *OCC22_SHARE_COLS,
]

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)


def _request(url: str) -> Request:
    return Request(url, headers={"User-Agent": USER_AGENT})


def _sha256_local(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(1 << 20)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def _contiguous_share_sum_check(values: list[float], tol: float) -> bool:
    s = float(sum(values))
    return math.isfinite(s) and abs(s - 1.0) <= tol


def report(errors: list[str]) -> int:
    if errors:
        print("QA failures:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1
    print("QA OK: figureA9_acs_local_composition.csv")
    return 0


def main() -> int:
    root = repo_root()
    FIG_CSV = root / "figures" / "figureA9_acs_local_composition.csv"
    META_JSON = (
        root / "intermediate" / "figureA9_acs_local_composition_run_metadata.json"
    )
    errors: list[str] = []
    if not FIG_CSV.is_file():
        errors.append(f"missing output: {FIG_CSV}")
        return report(errors)
    if not META_JSON.is_file():
        errors.append(f"missing metadata: {META_JSON}")
        return report(errors)

    df = pd.read_csv(FIG_CSV, dtype={"puma": str})
    if list(df.columns) != EXP_COLS:
        errors.append(f"columns must be {EXP_COLS}, got {list(df.columns)}")
    if df.empty:
        errors.append("csv is empty")
        return report(errors)

    # Uniqueness: one row per PUMA.
    if df["puma"].duplicated().any():
        errors.append("duplicate puma rows found")

    # Basic validity checks.
    puma_series = df["puma"].astype(str)
    if not puma_series.str.fullmatch(r"\d{5}").all():
        errors.append("puma must be 5-digit numeric")
    if (puma_series == "00000").any():
        errors.append("puma must not be 00000")

    if (df["population_weight_sum"] <= 0).any():
        errors.append("population_weight_sum must be > 0")

    # Share ranges and finite-ness.
    share_cols = AI_SHARE_COLS + OCC22_SHARE_COLS
    for c in share_cols:
        if df[c].isna().any():
            errors.append(f"NaN in {c}")
        if not pd.to_numeric(df[c], errors="coerce").notna().all():
            errors.append(f"non-numeric values in {c}")
        if not (df[c] >= 0).all():
            errors.append(f"{c} must be >= 0")
        if not (df[c] <= 1.0 + 1e-9).all():
            errors.append(f"{c} must be <= 1")
        if df[c].apply(lambda x: not math.isfinite(float(x))).any():
            errors.append(f"{c} must be finite")

    tol = 1e-6
    # Per PUMA normalization: AI terciles sum to 1 and occ shares sum to check.
    ai_sums = df[AI_SHARE_COLS].sum(axis=1).astype(float)
    if (ai_sums - 1.0).abs().max() > tol:
        errors.append(f"ai tercile shares must sum to 1 within tol={tol}")

    occ_sum_check = df["occ22_share_sum_check"].astype(float)
    occ_shares_sum = df[OCC22_SHARE_COLS].sum(axis=1).astype(float)
    if (occ_sum_check - occ_shares_sum).abs().max() > 1e-8:
        errors.append("occ22_share_sum_check mismatch with occ22 share sums")
    if (occ_sum_check - 1.0).abs().max() > tol:
        errors.append(f"occ22 shares must sum to 1 within tol={tol}")

    # Metadata checks.
    meta = json.loads(META_JSON.read_text(encoding="utf-8"))
    if meta.get("ticket") != "T-019":
        errors.append("metadata ticket must be T-019")
    if meta.get("row_count") != len(df):
        errors.append("metadata row_count mismatch")
    if meta.get("output_csv") != "figures/figureA9_acs_local_composition.csv":
        errors.append("metadata output_csv mismatch")
    if meta.get(ACS_YEAR_COL) != int(df[ACS_YEAR_COL].iloc[0]):
        errors.append("metadata acs_year mismatch output")

    crosswalk_file = root / str(meta.get("crosswalk_file", ""))
    ai_file = root / str(meta.get("ai_terciles_file", ""))
    crosswalk_sha = str(meta.get("crosswalk_sha256", ""))
    ai_sha = str(meta.get("ai_terciles_sha256", ""))
    if crosswalk_file.is_file():
        got = _sha256_local(crosswalk_file)
        if got != crosswalk_sha:
            errors.append("crosswalk_sha256 mismatch")
    else:
        errors.append("crosswalk_file missing locally for hash verification")
    if ai_file.is_file():
        got = _sha256_local(ai_file)
        if got != ai_sha:
            errors.append("ai_terciles_sha256 mismatch")
    else:
        errors.append("ai_terciles_file missing locally for hash verification")

    hashes = meta.get("source_files_sha256", [])
    if len(hashes) != 1:
        errors.append("expected exactly one cached ACS zip entry in metadata")

    for h in hashes:
        local_path_s = h.get("local_cache_path")
        exp_sha = h.get("sha256")
        url = h.get("url")
        if not local_path_s or not exp_sha or not url:
            errors.append(f"incomplete source hash entry: {h!r}")
            continue
        local_path = root / local_path_s
        if not local_path.is_file():
            errors.append(f"missing cached source file: {local_path}")
            continue
        got = _sha256_local(local_path)
        if got != exp_sha:
            errors.append("ACS zip sha256 mismatch")

    return report(errors)


if __name__ == "__main__":
    raise SystemExit(main())
