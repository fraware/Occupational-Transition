"""
Example: build the national BTOS naics2=XX AI use series using the library.

Requires network. Run from repository root::

    pip install -e .
    python examples/01_btos_national.py
"""

from __future__ import annotations

from occupational_transition.http import fetch_text
from occupational_transition.sources.btos import build_btos_ai_trends_national_xx


def main() -> None:
    def ft(url: str) -> str:
        return fetch_text(url, timeout=180.0)

    result = build_btos_ai_trends_national_xx(ft, sleep_between_periods_s=0.25)
    print(f"rows: {len(result.rows)}")
    if result.rows:
        print("first", result.rows[0])
        print("last", result.rows[-1])


if __name__ == "__main__":
    main()
