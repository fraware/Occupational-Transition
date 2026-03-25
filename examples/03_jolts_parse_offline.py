"""
Example: parse a small JOLTS LABSTAT snippet without hitting the network.

Demonstrates ``load_jt_series_table``, ``period_to_month``, and ``parse_data_line``.
For live BLS downloads, use ``jolts.ensure_jt_file`` (see ``sources.jolts``).

Run::

    pip install -e .
    python examples/03_jolts_parse_offline.py
"""

from __future__ import annotations

from occupational_transition.sources.jolts import (
    load_jt_series_table,
    parse_data_line,
    period_to_month,
)

SAMPLE_SERIES = (
    "series_id\tseasonal\tstate_code\tarea_code\tindustry_code\t"
    "dataelement_code\tsizeclass_code\tratelevel_code\n"
    "JTS000000000000000000S\tS\t00\t00000\t300000\tJO\t00\tR\n"
)


def main() -> None:
    rows = load_jt_series_table(SAMPLE_SERIES)
    print("series rows:", len(rows))
    print(rows[0])
    print("month:", period_to_month("2020", "M01"))
    line = "JTS000000000000000000S\t2020\tM01\t3.1"
    print("parsed line:", parse_data_line(line))


if __name__ == "__main__":
    main()
