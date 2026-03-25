"""Loaders for committed crosswalk CSVs under ``crosswalks/``."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def load_occ22_labels(crosswalk_csv: Path) -> pd.DataFrame:
    """occ22_id and label from CPS_PRDTOCC1 rows (22 civilian groups)."""
    cx = pd.read_csv(crosswalk_csv)
    pr = cx[cx["source_system"] == "CPS_PRDTOCC1"].copy()
    pr = pr[pr["source_occ_code"].astype(str) != "23"]
    pr["occ22_id"] = pr["occ22_id"].astype(int)
    return pr[["occ22_id", "occ22_label", "soc_major_group_code"]].drop_duplicates()


def load_sector6_jolts_labels(sector6_crosswalk_csv: Path) -> dict[str, str]:
    """
    sector6_code -> sector6_label for JOLTS in-scope rows (matches T-008 script).
    """
    df = pd.read_csv(sector6_crosswalk_csv)
    sub = df[
        (df["source_program"] == "JOLTS")
        & (df["is_in_scope"] == 1)
        & (df["sector6_code"].notna())
        & (df["sector6_code"].astype(str).str.len() > 0)
    ]
    out: dict[str, str] = {}
    for _, row in sub.iterrows():
        code = str(row["sector6_code"])
        label = str(row["sector6_label"])
        if code not in out:
            out[code] = label
    return out
