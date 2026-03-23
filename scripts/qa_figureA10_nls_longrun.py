"""QA checks for T-020 Figure A10 output."""

from __future__ import annotations

import hashlib
import json
import math
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT_CSV = ROOT / "figures" / "figureA10_nls_longrun.csv"
OUT_META = ROOT / "intermediate" / "figureA10_nls_longrun_run_metadata.json"

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


def fail(msg: str) -> None:
    print(f"QA failure: {msg}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    if not OUT_CSV.exists():
        fail(f"missing output csv: {OUT_CSV}")
    if not OUT_META.exists():
        fail(f"missing metadata json: {OUT_META}")

    df = pd.read_csv(
        OUT_CSV,
        dtype={"survey_round": str, "baseline_ai_tercile": str},
    )
    if list(df.columns) != EXP_COLS:
        fail(f"column order mismatch: {list(df.columns)}")
    if df.empty:
        fail("output csv is empty")

    if df[["survey_round", "baseline_ai_tercile"]].duplicated().any():
        fail("duplicate survey_round x baseline_ai_tercile rows")

    terciles = set(df["baseline_ai_tercile"].unique())
    if terciles != {"low", "middle", "high"}:
        fail(f"unexpected tercile set: {sorted(terciles)}")

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
            fail(f"non-numeric or missing values in {c}")
        if df[c].map(lambda x: math.isfinite(float(x))).eq(False).any():
            fail(f"non-finite values in {c}")

    if (df["weighted_n"] <= 0).any():
        fail("weighted_n must be > 0")
    if (df["mean_annual_earnings"] <= 0).any():
        fail("mean_annual_earnings must be > 0")

    for c in [
        "occupation_switch_rate",
        "employment_rate",
        "unemployment_rate",
        "nilf_rate",
        "training_participation_rate",
    ]:
        if (df[c] < -1e-9).any() or (df[c] > 1 + 1e-9).any():
            fail(f"{c} out of [0,1] bounds")

    # Round ordering and completeness.
    rounds = sorted(df["survey_round"].astype(int).unique())
    for r in rounds:
        sub = df[df["survey_round"].astype(int) == r]
        if set(sub["baseline_ai_tercile"]) != {"low", "middle", "high"}:
            fail(f"round {r} does not contain low/middle/high terciles")

    meta = json.loads(OUT_META.read_text(encoding="utf-8"))
    if meta.get("ticket") != "T-020":
        fail("metadata ticket must equal T-020")
    if meta.get("output_csv") != "figures/figureA10_nls_longrun.csv":
        fail("metadata output_csv mismatch")
    if int(meta.get("row_count", -1)) != len(df):
        fail("metadata row_count mismatch")

    retained = [int(x) for x in meta.get("retained_rounds", [])]
    if retained != rounds:
        fail("metadata retained_rounds do not match output rounds")

    hashes = meta.get("source_files_sha256", [])
    if not hashes:
        fail("metadata source_files_sha256 missing")
    for h in hashes:
        lp = h.get("local_cache_path")
        exp = h.get("sha256")
        if not lp or not exp:
            fail("incomplete source_files_sha256 entry")
        p = ROOT / lp
        if not p.exists():
            fail(f"cached source file not found: {p}")
        got = sha256_file(p)
        if got != exp:
            fail(f"sha256 mismatch for {p}")

    for file_key, hash_key in [
        ("crosswalk_file", "crosswalk_sha256"),
        ("ai_terciles_file", "ai_terciles_sha256"),
    ]:
        p = ROOT / str(meta.get(file_key, ""))
        if not p.exists():
            fail(f"metadata file missing: {p}")
        got = sha256_file(p)
        if got != meta.get(hash_key):
            fail(f"metadata hash mismatch for {file_key}")

    print("QA OK: figureA10_nls_longrun.csv")


if __name__ == "__main__":
    main()
