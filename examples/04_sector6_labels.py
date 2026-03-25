"""
Example: sector6 labels for JOLTS in-scope rows from ``sector6_crosswalk.csv``
(no network).

Run::

    pip install -e .
    python examples/04_sector6_labels.py
"""

from __future__ import annotations

from pathlib import Path

from occupational_transition.crosswalks import load_sector6_jolts_labels


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    path = root / "crosswalks" / "sector6_crosswalk.csv"
    labels = load_sector6_jolts_labels(path)
    for code in sorted(labels.keys())[:8]:
        print(code, labels[code])
    print(f"... total codes: {len(labels)}")


if __name__ == "__main__":
    main()
