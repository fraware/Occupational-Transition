"""
Example: load occ22 group labels from the committed crosswalk (no network).

Run from repository root::

    pip install -e .
    python examples/02_occ22_from_crosswalk.py
"""

from __future__ import annotations

from pathlib import Path

from occupational_transition.crosswalks import load_occ22_labels


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    cx = root / "crosswalks" / "occ22_crosswalk.csv"
    df = load_occ22_labels(cx)
    print(df.head())
    print(f"rows: {len(df)}")


if __name__ == "__main__":
    main()
