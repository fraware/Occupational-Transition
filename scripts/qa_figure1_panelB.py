"""QA for Figure 1 Panel B outputs (T-002). Exit 1 on failure."""

from __future__ import annotations

import sys
import json
import hashlib
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
HEAT = ROOT / "figures" / "figure1_panelB_task_heatmap.csv"
TERC = ROOT / "intermediate" / "ai_relevance_terciles.csv"
EXPO = ROOT / "intermediate" / "occ22_exposure_components.csv"
CROSS_PATH = ROOT / "crosswalks" / "occ22_crosswalk.csv"
META_JSON = ROOT / "intermediate" / "figure1_panelB_run_metadata.json"

EXPO_COLS = [
    "occ22_code",
    "occ22_label",
    "ai_task_index_raw",
    "exposure_pct",
    "onet_analyzing_data_z",
    "onet_processing_information_z",
    "onet_documenting_recording_z",
    "onet_working_with_computers_z",
    "onet_assisting_caring_z",
    "onet_handling_moving_z",
]

Z_COLS = [
    "z_analyzing_data_or_information",
    "z_processing_information",
    "z_documenting_recording_information",
    "z_working_with_computers",
    "z_assisting_and_caring_for_others",
    "z_handling_and_moving_objects",
]


def main() -> int:
    errors: list[str] = []

    h = pd.read_csv(HEAT)
    t = pd.read_csv(TERC)

    if len(h) != 22:
        errors.append(f"heatmap: expected 22 rows, got {len(h)}")
    if len(t) != 22:
        errors.append(f"terciles: expected 22 rows, got {len(t)}")

    exp_cols = ["occupation_group", "occ22_id"] + Z_COLS
    if list(h.columns) != exp_cols:
        errors.append(
            f"heatmap columns must be {exp_cols}, got {list(h.columns)}"
        )

    terc_cols = [
        "occupation_group",
        "occ22_id",
        "ai_task_index",
        "ai_relevance_tercile",
    ]
    if list(t.columns) != terc_cols:
        errors.append(
            f"tercile columns must be {terc_cols}, got {list(t.columns)}"
        )

    for col in Z_COLS:
        if h[col].isna().any():
            errors.append(f"heatmap: NaN in {col}")

    if t["ai_task_index"].isna().any():
        errors.append("terciles: NaN in ai_task_index")

    valid_terc = {"low", "middle", "high"}
    if not set(t["ai_relevance_tercile"].unique()) <= valid_terc:
        u = t["ai_relevance_tercile"].unique()
        errors.append(f"terciles: invalid labels {u}")

    if t["occ22_id"].duplicated().any():
        errors.append("terciles: duplicate occ22_id")

    if h["occ22_id"].duplicated().any():
        errors.append("heatmap: duplicate occ22_id")

    vc = t["ai_relevance_tercile"].value_counts()
    ok_counts = (
        vc.get("low", 0) == 7
        and vc.get("middle", 0) == 7
        and vc.get("high", 0) == 8
    )
    if not ok_counts:
        errors.append(
            "terciles: expected counts low=7 middle=7 high=8, "
            f"got {vc.to_dict()}"
        )

    cx = pd.read_csv(CROSS_PATH)
    pr = cx[cx["source_system"] == "CPS_PRDTOCC1"]
    pr = pr[pr["source_occ_code"].astype(str) != "23"]
    expected_labels = set(pr["occ22_label"].astype(str).unique())
    if set(h["occupation_group"].astype(str)) != expected_labels:
        errors.append(
            "heatmap occupation_group set must match PR-000 occ22 CPS labels"
        )

    if set(t["occupation_group"].astype(str)) != expected_labels:
        errors.append(
            "tercile occupation_group set must match PR-000 occ22 CPS labels"
        )

    if not EXPO.is_file():
        errors.append(f"missing {EXPO}")
    else:
        exp = pd.read_csv(EXPO)
        if list(exp.columns) != EXPO_COLS:
            errors.append(
                f"exposure columns must be {EXPO_COLS}, got {list(exp.columns)}"
            )
        if len(exp) != 22:
            errors.append(f"exposure: expected 22 rows, got {len(exp)}")
        if exp["occ22_code"].duplicated().any():
            errors.append("exposure: duplicate occ22_code")
        for c in ("ai_task_index_raw", "exposure_pct"):
            if exp[c].isna().any():
                errors.append(f"exposure: NaN in {c}")
        if (exp["exposure_pct"] < 0).any() or (exp["exposure_pct"] > 1).any():
            errors.append("exposure: exposure_pct outside [0,1]")

    h_ids = set(h["occ22_id"].astype(int))
    if h_ids != set(range(1, 23)):
        errors.append(f"heatmap occ22_id must be 1..22, got {sorted(h_ids)}")

    def _sha(path: Path) -> str:
        hh = hashlib.sha256()
        with path.open("rb") as f:
            while True:
                b = f.read(1024 * 1024)
                if not b:
                    break
                hh.update(b)
        return hh.hexdigest()

    if not META_JSON.exists():
        errors.append(f"missing metadata json: {META_JSON}")
    else:
        meta = json.loads(META_JSON.read_text(encoding="utf-8"))
        if meta.get("ticket") != "T-002":
            errors.append("metadata ticket must be T-002")
        if (
            meta.get("source_selection_mode")
            != "pinned_vintage_required_by_ticket"
        ):
            errors.append("metadata source_selection_mode mismatch")
        if int(meta.get("row_count_heatmap", -1)) != len(h):
            errors.append("metadata row_count_heatmap mismatch")
        if int(meta.get("row_count_terciles", -1)) != len(t):
            errors.append("metadata row_count_terciles mismatch")
        srcs = meta.get("sources", [])
        if len(srcs) < 2:
            errors.append("metadata sources must include pinned artifacts")
        for s in srcs:
            lp = s.get("local_cache_path")
            exp = s.get("sha256")
            if not lp or not exp:
                errors.append(
                    "metadata source entry missing local_cache_path/sha256"
                )
                continue
            p = ROOT / lp
            if not p.exists():
                errors.append(f"metadata source file not found: {p}")
                continue
            if _sha(p) != exp:
                errors.append(f"metadata source hash mismatch: {p}")
        cross_exp = meta.get("crosswalk_sha256")
        if cross_exp and _sha(CROSS_PATH) != cross_exp:
            errors.append("metadata crosswalk_sha256 mismatch")

    if errors:
        for e in errors:
            print(f"FAIL: {e}", file=sys.stderr)
        return 1
    print(
        "QA OK: figure1_panelB_task_heatmap.csv and "
        "ai_relevance_terciles.csv"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
