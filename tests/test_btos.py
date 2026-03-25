"""Unit tests for BTOS parsing (no live network)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from occupational_transition.sources.btos import (
    build_btos_ai_trends_national_xx,
    extract_yes_rates,
    parse_collection_start,
    period_ids_with_ai_questions,
)

FIXTURES = Path(__file__).resolve().parent / "fixtures"


def test_parse_collection_start() -> None:
    dt = parse_collection_start("11-SEP-23 12.00.00.000000 AM")
    assert dt.year == 2023
    assert dt.month == 9
    assert dt.day == 11


def test_period_ids_with_ai_questions() -> None:
    rows = [
        {"PERIOD_ID": "31", "QUESTION": "Use artificial intelligence"},
        {"PERIOD_ID": "30", "QUESTION": "Something else"},
    ]
    assert period_ids_with_ai_questions(rows) == {"31"}


def test_extract_yes_rates() -> None:
    payload = {
        "0": {
            "OPTION_TEXT": "AI current",
            "ANSWER": "Yes",
            "ESTIMATE_PERCENTAGE": "12.5",
        },
        "1": {
            "OPTION_TEXT": "AI future",
            "ANSWER": "Yes",
            "ESTIMATE_PERCENTAGE": "25.0",
        },
    }
    cur, fut = extract_yes_rates(payload)
    assert cur == pytest.approx(0.125)
    assert fut == pytest.approx(0.25)


def test_build_btos_ai_trends_mocked_fetch() -> None:
    enc = "utf-8"
    periods = json.loads((FIXTURES / "btos_periods_small.json").read_text(encoding=enc))
    questions = json.loads(
        (FIXTURES / "btos_questions_small.json").read_text(encoding=enc)
    )
    data_31 = json.loads(
        (FIXTURES / "btos_data_period_31.json").read_text(encoding=enc)
    )

    def fake_fetch(url: str) -> str:
        if url.endswith("/periods"):
            return json.dumps(periods)
        if url.endswith("/questions"):
            return json.dumps(questions)
        if "/periods/31/data/" in url:
            return json.dumps(data_31)
        raise AssertionError(f"unexpected URL: {url}")

    result = build_btos_ai_trends_national_xx(
        fake_fetch, sleep_between_periods_s=0.0
    )
    assert len(result.rows) == 1
    assert result.rows[0]["btos_period_id"] == "31"
    assert result.rows[0]["ai_use_current_rate"] == pytest.approx(0.125)
    assert result.rows[0]["ai_use_expected_6m_rate"] == pytest.approx(0.25)
    assert not result.dropped
