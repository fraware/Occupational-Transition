"""Crosswalk loaders (uses committed crosswalks in repo)."""

from pathlib import Path

from occupational_transition.crosswalks import (
    load_occ22_labels,
    load_sector6_jolts_labels,
)

ROOT = Path(__file__).resolve().parents[1]


def test_load_occ22_labels_smoke() -> None:
    df = load_occ22_labels(ROOT / "crosswalks" / "occ22_crosswalk.csv")
    assert "occ22_id" in df.columns
    assert len(df) >= 22


def test_load_sector6_jolts_labels_smoke() -> None:
    d = load_sector6_jolts_labels(ROOT / "crosswalks" / "sector6_crosswalk.csv")
    assert "MFG" in d
    assert isinstance(d["MFG"], str)
