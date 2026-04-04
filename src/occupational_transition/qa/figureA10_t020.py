"""Ticket QA (from scripts/qa_figureA10_nls_longrun.py)."""

from __future__ import annotations

import hashlib
import json
import math
import sys
from pathlib import Path

import pandas as pd

from occupational_transition.paths import repo_root

EXP_COLS = [
    "survey_round",
    "baseline_ai_tercile",
    "weighted_n",
    "occupation_switch_rate",
    "employment_rate",
    "unemployment_rate",
    "nilf_rate",
    "mean_annual_earnings",
    "training_participation_rate",
    "source_program",
    "source_series_id",
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            b = f.read(1024 * 1024)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def _fail_a10(msg: str) -> int:
    print(f"QA failure: {msg}", file=sys.stderr)
    return 1


def main() -> int:
    root = repo_root()
    OUT_CSV = root / "figures" / "figureA10_nls_longrun.csv"
    OUT_META = root / "intermediate" / "figureA10_nls_longrun_run_metadata.json"
    if not OUT_CSV.exists():
        return _fail_a10(f"missing output csv: {OUT_CSV}")
    if not OUT_META.exists():
        return _fail_a10(f"missing metadata json: {OUT_META}")

    df = pd.read_csv(
        OUT_CSV,
        dtype={"survey_round": str, "baseline_ai_tercile": str},
    )
    if list(df.columns) != EXP_COLS:
        return _fail_a10(f"column order mismatch: {list(df.columns)}")
    if df.empty:
        return _fail_a10("output csv is empty")

    if df[["survey_round", "baseline_ai_tercile"]].duplicated().any():
        return _fail_a10("duplicate survey_round x baseline_ai_tercile rows")

    terciles = set(df["baseline_ai_tercile"].unique())
    if terciles != {"low", "middle", "high"}:
        return _fail_a10(f"unexpected tercile set: {sorted(terciles)}")

    for c in [
        "weighted_n",
        "occupation_switch_rate",
        "employment_rate",
        "unemployment_rate",
        "nilf_rate",
        "mean_annual_earnings",
        "training_participation_rate",
    ]:
        if pd.to_numeric(df[c], errors="coerce").isna().any():
            return _fail_a10(f"non-numeric or missing values in {c}")
        if df[c].map(lambda x: math.isfinite(float(x))).eq(False).any():
            return _fail_a10(f"non-finite values in {c}")

    if (df["weighted_n"] <= 0).any():
        return _fail_a10("weighted_n must be > 0")
    if (df["mean_annual_earnings"] <= 0).any():
        return _fail_a10("mean_annual_earnings must be > 0")

    for c in [
        "occupation_switch_rate",
        "employment_rate",
        "unemployment_rate",
        "nilf_rate",
        "training_participation_rate",
    ]:
        if (df[c] < -1e-9).any() or (df[c] > 1 + 1e-9).any():
            return _fail_a10(f"{c} out of [0,1] bounds")

    # Round ordering and completeness.
    rounds = sorted(df["survey_round"].astype(int).unique())
    for r in rounds:
        sub = df[df["survey_round"].astype(int) == r]
        if set(sub["baseline_ai_tercile"]) != {"low", "middle", "high"}:
            return _fail_a10(f"round {r} does not contain low/middle/high terciles")

    meta = json.loads(OUT_META.read_text(encoding="utf-8"))
    if meta.get("ticket") != "T-020":
        return _fail_a10("metadata ticket must equal T-020")
    if meta.get("output_csv") != "figures/figureA10_nls_longrun.csv":
        return _fail_a10("metadata output_csv mismatch")
    if int(meta.get("row_count", -1)) != len(df):
        return _fail_a10("metadata row_count mismatch")

    retained = [int(x) for x in meta.get("retained_rounds", [])]
    if retained != rounds:
        return _fail_a10("metadata retained_rounds do not match output rounds")

    hashes = meta.get("source_files_sha256", [])
    if not hashes:
        return _fail_a10("metadata source_files_sha256 missing")
    for h in hashes:
        lp = h.get("local_cache_path")
        exp = h.get("sha256")
        if not lp or not exp:
            return _fail_a10("incomplete source_files_sha256 entry")
        p = root / lp
        if not p.exists():
            return _fail_a10(f"cached source file not found: {p}")
        got = sha256_file(p)
        if got != exp:
            return _fail_a10(f"sha256 mismatch for {p}")

    for file_key, hash_key in [
        ("crosswalk_file", "crosswalk_sha256"),
        ("ai_terciles_file", "ai_terciles_sha256"),
    ]:
        p = root / str(meta.get(file_key, ""))
        if not p.exists():
            return _fail_a10(f"metadata file missing: {p}")
        got = sha256_file(p)
        if got != meta.get(hash_key):
            return _fail_a10(f"metadata hash mismatch for {file_key}")

    print("QA OK: figureA10_nls_longrun.csv")
    return 0


if __name__ == "__main__":
    main()
