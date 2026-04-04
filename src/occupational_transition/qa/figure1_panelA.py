"""QA for figures/figure1_panelA_occ_baseline.csv (T-001)."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import pandas as pd

from occupational_transition.paths import repo_root


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            b = f.read(1024 * 1024)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def main() -> int:
    root = repo_root()
    csv_path = root / "figures" / "figure1_panelA_occ_baseline.csv"
    cross_path = root / "crosswalks" / "occ22_crosswalk.csv"
    meta_json = root / "intermediate" / "figure1_panelA_run_metadata.json"

    errors: list[str] = []
    df = pd.read_csv(csv_path)
    if len(df) != 22:
        errors.append(f"expected 22 rows, got {len(df)}")
    cols = {
        "occupation_group",
        "employment",
        "employment_share",
        "median_annual_wage",
    }
    if set(df.columns) != cols:
        errors.append(f"columns must be exactly {cols}, got {set(df.columns)}")

    if df.isnull().any().any():
        errors.append("null values in output")

    s = df["employment_share"].sum()
    if abs(s - 1.0) > 2e-5:
        errors.append(f"employment_share sum {s} not ~1 (tolerance 2e-5)")

    if (df["employment"] < 0).any():
        errors.append("negative employment")

    if not meta_json.exists():
        errors.append(f"missing metadata json: {meta_json}")
    else:
        meta = json.loads(meta_json.read_text(encoding="utf-8"))
        if meta.get("ticket") != "T-001":
            errors.append("metadata ticket must be T-001")
        if meta.get("output_csv") != "figures/figure1_panelA_occ_baseline.csv":
            errors.append("metadata output_csv mismatch")
        if int(meta.get("row_count", -1)) != len(df):
            errors.append("metadata row_count mismatch")
        if meta.get("source_selection_mode") != "pinned_vintage_required_by_ticket":
            errors.append("metadata source_selection_mode mismatch")
        srcs = meta.get("sources", [])
        if not srcs:
            errors.append("metadata sources missing")
        else:
            for s in srcs:
                lp = s.get("local_cache_path")
                exp = s.get("sha256")
                if not lp or not exp:
                    errors.append(
                        "metadata source entry missing local_cache_path/sha256"
                    )
                    continue
                p = root / lp
                if not p.exists():
                    errors.append(f"metadata source file not found: {p}")
                    continue
                if sha256_file(p) != exp:
                    errors.append(f"metadata source hash mismatch: {p}")
        cross_exp = meta.get("crosswalk_sha256")
        if cross_exp and sha256_file(cross_path) != cross_exp:
            errors.append("metadata crosswalk_sha256 mismatch")

    cx = pd.read_csv(cross_path)
    pr = cx[cx["source_system"] == "CPS_PRDTOCC1"]
    pr = pr[pr["source_occ_code"].astype(str) != "23"]
    expected_labels = set(pr["occ22_label"].astype(str).unique())
    got_labels = set(df["occupation_group"].astype(str))
    if expected_labels != got_labels:
        only_exp = expected_labels - got_labels
        only_got = got_labels - expected_labels
        errors.append(
            f"occupation_group must match PR-000 occ22 CPS labels; "
            f"only in crosswalk: {only_exp}; only in output: {only_got}"
        )

    if errors:
        for e in errors:
            print(f"FAIL: {e}", file=sys.stderr)
        return 1
    print("QA OK: figure1_panelA_occ_baseline.csv")
    return 0
