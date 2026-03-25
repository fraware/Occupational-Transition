"""JOLTS LABSTAT parsing (no live network)."""

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


def test_load_jt_series_table() -> None:
    rows = load_jt_series_table(SAMPLE_SERIES)
    assert len(rows) == 1
    assert rows[0]["series_id"] == "JTS000000000000000000S"
    assert rows[0]["dataelement_code"] == "JO"


def test_period_to_month() -> None:
    assert period_to_month("2020", "M01") == "2020-01"
    assert period_to_month("2020", "M13") is None


def test_parse_data_line() -> None:
    assert parse_data_line("a\tb\tc\td") == ("a", "b", "c", "d")
    assert parse_data_line("") is None
